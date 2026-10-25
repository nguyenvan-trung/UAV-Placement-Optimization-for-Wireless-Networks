"""Create scenario examples and source CSVs; does not run optimizers."""
import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'implementation'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from src.scenarios import NAMES,ScenarioParameters,generate_scenario


def main():
    destination=ROOT/'figures'
    destination.mkdir(exist_ok=True)
    params=ScenarioParameters()
    fig,axes=plt.subplots(1,len(NAMES),figsize=(20,4),sharex=True,sharey=True)
    for ax,name in zip(axes,NAMES):
        df=generate_scenario(name,300,42,params)
        df.to_csv(destination/f'scenario_{name}.csv',index=False)
        ax.scatter(df.x_m,df.y_m,s=6,c=df.is_outlier.map({True:'tab:red',False:'tab:blue'}))
        ax.set(title=name,xlim=(0,1000),ylim=(0,1000),xlabel='x (m)',aspect='equal')
    axes[0].set_ylabel('y (m)')
    fig.tight_layout()
    fig.savefig(destination/'scenarios.png',dpi=160)
    plt.close(fig)
    (destination/'scenarios_metadata.json').write_text(json.dumps(dict(data_seed=42,count=300,
        parameters=asdict(params),purpose='illustration only; not benchmark results'),indent=2),encoding='utf-8')


if __name__=='__main__':main()
