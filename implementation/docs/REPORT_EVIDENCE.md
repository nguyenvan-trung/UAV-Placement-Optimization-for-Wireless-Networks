# Danh sách kiểm tra truy xuất số liệu

[Mục lục](README.md) · [Người mới](PROJECT_GUIDE.md) · [Thuật ngữ](GLOSSARY.md) · [Study notebook](NOTEBOOK_STUDY.md)


Ledger lịch sử được sinh bằng `python implementation/scripts/build_report_evidence.py`; không chạy lại công cụ chỉ để đọc trang này. Công cụ/CSV cũ không tự bao phủ study notebook mới.
CSV kèm theo chỉ rõ file, dòng CSV (header là dòng đầu), cột, giá trị và
phân loại. Không dùng dữ liệu trong statistics_test_artifacts làm nguồn.

- [x] Rút các số liệu benchmark cũ khỏi các chương DW.
- [x] Phân biệt tham số/công thức định trước với kết quả đo.
- [x] Log kiểm toán truy được đến từng dòng, nhưng không phải benchmark.
- [x] Bộ số liệu lịch sử do người dùng cung cấp được đánh dấu chưa xác minh.
- [x] Không đồng nhất độ phủ gần toàn bộ với mọi UE đạt ngưỡng.
- [x] Không khẳng định thứ hạng hoặc nguyên nhân từ mô tả toán tử.
- [ ] Có runs.csv benchmark FE thật và manifest đầy đủ.
- [ ] Mỗi ô kết quả mới truy đến tập dòng nguồn sau lọc/gộp, kèm script,
  hash dữ liệu và cấu hình; không chỉ dẫn tới một bảng trung gian.
- [ ] Có ue_pass/ue_total cho từng run và cách gộp rõ ràng.
- [ ] Có CPU/worker/wall/CPU tổng/FE và phạm vi đo từ batch thật.
- [ ] Có kiểm định, CI và effect size cho kết luận so sánh.
- [ ] Sinh viên xác nhận đọc nguồn trước khi đưa trích dẫn vào bản nộp.

**Giới hạn:** báo cáo tổng hợp hiện chưa đưa số đo benchmark vào nên chưa
thể hoàn tất các mục còn trống. Đây là ledger kiểm toán đầu vào hiện có,
không tự chứng nhận mọi số trong toàn bộ tài liệu dự án. Các số trong
công thức và mã giả là định nghĩa; cần dẫn code/cấu hình, không gán giả
cho một dòng log thực nghiệm.

## Bằng chứng cho notebook 100 vòng

Khi có lần chạy thật, mỗi bảng phải truy ngược đến manifest, tập task JSON dataset–case–seed, trường result/history và phép gộp trong notebook_study.py. Giữ chữ ký source/config/data và danh sách seed. completion.json xác nhận số task theo thiết kế nhưng không tự chứng minh mô hình vật lý hoặc độc lập thống kê.

Trước khi đưa kết quả vào báo cáo, kiểm tra đủ cặp, nghiệm khả thi, định nghĩa best/mean/SD, mốc vòng, FE và phạm vi thời gian. Phần nhận xét phải dùng đúng dữ liệu đã chạy, không lấy kết quả test hoặc ảnh scenario thay thế.

Notebook hiện chưa lưu đầy đủ metadata môi trường như env.json của runner FE. Nêu giới hạn này nếu tuyên bố tái lập; không suy ra hai luồng cùng mức truy vết.

Chi tiết ledger lịch sử: [REPORT_EVIDENCE.csv](REPORT_EVIDENCE.csv). Lộ trình nguồn kết quả mới: [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md) → [DATA_FORMAT](DATA_FORMAT.md) → bảng/task → báo cáo.
