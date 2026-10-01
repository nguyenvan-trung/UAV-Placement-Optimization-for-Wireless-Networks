# 👥 Dự kiến và phân công nhiệm vụ nhóm

> **Đề tài:** Tối ưu hóa vị trí 3D trạm phát sóng UAV trong mạng không dây 5G sử dụng thuật toán bầy cá voi cải tiến (I-WOA)  
> **Nhóm thực hiện:** 3 thành viên

---

## 1. Nguyễn Văn Trung — Chủ nhóm

### Phụ trách chính:
- **Quản lý & Điều phối tổng thể:** Lên kế hoạch 10 tuần, kiểm soát tiến độ, tích hợp toàn bộ các module trong hệ thống và chuẩn bị demo.
- **Kiến trúc hệ thống:** Thiết kế cấu trúc phân tầng sạch (`input/` $\to$ `preprocessing/` $\to$ `physics/` $\to$ `objectives/` $\to$ `problem/` $\to$ `algorithms/` $\to$ `results/`).
- **Thuật toán đề xuất cốt lõi (I-WOA):** Chủ trì nghiên cứu và cài đặt thuật toán **Improved Whale Optimization Algorithm (I-WOA)** tích hợp phân cụm K-Means, học đối kháng (OBL) và bước nhảy Levy Flight.
- **Hạ tầng thực thi:** Xây dựng script batch run đa tiến trình (`run_batch.py`), giám sát quá trình chạy 3.000 lượt mô phỏng trên 500 datasets.
- **Thực nghiệm Part 2 & Phân tích:** Phân tích thực nghiệm chuyên sâu 80 vòng lặp, chứng minh bước nhảy vọt Top 1 của I-WOA và viết báo cáo đối chiếu [`DEMO_REPORT.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/results/DEMO_REPORT.md).
- **Thuyết trình:** Soạn thảo kịch bản bảo vệ [`TALK.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/TALK.md) và tài liệu kỹ thuật [`DWI_WOA.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWI_WOA.md).

---

## 2. Hoàng Văn Trường — Thành viên

### Phụ trách chính:
- **Thuật toán Di truyền (GA):** Nghiên cứu lý thuyết GA liên tục, cài đặt chọn lọc Tournament, lai ghép số học (Arithmetic Crossover), đột biến Gaussian và chiến lược Elitism.
- **Thuật toán lai Hybrid PSO-GA (H-PSO-GA):** Kết hợp động lực học hạt PSO với các toán tử di truyền GA để duy trì đa dạng quần thể và giải cứu hạt khỏi bẫy cực trị.
- **Hạ tầng dữ liệu:** Xây dựng quy trình quản lý và kiểm tra tính toàn vẹn của **500 file CSV dữ liệu người dùng** (từ 50 đến 500 UEs) trong `data/stores/`.
- **Tài liệu kỹ thuật:** Biên soạn tài liệu chi tiết [`DWGA.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWGA.md), [`DWH_PSO_GA.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWH_PSO_GA.md), rà soát cơ sở lý thuyết toán học và trích dẫn chuẩn IEEE.

---

## 3. Nguyễn Minh Hiếu — Thành viên

### Phụ trách chính:
- **Thuật toán bầy đàn (PSO & WOA gốc):** Cài đặt PSO chuẩn (vận tốc, quán tính, $V_{\max}$) và WOA gốc (bao vây, bơi xoắn ốc bọt khí, thám hiểm toàn cục).
- **Thuật toán lai Hybrid WOA-PSO (H-WOA-PSO):** Kết hợp đường bơi xoắn ốc của WOA với vector gia tốc của PSO, phân tích vì sao giải thuật này đạt Quán quân ở Part 1 (35 vòng lặp).
- **Trực quan hóa & Đồ họa:** Phát triển các công cụ vẽ biểu đồ 2D/3D (`uav_3d_placement_demo.png`), biểu đồ cột bứt phá (`part1_vs_part2_breakthrough_comparison.png`), các đồ thị hội tụ và bảng thông số ảnh (`parameter_and_metrics_table.png`).
- **Tài liệu kỹ thuật:** Biên soạn tài liệu chi tiết [`DWPSO.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWPSO.md), [`DWWOA.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWWOA.md), [`DWH_WOA_PSO.md`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/docs/DWH_WOA_PSO.md).

---

## 4. Công việc phối hợp chung của cả nhóm

- Cùng thống nhất mô hình kênh truyền vô tuyến 5G Al-Hourani và hàm mục tiêu đa tiêu chí chuẩn hóa ($\text{Fitness} = 0.6 f_1 - 0.2 f_2 - 0.2 f_3$).
- Review chéo mã nguồn đảm bảo tuân thủ nghiêm ngặt các nguyên tắc Clean Code và tính công bằng trong thực nghiệm (cùng Seed, cùng kích thước quần thể, cùng ngân sách vòng lặp).
- Phối hợp tổng hợp số liệu thực nghiệm giữa Part 1 (Hội tụ sớm) và Part 2 (Tối ưu sâu).
- Cùng tham gia tập dượt thuyết trình dựa trên kịch bản `TALK.md` và giải đáp bộ câu hỏi phản biện của hội đồng.

---

## 5. Quy tắc phân công & Review chéo

| Hạng mục chuyên môn | Người phụ trách chính | Người review / Kiểm tra độc lập | Sản phẩm nghiệm thu |
| :--- | :--- | :--- | :--- |
| **Kiến trúc, I-WOA, Báo cáo đối chiếu** | Nguyễn Văn Trung | Hoàng Văn Trường | Module `src/algorithms/I_WOA/`, `DEMO_REPORT.md` |
| **Dữ liệu 500 files, GA, H-PSO-GA** | Hoàng Văn Trường | Nguyễn Minh Hiếu | Module `src/algorithms/GA/`, `data/stores/*.csv` |
| **PSO, WOA, H-WOA-PSO, Visualization** | Nguyễn Minh Hiếu | Nguyễn Văn Trung | Module `src/algorithms/PSO/`, `WOA/`, Biểu đồ PNG |
