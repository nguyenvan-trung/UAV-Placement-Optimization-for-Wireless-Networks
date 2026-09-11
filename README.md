# UAV Placement Optimization for Wireless Networks

Dự án so sánh GA, PSO và WOA cho bài toán tối ưu vị trí UAV trong mạng không dây.

```text
.
├── documents/                    # Bài báo, tài liệu và ghi chú nghiên cứu
│   ├── GA/
│   ├── PSO/
│   └── WOA/
├── plan/                         # Ý tưởng, phân công và kế hoạch 10 tuần
└── implementation/               # Dataset, thuật toán và thí nghiệm
    ├── datasets/
    ├── notebooks/
    ├── results/
    ├── src/
    │   ├── algorithms/           # GA, PSO và WOA tách riêng
    │   ├── constants/            # Thông số cố định
    │   ├── data_processing/      # Đọc, kiểm tra và tiền xử lý đầu vào
    │   ├── evaluation/           # Đo coverage, convergence, runtime
    │   ├── models/               # Mô hình UAV, user, kênh truyền
    │   ├── problem/              # Hàm mục tiêu và ràng buộc
    │   └── visualization/        # Bảng và biểu đồ
    ├── main.py                   # Điểm chạy chính
    └── run_experiments.py        # Chạy hàng loạt và xuất kết quả
```

Xem [implementation/README.md](implementation/README.md) để hiểu trách nhiệm của từng file và quy trình chạy.

Kế hoạch thực hiện và phân công nhóm được trình bày tại [plan/README.md](plan/README.md).
