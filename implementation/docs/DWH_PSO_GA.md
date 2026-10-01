# 🧬🦅 DWH_PSO_GA: TÀI LIỆU KỸ THUẬT & CÔNG THỨC THUẬT TOÁN LAI H-PSO-GA
> **Mục đích:** Hướng dẫn chi tiết công thức toán học, cơ chế lai ghép và kịch bản trả lời phản biện dành cho thuật toán lai **Hybrid PSO-GA (H-PSO-GA)** trong bài toán tối ưu hóa vị trí 3D trạm phát sóng UAV.

---

## 1. 💡 Ý TƯỞNG CỐT LÕI & TRIẾT LÝ LAI GHÉP
- **Vấn đề đặt ra:**
  - **PSO thuần túy:** Hội tụ siêu nhanh ở những vòng lặp đầu nhưng hay bị "đóng băng" do mất tính đa dạng quần thể, dễ kẹt ở cực trị địa phương.
  - **GA thuần túy:** Duy trì đa dạng rất tốt nhờ đột biến nhưng tốc độ hội tụ lại chậm do không có vector định hướng gia tốc.
- **Triết lý lai ghép H-PSO-GA:** Kết hợp **"Gia tốc bầy đàn của PSO"** với **"Đa dạng di truyền của GA"**:
  1. Cho bầy hạt chuyển động theo phương trình vận tốc PSO hướng về $P_{\text{best}}$ và $G_{\text{best}}$ để khai thác nhanh.
  2. Đưa các hạt qua toán tử **Lai ghép số học (Arithmetic Crossover)** và **Đột biến Gaussian (Gaussian Mutation)** của GA để tái cấu trúc không gian nghiệm, bơm thêm tính ngẫu nhiên nhằm kéo bầy hạt thoát khỏi bẫy cực trị.

---

## 2. 🎯 QUY TRÌNH LAI GHÉP TỪNG THẾ HỆ (PIPELINE)

Tại mỗi vòng lặp $t$:

```text
 ┌────────────────────────────────────────────────────────┐
 │ 1. CẬP NHẬT VẬN TỐC & VỊ TRÍ THEO PSO                  │
 │    v(t+1) = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x) │
 │    x(t+1) = x(t) + v(t+1)                              │
 └──────────────────────────┬─────────────────────────────┘
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 2. TOÁN TỬ LAI GHÉP DI TRUYỀN (ARITHMETIC CROSSOVER)    │
 │    Ghép cặp ngẫu nhiên các hạt (Xác suất Pc = 0.8)     │
 │    Child = alpha * Parent1 + (1 - alpha) * Parent2     │
 └──────────────────────────┬─────────────────────────────┘
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 3. TOÁN TỬ ĐỘT BIẾN GAUSSIAN (GAUSSIAN MUTATION)       │
 │    Đột biến gene theo xác suất Pm = 0.15               │
 │    x_j' = x_j + Normal(0, sigma * Range)               │
 └──────────────────────────┬─────────────────────────────┘
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 4. ĐÁNH GIÁ LẠI & CẬP NHẬT P_best, G_best              │
 └────────────────────────────────────────────────────────┘
```

---

## 3. 📐 CÔNG THỨC TOÁN HỌC CỐT LÕI

### 3.1. Pha 1: Động lực học hạt PSO
- Cập nhật vận tốc từng chiều $d \in \{1, \dots, 12\}$:
  $$v_{i,d}(t+1) = w \cdot v_{i,d}(t) + c_1 r_{1,d} \cdot (p_{i,d} - x_{i,d}(t)) + c_2 r_{2,d} \cdot (g^*_d - x_{i,d}(t))$$
  - Tham số: $w = 0.7, c_1 = 1.5, c_2 = 1.5$.
  - Cắt tỉa vận tốc: $v_{i,d} \in [-0.2 \Delta_d, \; 0.2 \Delta_d]$.
- Cập nhật vị trí tạm thời:
  $$\mathbf{X}_i^{\text{temp}} = \text{clip}(\mathbf{X}_i(t) + \mathbf{V}_i(t+1), \mathbf{LB}, \mathbf{UB})$$

### 3.2. Pha 2: Lai ghép số học GA (Arithmetic Crossover)
- Bầy hạt sau khi di chuyển được ghép thành từng cặp $(\mathbf{X}_i, \mathbf{X}_j)$.
- Với xác suất lai ghép $P_c = 0.8$:
  - Sinh vector ngẫu nhiên $\boldsymbol{\alpha} \sim \mathcal{U}(0, 1)^{12}$.
  - Hoán đổi tạo ra hai vị trí mới:
    $$\mathbf{X}_i^{\text{cross}} = \boldsymbol{\alpha} \odot \mathbf{X}_i^{\text{temp}} + (1 - \boldsymbol{\alpha}) \odot \mathbf{X}_j^{\text{temp}}$$
    $$\mathbf{X}_j^{\text{cross}} = (1 - \boldsymbol{\alpha}) \odot \mathbf{X}_i^{\text{temp}} + \boldsymbol{\alpha} \odot \mathbf{X}_j^{\text{temp}}$$

### 3.3. Pha 3: Đột biến Gaussian
- Với xác suất đột biến $P_m = 0.15$ trên từng tọa độ:
  $$x_{i,d}^{\text{final}} = x_{i,d}^{\text{cross}} + \mathcal{N}\left(0, \; (0.1 \cdot (UB_d - LB_d))^2\right)$$
- Sau đó cắt tỉa biên an toàn vào dải $[LB_d, UB_d]$.

---

## 4. 🗺️ BẢN ĐỒ MÃ NGUỒN (CODE MAPPING)

- **File triển khai chính:** [`hybrid_pso_ga.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/hybrid/hybrid_pso_ga.py)
- **Tái sử dụng các module:**
  - Vận tốc & Vị trí PSO: [`velocity_update.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/PSO/velocity_update.py), [`position_update.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/PSO/position_update.py).
  - Lai ghép & Đột biến GA: [`crossover.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/GA/crossover.py), [`mutation.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/GA/mutation.py).

---

## 5. 📊 ĐÁNH GIÁ THỰC NGHIỆM TRONG BÀI TOÁN UAV
- **Part 1 (35 vòng lặp):** Fitness TB = `0.4416` (Xếp hạng 4/6).
- **Part 2 (80 vòng lặp):** Fitness TB = `0.4481` (**Xếp hạng 2/6, chỉ đứng sau I-WOA**).
- **Nhận xét chuyên sâu:** H-PSO-GA thể hiện sức mạnh vượt trội hơn hẳn so với cả PSO thuần và GA thuần. Các toán tử lai ghép và đột biến của GA đã thành công "giải cứu" bầy hạt PSO khỏi hiện tượng trì trệ, giúp thuật toán liên tục cải thiện Fitness ở các vòng lặp sâu.

---

## 6. 🎓 BỘ CÂU HỎI THẦY CÔ VẤN ĐÁP & CÂU TRẢ LỜI MẪU

### ❓ Câu 1: *"Tại sao em lại lai ghép PSO với GA mà không giữ nguyên PSO thuần?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, điểm yếu tử huyệt của PSO là sau khi các hạt tiến lại gần $G_{\text{best}}$, thành phần vận tốc triệt tiêu dần và bầy bị tê liệt (kẹt cực trị địa phương). Việc tích hợp GA đóng vai trò như một **bộ sốc điện tái tạo năng lượng**: lai ghép giúp các hạt chia sẻ thông tin vị trí tốt cho nhau, còn đột biến Gauss thỉnh thoảng làm lệch vị trí một vài hạt, giúp bầy tiếp tục khám phá các vùng không gian tiềm năng mới."*

### ❓ Câu 2: *"H-PSO-GA đứng thứ 2 rất tốt, vậy vì sao I-WOA vẫn vượt trội hơn H-PSO-GA ở Part 2?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, dù H-PSO-GA cải thiện được tính đa dạng, nhưng quỹ đạo chuyển động của nó vẫn dựa trên vector gia tốc thẳng của PSO nên có xu hướng kéo các UAV về cùng cụm trung tâm, khiến **tỷ lệ nhiễu giao thoa vẫn ở mức $7.75\%$**. 
> Trong khi đó, **I-WOA** dùng quỹ đạo xoắn ốc kết hợp với **phân cụm K-Means** và **bước nhảy Levy** giúp các UAV tản đều thành các vùng nón phủ độc lập, hạ tỷ lệ nhiễu xuống đáy kỷ lục **$5.72\%$**, do đó đạt điểm số Fitness cao hơn."*

---

## 7. 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT (ACADEMIC REFERENCES)
1. **Juang, C. F. (2004).** "A hybrid of genetic algorithm and particle swarm optimization for recurrent network design". *IEEE Transactions on Systems, Man, and Cybernetics, Part B*, vol. 34, no. 2, pp. 997–1006. DOI: [`10.1109/TSMCB.2003.818557`](https://doi.org/10.1109/TSMCB.2003.818557). *(Nguyên lý lai ghép PSO với các toán tử di truyền GA)*.
2. **Shi, X. H., Lu, Y. H., Shen, C. G., & Wang, L. X. (2005).** "A hybrid algorithm of genetic algorithm and particle swarm optimization for TSP". *Fourth International Conference on Machine Learning and Cybernetics*, pp. 4941–4946.
3. **Robinson, J., Sinton, S., & Rahmat-Samii, Y. (2002).** "Particle swarm, genetic algorithm, and their hybrids: optimization of a profiled corrugated horn antenna". *IEEE Antennas and Propagation Society International Symposium*, vol. 1, pp. 314–317.

