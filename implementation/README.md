# Implementation

ThÆ° má»¥c nÃ y chá»©a mÃ£ nguá»“n cháº¡y mÃ´ phá»ng. Má»—i nhÃ³m trÃ¡ch nhiá»‡m cÃ³ má»™t vá»‹ trÃ­
riÃªng Ä‘á»ƒ dá»… tÃ¬m, kiá»ƒm thá»­ vÃ  thay tháº¿ mÃ  khÃ´ng trá»™n láº«n dá»¯ liá»‡u vá»›i mÃ£ nguá»“n.

## Cáº¥u trÃºc Ä‘á» xuáº¥t

```text
implementation/
â”œâ”€â”€ scripts/                         # CÃ¡c lá»‡nh cháº¡y tá»« terminal
â”‚   â”œâ”€â”€ generate_dataset.py          # Chá»‰ sinh CSV vÃ  áº£nh quan sÃ¡t
â”‚   â”œâ”€â”€ run_optimizer.py             # Chá»‰ cháº¡y má»™t thuáº­t toÃ¡n hoáº·c táº¥t cáº£
â”‚   â”œâ”€â”€ run_experiments.py           # Cháº¡y nhiá»u seed Ä‘á»ƒ so sÃ¡nh
â”‚   â””â”€â”€ README.md                    # Khi nÃ o dÃ¹ng tá»«ng script
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ constants/                   # Háº±ng sá»‘ há»‡ thá»‘ng vÃ  Ä‘Æ°á»ng dáº«n
â”‚   â”œâ”€â”€ data_generation/             # Logic sinh dá»¯ liá»‡u mÃ´ phá»ng
â”‚   â”œâ”€â”€ input/                       # Äá»c CSV, kiá»ƒm tra schema, chuáº©n hÃ³a Ä‘áº§u vÃ o
â”‚   â”œâ”€â”€ preprocessing/               # K-Means vÃ  cÃ¡c bÆ°á»›c táº¡o Ä‘iá»ƒm khá»Ÿi táº¡o
â”‚   â”œâ”€â”€ models/                      # User, UAV, nghiá»‡m vÃ  cÃ¡c kiá»ƒu dá»¯ liá»‡u miá»n
â”‚   â”œâ”€â”€ physics/                     # Khoáº£ng cÃ¡ch, gÃ³c, LoS, pathloss, SNR
â”‚   â”œâ”€â”€ objectives/                  # Coverage, energy, interference, fitness
â”‚   â”œâ”€â”€ problem/                     # BiÃªn, rÃ ng buá»™c vÃ  bÃ i toÃ¡n tá»‘i Æ°u
â”‚   â”œâ”€â”€ optimization/                # Äiá»u phá»‘i pipeline tá»‘i Æ°u
â”‚   â”œâ”€â”€ algorithms/                  # GA, PSO, WOA vÃ  I-WOA
â”‚   â”œâ”€â”€ evaluation/                  # Metric, Monte Carlo, kiá»ƒm Ä‘á»‹nh thá»‘ng kÃª
â”‚   â””â”€â”€ visualization/               # Báº£ng, biá»ƒu Ä‘á»“ vÃ  áº£nh quan sÃ¡t
â”œâ”€â”€ notebooks/                       # Äá»c results vÃ  phÃ¢n tÃ­ch/trÃ¬nh bÃ y
â”œâ”€â”€ results/                         # Chá»‰ chá»©a káº¿t quáº£ sinh ra, khÃ´ng chá»©a code
â””â”€â”€ datasets/README.md               # TÃ i liá»‡u vá» data/stores vÃ  data/views
```

## Dá»¯ liá»‡u vÃ  káº¿t quáº£

```text
data/
â”œâ”€â”€ raw/                             # Dá»¯ liá»‡u gá»‘c bÃªn ngoÃ i hoáº·c chÆ°a xá»­ lÃ½
â”œâ”€â”€ stores/                          # CSV Ä‘áº§u vÃ o chÃ­nh thá»©c cho thuáº­t toÃ¡n
â””â”€â”€ views/                           # top/front/side/3d cá»§a tá»«ng CSV

implementation/results/
â”œâ”€â”€ tables/                          # CSV/JSON metric vÃ  thá»‘ng kÃª
â”œâ”€â”€ figures/                         # Biá»ƒu Ä‘á»“ há»™i tá»¥, coverage, energy
â”œâ”€â”€ solutions/                       # Vá»‹ trÃ­ UAV tá»‘t nháº¥t vÃ  metadata
â””â”€â”€ logs/                            # Log cá»§a cÃ¡c láº§n cháº¡y
```

`data/stores` lÃ  dá»¯ liá»‡u Ä‘áº§u vÃ o cÃ³ thá»ƒ tÃ¡i sá»­ dá»¥ng. `implementation/results`
lÃ  Ä‘áº§u ra cá»§a thuáº­t toÃ¡n; khÃ´ng ghi káº¿t quáº£ ngÆ°á»£c vÃ o `data/stores`.

## Quy Æ°á»›c trÃ¡ch nhiá»‡m

| CÃ¢u há»i | NÆ¡i cáº§n tÃ¬m |
| --- | --- |
| Sinh thÃªm bá»™ CSV á»Ÿ Ä‘Ã¢u? | `scripts/generate_dataset.py` vÃ  `src/data_generation/` |
| CSV cÃ³ Ä‘Ãºng schema khÃ´ng? | `src/input/` |
| K-Means Ä‘áº·t UAV ban Ä‘áº§u á»Ÿ Ä‘Ã¢u? | `src/preprocessing/` |
| CÃ´ng thá»©c kÃªnh truyá»n á»Ÿ Ä‘Ã¢u? | `src/physics/` |
| CÃ´ng thá»©c fitness á»Ÿ Ä‘Ã¢u? | `src/objectives/` |
| RÃ ng buá»™c vá»‹ trÃ­ vÃ  Ä‘á»™ cao á»Ÿ Ä‘Ã¢u? | `src/problem/` |
| Thuáº­t toÃ¡n GA/PSO/WOA/I-WOA á»Ÿ Ä‘Ã¢u? | `src/algorithms/` |
| Cháº¡y mÃ´ phá»ng á»Ÿ Ä‘Ã¢u? | `scripts/run_optimizer.py` |
| So sÃ¡nh 30 Monte Carlo runs á»Ÿ Ä‘Ã¢u? | `src/evaluation/` |
| Xem biá»ƒu Ä‘á»“ hoáº·c báº£ng káº¿t quáº£ á»Ÿ Ä‘Ã¢u? | `results/` vÃ  `notebooks/` |

Chi tiáº¿t cÃ´ng thá»©c vÃ  nÆ¡i triá»ƒn khai Ä‘Æ°á»£c ghi trong
[docs/formulas.md](docs/formulas.md). File nÃ y lÃ  báº£n Ä‘á»“ thiáº¿t káº¿; khÃ´ng thay
tháº¿ viá»‡c kiá»ƒm tra mÃ£ nguá»“n thá»±c táº¿.

## CÃ¡ch cháº¡y

Sinh láº¡i CSV vÃ  áº£nh:

```powershell
cd implementation
python scripts/generate_dataset.py
```

Cháº¡y thuáº­t toÃ¡n trÃªn má»™t bá»™ dá»¯ liá»‡u:

```powershell
python scripts/run_optimizer.py `
  --algorithm all `
  --dataset ../data/stores/001_UAV_3D_50_users_connect.csv
```

Cháº¡y nhiá»u seed:

```powershell
python scripts/run_experiments.py
```

PhÃ¢n tÃ­ch káº¿t quáº£ sau khi cháº¡y:

```powershell
jupyter notebook notebooks/comparison_experiment.ipynb
```

CÃ¡c module thuáº­t toÃ¡n hiá»‡n váº«n lÃ  scaffold á»Ÿ nhá»¯ng pháº§n chÆ°a triá»ƒn khai.
KhÃ´ng coi má»™t thÆ° má»¥c lÃ  Ä‘Ã£ cÃ³ chá»©c nÄƒng chá»‰ vÃ¬ nÃ³ Ä‘Ã£ Ä‘Æ°á»£c táº¡o sáºµn.


