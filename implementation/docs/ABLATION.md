# Ablation: thiết kế đo đóng góp thành phần

## Mục lục

1. [Hai phạm vi đã có mã](#doc-section-01)
2. [Thiết kế K/O/L](#doc-section-02)
3. [Cặp đối chiếu](#doc-section-03)
4. [Bản lai](#doc-section-04)
5. [Chi phí và diễn giải](#doc-section-05)


[Mục lục](README.md) · [Thuật ngữ](GLOSSARY.md) · [Study notebook](NOTEBOOK_STUDY.md)

Ablation so sánh các trường hợp chỉ khác thành phần cần đánh giá. Chạy I-WOA đầy đủ so với GA/PSO chỉ cho biết khác biệt giữa phương pháp, chưa chỉ ra đóng góp riêng K-Means, OBL hoặc Lévy.

<a id="doc-section-01"></a>

## Hai phạm vi đã có mã

| Luồng | Các biến thể | Dữ liệu và ngân sách |
|---|---|---|
| Notebook hiện tại | Tám case mỗi họ WOA/PSO/GA và ablation hai bản lai | 500 CSV có sẵn, 100 vòng |
| FE ablation | Tám tổ hợp K/O/L của I-WOA trong benchmark.yaml | Kịch bản sinh từ manifest, cùng max_fe |

Hai luồng độc lập. Phần này không còn coi runner FE hoặc counter là chưa triển khai. Chưa có study mới hoàn tất để tính đóng góp thực nghiệm.

<a id="doc-section-02"></a>

## Thiết kế K/O/L

| Tổ hợp | K-Means | OBL | Lévy |
|---|:---:|:---:|:---:|
| Gốc | Không | Không | Không |
| K | Có | Không | Không |
| O | Không | Có | Không |
| L | Không | Không | Có |
| KO | Có | Có | Không |
| KL | Có | Không | Có |
| OL | Không | Có | Có |
| KOL | Có | Có | Có |

Trong notebook, áp dụng bảng này cho ba họ; KOL của WOA được đặt tên I-WOA. Quy tắc chèn toán tử và quản lý pbest/vận tốc nằm tại [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md), không suy ra bằng cách đổi tên thuật toán.

<a id="doc-section-03"></a>

## Cặp đối chiếu

| Thành phần | Các so sánh bật trừ tắt trong từng họ |
|---|---|
| K | K−gốc; KO−O; KL−L; KOL−OL |
| O | O−gốc; KO−K; OL−L; KOL−KL |
| L | L−gốc; KL−K; OL−O; KOL−KO |

Có 12 cặp mỗi họ, tổng 36 cặp. Giữ dataset/seed ghép cặp. Chênh lệch dương về fitness có lợi cho trường hợp bật, nhưng phải đọc kèm thời gian, FE và các chỉ số riêng. Không cộng cơ học các chênh lệch để giả định hiệu quả KOL.

<a id="doc-section-04"></a>

## Bản lai

H-PSO-GA có ba case: chỉ crossover, chỉ mutation, cả hai; thêm PSO gốc làm đối chứng. H-WOA-PSO có bản đầy đủ và hai case bỏ lực hút pbest hoặc gbest trong nhánh vận tốc; thêm WOA/PSO gốc.

Nhánh WOA vẫn dùng best khi bỏ gbest trong vận tốc. Các case bản lai không có K/O/L trong thiết kế hiện tại.

<a id="doc-section-05"></a>

## Chi phí và diễn giải

K-Means không gọi fitness trực tiếp nhưng tốn thời gian. OBL/Lévy gọi thêm fitness, kể cả ứng viên không được nhận. So sánh 100 vòng phải công bố FE thực tế; đối chứng cùng FE cần luồng FE riêng.

Bảng contribution notebook là mô tả ghép cặp; chưa có kiểm định/CI cho 30 case. Analyzer ablation FE chuyên biệt vẫn chưa có. Không gọi kiểm tra số học, test tương đương hoặc smoke là kết quả ablation nghiên cứu.

Đọc tiếp [STATISTICS](STATISTICS.md) cho phạm vi suy luận và [REPORT_EVIDENCE](REPORT_EVIDENCE.md) cho cách truy nguồn.
