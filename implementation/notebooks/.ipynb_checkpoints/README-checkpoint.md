# Notebooks: phân tích và trình bày kết quả

Notebook không sinh dataset mới và không chứa logic thuật toán chính. Nó dùng
để đọc dữ liệu/kết quả đã có, kiểm tra trực quan và trình bày so sánh.

## Notebook hiện có

### `comparison_experiment.ipynb`

Mục đích:

1. Đọc kết quả chạy từ `../results/tables/`.
2. Tóm tắt coverage, objective, số vòng hội tụ và runtime theo thuật toán.
3. Vẽ biểu đồ so sánh để kiểm tra nhanh trước khi đưa vào báo cáo.
4. Thử nghiệm tương tác các cách trình bày mà không làm thay đổi mã nguồn.

Luồng dữ liệu:

```text
data/stores/*.csv
    -> scripts/run_experiments.py
    -> results/tables/*.csv
    -> comparison_experiment.ipynb
    -> results/figures/ hoặc biểu đồ hiển thị trong notebook
```

Notebook hiện là khung giao diện phân tích; các ô có `TODO` sẽ dùng kết quả
thật sau khi optimizer và evaluator hoàn thiện.

## Cách mở và chạy

```powershell
cd implementation
jupyter notebook notebooks/comparison_experiment.ipynb
```

Nên chạy `scripts/run_experiments.py` trước. Không chạy notebook để thay thế
pipeline thực nghiệm chính thức.
