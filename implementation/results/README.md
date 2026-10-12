# Results: kết quả chạy thuật toán

Thư mục này chỉ chứa đầu ra được sinh bởi pipeline, không chứa mã nguồn và
không phải nơi lưu dataset đầu vào.

```text
results/
├── tables/       # CSV/JSON metric theo seed và thuật toán
├── figures/      # coverage, objective, runtime, convergence
├── solutions/    # vị trí UAV tốt nhất và metadata
├── convergence/  # lịch sử fitness theo iteration
└── logs/         # log cấu hình và lỗi của từng lần chạy
```

## Nguồn tạo kết quả

- `scripts/run_optimizer.py`: chạy một dataset và một lựa chọn thuật toán.
- `scripts/run_experiments.py`: chạy nhiều seed/thuật toán để so sánh.
- `notebooks/comparison_experiment.ipynb`: đọc bảng trong `results/tables/`
  và phân tích/trình bày, không thay thế script chạy chính thức.

Khi chưa có optimizer/evaluator hoàn chỉnh, các thư mục kết quả có thể rỗng.
Không nhập kết quả thủ công vào đây vì notebook sẽ không biết nguồn và cấu
hình của kết quả.
