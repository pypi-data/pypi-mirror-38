from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

from pypairs import sandbag, cyclone, helper


def sandbag_from_file(genecounts_file, annotation_file, sep_genecounts=",", sep_annotation=",",
                      annotation_fields=(0, 1), dtype=np.float32, index_col="Unnamed: 0", random_subset=None,
                      fraction=0.5, rm_zeros=True, subset_genes=None, subset_samples=None,
                      filter_genes_dispersion=False, always_keep_genes=None, min_diff=0, processes=1):
    gencounts = None

    try:
        gencounts = pd.read_csv(Path(genecounts_file), sep=sep_genecounts)
    except FileNotFoundError:
        helper.print_info("E", "File not found: {}".format(genecounts_file), "sandbag")
        exit(1)

    try:
        gencounts.set_index(index_col, inplace=True)
    except KeyError:
        helper.print_info("E", "Index column not found {}".format(index_col), "sandbag")
        exit(1)

    matrix = np.array(gencounts.values, dtype=dtype)

    annotation = defaultdict(list)

    try:
        for line in open(annotation_file, "r"):
            line = line.replace("\n", "").replace("\r", "")
            infos = line.split(sep_annotation)
            annotation[infos[annotation_fields[1]]].append(infos[annotation_fields[0]])
    except FileNotFoundError:
        helper.print_info("E", "File not found: {}".format(genecounts_file), "sandbag")
        exit(1)

    if random_subset is not None:
        for cat, samples in annotation.items():
            annotation[cat] = helper.random_subset(samples, random_subset)

    return sandbag.sandbag(
        matrix, categories=annotation,
        gene_names=list(gencounts.index), sample_names=list(gencounts.columns),
        rm_zeros=rm_zeros, fraction=fraction, processes=processes, filter_genes_dispersion=filter_genes_dispersion,
        always_keep_genes=always_keep_genes, subset_samples=subset_samples, subset_genes=subset_genes, min_diff=min_diff
    )


def cyclone_from_file(gencounts_file, marker_pairs, sep_genecounts=",", index_col="Unnamed: 0", dtype=np.float32,
                      subset_genes=None, subset_samples=None, iterations=1000, min_iter=100, min_pairs=50,
                      rm_zeros=True, processes=1):
    gencounts = None

    try:
        gencounts = pd.read_csv(Path(gencounts_file), sep=sep_genecounts)
    except FileNotFoundError:
        helper.print_info("E", "File not found: {}".format(gencounts_file), "sandbag")
        exit(1)

    try:
        gencounts.set_index(index_col, inplace=True)
    except KeyError:
        helper.print_info("E", "Index column not found {}".format(index_col), "sandbag")
        exit(1)

    matrix = np.array(gencounts.values, dtype=dtype)

    return cyclone.cyclone(matrix, marker_pairs, gene_names=list(gencounts.index),
                           sample_names=list(gencounts.columns), rm_zeros=rm_zeros, min_pairs=min_pairs,
                           min_iter=min_iter, iterations=iterations, subset_genes=subset_genes,
                           subset_samples=subset_samples, processes=processes)
