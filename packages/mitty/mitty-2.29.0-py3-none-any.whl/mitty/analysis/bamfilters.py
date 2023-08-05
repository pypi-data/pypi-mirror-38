"""
Supplies primitives for streaming (filter based) analysis of BAMs produced from simulated data.
"""
import tempfile
from collections import OrderedDict, Counter
import logging

import cytoolz
import numpy as np
import pysam
import pandas as pd

import xarray as xr

from mitty.benchmarking.alignmentscore import score_alignment_error, correct_tlen, load_qname_sidecar, parse_qname

logger = logging.getLogger(__name__)


@cytoolz.curry
def parse_read_qnames(sidecar_fname, titer):
  """Mutates dictionary: adds 'read_info' field to it.

  :param titer:
  :return:
  """
  long_qname_table = load_qname_sidecar(sidecar_fname) if sidecar_fname is not None else None

  for template in titer:
    ri = parse_qname(
        template[0].qname,
        long_qname_table=long_qname_table
    ) if long_qname_table is not None else [None, None]
    yield tuple(
      {
        'read': mate,
        'read_info': ri[1 if mate.is_read2 else 0]
      }
      for mate in template
    )


@cytoolz.curry
def compute_derr(titer, max_d=200):
  """Mutates dictionary: adds d_err field to it. Requires qname parsing step

  :param max_d:
  :param riter:
  :return:
  """
  for template in titer:
    for mate in template:
      mate['d_err'] = score_alignment_error(r=mate['read'], ri=mate['read_info'], max_d=max_d)
    yield template


@cytoolz.curry
def categorize_reads(f_dict, titer):
  """Fill in cat_list of Reads. Note that there is no loss of reads in this function.
  If a read does not match any filter cat_list is empty, which corresponds to 'uncategorized'
  Mutates read dictionary: adds 'cat_list' field to it. If a 'cat_list' field already exists
  it appends to it.

  :param titer:
  :param f_dict: Dictionary of key: filter_function pairs
                 key will go into cat_list field of read if filter passes

  e.g. f_dict = {
    'd = 0': lambda mate: mate['d_err'] == 0,
    '0 < d <= 50': lambda mate: 0 < mate['d_err'] <= 50,
    '50 < d': lambda mate: 50 < mate['d_err'] < 200,
    'WC': lambda mate: 200 < mate['d_err'],
    'UM': lambda mate: mate['read'].is_unmapped
    }

  :return: iterator
  """
  for template in titer:
    for mate in template:
      mate['cat_list'] = mate.get('cat_list', []) + [k for k, f in f_dict.items() if f(mate)]
    yield template


@cytoolz.curry
def count_reads(titer):
  """The reads need to have gone through `categorize_reads` so that they have the
    'cat_list' field filled out

  :param titer:
  :return: a Counter() object
  """
  c = Counter()
  for template in titer:
    for mate in template:
      for cat in (mate['cat_list'] or ['nocat']):
        c[cat] += 1
  return c


# Data sinks ------------------------------------------------------------------


def simple_sink(riter):
  """This just consumes the reads so that our filter chain is processed. Comes in useful in
  some cases when we just drop the reads off at the end of the pipeline

  :param riter:
  :return:
  """
  for r in riter:
    pass


@cytoolz.curry
def write_bam(fname, header, riter):
  out_fp = pysam.AlignmentFile(fname, 'wb', header=header)
  for r in riter:
    for mate in r:
      out_fp.write(mate['read'])
    yield r


# Filtering operations --------------------------------------------------------


@cytoolz.curry
def filter_reads(f, condition, riter):
  """Filter out reads based on f

  :param f: filter function
  :param condition: is either one of the python functions all or any
                    to indicate if we should accept paired reads only if both the mates pass
                    or if any of the mates pass
  :param riter:
  :return:
  """
  for r in riter:
    # TODO: looks like we don't need 'fpass'
    new_r = tuple(dict(mate, fpass=f(mate) and mate['fpass']) for mate in r)
    if condition(tuple(mate['fpass'] for mate in new_r)):
      yield new_r


# Library of useful filter functions ------------------------------------------


def non_ref():
  """Keep reads with variants

  :return: function that takes mate as input and returns T/F
  """
  return lambda mate: len(mate['read_info'].v_list) > 0


def pure_ref():
  """Keep reads with no variants

  :return: function that takes mate as input and returns T/F
  """
  return lambda mate: len(mate['read_info'].v_list) == 0


def derr(min, max):
  """Keep reads within this limit

  :param min:
  :param max:
  :return:
  """
  return lambda mate: min <= mate['d_err'] <= max


def vsize(min, max):
  """Keep reads with at least one variant falling within given v_range
  Returns False for pure reference reads

  :param min:
  :param max:
  :return:
  """
  return lambda mate: any(min <= v <= max for v in mate['read_info'].v_list)


# Processing tools ------------------------------------------------------------



def zero_dmv(max_d=200, max_MQ=70, max_vlen=200):
  return np.zeros(shape=(2 * max_d + 1 + 2, max_MQ + 1, 2 * max_vlen + 1 + 2), dtype=int)


@cytoolz.curry
def alignment_hist(dmv_mat, riter):
  """Compute the dmv matrix which is as defined as follows:

  A 3D matrix with dimensions:
    Xd - alignment error  [0]  -max_d, ... 0, ... +max_d, wrong_chrom, unmapped (2 * max_d + 1 + 2)
    MQ - mapping quality  [1]  0, ... max_MQ (max_MQ + 1)
    vlen - length of variant carried by read [2]  -max_vlen, ... 0, ... +max_vlen, Ref, Margin, Multiple
                                                  (2 * max_vlen + 1 + 2)



  * The ends of the ranges (-max_d, max_d) (-max_vlen, +max_vlen) include that value and all values exceeding
  * Ref collects all the reference reads
  * Margin collects the marginal sums for d x MQ. This is necessary because one read can appear in multiple
    bins on the vlen axis and cause a slight excess of counts when marginals are computed

  :param dmv_mat:
  :param riter:
  :return: iterator
  """
  max_d = int((dmv_mat.shape[0] - 3) / 2)
  max_MQ = int(dmv_mat.shape[1] - 1)
  max_vlen = int((dmv_mat.shape[2] - 3) / 2)

  for r in riter:
    for mate in r:
      i = max_d + mate['d_err']
      j = min(mate['read'].mapping_quality, max_MQ)
      if mate['read_info'].v_list:
        for v_size in mate['read_info'].v_list:
          k = min(max_vlen, max(0, max_vlen + v_size))
          dmv_mat[i, j, k] += 1
      else:
        k = 2 * max_vlen + 1
        dmv_mat[i, j, k] += 1
      dmv_mat[i, j, -1] += 1  # The exact marginal

    yield r


def tlen_matrix():
  pass


@cytoolz.curry
def to_df(riter, tags=None):
  """This is a terminal, it produces a data frame

  :param riter:
  :param tags:
  :return:
  """
  qname = []
  read_data = [
    OrderedDict(
      [
        ('mate', []),
        ('chrom', []),
        ('pos', []),
        ('cigar', []),
        ('MQ', []),
        ('d_err', []),
        ('correct_chrom', []),
        ('correct_pos', []),
        ('correct_cigar', []),
      ] + [
        (tag, [])
        for tag in tags
      ])
    for _ in [0, 1]
  ]

  for r in riter:
    qname.append(r[0]['read'].qname.split('|')[0])
    for n, mate in enumerate(r):
      rdta = read_data[n]
      rd = mate['read']
      rdta['mate'].append(1 if rd.is_read1 else 2)
      rdta['chrom'].append(rd.reference_name)
      rdta['pos'].append(rd.pos)
      rdta['cigar'].append(rd.cigarstring)
      rdta['MQ'].append(rd.mapping_quality)
      rdta['d_err'].append(mate['d_err'])
      rdta['correct_chrom'].append(mate['read_info'].chrom)
      rdta['correct_pos'].append(mate['read_info'].pos)
      rdta['correct_cigar'].append(mate['read_info'].cigar)
      for tag in tags:
        rdta[tag] = rd.get_tag(tag)

  mates_were_paired = True if len(read_data[1]['mate']) else False
  data = OrderedDict(
    [
      (('qname',) if mates_were_paired else 'qname', qname),
    ] + [
      (('mate1', k) if mates_were_paired else k, v)
      for k, v in read_data[0].items()
    ] + ([
      (('mate2', k), v)
      for k, v in read_data[1].items()
    ] if mates_were_paired else [])
  )

  return pd.DataFrame(data)

