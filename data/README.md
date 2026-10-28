# Quy ước dữ liệu đầu vào

[Trang đầu](../README.md) · [Mục lục](../implementation/docs/README.md) · [Schema](../implementation/docs/DATA_FORMAT.md)

Thư mục này chứa dữ liệu đầu vào. CSV dùng cho notebook nằm ở `stores/`; hình quan sát nằm ở `views/`.

Mỗi CSV có các cột user_id, x_m, y_m, z_m, demand. Tọa độ là vị trí user, không phải nghiệm UAV. Đọc/kiểm tra tại src/input; tiền xử lý bỏ user_id trùng và không ép z_m về 0.

Study hiện tại dùng 200 file có sẵn; không cần sinh lại. Thay dữ liệu làm thay đổi giao thức và chữ ký resume. Dữ liệu FE từ scenarios.py là luồng khác, xem [STABILITY](../implementation/docs/STABILITY.md).

Bộ hiện tại gồm 5 mức: 100, 200, 300, 400, 500 người dùng, mỗi mức 40 file. CSV được đánh số liên tục từ 001 đến 200; `views/` có 200 thư mục cùng tên với CSV, mỗi thư mục gồm `3d.png`, `front.png`, `side.png`, `top.png`.

[Danh sách chọn](dataset_selection_200.json) lưu seed lựa chọn 20261027 và các file giữ/xóa; [bảng đổi tên](dataset_renaming_200.csv) đối chiếu tên gốc với tên hiện tại. Không dùng chỉ số đầu tên file để suy ra số người dùng.

Hình top/front/side/3d chỉ minh họa dataset, không được dùng làm đầu vào optimizer và không chứng minh hiệu quả thuật toán.
