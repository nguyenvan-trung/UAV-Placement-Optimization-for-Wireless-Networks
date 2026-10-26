# Cách đọc kết quả

**Hiện tại:** toàn bộ kết quả đã được xóa theo yêu cầu. Các đường dẫn dưới đây mô tả cấu trúc đầu ra khi chạy lại, không phải các file đang tồn tại.

## Đọc đúng thư mục

- `pipeline_check/`: chỉ kiểm tra luồng xuất kết quả trên **1 dataset, 30 case, 1 seed**. Không đại diện cho toàn bộ 500 dataset.
- `study_100_iterations/`: kết quả study chính, **500 dataset × 30 case × 30 seed = 450.000 lượt**. Một lượt là một tổ hợp dataset–case–seed, không phải một dataset.

## Theo dõi mức hoàn thành

Mở `study_100_iterations/progress.json`:

- `completed`: số lượt đã xử lý; `expected`: tổng số lượt cần chạy.
- `phase`: `optimizing` là đang tối ưu; `aggregating` là đang tổng hợp; `complete` là hoàn tất; `failed` là đã dừng vì lỗi.
- `eta_s`: thời gian còn lại ước tính bằng giây, có thể thay đổi đáng kể.

Progress là ảnh chụp lần cập nhật cuối. Nếu file không cập nhật, kiểm tra log và tiến trình; không suy ra tiến trình còn chạy chỉ từ chữ `optimizing`.

Mỗi dataset cần đủ **30 case × 30 seed = 900 lượt** mới xuất bộ CSV cho dataset đó. Vì vậy lúc đầu có task JSON nhưng chưa có CSV là bình thường. Bảng tổng kết toàn study và ảnh cuối chỉ tạo sau khi tất cả worker hoàn tất. `completion.json` ở thư mục study gốc xác nhận bước xuất báo cáo đã thành công.

## Nên đọc file nào trước?

1. `study_100_iterations/datasets/<dataset>/<dataset>_result.csv`: một dòng cho mỗi case × seed. Dùng để xem kết quả gốc của dataset.
2. `tables/by_dataset.csv`: fitness trung bình và độ lệch chuẩn qua seed, cùng các chỉ số trung bình, riêng cho mỗi dataset × case.
3. `tables/by_scale.csv`: tổng hợp theo **số người dùng × case**, không phải một dòng cho mỗi file dữ liệu. Nhiều dataset có cùng số user được gộp lại.
4. `tables/main.csv`: so sánh sáu phương pháp chính; `tables/GA.csv`, `PSO.csv`, `WOA.csv`: so sánh tám tổ hợp Có/Không của mỗi họ.
5. `tables/design.csv`: bảng thành phần K/O/L và hybrid. `contributions.csv`: tác động ghép cặp của các thành phần. `stability.csv`: độ dao động qua seed trên từng dataset. `ranking.csv`: xếp hạng mô tả qua dataset.
6. `study_results.ipynb`: báo cáo có bảng và 13 ảnh nhúng. Mở trực tiếp sau khi study hoàn tất. `figures/` chứa PNG riêng.

Các bảng tổng kết trên nằm trong thư mục `tables/` của từng bộ kết quả. Bảng trong `pipeline_check/tables/` chỉ dùng số liệu kiểm tra, dù tên file giống bảng study chính.

## Ý nghĩa các cột

| Cột | Cách hiểu |
|---|---|
| `users` | Số người dùng trong dataset |
| `case` | Thuật toán và tổ hợp cải tiến |
| `seed` | Số khởi tạo ngẫu nhiên; mỗi seed là một lần thử |
| `fitness`, `fitness_mean` | Điểm mục tiêu, càng lớn càng tốt |
| `fitness_sd`, `sd` | Độ lệch chuẩn fitness qua seed; nhỏ hơn nghĩa là ít dao động hơn |
| `coverage`, `coverage_mean` | Tỷ lệ phủ, 0.92 tương ứng 92% |
| `energy`, `energy_mean` | Chỉ số công suất chuẩn hóa, càng nhỏ càng tốt |
| `interference`, `interference_mean` | Tỷ lệ người dùng được từ hai UAV phủ đồng thời, là proxy chồng lấn |
| `wall_s`, `wall_s_mean` | Thời gian quan sát bằng giây |
| `fe`, `fe_mean` | Số lần đánh giá hàm mục tiêu |
| `feasible` | Nghiệm có thỏa ràng buộc hay không |

`fitness = 0.6 × coverage − 0.2 × energy − 0.2 × interference` với trọng số mặc định. Coverage cao nhất chưa chắc có fitness cao nhất. Cùng 100 vòng không đồng nghĩa cùng FE.

`<dataset>_positions.csv` có tọa độ nghiệm cuối, một dòng cho mỗi case × seed × UAV. `<dataset>_convergence.csv` có chỉ số tại vòng 0–100, một dòng cho mỗi case × seed × vòng.

Ví dụ `pipeline_check/tables/by_scale.csv` chỉ có `users=50` vì chỉ chạy dataset đầu tiên có 50 người dùng. Trong study đầy đủ, bảng này có một dòng cho mỗi quy mô × case; không có 500 dòng tương ứng 500 file đầu vào.
