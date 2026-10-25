# Tối ưu vị trí UAV cho mạng không dây

Dự án mô phỏng việc đặt trạm phát sóng UAV trong không gian ba chiều để phục vụ user có tọa độ cho trước. GA, PSO, WOA, hai thuật toán lai và I-WOA tìm tọa độ UAV theo cùng hàm đánh giá phủ sóng, công suất chuẩn hóa và chồng lấn kết nối.

**Trạng thái ngày 25/10/2026:** đã có mã thuật toán, bộ 500 CSV, runner FE và notebook thiết kế 30 trường hợp chạy 100 vòng. Notebook chưa chạy thí nghiệm; danh sách seed chưa chốt. Chưa có kết quả mới để kết luận thuật toán nào tốt nhất. Đầu ra smoke và batch dở trong `implementation/results/` đã được dọn.

## Bắt đầu đọc

| Bạn cần hiểu gì? | Đọc ở đâu? |
|---|---|
| Toàn bộ tài liệu liên kết thế nào | [Mục lục và lộ trình đọc](implementation/docs/README.md) |
| Bài toán, kiến trúc và luồng dữ liệu | [Hướng dẫn người mới](implementation/docs/PROJECT_GUIDE.md) |
| UE, seed, FE, ablation, fitness | [Thuật ngữ](implementation/docs/GLOSSARY.md) |
| Mô hình và giới hạn kết luận | [Báo cáo phương pháp](implementation/docs/REPORT.md) |
| Thiết kế 30 trường hợp, 100 vòng | [Hướng dẫn notebook](implementation/docs/NOTEBOOK_STUDY.md) |
| Chuẩn bị môi trường và chọn luồng chạy | [Hướng dẫn tái lập](REPRODUCE.md) |
| Trình bày và trả lời câu hỏi | [Kịch bản thuyết trình](TALK.md) |

Người mới nên đọc README này → PROJECT_GUIDE → GLOSSARY → REPORT → NOTEBOOK_STUDY. Sau đó chọn tài liệu thuật toán hoặc thống kê trong mục lục.

## Bài toán được giải

Với N UAV, một nghiệm chứa 3N số: `[x1, y1, z1, ..., xN, yN, zN]`. Với 4 UAV, đó là vector 12 chiều. User là đầu vào cố định trong một dataset; UAV là vị trí thuật toán tìm.

Hàm mục tiêu mặc định cần cực đại hóa: `F = 0,6C − 0,2E − 0,2I`.

- C: tỷ lệ user được ít nhất một UAV phủ theo ngưỡng SNR.
- E: proxy công suất trung bình chuẩn hóa; không phải năng lượng Joule.
- I: tỷ lệ user được từ hai UAV trở lên phủ theo cùng ngưỡng; không phải công suất nhiễu hoặc diện tích giao nhau.

Trọng số và ngưỡng là lựa chọn mô phỏng. Mô hình chưa mô tả đầy đủ dung lượng, backhaul hoặc điều khiển bay. Xem [REPORT](implementation/docs/REPORT.md).

## Ba luồng chạy

| Luồng | Đầu vào | Ngân sách | Mục đích |
|---|---|---|---|
| Notebook | 500 CSV có sẵn | 100 vòng, quần thể 25, 4 UAV | 30 trường hợp, bảng và ảnh cùng chỗ |
| Benchmark FE | Kịch bản sinh từ YAML và seed manifest | Mặc định 3030 FE, quần thể 30 | Đối chứng cùng FE, ablation và sensitivity |
| Script đơn lẻ/batch cũ | CSV có sẵn | Số vòng qua CLI | Một dataset hoặc batch sáu thuật toán |

Không gộp kết quả ba luồng như cùng thí nghiệm. Cùng 100 vòng không có nghĩa cùng FE. Analyzer FE không nhận trực tiếp schema notebook.

## Cấu trúc thư mục

| Thư mục | Vai trò |
|---|---|
| `configs/` | Cấu hình notebook và benchmark FE |
| `data/stores/`, `data/views/` | CSV user và hình đầu vào |
| `implementation/src/` | Mô hình, thuật toán, bộ chạy, tổng hợp |
| `implementation/notebooks/`, `implementation/scripts/` | Giao diện notebook và điểm vào CLI |
| `implementation/docs/` | Tài liệu phương pháp và thiết kế |
| `implementation/tests/` | Kiểm tra mã, không phải kết quả nghiên cứu |
| `implementation/results/` | Đầu ra khi chạy thực nghiệm |
| `documents/`, `plan/` | Danh mục tham khảo và kế hoạch |
| `figures/`, `reports/`, `tmp_audit/` | Minh họa, kiểm toán hoặc kiểm tra; xác minh nguồn trước khi dùng |

Đọc tài liệu không cần chạy mã. Khi có yêu cầu thực thi, theo [REPRODUCE](REPRODUCE.md). Notebook mặc định `CONFIRM_RUN = False`, seed để trống. Không điền kết luận bằng số liệu lịch sử thiếu log.

Nhóm thực hiện: Nguyễn Văn Trung, Hoàng Văn Trường, Nguyễn Minh Hiếu.
