# 📅 Kế hoạch thực hiện đề tài trong 10 tuần

> **Tên đề tài:** Tối ưu hóa vị trí 3D trạm phát sóng UAV trong mạng không dây 5G sử dụng thuật toán bầy cá voi cải tiến (I-WOA)  
> **Nhóm thực hiện:** Nguyễn Văn Trung (Chủ nhóm), Hoàng Văn Trường, Nguyễn Minh Hiếu  
> **Mục tiêu cốt lõi:** Thiết kế, cài đặt và đánh giá đối chứng toàn diện **6 thuật toán** (GA, PSO, WOA, I-WOA đề xuất, H-PSO-GA, H-WOA-PSO) trên **500 kịch bản dữ liệu người dùng**, thực hiện theo chiến lược thực nghiệm 2 giai đoạn (Hội tụ sớm 35 vòng lặp & Tối ưu hóa sâu 80 vòng lặp).

---

## 📊 Bảng kế hoạch tổng quát 10 tuần

| Tuần | Trọng tâm | Nguyễn Văn Trung (Chủ nhóm) | Hoàng Văn Trường | Nguyễn Minh Hiếu | Sản phẩm nghiệm thu cuối tuần |
|:---:|:---|:---|:---|:---|:---|
| **1** | **Xác định bài toán & Cơ sở lý thuyết** | Nghiên cứu tổng quan mạng UAV-BS 5G, phân phối vùng phủ sóng, điều phối phạm vi | Tìm hiểu thuật toán di truyền (GA) và ứng dụng trong tối ưu hóa liên tục | Tìm hiểu giải thuật bầy đàn (PSO, WOA) và các chỉ số đo lường QoS (SNR, Coverage) | Danh mục thuật ngữ, câu hỏi nghiên cứu và sơ đồ ý tưởng bài toán |
| **2** | **Nghiên cứu tài liệu & Khảo sát mô hình** | Nghiên cứu mô hình kênh truyền vô tuyến Al-Hourani (LoS/NLoS) và hàm mục tiêu đa tiêu chí | Tổng hợp các kỹ thuật mã hóa nghiệm GA liên tục (Arithmetic Crossover, Gaussian Mutation) | Nghiên cứu cơ chế săn mồi xoắn ốc của WOA và động lực học vận tốc của PSO | Bảng tổng hợp tài liệu quốc tế IEEE và phương án mô hình toán học |
| **3** | **Thiết kế kiến trúc & Đề xuất I-WOA** | Chủ trì chốt kiến trúc hệ thống module hóa; đề xuất thuật toán cải tiến **I-WOA** (K-Means + OBL + Levy) | Thiết kế pipeline xử lý dữ liệu người dùng và cấu trúc module GA | Đề xuất thiết kế các giải thuật lai (H-PSO-GA, H-WOA-PSO) và hệ thống metric | Bản đặc tả kiến trúc, công thức toán học (`formulas.md`) được duyệt |
| **4** | **Xây dựng module dùng chung & Dữ liệu** | Cài đặt không gian tìm kiếm (`search_space`), nghiệm mã hóa 12D và hàm mục tiêu ($f_1, f_2, f_3$) | Xây dựng bộ sinh và nạp 500 file CSV dữ liệu người dùng (50 – 500 UEs) | Cài đặt mô hình vật lý kênh truyền 5G Al-Hourani (`src/physics/`) và ngưỡng SNR | Pipeline dữ liệu 500 files hoàn chỉnh và module vật lý đạt chuẩn |
| **5** | **Triển khai 3 thuật toán cơ sở** | Cài đặt bầy đàn PSO (cập nhật vận tốc $v$, vị trí $x$, neo biên $V_{\max}$, $P_{\text{best}}, G_{\text{best}}$) | Cài đặt GA (Chromosome, chọn lọc Tournament, Arithmetic Crossover, Gaussian Mutation) | Cài đặt WOA gốc (Whale, hệ số thích nghi $a, A, C$, bao vây, bơi xoắn ốc bọt khí) | 3 thuật toán GA, PSO, WOA chạy độc lập và vượt qua unit test |
| **6** | **Phát triển I-WOA & Các thuật toán lai** | Phát triển thuật toán đề xuất **I-WOA**: tích hợp K-Means khởi tạo, học đối kháng (OBL) và bước nhảy Levy | Phát triển thuật toán lai **H-PSO-GA**: kết hợp cập nhật vận tốc PSO với lai ghép/đột biến GA | Phát triển thuật toán lai **H-WOA-PSO**: kết hợp đường bơi xoắn ốc WOA với gia tốc PSO | Hoàn thành đủ 6 thuật toán tối ưu hóa trong `src/algorithms/` |
| **7** | **Tích hợp hệ thống & Kiểm thử bài toán UAV** | Xây dựng script thực thi đa tiến trình (`run_batch.py`), tích hợp hàm đánh giá UAV đa mục tiêu | Kiểm thử tính hợp lệ của nghiệm đầu ra, ràng buộc độ cao $z \in [50, 300]\text{m}$ và diện tích $1\text{ km}^2$ | Xây dựng công cụ vẽ đồ thị 3D vị trí UAV và nón phát sóng 5G (`uav_3d_placement_demo.png`) | Hệ thống chạy trơn tru cả 6 thuật toán trên kịch bản phân bố UAV 3D |
| **8** | **Thực nghiệm Part 1 (35 vòng lặp — 500 datasets)** | Chủ trì chạy batch run đa tiến trình 3.000 lượt chạy (500 files $\times$ 6 thuật toán); theo dõi tải CPU | Thu thập log dữ liệu thô, kiểm tra tính toàn vẹn và không lỗi của 3.000 kết quả | Xử lý dữ liệu thống kê trung bình Part 1, vẽ bộ 4 biểu đồ hội tụ sớm (`part1_early_convergence_35_iter.png`) | Bộ dữ liệu thô Part 1, bảng xếp hạng và biểu đồ hội tụ sớm hoàn chỉnh |
| **9** | **Thực nghiệm Part 2 (80 vòng lặp) & Đối chiếu** | Thực hiện thí nghiệm tối ưu sâu 80 vòng lặp; phân tích bước nhảy vọt lên Top 1 của I-WOA | Phân tích cơ chế thoát cực trị của I-WOA (Levy Flight) so với sự bão hòa của PSO/WOA | Xuất báo cáo đối chiếu Part 1 vs Part 2 (`DEMO_REPORT.md`) và biểu đồ cột bứt phá (`part1_vs_part2_breakthrough_comparison.png`) | Hoàn tất phân tích thực nghiệm, bảng thông số ảnh, chứng minh I-WOA vượt trội |
| **10** | **Hoàn thiện tài liệu, Báo cáo & Bảo vệ** | Biên soạn kịch bản thuyết trình (`TALK.md`), tổng duyệt toàn bộ tài liệu báo cáo và chuẩn bị demo | Biên soạn bộ tài liệu kỹ thuật chi tiết (`DWGA.md`, `DWH_PSO_GA.md`, rà soát thuật ngữ lý thuyết) | Biên soạn bộ tài liệu kỹ thuật (`DWPSO.md`, `DWWOA.md`, `DWH_WOA_PSO.md`, bảng số liệu) | Toàn bộ tài liệu báo cáo, kịch bản bảo vệ và mã nguồn hoàn thiện 100% |

---

## 📝 Chi tiết nội dung công việc từng tuần

### Tuần 1 — Khởi động & Nghiên cứu lý thuyết nền tảng
- Tìm hiểu bài toán định vị trạm phát sóng bay không người lái (UAV-BS) hỗ trợ phủ sóng di động đô thị.
- Phân tích các thách thức: suy hao khoảng cách, che khuất công trình đô thị (NLOS), vùng chồng lấn gây nhiễu đồng kênh và giới hạn năng lượng pin UAV.
- Tìm hiểu các thuật toán tối ưu hóa thông minh bầy đàn và tiến hóa (Metaheuristics): GA, PSO, WOA.
- Thống nhất môi trường phát triển: Python 3.10+, NumPy, SciPy, Matplotlib, chuẩn kiến trúc module.

### Tuần 2 — Khảo sát tài liệu IEEE & Phân tích yêu cầu kỹ thuật
- Khảo sát các bài báo khoa học chuẩn IEEE (Al-Hourani 2014, Mozaffari 2016, Mirjalili 2016).
- Lựa chọn mô hình suy hao truyền sóng không-mặt đất (Air-to-Ground Path Loss) với xác suất nhìn thẳng tầm mắt (LoS) đặc trưng cho đô thị.
- Xác định không gian tìm kiếm 3D thực tế: diện tích vùng phục vụ $1000\text{ m} \times 1000\text{ m}$ ($1\text{ km}^2$), độ cao an toàn $z \in [50, 300]\text{ m}$.
- Xác định cấu hình trạm 5G Sub-6 ($3.5\text{ GHz}$), công suất phát $30\text{ dBm}$ ($1\text{ W}$), ngưỡng $SNR_{\text{th}} = 18\text{ dB}$.

### Tuần 3 — Thống nhất kiến trúc hệ thống & Đề xuất I-WOA
- Thiết kế luồng xử lý chuẩn mực (Pipeline):
  $$\text{Data Stores} \longrightarrow \text{Preprocessing} \longrightarrow \text{Physics} \longrightarrow \text{Objectives} \longrightarrow \text{Problem} \longrightarrow \text{Algorithms} \longrightarrow \text{Evaluation} \longrightarrow \text{Results}$$
- Xây dựng hàm mục tiêu đa tiêu chí chuẩn hóa: $\text{Fitness} = 0.6 \cdot f_1 - 0.2 \cdot f_2 - 0.2 \cdot f_3$ (Phủ sóng $f_1$, Tiết kiệm năng lượng $f_2$, Giảm nhiễu $f_3$).
- Đề xuất giải pháp cải tiến **I-WOA** khắc phục điểm yếu của WOA gốc:
  1. Phân cụm **K-Means** đưa nghiệm ban đầu bám sát các cụm mật độ người dùng.
  2. Cơ chế **Học đối kháng đa chiều (OBL)** mở rộng không gian tìm kiếm đối xứng, chống lệch góc bản đồ.
  3. Đột biến **Bước nhảy Levy Flight** phân phối đuôi nặng (Mantegna algorithm) tạo các cú nhảy dài ngẫu nhiên giúp thoát khỏi các hố trũng cực trị địa phương.

### Tuần 4 — Xây dựng hạ tầng dữ liệu & Module vật lý 5G
- Tạo lập bộ dữ liệu thực nghiệm quy mô lớn: **500 file CSV kịch bản phân bố người dùng ngẫu nhiên** trong `data/stores/` (gồm 10 mức quy mô từ 50 đến 500 UEs, mỗi mức 50 file độc lập để đảm bảo kiểm định Monte Carlo).
- Triển khai module vật lý truyền sóng trong `src/physics/`: tính khoảng cách Euclid 3D, góc ngẩng $\theta$, xác suất $P_{\text{LoS}}$, suy hao tổng hợp và chỉ số SNR.
- Đóng gói bài toán tối ưu trong `src/problem/uav_placement.py` với vector nghiệm 12 chiều $[x_1, y_1, z_1, \dots, x_4, y_4, z_4]$.

### Tuần 5 — Triển khai 3 thuật toán cơ sở (GA, PSO, WOA)
- **GA:** Xây dựng `chromosome.py`, `selection.py` (Tournament $k=3$), `crossover.py` (Arithmetic Crossover số học tổ hợp lồi), `mutation.py` (Gaussian Mutation) và `replacement.py` (Elitism giữ lại cá thể tốt nhất).
- **PSO:** Xây dựng `particle.py`, `velocity_update.py` (quán tính $w=0.7$, nhận thức $c_1=1.5$, xã hội $c_2=1.5$), `position_update.py`, giới hạn vận tốc $V_{\max} = 0.2 \times (UB - LB)$ và cập nhật $P_{\text{best}}, G_{\text{best}}$.
- **WOA:** Xây dựng `whale.py`, `coefficient_update.py` (suy giảm $a=2 \to 0$, tính $\vec{A}, \vec{C}, l$), `encircling.py` (bao vây), `spiral_update.py` (bơi xoắn ốc bọt khí) và `exploration.py` (thám hiểm theo cá thể ngẫu nhiên).

### Tuần 6 — Triển khai I-WOA & Các thuật toán lai ghép
- Hoàn thiện thuật toán đề xuất **I-WOA**:
  - Tích hợp module phân cụm K-Means (`src/preprocessing/kmeans.py`).
  - Viết module học đối kháng OBL (`src/algorithms/I_WOA/obl.py`).
  - Viết module bước nhảy Levy Flight (`src/algorithms/I_WOA/levy_flight.py`).
- Xây dựng thuật toán lai **Hybrid PSO-GA (`H-PSO-GA`)**: kết hợp tốc độ khai thác của PSO với khả năng duy trì đa dạng di truyền của GA.
- Xây dựng thuật toán lai **Hybrid WOA-PSO (`H-WOA-PSO`)**: kết hợp đường bơi xoắn ốc của WOA với vector gia tốc của PSO.

### Tuần 7 — Tích hợp hệ thống & Kiểm thử bài toán UAV 3D
- Hoàn thiện script tối ưu hóa đa tiến trình `run_batch.py` tận dụng tối đa CPU đa lõi (Multiprocessing Pool) trên hệ điều hành Windows.
- Đảm bảo tính công bằng tuyệt đối: cả 6 thuật toán chạy trên cùng một bộ dữ liệu, cùng kích thước quần thể ($PopSize = 25$), cùng seed ngẫu nhiên ($Seed = 42$) và cùng hàm mục tiêu.
- Xây dựng mô phỏng trực quan không gian 3D đặt trạm UAV (`uav_3d_placement_demo.png`), hiển thị người dùng mặt đất, vị trí 4 UAV trên không và nón phủ sóng 5G.

### Tuần 8 — Thực nghiệm Phần 1: Khảo sát tốc độ hội tụ sớm (35 vòng lặp — 500 datasets)
- Thực thi toàn bộ 500 file CSV trên 6 thuật toán, hoàn thành **3.000 lượt chạy tối ưu hóa Monte Carlo**.
- Ghi nhận và phân tích kết quả:
  - Các thuật toán bầy đàn truyền thống hội tụ rất nhanh ở giai đoạn đầu: **H-WOA-PSO đạt Hạng 1** (Fitness 0.4430), **PSO đạt Hạng 2** (Fitness 0.4426).
  - Thuật toán đề xuất **I-WOA xếp Hạng 5** (Fitness 0.4405) do các cơ chế OBL và Levy Flight đang dành số vòng lặp đầu để mở rộng không gian tìm kiếm (Exploration), chưa co cụm khai thác sâu.
- Xuất dữ liệu thống kê `part1_early_convergence_35_iter.csv` và biểu đồ 4 ô `part1_early_convergence_35_iter.png`.

### Tuần 9 — Thực nghiệm Phần 2: Khảo sát tối ưu sâu (80 vòng lặp) & Phân tích bứt phá
- Thực thi tối ưu hóa sâu 80 vòng lặp trên 10 mức quy mô đại diện (50 đến 500 UEs).
- **Phát hiện bước nhảy vọt mang tính quyết định của I-WOA:**
  - 🥇 **I-WOA chính thức vươn lên dẫn đầu toàn bảng (Hạng 1/6)** với Fitness trung bình đạt **0.4505**.
  - 🥇 **Tỷ lệ can nhiễu $f_3$ giảm xuống đáy kỷ lục: 5.72%** (thấp hơn hẳn so với WOA gốc 7.78% và PSO 8.26%, giảm tới 45% so với H-WOA-PSO).
  - 🥇 **Độ phủ sóng đạt xấp xỉ tuyệt đối: 99.91%**.
  - 🚀 **Tốc độ cải thiện Fitness của I-WOA đạt $+0.0100$** (gấp 3 lần mức tăng $+0.0033$ của PSO do PSO và WOA đã bị sa lầy vào cực trị địa phương).
- Hoàn thiện báo cáo đối chiếu 2 giai đoạn `DEMO_REPORT.md`, biểu đồ so sánh bứt phá `part1_vs_part2_breakthrough_comparison.png` và các bảng thông số ảnh `parameter_and_metrics_table.png`.

### Tuần 10 — Hoàn thiện tài liệu, Báo cáo kỹ thuật & Chuẩn bị bảo vệ
- Soạn thảo kịch bản bảo vệ đồ án và hướng dẫn thuyết trình chi tiết trong [`TALK.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/TALK.md).
- Soạn thảo bộ 6 tài liệu kỹ thuật chuyên sâu giải thích công thức và mã nguồn từng thuật toán trong thư mục [`docs/`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/):
  - [`DWGA.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWGA.md), [`DWPSO.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWPSO.md), [`DWWOA.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWWOA.md).
  - [`DWI_WOA.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWI_WOA.md) (Thuật toán đề xuất).
  - [`DWH_PSO_GA.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWH_PSO_GA.md), [`DWH_WOA_PSO.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWH_WOA_PSO.md).
- Bổ sung bộ câu hỏi phản biện trọng điểm (tại sao chọn khu vực $1\text{ km}^2$, độ tin cậy của 500 file kịch bản, ý nghĩa vật lý của việc giảm 45% nhiễu giao thoa).
- Đóng gói toàn bộ sản phẩm mã nguồn, hình ảnh và báo cáo sẵn sàng cho buổi bảo vệ nghiệm thu.

---

## 📈 Bảng theo dõi tiến độ thực tế (Progress Tracking)

| Tuần | Trạng thái thực tế | Kết quả đạt được & Sản phẩm nghiệm thu | Vấn đề đã xử lý | Người xác nhận |
|:---:|:---:|:---|:---|:---:|
| **1** | ✅ **Hoàn thành** | Hoàn thành tài liệu tổng quan bài toán UAV 3D, mô hình kênh và khảo sát metaheuristics | Làm rõ bài toán tối ưu hóa liên tục 12D | Nguyễn Văn Trung |
| **2** | ✅ **Hoàn thành** | Chốt mô hình toán học kênh truyền Al-Hourani đô thị và tham số vô tuyến 5G NR | Thống nhất chuẩn tần số 3.5 GHz Sub-6 | Hoàng Văn Trường |
| **3** | ✅ **Hoàn thành** | Hoàn thành thiết kế kiến trúc module sạch; đề xuất giải pháp I-WOA (K-Means, OBL, Levy) | Tách bạch tầng vật lý, hàm mục tiêu và giải thuật | Nguyễn Minh Hiếu |
| **4** | ✅ **Hoàn thành** | Sinh toàn bộ 500 file CSV dữ liệu người dùng (50 – 500 UEs); hoàn thành module vật lý & SNR | Đảm bảo tính nhất quán định dạng CSV | Hoàng Văn Trường |
| **5** | ✅ **Hoàn thành** | Triển khai hoàn chỉnh 3 thuật toán cơ sở: GA (Arithmetic/Gaussian), PSO (V-clamping), WOA | Khắc phục lỗi hạt PSO bay vượt biên bản đồ | Nguyễn Văn Trung |
| **6** | ✅ **Hoàn thành** | Triển khai thành công I-WOA đề xuất cùng 2 thuật toán lai H-PSO-GA và H-WOA-PSO | Hoàn thiện công thức Mantegna cho bước nhảy Levy | Nguyễn Văn Trung |
| **7** | ✅ **Hoàn thành** | Tích hợp thành công script chạy đa tiến trình; xuất biểu đồ trực quan hóa không gian 3D | Tối ưu hóa Multiprocessing trên Windows | Nguyễn Minh Hiếu |
| **8** | ✅ **Hoàn thành** | Chạy xong toàn bộ 3.000 lượt mô phỏng Part 1 (35 vòng lặp); xuất dữ liệu và biểu đồ hội tụ sớm | Xử lý triệt để bài toán hiệu năng tải CPU | Hoàng Văn Trường |
| **9** | ✅ **Hoàn thành** | Hoàn thành Part 2 (80 vòng lặp); chứng minh I-WOA vươn lên dẫn đầu toàn bảng (Fitness 0.4505, Nhiễu 5.72%) | Phân tích rõ hiện tượng bão hòa của PSO | Nguyễn Văn Trung |
| **10** | 🚀 **Sẵn sàng báo cáo** | Hoàn tất kịch bản bảo vệ `TALK.md`, bộ tài liệu kỹ thuật `DW*.md`, báo cáo `DEMO_REPORT.md` và bảng thông số ảnh | Sẵn sàng demo thuyết trình cho Thầy/Hội đồng | Cả nhóm |
