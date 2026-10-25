# Hướng dẫn thuyết trình và hỏi đáp

[Trang đầu](README.md) · [Mục lục](implementation/docs/README.md) · [Mô hình](implementation/docs/REPORT.md)

Tài liệu giúp người mới trình bày đúng phần đã có và phần chưa có. Study notebook 100 vòng chưa chạy; không có số đo hoặc thứ hạng mới để đưa vào phần kết quả.

## Trình tự trình bày

| Phần | Nội dung | Đọc trước |
|---|---|---|
| Bài toán | User là đầu vào; vị trí UAV là nghiệm đầu ra | [PROJECT_GUIDE](implementation/docs/PROJECT_GUIDE.md) |
| Mô hình | SNR, C/E/I, ràng buộc và giới hạn | [REPORT](implementation/docs/REPORT.md) |
| Phương pháp | Sáu thuật toán và ba toán tử K/O/L | [Mục lục thuật toán](implementation/docs/README.md) |
| Thiết kế | 500 CSV, 100 vòng, 30 trường hợp; seed cần chốt | [NOTEBOOK_STUDY](implementation/docs/NOTEBOOK_STUDY.md) |
| Kết quả | Chỉ điền khi có task đầy đủ và log nguồn | [REPORT_EVIDENCE](implementation/docs/REPORT_EVIDENCE.md) |
| Thảo luận | Chất lượng, chi phí, độ ổn định, giới hạn | [STATISTICS](implementation/docs/STATISTICS.md) |

## Mẫu giới thiệu

“Nhóm tìm tọa độ ba chiều cho các UAV phát sóng trên một tập user cố định. Nhóm dùng chung hàm mục tiêu cho sáu thuật toán chính và thiết kế ablation để đánh giá đóng góp các toán tử. Hiện mã và thiết kế đã có; study mới chưa chạy nên chưa kết luận thuật toán tốt nhất.”

## Hỏi đáp theo triển khai

**Vì sao dùng 4 UAV?** Đây là cấu hình đối chứng cố định, chưa phải số UAV đã chứng minh tối ưu. Muốn chọn số UAV cần thêm thí nghiệm và mô hình chi phí phù hợp.

**Phủ sóng nghĩa là gì?** Một user được ít nhất một UAV cung cấp SNR đạt ngưỡng. Chưa bảo đảm tốc độ, dung lượng hoặc độ trễ ứng dụng.

**E có phải năng lượng pin không?** Chưa. Đó là proxy công suất trung bình chuẩn hóa, chưa tích phân theo thời gian nhiệm vụ.

**I có phải nhiễu đồng kênh không?** Bản chính đếm tỷ lệ user có từ hai liên kết đạt ngưỡng SNR. SINR là phân tích phụ riêng.

**H-WOA-PSO có chia đôi quần thể không?** Không. Mỗi cá thể có đề xuất WOA và bước PSO; vị trí mới trộn hai đề xuất theo tỷ lệ 0,5/0,5. Xem [DWH_WOA_PSO](implementation/docs/DWH_WOA_PSO.md).

**Vì sao I-WOA có thể tốn thời gian hơn?** OBL/Lévy thêm đánh giá fitness; K-Means có chi phí khởi tạo. Mức chênh lệch phải đo.

**100 vòng có phải cùng ngân sách không?** Cùng số vòng, chưa chắc cùng FE. Notebook báo cả FE và thời gian; thiết kế FE là luồng riêng.

**Có chạy riêng 35 và 80 vòng không?** Không trong study này. Đó là checkpoint của lần chạy cấu hình 100 vòng, không phải thí nghiệm có tổng ngân sách 35/80.

**500 file có đủ tin cậy không?** Số file không tự bảo đảm kết luận. Cần biết cách tạo dữ liệu, độc lập giữa dataset, số seed và phương pháp phân tích.

**Có chứng minh tối ưu toàn cục không?** Không. Hội tụ, SD nhỏ hoặc thắng các đối chứng không phải chứng minh toàn cục.

**Trọng số 0,6/0,2/0,2 từ đâu?** Là lựa chọn thiết kế ưu tiên phủ sóng; cần phân tích độ nhạy, không gọi là tỷ lệ vàng hay chuẩn IEEE.

## Khi có kết quả

Ghi rõ dataset, seed, ngân sách, phiên bản mã, phép gộp và nguồn bảng. Trình bày cả trường hợp phương án đề xuất thua. Phân biệt mô tả với kiểm định; một hình 3D không đại diện cho toàn bộ dữ liệu.
