# Kiểm toán fitness: lịch sử, trạng thái và giới hạn

## Mục lục

1. [Lịch sử kiểm toán nền](#doc-section-01)
2. [Trạng thái nhìn từ mã hiện tại](#doc-section-02)
3. [Những điều cần hiểu khi đọc công thức](#doc-section-03)
4. [Nguồn cần đối chiếu](#doc-section-04)
5. [Khi có yêu cầu kiểm tra lại](#doc-section-05)


[Mục lục](README.md) · [Mô hình](REPORT.md) · [Schema](DATA_FORMAT.md) · [Bằng chứng](REPORT_EVIDENCE.md)

Phạm vi là kiểm tra công thức, số học và giả định. Kiểm tra số học đạt không chứng minh mô hình vật lý đúng. Đây không phải bảng so sánh thuật toán.

<a id="doc-section-01"></a>

## Lịch sử kiểm toán nền

Bản ngày 24/10/2026 ghi 15/17 ca đạt và hai phát hiện: biên độ cao tùy chỉnh không truyền xuống E; vị trí UAV trùng nhau vẫn nhận fitness hữu hạn. Đó là ghi nhận trước sửa, không phải kết quả chạy lại trên code hiện tại.

Một phần ghi chú cũ có số đạt sau sửa nhưng không được xác nhận lại trong lượt tài liệu này; không dùng nó làm trạng thái kiểm thử hiện hành. Không chạy audit/test trong đợt chỉ chỉnh Markdown.

<a id="doc-section-02"></a>

## Trạng thái nhìn từ mã hiện tại

[objective.py](../src/problem/objective.py) đã truyền min/max altitude và kiểm tra khoảng cách UAV; [metrics.py](../src/objectives/metrics.py) nhận biên chuẩn hóa. Khoảng cách mặc định 10 m là giả định mô phỏng có thể cấu hình, không phải tiêu chuẩn vận hành.

evaluate clip tọa độ vào miền trước khi kiểm tra khoảng cách. is_feasible kiểm tra nghiệm được truyền vào; evaluate_detailed từ chối nghiệm không khả thi. Sửa mã không đồng nghĩa dữ liệu lịch sử đã được chạy lại với ràng buộc mới.

<a id="doc-section-03"></a>

## Những điều cần hiểu khi đọc công thức

| Thành phần | Ý nghĩa và giới hạn |
|---|---|
| Khoảng cách | Euclid 3D dùng z của cả UAV và user; có bảo vệ số học |
| Góc | Chuyển sang độ trước công thức LoS; góc âm bị ép về 0, cần thẩm định với user cao hơn UAV |
| LoS/pathloss | Xác suất theo góc và suy hao trung bình theo dB; không lấy mẫu fading/LoS từng liên kết |
| SNR | Ptx[dBm] − pathloss[dB] − noise[dBm]; chưa tính nhiễu liên UAV |
| C | Phần user có ít nhất một UAV đạt ngưỡng; không bảo đảm dung lượng |
| E | Proxy công suất trung bình chuẩn hóa; không có thời gian nên không phải Joule |
| I | Phần user có từ hai liên kết đạt ngưỡng; không phải công suất nhiễu hoặc diện tích |
| F | Tổng 0,6C−0,2E−0,2I; trọng số là lựa chọn thiết kế |

Ví dụ số học 30−116−(−104)=18 dB chỉ minh họa đơn vị. Nó không chứng minh ngưỡng 18 dB là chuẩn QoS chung.

<a id="doc-section-04"></a>

## Nguồn cần đối chiếu

Danh mục ứng viên nằm trong [documents](../../documents/README.md); chưa đọc lại nguồn ngoài trong đợt này. Cần tách công thức kế thừa với phần nhóm đề xuất.

- [Alzenad và cộng sự](https://arxiv.org/pdf/1705.03415): ứng viên đối chiếu LoS, pathloss và phủ sóng; không dùng làm nguồn cho toàn bộ fitness.
- [Mozaffari và cộng sự](https://arxiv.org/pdf/1606.01962): ứng viên về nhiều UAV/vùng phủ/nhiễu; không tự suy ra I hiện tại.
- [Zeng và cộng sự](https://arxiv.org/pdf/1804.02238): hướng năng lượng vật lý mở rộng, chưa phải mô hình E hiện tại.

Cần giải trình nguồn/giả định của công suất hover 100 W, hệ số tăng 50%, noise −104 dBm, trọng số, ngưỡng và tính phù hợp với user 3D. Không đổi SNR thành SINR hoặc E thành mô hình mới rồi gộp kết quả cũ.

<a id="doc-section-05"></a>

## Khi có yêu cầu kiểm tra lại

[audit_fitness.py](../scripts/audit_fitness.py) in JSON từng ca và trả mã lỗi nếu có phát hiện. Khi thực thi sau này, lưu source/config và output thực, cập nhật ngày/số ca từ log thay vì sửa theo dự đoán.

Đọc tiếp [REPORT](REPORT.md) cho giới hạn nghiên cứu, [EXPERIMENT_DESIGN](EXPERIMENT_DESIGN.md) cho FE hoặc [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md) cho study hiện tại.
