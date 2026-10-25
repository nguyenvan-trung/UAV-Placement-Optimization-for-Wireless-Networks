"""Analyze reoptimized sensitivity runs; fitness ranks only within each config."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml
from scipy.stats import rankdata, spearmanr, wilcoxon

ALGORITHMS={'GA','PSO','WOA','H-PSO-GA','H-WOA-PSO','I-WOA'}
KEYS=['scenario_id','ue_count','distribution','instance_k','run_id']


def holm(values):
    values=np.asarray(values,dtype=float)
    order=np.argsort(values)
    adjusted=np.empty(len(values))
    adjusted[order]=np.minimum(1,np.maximum.accumulate(values[order]*(len(values)-np.arange(len(values)))))
    return adjusted


def paired_test(left,right):
    d=np.asarray(left)-np.asarray(right)
    nonzero=d[d!=0]
    if not len(nonzero):return 1.,0.
    ranks=rankdata(np.abs(nonzero))
    effect=float(np.sum(np.sign(nonzero)*ranks)/ranks.sum())
    return float(wilcoxon(d,zero_method='wilcox',alternative='two-sided',method='auto').pvalue),effect


def analyze(source,config_path,output):
    config=yaml.safe_load(config_path.read_text(encoding='utf-8'))
    df=pd.read_csv(source)
    configs={c['id']:c for c in config['sensitivity']['configurations']}
    required=set(KEYS+['config_id','algorithm','fitness','C','C_snr','C_sinr','E','I',
                       'data_seed','algo_seed','fe_used','purpose','reoptimized','feasible'])
    if required-set(df):raise ValueError(f'Missing columns: {sorted(required-set(df))}')
    df=df[df.purpose=='eval'].copy()
    if df.empty or set(df.config_id)!=set(configs):raise ValueError('Incomplete configurations')
    if df.duplicated(KEYS+['config_id','algorithm']).any():raise ValueError('Duplicate rows')
    for flag in ['reoptimized','feasible']:
        if not df[flag].astype(str).str.lower().isin(['true','1']).all():
            raise ValueError(f'{flag} must be true; no rescoring-only or infeasible runs')
    quality=['fitness','C','C_snr','C_sinr','E','I']
    if not np.isfinite(df[quality].to_numpy()).all():raise ValueError('Nonfinite metrics')
    if ((df[['C','C_snr','C_sinr','E','I']]<0)|(df[['C','C_snr','C_sinr','E','I']]>1)).any().any():
        raise ValueError('Metrics outside [0,1]')
    for _,g in df.groupby(KEYS):
        if len(g)!=len(configs)*len(ALGORITHMS):raise ValueError('Incomplete paired run')
        if any(set(part.algorithm)!=ALGORITHMS for _,part in g.groupby('config_id')):
            raise ValueError('Missing algorithms')
        if any(g[c].nunique()!=1 for c in ['data_seed','algo_seed','fe_used']):
            raise ValueError('Unpaired seeds or unequal FE')
    for name,cfg in configs.items():
        part=df[df.config_id==name]
        c=part.C_snr if cfg['coverage_quantity']=='SNR' else part.C_sinr
        w=cfg['weights']
        if not np.allclose(part.C,c) or not np.allclose(part.fitness,w['C']*c-w['E']*part.E-w['I']*part.I):
            raise ValueError(f'Fitness mismatch: {name}')
    output.mkdir(parents=True,exist_ok=True)
    ranks=df.groupby(['config_id','algorithm']).fitness.mean().rename('fitness_mean').reset_index()
    ranks['rank']=ranks.groupby('config_id').fitness_mean.rank(ascending=False,method='average')
    ranks.to_csv(output/'ranks.csv',index=False)
    matrix=ranks.pivot(index='algorithm',columns='config_id',values='rank')
    baseline=config['sensitivity']['baseline_id']
    correlations=[]
    for name in configs:
        value=spearmanr(matrix[baseline],matrix[name]).statistic if matrix[baseline].nunique()>1 and matrix[name].nunique()>1 else np.nan
        correlations.append(dict(config_id=name,spearman=value,rank_changed=bool((matrix[baseline]!=matrix[name]).any())))
    pd.DataFrame(correlations).to_csv(output/'rank_correlations.csv',index=False)
    tests=[]
    for name,g in df.groupby('config_id'):
        instance_keys=KEYS[:-1]
        instance_medians=g.groupby(instance_keys+['algorithm']).fitness.median().reset_index()
        pivot=instance_medians.pivot(index=instance_keys,columns='algorithm',values='fitness')
        for algo in sorted(ALGORITHMS-{'I-WOA'}):
            p,effect=paired_test(pivot['I-WOA'],pivot[algo])
            tests.append(dict(config_id=name,opponent=algo,n_pairs=len(pivot),
                              p_raw=p,rank_biserial=effect,
                              median_difference=float(np.median(pivot['I-WOA']-pivot[algo]))))
    tests=pd.DataFrame(tests)
    tests['p_holm']=holm(tests.p_raw)
    tests.to_csv(output/'paired_tests.csv',index=False)
    medians=df.groupby(['config_id','algorithm'])[['C_snr','C_sinr','E','I']].median().reset_index()
    medians.to_csv(output/'metric_medians.csv',index=False)
    diagnostic=df.groupby(['config_id','algorithm']).agg(
        energy_variance=('E',lambda x: x.var(ddof=1)),
        coverage_unique=('C','nunique'),runs=('C','size'),
        saturated_fraction=('C',lambda x: (x>=config['statistics']['coverage_saturation_threshold']).mean())).reset_index()
    diagnostic['energy_near_constant']=diagnostic.energy_variance<config['statistics']['near_constant_energy_variance']
    diagnostic.to_csv(output/'diagnostics.csv',index=False)
    for cost in ['E','I']:
        fig,ax=plt.subplots()
        for algo,g in medians.groupby('algorithm'):
            ax.scatter(g[cost],g.C_snr,label=algo)
            for _,r in g.iterrows():ax.annotate(r.config_id,(r[cost],r.C_snr),fontsize=6)
        ax.set(xlabel=cost+' (minimize)',ylabel='C_snr (maximize)',title='Median trade-offs; not a Pareto frontier')
        ax.legend(fontsize=7);fig.tight_layout();fig.savefig(output/f'tradeoff_C_{cost}.png',dpi=150);plt.close(fig)
    changed=[r['config_id'] for r in correlations if r['rank_changed']]
    text='# Sensitivity analysis\n\nRanks use mean fitness within each configuration only.\n'
    text+=f'Configurations with changed ranks versus {baseline}: {changed}.\n\n'
    text+=matrix.to_markdown()+'\n\n'
    text+='All-tie ranks have undefined Spearman (NaN), not zero stability.\n'
    text+='Positive rank-biserial favors I-WOA; Holm family includes all config/opponent tests.\n'
    text+='Pairs are matched by scenario/instance/run; inference pooling heterogeneous scenarios requires caution.\n'
    text+='Inspect diagnostics.csv for saturation and near-constant E; final-solution variance does not prove a globally flat objective.\n'
    text+='SINR variant retains I and reflects interference twice by design; C_snr is used for common trade-off axes.\n'
    text+='The reoptimized flag is required but provenance must also be verified from runner logs and the seed manifest.\n'
    (output/'analysis.md').write_text(text,encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('runs',type=Path)
    parser.add_argument('--config',type=Path,default=Path('configs/sensitivity.yaml'))
    parser.add_argument('--output',type=Path,default=Path('reports/sensitivity'))
    args=parser.parse_args()
    analyze(args.runs,args.config,args.output)
