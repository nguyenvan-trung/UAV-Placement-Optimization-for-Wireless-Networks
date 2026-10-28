# Độ nhạy theo trọng số và tiêu chí phủ sóng

## Mục lục

1. [Hạ tầng hiện có](#doc-section-01)
2. [Quy tắc so sánh](#doc-section-02)
3. [Đầu ra analyzer](#doc-section-03)
4. [Giới hạn kết luận](#doc-section-04)


[Mục lục](README.md) · [Mô hình](REPORT.md) · [Thiết kế FE](EXPERIMENT_DESIGN.md)

Sensitivity hỏi: nếu thay trọng số hoặc định nghĩa coverage thì thứ hạng, chất lượng và đánh đổi có thay đổi không? Nó khác [ablation](ABLATION.md), nơi giữ mô hình và đổi thành phần thuật toán.

<a id="doc-section-01"></a>

## Hạ tầng hiện có

- [sensitivity.yaml](../../configs/sensitivity.yaml): các cấu hình trọng số, coverage-only và SINR phụ.
- [sensitivity.py](../src/objectives/sensitivity.py): evaluator riêng.
- [run_benchmark.py](../scripts/run_benchmark.py): mode sensitivity chạy optimizer lại cho từng cấu hình.
- [analyze_sensitivity.py](../scripts/analyze_sensitivity.py): tổng hợp, tương quan hạng, kiểm định ghép cặp và chẩn đoán.

Ngân sách, instance và seed lấy từ benchmark.yaml. Full study chưa chạy. Luồng notebook 12 case hiện không tự chạy sensitivity; không cộng các thí nghiệm này vào 12 case.

<a id="doc-section-02"></a>

## Quy tắc so sánh

Cần tối ưu lại từng cấu hình với cùng FE và seed; chấm lại một nghiệm cũ không thay thế thí nghiệm này. Chỉ so fitness trong cùng bộ trọng số/coverage. Giữa các cấu hình, xem riêng C_snr, C_sinr, E và I.

SINR phụ dùng công suất tuyến tính mW với giả định các UAV phát đồng thời, đồng kênh. Nếu vẫn giữ I trong mục tiêu, nhiễu được phản ánh cả trong C lẫn I; đây là lựa chọn của nhánh phụ, không thay baseline SNR.

Evaluator riêng không tự bảo đảm khả thi; runner áp dụng cùng ràng buộc bài toán.

<a id="doc-section-03"></a>

## Đầu ra analyzer

| Sản phẩm | Cách đọc |
|---|---|
| ranks | Hạng fitness trung bình trong từng cấu hình |
| rank_correlations | Spearman so với baseline; tất cả hòa thì có thể NaN |
| paired_tests | So I-WOA với đối thủ trên trung vị instance, p điều chỉnh Holm và effect |
| metric_medians | C_snr/C_sinr/E/I để xem đánh đổi |
| diagnostics | Phương sai E, số mức coverage, tỷ lệ bão hòa |
| tradeoff_C_E / tradeoff_C_I | Các điểm trung vị, chưa phải mặt Pareto toàn miền |

Script kiểm tra đủ cấu hình/thuật toán/cặp seed/FE, các cờ feasible/reoptimized và công thức fitness. Các cờ không tự chứng minh nguồn gốc; cần log và manifest. Ngưỡng bão hòa/gần hằng số trong YAML là cấu hình chẩn đoán, không phải kết quả.

<a id="doc-section-04"></a>

## Giới hạn kết luận

Chưa có kết quả để bảo vệ trọng số 0,6/0,2/0,2 như tối ưu hoặc khẳng định thứ hạng bền vững. Phương sai E nhỏ trên nghiệm cuối không chứng minh E hằng số toàn miền. Cần thẩm định đơn vị độc lập và các giả định kiểm định; xem [STATISTICS](STATISTICS.md).

Cách chọn đúng luồng và lệnh thực thi khi được yêu cầu: [REPRODUCE](../../REPRODUCE.md).
