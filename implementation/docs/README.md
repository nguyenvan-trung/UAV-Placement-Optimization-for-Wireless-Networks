# Mục lục tài liệu và lộ trình đọc

[Trang đầu dự án](../../README.md)

Đây là điểm tra cứu chung. Mỗi trang có phạm vi riêng; liên kết dẫn sang phần tiếp theo thay vì yêu cầu người đọc biết lịch sử trao đổi. Trạng thái hiện tại: study 30 trường hợp đã được triển khai nhưng chưa chạy; seed chưa chốt.

## Lộ trình cho người mới

1. [PROJECT_GUIDE](PROJECT_GUIDE.md): bài toán và đường đi từ dữ liệu tới kết quả.
2. [GLOSSARY](GLOSSARY.md): từ viết tắt, ký hiệu và đơn vị.
3. [REPORT](REPORT.md): công thức dùng chung và giới hạn mô hình.
4. [formulas](formulas.md): ánh xạ công thức sang mã.
5. [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md): thiết kế 30 trường hợp và cách đọc đầu ra.
6. [REPORT_EVIDENCE](REPORT_EVIDENCE.md): điều kiện để đưa số liệu vào báo cáo.

Muốn chỉ đọc phương pháp thì không cần cài Python hoặc thực thi notebook.

## Tài liệu thuật toán

| Tài liệu | Câu hỏi được trả lời |
|---|---|
| [DWGA](DWGA.md) | GA chọn lọc, lai ghép, đột biến và elitism như thế nào? |
| [DWPSO](DWPSO.md) | PSO cập nhật vận tốc, pbest, gbest ra sao? |
| [DWWOA](DWWOA.md) | WOA chọn bao vây, khám phá và xoắn ốc thế nào? |
| [DWI_WOA](DWI_WOA.md) | I-WOA bổ sung K-Means, OBL và Lévy ở đâu? |
| [DWH_PSO_GA](DWH_PSO_GA.md) | PSO kết hợp toán tử GA theo thứ tự nào? |
| [DWH_WOA_PSO](DWH_WOA_PSO.md) | Mỗi cá thể trộn đề xuất WOA và PSO ra sao? |
| [ABLATION](ABLATION.md) | Bật/tắt thành phần để đo đóng góp thế nào? |

Các chương DW giải thích cơ chế. Quy tắc biến thể mới của GA/PSO và các cờ bản lai được tập trung tại NOTEBOOK_STUDY để không trộn với baseline.

## Chạy và phân tích

| Tài liệu | Phạm vi |
|---|---|
| [REPRODUCE](../../REPRODUCE.md) | Chuẩn bị môi trường; chọn đúng notebook, FE hoặc script CSV |
| [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md) | 500 CSV, 100 vòng, 30 trường hợp |
| [EXPERIMENT_DESIGN](EXPERIMENT_DESIGN.md) | Luồng FE với kịch bản sinh từ cấu hình |
| [DATA_FORMAT](DATA_FORMAT.md) | Phân biệt schema CSV đầu vào, notebook, batch cũ và FE |
| [STATISTICS](STATISTICS.md) | Analyzer sáu thuật toán theo FE và giới hạn suy luận |
| [STABILITY](STABILITY.md) | Phân bố user, biến động qua seed và quy mô |
| [SENSITIVITY](SENSITIVITY.md) | Tối ưu lại khi đổi trọng số hoặc coverage |
| [FITNESS_AUDIT](FITNESS_AUDIT.md) | Kiểm toán mô hình và truy nguồn công thức |

## Báo cáo và nguồn tham khảo

- [REPORT](REPORT.md): tổng hợp phương pháp; phần kết quả chưa có dữ liệu mới.
- [REPORT_EVIDENCE](REPORT_EVIDENCE.md): phân loại tham số, minh họa, test và kết quả thật.
- [REPORT_CHANGES](REPORT_CHANGES.md): lịch sử chỉnh tài liệu và quy tắc cập nhật.
- [PROMPTS](PROMPTS.md): yêu cầu tác nghiệp lịch sử; không phải trạng thái triển khai.
- [NOTE](../../NOTE.md): quyết định và câu hỏi còn mở.
- [TALK](../../TALK.md): cách trình bày đúng phạm vi chứng cứ.
- [documents](../../documents/README.md): danh mục nguồn cần đọc xác minh.
- [plan](../../plan/README.md): kế hoạch/phân công, không phải bằng chứng đã hoàn tất.

## Khi có thông tin mâu thuẫn

Đối chiếu đúng luồng: cấu hình thực chạy → mã runner/thuật toán → manifest và log → bảng tổng hợp. Một lệnh trong tài liệu không chứng minh lệnh đã được thực hiện. Một bảng checklist cũ không thay completion hoặc log nguồn.

Ngày cập nhật trong tài liệu là mốc biên tập, không phải ngày đã chạy benchmark. Khi đổi thiết kế, cập nhật NOTEBOOK_STUDY hoặc EXPERIMENT_DESIGN tương ứng, rồi cập nhật README/PROJECT_GUIDE và schema nếu cần.
