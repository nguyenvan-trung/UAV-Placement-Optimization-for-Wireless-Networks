﻿# UAV Placement Optimization for Wireless Networks

Dự án nghiên cứu tối ưu vị trí 3D của các UAV base station trong mạng không
dây. Ý tưởng, công thức và mục tiêu nghiên cứu nằm trong [NOTE.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/NOTE.md>).
README này chỉ hướng dẫn cách tìm mã nguồn, dữ liệu và cách chạy.

## 1. Bản đồ thư mục

```text
.
├── data/                         # Dữ liệu; giữ độc lập với mã nguồn
│   ├── raw/                      # Dữ liệu gốc nếu có
│   ├── stores/                   # CSV đầu vào chính thức
│   └── views/                    # Ảnh quan sát của từng CSV
├── documents/                    # Bài báo và tài liệu nền tảng
│   ├── GA/
│   ├── PSO/
│   └── WOA/
├── plan/                         # Kế hoạch, phân công và tiến độ
├── implementation/               # Mã nguồn mô phỏng
│   ├── scripts/                  # Các lệnh chạy từ terminal
│   ├── src/
│   │   ├── constants/            # Tham số và đường dẫn cố định
│   │   ├── data_generation/      # Sinh dataset
│   │   ├── input/                # Đọc và kiểm tra CSV
│   │   ├── preprocessing/        # K-Means, khởi tạo UAV
│   │   ├── models/               # Kiểu dữ liệu miền
│   │   ├── physics/              # Công thức kênh truyền
│   │   ├── objectives/           # Coverage, energy, interference, fitness
│   │   ├── problem/              # Biên và ràng buộc
│   │   ├── algorithms/           # GA, PSO, WOA, I-WOA
│   │   ├── evaluation/           # Monte Carlo, metric, thống kê
│   │   └── visualization/        # Bảng và biểu đồ
│   ├── docs/                     # Tài liệu kỹ thuật của implementation
│   ├── notebooks/                # Phân tích kết quả, không phải entry point
│   ├── results/                  # Output sinh bởi thí nghiệm
│   └── datasets/                  # Chỉ tài liệu quy ước dataset
└── NOTE.md                      # Ý tưởng, mô hình và định hướng nghiên cứu
```

Xem [implementation/README.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/README.md>) để biết trách nhiệm chi tiết của từng tầng.

## 2. Tham số mặc định hiện tại

Các giá trị này là giá trị code đang dùng, nằm trong
[network.py](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/constants/network.py>)
và
[experiment.py](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/constants/experiment.py>).

| Nhóm | Tham số | Giá trị |
| --- | --- | ---: |
| Khu vực | `area_width_m` | `1000.0 m` |
| Khu vực | `area_height_m` | `1000.0 m` |
| UAV | `min_altitude_m` | `50.0 m` |
| UAV | `max_altitude_m` | `300.0 m` |
| Kết nối | `coverage_threshold_dbm` | `-90.0 dBm` |
| Thí nghiệm | `seeds` | `42, 123, 2026` |
| Thí nghiệm | `population_size` | `30` |
| Thí nghiệm | `max_iterations` | `100` |

Mặc định bộ sinh tạo **500 CSV**: 10 mức quy mô `50, 100, 150, 200, 250, 300, 350, 400, 450, 500` users, mỗi mức 50 bộ. Vị trí được sinh theo các hotspot, tòa nhà và nền rải thưa, không dùng lưới đều.
CSV có schema:
`user_id,x_m,y_m,z_m,demand`.

Trong schema 3D, `z_m=0` la user o mat dat/ngoai troi va `z_m>0` la user
o tang toa nha. Cac anh trong `data/views` co y nghia:
`top.png` (X-Y), `front.png` (X-Z), `side.png` (Y-Z) va `3d.png` (X-Y-Z).
UAV khong duoc tron vao CSV user; toa do UAV `(x,y,z)` la bien toi uu va
duoc luu o ket qua sau khi chay thuat toan.

`NOTE.md` có thể mô tả tham số nghiên cứu mục tiêu khác với scaffold hiện tại;
khi chạy code, ưu tiên giá trị trong `src/constants/`.

## 3. Cài môi trường và thư viện

Yêu cầu:

- Windows PowerShell.
- Python 3.10 trở lên.
- `pip` có trong Python.

Các thư viện của project được khai báo tại
[implementation/requirements.txt](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/requirements.txt>):
`numpy`, `pandas`, `matplotlib` và `jupyter`.

Từ thư mục gốc project, tạo môi trường ảo:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r implementation\requirements.txt
```

Nếu PowerShell chặn activate script, có thể chạy lệnh cài đặt bằng Python
trong môi trường ảo mà không activate:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r implementation\requirements.txt
```

Kiểm tra môi trường:

```powershell
.\.venv\Scripts\python.exe -c "import numpy, pandas, matplotlib; print('Dependencies OK')"
```

Sau khi cài xong, mọi lệnh dưới đây dùng `python` nếu môi trường đã activate,
hoặc dùng `.\.venv\Scripts\python.exe` nếu chưa activate.

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

Ch? sinh l?i khi mu?n thay d?i s? lu?ng users, s? file, seed ho?c quy t?c ph�n b?.
## 5. Quy trình B — Chạy thuật toán (dùng dataset có sẵn)

Phần này chỉ đọc CSV trong `data/stores`; không tự sinh dataset mới.

```powershell
cd implementation
python scripts\run_optimizer.py `
  --algorithm all `
  --seed 42 `
  --dataset ..\data\stores\001_UAV_3D_50_users_connect.csv
```

`--algorithm` nhận `GA`, `PSO`, `WOA` hoặc `all`. Đổi dataset bằng một trong
các file được đánh số từ `001` đến `100` trong `data/stores`.

## 6. Quy trình C — Chạy thí nghiệm nhiều seed

```powershell
cd implementation
python scripts\run_experiments.py
```

Quy trình này dùng cho so sánh công bằng nhiều seed/thuật toán. Kết quả phải
được ghi vào `implementation/results/`, không ghi ngược vào `data/stores`.

## 7. Quy trình D — Phân tích bằng notebook

Notebook chỉ đọc kết quả đã sinh, tạo bảng tổng hợp và biểu đồ; không sinh
dataset và không thay thế optimizer.

```powershell
cd implementation
jupyter notebook notebooks\comparison_experiment.ipynb
```

Luồng độc lập là:

```text
data/stores
  -> run_optimizer.py hoặc run_experiments.py
  -> implementation/results
  -> notebooks/comparison_experiment.ipynb
```

## 8. Trạng thái triển khai

Cấu trúc module đã tách sẵn theo trách nhiệm. Một số optimizer, objective và
evaluator vẫn là scaffold; không coi thư mục đã có nghĩa là chức năng đã hoàn
thiện. Phần công thức/ý tưởng cần đối chiếu với [NOTE.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/NOTE.md>) và phần kỹ thuật tại [implementation/docs/formulas.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/formulas.md>).




