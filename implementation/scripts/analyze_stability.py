"""Aggregate actual FE benchmark CSVs; never invent or impute missing runs."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

ALGORITHMS={'GA','PSO','WOA','H-PSO-GA','H-WOA-PSO','I-WOA'}
PAIRS=['scenario_id','ue_count','distribution','instance_k','run_id']


def analyze(source,destination):
    df=pd.read_csv(source)
    required=set(PAIRS+['algorithm','fitness','C','E','I','ue_pass','ue_total','fe_used',
                       'hit_target','feasible','data_seed','algo_seed','purpose'])
    missing=required-set(df.columns)
    if missing:raise ValueError(f'Missing CSV columns: {sorted(missing)}')
    df=df[df.purpose=='eval'].copy()
    if df.empty:raise ValueError('No evaluation rows')
    keys=PAIRS+['algorithm']
    if df.duplicated(keys).any():raise ValueError('Duplicate run identifiers')
    for _,group in df.groupby(PAIRS):
        if set(group.algorithm)!=ALGORITHMS:raise ValueError('Incomplete paired algorithm set')
        for column in ['data_seed','algo_seed','fe_used']:
            if group[column].nunique()!=1:raise ValueError(f'Unpaired {column}')
    if not np.isfinite(df[['fitness','C','E','I']].to_numpy()).all():
        raise ValueError('Nonfinite quality metrics; inspect failed runs before analysis')
    for column in ['hit_target','feasible']:
        original=df[column]
        parsed=original.astype(str).str.lower().map({'true':True,'false':False,'1':True,'0':False})
        if (parsed.isna() & original.notna()).any() or (column=='feasible' and parsed.isna().any()):
            raise ValueError(f'Invalid Boolean: {column}')
        df[column]=parsed
    if not df.feasible.all():raise ValueError('Infeasible runs: audit before ranking')
    if ((df.ue_total<=0)|(df.ue_total!=df.ue_count)|(df.ue_pass<0)|(df.ue_pass>df.ue_total)).any():
        raise ValueError('Invalid UE counts')
    if not np.allclose(df.C,df.ue_pass/df.ue_total):raise ValueError('Coverage does not match UE counts')
    destination.mkdir(parents=True,exist_ok=True)
    summary=df.groupby(['ue_count','distribution','algorithm']).agg(
        fitness_mean=('fitness','mean'),fitness_median=('fitness','median'),
        fitness_best=('fitness','max'),fitness_std=('fitness','std'),
        C_mean=('C','mean'),E_mean=('E','mean'),I_mean=('I','mean'),
        hit_rate=('hit_target','mean'),runs=('fitness','size'),
        ue_pass_sum=('ue_pass','sum'),ue_total_sum=('ue_total','sum')).reset_index()
    summary['coverage_pooled']=summary.ue_pass_sum/summary.ue_total_sum
    summary.to_csv(destination/'stability_summary.csv',index=False)
    for axis in ['ue_count','distribution']:
        # Equal weight per scenario/instance/run, not rank of the single best run.
        rank=df.groupby([axis,'algorithm']).fitness.mean().rename('fitness_mean').reset_index()
        rank['rank']=rank.groupby(axis).fitness_mean.rank(ascending=False,method='min')
        rank.to_csv(destination/f'ranks_by_{axis}.csv',index=False)
    pivot=df.pivot(index=PAIRS,columns='algorithm',values='fitness')
    losses=pivot[pivot['I-WOA']<pivot.max(axis=1)].copy()
    losses['best_algorithm']=losses[list(ALGORITHMS)].idxmax(axis=1)
    losses['gap_to_best']=losses[list(ALGORITHMS)].max(axis=1)-losses['I-WOA']
    losses.to_csv(destination/'iwoa_not_first.csv')
    (destination/'README.md').write_text(
        '# Stability analysis\n\nGenerated only from evaluation rows in the supplied runs.csv.\n'
        'C_mean averages per-run coverage; coverage_pooled sums UE passes and totals across runs.\n'
        'Ranks use mean fitness; ties share rank. No missing runs are imputed.\n'
        'iwoa_not_first lists strictly lower I-WOA fitness; ties are not losses.\n'
        'Possible causes (unverified): FE spent on OBL/Levy; clustered initialization; dimension.\n'
        'Test using paired ablation under the same FE budget before attributing causes.\n'
        'Completeness against the preregistered seed manifest must be checked by the benchmark runner.\n',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('runs',type=Path)
    parser.add_argument('--output',type=Path,default=Path('reports/stability'))
    args=parser.parse_args()
    analyze(args.runs,args.output)
