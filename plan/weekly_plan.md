# Kế hoạch thực hiện trong 10 tuần

Tuần 1–9 dành cho nghiên cứu, thiết kế, triển khai và thí nghiệm. **Tuần 10 chỉ hoàn thiện báo cáo**, không bổ sung chức năng hoặc thay đổi mô hình lớn.

## Bảng kế hoạch tổng quát

| Tuần | Trọng tâm | Nguyễn Văn Trung | Hoàng Văn Trường | Nguyễn Minh Hiếu | Sản phẩm cuối tuần |
|---:|---|---|---|---|---|
| 1 | Học và xác định bài toán | Tìm hiểu UAV placement, điều phối phạm vi | Tìm hiểu GA và các ứng dụng liên quan | Tìm hiểu WOA, PSO và các metric | Danh mục kiến thức, thuật ngữ và câu hỏi nghiên cứu |
| 2 | Đọc tài liệu và phân tích yêu cầu | Nghiên cứu mô hình hệ thống, PSO | Đọc tài liệu GA, tổng hợp cách mã hóa nghiệm | Đọc tài liệu WOA, tổng hợp cách đánh giá | Bảng tổng hợp tài liệu và các phương án mô hình |
| 3 | Thống nhất ý tưởng và logic code | Chủ trì chốt kiến trúc, interface, quy ước | Đề xuất pipeline dữ liệu và module GA | Đề xuất metric, biểu đồ và module WOA | Sơ đồ logic, công thức mục tiêu, ràng buộc và cấu trúc code được duyệt |
| 4 | Dữ liệu và mô hình dùng chung | Cài search space, encoding, interface | Cài loader, validator, preprocessor, dữ liệu giả | Cài user/UAV model, phối hợp channel model | Pipeline đầu vào và bài toán mẫu chạy được |
| 5 | Triển khai thuật toán phần 1 | Cài particle, initialization, velocity của PSO | Cài chromosome, initialization, selection của GA | Cài whale, initialization, coefficients của WOA | Các thành phần nền của ba thuật toán và test cơ bản |
| 6 | Triển khai thuật toán phần 2 | Hoàn thiện PSO, pbest/gbest, xử lý biên | Hoàn thiện crossover, mutation, replacement, GA optimizer | Hoàn thiện encircling, spiral, exploration, WOA optimizer | GA, PSO, WOA chạy độc lập trên hàm benchmark |
| 7 | Tích hợp bài toán UAV | Tích hợp `main.py`, PSO với objective UAV | Tích hợp GA và kiểm tra dữ liệu đầu vào | Tích hợp WOA, metric và visualization | Ba thuật toán chạy được trên cùng bài toán UAV |
| 8 | Thử nghiệm và sửa lỗi | Thiết kế kịch bản, giám sát tính công bằng | Chạy GA, ghi log, kiểm tra bất thường | Chạy WOA/PSO đối chứng, tạo bảng và biểu đồ | Kết quả thô cho mọi kịch bản, danh sách lỗi đã xử lý |
| 9 | Thí nghiệm cuối và phân tích | Tổng hợp, kiểm chứng và kết luận | Phân tích GA, viết phần dữ liệu/phương pháp | Phân tích WOA/PSO, hoàn thiện notebook/biểu đồ | Bộ kết quả cuối, bảng, hình và nội dung phân tích hoàn chỉnh |
| 10 | Hoàn thành báo cáo | Ghép báo cáo, kiểm tra cấu trúc và định dạng | Rà soát lý thuyết, trích dẫn và tài liệu tham khảo | Rà soát kết quả, bảng, hình và phụ lục | Báo cáo hoàn chỉnh và bộ tài liệu sẵn sàng nộp |

## Chi tiết từng tuần

### Tuần 1 — Học kiến thức nền tảng

- Học tổng quan mạng không dây, UAV-BS, coverage và path loss.
- Hiểu metaheuristic, exploration, exploitation và convergence.
- Làm rõ sự khác nhau giữa GA, PSO và WOA.
- Tạo danh sách thuật ngữ và câu hỏi chưa rõ để thảo luận.

### Tuần 2 — Đọc và tổng hợp tài liệu

- Mỗi thành viên thêm bài báo/ghi chú vào `documents/`.
- Trích xuất cách biểu diễn nghiệm, hàm mục tiêu, ràng buộc và dataset.
- So sánh những mô hình hệ thống có thể áp dụng trong phạm vi đề tài.
- Không sao chép công thức vào code khi nhóm chưa thống nhất.

### Tuần 3 — Thống nhất ý tưởng, công thức và logic code

- Chốt đầu vào, đầu ra, số UAV và dạng dữ liệu người dùng.
- Chốt mô hình kênh, coverage, objective và penalty.
- Chốt interface chung để ba thuật toán có cùng kiểu kết quả.
- Vẽ luồng: input → preprocessing → problem → optimizer → evaluation → output.
- Chốt quy tắc đặt tên, seed, log, test và thư mục kết quả.

### Tuần 4 — Xây dựng phần dùng chung

- Hoàn thiện constants, dataset loader, validator và preprocessor.
- Tạo dữ liệu giả để không phụ thuộc dataset thật trong giai đoạn đầu.
- Cài model UAV/user, solution encoding, search space và constraints.
- Viết kiểm thử cho dữ liệu sai, nghiệm vượt biên và decode nghiệm.

### Tuần 5 — Cài đặt nền tảng GA, PSO, WOA

- Mỗi người cài các cấu trúc dữ liệu và bước khởi tạo của phần được giao.
- Tách từng toán tử ra file riêng, không viết toàn bộ thuật toán vào `optimizer.py`.
- Dùng random generator có seed để tái lập kết quả.
- Review chéo cách xử lý kích thước quần thể và giới hạn nghiệm.

### Tuần 6 — Hoàn thiện ba thuật toán

- Ghép các toán tử thành vòng lặp optimizer hoàn chỉnh.
- Kiểm thử trước trên hàm Sphere/Rastrigin đơn giản.
- Kiểm tra lịch sử hội tụ, nghiệm tốt nhất và điều kiện dừng.
- Thống nhất ngân sách đánh giá để chuẩn bị so sánh công bằng.

### Tuần 7 — Tích hợp với bài toán UAV

- Thay benchmark bằng hàm mục tiêu UAV đã thống nhất.
- Kết nối dataset, channel model, constraints và optimizer.
- Hoàn thiện `main.py` để chọn `GA`, `PSO`, `WOA` hoặc `all`.
- Kiểm tra nghiệm đầu ra có hợp lệ và coverage có hợp lý hay không.

### Tuần 8 — Chạy thử nghiệm

- Chạy nhiều seed và nhiều kịch bản user/UAV.
- Lưu cấu hình đi kèm từng kết quả để có thể tái lập.
- Xuất coverage, objective, convergence và runtime.
- Sửa lỗi, phát hiện tham số bất hợp lý và chạy lại khi cần.

### Tuần 9 — Chốt kết quả và phân tích

- Chạy bộ thí nghiệm cuối trên phiên bản code đã đóng băng.
- Tính trung bình, độ lệch chuẩn, tốt nhất và kém nhất.
- Hoàn thiện bảng, đường hội tụ, biểu đồ runtime và placement.
- Phân tích ưu/nhược điểm của từng thuật toán; không chỉ chọn thuật toán có một lần chạy tốt nhất.
- Viết xong nội dung kỹ thuật để tuần 10 không phải phát triển thêm.

### Tuần 10 — Hoàn thiện báo cáo

- Ghép các phần thành báo cáo thống nhất.
- Kiểm tra trích dẫn, đánh số bảng/hình, thuật ngữ và định dạng.
- Đối chiếu mọi kết luận với bảng và biểu đồ thực nghiệm.
- Viết tóm tắt, kết luận, hạn chế và hướng phát triển.
- Kiểm tra lần cuối file báo cáo, phụ lục code và tài liệu cần nộp.

## Theo dõi tiến độ mỗi tuần

| Tuần | Trạng thái | Vấn đề tồn tại | Hành động tiếp theo | Người xác nhận |
|---:|---|---|---|---|
| 1 | Chưa bắt đầu | | | |
| 2 | Chưa bắt đầu | | | |
| 3 | Chưa bắt đầu | | | |
| 4 | Chưa bắt đầu | | | |
| 5 | Chưa bắt đầu | | | |
| 6 | Chưa bắt đầu | | | |
| 7 | Chưa bắt đầu | | | |
| 8 | Chưa bắt đầu | | | |
| 9 | Chưa bắt đầu | | | |
| 10 | Chưa bắt đầu | | | |
