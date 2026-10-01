# 🧬 DWGA: TÀI LIỆU KỸ THUẬT & CÔNG THỨC THUẬT TOÁN DI TRUYỀN (GA)
> **Mục đích:** Hướng dẫn chi tiết công thức toán học, cấu trúc mã nguồn và kịch bản trả lời phản biện dành cho thuật toán **Genetic Algorithm (GA)** trong bài toán tối ưu hóa vị trí 3D trạm phát sóng UAV.

---

## 1. 💡 Ý TƯỞNG CỐT LÕI & CẢM HỨNG TỰ NHIÊN
- **Cảm hứng sinh học:** Thuật toán Di truyền (GA - John Holland, 1975) mô phỏng thuyết tiến hóa tự nhiên của Charles Darwin: *"Cá thể nào thích nghi tốt nhất với môi trường (Fitness cao nhất) sẽ có cơ hội sống sót, sinh sản và truyền gene ưu tú cho thế hệ sau"*.
- **Cơ chế chính:** Gồm 4 mắt xích lặp đi lặp lại qua các thế hệ:
  $$\text{Quần thể ban đầu} \longrightarrow \text{Đánh giá Fitness} \longrightarrow \text{Chọn lọc (Selection)} \longrightarrow \text{Lai ghép (Crossover)} \longrightarrow \text{Đột biến (Mutation)} \longrightarrow \text{Thay thế (Elitism Replacement)}$$

---

## 2. 🎯 BIỂU DIỄN NGHIỆM TRONG BÀI TOÁN UAV (CHROMOSOME REPRESENTATION)
Trong bài toán tối ưu hóa vị trí $N = 4$ trạm phát sóng UAV trong không gian 3 chiều, mỗi cá thể (Chromosome) được mã hóa dưới dạng một **vector số thực liên tục (Continuous Real-valued Vector)** gồm $4 \times 3 = 12$ chiều:

$$\mathbf{X} = [x_1, y_1, z_1, \; x_2, y_2, z_2, \; x_3, y_3, z_3, \; x_4, y_4, z_4]^T$$

- **Không gian tìm kiếm:**
  - Tọa độ mặt phẳng: $x_i, y_i \in [0, 1000]\text{ m}$ (khu vực $1\text{ km}^2$).
  - Độ cao bay an toàn: $z_i \in [50, 300]\text{ m}$.

---

## 3. 📐 CÔNG THỨC TOÁN HỌC CHI TIẾT

### 3.1. Chọn lọc đấu loại (Tournament Selection)
Thay vì dùng bánh xe Roulette dễ bị trôi dạt di truyền (genetic drift) khi có cá thể quá vượt trội, hệ thống sử dụng **Tournament Selection** với kích thước bảng đấu $k = 3$:
- Chọn ngẫu nhiên $k$ cá thể từ quần thể: $\mathcal{S} = \{ \mathbf{X}_{r_1}, \mathbf{X}_{r_2}, \dots, \mathbf{X}_{r_k} \}$.
- Chọn cá thể cha/mẹ có Fitness lớn nhất:
  $$\mathbf{X}_{\text{parent}} = \arg\max_{\mathbf{X} \in \mathcal{S}} \text{Fitness}(\mathbf{X})$$

### 3.2. Lai ghép số học liên tục (Arithmetic Crossover)
Khác với GA nhị phân cắt điểm, bài toán tọa độ liên tục sử dụng phép tổ hợp lồi ngẫu nhiên (Convex Combination):
- Với xác suất lai ghép $P_c = 0.8$, nếu $r \sim \mathcal{U}(0, 1) < P_c$:
  - Sinh vector trọng số ngẫu nhiên $\boldsymbol{\alpha} = [\alpha_1, \alpha_2, \dots, \alpha_D] \sim \mathcal{U}(0, 1)^D$ với $D = 12$.
  - Hai cá thể con (Offspring) được sinh ra theo công thức:
    $$\mathbf{X}_{\text{child1}} = \boldsymbol{\alpha} \odot \mathbf{X}_{\text{parent1}} + (1 - \boldsymbol{\alpha}) \odot \mathbf{X}_{\text{parent2}}$$
    $$\mathbf{X}_{\text{child2}} = (1 - \boldsymbol{\alpha}) \odot \mathbf{X}_{\text{parent1}} + \boldsymbol{\alpha} \odot \mathbf{X}_{\text{parent2}}$$
    *(trong đó $\odot$ là phép nhân từng phần tử - Hadamard product)*.
  - Sau đó cắt tỉa biên: $\mathbf{X}_{\text{child}} = \text{clip}(\mathbf{X}_{\text{child}}, \mathbf{LB}, \mathbf{UB})$.

### 3.3. Đột biến Gaussian (Gaussian Mutation)
Đột biến đóng vai trò khai phá vùng không gian mới và chống nghẽn gen:
- Với mỗi gene $j \in \{1, \dots, 12\}$ của cá thể, nếu $r_j \sim \mathcal{U}(0, 1) < P_m$ ($P_m = 0.15$):
  - Giá trị gene được cộng thêm nhiễu Gauss tỉ lệ với dải tìm kiếm:
    $$x_j' = x_j + \Delta_j, \quad \Delta_j \sim \mathcal{N}\left(0, \; (\sigma \cdot (UB_j - LB_j))^2\right)$$
  - Với $\sigma = 0.1$ (độ lệch chuẩn bằng 10% biên độ tìm kiếm).

### 3.4. Chiến lược giữ lại cá thể ưu tú (Elitism Replacement)
Để bảo toàn nghiệm tốt nhất qua các thế hệ không bị phá hủy bởi lai ghép và đột biến:
- Giữ lại $E = 2$ cá thể có Fitness cao nhất từ thế hệ cha mẹ: $\mathcal{P}_{\text{elite}} = \text{Top}_E(\mathcal{P}_t)$.
- Lấy $PopSize - E$ cá thể tốt nhất từ tập con cháu: $\mathcal{P}_{\text{offspring\_selected}} = \text{Top}_{PopSize - E}(\mathcal{P}_{\text{offspring}})$.
- Quần thể thế hệ kế tiếp: $\mathcal{P}_{t+1} = \mathcal{P}_{\text{elite}} \cup \mathcal{P}_{\text{offspring\_selected}}$.

---

## 4. 🗺️ BẢN ĐỒ MÃ NGUỒN (CODE MAPPING)

| Thành phần thuật toán | File mã nguồn tương ứng | Hàm / Class chính |
| :--- | :--- | :--- |
| Cấu trúc cá thể | [`chromosome.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/GA/chromosome.py) | `class Chromosome` |
| Khởi tạo quần thể | [`initialization.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/GA/initialization.py) | `initialize_population()` |
| Chọn lọc cha mẹ | [`selection.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/GA/selection.py) | `tournament_selection()` |
| Lai ghép số học | [`crossover.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/GA/crossover.py) | `arithmetic_crossover()` |
| Đột biến Gaussian | [`mutation.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/GA/mutation.py) | `gaussian_mutation()` |
| Chiến lược Elitism | [`replacement.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/GA/replacement.py) | `elitism_replacement()` |
| Bộ điều khiển vòng lặp | [`optimizer.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/GA/optimizer.py) | `class GAOptimizer.optimize()` |

---

## 5. 📊 ĐÁNH GIÁ THỰC NGHIỆM TRONG BÀI TOÁN UAV
- **Part 1 (35 vòng lặp):** Fitness TB = `0.4369` (Xếp hạng 6/6). GA khởi động chậm do phụ thuộc vào phép lai ngẫu nhiên, chưa hội tụ kịp.
- **Part 2 (80 vòng lặp):** Fitness TB = `0.4447` (Vươn lên hạng 4/6, tăng $+0.0078$). 
- **Đặc trưng:** GA có khả năng khám phá không gian rộng rất tốt nhờ đột biến Gauss, độ phủ sóng luôn cao ($99.91\%$), nhưng tỷ lệ nhiễu giao thoa cao ($8.42\% - 11.24\%$) do các UAV dễ bị dồn cụm ngẫu nhiên.

---

## 6. 🎓 BỘ CÂU HỎI THẦY CÔ VẤN ĐÁP & CÂU TRẢ LỜI MẪU

### ❓ Câu 1: *"Tại sao em không dùng lai ghép 1 điểm cắt (Single-point Crossover) như GA truyền thống mà lại dùng Arithmetic Crossover?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, GA truyền thống dùng cho chuỗi bit nhị phân nên cắt 1 điểm rất phù hợp. Tuy nhiên bài toán định vị UAV là bài toán trong **không gian liên tục 3D thực**. Nếu cắt ghép thô bạo tọa độ giữa 2 UAV khác nhau sẽ làm đứt gãy cấu trúc hình học của bầy UAV. Phép **Arithmetic Crossover (lai ghép số học tổ hợp lồi)** giúp tạo ra nghiệm con là phép suy rộng vị trí mềm dẻo giữa 2 cấu hình bay của cha mẹ, giữ được tính liên tục của không gian vật lý."*

### ❓ Câu 2: *"Cơ chế Elitism đóng vai trò gì, nếu bỏ đi thì thuật toán bị sao?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, Elitism đảm bảo **tính đơn điệu không giảm** của nghiệm tốt nhất. Do lai ghép và đột biến đều có tính ngẫu nhiên, nếu không giữ lại cá thể tốt nhất ($E=2$), một thế hệ sau có thể vô tình phá hủy cấu hình đặt trạm tối ưu đã tìm được ở thế hệ trước, dẫn đến hiện tượng dao động và mất nghiệm tốt."*

### ❓ Câu 3: *"Tại sao đột biến Gaussian lại tốt hơn đột biến đều (Uniform Mutation)?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, đột biến Uniform làm biến đổi gene nhảy lung tung khắp bản đồ với xác suất như nhau. Trong khi đó, **đột biến Gaussian** có hàm mật độ hình chuông: ưu tiên tạo ra các bước vi chỉnh nhỏ quanh vị trí hiện tại (khai thác tinh chỉnh vị trí UAV) nhưng thỉnh thoảng vẫn có bước nhảy lớn ở đuôi phân phối (giúp thoát khỏi cực trị địa phương)."*

---

## 7. 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT (ACADEMIC REFERENCES)
1. **Holland, J. H. (1975).** *Adaptation in Natural and Artificial Systems*. University of Michigan Press. *(Nền tảng lý thuyết GA và cơ chế chọn lọc tự nhiên)*.
2. **Herrera, F., Lozano, M., & Verdegay, J. L. (1998).** "Tackling real-coded genetic algorithms: Operators and tools for behavioural analysis". *Artificial Intelligence Review*, vol. 12, no. 4, pp. 265–319. DOI: [`10.1023/A:1006504901164`](https://doi.org/10.1023/A:1006504901164). *(Cơ sở cho toán tử Arithmetic Crossover liên tục trong `crossover.py`)*.
3. **Michalewicz, Z. (1996).** *Genetic Algorithms + Data Structures = Evolution Programs*. Springer. *(Đột biến Gaussian và chiến lược Elitism)*.

