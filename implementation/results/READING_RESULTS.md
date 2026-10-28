# Cách đọc kết quả

## Vị trí đầu ra hiện hành

Dữ liệu, checkpoint, CSV/Markdown và `RESULTS.md` nằm trong `implementation/results/<study>/`.
Notebook báo cáo nằm tại `implementation/notebooks/<study>/study_results.ipynb`;
toàn bộ ảnh bảng và đồ thị JPG nằm trong `implementation/notebooks/<study>/picture/`.
Các tên `study_results.ipynb` và `picture/` bên dưới được hiểu theo vị trí notebook này.
Chạy lại các ô đọc bảng/ảnh từ thư mục chứa notebook; không chạy optimizer để xem báo cáo.

**Hiện tại:** toàn bộ kết quả đã được xóa theo yêu cầu. Các đường dẫn dưới đây mô tả cấu trúc đầu ra khi chạy lại, không phải các file đang tồn tại.

## Đọc đúng thư mục

- `pipeline_check/`: chỉ kiểm tra luồng xuất kết quả trên **1 dataset, 12 case, 1 seed**. Không đại diện cho toàn bộ 200 dataset.
- `study_80_iterations/`: kết quả study chính, **200 dataset × 12 case × 10 seed = 24.000 lượt**. Một lượt là một tổ hợp dataset–case–seed, không phải một dataset.

## Theo dõi mức hoàn thành

Mở `study_80_iterations/progress.json`:

- `completed`: số lượt đã xử lý; `expected`: tổng số lượt cần chạy.
- `phase`: `optimizing` là đang tối ưu; `aggregating` là đang tổng hợp; `complete` là hoàn tất; `failed` là đã dừng vì lỗi.
- `eta_s`: thời gian còn lại ước tính bằng giây, có thể thay đổi đáng kể.

Progress là ảnh chụp lần cập nhật cuối. Nếu file không cập nhật, kiểm tra log và tiến trình; không suy ra tiến trình còn chạy chỉ từ chữ `optimizing`.

Mỗi dataset cần đủ **12 case × 10 seed = 120 lượt** mới xuất bộ CSV cho dataset đó. Vì vậy lúc đầu có task JSON nhưng chưa có CSV là bình thường. Bảng tổng kết toàn study và ảnh cuối chỉ tạo sau khi tất cả worker hoàn tất. `completion.json` ở thư mục study gốc xác nhận bước xuất báo cáo đã thành công.

## Nên đọc file nào trước?

1. `study_80_iterations/datasets/<dataset>/<dataset>_result.csv`: một dòng cho mỗi case × seed. Dùng để xem kết quả gốc của dataset.
2. `tables/by_dataset.csv`: fitness trung bình và độ lệch chuẩn qua seed, cùng các chỉ số trung bình, riêng cho mỗi dataset × case.
3. `tables/by_scale.csv`: tổng hợp theo **số người dùng × case**, không phải một dòng cho mỗi file dữ liệu. Nhiều dataset có cùng số user được gộp lại.
4. `tables/main.csv`: so sánh sáu phương pháp chính; `tables/WOA.csv`: so sánh tám tổ hợp bật/tắt K-Means, OBL và Lévy của WOA.
5. `tables/design.csv`: bảng thành phần K/O/L và hybrid. `contributions.csv`: tác động ghép cặp của các thành phần. `stability.csv`: độ dao động qua seed trên từng dataset. `ranking.csv`: xếp hạng mô tả qua dataset.
6. `study_results.ipynb`: báo cáo có bảng và ảnh JPG nhúng. Mở trực tiếp sau khi study hoàn tất. `picture/` chứa ảnh riêng, tên tiếng Việt không dấu; tiêu đề và nội dung trong ảnh bằng tiếng Anh.

## Bảng và ảnh so sánh bổ sung

- `checkpoints.csv`: chỉ số tích lũy tại vòng 0, 20, 40, 60, 80 với study 80 vòng. Mốc 0 bao gồm khởi tạo. Với 100 vòng, dùng mốc 0, 25, 50, 75, 100.
- `stages.csv`: thời gian, FE và mức tăng fitness riêng từng khoảng giữa hai mốc, cùng chất lượng ở cuối khoảng. Không tính lại thời gian khởi tạo vào giai đoạn đầu.
- `stages_by_scale.csv`: các chỉ số giai đoạn theo số user và case.
- `quality_by_scale.csv`: trung bình, trung vị, SD của fitness/thời gian, trung bình và SD coverage, FE trung bình theo quy mô. SD ở bảng này gộp biến thiên giữa dataset và seed.
- `stability_summary.csv`: trung bình và lớn nhất của SD qua seed trong từng dataset; dùng để phân biệt với SD gộp theo quy mô.
- `paired_comparison.csv`: chênh lệch fitness, thời gian, tỷ lệ thắng/hòa của hybrid so với các thuật toán thành phần và I-WOA so với WOA, ghép cặp cùng dataset và seed.

Ảnh bảng gồm `bangsosanhthuattoan`, `bangsosanhcaitienwoa`, `bangthietkethuattoan`, `bangxephang`, `bangchatluongvasonguoi`, `bangthoigianvavongchay`, `bangsosanhgiaidoan`, `banggiaidoanvasonguoi`, `bangdoondinh`, `bangdonggopcaitien`, `bangsosanhhybrid`. Tên có hậu tố phần/trang và đuôi `.jpg`; tối đa 24 dòng mỗi trang, bảng rộng chia phần và lặp cột định danh.

Đồ thị gồm `dothihoitu_chinh.jpg`, `dothihoitu_woa.jpg`, `dothisosanhvasonguoi_chinh.jpg`, `dothisosanhvasonguoi_woa.jpg`, `dothigiaidoan_chinh.jpg`, `dothigiaidoan_woa.jpg`, `dothidoondinh.jpg`, `vitribotriuav3d.jpg`. Hình bố trí vẫn là một lượt I-WOA minh họa, không phải kết quả tốt nhất.

CSV chi tiết từng dataset và từng vòng giữ nguyên, không xuất mỗi dòng thành ảnh. Các bảng bổ sung vẫn là thống kê mô tả, không phải kiểm định ý nghĩa thống kê. Thời gian quan sát chịu ảnh hưởng môi trường và chạy đồng thời; không tự suy ra thời gian chạy toàn study bằng cách cộng thời gian task.

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

`fitness = 0.6 × coverage − 0.2 × energy − 0.2 × interference` với trọng số mặc định. Coverage cao nhất chưa chắc có fitness cao nhất. Cùng 80 vòng không đồng nghĩa cùng FE.

`<dataset>_positions.csv` có tọa độ nghiệm cuối, một dòng cho mỗi case × seed × UAV. `<dataset>_convergence.csv` có chỉ số tại vòng 0–80, một dòng cho mỗi case × seed × vòng.

Ví dụ `pipeline_check/tables/by_scale.csv` chỉ có `users=50` vì chỉ chạy dataset đầu tiên có 50 người dùng. Trong study đầy đủ, bảng này có một dòng cho mỗi quy mô × case; không có 500 dòng tương ứng 200 file đầu vào.
