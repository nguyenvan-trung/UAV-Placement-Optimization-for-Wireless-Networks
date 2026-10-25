# Thuật ngữ và ký hiệu

[Mục lục](README.md) · [Bài toán](REPORT.md) · [Thiết kế notebook](NOTEBOOK_STUDY.md)

| Thuật ngữ | Ý nghĩa trong dự án |
|---|---|
| UAV / UAV-BS | Thiết bị bay / thiết bị bay mang trạm phát sóng |
| UE / user | Người dùng có tọa độ đầu vào; mỗi dòng CSV là một user |
| Dataset / instance | Một bộ tọa độ user cố định; không phải một vòng tối ưu |
| Scenario | Kiểu và quy mô dữ liệu; trong FE được định danh bằng mức UE và phân bố |
| Run | Một lần tối ưu một dataset với một thuật toán/biến thể và seed |
| Task | Đơn vị checkpoint; notebook dùng bộ ba dataset–case–seed |
| Seed | Số khởi tạo bộ sinh ngẫu nhiên; cần giữ danh sách giống nhau giữa các đối chứng |
| Data seed | Seed sinh tọa độ trong luồng FE; 500 CSV notebook đã có tọa độ sẵn |
| Algorithm seed | Seed cho khởi tạo và tìm kiếm |
| Tuning / eval | Tập chọn tham số / tập đánh giá; không dùng chung dữ liệu để tự đánh giá |
| Population P | Số ứng viên; mỗi ứng viên là cả cấu hình N UAV |
| N / M / D | Số UAV / số user / số chiều nghiệm; D = 3N |
| Iteration / generation / sweep | Một lượt cập nhật quần thể; chi phí FE có thể khác giữa thuật toán |
| FE | Một lời gọi hàm fitness; tính cả ứng viên bị loại hoặc không khả thi |
| Fitness F | Điểm cần cực đại hóa, mặc định 0,6C − 0,2E − 0,2I |
| C / f1 | Tỷ lệ user có ít nhất một liên kết SNR đạt ngưỡng |
| E / f2 | Proxy công suất trung bình chuẩn hóa, không có đơn vị Joule |
| I / f3 | Tỷ lệ user có ít nhất hai liên kết SNR đạt ngưỡng |
| SNR | Tín hiệu so với tạp âm; chưa cộng nhiễu liên UAV |
| SINR | Tín hiệu so với nhiễu và tạp âm; chỉ dùng trong nhánh độ nhạy phụ |
| LoS / NLoS | Truyền thẳng / không truyền thẳng; mô hình dùng xác suất LoS theo góc |
| Proxy | Đại lượng đại diện đơn giản hóa, không đồng nghĩa đại lượng vật lý đầy đủ |
| Baseline | Thuật toán hoặc cấu hình đối chứng |
| Ablation | Bật/tắt có kiểm soát để so đóng góp thành phần |
| K / O / L | K-Means khởi tạo / Opposition-Based Learning / Lévy Flight |
| pbest / gbest | Nghiệm tốt nhất cá nhân / tốt nhất toàn cục trong cơ chế PSO |
| Elitism | Giữ các cá thể tốt khi thay thế thế hệ GA |
| Best-so-far | Nghiệm tốt nhất đã đánh giá đến một mốc, không nhất thiết còn trong quần thể |
| Checkpoint | Dữ liệu lưu để truy vết/tiếp tục; không đồng nghĩa đã chạy xong toàn study |
| Manifest | Bản kê cấu hình, dataset, seed và định danh để kiểm tra đầy đủ |
| Hash / signature | Dấu kiểm nội dung để phát hiện nguồn/cấu hình thay đổi |
| SD | Độ lệch chuẩn; phải nêu tính qua seed hay gộp dataset |
| Median / IQR | Trung vị / khoảng phân vị 25–75%; IQR không phải CI |
| CI | Khoảng tin cậy theo một phương pháp và đơn vị lấy mẫu cụ thể |
| Mean rank | Hạng trung bình; thấp hơn là tốt hơn, không tự chứng minh khác biệt thống kê |
| Effect size | Độ lớn/hướng khác biệt, bổ sung cho p-value |
| Wall / CPU time | Thời gian trôi thực / thời gian CPU theo phạm vi đo được công bố |
| Smoke / test | Kiểm tra nhỏ hoặc dữ liệu phục vụ kiểm tra; không phải benchmark nghiên cứu |

Tỷ lệ trong log thường thuộc [0,1]; nhân 100 khi hiển thị phần trăm. Thời gian dùng giây; tọa độ dùng mét; tần số Hz; SNR dB; công suất phát/tạp âm dBm. Không trừ cộng dBm như công suất tuyến tính khi tính SINR.

Đọc tiếp [DATA_FORMAT](DATA_FORMAT.md) để hiểu tên trường, hoặc [STATISTICS](STATISTICS.md) để hiểu cách gộp nhiều run.
