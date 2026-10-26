# Tối ưu vị trí UAV cho mạng không dây

Tìm vị trí ba chiều cho các UAV phát sóng để phục vụ một tập người dùng cố định. Người đọc có thể theo dõi dự án theo thứ tự: **bài toán → mô hình → thuật toán → thiết kế thí nghiệm → kết quả có nguồn**.

**Trạng thái:** study đã dừng theo yêu cầu; kết quả, log và file tạm đã được xóa. Giữ nguyên 500 CSV đầu vào và cấu hình 30 trường hợp / 100 vòng / 30 seed. Xem [trạng thái](implementation/docs/RUN_STATUS.md). Chưa có kết quả để xếp hạng toàn study.

## Mục lục

0. [Cài đặt, chạy và đọc kết quả](#bat-dau)
1. [Mô hình tổng quan](#tong-quan)
2. [Đầu vào, đầu ra và một ví dụ](#dau-vao)
3. [Cách chấm một phương án](#fitness)
4. [Sáu thuật toán và 30 trường hợp](#thuat-toan)
5. [Ba luồng thực thi](#luong-chay)
6. [Bản đồ thư mục](#thu-muc)
7. [Lộ trình đọc tài liệu](#lo-trinh)
8. [Nguồn và trạng thái kiểm chứng](#nguon)

<a id="bat-dau"></a>

## Cài đặt, chạy và đọc kết quả

Các lệnh dưới đây dùng **PowerShell trên Windows**, chạy tại thư mục gốc repository, nơi có `configs/`, `data/` và `implementation/`. Cần Python **3.10 trở lên**; dùng bản Python cho Windows, không chọn nhầm Python của MSYS2. Việc cài môi trường không khởi chạy thí nghiệm.

### 1. Cài môi trường

Tạo môi trường mới để tránh dùng nhầm `.venv` cũ:

```powershell
py -3 -m venv .venv-uav
& ".\.venv-uav\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv-uav\Scripts\python.exe" -m pip install -r implementation\requirements.txt ipykernel nbformat
```

Nếu không có lệnh `py`, thay `py -3` bằng đường dẫn đến Python đã cài. Không cần activate môi trường vì các lệnh gọi trực tiếp interpreter.

Kiểm tra thư viện mà không chạy optimizer:

```powershell
& ".\.venv-uav\Scripts\python.exe" -B -c "import numpy, pandas, scipy, sklearn, matplotlib, ipykernel, nbformat, tabulate, threadpoolctl; print('Environment OK')"
```

### 2. Kiểm tra dữ liệu và cấu hình

Đầu vào là **500 file có sẵn** tại `data/stores/*_users_connect.csv`. Không cần sinh lại dữ liệu. Xem [hướng dẫn dữ liệu](data/README.md).

```powershell
(Get-ChildItem data\stores\*_users_connect.csv -File).Count
Get-Content configs\notebook_study.json
```

Cấu hình luồng này nằm trong **`configs/notebook_study.json`**:

| Tham số | Hiện tại |
|---|---|
| `iterations` | 100 vòng mỗi lượt |
| `population` | 25 phương án bố trí UAV |
| `num_uavs` | 4 UAV mỗi phương án |
| `seeds` | 30 seed cố định |
| `output` | `implementation/results/study_100_iterations` |

30 case được định nghĩa trong `implementation/src/notebook_study.py`: ba họ GA/PSO/WOA, mỗi họ có tám tổ hợp bật/tắt K-Means, OBL, Lévy; thêm sáu case hybrid. `benchmark.yaml` và `sensitivity.yaml` thuộc luồng FE riêng, không điều khiển study CSV này.

Tổng khối lượng: **500 dataset × 30 case × 30 seed = 450.000 lượt tối ưu**. Một lượt là một tổ hợp dataset–case–seed. Đây là tác vụ dài, có thể mất nhiều ngày tùy máy.

### 3. Chạy toàn bộ dữ liệu

Chỉ chạy lệnh này khi muốn bắt đầu hoặc tiếp tục study:

```powershell
& ".\.venv-uav\Scripts\python.exe" -B implementation\scripts\run_notebook_study.py --workers 4
```

Giữ terminal mở và máy hoạt động; tránh sleep. Chỉ chạy một coordinator cho cùng thư mục output. Có thể giảm `--workers` để giảm tải trước lần chạy mới; khi tiếp tục một study phải giữ nguyên số worker, dữ liệu, code, cấu hình và môi trường.

**Theo dõi** ở terminal khác:

```powershell
Get-Content implementation\results\study_100_iterations\progress.json
Get-Content implementation\results\study_100_iterations\logs\worker_00.log -Tail 20
```

`completed/expected` đếm lượt tối ưu, không đếm dataset. `eta_s` là số giây còn lại ước tính, có thể thay đổi; `phase` cho biết đang tối ưu, tổng hợp, hoàn tất hoặc gặp lỗi. File không cập nhật có thể là tiến độ cũ; kiểm tra terminal và log nếu nghi ngờ tiến trình đã dừng.

**Dừng:** nhấn `Ctrl+C` trong terminal chạy chính. Checkpoint đã ghi được giữ lại. Chạy lại cùng lệnh để tiếp tục sau khi xác nhận các tiến trình cũ đã dừng; các task hợp lệ được kiểm tra rồi bỏ qua. Nếu bị tắt cưỡng bức, có thể còn `.coordinator`/`.running`; chỉ gỡ khóa sau khi xác minh không còn coordinator/worker. Đổi code/config/data hoặc số worker thì dùng output mới. Nếu đã xóa checkpoint, lần chạy sau bắt đầu từ đầu.

### 4. Cấu trúc file kết quả

```text
implementation/results/
├── README.md
├── READING_RESULTS.md
└── study_100_iterations/             # Chỉ xuất hiện sau khi chạy
    ├── manifest.json                # Cấu hình, case, dataset, chữ ký source/input
    ├── progress.json                # Tiến độ cập nhật trong khi chạy
    ├── completion.json              # Chỉ ghi sau khi xuất báo cáo thành công
    ├── runs.csv                     # Tất cả lượt chạy, sau khi đủ task
    ├── RESULTS.md                   # Báo cáo tổng hợp
    ├── study_results.ipynb           # Bảng và 13 ảnh nhúng
    ├── datasets/                    # CSV để mở trong Excel
    │   ├── 001_UAV_3D_50/
    │   │   ├── 001_UAV_3D_50_result.csv
    │   │   ├── 001_UAV_3D_50_positions.csv
    │   │   └── 001_UAV_3D_50_convergence.csv
    │   └── ...                      # Các dataset khác
    ├── tables/                      # Bảng CSV và Markdown (.md)
    │   ├── design.csv               # Bảng bật/tắt các thành phần
    │   ├── by_dataset.csv           # Trung bình/SD qua seed trên từng dataset
    │   ├── by_scale.csv             # Gộp theo số user và case
    │   ├── main.csv                 # Sáu phương pháp chính
    │   ├── GA.csv / PSO.csv / WOA.csv
    │   ├── ranking.csv
    │   └── ...                      # Hội tụ, độ ổn định, đóng góp, hybrid
    ├── figures/                     # 13 PNG: hội tụ, quy mô, bố trí UAV 3D
    ├── logs/                        # worker_00.log đến worker_03.log
    └── shards/                      # Checkpoint nội bộ để tiếp tục
        └── worker_00/               # Tương tự worker_01, 02, 03
            ├── manifest.json
            ├── env.json
            ├── progress.json
            └── tasks/001_UAV_3D_50/
                └── 001_UAV_3D_50_result_GA_seed1051920946.json.gz
```

File kết quả đặt theo tên dataset. Hậu tố case và seed phân biệt các lượt chạy; `.json.gz` là JSON nén dùng nội bộ để resume. Các file CSV dành cho người đọc được lưu UTF-8 BOM để mở bằng Excel.

**Thời điểm xuất:** mỗi dataset chạy đủ **30 case × 30 seed = 900 lượt** mới có bộ ba CSV của dataset đó. Bảng toàn study, ảnh và notebook báo cáo được xuất sau khi tất cả worker hoàn tất. Vì vậy lúc đầu có checkpoint nhưng chưa có CSV/ảnh là bình thường. Lệnh chạy trực tiếp in tiến độ/lỗi ra terminal; các file `*.launch.log` hoặc `*.error.log` ở ngoài thư mục study chỉ có nếu chủ động chuyển hướng đầu ra, không tự được tạo bởi lệnh trên.

### 5. Đọc bảng và xem ảnh trong notebook

- Mở `datasets/<dataset>/<dataset>_result.csv` để so sánh các case/seed của một dataset. `positions.csv` lưu tọa độ nghiệm cuối, `convergence.csv` lưu chỉ số vòng 0–100.
- Mở `tables/by_dataset.csv` để xem trung bình và độ lệch chuẩn qua seed; `tables/by_scale.csv` gộp theo số user, nên không có một dòng riêng cho mỗi file đầu vào.
- Khi hoàn tất, mở `study_results.ipynb`: các bảng và ảnh đã được nhúng sẵn, không cần chạy optimizer lại.
- Muốn tự tạo lại ảnh từ artifact, mở `implementation/notebooks/full_study_100_iterations.ipynb`, bấm **Select Kernel → Python Environments**, chọn `.venv-uav\Scripts\python.exe`. Chạy ô thiết lập, đọc bảng và vẽ; giữ **`CONFIRM_RUN = False`** nếu chỉ xem kết quả. Notebook và script dùng chung hàm tạo ảnh: script tự xuất PNG vào `figures/`, notebook có thể tạo lại và hiển thị ảnh dưới ô code.

Ý nghĩa cột và thứ tự đọc chi tiết: [READING_RESULTS](implementation/results/READING_RESULTS.md). Khi chưa có kết quả đầy đủ, không dùng số liệu kiểm tra hoặc checkpoint dở để kết luận thứ hạng toàn study.

<a id="tong-quan"></a>

## 1. Mô hình tổng quan

![Mô hình tổng quan: dữ liệu user, bài toán, thuật toán, fitness, lưu task và tổng hợp](implementation/docs/assets/overview.svg)

**Cách đọc sơ đồ:** bắt đầu từ tọa độ user; tạo bài toán đặt UAV; thuật toán liên tục đề xuất cấu hình và nhận điểm fitness; cuối cùng lưu lịch sử để tổng hợp. Khối “đánh giá” được gọi nhiều lần trong tìm kiếm, không phải chỉ một lần sau khi thuật toán kết thúc.

| Khối | Giải thích |
|---|---|
| Dữ liệu user | Cùng một CSV được dùng cho mọi case và seed; thuật toán không di chuyển user |
| Bài toán | Xác định nghiệm hợp lệ và dùng chung cách chấm |
| Thuật toán | Khác nhau ở cách tạo/cập nhật ứng viên |
| Fitness | Cùng mô hình để đối chứng có ý nghĩa |
| Task | Một bộ dataset–case–seed; là đơn vị lưu/tiếp tục |
| Báo cáo | Đọc artifact; không lấy ảnh minh họa làm số đo thuật toán |

Sơ đồ do dự án biên soạn từ [runner notebook](implementation/src/notebook_study.py) và [bài toán](implementation/src/problem/objective.py), không phải hình lấy từ bài báo.

<a id="dau-vao"></a>

## 2. Đầu vào, đầu ra và một ví dụ

**Đầu vào:** một CSV có cột user_id, x_m, y_m, z_m, demand. Tọa độ dùng mét. Bộ hiện có gồm 500 file, 10 mức từ 50 đến 500 user, mỗi mức 50 file. User có độ cao 0–132 m theo rà soát, nên không gọi toàn bộ bộ dữ liệu là user mặt đất.

**Một nghiệm:** vector ghép tọa độ N UAV. Với N=4, nghiệm có D=12 số:

`X = [x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4]`.

**Ví dụ minh họa:** dataset 100 user, một ứng viên chứa vị trí của cả bốn UAV. Quần thể P=25 nghĩa là có 25 cấu hình bốn UAV, không phải 25 UAV. Sau 100 vòng, lưu best đã đánh giá và các mốc lịch sử. Đây là diễn giải cấu trúc, không phải số đo của một lần chạy.

Định dạng đầy đủ: [DATA_FORMAT](implementation/docs/DATA_FORMAT.md).

<a id="fitness"></a>

## 3. Cách chấm một phương án

`F = 0,6 × C − 0,2 × E − 0,2 × I`, cực đại hóa.

| Thành phần | Định nghĩa dễ đọc | Chiều mong muốn |
|---|---|---|
| C | Tỷ lệ user được ít nhất một UAV phủ theo ngưỡng SNR | Cao |
| E | Proxy công suất trung bình chuẩn hóa theo độ cao | Thấp |
| I | Tỷ lệ user có từ hai liên kết SNR đạt ngưỡng | Thấp |

E chưa phải năng lượng Joule; I chưa phải công suất nhiễu. Trọng số là lựa chọn thiết kế, không phải tỷ lệ chuẩn của ngành. Công thức có bảng ký hiệu, đơn vị và nguồn tại [REPORT](implementation/docs/REPORT.md); bảng truy nguồn tại [SOURCES](implementation/docs/SOURCES.md).

<a id="thuat-toan"></a>

## 4. Sáu thuật toán và 30 trường hợp

| Thuật toán chính | Ý tưởng | Giải thích chi tiết |
|---|---|---|
| GA | Chọn cha mẹ, lai ghép, đột biến và giữ elite | [DWGA](implementation/docs/DWGA.md) |
| PSO | Di chuyển theo vận tốc, pbest và gbest | [DWPSO](implementation/docs/DWPSO.md) |
| WOA | Bao vây, khám phá hoặc xoắn ốc quanh best | [DWWOA](implementation/docs/DWWOA.md) |
| H-PSO-GA | Bước PSO rồi crossover/mutation | [DWH_PSO_GA](implementation/docs/DWH_PSO_GA.md) |
| H-WOA-PSO | Trộn hai đề xuất trên mỗi cá thể | [DWH_WOA_PSO](implementation/docs/DWH_WOA_PSO.md) |
| I-WOA | WOA thêm K-Means, OBL và Lévy | [DWI_WOA](implementation/docs/DWI_WOA.md) |

Study mở rộng thành 24 case của ba họ WOA/PSO/GA, hai bản lai đầy đủ và bốn case ablation bản lai: **30 case duy nhất**. Một case có thể xuất hiện trong nhiều bảng nhưng không phải chạy lại. Xem bảng bật/tắt trong [NOTEBOOK_STUDY](implementation/docs/NOTEBOOK_STUDY.md).

<a id="luong-chay"></a>

## 5. Ba luồng thực thi

| Luồng | Đầu vào | Ngân sách và phạm vi |
|---|---|---|
| Notebook hiện tại | 500 CSV có sẵn | 30 case, 100 vòng, P=25, N=4 |
| Benchmark FE | Dữ liệu sinh từ YAML/manifest | Mặc định 3030 FE, P=30; schema riêng |
| Script CSV legacy | CSV có sẵn | Một dataset hoặc batch sáu thuật toán theo vòng |

FE là một lần đánh giá fitness. Cùng vòng không bảo đảm cùng FE, đặc biệt khi có OBL/Lévy. Không gộp ba luồng như cùng giao thức. Hướng dẫn môi trường và thực thi: [REPRODUCE](REPRODUCE.md).

<a id="thu-muc"></a>

## 6. Bản đồ thư mục

| Đường dẫn từ gốc repository | Chứa gì? |
|---|---|
| configs/ | Cấu hình notebook và FE |
| data/stores/ | Tọa độ user đầu vào |
| data/views/ | Ảnh quan sát input |
| implementation/src/ | Mô hình và thuật toán |
| implementation/notebooks/ | Notebook study và trình bày |
| implementation/scripts/ | Điểm vào CLI/analyzer |
| implementation/docs/ | Phương pháp, thiết kế, nguồn và hướng dẫn |
| implementation/docs/assets/ | Sơ đồ SVG nhúng vào Markdown |
| implementation/tests/ | Kiểm tra mã |
| implementation/results/ | Đầu ra khi được thực thi |
| documents/ | Danh mục tài liệu học thuật |
| plan/ | Kế hoạch/phân công |
| reports/ | Ghi chú hạ tầng benchmark FE; không phải kết quả study CSV |

<a id="lo-trinh"></a>

## 7. Lộ trình đọc tài liệu

| Thứ tự | Tài liệu | Sau khi đọc cần hiểu |
|---|---|---|
| 1 | README hiện tại | Dự án làm gì và đang ở đâu |
| 2 | [NOTE](NOTE.md) | Câu hỏi nghiên cứu, logic thiết kế |
| 3 | [REPORT](implementation/docs/REPORT.md) | Cách tính điểm và giới hạn |
| 4 | Các chương thuật toán ở mục 4 | Vì sao mỗi phương pháp tạo ứng viên khác nhau |
| 5 | [NOTEBOOK_STUDY](implementation/docs/NOTEBOOK_STUDY.md) | Đối chứng và các bảng sẽ được tạo |
| 6 | [REPRODUCE](REPRODUCE.md) | Cách chuẩn bị và thực thi khi được duyệt |
| 7 | [TALK](TALK.md) | Cách kể lại toàn bộ dự án và trả lời phản biện |

[Mục lục toàn bộ tài liệu](implementation/docs/README.md) có các nhánh chuyên sâu về thuật ngữ, thống kê, độ nhạy và bằng chứng.

<a id="nguon"></a>

## 8. Nguồn và trạng thái kiểm chứng

[SOURCES](implementation/docs/SOURCES.md) tách nguồn học thuật, lựa chọn riêng của nhóm và mã triển khai. Mỗi chương công thức dẫn về phần tương ứng; không quy toàn bộ phương pháp cho một bài báo.

Study đã dừng và kết quả chạy thử đã được dọn sạch. Không có coordinator chạy nền. Notebook giữ ô chạy tắt; chỉ khởi chạy khi được yêu cầu. Đọc tài liệu không cần thực thi Python.

Nhóm: Nguyễn Văn Trung, Hoàng Văn Trường, Nguyễn Minh Hiếu.
