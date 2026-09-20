# Scripts

ÄÃ¢y lÃ  cÃ¡c entry point cháº¡y tá»« terminal. Logic nghiá»‡p vá»¥ pháº£i náº±m trong
`src/`, khÃ´ng viáº¿t dá»“n vÃ o script.

| Script | DÃ¹ng khi nÃ o | Äáº§u vÃ o | Äáº§u ra |
| --- | --- | --- | --- |
| `generate_dataset.py` | Táº¡o láº¡i dá»¯ liá»‡u mÃ´ phá»ng | tham sá»‘ sá»‘ user/seed | `data/stores/`, `data/views/` |
| `run_optimizer.py` | Cháº¡y má»™t hoáº·c táº¥t cáº£ thuáº­t toÃ¡n | má»™t CSV trong `data/stores/` | nghiá»‡m vÃ  metric trong `results/` |
| `run_experiments.py` | Cháº¡y nhiá»u seed Ä‘á»ƒ so sÃ¡nh | dataset + cáº¥u hÃ¬nh thÃ­ nghiá»‡m | báº£ng, log, biá»ƒu Ä‘á»“ trong `results/` |

## Quy trình 1 — Sinh dataset (riêng)

```powershell
cd implementation
python scripts/generate_dataset.py
```

Mặc định tạo 500 CSV, đánh số `001` đến `500`; mỗi kích thước
`50, 100, 150, ..., 500` có 50 bộ. Vị trí dùng hotspot pha với nền rải thưa.

```powershell
python scripts/generate_dataset.py --num-datasets 150
python scripts/generate_dataset.py --num-datasets 500 `
  --counts 50 100 150 200 250 300 350 400 450 500
```

Neu chi can tao lai anh tu cac CSV da co trong `data/stores` ma khong sinh lai
du lieu, chay script PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\regenerate_views.ps1
```

Script tao bon anh cho moi CSV trong `data/views/<ten-dataset>`:

- `top.png`: phep chieu X-Y.
- `front.png`: phep chieu X-Z.
- `side.png`: phep chieu Y-Z.
- `3d.png`: phep chieu 3D X-Y-Z.

Cot `z_m` la do cao cua user: `0` la user ngoai troi/mat dat, gia tri duong
la user o tang toa nha. Vi tri UAV khong nam trong CSV user; no la dau ra 3D
cua bai toan toi uu.
## Quy trình 2 â€” Cháº¡y thuáº­t toÃ¡n (riÃªng)

python scripts/run_optimizer.py `
  --algorithm all `
  --seed 42 `
  --dataset ../data/stores/001_UAV_3D_50_users_connect.csv
```

`--algorithm` nháº­n `GA`, `PSO`, `WOA` hoáº·c `all`.

## Quy trÃ¬nh 3 â€” ThÃ­ nghiá»‡m vÃ  notebook

```powershell
# Cháº¡y bá»™ nhiá»u seed
python scripts/run_experiments.py

# Chá»‰ má»Ÿ notebook sau khi Ä‘Ã£ cÃ³ output
jupyter notebook notebooks/comparison_experiment.ipynb
```



