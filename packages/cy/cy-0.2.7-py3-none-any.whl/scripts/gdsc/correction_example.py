#!/usr/bin/env python
# Copyright (C) 2018 Emanuel Goncalves

import gdsc
import numpy as np
import pandas as pd
import crispy as cy
import seaborn as sns
import matplotlib.pyplot as plt
from crispy.qc_plot import QCplot


if __name__ == '__main__':
    # - Samplesheet
    ss = gdsc.get_sample_info()

    # - Non-expressed genes
    nexp = gdsc.get_non_exp()

    # - Crispy bed files
    beds = gdsc.import_crispy_beds()

    # -
    g_ess = set.union(cy.Utils.get_adam_core_essential(), cy.Utils.get_broad_core_essential())

    # - Aggregate by gene
    agg_fun = dict(
        fold_change=np.mean, copy_number=np.mean, ploidy=np.mean, chr_copy=np.mean, ratio=np.mean, chr='first',
        corrected=np.mean
    )

    bed_nexp_gene = []

    for s in beds:
        df = beds[s].groupby('gene').agg(agg_fun)
        df = df.assign(scaled=cy.Crispy.scale_crispr(df['fold_change']))
        df = df.reindex(nexp[nexp[s] == 1].index).dropna()
        df = df.assign(sample=s)

        bed_nexp_gene.append(df)

    bed_nexp_gene = pd.concat(bed_nexp_gene).reset_index()
    bed_nexp_gene = bed_nexp_gene[~bed_nexp_gene['index'].isin(g_ess)]

    bed_nexp_gene = bed_nexp_gene.assign(copy_number_bin=bed_nexp_gene['copy_number'].apply(cy.Utils.bin_cnv, args=(10,)))
    bed_nexp_gene = bed_nexp_gene.assign(ratio_bin=bed_nexp_gene['ratio'].apply(cy.Utils.bin_cnv, args=(4,)))
    bed_nexp_gene = bed_nexp_gene.assign(chr_copy_bin=bed_nexp_gene['chr_copy'].apply(cy.Utils.bin_cnv, args=(6,)))

    # -
    gene = 'NEUROD2'

    plot_df = bed_nexp_gene[bed_nexp_gene['index'] == gene].sort_values('copy_number')
    plot_df['Cancer Type'] = ss.loc[plot_df['sample'], 'Cancer Type'].values

    f, (ax1, ax2) = plt.subplots(1, 2, sharex='none', sharey='row')

    QCplot.bias_boxplot(plot_df, 'copy_number_bin', 'scaled', ax=ax1, tick_base=.5, notch=False, add_n=True)
    ax1.axhline(0, ls='-', color='black', lw=.1, zorder=0, alpha=.5)
    ax1.set_xlabel('Copy-number')
    ax1.set_ylabel('CRISPR-Cas9 fold-change')

    QCplot.bias_boxplot(plot_df, 'ratio_bin', 'scaled', ax=ax2, tick_base=.5, notch=False, add_n=True)
    ax2.axhline(0, ls='-', color='black', lw=.1, zorder=0, alpha=.5)
    ax2.set_xlabel('Copy-number ratio')
    ax2.set_ylabel('')

    plt.suptitle(gene, fontsize=10, y=1.02)

    plt.gcf().set_size_inches(4, 2)
    plt.savefig(f'reports/correction_example.pdf', bbox_inches='tight', transparent=True)
    plt.close('all')
