# 🛸 UAV Placement Optimization for 5G Wireless Networks

> **Đề tài:** Tối ưu hóa vị trí 3D trạm phát sóng UAV trong mạng không dây 5G sử dụng thuật toán bầy cá voi cải tiến (I-WOA)  
> **Nhóm thực hiện:** Nguyễn Văn Trung (Chủ nhóm), Hoàng Văn Trường, Nguyễn Minh Hiếu  
> **Tài liệu thuyết trình:** [TALK.md](TALK.md) | **Báo cáo thực nghiệm 2 giai đoạn:** [DEMO_REPORT.md](implementation/results/DEMO_REPORT.md)

---

## 1. 📂 Bản đồ cấu trúc dự án

```text
.
├── data/                         # Dữ liệu độc lập với mã nguồn
│   ├── stores/                   # 500 file CSV dữ liệu người dùng (50 - 500 UEs)
│   └── views/                    # Hình ảnh trực quan hóa không gian của từng kịch bản
├── documents/                    # Tổng hợp tài liệu tham khảo học thuật chuẩn IEEE
│   └── README.md                 # Danh mục bài báo về Al-Hourani, I-WOA, OBL, Levy, PSO, GA
├── plan/                         # Kế hoạch tiến độ 10 tuần và phân công nhóm
│   ├── weekly_plan.md            # Kế hoạch 10 tuần chi tiết (Hoàn thành 100%)
│   ├── team_assignment.md        # Phân công vai trò từng thành viên và review chéo
│   └── team_weekly_progress.xlsx # Bảng Excel theo dõi tiến độ chi tiết
├── implementation/               # Toàn bộ mã nguồn mô phỏng và kết quả
│   ├── docs/                     # Tài liệu kỹ thuật chuyên sâu từng giải thuật
│   │   ├── formulas.md           # Kiến trúc phân tầng và ánh xạ công thức
│   │   ├── DWGA.md               # Giải thích chi tiết & công thức GA
│   │   ├── DWPSO.md              # Giải thích chi tiết & công thức PSO
│   │   ├── DWWOA.md              # Giải thích chi tiết & công thức WOA
│   │   ├── DWI_WOA.md            # Giải thích chi tiết & công thức I-WOA (Đề xuất)
│   │   ├── DWH_PSO_GA.md         # Giải thích chi tiết thuật toán lai H-PSO-GA
│   │   └── DWH_WOA_PSO.md        # Giải thích chi tiết thuật toán lai H-WOA-PSO
│   ├── results/                  # Kết quả thực nghiệm và bảng biểu đồ đối chứng
│   │   ├── part1_35_iterations/ # Giai đoạn 1: Hội tụ sớm (35 vòng lặp, 500 datasets)
│   │   ├── part2_80_iterations/ # Giai đoạn 2: Tối ưu sâu (80 vòng lặp, I-WOA Top 1)
│   │   ├── DEMO_REPORT.md        # Báo cáo so sánh đối chiếu bước nhảy vọt
│   │   ├── system_parameters_table.png # Ảnh bảng thông số mô phỏng chuẩn
│   │   ├── part1_vs_part2_breakthrough_comparison.png # Biểu đồ cột bứt phá
│   │   └── uav_3d_placement_demo.png # Hình ảnh mô phỏng không gian 3D đặt 4 UAV
│   ├── scripts/                  # Các tập lệnh thực thi dòng lệnh
│   │   ├── run_batch.py          # Script chạy hàng loạt đa tiến trình (Part 1 & Part 2)
│   │   ├── run_optimizer.py      # Script chạy tối ưu hóa đơn lẻ cho 1 kịch bản
│   │   └── generate_dataset.py   # Script sinh 500 kịch bản người dùng
│   └── src/                      # Cấu trúc mã nguồn module hóa sạch (Clean Architecture)
│       ├── algorithms/           # Cài đặt 6 thuật toán (GA, PSO, WOA, I-WOA, Hybrid)
│       ├── physics/              # Kênh truyền vô tuyến Al-Hourani Sub-6 5G (LoS/NLoS, SNR)
│       ├── objectives/           # Hàm mục tiêu đa tiêu chí (Phủ sóng f1, Năng lượng f2, Nhiễu f3)
│       ├── preprocessing/        # Phân cụm K-Means khởi tạo thông minh
│       └── problem/              # Đóng gói bài toán không gian tìm kiếm 12D
├── NOTE.md                       # Ghi chú nghiên cứu lý thuyết chuyên sâu
└── TALK.md                       # Kịch bản bảo vệ đồ án và hướng dẫn vấn đáp
```

---

## 2. ⚙️ Tham số thiết lập mô phỏng chuẩn 5G

Toàn bộ tham số được quản lý tập trung trong `implementation/src/constants/network.py` và `experiment.py`:

| Nhóm thông số | Tên thông số | Ký hiệu | Giá trị thiết lập | Đơn vị / Ý nghĩa |
| :--- | :--- | :---: | :---: | :--- |
| **Không gian mạng** | Kích thước khu vực | $W \times H$ | $1000 \times 1000$ | $\text{m}^2$ (Diện tích $1\text{ km}^2$) |
| | Độ cao bay UAV | $[z_{\min}, z_{\max}]$ | $[50, 300]$ | mét (Độ cao bay hành trình an toàn) |
| | Số lượng UAV | $N$ | **4** | trạm phát sóng bay |
| | Số lượng người dùng | $M$ | **50 đến 500** | người dùng (10 mức quy mô) |
| **Vật lý vô tuyến (5G)** | Tần số sóng mang | $f_c$ | **3.5** | $\text{GHz}$ (Dải tần Sub-6 chuẩn 5G) |
| | Công suất phát UAV | $P_{\text{tx}}$ | **30** | $\text{dBm}$ (Tương đương 1.0 W) |
| | Tạp âm nền | $N_0$ | **-104** | $\text{dBm}$ |
| | Ngưỡng kết nối khả dụng | $SNR_{\text{th}}$ | **18.0** | $\text{dB}$ (Chuẩn đảm bảo QoS 5G) |
| | Tham số đô thị (Al-Hourani)| $a, b$ | $9.61,\; 0.16$ | Môi trường truyền dẫn đô thị dày đặc |
| | Suy hao cộng thêm | $\eta_{\text{LoS}}, \eta_{\text{NLoS}}$ | $1.0,\; 20.0$ | $\text{dB}$ |
| **Hàm mục tiêu đa tiêu chí** | Trọng số Phủ sóng ($f_1$) | $w_1$ | **0.6** | Càng cao càng tốt |
| | Trọng số Năng lượng ($f_2$) | $w_2$ | **0.2** | Càng thấp càng tốt |
| | Trọng số Can nhiễu ($f_3$) | $w_3$ | **0.2** | Càng thấp càng tốt |

---

## 3. 🚀 Cài đặt môi trường & Chạy thử nghiệm

### 3.1. Kích hoạt môi trường ảo Python
Yêu cầu Python 3.10 trở lên trên Windows PowerShell:

```powershell
# Kích hoạt venv có sẵn
.\.venv\Scripts\Activate.ps1

# Hoặc cài đặt thư viện
pip install -r implementation\requirements.txt
```

### 3.2. Chạy tối ưu hóa đơn lẻ (1 kịch bản CSV)
```powershell
python implementation\scripts\run_optimizer.py --algorithm all --seed 42 --dataset data\stores\001_UAV_3D_50_users_connect.csv
```
*(Tham số `--algorithm` hỗ trợ: `GA`, `PSO`, `WOA`, `I_WOA`, `H_PSO_GA`, `H_WOA_PSO`, hoặc `all`)*.

### 3.3. Chạy thực nghiệm 2 giai đoạn (Toàn bộ 500 datasets & Đối chiếu Part 1 vs Part 2)
Script `run_batch.py` tự động kích hoạt chế độ đa tiến trình (Multiprocessing Pool) trên toàn bộ các lõi CPU:

```powershell
# Chạy cả 2 phần thực nghiệm và tự động xuất biểu đồ, bảng báo cáo
python implementation\scripts\run_batch.py --phase all
```

---

## 4. 🏆 Kết quả thực nghiệm đột phá của I-WOA

| Tiêu chí đánh giá | Part 1 (35 vòng lặp — 500 datasets) | Part 2 (80 vòng lặp — 10 mức quy mô) | Đánh giá bứt phá của I-WOA |
| :--- | :---: | :---: | :--- |
| **Xếp hạng tổng thể I-WOA** | Hạng 5 / 6 | **Hạng 1 / 6 🏆** | **Vươn lên dẫn đầu toàn bảng** |
| **Fitness trung bình** | 0.4405 | **0.4505 🚀** | **Tăng +0.0100 (Gấp 3 lần mức tăng của PSO)** |
| **Tỷ lệ Nhiễu giao thoa ($f_3$)** | 9.04% | **5.72% 🎯** | **Giảm tới 45% lượng nhiễu so với các giải thuật lai** |
| **Tỷ lệ Phủ sóng ($f_1$)** | 99.57% | **99.91%** | Phủ sóng gần như hoàn hảo tuyệt đối |

Chi tiết số liệu kiểm chứng và kịch bản thuyết trình xem tại:
- Báo cáo đối chiếu: [DEMO_REPORT.md](implementation/results/DEMO_REPORT.md)
- Kịch bản bảo vệ đồ án: [TALK.md](TALK.md)
