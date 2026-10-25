# Study notebook: 30 trường hợp, 100 vòng, 500 CSV

[Mục lục](README.md) · [Người mới](PROJECT_GUIDE.md) · [Mô hình](REPORT.md) · [Schema](DATA_FORMAT.md)

Ngày 25/10/2026: **đã triển khai, chưa chạy thí nghiệm**. Notebook chưa có output; danh sách seed chưa chốt. Tài liệu này mô tả hành vi mã hiện tại và các giới hạn, không phải kết quả nghiên cứu.

## 1. Tệp và điều kiện chung

| Tệp | Vai trò |
|---|---|
| [full_study_100_iterations.ipynb](../notebooks/full_study_100_iterations.ipynb) | Thiết kế, ô chạy, bảng và ảnh bên dưới code |
| [notebook_study.json](../../configs/notebook_study.json) | 100 vòng, quần thể 25, 4 UAV, seeds=[] |
| [notebook_study.py](../src/notebook_study.py) | 30 case, đọc CSV, chạy tuần tự, lưu task, tổng hợp |
| [enhancements.py](../src/algorithms/base/enhancements.py) | K/OBL/Lévy cho GA và PSO |
| [test_notebook_study.py](../tests/test_notebook_study.py) | Kiểm tra hợp đồng; không phải benchmark |

Dùng 500 CSV có sẵn, dự kiến 10 mức 50–500 user, mỗi mức 50 dataset. Không tự thay tọa độ bằng bộ sinh FE và không ép độ cao user về 0. plan kiểm tra số file; loader/validator kiểm tra dữ liệu từng file khi thực thi.

Cùng dataset, seed, quần thể nền và hàm fitness giữa các đối chứng. Seed thuật toán chưa được chọn; bộ chạy yêu cầu ít nhất hai seed khác nhau, nhưng hai chỉ là điều kiện kỹ thuật, không bảo đảm lực thống kê.

Khối lượng: 500 × 30 = **15.000 task mỗi seed**. Nếu chọn 30 seed sẽ là 450.000 task; đây là phép tính thiết kế, không phải số task đã chạy.

## 2. Sáu thuật toán chính

GA, PSO, WOA, H-PSO-GA, H-WOA-PSO và I-WOA là nhóm main. Các hàng dùng chung kết quả với nhóm ablation khi case trùng, không chạy lặp chỉ vì xuất nhiều bảng.

Cơ chế baseline nằm trong [các chương DW](README.md). Số case duy nhất của toàn study là 30, không phải tổng số hàng của mọi bảng.

## 3. Hai mươi bốn case của WOA, PSO và GA

| Cấu hình | K-Means | OBL | Lévy | Họ WOA | Họ PSO | Họ GA |
|---|:---:|:---:|:---:|---|---|---|
| Gốc | Không | Không | Không | WOA | PSO | GA |
| K | Có | Không | Không | WOA-K | PSO-K | GA-K |
| O | Không | Có | Không | WOA-O | PSO-O | GA-O |
| L | Không | Không | Có | WOA-L | PSO-L | GA-L |
| KO | Có | Có | Không | WOA-KO | PSO-KO | GA-KO |
| KL | Có | Không | Có | WOA-KL | PSO-KL | GA-KL |
| OL | Không | Có | Có | WOA-OL | PSO-OL | GA-OL |
| KOL | Có | Có | Có | I-WOA | PSO-KOL | GA-KOL |

WOA gốc dùng WOAOptimizer. Các case WOA có toán tử dùng IWOAOptimizer với cờ tương ứng. PSO và GA giữ lõi riêng, bật thêm toán tử, không được đổi tên rồi dùng lõi WOA thay thế.

## 4. Sáu case của hai bản lai

| Case | Crossover | Mutation | Lực hút pbest trong vận tốc | Lực hút gbest trong vận tốc |
|---|:---:|:---:|:---:|:---:|
| H-PSO-GA | Có | Có | Có | Có |
| PSO+Crossover | Có | Không | Có | Có |
| PSO+Mutation | Không | Có | Có | Có |
| H-WOA-PSO | Không | Không | Có | Có |
| H-WOA-PSO-no-pbest | Không | Không | Không | Có |
| H-WOA-PSO-no-gbest-velocity | Không | Không | Có | Không |

Không thêm K/O/L vào các bản lai trong thiết kế hiện tại. PSO gốc và WOA gốc từ bảng trước làm đối chứng bổ sung. H-WOA-PSO trộn hai đề xuất trên từng cá thể, không chia quần thể thành hai nửa. Bỏ gbest trong vận tốc vẫn giữ ảnh hưởng best ở nhánh WOA.

## 5. Quy tắc toán tử

| Thành phần | Cách áp dụng |
|---|---|
| Quần thể nền | Stream seed riêng; cùng ma trận tọa độ nền trên mỗi dataset/seed |
| K-Means | Thay một cá thể trước đánh giá khởi tạo bằng nghiệm từ tâm cụm; clip vào miền |
| OBL khởi tạo | Tạo nghiệm đối lập L+U−X; chọn P tốt nhất từ 2P |
| OBL động | Xác suất 0,2 mỗi vòng; dùng biên hiện tại của quần thể |
| Lévy | Xác suất 0,3 mỗi cá thể, beta=1,5, step size=0,05; nhận nếu tốt hơn ứng viên |
| PSO khi thay vị trí | Đặt vận tốc bằng 0; chỉ cập nhật pbest nếu cải thiện; giữ lịch sử pbest khi OBL chọn cá thể |
| GA | Giữ tournament, arithmetic crossover, Gaussian mutation, elitism |

WOA chèn Lévy sau cập nhật từng cá thể; PSO chèn sau lượt cập nhật bầy, trước cập nhật best; GA chèn sau replacement. Đây là quy tắc riêng theo lõi, không có nghĩa trình tự ba họ giống hệt nhau.

Các case H-PSO-GA dùng crossover 0,8 và mutation 0,15 khi bật. Baseline GA có tham số riêng, xem parameter class. Tắt toán tử có thể thay đổi tiêu thụ RNG, nên cùng seed không đồng nghĩa cùng quỹ đạo sau mọi bước.

## 6. Định nghĩa kết quả và thời gian

Fitness là tốt nhất **đã được đánh giá** đến mốc, kể cả ứng viên bị loại. optimizer_fitness lưu thêm kết quả optimizer trả về để truy vết.

History có 101 mốc: vòng 0 sau khởi tạo/OBL khởi tạo, rồi vòng 1–100. Mỗi mốc có fitness, FE, thời gian, C/E/I và tọa độ best. Vòng 35/80 là checkpoint trong lần chạy 100 vòng, không tương đương chạy độc lập với tổng ngân sách 35/80.

FE tính cả khởi tạo, OBL, Lévy, ứng viên không khả thi và ứng viên không được giữ. Không đếm tính metric cho bảng. GA quần thể lẻ có thể sinh 26 con khi P=25; không giả định mỗi vòng luôn đúng 25 FE.

Thời gian tính từ khi tạo observer tới mốc ghi: gồm khởi tạo, K-Means, tối ưu và chi phí quan sát các mốc trước. Không gồm đọc/tiền xử lý CSV, tạo ma trận quần thể nền, ghi JSON; có thể gồm thời gian tạo optimizer. Mốc thời gian được chụp trước khi tính metric cho chính mốc đó. Không so trực tiếp với thời gian FE runner có phạm vi khác.

Cùng 100 vòng không bảo đảm cùng FE. Study này là so sánh theo vòng; đối chứng theo FE nằm trong [EXPERIMENT_DESIGN](EXPERIMENT_DESIGN.md).

## 7. Bảng đầu ra

| Tên | Nội dung |
|---|---|
| main | Sáu thuật toán chính |
| WOA, PSO, GA | Tám case mỗi họ |
| hybrid_pso_ga | PSO gốc, crossover, mutation, bản lai đầy đủ |
| hybrid_woa_pso | WOA, PSO, hai ablation và bản lai đầy đủ |
| by_scale | Fitness, C/E/I, thời gian, FE theo số user/case |
| checkpoints | Trung bình tại vòng 0, 35, 80, 100 |
| convergence | Median và phân vị 25–75% fitness từng vòng |
| stability | Mean/SD/min/max qua seed trên từng dataset/case |
| contributions | 36 cặp K/O/L chỉ khác đúng một thành phần |
| ranking | Mean rank từ median seed trên từng dataset, kèm chất lượng/chi phí |

Mỗi bảng xuất CSV/MD dưới tables và hiển thị trong notebook. Summary có mean fitness, best thực trên các lượt, C/E/I, thời gian, FE và trung bình SD qua seed tính riêng từng dataset. Không gọi độ lệch chuẩn gộp dataset là độ ổn định qua seed.

Mỗi nhóm có ảnh hội tụ median/IQR và ảnh sáu chỉ số theo quy mô. IQR là phân tán mô tả, không phải CI. Ảnh 3D lấy nghiệm I-WOA đã lưu trên dataset 200 user đầu tiên theo tên, seed nhỏ nhất, vòng 100; không tối ưu lại và không chọn hình theo thắng/thua.

## 8. Chạy, lưu và tiếp tục

Notebook mặc định CONFIRM_RUN=False. Danh sách seed để trống. Đọc [REPRODUCE](../../REPRODUCE.md) trước khi được yêu cầu chạy; trong lượt chỉnh tài liệu này không thực thi notebook.

Mỗi task ghi JSON nguyên tử. Manifest lưu config, case, dataset, hash source/config/nội dung CSV. Khi chạy lại, task có JSON được bỏ qua; task chưa hoàn thành chạy lại. Nếu đổi source/config/data, dùng output mới thay vì trộn kết quả.

Khóa .running ngăn hai kernel ghi cùng output. Kill kernel có thể để lại khóa; xác minh tiến trình cũ đã dừng trước khi xử lý. Không xóa kết quả để chữa lỗi resume.

Chỉ đủ task mới ghi runs.csv/completion.json và cho phép tổng hợp. Thư mục mặc định là implementation/results/study_100_iterations. Bộ chạy tuần tự một worker; đọc bảng không gọi optimizer. Tổng hợp đọc từng artifact để tránh nạp toàn bộ tọa độ lịch sử vào RAM, nhưng vẫn cần bộ nhớ cho chuỗi fitness.

## 9. Đánh giá và giới hạn

Ranking/contributions hiện là mô tả, chưa có kiểm định/CI cho 30 case. Không đưa CSV này vào analyzer FE sáu thuật toán như cùng schema. Chọn phương án theo chất lượng, chi phí và ổn định; không mặc định I-WOA hoặc KOL tốt nhất.

Trạng thái xác minh trước lượt tài liệu này: sáu kiểm tra hợp đồng đạt, cấu trúc notebook hợp lệ; chưa xác nhận optimizer study toàn trình, chưa chạy study 500 file. Kết quả test không thay kết quả nghiên cứu. Xem [REPORT_EVIDENCE](REPORT_EVIDENCE.md).
