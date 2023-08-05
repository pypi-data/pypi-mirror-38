#!/usr/bin/env python
# Copyright (C) 2018 Emanuel Goncalves

import os
import gdsc
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pybedtools import BedTool
from qc_plot import QCplot
from scipy.stats import ttest_ind


def sv_cn_aligned(brass, ascat, offset=1e5, svtypes=None):
    svtypes = ['tandem-duplication', 'deletion'] if svtypes is None else svtypes

    sv_aligned = []

    for sv_chr, sv_start, sv_end, sv in brass[['chr1', 'start1', 'end2', 'svclass']].values:
        for cn_chr, cn_start, cn_end, cn in ascat.values:
            is_in_svtypes = sv in svtypes

            is_same_chr = cn_chr == sv_chr
            is_start_close = cn_start - offset < sv_start < cn_start + offset
            is_end_close = cn_end - offset < sv_end < cn_end + offset

            if is_in_svtypes and is_same_chr and is_start_close and is_end_close:
                alignment = dict(
                    chr=cn_chr,
                    start_cn=cn_start, end_cn=cn_end, cn=cn,
                    start_sv=sv_start, end_sv=sv_end, sv=sv
                )

                sv_aligned.append(alignment)

    sv_aligned = pd.DataFrame(sv_aligned)
    return sv_aligned


if __name__ == '__main__':
    # - Imports
    crispy_beds = gdsc.import_crispy_beds(wgs=True)
    brass_bedpes = gdsc.import_brass_bedpes(samples=gdsc.BRCA_SAMPLES)
    ascat_beds = gdsc.get_copy_number_segments_wgs(as_dict=True, samples=gdsc.BRCA_SAMPLES)

    # -
    crispr_beds = {
        c: BedTool(
            crispy_beds[c][['chr', 'start', 'end', 'fold_change', 'ratio']].to_string(index=False, header=False),
            from_string=True
        ).sort() for c in crispy_beds
    }

    # -
    sv_df, ratio_df = [], []
    for dist_offset in [1e3, 1e4, 1e5]:
        for c in brass_bedpes:
            svs = sv_cn_aligned(brass_bedpes[c], ascat_beds[c], offset=dist_offset)

            if svs.shape[0] != 0:
                names = ['chr', 'start_sv', 'end_sv', 'start_cn', 'end_cn', 'cn', 'sv']
                svs_bed = BedTool(svs[names].to_string(index=False, header=False), from_string=True).sort()

                svs_sgrnas = svs_bed.map(crispr_beds[c], c='4', o='mean,count') \
                    .to_dataframe(names=names + ['fc_mean', 'fc_count'])

                ratios_sgrnas = svs_bed.map(crispr_beds[c], c='5', o='mean,count') \
                    .to_dataframe(names=names + ['ratio_mean', 'ratio_count'])

                sv_align = pd.concat([
                    svs_sgrnas.set_index(names),
                    ratios_sgrnas.set_index(names)
                ], axis=1)

                sv_df.append(
                    sv_align\
                        .reset_index()\
                        .assign(sample=c)\
                        .assign(offset=dist_offset)
                )

    sv_df = pd.concat(sv_df).query("fc_mean != '.'").reset_index(drop=True)

    sv_df['fc_mean'] = sv_df['fc_mean'].astype(float).values
    sv_df['fc_count'] = sv_df['fc_count'].astype(int).values

    sv_df['ratio_mean'] = sv_df['ratio_mean'].astype(float).values
    sv_df['ratio_count'] = sv_df['ratio_count'].astype(int).values

    # -
    for dist_offset in [1e3, 1e4, 1e5]:
        plot_df = sv_df.query(f'(fc_count > 10) & (offset == {dist_offset})')

        for y_var in ['fc_mean', 'ratio_mean']:
            t_stat, pval = ttest_ind(
                plot_df.query("sv == 'deletion'")[y_var],
                plot_df.query("sv == 'tandem-duplication'")[y_var],
                equal_var=False
            )

            order = ['deletion', 'tandem-duplication']

            ax = QCplot.bias_boxplot(plot_df, 'sv', y_var, notch=False, add_n=True, tick_base=.2)

            ax.axhline(0, ls='-', color='black', lw=.1, zorder=0, alpha=.5)

            for i in ax.get_xticklabels():
                i.set_rotation(30)
                i.set_horizontalalignment("right")

            ax.set_xlabel('')
            ax.set_ylabel('CRISPR-Cas9 fold-change' if y_var == 'fc_mean' else 'Copy-number ratio')

            ax.set_title(f"Welch's t-test\np-value={pval:.1e}")

            plt.gcf().set_size_inches(1, 2)
            plt.savefig(f'reports/gdsc/wgs/svs_{y_var}_boxplot_{dist_offset:.1e}.pdf', bbox_inches='tight', transparent=True)
            plt.close('all')
