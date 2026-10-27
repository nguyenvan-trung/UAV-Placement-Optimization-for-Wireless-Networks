# Trình bày dự án: từ mô hình đến kết luận

[Trang đầu](README.md) · [Logic nghiên cứu](NOTE.md) · [Nguồn](implementation/docs/SOURCES.md)

Đây là kịch bản để người mới có thể giải thích dự án. Các câu nói về kết quả chỉ được điền sau khi có log. Study 80 vòng hiện chưa chạy.

## Mục lục

1. [Sơ đồ câu chuyện](#so-do)
2. [Kịch bản từng phần](#kich-ban)
3. [Giải thích công thức bằng lời](#cong-thuc)
4. [Cách trình bày kết quả khi có dữ liệu](#ket-qua)
5. [Hỏi đáp thường gặp](#hoi-dap)
6. [Tài liệu chuẩn bị và nguồn](#tai-lieu)

<a id="so-do"></a>

## 1. Sơ đồ câu chuyện

![Bức tranh tổng thể cần giải thích khi trình bày dự án](implementation/docs/assets/overview.svg)

**Cách kể:** user ở đâu → cần tìm gì cho UAV → chấm ứng viên thế nào → các thuật toán tìm khác nhau ra sao → đối chứng thế nào → kết quả có chứng cứ gì. Giải thích từng khối trước khi chuyển sang công thức.

<a id="kich-ban"></a>

## 2. Kịch bản từng phần

| Phần | Điều cần nói | Hình/tài liệu |
|---|---|---|
| Bài toán | “Đầu vào là user; đầu ra là vị trí của cả đội UAV.” | README, hình tổng quan |
| Biểu diễn | “4 UAV tạo một vector 12 chiều; mỗi cá thể là cả vector.” | REPORT |
| Hàm chấm | “Cùng một hàm F dùng cho mọi phương pháp.” | Hình fitness, bảng C/E/I |
| Phương pháp | “Khác nhau ở cách đề xuất cấu hình, không ở cách đếm user.” | Sáu hình thuật toán |
| Thiết kế | “12 case, 200 CSV, 80 vòng, cùng seed đã chốt.” | NOTEBOOK_STUDY |
| Kết quả | “Bảng này tổng hợp từ những task nào, bằng phép gộp gì?” | Task/manifest/bảng thật |
| Giới hạn | “E/I là proxy, chưa chứng minh tối ưu toàn cục hoặc mạng thực.” | REPORT, SOURCES |

**Mẫu mở đầu:** “Nhóm nghiên cứu vị trí UAV phát sóng trên một tập user có tọa độ cho trước. Nhóm dùng cùng hàm mục tiêu cho các thuật toán và thiết kế ablation để kiểm tra đóng góp từng thành phần. Mã và giao thức đã được chuẩn bị; study mới chưa có kết quả nên nhóm chưa kết luận phương án tốt nhất.”

<a id="cong-thuc"></a>

## 3. Giải thích công thức bằng lời

![Một lần chấm fitness: ứng viên, ràng buộc, kênh, ba chỉ số và điểm](implementation/docs/assets/fitness.svg)

Nói theo thứ tự dưới đây, không đọc một chuỗi công thức dài:

1. Với tọa độ UAV và user, tính khoảng cách và kênh để có SNR.
2. Một user được phủ nếu ít nhất một SNR đạt ngưỡng.
3. User có từ hai liên kết đạt ngưỡng được đếm trong chỉ số chồng lấn I.
4. Độ cao UAV quyết định proxy công suất E theo giả định hiện tại.
5. F cộng lợi ích phủ sóng và trừ hai chi phí theo trọng số.

| Ký hiệu | Diễn giải khi nói |
|---|---|
| C | Phần user được phủ, trong [0,1] |
| E | Công suất trung bình chuẩn hóa, không phải Joule |
| I | Phần user có nhiều liên kết đạt ngưỡng, không phải diện tích giao nhau |
| 0,6 / 0,2 / 0,2 | Trọng số nhóm chọn; cần nghiên cứu độ nhạy |
| FE | Số lần chấm một ứng viên, kể cả bị loại |

Công thức, đơn vị và nguồn chính xác: [REPORT](implementation/docs/REPORT.md). Không gọi ngưỡng SNR là chuẩn QoS chung.

<a id="ket-qua"></a>

## 4. Cách trình bày kết quả khi có dữ liệu

| Nội dung | Cần ghi trên bảng/hình |
|---|---|
| Phạm vi | Dataset, case, seed, số UAV, P, số vòng hoặc max FE |
| Phép gộp | Mean, median, best, SD và lấy trên đơn vị nào |
| Hội tụ | Trục vòng hoặc FE; dải IQR/CI phải gọi đúng |
| Chi phí | Thời gian có gồm phần nào; số FE thực |
| So sánh | Cả trường hợp thắng, hòa, thua; không chỉ chọn hình đẹp |
| Nguồn | Task/manifest và code tạo bảng |

Nếu chưa có log, để “chưa có kết quả”, không đặt số mẫu như số đã đo. Ảnh 3D chỉ là một nghiệm đã chọn theo quy tắc, không chứng minh cả study tốt.

<a id="hoi-dap"></a>

## 5. Hỏi đáp thường gặp

**Vì sao 4 UAV?** Cấu hình đối chứng cố định; chưa chứng minh đó là số UAV tối ưu.

**Vì sao 80 vòng?** Ngân sách theo vòng đã chọn. Cần xem lịch sử và chi phí để đánh giá, không khẳng định đã hội tụ trước khi chạy.

**80 vòng có công bằng tuyệt đối không?** Cùng số vòng, chưa chắc cùng FE. OBL/Lévy tăng đánh giá; cần báo cả FE và thời gian.

**K-Means có tìm nghiệm tối ưu không?** Nó tạo một nghiệm mầm theo tâm cụm XY; sau đó thuật toán tiếp tục tìm.

**Lévy có bảo đảm thoát cực trị không?** Không. Nó tạo thêm đề xuất bước nhảy theo xác suất; hiệu quả phải đo.

**H-WOA-PSO có chia đôi quần thể không?** Không. Mỗi cá thể có hai đề xuất rồi trộn 0,5/0,5.

**Đường phủ sóng phẳng có phải code sai không?** Chưa đủ kết luận. Coverage là tỷ lệ rời rạc và có thể bão hòa; cần xem C/E/I, dữ liệu và hàm chấm.

**200 file có thay 10 seed không?** Không. File thay bố trí user; seed thay tìm kiếm trên một bố trí.

**Có chứng minh tối ưu toàn cục hoặc đáp ứng mạng thực không?** Không từ study mô phỏng hiện tại. Mô hình thiếu dung lượng, backhaul và điều khiển bay.

**Nguồn công thức ở đâu?** Mỗi chương có mục nguồn; [SOURCES](implementation/docs/SOURCES.md) phân biệt công thức nguyên lý và lựa chọn riêng của nhóm.

<a id="tai-lieu"></a>

## 6. Tài liệu chuẩn bị và nguồn

Đọc [NOTE](NOTE.md) cho logic → [REPORT](implementation/docs/REPORT.md) cho mô hình → sáu chương DW cho cơ chế → [NOTEBOOK_STUDY](implementation/docs/NOTEBOOK_STUDY.md) cho đối chứng.

Không viện dẫn một bài báo như nguồn của cả fitness và thứ hạng dự án. Trình tự kể chuyện và sơ đồ trong trang này là phần biên soạn của dự án; nguyên lý học thuật được chỉ rõ ở SOURCES. [REPRODUCE](REPRODUCE.md) là nơi tra vận hành, không phải kịch bản chứng minh kết quả.
