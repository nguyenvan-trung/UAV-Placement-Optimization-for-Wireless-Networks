# Quy ước dữ liệu đầu vào

[Trang đầu](../README.md) · [Mục lục](../implementation/docs/README.md) · [Schema](../implementation/docs/DATA_FORMAT.md)

Thư mục này chứa dữ liệu đầu vào. CSV dùng cho notebook nằm ở `stores/`; hình quan sát nằm ở `views/`.

Mỗi CSV có các cột user_id, x_m, y_m, z_m, demand. Tọa độ là vị trí user, không phải nghiệm UAV. Đọc/kiểm tra tại src/input; tiền xử lý bỏ user_id trùng và không ép z_m về 0.

Study hiện tại dùng 500 file có sẵn; không cần sinh lại. Thay dữ liệu làm thay đổi giao thức và chữ ký resume. Dữ liệu FE từ scenarios.py là luồng khác, xem [STABILITY](../implementation/docs/STABILITY.md).

Hình top/front/side/3d chỉ minh họa dataset, không được dùng làm đầu vào optimizer và không chứng minh hiệu quả thuật toán.
