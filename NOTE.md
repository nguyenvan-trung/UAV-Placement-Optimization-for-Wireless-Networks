# Logic nghiên cứu và các quyết định thiết kế

[Trang đầu](README.md) · [Mục lục tài liệu](implementation/docs/README.md) · [Nguồn](implementation/docs/SOURCES.md)

Trang này trả lời **vì sao thiết kế như vậy**. Công thức chính thức nằm trong REPORT; cách vận hành nằm trong REPRODUCE. Study mới chưa có kết quả.

## Mục lục

1. [Mô hình lập luận](#logic)
2. [Từ câu hỏi đến thí nghiệm](#cau-hoi)
3. [Bảng thiết kế biến thể](#bien-the)
4. [Đại lượng đo và cách kết luận](#danh-gia)
5. [Quyết định đã chốt và còn mở](#quyet-dinh)
6. [Nguồn ý tưởng và phần nhóm tự thiết kế](#tham-khao)

<a id="logic"></a>

## 1. Mô hình lập luận

![Quy trình từ chốt thiết kế tới thực thi, bảng và bằng chứng](implementation/docs/assets/study.svg)

**Giải thích:** câu hỏi nghiên cứu quyết định những case phải chạy; thiết kế được giữ trước khi nhìn kết quả; sau thực thi mới tổng hợp và nhận xét. Không chọn case hoặc seed chỉ vì chúng làm phương án đề xuất thắng.

Sơ đồ do nhóm tài liệu biên soạn từ giao thức hiện có. Các khối “kiểm tra đủ” và “đánh giá” là yêu cầu cần xác minh, không phải xác nhận toàn study đã được kiểm chứng.

<a id="cau-hoi"></a>

## 2. Từ câu hỏi đến thí nghiệm

| Câu hỏi | Cách kiểm tra | Bằng chứng cần có |
|---|---|---|
| I-WOA so với các phương pháp khác thế nào? | Sáu thuật toán chính trên cùng dataset/seed | Fitness và C/E/I, FE, thời gian |
| K/O/L đóng góp gì? | Bật/tắt một thành phần trong từng họ | Chênh lệch ghép cặp |
| Bản lai cải thiện nhờ bước nào? | Tắt crossover/mutation hoặc lực hút nhánh PSO | Các case bản lai và đối chứng gốc |
| Có phụ thuộc may rủi seed không? | Lặp seed trên cùng dataset | SD, median, min/max theo dataset |
| Có phụ thuộc quy mô/phân bố không? | Phân tầng dữ liệu đúng nhãn | Bảng theo quy mô; study phân bố FE riêng |
| Trọng số có làm đổi hạng không? | Tối ưu lại với cấu hình khác | Nhánh sensitivity, không chỉ chấm lại nghiệm |

K/O/L lần lượt là K-Means, Opposition-Based Learning và Lévy Flight. Giải thích thuật ngữ tại [GLOSSARY](implementation/docs/GLOSSARY.md).

<a id="bien-the"></a>

## 3. Bảng thiết kế biến thể

| Tổ hợp | K | O | L | Áp dụng trên |
|---|:---:|:---:|:---:|---|
| Gốc | Không | Không | Không | WOA, PSO, GA |
| K | Có | Không | Không | Cả ba họ |
| O | Không | Có | Không | Cả ba họ |
| L | Không | Không | Có | Cả ba họ |
| KO | Có | Có | Không | Cả ba họ |
| KL | Có | Không | Có | Cả ba họ |
| OL | Không | Có | Có | Cả ba họ |
| KOL | Có | Có | Có | WOA-KOL đặt tên I-WOA |

Bảng tạo 24 case. Cộng H-PSO-GA, H-WOA-PSO và bốn ablation của hai bản lai thành 30 case. Case gốc dùng chung cho nhiều bảng. Bảng tên case và quy tắc chính xác: [NOTEBOOK_STUDY](implementation/docs/NOTEBOOK_STUDY.md).

Ví dụ logic: để đo K trong bối cảnh đã có O, so KO với O; không so KO với L vì đồng thời đổi nhiều thành phần. Hiệu quả có thể tương tác, nên không cộng các đóng góp riêng để đoán kết quả KOL.

<a id="danh-gia"></a>

## 4. Đại lượng đo và cách kết luận

Hàm F=0,6C−0,2E−0,2I ưu tiên coverage theo một lựa chọn trọng số. Một phương án F cao hơn vẫn có thể tốn thời gian/FE hơn. Vì vậy cần đọc đồng thời:

| Góc nhìn | Đại lượng | Câu hỏi |
|---|---|---|
| Chất lượng | Fitness, C/E/I | Phục vụ được bao nhiêu user và đánh đổi gì? |
| Chi phí | FE, thời gian theo phạm vi đo | Mất bao nhiêu tính toán? |
| Ổn định | SD/median giữa seed trong từng dataset | Có phụ thuộc một lượt may mắn? |
| Theo quy mô | Các chỉ số ở 50–500 user | Phương án nào phù hợp điều kiện nào? |
| Bằng chứng | Manifest, task, phép gộp, kiểm định phù hợp | Có truy nguồn và suy luận đúng không? |

Best cao nhất trong một run không thay mean/median trên toàn thiết kế. IQR không phải CI. Hạng trung bình là mô tả; notebook chưa có kiểm định cho 30 case. Không kết luận tối ưu toàn cục từ đường hội tụ phẳng.

<a id="quyet-dinh"></a>

## 5. Quyết định đã chốt và còn mở

| Hạng mục | Trạng thái |
|---|---|
| 500 CSV sẵn có, 4 UAV, P=25, 100 vòng | Thiết kế hiện tại |
| Vòng 35/80 | Đọc từ history của lần chạy 100 vòng |
| Lưu tọa độ và chỉ số mỗi mốc | Có mã quan sát 101 mốc |
| Danh sách seed | Chưa chốt |
| Sửa requirements/notebook và củng cố resume | Cần xử lý theo PRE_RUN_REVIEW |
| Chạy benchmark 500 file | Chờ duyệt riêng |
| Kết luận phương án tốt nhất | Chưa có dữ liệu để viết |

Cùng 100 vòng không có nghĩa cùng FE. Dùng lại bộ 500 CSV hiện có không đồng nghĩa dùng bộ sinh ground-user của runner FE. Không ép độ cao user về 0 khi chưa có thiết kế mới.

<a id="tham-khao"></a>

## 6. Nguồn ý tưởng và phần nhóm tự thiết kế

| Nội dung | Nguồn / phạm vi |
|---|---|
| Mô hình liên kết UAV–UE | [REPORT và nguồn A2G](implementation/docs/REPORT.md) |
| GA/PSO/WOA | [SOURCES](implementation/docs/SOURCES.md): nguồn nguyên lý và mã triển khai |
| K-Means/OBL/Lévy | Nguyên lý tham khảo; vị trí chèn và tham số trong code là lựa chọn dự án |
| F, E, I và trọng số cụ thể | Thiết kế/giả định dự án; không gán cho một bài báo |
| Thiết kế 30 case và 100 vòng | Giao thức hiện tại của dự án |
| Kết quả và thứ hạng | Chỉ lấy từ task thật sau chạy; hiện chưa có |

Đọc tiếp [REPORT](implementation/docs/REPORT.md) → chương thuật toán → [REPRODUCE](REPRODUCE.md).
