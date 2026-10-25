# Độ ổn định theo seed, quy mô và phân bố user

[Mục lục](README.md) · [Thuật ngữ](GLOSSARY.md) · [Schema](DATA_FORMAT.md)

Có hai câu hỏi khác nhau: thuật toán có ổn định giữa các seed trên cùng dataset không, và kết quả có thay đổi khi dataset/phân bố thay đổi không? Không gộp cả hai thành một độ lệch chuẩn rồi gọi đó là ổn định thuật toán.

## Notebook 500 CSV

[Study notebook](NOTEBOOK_STUDY.md) giữ dữ liệu từng file cố định và lặp seed. Bảng stability tính mean/SD/min/max qua seed trên từng dataset/case; summary lấy trung bình các SD đó. by_scale gộp theo số user. ranking dùng trung vị seed trên từng dataset rồi tính hạng.

Notebook không tự gán nhãn single_cluster/uniform cho 500 CSV từ tên file. Tên mức user không chứng minh loại phân bố.

## Luồng FE và năm bộ sinh

[scenarios.py](../src/scenarios.py) và [benchmark.yaml](../../configs/benchmark.yaml) đã được tích hợp với runner FE. Tọa độ dưới đây là tham số thiết kế mặc định, không phải kết quả.

| Phân bố | Quy tắc |
|---|---|
| single_cluster | Cụm giữa miền; Gaussian sigma 50 m, bán kính tối đa 120 m |
| multi_cluster | Bốn tâm tại các phần tư miền 1000×1000 m, chia user gần đều |
| uniform | Đều theo diện tích miền chữ nhật |
| offset_cluster | Cụm lệch tâm (200,750) m |
| with_outliers | Lõi giữa miền và khoảng 10% ngoại lai trong vành 350–450 m |

Bộ sinh FE dùng user mặt đất z=0, demand=1. Các CSV minh họa trong figures và ảnh scenario chỉ trình bày hình học; không phải output tối ưu hoặc bằng chứng tổng quát hóa.

## Analyzer FE

[analyze_stability.py](../scripts/analyze_stability.py) đọc log FE sáu thuật toán, chỉ lấy purpose=eval, kiểm tra cặp seed/FE, khả thi và số UE. Các bảng gồm tổng hợp, hạng theo quy mô/phân bố và trường hợp I-WOA không đứng đầu.

Tên output thực: `stability_summary.csv`, `ranks_by_ue_count.csv`, `ranks_by_distribution.csv`, `iwoa_not_first.csv`. File cuối liệt kê I-WOA có fitness thấp hơn best cùng cặp; hòa không tính là thua.

Analyzer không tự chứng minh đủ manifest. Runner và người phân tích cần đối chiếu thiết kế. Không đưa runs.csv notebook vào analyzer FE trực tiếp.

## Điều còn thiếu

Chưa có study mới đủ dữ liệu để kết luận case nào ổn định hơn. Target chưa chốt trong cấu hình FE nên hit-rate có thể trống; không diễn giải là thất bại. Số instance/run trong YAML là thiết kế cần thẩm định trước full run, không phải bằng chứng đủ lực thống kê.

Đọc tiếp [SENSITIVITY](SENSITIVITY.md) nếu muốn đổi hàm mục tiêu, hoặc [STATISTICS](STATISTICS.md) nếu muốn suy luận từ các instance.
