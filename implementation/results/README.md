# Kết quả được sinh khi thực thi

## Mục lục

1. [Notebook hiện tại](#doc-section-01)
2. [Các luồng khác](#doc-section-02)


[Trang đầu](../../README.md) · [Mục lục](../docs/README.md) · [Schema](../docs/DATA_FORMAT.md)

Thư mục này dành cho đầu ra, không chứa dataset gốc hoặc mã thuật toán. Đầu ra smoke và batch dở trước đây đã được dọn. Hiện chưa có study notebook hoàn tất.

<a id="doc-section-01"></a>

## Notebook hiện tại

Output mặc định: study_100_iterations, chỉ được tạo khi thực thi có xác nhận.

| Đường dẫn trong output | Nội dung |
|---|---|
| manifest.json | Cấu hình, case, dataset và chữ ký nội dung |
| tasks/*.json | Một task dataset–case–seed, result và 101 mốc history |
| runs.csv | Tổng hợp lượt chạy sau khi đủ task |
| completion.json | Dấu hoàn thành với expected/actual |
| tables/*.csv và *.md | Bảng mô tả từ toàn study |
| figures/*.png | Hình xuất bởi các ô vẽ của notebook |
| .running | Khóa trong lúc chạy; không phải kết quả |

Đọc bảng chỉ khi đủ task và manifest khớp. Không dùng checkpoint dở để xếp hạng toàn thiết kế. Xem [NOTEBOOK_STUDY](../docs/NOTEBOOK_STUDY.md).

<a id="doc-section-02"></a>

## Các luồng khác

Batch cũ ghi CSV và báo cáo trực tiếp ở output-dir. Benchmark FE mặc định có thể ghi ngoài thư mục này theo config/CLI và dùng schema riêng. Các thư mục tables/figures/solutions/convergence không phải cấu trúc bắt buộc chung cho mọi runner.

Không coi ảnh minh họa, test hoặc số liệu lịch sử thiếu log là kết quả chính thức. Quy tắc truy nguồn nằm trong [REPORT_EVIDENCE](../docs/REPORT_EVIDENCE.md).
