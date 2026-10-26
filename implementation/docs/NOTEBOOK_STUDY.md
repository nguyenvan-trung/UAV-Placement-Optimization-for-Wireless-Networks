# Study notebook: 30 trường hợp, 100 vòng, 500 CSV

## Mục lục

1. [1. Tệp và điều kiện chung](#doc-section-01)
2. [2. Sáu thuật toán chính](#doc-section-02)
3. [3. Hai mươi bốn case của WOA, PSO và GA](#doc-section-03)
4. [4. Sáu case của hai bản lai](#doc-section-04)
5. [5. Quy tắc toán tử](#doc-section-05)
6. [6. Định nghĩa kết quả và thời gian](#doc-section-06)
7. [7. Bảng đầu ra](#doc-section-07)
8. [8. Chạy, lưu và tiếp tục](#doc-section-08)
9. [9. Đánh giá và giới hạn](#doc-section-09)


[Mục lục](README.md) · [Người mới](PROJECT_GUIDE.md) · [Mô hình](REPORT.md) · [Schema](DATA_FORMAT.md)

**Study đang chạy:** người dùng đã chốt 30 seed; coordinator bốn worker thực hiện 450.000 task. Xem [RUN_STATUS](RUN_STATUS.md) để theo dõi. Chưa có bảng cuối khi chưa đủ task.

![Thiết kế, duyệt chạy, thực thi task, kiểm tra và tổng hợp](assets/study.svg)

**Cách đọc:** thiết kế đã được duyệt; lưu task rồi kiểm tra đủ cặp mới tổng hợp. Hình theo notebook_study.py; validator đã bổ sung kiểm tra identity, 101 mốc, metric hữu hạn, best không giảm, FE/thời gian và tái tính nghiệm.

<a id="doc-section-01"></a>

## 1. Tệp và điều kiện chung

| Tệp | Vai trò |
|---|---|
| [full_study_100_iterations.ipynb](../notebooks/full_study_100_iterations.ipynb) | Thiết kế, ô chạy, bảng và ảnh bên dưới code |
| [notebook_study.json](../../configs/notebook_study.json) | 100 vòng, quần thể 25, 4 UAV, 30 seed cố định |
| [notebook_study.py](../src/notebook_study.py) | 30 case, đọc CSV, worker, validator và bảng |
| [run_notebook_study.py](../scripts/run_notebook_study.py) | Coordinator bốn tiến trình, tổng hợp sau hoàn tất |
| [study_report.py](../src/study_report.py) | Xuất hình, RESULTS.md và notebook kết quả |
| [enhancements.py](../src/algorithms/base/enhancements.py) | K/OBL/Lévy cho GA và PSO |
| [test_notebook_study.py](../tests/test_notebook_study.py) | Kiểm tra hợp đồng; không phải benchmark |

Dùng 500 CSV có sẵn, dự kiến 10 mức 50–500 user, mỗi mức 50 dataset. Không tự thay tọa độ bằng bộ sinh FE và không ép độ cao user về 0. plan kiểm tra số file; loader/validator kiểm tra dữ liệu từng file khi thực thi.

Cùng dataset, seed, quần thể nền và fitness giữa các đối chứng. Đã chọn 30 seed bằng SeedSequence(20261024), ghi vào config trước chạy. Số seed không tự chứng minh độc lập giữa dataset hoặc đủ lực mọi kiểm định.

Khối lượng: 500 × 30 = **15.000 task mỗi seed**, tổng **450.000 task**. Số đã hoàn tất xem progress, không dùng tổng thiết kế để nói đã chạy xong.

<a id="doc-section-02"></a>

## 2. Sáu thuật toán chính

GA, PSO, WOA, H-PSO-GA, H-WOA-PSO và I-WOA là nhóm main. Các hàng dùng chung kết quả với nhóm ablation khi case trùng, không chạy lặp chỉ vì xuất nhiều bảng.

Cơ chế baseline nằm trong [các chương DW](README.md). Số case duy nhất của toàn study là 30, không phải tổng số hàng của mọi bảng.

<a id="doc-section-03"></a>

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

<a id="doc-section-04"></a>

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

<a id="doc-section-05"></a>

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

<a id="doc-section-06"></a>

## 6. Định nghĩa kết quả và thời gian

Fitness là tốt nhất **đã được đánh giá** đến mốc, kể cả ứng viên bị loại. optimizer_fitness lưu thêm kết quả optimizer trả về để truy vết.

History có 101 mốc: vòng 0 sau khởi tạo/OBL khởi tạo, rồi vòng 1–100. Mỗi mốc có fitness, FE, thời gian, C/E/I và tọa độ best. Vòng 35/80 là checkpoint trong lần chạy 100 vòng, không tương đương chạy độc lập với tổng ngân sách 35/80.

FE tính cả khởi tạo, OBL, Lévy, ứng viên không khả thi và ứng viên không được giữ. Không đếm tính metric cho bảng. GA quần thể lẻ có thể sinh 26 con khi P=25; không giả định mỗi vòng luôn đúng 25 FE.

Thời gian tính từ khi tạo observer tới mốc ghi: gồm khởi tạo, K-Means, tối ưu và chi phí quan sát các mốc trước. Không gồm đọc/tiền xử lý CSV, tạo ma trận quần thể nền, ghi JSON; có thể gồm thời gian tạo optimizer. Mốc thời gian được chụp trước khi tính metric cho chính mốc đó. Không so trực tiếp với thời gian FE runner có phạm vi khác.

Cùng 100 vòng không bảo đảm cùng FE. Study này là so sánh theo vòng; đối chứng theo FE nằm trong [EXPERIMENT_DESIGN](EXPERIMENT_DESIGN.md).

<a id="doc-section-07"></a>

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

<a id="doc-section-08"></a>

## 8. Chạy, lưu và tiếp tục

Notebook giữ CONFIRM_RUN=False để không mở trùng coordinator. CLI hiện chạy nền; không bật ô chạy trong lúc đó. Seed đã lưu trong config.

Mỗi task ghi JSON gzip không mất dữ liệu, nguyên tử, theo bucket. Root output có shards/worker_XX/tasks/bucket/*.json.gz. Manifest lưu config, case, dataset và chữ ký source/config/CSV. Artifact cũ được xác minh trước khi bỏ qua; task thiếu chạy lại. Nếu đổi source/config/data, dùng output mới.

Khóa .running ngăn hai kernel ghi cùng output. Kill kernel có thể để lại khóa; xác minh tiến trình cũ đã dừng trước khi xử lý. Không xóa kết quả để chữa lỗi resume.

Mỗi shard có completion riêng; completion.json gốc chỉ xuất sau khi đủ 450.000 task và xuất báo cáo. Output mặc định là implementation/results/study_100_iterations. Bốn worker dùng subprocess độc lập để tránh lỗi multiprocessing Pipe của Windows. Đọc bảng không gọi optimizer. Tổng hợp vẫn cần bộ nhớ cho chuỗi fitness.

<a id="doc-section-09"></a>

## 9. Đánh giá và giới hạn

Ranking/contributions hiện là mô tả, chưa có kiểm định/CI cho 30 case. Không đưa CSV này vào analyzer FE sáu thuật toán như cùng schema. Chọn phương án theo chất lượng, chi phí và ổn định; không mặc định I-WOA hoặc KOL tốt nhất.

Chuẩn bị hiện tại: 83 kiểm tra đạt; 90 task kiểm tra thật xác nhận cả tối ưu và luồng xuất 12 bảng/13 hình/notebook. Study 500 file đang chạy. Artifact kiểm tra ở tmp_audit không thay kết quả nghiên cứu. Xem [REPORT_EVIDENCE](REPORT_EVIDENCE.md).
