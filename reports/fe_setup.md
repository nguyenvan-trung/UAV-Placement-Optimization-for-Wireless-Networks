# Bổ sung hạ tầng benchmark FE

Mục đích: ghi phạm vi thay đổi và bằng chứng kiểm thử nhỏ. Cập nhật 24/10/2026.
Không chạy full benchmark hoặc bộ 500 CSV trong lần bổ sung này.

## Thay đổi và tác động

| Tệp | Thay đổi | Tác động |
|---|---|---|
| implementation/src/counter.py | FitnessCounter, BudgetExhausted, best/phase/history/target | Đếm mọi đánh giá kể cả nghiệm không khả thi; chặn trước FE vượt ngân sách |
| implementation/src/algorithms/base/budget.py | Wrapper opt-in, quần thể chung, lịch FE, ngắt giữa vòng | Chỉ bật khi optimize nhận max_fe; trả best của mọi nghiệm đã đánh giá |
| GA/PSO/WOA/I_WOA optimizer và hai hybrid | Decorator, khởi tạo nền, vòng lặp FE, progress | Lệnh legacy không truyền max_fe giữ nhánh cũ; không gộp số liệu hai chế độ |
| WOA/coefficient_update.py | Tham số progress_fraction tùy chọn | a theo FE khi bật, mặc định vẫn theo iteration |
| I_WOA/obl.py và optimizer.py | Gắn phase cho OBL/Lévy | Đánh giá phụ nằm trong cùng counter |
| src/benchmark.py | Factory và raw final metrics | Fitness baseline dùng hàm gốc, SINR chỉ opt-in; final reporting ngoài FE |
| scripts/run_benchmark.py, run_benchmark.py | Runner CLI, atomic outputs, resume, multiprocessing | Lưu schema mới cùng solutions/convergence và metadata |
| configs/benchmark.yaml, seeds/seeds.csv, generate_seeds.py | Kế hoạch và manifest trước chạy | Tách purpose và data/algo seeds, kiểm toàn manifest với cấu hình |
| configs/sensitivity.yaml | Đồng bộ budget/manifest tham khảo | Runner lấy ngân sách/instance chính từ benchmark.yaml |
| analyze_sensitivity.py | Gộp median theo instance trước Wilcoxon | Không coi run cùng instance là cặp độc lập cho kiểm định |
| analyze_stability.py | Cho phép target chưa khai báo | Hit-rate thiếu không bị diễn giải thành thất bại |
| requirements.txt/lock, REPRODUCE.md, docs/EXPERIMENT_DESIGN.md, DATA_FORMAT.md | Phụ thuộc, schema và lệnh chạy | Lock là snapshot trên máy, chưa chứng minh cài sạch đa nền tảng |
| .gitignore | Bỏ theo dõi cache và thư mục audit/test mới | Không xóa bất kỳ dữ liệu nào |

Đường dẫn optimizer/WOA/I_WOA trong bảng tương đối từ implementation/src/algorithms.
Không sửa công thức F, định nghĩa C/E/I hoặc dữ liệu UE cũ. Chế độ FE thay
giao thức điều khiển và khởi tạo ghép cặp, nên không so trực tiếp với legacy.

## Bằng chứng kiểm tra

- Toàn bộ pytest trên bản sao: **111 passed**. Log:
  `tmp_audit/fe_final_regression_01d34520/pytest.log`.
- Sáu thuật toán và tám ablation: budget test dùng nhiều mức FE, gồm ngắt
  giữa khởi tạo/vòng lặp; số gọi raw được spy độc lập phải bằng ngân sách.
- CLI checkpoint/resume, tuần tự/song song, final positions và convergence
  khớp: xem `tmp_audit/fe_final_current.json` trỏ tới verification.json và
  log từng lệnh. Thử multiprocessing được chạy ngoài sandbox hạn chế pipe.
- Log FE thật ở phạm vi smoke đã được analyze.py và analyze_stability.py
  đọc thành công, **không phải** dữ liệu benchmark để suy luận hơn/thua.
- Smoke cả mode ablation và sensitivity đã chạy với ngân sách nhỏ; chưa
  có kết luận đóng góp hay độ nhạy của thuật toán.
- Sau bổ sung kiểm tra phiên bản môi trường cho resume, thử checkpoint và
  resume lần nữa: đường dẫn được ghi tại tmp_audit/fe_checkpoint_final_current.json.

Đây là file chỉ vị trí bằng chứng, không thay log nguồn. Không xóa tmp_audit
trước khi gom các log còn cần giữ. Thư mục đã được gitignore để tránh commit
cache và bản sao. Chưa kiểm kill tại mọi vị trí ghi hoặc cài lock venv sạch.

## Lệnh người dùng chạy tiếp khi sẵn sàng

```powershell
python run_benchmark.py --smoke --output tmp_audit/my_fe_smoke
```

Đọc REPRODUCE.md trước khi bỏ --smoke. Không tự chạy lớn trong lần bổ sung.
Thiết kế mặc định là lựa chọn khởi đầu: cần chốt số instance và ngưỡng mục
tiêu trước nghiên cứu chính thức. Target null được lưu trống, không có tỷ lệ
đạt ngưỡng hợp lệ cho đến khi chọn ngưỡng trước chạy.

## Còn thiếu / chưa chắc chắn

- Chưa có analyze_ablation.py đầy đủ và full benchmark mới.
- Chưa xác thực vật lý E/I, ngưỡng, tham số kênh hoặc UE cao hơn UAV; bộ
  scenario mới đặt UE ở mặt đất để giữ phạm vi rõ ràng, không sửa 500 CSV cũ.
- Root lock phụ thuộc phiên bản Python/OS lúc chụp, chưa cài thử sạch.
- Tài liệu audit cũ là snapshot trước sửa; không coi các dòng “chưa có
  counter” trong snapshot lịch sử là trạng thái hiện tại.
