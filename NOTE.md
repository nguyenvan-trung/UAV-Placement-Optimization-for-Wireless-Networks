# Tối Ưu Hóa Vị Trí UAV 3D Trong Mạng Không Dây 5G/6G Bằng Thuật Toán Metaheuristic Cải Tiến (I-WOA)

## 📌 1. Giới Thiệu Đề Tài & Tính Mới

Nghiên cứu này giải quyết bài toán NP-Hard về **tối ưu hóa vị trí không gian 3D** $(x, y, z)$ của các trạm phát sóng UAV (Unmanned Aerial Vehicle Base Stations) nhằm khôi phục và tăng cường vùng phủ sóng cho mạng không dây 5G/6G.

### Đóng Góp Khoa Học Cốt Lõi (Novelty):

1. **Mô hình hóa 3D thực tế:** Tích hợp mô hình kênh truyền Air-to-Ground (A2G) ngẫu nhiên phụ thuộc góc ngẩng $\theta$ và địa hình đô thị nén.
2. **Khởi tạo K-Means Smart Initialization:** Gom cụm mật độ người dùng mặt đất để định vị vị trí khởi tạo tối ưu ban đầu cho các UAV.
3. **Giải thuật I-WOA (Improved WOA):** Kết hợp **Học đối kháng (Opposition-Based Learning - OBL)** tăng tốc hội tụ và **Bước nhảy Levy Flight** giúp quần thể bứt phá khỏi các cực trị địa phương (Local Optima).
4. **Tối ưu hóa đa mục tiêu:** Cân bằng đồng thời giữa **Độ phủ sóng ($f_1$)**, **Tiết kiệm năng lượng ($f_2$)** và **Nhiễu giao thoa chồng lấp ($f_3$)**.

---

## 📐 2. Mô Hình Toán Học Đầy Đủ (Mathematical Formulation)

### 2.1. Mô Hình Kênh Truyền Air-to-Ground (A2G)

- **Khoảng cách hình học 3D:**
  $$d_{ij} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2 + z_i^2}$$

- **Góc ngẩng (Elevation Angle):**
  $$\theta_{ij} = \arcsin\left(\frac{z_i}{d_{ij}}\right) \quad (\text{đơn vị: rad})$$

- **Xác suất nhìn thẳng (Probability of Line-of-Sight - LoS):**
  $$P_{\text{LoS}}(\theta_{ij}) = \frac{1}{1 + a \cdot \exp\left(-b(\theta_{ij} - a)\right)}$$

  _(với $a, b$ là các hằng số môi trường đô thị - Urban Dense: $a = 9.61, b = 0.16$)_.

- **Suy hao đường truyền (Pathloss):**
  $$PL_{\text{LoS}}(d_{ij}) = 20 \log_{10}\left(\frac{4\pi f d_{ij}}{c}\right) + \eta_{\text{LoS}}$$
  $$PL_{\text{NLoS}}(d_{ij}) = 20 \log_{10}\left(\frac{4\pi f d_{ij}}{c}\right) + \eta_{\text{NLoS}}$$
  $$PL_{ij} = P_{\text{LoS}}(\theta_{ij}) \cdot PL_{\text{LoS}}(d_{ij}) + \left(1 - P_{\text{LoS}}(\theta_{ij})\right) \cdot PL_{\text{NLoS}}(d_{ij})$$

- **Tỷ số Tín hiệu trên Nhiễu (SNR):**
  $$SNR_{ij} = P_{\text{tx}} - PL_{ij} - N_0$$
  _(với $P_{\text{tx}}$ là công suất phát, $N_0$ là công suất tạp âm nền)\_.

### 2.2. Chi Tiết Các Hàm Mục Tiêu (Fitness Objectives)

Hàm Fitness tổng hợp (Weighted Sum Approach):
$$\text{Fitness} = w_1 \cdot f_1 - w_2 \cdot f_2 - w_3 \cdot f_3 \quad (\text{với } w_1 + w_2 + w_3 = 1)$$

1. **Hàm Phủ Sóng ($f_1$ - Maximize Coverage Rate):**
   $$f_1 = \frac{1}{M} \sum_{j=1}^{M} \mathbb{I}\left( \max_{i=1 \dots N} (SNR_{ij}) \ge SNR_{\text{th}} \right)$$

   _(người dùng $j$ được phủ sóng nếu có ít nhất 1 UAV cung cấp $SNR \ge SNR_{\text{th}}$)\_.

2. **Hàm Năng Lượng ($f_2$ - Minimize Energy Consumption):**
   $$f_2 = \sum_{i=1}^{N} \left( P_{\text{hover}}(z_i) + P_{\text{transmit}, i} \right)$$

   _(trong đó công suất nâng $P_{\text{hover}}(z*i)$ tăng dần theo độ cao $z_i$)*.

3. **Hàm Nhiễu Chồng Lấp ($f_3$ - Minimize Interference):**
   $$f_3 = \sum_{i=1}^{N} \sum_{k=i+1}^{N} \text{Area\_Overlap}(U_i, U_k)$$

   _(diện tích giao nhau của vùng phủ mặt đất giữa UAV $i$ và UAV $k$)_.

---

## 🧬 3. Chi Tiết Giải Thuật I-WOA (Algorithms & Improvements)

### 3.1. Tiền xử lý: K-Means Clustering Init

Chạy thuật toán K-Means phân cụm $M$ người dùng mặt đất thành $N$ cụm ($N$ = số UAV)[cite: 1]. Lấy tọa độ tâm 2D $(x_c, y_c)$ của $N$ cụm để tạo vị trí gợi ý ban đầu cho các UAV[cite: 1].

### 3.2. Cải tiến 1: Học Đối Kháng (Opposition-Based Learning - OBL)

Với mỗi vị trí giải pháp $X = (x, y, z)$ trong không gian $[L, U]$, sinh vị trí đối kháng:
$$X^{\text{op}} = L + U - X$$
[cite: 1]
So sánh giá trị Fitness giữa $X$ và $X^{\text{op}}$, giữ lại $N$ cá thể tốt nhất giúp tăng tốc độ hội tụ ban đầu[cite: 1].

### 3.3. Cải tiến 2: Bước Nhảy Levy Flight Mutation

Khi thuật toán bị kẹt tại cực trị địa phương, vị trí được cập nhật theo phân phối Levy với các bước nhảy ngẫu nhiên dài:
$$X_i(t+1) = X_i(t) + \alpha \oplus \text{Levy}(\beta)$$
[cite: 1]
$$\text{Levy}(s) \sim \vert{}s\vert{}^{-1-\beta}, \quad 0 < \beta \le 2$$
[cite: 1]

---

## 📊 4. Chi Tiết Bộ Dữ Liệu Thực Nghiệm (Dataset Specifications)

Dữ liệu được sinh bằng mô phỏng số (Synthetic Dataset) và đánh giá qua **30 lượt Monte Carlo Runs** độc lập[cite: 1]:

| Thông số (Parameter)                   | Kịch bản 1 (Uniform)                        | Kịch bản 2 (Dense Urban Cluster)                   |
| :------------------------------------- | :------------------------------------------ | :------------------------------------------------- |
| **Kích thước không gian**              | $1000\text{m} \times 1000\text{m}$[cite: 1] | $1000\text{m} \times 1000\text{m}$[cite: 1]        |
| **Số người dùng mặt đất ($M$)**        | 200, 300, 500 UEs[cite: 1]                  | 200, 300, 500 UEs (chia 3-5 cụm Gaussian)[cite: 1] |
| **Số lượng UAV ($N$)**                 | 4 đến 10 UAVs[cite: 1]                      | 4 đến 10 UAVs[cite: 1]                             |
| **Độ cao UAV ($z_{\min} - z_{\max}$)** | $50\text{m} - 200\text{m}$[cite: 1]         | $50\text{m} - 200\text{m}$[cite: 1]                |
| **Tần số sóng 5G**                     | $3.5\text{ GHz}$ (Sub-6)[cite: 1]           | $3.5\text{ GHz}$ (Sub-6)[cite: 1]                  |
| **Ngưỡng kết nối $SNR_{\text{th}}$**   | $5\text{ dB}$                               | $5\text{ dB}$                                      |
| **Số lượt chạy Monte Carlo**           | 30 runs[cite: 1]                            | 30 runs[cite: 1]                                   |

---

## 🔄 5. Luồng Chạy Thuật Toán (Processing Pipeline)

````text
[Đầu Vào: Datasets UEs & Config Params]
               │
               ▼
[Bước 1: Phân Cụm Ban Đầu (K-Means)] ──> Phân cụm M người dùng thành N cụm & trích xuất tâm (x_c, y_c)
               │
               ▼
[Bước 2: Khởi Tạo Quần Thể (OBL)]    ──> Tạo quần thể gốc + quần thể đối kháng (X_op = a + b - X)
               │
               ▼
┌───> [Bước 3: Vòng Lặp Chính I-WOA (Main Loop)]
│              │
│              ├──> Tính d_ij 3D, góc ngẩng θ_ij, xác suất LoS/NLoS & Pathloss
│              ├──> Tính SNR_ij cho từng UE và đếm số UE đạt chuẩn SNR_th
│              ├──> Đánh giá Fitness = w1*f1 - w2*f2 - w3*f3
│              ├──> Cập nhật vị trí xoắn ốc (Bubble-net Mechanism)
│              └──> Áp dụng Bước nhảy Levy (Levy Flight) đột biến thoát cực trị
│              │
└─── Lặp t < Max_Iter? (Default: 200 iter)
               │
               ▼
[Bước 4: Xuất Nghiệm 3D & Kiểm Định Thống Kê] ──> Chạy 30 Monte Carlo Runs & Kiểm định Wilcoxon Rank-Sum
```[cite: 1]

---

## 🛠️ 6. Cấu Trúc Thư Mục Dự Án (Project Structure)

`NOTE.md` là tài liệu ý tưởng và mô hình nghiên cứu. Cách chạy thực tế, tham
số code hiện tại và trách nhiệm của từng thư mục được duy trì trong
[README.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/README.md>)
và [implementation/README.md](<D:/Personal Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/README.md>).
Các giá trị trong phần ý tưởng là mục tiêu nghiên cứu; khi chạy chương trình,
ưu tiên các giá trị trong `implementation/src/constants/`.

```text
├── config/
│   └── params.json            # Tham số hệ thống 5G, kênh truyền, trọng số f1, f2, f3[cite: 1]
├── data/
│   ├── raw/                   # Tọa độ UEs ngẫu nhiên & phân cụm (CSV/MAT)[cite: 1]
│   ├── stores/                # Các bộ dữ liệu CSV đã xử lý[cite: 1]
│   └── views/                 # Ảnh quan sát của từng bộ dữ liệu
├── implementation/
│   ├── scripts/                # Sinh dữ liệu, chạy optimizer, chạy thí nghiệm
│   ├── src/
│   │   ├── constants/          # Tham số và đường dẫn code
│   │   ├── data_generation/    # Sinh dataset mô phỏng
│   │   ├── input/              # Đọc và kiểm tra CSV
│   │   ├── preprocessing/      # K-Means và khởi tạo UAV
│   │   ├── models/             # User, UAV và nghiệm
│   │   ├── physics/            # d_ij, θ_ij, LoS, Pathloss, SNR
│   │   ├── objectives/         # f1, f2, f3 và Fitness
│   │   ├── problem/            # Biên và ràng buộc
│   │   ├── algorithms/         # GA, PSO, WOA, I-WOA
│   │   ├── evaluation/         # Monte Carlo và kiểm định thống kê
│   │   └── visualization/      # Bảng và biểu đồ
│   ├── docs/                   # Công thức và ranh giới triển khai
│   ├── notebooks/              # Phân tích kết quả, không chạy pipeline chính
│   ├── results/                # Bảng, biểu đồ, nghiệm và log
│   ├── datasets/               # Chỉ tài liệu quy ước dataset
│   └── requirements.txt        # Thư viện phụ thuộc


````

---

## 📈 7. Chỉ Số KPIs Kỳ Vọng & Kiểm Định Khoa Học

- **Độ phủ sóng ($f_1$):** Đạt **> 90%** (Tăng 5–8% so với WOA gốc)[cite: 1].
- **Tiết kiệm năng lượng ($f_2$):** Giảm **15%** tổng công suất tiêu thụ toàn hệ thống UAV[cite: 1].
- **Tốc độ hội tụ:** Nhanh hơn **25%** so với các thuật toán baseline nhờ K-Means + OBL[cite: 1].
- **Đánh giá thống kê:** Đạt ý nghĩa thống kê $p$-value $< 0.05$ trong phép kiểm định **Wilcoxon Rank-Sum Test** qua 30 lần chạy độc lập[cite: 1].

---

## 🧩 8. Phân Tích Logic Thuật Toán & Vai Trò Trong Nghiên Cứu

### 8.1. Tại Sao Lại Lựa Chọn Các Thuật Toán Này?

Bài toán tối ưu vị trí 3D cho UAV trong mạng không dây là bài toán **NP-Hard với không gian tìm kiếm liên tục và phi tuyến**[cite: 1]. Các phương pháp duyệt cạn hay quy hoạch toán học truyền thống không thể giải được trong thời gian thực. Vì vậy, nhóm giải thuật **Metaheuristic (Giải thuật siêu kinh nghiệm)** là lựa chọn bắt buộc[cite: 1].

Mỗi thuật toán trong đề tài được đưa vào với vai trò và lý do kỹ thuật cụ thể:

- **K-Means Clustering (Tiền xử lý):**
  - _Lý do:_ Không gian tìm kiếm 3D rất rộng ($1000\text{m} \times 1000\text{m}$)[cite: 1]. Nếu thả ngẫu nhiên các UAV, thuật toán sẽ tốn 30-50% số vòng lặp đầu tiên chỉ để di chuyển UAV từ vùng "không có dân" vào vùng "có dân". K-Means dựa vào mật độ tọa độ người dùng để đặt UAV ngay vào các "tâm điểm vùng cầu", tạo một **vị trí khởi tạo chất lượng cao (Good Initial Guess)**.
- **Whale Optimization Algorithm - WOA (Thuật toán nền tảng):**
  - _Lý do:_ WOA mô phỏng cơ chế săn mồi bằng lưới bọt xoắn ốc của cá kình[cite: 1]. WOA có ưu điểm vượt trội hơn PSO và GA ở khả năng **cân bằng giữa thám hiểm (Exploration) và khai thác (Exploitation)** trong không gian liên tục với số lượng tham số cần chỉnh ít hơn hẳn[cite: 1].
- **Opposition-Based Learning - OBL (Cải tiến 1):**
  - _Lý do:_ Khắc phục điểm yếu của khởi tạo ngẫu nhiên. OBL sinh các nghiệm đối lập song song ($X^{\text{op}} = a + b - X$)[cite: 1], giúp thuật toán "quét" đối ứng toàn bộ không gian 3D, tránh việc tất cả cá thể bị dồn về một góc bản đồ ở thế hệ ban đầu[cite: 1].
- **Levy Flight Mutation (Cải tiến 2):**
  - _Lý do:_ Khắc phục hiện tượng **Hội tụ sớm / Kẹt cực trị địa phương (Local Optima)**[cite: 1] - điểm yếu cố hữu của WOA gốc[cite: 1]. Phân phối bước nhảy Levy có đặc trưng: các bước ngắn lăn tăn xen kẽ những bước nhảy rất dài ngột ngạt[cite: 1]. Cú nhảy dài này giúp "hất" cá thể bứt phá ra khỏi khu vực sa lầy để tìm vùng không gian mới[cite: 1].

### 8.2. Phân Định Thuật Toán Trọng Tâm & Thuật Toán Đối Chứng (Baselines)

| Loại Thuật Toán                                 | Tên Thuật Toán                                     | Vai Trò & Mục Đích Trong Nghiên Cứu                                                                                                                                                                                              |
| :---------------------------------------------- | :------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **THUẬT TOÁN TRỌNG TÂM**<br>_(Proposed Method)_ | **K-Means + I-WOA**<br>_(WOA + OBL + Levy Flight)_ | • Đóng góp khoa học cốt lõi của đề tài[cite: 1, 2].<br>• Bộ não tính toán tọa độ 3D tối ưu $(x^*, y^*, z^*)$ cho dàn UAV[cite: 1].<br>• Kỳ vọng phủ sóng $>90\%$, tiết kiệm $15\%$ năng lượng, hội tụ nhanh hơn $25\%$[cite: 1]. |
| **THUẬT TOÁN ĐỐI CHỨNG 1**<br>_(Baseline 1)_    | **WOA Gốc (Original WOA)**                         | • Làm mốc so sánh trực tiếp để chứng minh hiệu quả vượt trội của 2 cơ chế cải tiến OBL & Levy Flight[cite: 1, 2].                                                                                                                |
| **THUẬT TOÁN ĐỐI CHỨNG 2**<br>_(Baseline 2)_    | **PSO Gốc (Particle Swarm)**                       | • Đại diện nhóm thuật toán Trí tuệ bầy đàn (Swarm Intelligence) kinh điển[cite: 1, 2].                                                                                                                                           |
| **THUẬT TOÁN ĐỐI CHỨNG 3**<br>_(Baseline 3)_    | **GA Gốc (Genetic Algorithm)**                     | • Đại diện nhóm thuật toán Tiến hóa (Evolutionary Algorithms) kinh điển[cite: 1, 2].                                                                                                                                             |

### 8.3. Sơ Đồ Phân Cấp Thuật Toán (Hierarchy Diagram)

```text
                             [BÀI TOÁN TỐI ƯU VỊ TRÍ UAV 3D]
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
        [Thuật Toán Trọng Tâm]                         [Bộ Thuật Toán Đối Chứng]
    (Proposed: K-Means + I-WOA)                        (Baseline Algorithms)
                    │                                             │
      ┌─────────────┴─────────────┐                ┌──────────────┼──────────────┐
      ▼                           ▼                ▼              ▼              ▼
[Pre-processing]        [Core Optimization]    [WOA Gốc]      [PSO Gốc]      [GA Gốc]
(K-Means Cluster)      (WOA + OBL + Levy)     (Cơ bản)       (Bầy đàn)      (Di truyền)
```
