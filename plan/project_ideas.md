# Ý tưởng và phạm vi dự kiến

## 1. Bài toán

Tìm vị trí ba chiều `(x, y, h)` của một hoặc nhiều UAV để phục vụ tập người dùng mặt đất trong khu vực cho trước.

## 2. Đầu vào dự kiến

- Tọa độ người dùng `(x, y)` và nhu cầu dịch vụ.
- Kích thước khu vực triển khai.
- Số lượng UAV.
- Giới hạn độ cao và tọa độ UAV.
- Công suất phát, ngưỡng chất lượng tín hiệu và tham số mô hình kênh.
- Tham số riêng của GA, PSO và WOA.

## 3. Đầu ra dự kiến

- Vị trí tốt nhất của từng UAV.
- Số lượng và tỷ lệ người dùng được phủ sóng.
- Giá trị hàm mục tiêu tốt nhất.
- Lịch sử hội tụ theo vòng lặp.
- Thời gian chạy của thuật toán.
- Bảng và biểu đồ so sánh GA, PSO, WOA.

## 4. Hàm mục tiêu dự kiến

Ưu tiên tối đa hóa vùng phủ sóng, đồng thời có thể bổ sung penalty cho người dùng không được phục vụ, nhiễu, công suất hoặc nghiệm vi phạm ràng buộc.

Trước khi lập trình chính thức, nhóm phải thống nhất:

1. Bài toán tối đa hóa hay tối thiểu hóa.
2. Công thức coverage và ngưỡng được phục vụ.
3. Mô hình path loss/LoS-NLoS.
4. Cách kết hợp nhiều mục tiêu và hệ số trọng số.
5. Ràng buộc vị trí, độ cao, công suất và khoảng cách UAV.

## 5. Nguyên tắc so sánh

GA, PSO và WOA phải dùng cùng:

- Một tập dữ liệu cho mỗi kịch bản.
- Một cách biểu diễn nghiệm.
- Một hàm đánh giá và cách xử lý ràng buộc.
- Cùng kích thước quần thể nếu phù hợp.
- Cùng ngân sách đánh giá hàm mục tiêu hoặc điều kiện dừng.
- Cùng danh sách random seed và số lần chạy độc lập.

## 6. Kịch bản thí nghiệm dự kiến

- Thay đổi số lượng người dùng.
- Thay đổi số lượng UAV.
- Phân bố người dùng đồng đều và phân bố theo cụm.
- So sánh coverage, objective, convergence và runtime.
- Báo cáo trung bình, độ lệch chuẩn, kết quả tốt nhất và kém nhất.

## 7. Giới hạn giai đoạn đầu

- Ưu tiên mô phỏng offline bằng Python.
- Chưa tích hợp phần cứng UAV thật.
- Chưa triển khai điều khiển quỹ đạo theo thời gian.
- Chỉ mở rộng thêm mục tiêu sau khi phiên bản một mục tiêu chạy ổn định.
