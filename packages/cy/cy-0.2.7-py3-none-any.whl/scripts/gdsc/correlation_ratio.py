#!/usr/bin/env python
# Copyright (C) 2018 Emanuel Goncalves

import gdsc
import numpy as np
import crispy as cy
import pandas as pd
import matplotlib.pyplot as plt
from numpy import corrcoef
from scipy.stats import spearmanr


if __name__ == '__main__':
    # - Non-expressed genes
    nexp = gdsc.get_non_exp()

    # - Crispy bed files
    beds = gdsc.import_crispy_beds()

    # - Add ccleanr gene scores to bed
    ccleanr = gdsc.import_ccleanr()
    beds = {s: beds[s].assign(ccleanr=ccleanr.loc[beds[s]['gene'], s].values) for s in beds}

    # - Aggregate by gene
    agg_fun = dict(
        fold_change=np.mean, copy_number=np.mean, ploidy=np.mean, chr_copy=np.mean, ratio=np.mean, chr='first',
        ccleanr=np.mean, corrected=np.mean
    )

    bed_nexp_gene = []

    for s in beds:
        df = beds[s].groupby('gene').agg(agg_fun)
        df = df.assign(scaled=cy.Crispy.scale_crispr(df['fold_change']))
        df = df.reindex(nexp[nexp[s] == 1].index).dropna()
        df = df.assign(sample=s)

        bed_nexp_gene.append(df)

    bed_nexp_gene = pd.concat(bed_nexp_gene)

    #
    ratio = pd.DataFrame({c: bed_nexp_gene.query(f"sample == '{c}'")['ratio'] for c in beds}).dropna()
    copynumber = pd.DataFrame({c: bed_nexp_gene.query(f"sample == '{c}'")['copy_number'] for c in beds}).dropna()
    foldchange = pd.DataFrame({c: bed_nexp_gene.query(f"sample == '{c}'")['fold_change'] for c in beds}).dropna()

    #
    samples = list(set.intersection(set(ratio.columns), set(copynumber.columns), set(foldchange.columns)))
    genes = list(set.intersection(set(ratio.index), set(copynumber.index), set(foldchange.index)))

    cors = []
    for g in genes:
        cors.append(dict(
            sgrna=g,
            ratio=spearmanr(foldchange.loc[g, samples], ratio.loc[g, samples])[0],
            copynumber=spearmanr(foldchange.loc[g, samples], copynumber.loc[g, samples])[0],
        ))
    cors = pd.DataFrame(cors).dropna()
