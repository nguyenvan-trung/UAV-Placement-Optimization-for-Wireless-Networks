# Nhiệm vụ 5 — phân tích thống kê

## Mục lục

1. [Phân biệt với notebook 12 trường hợp](#doc-section-01)
2. [Chạy khi được yêu cầu](#doc-section-02)
3. [Hợp đồng log](#doc-section-03)
4. [Phương pháp và sản phẩm](#doc-section-04)


[Mục lục](README.md) · [Người mới](PROJECT_GUIDE.md) · [Thuật ngữ](GLOSSARY.md) · [Study notebook](NOTEBOOK_STUDY.md)


Đã triển khai `implementation/scripts/analyze.py`. Không thay mã Fitness hay
thuật toán. Chưa phân tích kết quả nghiên cứu thật vì chưa có runs.csv theo FE.

<a id="doc-section-01"></a>

## Phân biệt với notebook 12 trường hợp

Trang này mô tả analyzer FE sáu thuật toán chính. Notebook có bảng mô tả, hạng và đóng góp riêng trong [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md); chưa triển khai kiểm định/CI cho 12 case. Không truyền trực tiếp runs.csv notebook vào analyze.py vì khác schema, số thuật toán và giao thức ngân sách.

Trong notebook, SD qua seed được tính trên mỗi dataset trước khi gộp; dải IQR hội tụ không phải CI. Bảng hạng hoặc win_fraction chỉ mô tả, không tự tạo kết luận có ý nghĩa thống kê. Các từ instance/run/seed được giải thích tại [GLOSSARY](GLOSSARY.md).

<a id="doc-section-02"></a>

## Chạy khi được yêu cầu

```powershell
$env:PYTHONPATH='implementation'
python -m pytest implementation/tests/test_statistics.py -q -p no:cacheprovider
python implementation/scripts/analyze.py path/to/runs.csv --output reports/statistics_run_01 --expected-runs 30 --resamples 2000 --seed 20261024 --alpha 0.05
```

Thư mục đầu ra phải rỗng để không trộn bảng/hình cũ. Các giá trị CLI là cấu
hình phân tích định trước, không phải kết quả đo. Metadata lưu hash CSV,
bootstrap seed, số resample và alpha. Có thể đổi trước khi chạy; không đổi
theo p-value. Test dữ liệu giả lập nằm trong reports/statistics_test_artifacts,
không được dùng làm bằng chứng I-WOA tốt hơn trên dữ liệu nghiên cứu.

<a id="doc-section-03"></a>

## Hợp đồng log

Cột bắt buộc: scenario_id, ue_count, distribution, instance_k, data_seed,
run_id, algo_seed, algorithm, fitness, wall_time_s, cpu_time_s, fe_used,
batch_id, batch_wall_time_s, batch_total_cpu_s, n_workers, purpose, feasible.
Chỉ một config_id nếu cột đó tồn tại. Không trộn Fitness khác trọng số.
Tên thuật toán: GA, PSO, WOA, H-PSO-GA, H-WOA-PSO, I-WOA.
Runner cần cung cấp batch_id và tổng CPU từ các process_time đã đo; script
không tự suy ra tổng CPU từ thời gian wall hoặc số worker.

Script kiểm tra ghép cặp, số run định trước, seed/FE đồng nhất giữa thuật
toán, tuning/eval không giao theo từng loại seed, giá trị hữu hạn/khả thi.
Vẫn cần manifest để xác nhận không thiếu cả một instance/scenario.

<a id="doc-section-04"></a>

## Phương pháp và sản phẩm

- `descriptive`: mean/median/best/std/IQR trên run (chỉ mô tả); CI của mean
  instance medians bằng percentile bootstrap ở cấp instance, không coi run
  cùng instance độc lập. Số run và số instance đều ghi trong bảng.
- `instance_medians`: gộp run trước kiểm định; một khối là một instance UE.
- `paired_comparisons`: chênh lệch I-WOA trừ đối thủ; median chênh lệch,
  bootstrap CI, rank-biserial và CI, p gốc/Holm, phương pháp, ties/zeros,
  kết luận thắng/hòa/thua. Holm family là toàn bộ đối thủ trong lần chạy.
- Nếu ít hơn 10 cặp khác không hoặc tỷ lệ ties độ lớn trên 25%, dùng sign
  test chính xác, nêu lý do. Đây là quy tắc thận trọng khai báo trước, không
  phải định lý đảm bảo đủ lực kiểm định. Các giả định độc lập vẫn cần thẩm định.
  Wilcoxon cần phân bố chênh lệch đối xứng; script ghi giả định chứ không
  khẳng định đã chứng minh. Có thể yêu cầu sign test làm phân tích độ nhạy.
- Tất cả chênh lệch bằng không: p=1, effect=0. “Hòa” chỉ là chưa đủ bằng
  chứng khác biệt, không chứng minh tương đương. CI là pointwise, không phải
  CI đồng thời sau hiệu chỉnh đa so sánh. Bootstrap ít instance có thể kém ổn định.
- `omnibus`, `overall_ranks`: Friedman và rank trung bình trên instance.
  Chỉ thực hiện xấp xỉ Friedman từ 10 khối; nếu omnibus có ý nghĩa mới chạy
  Nemenyi và hình thang critical difference. Nemenyi dùng studentized range
  và hiệu chỉnh toàn family; hình chưa biểu diễn các clique không khác biệt.
- `performance`: wall/CPU riêng, FE và FE/wall-second (bao gồm overhead).
  `batches`: wall thực tế, tổng CPU, worker; loại lặp metadata theo batch_id,
  không cộng thời gian batch lặp trên mỗi dòng run.
- Tất cả bảng xuất CSV/Markdown/LaTeX có chú thích; hình CD xuất PNG/PDF khi
  đủ điều kiện. Không tự vẽ CD khi ít khối hoặc omnibus không có ý nghĩa.

Gộp instance từ nhiều kịch bản giả định các instance độc lập và được cân
trọng số đều. Nếu dùng chung dữ liệu nền giữa các kịch bản, phải thiết kế
khối/cluster bootstrap khác; nhiều run không sửa được phụ thuộc đó.

Kiểm thử giả lập xác nhận số cặp theo instance, effect/ties, Holm, bootstrap
tái lập, đường xuất đầy đủ và từ chối mất thuật toán. Chưa xác minh nguồn
thống kê bên ngoài trong lượt này; nếu trích dẫn bài phương pháp, cần sinh
viên tự xác minh nguồn trước khi đưa vào luận văn.
