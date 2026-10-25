# Kiểm tra toàn bộ luồng — 24/10/2026

**Kết luận:** chưa sẵn sàng nộp như một pipeline thực nghiệm FE tái lập đầy đủ.
Lõi thuật toán và các phân tích riêng lẻ chạy được ở phạm vi dưới đây; đoạn
runner FE → schema log mới → phân tích chưa được nối. Không có benchmark mới
hoặc kiểm định chất lượng I-WOA trên dữ liệu thật trong lượt audit này.

## Phạm vi, an toàn và bằng chứng

Ban sao: `tmp_audit/audit_045f1c6d6720`. Logs: `tmp_audit/audit_045f1c6d6720/evidence/commands*.json`.

Chỉ chạy bản sao có src/tests/scripts/configs/docs, dữ liệu nhỏ tự sinh và
CSV kiểm toán. Không chạy lệnh chỉnh sửa docs, xóa hoặc sửa mã gốc. File mới
ngoài tmp chỉ là báo cáo này. Không cập nhật PROMPTS.md vì yêu cầu lần này
không sửa file sẵn có; nguyên văn yêu cầu vẫn nằm trong hội thoại.

SHA256: checked=633, changed=0, deleted=0. Evidence: source_integrity.json.

Không dùng git diff sạch làm bằng chứng vì workspace vốn dirty. So SHA256
trước/sau cho các file gốc được chụp; không tự nhận đã kiểm tra byte mọi file
trong .git, .venv hoặc các thư mục test cũ không truy cập được. Có một thư mục
test_tmp cũ bị từ chối truy cập, không xóa/chỉnh quyền.

Các log lệnh lưu command, exit code, stdout, stderr trong evidence. `124`
là timeout của harness, không phải mã lỗi tự phát của chương trình. Bộ probe
không có counter nên chỉ đo số lời gọi Fitness kiểu cũ; không coi là FE cap.

## Bản đồ luồng từ mã thật

| Luồng | File / điểm vào | Đầu vào | Đầu ra kỳ vọng | Trạng thái và bằng chứng |
|---|---|---|---|---|
| Sinh seed | src/scenarios.py:make_seed_split, validate_seed_split | root seed, số tuning/eval | hai tập seed rời nhau | PASS helper; edge_cases.json. Chưa có manifest data/algo |
| Sinh UE | src/scenarios.py:generate_scenario | phân bố, count, data_seed, parameters | DataFrame UE | PASS đủ năm phân bố ở 50/500; scenario_optimizer_probes.json |
| Sinh dataset cũ | scripts/generate_dataset.py:main | counts, num-datasets | CSV và hình | Đã chạy --help; chưa chạy đầy đủ bộ cũ vì ngân sách nhỏ; bộ sinh mới được thử bằng API |
| Fitness | src/problem/objective.py:UAVPlacementProblem.evaluate/detailed | vector vị trí + UE | F/C/E/I | PASS đầu vào hợp lệ, audit_fitness và probe độc lập; có lỗi input bất hợp lệ ở dưới |
| FitnessCounter | src/counter.py | fitness, max_fe | đếm và dừng FE | CHƯA CÀI ĐẶT; import exit 1 |
| Sáu thuật toán | src/algorithms/*/optimizer.py:optimize | problem, params, seed | OptimizationResult | PASS budget vòng lặp nhỏ; không có đảm bảo max_fe |
| Tám ablation | I_WOA/optimizer.py + parameters flags | K/O/L, chung problem | nghiệm/lịch sử | PASS test lõi và probe đếm lời gọi; chưa có runner ablation FE |
| Benchmark FE | run_benchmark.py, benchmark.yaml | seed manifest + budget | runs/convergence/env | CHƯA CÀI ĐẶT; file missing/exit 2 |
| Batch cũ | scripts/run_batch.py:main/process_single_dataset | CSV, pop, iterations | batch_results_custom.csv | PASS tuần tự; KHÔNG CHẠY ĐƯỢC đa tiến trình do quyền pipe Windows |
| Log schema mới | runner FE chưa có | FE/config/seed/positions | runs.csv, convergence, env.json | CHƯA CÀI ĐẶT; CSV batch cũ không đủ cột |
| Thống kê | scripts/analyze.py:analyze/main | schema runs mới | CSV/MD/TeX/PNG/PDF | PASS dữ liệu giả lập kiểm thử; FAIL khi đưa CSV batch cũ |
| Ablation analysis | scripts/analyze_ablation.py | runs ablation | đóng góp/CI/biểu đồ | CHƯA CÀI ĐẶT; exit 2 |
| Độ nhạy | objectives/sensitivity.py; scripts/analyze_sensitivity.py:analyze | cấu hình + runs đã tối ưu lại | ranks/test/tradeoff | PASS evaluator/test + CSV giả lập; chưa có tối ưu lại theo FE; CSV batch cũ FAIL |
| Tổng quát hóa | scripts/analyze_stability.py:analyze | schema mới | summary/ranks/losses | PASS CSV giả lập; CSV batch cũ FAIL |
| Báo cáo/hình | plot_scenarios.py; build_fitness_audit_report.py; build_report_evidence.py | CSV kiểm toán/dữ liệu minh họa | MD/CSV/PNG | PASS trên bản sao, không phải kết quả nghiên cứu mới |
| README/REPRODUCE | README.md; REPRODUCE.md | môi trường/dataset | chuỗi tái lập | README có liên kết gãy; REPRODUCE CHƯA CÀI ĐẶT |

Đường dẫn src/scripts trong bảng tương đối từ implementation/. Danh sách
hàm và dòng lấy bằng AST: entrypoints.json. Mọi thao tác ghi thuộc bản sao.

## Ma trận đủ các mục kiểm tra

| Mục | Trạng thái | Bằng chứng / giới hạn |
|---|---|---|
| A1 pytest toàn bộ | PASS | 51 passed in 7.93s |
| A2 khớp F, C và tử/mẫu | PASS phạm vi smoke legacy | rows=12, duplicate=0, max |F-recomputed|=5.551115123125783e-17, C_count_error=0.0; legacy_log_checks.json |
| A3 nghiệm khả thi | PASS probe | n=60, independent feasible=60, repeat seed equal=60, max formula error=0.0, max scalar error=5.551115123125783e-17; tính độc lập bằng math.dist, miền, shape; log batch không có positions/feasible/violation để đối chiếu cột |
| B4 max_fe nhỏ/vừa/gấp đôi | CHƯA CÀI ĐẶT | Không có API max_fe; không giả lập ba mức rồi gọi đó là test đạt. legacy_fe_counts.json là số gọi với ba mức iterations, kèm chênh lệch so WOA |
| B5 gọi ngoài counter | FAIL yêu cầu FE | source_scans.json:fitness_calls, có file/dòng; khởi tạo, WOA, OBL, Lévy đều gọi problem.evaluate trực tiếp; detailed cuối là phép báo cáo riêng |
| B6 seed lặp tuần tự/song song | PASS tuần tự; KHÔNG CHẠY ĐƯỢC song song | Probe chạy lại từng cặp; batch_parallel PermissionError WinError 5 ở multiprocessing pipe; chưa thể kết luận tái lập song song |
| B7 quần thể/seed split | FAIL ghép cặp đầy đủ | GA vs GA: True; PSO vs GA: False; WOA vs GA: True; HPSOGA vs GA: False; HWOAPSO vs GA: True; IWOA vs GA: False. Seed helper không giao nhau, nhưng seeds.csv và tuning/eval manifest chưa có |
| B8 lịch theo FE | FAIL yêu cầu FE | WOA/coefficient_update.py:19; PSO/optimizer.py:54-57; hybrid schedules tính theo iterations. source_scans.json:iteration_schedule |
| B9 env/lock | CHƯA CÀI ĐẶT | Thiếu writer env.json và requirements.lock.txt; tool_versions.json chỉ là snapshot audit, không phải env của benchmark |
| C10 schema/log/timing | FAIL tích hợp | Legacy có log C/E/I đúng nhưng thiếu FE/cpu/seed split/IDs/feasible; analyze_legacy exit 1. Không đủ cột để kiểm CPU<=workers*wall; không gọi đây là lỗi CPU đo được |
| C11 mọi phân bố ở 50/500 | PASS ngân sách vòng lặp nhỏ | scenario_optimizer_probes.json; thử đủ sáu thuật toán, không chỉ sinh dữ liệu |
| C12 resume sau kill | CHƯA CÀI ĐẶT | run_batch.py --resume exit 2 unrecognized arguments. Không kill tiến trình vì không có resume để kiểm thử; không báo mất/nhân đôi dòng khi chưa đo |
| D13 phân tích chạy lại | PASS giả lập / FAIL real-log schema / thiếu ablation | TABLE_SHA256: checked=633, changed=0, deleted=0. Evidence: source_integrity.json.; table_hashes.json. Chỉ so SHA256 CSV, không metadata hình |
| D14 thiết kế kiểm định | PASS một phần; cảnh báo | analyze.py gộp instance, Holm/RBC/CI được test. analyze_sensitivity.py:76 dùng pivot theo KEYS có run_id: chưa theo gộp instance của Nhiệm vụ 5, có nguy cơ giả lặp |
| D15 số liệu báo cáo | FAIL truy xuất lịch sử | README.md:118-128 vẫn nói kết quả cũ và link đã mất; TALK.md:99,208 vẫn có khẳng định lịch sử/trọng số không được xác minh. REPORT.md mới ghi chưa có kết quả; ledger audit không chứng minh số liệu benchmark |
| D16 hard-code/TODO/YAML | CẢNH BÁO + thiếu tích hợp | analysis_numeric_literals.json liệt kê numeric AST, không quy mọi số là kết quả bịa; source_scans.json:todos. YAML mới có max_fe/instances/manifest null; không có runner đọc các khóa budget/scenarios/parallel. sensitivity analyzer chỉ đọc phần sensitivity/statistics, không dùng TODO để chạy |
| E17 venv sạch | KHÔNG CHẠY ĐƯỢC tái lập sạch | venv ensurepip exit 1; venv --without-pip tạo được, import numpy exit 1; không có lock, không chứng minh pip install từ lock. pip dry-run --no-index fail fqdn: giới hạn offline, không chứng minh cài online chắc lỗi |
| E18 lệnh tài liệu | FAIL/CHƯA CHẠY đầy đủ | activation exit 1 trong bản sao thiếu venv; optimizer có phiên bản giới hạn chạy PASS. Full batch trong README không chạy nguyên ngân sách vì yêu cầu audit nhỏ; readme_commands.json ghi rõ lệnh/chưa thử nguyên bản. doc_links.json liệt kê link gãy; REPRODUCE thiếu |
| E19 lint/type/dead | FAIL lint; chưa xác minh hết | Ruff exit 1: 114 diagnostics; flake8 --jobs 1 exit 1; mypy full timeout 60s, vulture not installed.. flake8 mặc định cũng bị pipe, --jobs 1 trả lỗi lint. mypy toàn src timeout; scoped counter thiếu file. Vulture không cài; chưa chứng minh không mã chết/import vòng. Import thuật toán và pytest chỉ kiểm các đường đã chạy |
| E20 ca biên | FAIL validation, cảnh báo mô hình/môi trường | edge_cases.json: UE rỗng bị problem chặn, nhưng helper metrics trả NaN; NaN weights qua problem trả NaN; beta=0 chia không; population=0 lỗi max(empty). Chưa chạy Linux. Luồng audit được ép về một thread, không chứng minh runner cũ tự ép thread |

## Lệnh, mã thoát và trích đầu ra

| Command ID | Actual command (copy workspace) | Exit | Output excerpt |
|---|---|---:|---|
| pytest | `D:\Downloads\Aquaroda\python.exe -m pytest implementation/tests -q -p no:cacheprovider` | 0 | 51 passed in 7.93s |
| audit_fitness | `D:\Downloads\Aquaroda\python.exe implementation/scripts/audit_fitness.py` | 0 | } |
| optimizer_cli | `D:\Downloads\Aquaroda\python.exe implementation/scripts/run_optimizer.py --algorithm all --seed 42 --dataset data/stores/50_uniform_users_connect.csv --pop-size 6 --iterations 2 --no-plot` | 0 | ================================================================================ |
| batch_serial | `D:\Downloads\Aquaroda\python.exe implementation/scripts/run_batch.py --mode custom --limit 2 --workers 1 --pop-size 6 --iterations 2 --output-dir batch_serial` | 0 | ✅ Hoàn tất kết xuất bảng báo cáo và biểu đồ trong D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\batch_serial |
| batch_parallel | `D:\Downloads\Aquaroda\python.exe implementation/scripts/run_batch.py --mode custom --limit 2 --workers 2 --pop-size 6 --iterations 2 --output-dir batch_parallel` | 1 | PermissionError: [WinError 5] Access is denied |
| experiments_cli | `D:\Downloads\Aquaroda\python.exe implementation/scripts/run_experiments.py --dataset data/stores/50_uniform_users_connect.csv --pop-size 6 --iterations 2 --seeds 42 123` | 0 | Da luu bieu do hoi tu Monte Carlo tai: D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\implementation\results\monte_carlo_convergence_50_uniform_users_connect.png |
| plot_scenarios | `D:\Downloads\Aquaroda\python.exe implementation/scripts/plot_scenarios.py` | 0 |  |
| build_audit_report | `D:\Downloads\Aquaroda\python.exe implementation/scripts/build_fitness_audit_report.py` | 0 |  |
| build_report_evidence | `D:\Downloads\Aquaroda\python.exe implementation/scripts/build_report_evidence.py` | 0 |  |
| analyze_1 | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze.py synthetic_runs.csv --output synthetic_analysis_1 --expected-runs 2 --resamples 100` | 0 |  |
| analyze_2 | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze.py synthetic_runs.csv --output synthetic_analysis_2 --expected-runs 2 --resamples 100` | 0 |  |
| ruff | `D:\Downloads\Aquaroda\python.exe -m ruff check implementation/src implementation/scripts` | 1 | [*] 7 fixable with the --fix option (2 hidden fixes can be enabled with the --unsafe-fixes option). |
| flake8 | `D:\Downloads\Aquaroda\python.exe -m flake8 implementation/src` | 1 | PermissionError: [WinError 5] Access is denied |
| mypy | `D:\Downloads\Aquaroda\python.exe -m mypy implementation/src` | 124 | TIMEOUT |
| vulture | not installed | N/A | NOT_INSTALLED |
| counter | `D:\Downloads\Aquaroda\python.exe -c from src.counter import FitnessCounter` | 1 | ModuleNotFoundError: No module named 'src.counter' |
| benchmark | `D:\Downloads\Aquaroda\python.exe run_benchmark.py --smoke` | 2 | D:\Downloads\Aquaroda\python.exe: can't open file 'D:\\Personal Base\\UAV-Placement-Optimization-for-Wireless-Networks\\tmp_audit\\audit_045f1c6d6720\\run_benchmark.py': [Errno 2] No such file or directory |
| ablation_analysis | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze_ablation.py synthetic_runs.csv` | 2 | D:\Downloads\Aquaroda\python.exe: can't open file 'D:\\Personal Base\\UAV-Placement-Optimization-for-Wireless-Networks\\tmp_audit\\audit_045f1c6d6720\\implementation\\scripts\\analyze_ablation.py': [Errno 2] No such file or direct |
| resume | `D:\Downloads\Aquaroda\python.exe implementation/scripts/run_batch.py --resume` | 2 | run_batch.py: error: unrecognized arguments: --resume |
| clean_venv | `D:\Downloads\Aquaroda\python.exe -m venv clean_venv` | 1 | Error: Command '['D:\\Personal Base\\UAV-Placement-Optimization-for-Wireless-Networks\\tmp_audit\\audit_045f1c6d6720\\clean_venv\\Scripts\\python.exe', '-m', 'ensurepip', '--upgrade', '--default-pip']' returned non-zero exit statu |
| clean_install_lock | `D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\clean_venv\Scripts\python.exe -m pip install --no-index -r D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\requirements.lock.txt` | 1 | D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\clean_venv\Scripts\python.exe: No module named pip |
| pip_check | `D:\Downloads\Aquaroda\python.exe -m pip check` | 0 | No broken requirements found. |
| generate_help | `D:\Downloads\Aquaroda\python.exe implementation/scripts/generate_dataset.py --help` | 0 |                         Số CSV cần tạo, mặc định: 500 |
| analyze_legacy | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze.py D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\batch_serial\batch_results_custom.csv --output legacy_statistics --expected-runs 1 --resamples 100` | 1 | ValueError: Missing columns: ['algo_seed', 'algorithm', 'batch_id', 'batch_total_cpu_s', 'batch_wall_time_s', 'cpu_time_s', 'data_seed', 'distribution', 'fe_used', 'feasible', 'fitness', 'instance_k', 'n_workers', 'purpose', 'run_ |
| stability_legacy | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze_stability.py D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\batch_serial\batch_results_custom.csv --output legacy_stability` | 1 | ValueError: Missing CSV columns: ['C', 'E', 'I', 'algo_seed', 'algorithm', 'data_seed', 'distribution', 'fe_used', 'feasible', 'fitness', 'hit_target', 'instance_k', 'purpose', 'run_id', 'scenario_id', 'ue_count', 'ue_pass', 'ue_t |
| sensitivity_legacy | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze_sensitivity.py D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\batch_serial\batch_results_custom.csv --output legacy_sensitivity` | 1 | ValueError: Missing columns: ['C', 'C_sinr', 'C_snr', 'E', 'I', 'algo_seed', 'algorithm', 'config_id', 'data_seed', 'distribution', 'fe_used', 'feasible', 'fitness', 'instance_k', 'purpose', 'reoptimized', 'run_id', 'scenario_id', |
| sensitivity_synthetic_1 | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze_sensitivity.py synthetic_sensitivity.csv --output synthetic_sensitivity_1` | 0 |  |
| sensitivity_synthetic_2 | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze_sensitivity.py synthetic_sensitivity.csv --output synthetic_sensitivity_2` | 0 |  |
| stability_synthetic_1 | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze_stability.py synthetic_runs_stability.csv --output synthetic_stability_1` | 0 |  |
| stability_synthetic_2 | `D:\Downloads\Aquaroda\python.exe implementation/scripts/analyze_stability.py synthetic_runs_stability.csv --output synthetic_stability_2` | 0 |  |
| activation_readme | `powershell -NoProfile -Command .\.venv\Scripts\Activate.ps1` | 1 |     + FullyQualifiedErrorId : CommandNotFoundException |
| pip_dry_run_readme | `D:\Downloads\Aquaroda\python.exe -m pip install --dry-run --no-index -r implementation/requirements.txt` | 1 | You can safely remove it manually. |
| scalability_help | `D:\Downloads\Aquaroda\python.exe implementation/scripts/run_scalability_analysis.py --help` | 0 |   --seed SEED           Random seed. |
| flake8_single | `D:\Downloads\Aquaroda\python.exe -m flake8 --jobs 1 implementation/src` | 1 | implementation/src\visualization\dataset_views.py:62:80: E501 line too long (86 > 79 characters) |
| mypy_scoped | `D:\Downloads\Aquaroda\python.exe -m mypy --follow-imports skip --ignore-missing-imports --cache-dir D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\mypy_cache implementation/src/counter.py` | 2 | mypy: can't read file 'implementation\src\counter.py': No such file or directory |
| venv_without_pip | `D:\Downloads\Aquaroda\python.exe -m venv --without-pip isolated_no_pip` | 0 |  |
| isolated_import_numpy | `D:\Personal Base\UAV-Placement-Optimization-for-Wireless-Networks\tmp_audit\audit_045f1c6d6720\isolated_no_pip\Scripts\python.exe -c import numpy` | 1 | ModuleNotFoundError: No module named 'numpy' |

Các stdout/stderr đầy đủ nằm dưới ../tmp_audit/audit_045f1c6d6720/evidence/. Mã 0 của analyzer
trên CSV synthetic chỉ xác nhận phần mềm phân tích nhận được schema kiểm thử.
Chưa có kết quả tối ưu thật từ runner mới.

## FE quan sát theo code cũ

| Algorithm | Iterations | Calls | WOA reference | Delta |
|---|---:|---:|---:|---:|
| GA | 1 | 12 | 12 | 0 |
| PSO | 1 | 12 | 12 | 0 |
| WOA | 1 | 12 | 12 | 0 |
| HPSOGA | 1 | 12 | 12 | 0 |
| HWOAPSO | 1 | 12 | 12 | 0 |
| IWOA | 1 | 28 | 12 | 16 |
| ablation_000 | 1 | 12 | 12 | 0 |
| ablation_001 | 1 | 16 | 12 | 4 |
| ablation_010 | 1 | 18 | 12 | 6 |
| ablation_011 | 1 | 28 | 12 | 16 |
| ablation_100 | 1 | 12 | 12 | 0 |
| ablation_101 | 1 | 16 | 12 | 4 |
| ablation_110 | 1 | 18 | 12 | 6 |
| ablation_111 | 1 | 28 | 12 | 16 |
| GA | 3 | 24 | 24 | 0 |
| PSO | 3 | 24 | 24 | 0 |
| WOA | 3 | 24 | 24 | 0 |
| HPSOGA | 3 | 24 | 24 | 0 |
| HWOAPSO | 3 | 24 | 24 | 0 |
| IWOA | 3 | 43 | 24 | 19 |
| ablation_000 | 3 | 24 | 24 | 0 |
| ablation_001 | 3 | 33 | 24 | 9 |
| ablation_010 | 3 | 36 | 24 | 12 |
| ablation_011 | 3 | 43 | 24 | 19 |
| ablation_100 | 3 | 24 | 24 | 0 |
| ablation_101 | 3 | 33 | 24 | 9 |
| ablation_110 | 3 | 36 | 24 | 12 |
| ablation_111 | 3 | 43 | 24 | 19 |
| GA | 6 | 42 | 42 | 0 |
| PSO | 6 | 42 | 42 | 0 |
| WOA | 6 | 42 | 42 | 0 |
| HPSOGA | 6 | 42 | 42 | 0 |
| HWOAPSO | 6 | 42 | 42 | 0 |
| IWOA | 6 | 73 | 42 | 31 |
| ablation_000 | 6 | 42 | 42 | 0 |
| ablation_001 | 6 | 50 | 42 | 8 |
| ablation_010 | 6 | 60 | 42 | 18 |
| ablation_011 | 6 | 73 | 42 | 31 |
| ablation_100 | 6 | 42 | 42 | 0 |
| ablation_101 | 6 | 50 | 42 | 8 |
| ablation_110 | 6 | 60 | 42 | 18 |
| ablation_111 | 6 | 73 | 42 | 31 |

Đây là ngân sách theo iterations, không phải kiểm thử max_fe. Mọi chênh lệch
là số gọi thực đo, không kỳ vọng xác suất. K-Means tự nó không gọi Fitness;
chỉ thay cá thể trước lần đánh giá ban đầu. OBL và Lévy đánh giá bổ sung.

## (a) Lỗi đang có

| ID / mức | File, dòng | Bằng chứng | Đề xuất, chưa áp dụng |
|---|---|---|---|
| E01 cao | run_batch.py:134-148; analyze.py:72-76 | analyze_legacy/stability_legacy/sensitivity_legacy exit 1 thiếu schema | Không đổi tên cột rồi bịa FE/CPU/seed. Cần runner mới đo các trường còn thiếu; đây là thay đổi kiến trúc chưa có patch an toàn ngắn |
| E02 trung bình | problem/objective.py:56-57 | nan_weights trả NaN | validate_weights.patch: kiểm weights và threshold |
| E03 trung bình | objectives/metrics.py:105-115 | helper UE rỗng trả NaN và warning | empty_metrics_guard.patch: chặn đầu vào rỗng/shape sai |
| E04 trung bình | I_WOA/levy_flight.py:14-16 | beta=0 ZeroDivisionError | levy_beta_guard.patch: xác định miền beta hợp lệ cho Mantegna; thay đổi input-invalid contract, cần duyệt |
| E05 cao khi suy luận | analyze_sensitivity.py:76 | ghép theo run_id trong KEYS, chưa gộp instance | sensitivity_instance_pairs.patch: gộp trung vị run theo instance trước kiểm định; chưa chứng minh bootstrap/CI của sensitivity đầy đủ |
| E06 thấp | WOA/optimizer.py:45; các params | population=0 ValueError max(empty) | Cần validation population trước khởi tạo; đây là input ngoài CLI đã kiểm pop>0, không làm sai các run mặc định |
| E07 trung bình | README.md:5,124-128; TALK.md:99,208 | doc_links.json; nguồn thiếu | Rút link/số cũ, dẫn REPORT.md; không tự phục hồi số liệu làm bằng chứng |
| E08 thấp | ruff/flake8 file-line trong log | Ruff báo lỗi, Flake8 --jobs 1 báo style/import | Rà từng F401/F841 và style, không tự --fix; không suy từ lint rằng thuật toán tính sai |

Các patch áp dụng vào bản gốc cần duyệt; không patch lỗi quyền Windows bằng
thay đổi thuật toán. Với E01/E07 và các chức năng chưa làm, bản thiết kế được
ghi thay vì tạo diff giả đầy đủ. Chưa đáp ứng yêu cầu “mỗi lỗi có diff đã
kiểm thử”; các diff hiện mới là đề xuất, chưa áp dụng/chưa test hậu sửa.

## (b) Chưa cài đặt / còn thiếu

- Counter BudgetExhausted, dừng giữa vòng, lịch a/w theo FE.
- Runner benchmark, benchmark.yaml, data/algo seed manifest và quần thể
  ban đầu chung; hiện cùng seed không bảo đảm cùng quần thể.
- runs.csv schema mới, convergence theo FE, metadata env và lock.
- Resume/checkpoint và test kill/restart; không có để kiểm lúc này.
- analyze_ablation.py và dữ liệu ablation theo FE; tái tối ưu sensitivity.
- REPRODUCE.md và kiểm chứng môi trường sạch; kết quả kiểm định thật.

## (c) Cảnh báo chưa chắc là lỗi

- WinError 5 của multiprocessing và ensurepip có thể do sandbox/host;
  cần kiểm trên môi trường người dùng cho phép pipe, không quy kết lỗi code.
- Không có nguồn hiệu chuẩn E/I, tham số môi trường/UE cao hơn UAV;
  số học đạt không chứng minh đúng vật lý.
- Không thể chứng minh tính độc lập instance chỉ từ CSV cân bằng.
- Các numeric literal trong phân tích gồm alpha, bootstrap, định nghĩa
  effect và threshold định trước; chỉ coi là bịa kết quả khi có bằng chứng.
- PyYAML/pytest không được khai báo trực tiếp trong requirements.txt hiện
  tại dù được dùng; môi trường host có sẵn không bảo đảm venv sạch đủ.

## Mức sẵn sàng sản phẩm bàn giao

| Sản phẩm | Trạng thái | Lý do |
|---|---|---|
| Mã mô hình và kiểm thử | ĐỦ phần số học đã thử; THIẾU xác thực vật lý | ca hợp lệ pass; còn validation và giả định |
| Thiết kế đối chứng FE tái lập | THIẾU | counter/runner/manifest chưa có |
| Dữ liệu đầu vào và bộ sinh | ĐỦ bộ sinh đã thử; THIẾU manifest chính thức | năm phân bố chạy được |
| Log đầy đủ seed/FE/thời gian/env | THIẾU | batch cũ không đủ schema |
| Bảng tổng hợp tái tạo từ log thật | LỖI tích hợp | analyzer mới không nhận CSV batch cũ |
| Biểu đồ hội tụ FE và ablation | THIẾU | chưa chạy pipeline FE |
| Thảo luận giới hạn | ĐỦ bản docs mới; LỖI README/TALK cũ | chưa đồng bộ mọi tài liệu |
| Hướng dẫn tái lập từ checkout sạch | THIẾU | REPRODUCE/lock chưa có |

## Năm rủi ro lớn nhất

1. So sánh cùng iterations nhưng khác FE làm sai diễn giải hiệu quả thuật toán.
2. Chưa nối runner/log/schema: không thể tạo bảng kiểm định từ thí nghiệm thật.
3. E/I proxy và miền áp dụng kênh chưa được xác minh: kết luận mạng thực quá mức.
4. Giả lặp theo run và quần thể khởi tạo không ghép cặp làm yếu căn cứ thống kê.
5. README/TALK còn số cũ, thiếu lock/env và chưa kiểm venv/đa tiến trình sạch.

## Kết quả phải chạy lại khi sửa

- Thay ràng buộc, E/I, bộ tham số kênh hoặc SNR/SINR: chạy lại mọi đối chứng
  liên quan, không gộp điểm Fitness khác định nghĩa.
- Chuyển iterations sang FE, ghép quần thể, đổi lịch a/w: chạy lại cả sáu
  thuật toán và tám cấu hình; log cũ không tự chuyển thành FE đúng được.
- Chỉ sửa validation: đầu vào hợp lệ không nhất thiết phải chạy lại; loại
  run sai cấu hình và kiểm tra tương đương bằng regression trước khi quyết định.
- Sửa gộp instance ở sensitivity: chạy lại phân tích từ log đầy đủ nếu log
  đã đúng; không bắt buộc tối ưu lại chỉ vì đổi phép thống kê.
- Chỉ sửa style/tài liệu: không tự yêu cầu chạy lại tối ưu; phải kiểm tra
  hành vi nếu đụng import hoặc code thực thi.

## Giới hạn audit và các yêu cầu chưa hoàn thành

Không chạy nguyên các lệnh full-budget README; dùng lệnh giới hạn được ghi
rõ. Không có counter nên chưa thử đúng max_fe nhỏ/vừa/gấp đôi. Không kill
resume, không xác nhận Linux, môi trường sạch cài từ lock, không chứng minh
không mã chết hoặc mọi YAML key được dùng. Không sửa code để ép test pass.
Chi tiết ca chưa chạy/missing đều là hạn chế, không có mục “có vẻ ổn”.


## Patch applicability checks (proposals only)

- `tmp_audit\audit_045f1c6d6720\evidence\patches\empty_metrics_guard.patch`: git apply --check exit=0; not applied.
- `tmp_audit\audit_045f1c6d6720\evidence\patches\levy_beta_guard.patch`: git apply --check exit=0; not applied.
- `tmp_audit\audit_045f1c6d6720\evidence\patches\lint_safe_subset.patch`: git apply --check exit=0; not applied.
- `tmp_audit\audit_045f1c6d6720\evidence\patches\readme_broken_results.patch`: git apply --check exit=0; not applied.
- `tmp_audit\audit_045f1c6d6720\evidence\patches\sensitivity_instance_pairs.patch`: git apply --check exit=0; not applied.
- `tmp_audit\audit_045f1c6d6720\evidence\patches\validate_weights.patch`: git apply --check exit=0; not applied.
- `tmp_audit\audit_045f1c6d6720\evidence\patches\woa_population_guard.patch`: git apply --check exit=0; not applied.

Initial patch checks exposed CRLF/path incompatibilities; proposals were regenerated preserving source line endings. No source was edited.
