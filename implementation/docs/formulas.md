# Công thức và ranh giới triển khai

File này trả lời “công thức nằm ở đâu”, còn mã Python tương ứng nằm trong
`src/`. Mỗi tầng chỉ nhận đầu vào của tầng trước và không tự đọc CSV.

## Pipeline

```text
data/stores/*.csv
  -> input/
  -> preprocessing/ (K-Means)
  -> physics/
  -> objectives/
  -> problem/
  -> algorithms/
  -> evaluation/
  -> results/
```

## Phân chia công thức

### 1. `src/physics/`

Đặt các hàm vật lý dùng chung:

- khoảng cách 3D `d_ij`;
- góc ngẩng `theta_ij`;
- xác suất LoS;
- pathloss LoS/NLoS và pathloss kỳ vọng;
- SNR.

Tầng này không biết GA, PSO, WOA hay cách lưu CSV.

### 2. `src/objectives/`

Đặt các hàm mục tiêu:

- `f1`: tỷ lệ phủ sóng;
- `f2`: năng lượng;
- `f3`: diện tích giao thoa;
- fitness có trọng số `w1*f1 - w2*f2 - w3*f3`.

Tầng này gọi `physics/` nhưng không tự tạo quần thể.

### 3. `src/problem/`

Đặt biểu diễn nghiệm, giới hạn `x/y/z`, kiểm tra ràng buộc và hàm phạt.
Đây là nơi bảo đảm mọi thuật toán đánh giá cùng một bài toán.

### 4. `src/preprocessing/`

Đặt K-Means, chuẩn bị tâm cụm và chuyển tâm cụm thành nghiệm khởi tạo.
K-Means không được đặt trong `algorithms/` vì nó là tiền xử lý dùng chung cho
I-WOA và các thí nghiệm khởi tạo.

### 5. `src/algorithms/`

Chỉ chứa cơ chế tìm kiếm:

- WOA gốc;
- I-WOA với OBL và Levy Flight;
- PSO;
- GA.

Thuật toán nhận problem/objective qua interface, không đọc file và không vẽ
biểu đồ.

## Quy tắc thêm module

1. Hàm đọc/kiểm tra dữ liệu vào `input/`.
2. Hàm biến đổi dữ liệu trước tối ưu vào `preprocessing/`.
3. Công thức miền không phụ thuộc thuật toán vào `physics/` hoặc `objectives/`.
4. Vòng lặp tìm kiếm vào `algorithms/`.
5. Tổng hợp nhiều lần chạy và Wilcoxon vào `evaluation/`.
6. File CSV/JSON/PNG sinh ra chỉ vào `results/` hoặc `data/views/`.
