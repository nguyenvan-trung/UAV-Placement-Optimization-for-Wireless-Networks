# Câu hỏi nghiên cứu và phạm vi

[Kế hoạch](README.md) · [Ghi chú quyết định](../NOTE.md) · [Mô hình hiện tại](../implementation/docs/REPORT.md)

Tìm cấu hình tọa độ UAV để phục vụ tập user cố định trong miền cho trước. Đầu vào gồm tọa độ user, số UAV, giới hạn miền/độ cao và tham số kênh; đầu ra gồm nghiệm, fitness, lịch sử và chi phí tìm kiếm.

Phạm vi hiện tại là mô phỏng vị trí tĩnh với tổng có trọng số C/E/I. Chưa có điều khiển bay, mô hình pin theo thời gian, bảo đảm dung lượng, backhaul hoặc chứng minh tối ưu toàn cục.

Các câu hỏi chính: so sáu thuật toán; đo đóng góp K/O/L trên ba họ; đo đóng góp thành phần bản lai; xem ổn định theo seed/quy mô. Xem [thiết kế 30 case](../implementation/docs/NOTEBOOK_STUDY.md).

Các hướng mở rộng như SINR hoặc mô hình năng lượng vật lý cần được tách thành thay đổi mô hình và có đối chứng tương ứng. [SENSITIVITY](../implementation/docs/SENSITIVITY.md) mô tả nhánh phụ đã chuẩn bị. Không trình bày ý tưởng như kết quả đã có.
