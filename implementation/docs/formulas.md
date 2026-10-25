# Công thức, luồng gọi và vị trí mã

## Mục lục

1. [Luồng một thí nghiệm](#doc-section-01)
2. [Ánh xạ](#doc-section-02)
3. [Định nghĩa dùng chung](#doc-section-03)
4. [Cơ chế thuật toán](#doc-section-04)


[Mục lục](README.md) · [Mô hình đầy đủ](REPORT.md) · [Thuật ngữ](GLOSSARY.md)

Trang này nối công thức với code. Đây là quan hệ gọi hàm, không phải các tầng tuần tự độc lập mà dữ liệu chỉ đi qua đúng một lần.

<a id="doc-section-01"></a>

## Luồng một thí nghiệm

![Mô hình tổng quan từ input tới kết quả](assets/overview.svg)

Hình thể hiện trách nhiệm các khối; bảng bên dưới dẫn đến code. Công thức và ký hiệu tại [REPORT](REPORT.md); nguồn và phần nhóm thiết kế tại [SOURCES](SOURCES.md).

```text
CSV user → loader → validator → preprocess → problem
                                            ↑
                     optimizer → đề xuất X → evaluate(X)
                                            ↓
                           physics → C/E/I → fitness
                                            ↓
                         best + history → task → bảng/ảnh
```

K-Means chỉ được optimizer gọi khi case bật K; không chạy tự động trên mọi dataset trước mọi thuật toán.

<a id="doc-section-02"></a>

## Ánh xạ

| Phần | Mã | Ý nghĩa |
|---|---|---|
| Đọc/kiểm tra | [input](../src/input/) | Schema và giá trị user |
| Tiền xử lý | [preprocessor.py](../src/preprocessing/preprocessor.py) | Bỏ user_id trùng, giữ tọa độ |
| Khoảng cách/góc/LoS/pathloss/SNR | [channel.py](../src/physics/channel.py) | Tính liên kết UAV–UE |
| C/E/I/F | [metrics.py](../src/objectives/metrics.py) | Các proxy và tổng có trọng số |
| Miền/khả thi | [objective.py](../src/problem/objective.py) | Clip vào miền rồi kiểm tra khoảng cách |
| K-Means | [kmeans_init.py](../src/preprocessing/kmeans_init.py) | Tâm cụm XY thành nghiệm mầm |
| OBL/Lévy WOA | [I_WOA](../src/algorithms/I_WOA/) | Toán tử trong I-WOA |
| OBL/Lévy GA/PSO | [enhancements.py](../src/algorithms/base/enhancements.py) | Adapter theo kiểu cá thể |
| FE | [counter.py](../src/counter.py), [budget.py](../src/algorithms/base/budget.py) | Đếm, dừng, lịch điều khiển theo FE |
| Study notebook | [notebook_study.py](../src/notebook_study.py) | Quan sát 101 mốc, artifact và bảng mô tả |
| Suy luận FE | [analyze.py](../scripts/analyze.py) | Gộp instance, kiểm định và CI |

<a id="doc-section-03"></a>

## Định nghĩa dùng chung

C là phần user được ít nhất một UAV phủ theo SNR. I là phần user có từ hai liên kết đạt ngưỡng. E là trung bình công suất proxy theo độ cao chia công suất chuẩn hóa cố định. F=0,6C−0,2E−0,2I. Chi tiết công thức và giới hạn: [REPORT](REPORT.md).

Không gọi I là diện tích giao nhau hoặc nhiễu vật lý; không gọi E là tổng năng lượng đội UAV. Thay các định nghĩa này là thay mô hình, cần thiết kế và đối chứng mới.

<a id="doc-section-04"></a>

## Cơ chế thuật toán

[GA](DWGA.md) · [PSO](DWPSO.md) · [WOA](DWWOA.md) · [I-WOA](DWI_WOA.md) · [H-PSO-GA](DWH_PSO_GA.md) · [H-WOA-PSO](DWH_WOA_PSO.md)

Các chương giải thích baseline/bản đầy đủ; quy tắc biến thể tập trung tại [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md). Thuật toán không tự đọc CSV hoặc vẽ ảnh. Các bảng thống kê chuyên biệt hiện nằm trong script analyzer hoặc notebook_study, không mặc định mọi thứ đều ở evaluation.
