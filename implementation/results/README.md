# Kết quả được sinh khi thực thi

[Cách đọc bảng, chỉ số và mức hoàn thành](READING_RESULTS.md). Kết quả sẽ được tạo trong `study_80_iterations` khi chạy lại theo yêu cầu.

## Mục lục

1. [Notebook hiện tại](#doc-section-01)
2. [Các luồng khác](#doc-section-02)


[Trang đầu](../../README.md) · [Mục lục](../docs/README.md) · [Schema](../docs/DATA_FORMAT.md)

Thư mục này dành cho đầu ra. Study đã dừng; toàn bộ kết quả, log và checkpoint đã được xóa theo yêu cầu. Hiện chỉ giữ tài liệu hướng dẫn; xem [RUN_STATUS](../docs/RUN_STATUS.md).

<a id="doc-section-01"></a>

## Notebook hiện tại

Output mặc định: study_80_iterations, chỉ được tạo khi thực thi có xác nhận.

| Đường dẫn trong output | Nội dung |
|---|---|
| manifest.json | Cấu hình, case, dataset và chữ ký nội dung |
| tasks/<dataset>/<dataset>_result_<case>_seed<seed>.json.gz | Một task dataset–case–seed, result và 81 mốc history |
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

Tên kết quả theo dataset: `001_UAV_3D_50_users_connect.csv` → `tasks/001_UAV_3D_50/001_UAV_3D_50_result_GA_seed42.json.gz` (GA, seed 42). Tên file không dùng mã băm; JSON vẫn được nén gzip.

Sau khi hoàn tất runner, CSV để mở bằng Excel được xuất trong `datasets/<dataset>/`:

- `<dataset>_result.csv`: một dòng cho mỗi case × seed, gồm các chỉ số cuối cùng.
- `<dataset>_positions.csv`: tọa độ cuối cùng, một dòng cho mỗi case × seed × UAV.
- `<dataset>_convergence.csv`: lịch sử chỉ số, một dòng cho mỗi case × seed × vòng (0–80).

Ví dụ: `datasets/001_UAV_3D_50/001_UAV_3D_50_result.csv`. Các file dùng UTF-8 BOM và tỷ lệ coverage trong [0, 1]. JSON nén trong `tasks/` vẫn là checkpoint nội bộ để tiếp tục chạy và kiểm tra kết quả; CSV là bản xuất để xem và so sánh.
