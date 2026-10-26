# Phạm vi sửa báo cáo

## Mục lục

1. [Bố cục phục vụ đọc trên GitHub](#doc-section-01)
2. [Đồng bộ tài liệu ngày 25/10/2026](#doc-section-02)


[Mục lục](README.md) · [Người mới](PROJECT_GUIDE.md) · [Thuật ngữ](GLOSSARY.md) · [Study notebook](NOTEBOOK_STUDY.md)


Trang ghi lịch sử biên tập, không phải log chạy thí nghiệm. Bảng dưới mô tả đợt hiệu chỉnh báo cáo trước; phần cập nhật mới nêu phạm vi hiện tại.

| File | Vị trí | Lý do và tác động |
|---|---|---|
| DWGA.md, DWPSO.md, DWWOA.md | Mục thực nghiệm và hỏi đáp cũ | Rút số liệu/thứ hạng thiếu log; không dùng làm bằng chứng nghiên cứu |
| DWH_PSO_GA.md, DWH_WOA_PSO.md | Mục thực nghiệm và hỏi đáp cũ | Rút khẳng định ưu thế, nguyên nhân và khả năng triển khai chưa được kiểm chứng |
| DWI_WOA.md | Động lực, K-Means, OBL, bảng kết quả, hỏi đáp | Bỏ khẳng định toàn cục; mô tả lại khởi tạo theo code; rút bảng cũ |
| DWH_WOA_PSO.md | Công thức phối hợp vị trí | Khớp tổ hợp vị trí WOA và vị trí sau PSO trong code hiện tại |
| DWPSO.md, DWH_PSO_GA.md | Trọng số quán tính | Nêu lịch giảm theo vòng lặp hiện tại thay vì hằng số trong parameter class |
| Các file DW | Tài liệu tham khảo | Đánh dấu ứng viên cần sinh viên tự đọc xác minh |
| formulas.md | f2/f3 và K-Means | Đổi mô tả thành proxy công suất, proxy chồng lấn; làm rõ cách optimizer gọi K-Means |
| REPORT.md | Toàn bộ bản tổng hợp | Đủ mục thầy yêu cầu, không điền giả số liệu benchmark chưa có |
| REPORT_EVIDENCE.md/.csv | Checklist và ledger | Phân loại nguồn; truy đến file, dòng CSV và cột |
| PROMPTS.md | Nhiệm vụ 6 | Lưu nguyên văn yêu cầu |

Các heading trong file là mốc nội dung; dòng cụ thể xem diff của workspace.
Các số đo mới phải chờ kết quả đúng giao thức (notebook hoặc FE), không gộp hai loại ngân sách. Kiểm định cho 30 case notebook chưa có.

<a id="doc-section-01"></a>

## Khởi chạy study theo xác nhận người dùng

Người dùng chọn 30 seed, 450.000 task. Đã sửa requirements, validator artifact/resume, metadata môi trường, progress và lưu JSON gzip theo bucket. Thêm coordinator bốn subprocess cùng bộ xuất báo cáo/notebook; cập nhật notebook đọc task nén. 83 kiểm tra đạt và 90 task kiểm tra thật xác nhận pipeline xuất 12 bảng/13 hình. Study chính thức đang chạy; trạng thái trực tiếp ở RUN_STATUS.md. Không dùng kết quả kiểm tra để thay kết quả cuối.

## Bố cục phục vụ đọc trên GitHub

Sau khi người dùng cung cấp ảnh lỗi “The following macros are not allowed: operatorname”, đã thay 8 vị trí trong REPORT, DWGA, DWPSO, DWI_WOA, DWH_PSO_GA và DWH_WOA_PSO bằng cách viết math roman đơn giản. Bổ sung định nghĩa clip và quy tắc tránh macro này. Kiểm tra cấu trúc trước đó chưa bao phủ danh sách macro GitHub chấp nhận; chưa coi sửa cục bộ là đã xác nhận render của commit trên GitHub.

Rà soát kỹ lần tiếp theo: đổi ký hiệu đếm tập trong GA thành card(S) và giải thích; đơn giản hóa ngoặc của clip; dùng geq cho bất đẳng thức. Cả 41 khối toán được parser math độc lập chấp nhận và đã dựng/xem bốn trang ảnh preview cục bộ, không thấy công thức bị cắt. Kiểm tra lại 38 Markdown, 628 tham chiếu nội bộ và XML của 9 SVG không phát hiện đích thiếu. Preview dùng Matplotlib, không phải renderer GitHub. Công cụ web không truy cập được hai trang nhánh Trung_SICT trong lần kiểm tra, nên chưa xác nhận bản hiển thị từ xa. Không commit/push hoặc chạy optimizer.

Viết lại bốn file gốc, REPORT và sáu chương thuật toán theo cấu trúc: SVG lớn → cách đọc → bước xử lý → công thức ngắn → ký hiệu/đơn vị → nguồn/code. Thêm SOURCES và DOCUMENTATION_GUIDE. Math block đặt riêng ngoài danh sách/bảng; ảnh cần commit cùng Markdown. Không thay code, seed hoặc chạy optimizer.

Nguồn được đối chiếu trong phạm vi truy cập được, không tuyên bố đã đọc mọi toàn văn. E/I/F riêng, quy tắc hybrid và tham số được ghi theo code thay vì gán cho bài báo.

Kiểm tra tài liệu cục bộ: 38 Markdown, 628 tham chiếu nội bộ, 201 anchor, 40 khối toán và 9 SVG. Parse/link/anchor/cột bảng/UTF-8/XML và đo chiều rộng chữ SVG không phát hiện lỗi trong phạm vi kiểm tra. Chưa preview một commit trên GitHub, chưa commit/push; cần đưa cả ảnh SVG và các file Markdown mới lên cùng nhánh. Không chạy test thuật toán hoặc benchmark.

<a id="doc-section-02"></a>

## Đồng bộ tài liệu ngày 25/10/2026

- Viết lại README, PROJECT_GUIDE, NOTE và TALK theo trạng thái thực; bỏ liên kết kết quả 35/80 đã xóa và kết luận thắng thiếu log.
- Thêm [mục lục](README.md), [thuật ngữ](GLOSSARY.md) và các liên kết giữa phương pháp, thiết kế, schema, thống kê và bằng chứng.
- Sửa tiếng Việt bị mất dấu trong NOTEBOOK_STUDY; phân biệt 30 case/100 vòng với luồng FE.
- Đồng bộ ABLATION, STABILITY, SENSITIVITY, hướng dẫn scripts/notebooks/results/datasets và kế hoạch.
- Gắn nhãn kiểm toán nền và yêu cầu lịch sử để người đọc không nhầm với trạng thái hiện tại.
- Chỉ chỉnh tài liệu Markdown; không chạy notebook, optimizer, test hoặc benchmark trong đợt này.

Khi cập nhật sau này, sửa trang chuyên trách trước rồi đồng bộ mục lục/README. Không thêm thông báo “phần bên dưới đã lỗi thời” để giữ lại hai mô tả trạng thái mâu thuẫn trong cùng trang.
