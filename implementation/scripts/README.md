# Điểm vào dòng lệnh và công cụ phân tích

## Mục lục

1. [Nếu dùng batch CSV legacy](#doc-section-01)
2. [Nếu dùng benchmark FE](#doc-section-02)


[Trang đầu](../../README.md) · [Mục lục](../docs/README.md) · [Chọn luồng chạy](../../REPRODUCE.md)

Các script gọi logic trong src. Bảng này là hướng dẫn tìm tệp, không phải danh sách lệnh đã thực thi. Thiết kế hiện tại dùng [notebook 80 vòng](../docs/NOTEBOOK_STUDY.md); không chạy các script khác chỉ vì muốn mở notebook.

| Script | Đầu vào / vai trò | Đầu ra hoặc tài liệu liên quan |
|---|---|---|
| generate_dataset.py | Sinh CSV/hình user khi chủ động đổi bộ dữ liệu | data/stores, data/views; 200 CSV hiện đã có |
| run_optimizer.py | Một CSV, chọn thuật toán | Metric và hình theo tùy chọn |
| run_experiments.py | Nhiều seed trên CSV | So sánh theo cơ chế script này, không thay study mới |
| run_batch.py | Nhiều CSV, mặc định sáu thuật toán | CSV batch, summary, báo cáo và ảnh |
| run_benchmark.py | YAML + seed manifest, dữ liệu sinh mới, ngân sách FE | runs/convergence/solutions/env/completion |
| generate_seeds.py | Cấu hình FE | Manifest seed, không phải kết quả tối ưu |
| analyze.py | Log FE sáu thuật toán | Thống kê theo instance; [STATISTICS](../docs/STATISTICS.md) |
| analyze_stability.py | Log FE sáu thuật toán | Quy mô/phân bố/độ ổn định; [STABILITY](../docs/STABILITY.md) |
| analyze_sensitivity.py | Log FE nhiều cấu hình fitness | [SENSITIVITY](../docs/SENSITIVITY.md) |
| audit_fitness.py | Kiểm tra số học mô hình | JSON kiểm toán, không phải benchmark |
| plot_scenarios.py | Sinh minh họa năm phân bố | figures, không phải kết quả thuật toán |
| build_report_evidence.py | Dữ liệu kiểm toán/báo cáo hiện có | Ledger; không tự xác nhận nghiên cứu mới |
| build_fitness_audit_report.py | Tổng hợp kiểm toán fitness | Báo cáo kiểm toán |
| build_presentation.py | Dựng tài liệu trình bày | Cần rà nội dung/nguồn trước khi dùng |
| revise_report_docs.py | Công cụ chỉnh tài liệu cũ | Không tự chạy; có thể ghi đè biên tập hiện tại |
| run_scalability_analysis.py | Công cụ phân tích quy mô trước đó | Không thay các bảng notebook mới |
| regenerate_views.ps1 | Tạo lại hình từ CSV | data/views |

Các công cụ dựng/chỉnh tài liệu có thể chứa nội dung lịch sử; sau khi chạy phải đối chiếu [REPORT_EVIDENCE](../docs/REPORT_EVIDENCE.md). Không mặc định dùng chúng sẽ giữ nguyên các chỉnh sửa Markdown mới nhất.

<a id="doc-section-01"></a>

## Nếu dùng batch CSV legacy

Các mode gồm all, representative và custom. representative lấy 10 file đầu theo thứ tự tên; chỉ coi là mỗi mức một file nếu quy tắc đặt tên thực sự bảo đảm điều đó. --limit giới hạn số file. --random-uavs thay số UAV theo dataset, khác study hiện tại cố định 4 UAV.

Batch legacy có các mặc định riêng; truyền rõ tham số thay vì coi mặc định là giao thức study. Nó không xuất đủ lịch sử 81 mốc hoặc 12 case của notebook.

<a id="doc-section-02"></a>

## Nếu dùng benchmark FE

Điểm vào gốc run_benchmark.py gọi script FE. Mode benchmark, ablation và sensitivity có schema/thuật toán hợp lệ riêng. Xem [EXPERIMENT_DESIGN](../docs/EXPERIMENT_DESIGN.md) và [DATA_FORMAT](../docs/DATA_FORMAT.md).

Analyzer chỉ đọc kết quả, nhưng lệnh optimizer, plot_scenarios hoặc generate_dataset thực sự sinh/chạy dữ liệu. Chỉ thực hiện khi có yêu cầu tương ứng.
