# Notebook: code, bảng và biểu đồ cùng nơi

## Mục lục

1. [Notebook dùng cho thiết kế hiện tại](#doc-section-01)
2. [Notebook khác](#doc-section-02)


[Trang đầu](../../README.md) · [Mục lục](../docs/README.md)

<a id="doc-section-01"></a>

## Notebook dùng cho thiết kế hiện tại

[full_study_100_iterations.ipynb](full_study_100_iterations.ipynb) trình bày 30 case trên 500 CSV, 100 vòng. Logic chính được gọi từ notebook_study.py, không chép lại toàn bộ thuật toán vào các ô.

Thứ tự ô: thiết lập → bảng thiết kế → ô chạy có khóa → đọc bảng → hội tụ → kết quả theo quy mô → nghiệm 3D → hướng dẫn đánh giá.

**Chưa chạy study.** Ô chạy mặc định CONFIRM_RUN=False; seed trong config để trống. Mở file hoặc đọc Markdown không khởi chạy. Chỉ thực thi khi được yêu cầu.

Hướng dẫn đầy đủ và bảng case: [NOTEBOOK_STUDY](../docs/NOTEBOOK_STUDY.md). Schema đầu ra: [DATA_FORMAT](../docs/DATA_FORMAT.md). Môi trường/kernel: [REPRODUCE](../../REPRODUCE.md).

<a id="doc-section-02"></a>

## Notebook khác

comparison_experiment.ipynb là notebook so sánh trước đó, không phải điểm vào study 30 case. Không giả định nó đọc được schema mới. Không chạy script tạo kết quả cũ chỉ để mở notebook mới.

Tọa độ và số liệu trong bảng/ảnh phải lấy từ task thật. Các ô phân tích của notebook mới đọc lại artifact, không gọi optimizer để vẽ lại.
