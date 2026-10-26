# Định dạng dữ liệu: CSV đầu vào, notebook, batch và FE

## Mục lục

1. [1. CSV user đầu vào](#doc-section-01)
2. [2. Artifact notebook 100 vòng](#doc-section-02)
3. [3. CSV batch legacy](#doc-section-03)
4. [4. Luồng FE](#doc-section-04)
5. [seeds/seeds.csv](#doc-section-05)
6. [runs.csv](#doc-section-06)
7. [convergence và solutions](#doc-section-07)
8. [env.json và lock](#doc-section-08)


[Mục lục](README.md) · [Người mới](PROJECT_GUIDE.md) · [Thuật ngữ](GLOSSARY.md) · [Study notebook](NOTEBOOK_STUDY.md)


Mục đích: nhận diện đúng schema trước khi đọc hoặc phân tích. Các tên trường dưới đây là hợp đồng dữ liệu, không phải số liệu nghiên cứu. Notebook và FE đều có tên runs.csv nhưng không cùng cấu trúc.

<a id="doc-section-01"></a>

## 1. CSV user đầu vào

| Trường | Ý nghĩa |
|---|---|
| user_id | Định danh user trong file |
| x_m, y_m, z_m | Tọa độ user, đơn vị mét; không phải nghiệm UAV |
| demand | Nhu cầu dịch vụ đầu vào; fitness hiện tại không cân coverage theo demand |

Loader/validator yêu cầu các cột, dữ liệu không thiếu và số hữu hạn. Tiền xử lý bỏ user_id trùng; số user báo cáo là số sau tiền xử lý. Không tự ép z_m về 0. Notebook đọc data/stores; hình data/views chỉ minh họa.

<a id="doc-section-02"></a>

## 2. Artifact notebook 100 vòng

Nguồn: [notebook_study.py](../src/notebook_study.py). Thiết kế: [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md).

| Artifact | Cấu trúc |
|---|---|
| manifest.json | signature, config, expected_tasks, danh sách datasets và cases |
| tasks theo bucket: result | dataset, users, case, seed, fitness, coverage, energy, interference, fe, wall_s, optimizer_fitness, feasible |
| tasks theo bucket: history | 101 dòng, iteration=0..100; fitness, fe, elapsed_s, coverage, energy, interference, position |
| runs.csv | Các trường result, tạo khi đủ task |
| completion.json | complete, expected, actual |
| tables/*.csv, *.md | Các phép gộp được liệt kê trong NOTEBOOK_STUDY |

Khóa task là dataset–case–seed. position là vector phẳng 3N tọa độ UAV. fitness là best đã đánh giá; optimizer_fitness là giá trị optimizer trả về. C/E/I là tỷ lệ/chỉ số chuẩn hóa; thời gian giây; FE là số đếm. wall_s và elapsed_s là phạm vi quan sát notebook, không đồng nghĩa wall_time_s của runner FE.

Lần chạy 30 seed hiện dùng bốn shard: shards/worker_XX/tasks/bucket/task_id.json.gz. Nội dung JSON được gzip không mất dữ liệu; read_task/task_paths hỗ trợ cả định dạng này và JSON cũ. Mỗi shard có manifest/env/progress/completion riêng; root có manifest/progress và chỉ có completion cuối sau tổng hợp, vẽ hình và xuất notebook. Không dùng completion của một shard để tuyên bố xong cả study.

Không có scenario_id, distribution, purpose hoặc batch CPU trong schema notebook. Không tự bịa các cột này để đưa vào analyzer FE.

<a id="doc-section-03"></a>

## 3. CSV batch legacy

run_batch.py ghi các tên cột dạng Dataset, Total_Users, Num_UAVs, Algorithm, Population_Size, Iterations, Seed, Fitness, Coverage_Rate, Covered_Users, Energy_Normalized, Interference_Rate, Runtime_Seconds.

Đó là kết quả cuối, không phải history từng vòng. Summary theo user/UAV là các bảng gộp, không được coi mỗi dòng summary là một run độc lập. Schema này không dùng trực tiếp cho notebook study hoặc analyzer FE.

<a id="doc-section-04"></a>

## 4. Luồng FE

Các mục còn lại mô tả seed manifest và log của runner FE. Luồng này sinh dataset từ seed/config thay vì đọc trực tiếp CSV user của notebook. Xem [EXPERIMENT_DESIGN](EXPERIMENT_DESIGN.md).

<a id="doc-section-05"></a>

## seeds/seeds.csv

| Trường | Kiểu | Ý nghĩa |
|---|---|---|
| scenario_id | string | Mức UE và phân bố |
| ue_count | integer | Tổng UE trong instance |
| distribution | enum | Một trong năm tên bộ sinh |
| instance_k | integer | Chỉ số instance trong kịch bản và purpose |
| data_seed | integer | Seed sinh tọa độ; kênh hiện tại xác định, không lấy mẫu fading |
| run_id | integer | Lượt lặp thuật toán trong cùng instance |
| algo_seed | integer | Khởi tạo stream thuật toán và quần thể nền |
| purpose | tuning/eval | Hai tập không dùng chung data/algo seed |

Được sinh bởi generate_seeds.py từ benchmark.yaml. Không chỉnh tay giữa batch.

<a id="doc-section-06"></a>

## runs.csv

| Nhóm trường | Kiểu / đơn vị | Ý nghĩa |
|---|---|---|
| Các trường seeds phía trên | Giữ nguyên | Ghép cặp và phân tầng |
| algorithm, config_id, task_id | string | Thuật toán, cấu hình Fitness, định danh task |
| max_fe, fe_used | integer / FE | Ngân sách và số lần đánh giá thực tế |
| fitness | float, cực đại | Điểm theo cấu hình của dòng đó; trống nếu không khả thi |
| C | ratio | Độ phủ dùng trong mục tiêu, SNR hoặc SINR theo config |
| C_snr, C_sinr | ratio | Hai tiêu chí final để so giữa cấu hình |
| E, I | ratio | Proxy công suất chuẩn hóa và chồng lấn baseline |
| ue_pass, ue_total | integer | Tử/mẫu tương ứng C của cấu hình |
| feasible | boolean | Nghiệm cuối đáp ứng miền/độ cao/khoảng cách |
| violation | zero hoặc string | Không vi phạm hoặc mô tả vi phạm |
| iterations_done | integer | Số sweep hoàn tất; không tính sweep dở |
| wall_time_s, cpu_time_s | seconds | Thời gian task theo perf_counter/process_time |
| worker_id, n_workers | integer | PID task và worker được cấu hình |
| batch_id | string | Signature batch |
| batch_wall_time_s | seconds | Tổng các đoạn thực thi đã checkpoint, không gồm khoảng chờ resume |
| batch_total_cpu_s | seconds | Tổng cpu_time_s task; loại CPU startup/import khỏi phạm vi |
| hit_target, fe_to_target | bool/integer hoặc trống | Trống nếu target chưa khai báo |
| reoptimized | boolean | Task chạy optimizer, không chỉ chấm lại nghiệm cũ |
| initial_population_sha256 | hex string | Hash nền chung trước K-Means, không phải hash sau cải tiến |
| convergence_file, solution_file | path tương đối | Artifact theo task |

Không cộng batch metadata lặp trên nhiều dòng. Thời gian/PID không kỳ vọng
giống hệt khi chạy lại; so Fitness, nghiệm và convergence theo task ID.

<a id="doc-section-07"></a>

## convergence và solutions

convergence/*.csv có fe và best_fitness (maximize), lấy mẫu mỗi chu kỳ FE
và tại ngân sách cuối. solutions/*.json lưu identity, tọa độ UAV, quần thể
nền, hash UE, FE theo phase, khả thi và final metrics.

<a id="doc-section-08"></a>

## env.json và lock

Gồm commit/dirty, hash config/seed/source signature, phiên bản Python và
thư viện, CPU/logical cores/RAM/OS, môi trường luồng và lệnh gọi. Giá trị
RAM hoặc thông tin CPU có thể thiếu nếu host không cho truy vấn; không bịa.
requirements.lock.txt trong output là pip freeze của môi trường chạy,
khác root lock là snapshot phụ thuộc phát triển được chốt lúc bổ sung.

completion.json ghi complete/completed/expected để phân biệt run đã xong
với checkpoint dở. Không dùng chỉ số dòng CSV để kết luận đã đủ thiết kế.
