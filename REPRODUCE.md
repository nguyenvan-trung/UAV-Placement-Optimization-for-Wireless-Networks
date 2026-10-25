# Chuẩn bị môi trường và tái lập đúng luồng

[Trang đầu](README.md) · [Mục lục](implementation/docs/README.md) · [Trạng thái](implementation/docs/PROJECT_GUIDE.md)

Các lệnh là hướng dẫn dành cho lần thực thi sau khi có yêu cầu. Việc có lệnh trong tài liệu không có nghĩa lệnh đã được chạy. Study notebook hiện chưa chạy và chưa chốt seed.

## 1. Chọn luồng trước khi thực thi

| Nhu cầu | Luồng | Tài liệu |
|---|---|---|
| 500 CSV, 30 case, 100 vòng, bảng/ảnh trong notebook | Notebook | [NOTEBOOK_STUDY](implementation/docs/NOTEBOOK_STUDY.md) |
| So sánh cùng FE trên các phân bố sinh mới | Benchmark FE | [EXPERIMENT_DESIGN](implementation/docs/EXPERIMENT_DESIGN.md) |
| Chạy một CSV hoặc batch sáu thuật toán | Script legacy | [scripts/README](implementation/scripts/README.md) |

Không lấy output của luồng này làm input analyzer luồng kia nếu chưa có chuyển đổi schema đúng và giao thức phù hợp.

## 2. Môi trường

Dùng Python hỗ trợ cú pháp hiện tại (từ 3.10). Phiên trước dùng Python 3.13.9 và thư viện đã có sẵn; đó không phải cam kết cài sạch từ lock trên mọi máy.

Chạy lệnh dưới từ gốc repository chỉ khi muốn chuẩn bị môi trường. Không ghi đè môi trường đang dùng; ví dụ dùng tên riêng .venv-study:

```powershell
python -m venv .venv-study
.\.venv-study\Scripts\python.exe -m pip install -r implementation\requirements.txt
```

Hoặc cài requirements.lock.txt nếu muốn thử đúng snapshot phiên bản. Cài sạch từ lock chưa được xác minh. Thư mục .venv cũ có bố cục bin/lib và không có executable Windows tại Scripts/python.exe trong phiên trước; chỉ chọn một interpreter thực sự tồn tại.

Mở Jupyter/VS Code rồi chọn đúng kernel của môi trường có dependencies. Không cần Activate.ps1 nếu gọi trực tiếp interpreter.

## 3. Notebook 100 vòng

1. Đọc [NOTEBOOK_STUDY](implementation/docs/NOTEBOOK_STUDY.md) và [cấu hình](configs/notebook_study.json).
2. Chốt danh sách seed đánh giá, ít nhất hai seed khác nhau; ghi lựa chọn trước khi nhìn kết quả.
3. Mở [notebook](implementation/notebooks/full_study_100_iterations.ipynb), chọn kernel và chạy ô thiết lập/thiết kế khi được yêu cầu thực thi.
4. Kiểm tra số task = 500 × 30 × số seed; output riêng cho thiết kế.
5. Chỉ đặt CONFIRM_RUN=True khi đã có xác nhận chạy. Sau đó chạy ô thí nghiệm.
6. Sau completion, chạy các ô đọc bảng và vẽ ảnh. Những ô này không chạy lại optimizer.

Giữ bản gốc mặc định False và seeds=[] trong repository. Không chỉnh cấu hình hoặc source giữa chừng rồi resume vào cùng output. Không mở hai runner cùng output. Nếu cần dừng, ngắt kernel; task JSON đã hoàn tất được giữ. Hướng dẫn khóa/resume trong NOTEBOOK_STUDY.

## 4. Benchmark FE riêng

Nguồn thiết kế: [benchmark.yaml](configs/benchmark.yaml); manifest: [seeds.csv](seeds/seeds.csv). Runner sinh tọa độ từ data_seed; không đọc trực tiếp 500 CSV. Chốt số instance, số run và ngân sách trước chạy. Target hiện null; không báo hit-rate như tỷ lệ thất bại.

Ví dụ lệnh, chỉ thực thi khi được yêu cầu:

```powershell
python run_benchmark.py --smoke --output tmp_audit/my_fe_smoke --workers 1
python run_benchmark.py --output results/benchmark_fe_01 --workers 1
python run_benchmark.py --output results/benchmark_fe_01 --workers 1 --resume
```

Smoke dùng ngân sách nhỏ và không đại diện study. Runner có mode ablation/sensitivity riêng. Chữ ký resume gồm source/config/seed/mode/workers; không đổi các phần đó trong một output.

Đầu ra FE có runs.csv, convergence, solutions, env.json, config/seed/lock và completion. Đọc [DATA_FORMAT](implementation/docs/DATA_FORMAT.md) trước khi phân tích. analyze.py dành cho sáu thuật toán chính, không tự hỗ trợ 30 case.

## 5. Kiểm tra và nguồn bằng chứng

Đọc mã hoặc tài liệu không cần chạy test. Khi thực hiện kiểm tra sau này, tách output test khỏi kết quả thật và ghi rõ phạm vi. Một số test có thể tạo artifact; không đưa các bảng đó vào báo cáo nghiên cứu.

Để gọi một kết quả là tái lập được, cần giữ input, source/config, seed, môi trường, log, phép gộp và artifact. Notebook hiện có manifest/hash/task checkpoint nhưng chưa thu đủ metadata môi trường như env.json của runner FE. Không tuyên bố hai luồng có cùng mức ghi nhận môi trường.

Xem [REPORT_EVIDENCE](implementation/docs/REPORT_EVIDENCE.md) trước khi bổ sung số liệu vào báo cáo.
