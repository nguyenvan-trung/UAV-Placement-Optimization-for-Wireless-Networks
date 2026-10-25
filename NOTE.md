# Ghi chú nghiên cứu và quyết định thiết kế

[Trang đầu](README.md) · [Mục lục](implementation/docs/README.md)

Trang này ghi các quyết định và câu hỏi nghiên cứu. Công thức chuẩn nằm trong [REPORT](implementation/docs/REPORT.md); cách chạy nằm trong [REPRODUCE](REPRODUCE.md). Ghi chú không phải bảng kết quả thực nghiệm.

## Câu hỏi nghiên cứu

1. Sáu thuật toán chính khác nhau thế nào về chất lượng và chi phí?
2. K-Means, OBL và Lévy đóng góp gì trên WOA, PSO và GA?
3. Các thành phần trong hai thuật toán lai đóng góp gì?
4. Kết quả thay đổi theo quy mô user và seed ra sao?
5. Đổi trọng số hoặc tiêu chí phủ sóng có làm đổi thứ hạng không?

Câu 1–4 thuộc [study notebook](implementation/docs/NOTEBOOK_STUDY.md). Câu 5 có [thiết kế độ nhạy](implementation/docs/SENSITIVITY.md) riêng.

## Quyết định hiện tại

| Quyết định | Phạm vi |
|---|---|
| Notebook 100 vòng | Code, bảng và ảnh cùng nơi |
| 500 CSV có sẵn | Không tự thay bằng bộ sinh scenario |
| 4 UAV, quần thể 25 | Cố định giữa các trường hợp |
| 30 trường hợp | 24 cấu hình ba họ + hai bản lai + bốn ablation bản lai |
| Seed chưa chốt | Không tự chọn rồi khởi chạy |
| Lưu 101 mốc | Vòng 0 sau khởi tạo và vòng 1–100 |
| Không chạy riêng 35/80 | Lấy checkpoint của lần chạy 100 vòng |
| Ghi FE và thời gian | Cùng số vòng vẫn có chi phí khác nhau |

## Điều chưa được chứng minh

K-Means tạo một nghiệm mầm, không chứng minh tối ưu. OBL và Lévy bổ sung ứng viên, không bảo đảm cải thiện trên mọi dataset. Hội tụ hoặc SD nhỏ không chứng minh tối ưu toàn cục.

Fitness là tổng có trọng số, chưa phải phương pháp tìm mặt Pareto. E là proxy công suất; I là proxy chồng lấn theo user. Các tham số mô phỏng không tự trở thành chuẩn vận hành mạng.

Không dùng số dataset thay số seed. Không mặc định cùng seed tạo cùng quỹ đạo khi các toán tử tiêu thụ RNG khác nhau. Xem [thuật ngữ](implementation/docs/GLOSSARY.md).

## Việc còn mở

Chốt seed; thực hiện kiểm tra optimizer khi được yêu cầu; chạy study rồi mới viết kết quả. Phân tích suy luận cho 30 trường hợp chưa có. Không lấy bảng test hoặc CSV minh họa ở figures làm chứng cứ thuật toán thắng.
