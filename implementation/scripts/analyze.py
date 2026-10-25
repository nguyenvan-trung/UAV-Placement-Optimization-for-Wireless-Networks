"""Instance-level inference from real benchmark logs; no optimizer execution."""
import argparse
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import binomtest, friedmanchisquare, rankdata, studentized_range, wilcoxon

ALGORITHMS=['GA','PSO','WOA','H-PSO-GA','H-WOA-PSO','I-WOA']
INSTANCE=['scenario_id','ue_count','distribution','instance_k','data_seed']


def holm(p):
    p=np.asarray(p,float); order=np.argsort(p); result=np.empty(len(p))
    result[order]=np.minimum(1,np.maximum.accumulate(p[order]*(len(p)-np.arange(len(p)))))
    return result


def rbc(d):
    d=np.asarray(d); d=d[d!=0]
    if not len(d):return 0.
    ranks=rankdata(abs(d))
    return float(np.sum(np.sign(d)*ranks)/ranks.sum())


def bootstrap(values,statistic,rng,resamples,alpha):
    """Percentile bootstrap, resampling independent instances, not runs."""
    values=np.asarray(values)
    if len(values)<2:return (np.nan,np.nan)
    draws=[statistic(values[rng.integers(0,len(values),len(values))]) for _ in range(resamples)]
    return tuple(float(x) for x in np.quantile(draws,[alpha/2,1-alpha/2]))


def compare(d,rng,resamples=2000,alpha=.05):
    d=np.asarray(d,float); nonzero=d[d!=0]
    ties=len(nonzero)-len(np.unique(abs(nonzero)))
    n=len(d)
    if not len(nonzero):
        method,p,reason='all_equal',1.,'All paired differences are zero'
    elif len(nonzero)<10 or ties/len(nonzero)>.25:
        method='exact_sign'
        p=float(binomtest(int((nonzero>0).sum()),len(nonzero),.5).pvalue)
        reason='Predeclared fallback: fewer than 10 nonzero pairs or >25% tied absolute differences; sign test needs no symmetry'
    else:
        method='wilcoxon_signed_rank'
        p=float(wilcoxon(d,zero_method='wilcox',alternative='two-sided',method='auto').pvalue)
        reason='Assumes independent instance differences and symmetric difference distribution; symmetry not certified automatically'
    low,high=bootstrap(d,np.median,rng,resamples,alpha)
    elow,ehigh=bootstrap(d,rbc,rng,resamples,alpha)
    return dict(n_pairs=n,n_nonzero=len(nonzero),n_zeros=n-len(nonzero),ties_abs=ties,
                median_difference=float(np.median(d)),difference_ci_low=low,difference_ci_high=high,
                effect_rbc=rbc(d),effect_ci_low=elow,effect_ci_high=ehigh,
                p_raw=p,method=method,condition_note=reason)


def export(df,folder,name,caption):
    df.to_csv(folder/f'{name}.csv',index=False)
    (folder/f'{name}.md').write_text(caption+'\n\n'+df.to_markdown(index=False)+'\n',encoding='utf-8')
    (folder/f'{name}.tex').write_text(df.to_latex(index=False,escape=True,caption=caption),encoding='utf-8')


def analyze(source,output,resamples=2000,seed=20261024,alpha=.05,expected_runs=30):
    if resamples<100 or not 0<alpha<1 or expected_runs<1:raise ValueError('Invalid analysis parameters')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Use an empty output directory to avoid mixing stale statistical results')
    df=pd.read_csv(source)
    required=set(INSTANCE+['run_id','algo_seed','algorithm','fitness','wall_time_s','cpu_time_s',
                          'fe_used','batch_wall_time_s','batch_total_cpu_s','n_workers','purpose','feasible','batch_id'])
    if required-set(df):raise ValueError(f'Missing columns: {sorted(required-set(df))}')
    if 'config_id' in df and df.config_id.nunique()!=1:
        raise ValueError('Analyze one fitness configuration at a time; do not pool different weight sets')
    if df[list(required)].isna().any().any():raise ValueError('Missing required values')
    if set(df.purpose)-{'tuning','eval'}:raise ValueError('Unknown seed purpose')
    tuning=df[df.purpose=='tuning']; evaluation=df[df.purpose=='eval']
    for col in ['data_seed','algo_seed']:
        if set(tuning[col])&set(evaluation[col]):raise ValueError(f'Tuning/eval overlap: {col}')
    df=evaluation.copy()
    if df.empty:raise ValueError('No evaluation data')
    if not df.feasible.astype(str).str.lower().isin(['true','1']).all():
        raise ValueError('Infeasible runs must be audited; do not silently drop them')
    if not np.isfinite(df[['fitness','wall_time_s','cpu_time_s','fe_used']].to_numpy()).all():raise ValueError('Nonfinite metrics')
    if (df.wall_time_s<=0).any() or (df.cpu_time_s<0).any() or (df.fe_used<=0).any():raise ValueError('Invalid performance values')
    ids=INSTANCE+['run_id']
    if df.duplicated(ids+['algorithm']).any():raise ValueError('Duplicate observations')
    for _,g in df.groupby(ids):
        if set(g.algorithm)!=set(ALGORITHMS):raise ValueError('Incomplete paired algorithm set')
        if g.algo_seed.nunique()!=1 or g.fe_used.nunique()!=1:raise ValueError('Seeds/FE not matched')
    counts=df.groupby(INSTANCE+['algorithm']).run_id.nunique()
    if not (counts==expected_runs).all():raise ValueError('Run count differs from preregistered expected_runs')
    # Prevent the same UE instance appearing under multiple identifiers.
    if (df.groupby(['ue_count','distribution','data_seed']).scenario_id.nunique()>1).any():
        raise ValueError('Repeated instance under multiple scenario IDs')
    output.mkdir(parents=True,exist_ok=True)
    rng=np.random.default_rng(seed)
    med=df.groupby(INSTANCE+['algorithm'],sort=True).fitness.median().rename('instance_median').reset_index()
    pivot=med.pivot(index=INSTANCE,columns='algorithm',values='instance_median')[ALGORITHMS]
    if pivot.isna().any().any():raise ValueError('Missing instance pairs')
    export(med,output,'instance_medians','Fitness maximize; median across runs within each independent instance; unitless')
    descriptions=[]
    for algo in ALGORITHMS:
        raw=df[df.algorithm==algo].fitness
        x=pivot[algo].to_numpy()
        lo,hi=bootstrap(x,np.mean,rng,resamples,alpha)
        descriptions.append(dict(algorithm=algo,n_runs=len(raw),n_instances=len(x),
            run_mean=raw.mean(),run_median=raw.median(),run_best=raw.max(),run_std=raw.std(ddof=1),
            run_iqr=raw.quantile(.75)-raw.quantile(.25),instance_mean=x.mean(),
            instance_mean_ci_low=lo,instance_mean_ci_high=hi))
    caption=f'Fitness maximize, unitless; CI {100*(1-alpha):g}% percentile bootstrap of mean instance medians; B={resamples}, seed={seed}'
    export(pd.DataFrame(descriptions),output,'descriptive',caption)
    tests=[]
    for algo in ALGORITHMS[:-1]:
        row=compare((pivot['I-WOA']-pivot[algo]).to_numpy(),rng,resamples,alpha)
        row.update(opponent=algo,alpha=alpha);tests.append(row)
    tests=pd.DataFrame(tests);tests['p_holm']=holm(tests.p_raw)
    tests['conclusion']=[('thắng' if e>0 else 'thua') if p<alpha and e!=0 else 'hòa (chưa đủ bằng chứng khác biệt)'
                          for p,e in zip(tests.p_holm,tests.effect_rbc)]
    export(tests,output,'paired_comparisons',caption+'; I-WOA minus opponent; paired rank-biserial positive favors I-WOA; Holm across all opponents')
    ranks=np.array([rankdata(-row,method='average') for row in pivot.to_numpy()])
    means=ranks.mean(axis=0);n,k=ranks.shape
    all_tied=bool(np.all(np.ptp(pivot.to_numpy(),axis=1)==0))
    if n<10:
        omnibus=dict(method='Friedman not run',n_instances=n,p_value=np.nan,statistic=np.nan,reason='Predeclared minimum 10 independent blocks for asymptotic omnibus')
    elif all_tied:
        omnibus=dict(method='all_equal',n_instances=n,p_value=1.,statistic=0.,reason='All algorithms tied within every instance')
    else:
        stat,p=friedmanchisquare(*(pivot[a] for a in ALGORITHMS))
        omnibus=dict(method='Friedman',n_instances=n,p_value=p,statistic=stat,reason='Independent instance blocks; tied ranks corrected by scipy')
    export(pd.DataFrame([omnibus]),output,'omnibus','Fitness maximize; alpha='+str(alpha)+'; omnibus only, see paired effect/CI tables')
    export(pd.DataFrame(dict(algorithm=ALGORITHMS,mean_rank=means,n_instances=n)),output,'overall_ranks','Lower mean rank is better; ranks from instance median Fitness (maximize)')
    if n>=10 and not all_tied and omnibus['p_value']<alpha:
        scale=np.sqrt(k*(k+1)/(6*n))
        cd=float(studentized_range.ppf(1-alpha,k,np.inf)/np.sqrt(2)*scale)
        nemenyi=[]
        for i in range(k):
            for j in range(i):
                difference=means[i]-means[j]
                nemenyi.append(dict(algorithm_a=ALGORITHMS[i],algorithm_b=ALGORITHMS[j],
                    n_instances=n,rank_difference=difference,critical_difference=cd,
                    p_nemenyi=float(studentized_range.sf(abs(difference)/scale*np.sqrt(2),k,np.inf))))
        export(pd.DataFrame(nemenyi),output,'nemenyi','Nemenyi all-pairs family-adjusted p; asymptotic studentized range; lower rank better')
        fig,ax=plt.subplots(figsize=(9,4))
        order=np.argsort(means)
        ax.scatter(means[order],np.arange(k))
        ax.set_yticks(np.arange(k),[ALGORITHMS[i] for i in order]);ax.set_xlim(.5,k+.5)
        ax.plot([1,1+cd],[k,k],color='black');ax.text(1,k+.1,f'CD={cd:.3g}')
        ax.set(xlabel='Mean rank (lower is better)',title=f'Critical difference scale; n={n}; Nemenyi alpha={alpha}')
        fig.tight_layout()
        for suffix in ['png','pdf']:fig.savefig(output/f'critical_difference.{suffix}')
        plt.close(fig)
    else:
        (output/'posthoc_not_run.md').write_text('Nemenyi/CD not run: insufficient blocks, all ties, or nonsignificant omnibus. No pairwise superiority inferred.\n',encoding='utf-8')
    df['fe_per_wall_s']=df.fe_used/df.wall_time_s
    performance=df.groupby('algorithm').agg(n_runs=('run_id','size'),wall_mean_s=('wall_time_s','mean'),
        wall_median_s=('wall_time_s','median'),cpu_mean_s=('cpu_time_s','mean'),
        fe_mean=('fe_used','mean'),fe_per_wall_s_median=('fe_per_wall_s','median')).reset_index()
    export(performance,output,'performance','Per-run wall/CPU seconds; FE counts; FE per wall second includes optimizer overhead; lower times better')
    columns=['batch_wall_time_s','batch_total_cpu_s','n_workers']
    for _,g in df.groupby('batch_id'):
        if any(g[c].nunique()!=1 for c in columns):raise ValueError('Inconsistent batch metadata')
    batches=df[['batch_id']+columns].drop_duplicates()
    export(batches,output,'batches','Actual batch wall seconds versus total CPU seconds; worker count; never sum repeated per-run batch metadata')
    meta=dict(source=str(source),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
              bootstrap_resamples=resamples,bootstrap_seed=seed,alpha=alpha,expected_runs=expected_runs,
              ci_method='percentile at independent instance level',holm_family='all I-WOA opponent comparisons',
              numpy=np.__version__,pandas=pd.__version__)
    (output/'analysis_metadata.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    (output/'README.md').write_text(
        '# Statistical analysis\n\nAll tables generated from runs.csv; one configuration per invocation.\n'
        'Run summaries are descriptive; inferential unit is the instance median, not the run.\n'
        'Hòa means insufficient evidence of difference, not proof of equivalence.\n'
        'Bootstrap CIs are pointwise, not multiplicity-adjusted simultaneous intervals.\n'
        'Sign fallback tests signs; rank-biserial remains a descriptive signed-rank effect.\n'
        'Wilcoxon symmetry and independence require design/domain review. Scenario dependence is not cured by more runs.\n'
        'Nemenyi is asymptotic; ties reduce rank information. CD figure shows ranks and CD scale, not maximal nonsignificant cliques.\n'
        'Verify complete preregistered scenario/seed manifest externally; balanced CSV alone does not prove complete experiment.\n',encoding='utf-8')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('runs',type=Path)
    parser.add_argument('--output',type=Path,default=Path('reports/statistics'))
    parser.add_argument('--resamples',type=int,default=2000)
    parser.add_argument('--seed',type=int,default=20261024)
    parser.add_argument('--alpha',type=float,default=.05)
    parser.add_argument('--expected-runs',type=int,default=30)
    args=parser.parse_args()
    analyze(args.runs,args.output,args.resamples,args.seed,args.alpha,args.expected_runs)
