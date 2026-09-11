# Implementation

## Luồng xử lý

```text
datasets/raw
    -> data_processing (đọc, kiểm tra, làm sạch)
    -> models + problem (mô hình và hàm mục tiêu chung)
    -> algorithms/{GA, PSO, WOA}
    -> evaluation
    -> visualization
    -> results/{tables, figures, convergence}
```

## Trách nhiệm của các thư mục

- `datasets/raw/`: dữ liệu đầu vào nguyên bản.
- `datasets/processed/`: dữ liệu sau khi làm sạch/chuẩn hóa.
- `src/constants/`: tất cả giá trị cố định; không rải magic number trong thuật toán.
- `src/data_processing/`: tải file, xác thực schema và tiền xử lý.
- `src/models/`: các thực thể miền như UAV, user và mô hình kênh.
- `src/problem/`: biểu diễn nghiệm, ràng buộc và hàm mục tiêu dùng chung.
- `src/algorithms/`: thuật toán độc lập; mỗi bước nhỏ nằm trong một file.
- `src/evaluation/`: tính metric và gom kết quả của nhiều lần chạy.
- `src/visualization/`: tạo bảng và biểu đồ.
- `main.py`: chạy một hoặc cả ba thuật toán từ dòng lệnh.
- `run_experiments.py`: chạy nhiều seed, xuất CSV và biểu đồ.
- `notebooks/comparison_experiment.ipynb`: code ở ô trên, bảng/biểu đồ hiện ngay bên dưới.

## Chi tiết thuật toán

```text
algorithms/
├── base/                         # Interface và kết quả chuẩn
├── GA/
│   ├── chromosome.py             # Cấu trúc cá thể
│   ├── initialization.py         # Tạo quần thể ban đầu
│   ├── fitness.py                # Chuyển objective thành fitness
│   ├── selection.py              # Chọn bố mẹ
│   ├── crossover.py              # Lai ghép
│   ├── mutation.py               # Đột biến
│   ├── replacement.py            # Elitism/thay thế quần thể
│   ├── parameters.py             # Tham số riêng GA
│   └── optimizer.py              # Ghép các bước thành GA hoàn chỉnh
├── PSO/
│   ├── particle.py               # Trạng thái hạt
│   ├── initialization.py         # Tạo đàn hạt
│   ├── velocity_update.py        # Cập nhật vận tốc
│   ├── position_update.py        # Cập nhật vị trí
│   ├── best_update.py            # Cập nhật pbest/gbest
│   ├── boundary_handler.py       # Xử lý biên
│   ├── parameters.py             # Tham số riêng PSO
│   └── optimizer.py              # Ghép các bước thành PSO hoàn chỉnh
└── WOA/
    ├── whale.py                  # Trạng thái cá voi
    ├── initialization.py         # Tạo quần thể
    ├── coefficient_update.py     # Cập nhật a, A, C
    ├── encircling.py             # Bao vây con mồi
    ├── spiral_update.py          # Chuyển động xoắn ốc
    ├── exploration.py            # Tìm kiếm toàn cục
    ├── boundary_handler.py       # Xử lý biên
    ├── parameters.py             # Tham số riêng WOA
    └── optimizer.py              # Ghép các bước thành WOA hoàn chỉnh
```

## Cách chạy dự kiến

```bash
cd implementation
python main.py --algorithm all
python run_experiments.py
jupyter notebook notebooks/comparison_experiment.ipynb
```

Các file hiện là khung kiến trúc. Phần công thức cụ thể sẽ được hoàn thiện sau khi chốt dataset, mô hình kênh, hàm mục tiêu và ràng buộc từ tài liệu nghiên cứu.
