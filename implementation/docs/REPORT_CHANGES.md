# Phạm vi sửa báo cáo

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

## Đồng bộ tài liệu ngày 25/10/2026

- Viết lại README, PROJECT_GUIDE, NOTE và TALK theo trạng thái thực; bỏ liên kết kết quả 35/80 đã xóa và kết luận thắng thiếu log.
- Thêm [mục lục](README.md), [thuật ngữ](GLOSSARY.md) và các liên kết giữa phương pháp, thiết kế, schema, thống kê và bằng chứng.
- Sửa tiếng Việt bị mất dấu trong NOTEBOOK_STUDY; phân biệt 30 case/100 vòng với luồng FE.
- Đồng bộ ABLATION, STABILITY, SENSITIVITY, hướng dẫn scripts/notebooks/results/datasets và kế hoạch.
- Gắn nhãn kiểm toán nền và yêu cầu lịch sử để người đọc không nhầm với trạng thái hiện tại.
- Chỉ chỉnh tài liệu Markdown; không chạy notebook, optimizer, test hoặc benchmark trong đợt này.

Khi cập nhật sau này, sửa trang chuyên trách trước rồi đồng bộ mục lục/README. Không thêm thông báo “phần bên dưới đã lỗi thời” để giữ lại hai mô tả trạng thái mâu thuẫn trong cùng trang.
