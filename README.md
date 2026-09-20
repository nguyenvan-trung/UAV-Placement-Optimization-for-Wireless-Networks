# UAV Placement Optimization for Wireless Networks

Dá»± Ã¡n nghiÃªn cá»©u tá»‘i Æ°u vá»‹ trÃ­ 3D cá»§a cÃ¡c UAV base station trong máº¡ng khÃ´ng
dÃ¢y. Ã tÆ°á»Ÿng, cÃ´ng thá»©c vÃ  má»¥c tiÃªu nghiÃªn cá»©u náº±m trong [NOTE.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/NOTE.md>).
README nÃ y chá»‰ hÆ°á»›ng dáº«n cÃ¡ch tÃ¬m mÃ£ nguá»“n, dá»¯ liá»‡u vÃ  cÃ¡ch cháº¡y.

## 1. Báº£n Ä‘á»“ thÆ° má»¥c

```text
.
â”œâ”€â”€ data/                         # Dá»¯ liá»‡u; giá»¯ Ä‘á»™c láº­p vá»›i mÃ£ nguá»“n
â”‚   â”œâ”€â”€ raw/                      # Dá»¯ liá»‡u gá»‘c náº¿u cÃ³
â”‚   â”œâ”€â”€ stores/                   # CSV Ä‘áº§u vÃ o chÃ­nh thá»©c
â”‚   â””â”€â”€ views/                    # áº¢nh quan sÃ¡t cá»§a tá»«ng CSV
â”œâ”€â”€ documents/                    # BÃ i bÃ¡o vÃ  tÃ i liá»‡u ná»n táº£ng
â”‚   â”œâ”€â”€ GA/
â”‚   â”œâ”€â”€ PSO/
â”‚   â””â”€â”€ WOA/
â”œâ”€â”€ plan/                         # Káº¿ hoáº¡ch, phÃ¢n cÃ´ng vÃ  tiáº¿n Ä‘á»™
â”œâ”€â”€ implementation/               # MÃ£ nguá»“n mÃ´ phá»ng
â”‚   â”œâ”€â”€ scripts/                  # CÃ¡c lá»‡nh cháº¡y tá»« terminal
â”‚   â”œâ”€â”€ src/
â”‚   â”‚   â”œâ”€â”€ constants/            # Tham sá»‘ vÃ  Ä‘Æ°á»ng dáº«n cá»‘ Ä‘á»‹nh
â”‚   â”‚   â”œâ”€â”€ data_generation/      # Sinh dataset
â”‚   â”‚   â”œâ”€â”€ input/                # Äá»c vÃ  kiá»ƒm tra CSV
â”‚   â”‚   â”œâ”€â”€ preprocessing/        # K-Means, khá»Ÿi táº¡o UAV
â”‚   â”‚   â”œâ”€â”€ models/               # Kiá»ƒu dá»¯ liá»‡u miá»n
â”‚   â”‚   â”œâ”€â”€ physics/              # CÃ´ng thá»©c kÃªnh truyá»n
â”‚   â”‚   â”œâ”€â”€ objectives/           # Coverage, energy, interference, fitness
â”‚   â”‚   â”œâ”€â”€ problem/              # BiÃªn vÃ  rÃ ng buá»™c
â”‚   â”‚   â”œâ”€â”€ algorithms/           # GA, PSO, WOA, I-WOA
â”‚   â”‚   â”œâ”€â”€ evaluation/           # Monte Carlo, metric, thá»‘ng kÃª
â”‚   â”‚   â””â”€â”€ visualization/        # Báº£ng vÃ  biá»ƒu Ä‘á»“
â”‚   â”œâ”€â”€ docs/                     # TÃ i liá»‡u ká»¹ thuáº­t cá»§a implementation
â”‚   â”œâ”€â”€ notebooks/                # PhÃ¢n tÃ­ch káº¿t quáº£, khÃ´ng pháº£i entry point
â”‚   â”œâ”€â”€ results/                  # Output sinh bá»Ÿi thÃ­ nghiá»‡m
â”‚   â””â”€â”€ datasets/                  # Chá»‰ tÃ i liá»‡u quy Æ°á»›c dataset
â””â”€â”€ NOTE.md                      # Ã tÆ°á»Ÿng, mÃ´ hÃ¬nh vÃ  Ä‘á»‹nh hÆ°á»›ng nghiÃªn cá»©u
```

Xem [implementation/README.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/README.md>) Ä‘á»ƒ biáº¿t trÃ¡ch nhiá»‡m chi tiáº¿t cá»§a tá»«ng táº§ng.

## 2. Tham sá»‘ máº·c Ä‘á»‹nh hiá»‡n táº¡i

CÃ¡c giÃ¡ trá»‹ nÃ y lÃ  giÃ¡ trá»‹ code Ä‘ang dÃ¹ng, náº±m trong
[network.py](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/constants/network.py>)
vÃ 
[experiment.py](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/constants/experiment.py>).

| NhÃ³m | Tham sá»‘ | GiÃ¡ trá»‹ |
| --- | --- | ---: |
| Khu vá»±c | `area_width_m` | `1000.0 m` |
| Khu vá»±c | `area_height_m` | `1000.0 m` |
| UAV | `min_altitude_m` | `50.0 m` |
| UAV | `max_altitude_m` | `300.0 m` |
| Káº¿t ná»‘i | `coverage_threshold_dbm` | `-90.0 dBm` |
| ThÃ­ nghiá»‡m | `seeds` | `42, 123, 2026` |
| ThÃ­ nghiá»‡m | `population_size` | `30` |
| ThÃ­ nghiá»‡m | `max_iterations` | `100` |

Mặc định bộ sinh tạo **500 CSV**: 10 mức quy mô `50, 100, 150, 200, 250, 300, 350, 400, 450, 500` users, mỗi mức 50 bộ. Vị trí được sinh theo các hotspot, tòa nhà và nền rải thưa, không dùng lưới đều.
CSV cÃ³ schema:
`user_id,x_m,y_m,z_m,demand`.

Trong schema 3D, `z_m=0` la user o mat dat/ngoai troi va `z_m>0` la user
o tang toa nha. Cac anh trong `data/views` co y nghia:
`top.png` (X-Y), `front.png` (X-Z), `side.png` (Y-Z) va `3d.png` (X-Y-Z).
UAV khong duoc tron vao CSV user; toa do UAV `(x,y,z)` la bien toi uu va
duoc luu o ket qua sau khi chay thuat toan.

`NOTE.md` cÃ³ thá»ƒ mÃ´ táº£ tham sá»‘ nghiÃªn cá»©u má»¥c tiÃªu khÃ¡c vá»›i scaffold hiá»‡n táº¡i;
khi cháº¡y code, Æ°u tiÃªn giÃ¡ trá»‹ trong `src/constants/`.

## 3. CÃ i mÃ´i trÆ°á»ng vÃ  thÆ° viá»‡n

YÃªu cáº§u:

- Windows PowerShell.
- Python 3.10 trá»Ÿ lÃªn.
- `pip` cÃ³ trong Python.

CÃ¡c thÆ° viá»‡n cá»§a project Ä‘Æ°á»£c khai bÃ¡o táº¡i
[implementation/requirements.txt](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/requirements.txt>):
`numpy`, `pandas`, `matplotlib` vÃ  `jupyter`.

Tá»« thÆ° má»¥c gá»‘c project, táº¡o mÃ´i trÆ°á»ng áº£o:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r implementation\requirements.txt
```

Náº¿u PowerShell cháº·n activate script, cÃ³ thá»ƒ cháº¡y lá»‡nh cÃ i Ä‘áº·t báº±ng Python
trong mÃ´i trÆ°á»ng áº£o mÃ  khÃ´ng activate:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r implementation\requirements.txt
```

Kiá»ƒm tra mÃ´i trÆ°á»ng:

```powershell
.\.venv\Scripts\python.exe -c "import numpy, pandas, matplotlib; print('Dependencies OK')"
```

Sau khi cÃ i xong, má»i lá»‡nh dÆ°á»›i Ä‘Ã¢y dÃ¹ng `python` náº¿u mÃ´i trÆ°á»ng Ä‘Ã£ activate,
hoáº·c dÃ¹ng `.\.venv\Scripts\python.exe` náº¿u chÆ°a activate.

## 4. Quy trình A — Sinh dataset (độc lập)

Phần này **không chạy thuật toán tối ưu**. Dataset được sinh tự động với vị trí theo hotspot và nền rải thưa.

```powershell
cd implementation
python scripts\generate_dataset.py
```

Kết quả được ghi vào `..\data\stores\` và `..\data\views\`.
Mặc định tạo 500 CSV, đánh số từ `001` đến `500`: 10 mức quy mô
`50, 100, 150, 200, 250, 300, 350, 400, 450, 500` users, mỗi mức 50 bộ.

```powershell
python scripts\generate_dataset.py --num-datasets 150
python scripts\generate_dataset.py --num-datasets 500 `
  --counts 50 100 150 200 250 300 350 400 450 500
```

Chỉ sinh lại khi muốn thay đổi số lượng users, số file, seed hoặc quy tắc phân bố.
## 5. Quy trÃ¬nh B â€” Cháº¡y thuáº­t toÃ¡n (dÃ¹ng dataset cÃ³ sáºµn)

Pháº§n nÃ y chá»‰ Ä‘á»c CSV trong `data/stores`; khÃ´ng tá»± sinh dataset má»›i.

```powershell
cd implementation
python scripts\run_optimizer.py `
  --algorithm all `
  --seed 42 `
  --dataset ..\data\stores\001_UAV_3D_50_users_connect.csv
```

`--algorithm` nháº­n `GA`, `PSO`, `WOA` hoáº·c `all`. Äá»•i dataset báº±ng má»™t trong
cÃ¡c file Ä‘Æ°á»£c Ä‘Ã¡nh sá»‘ tá»« `001` Ä‘áº¿n `100` trong `data/stores`.

## 6. Quy trÃ¬nh C â€” Cháº¡y thÃ­ nghiá»‡m nhiá»u seed

```powershell
cd implementation
python scripts\run_experiments.py
```

Quy trÃ¬nh nÃ y dÃ¹ng cho so sÃ¡nh cÃ´ng báº±ng nhiá»u seed/thuáº­t toÃ¡n. Káº¿t quáº£ pháº£i
Ä‘Æ°á»£c ghi vÃ o `implementation/results/`, khÃ´ng ghi ngÆ°á»£c vÃ o `data/stores`.

## 7. Quy trÃ¬nh D â€” PhÃ¢n tÃ­ch báº±ng notebook

Notebook chá»‰ Ä‘á»c káº¿t quáº£ Ä‘Ã£ sinh, táº¡o báº£ng tá»•ng há»£p vÃ  biá»ƒu Ä‘á»“; khÃ´ng sinh
dataset vÃ  khÃ´ng thay tháº¿ optimizer.

```powershell
cd implementation
jupyter notebook notebooks\comparison_experiment.ipynb
```

Luá»“ng Ä‘á»™c láº­p lÃ :

```text
data/stores
  -> run_optimizer.py hoáº·c run_experiments.py
  -> implementation/results
  -> notebooks/comparison_experiment.ipynb
```

## 8. Tráº¡ng thÃ¡i triá»ƒn khai

Cáº¥u trÃºc module Ä‘Ã£ tÃ¡ch sáºµn theo trÃ¡ch nhiá»‡m. Má»™t sá»‘ optimizer, objective vÃ 
evaluator váº«n lÃ  scaffold; khÃ´ng coi thÆ° má»¥c Ä‘Ã£ cÃ³ nghÄ©a lÃ  chá»©c nÄƒng Ä‘Ã£ hoÃ n
thiá»‡n. Pháº§n cÃ´ng thá»©c/Ã½ tÆ°á»Ÿng cáº§n Ä‘á»‘i chiáº¿u vá»›i [NOTE.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/NOTE.md>) vÃ  pháº§n ká»¹ thuáº­t táº¡i [implementation/docs/formulas.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/formulas.md>).




