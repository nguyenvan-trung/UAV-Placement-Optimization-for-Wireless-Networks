# 🧬 DWGA: TÀI LIỆU KỸ THUẬT & CÔNG THỨC THUẬT TOÁN DI TRUYỀN (GA)

[Mục lục](README.md) · [Thuật ngữ](GLOSSARY.md) · [Mô hình chung](REPORT.md) · [Biến thể và study 100 vòng](NOTEBOOK_STUDY.md)

Trang này giải thích cơ chế baseline/bản đầy đủ. Các cờ K/O/L mới của GA/PSO và ablation bản lai được mô tả tại NOTEBOOK_STUDY; không suy ra hiệu quả thực nghiệm từ tên toán tử. Đọc mô hình và thuật ngữ trước, rồi xem thiết kế study sau chương này.


> Tài liệu phương pháp; các kết luận thực nghiệm cũ đã được rút. Không có bảng xếp hạng mới khi chưa có log FE. Mô hình chung: [REPORT.md](REPORT.md).

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
  - Độ cao bay mô phỏng: $z_i \in [50, 300]\text{ m}$.

---

## 3. 📐 CÔNG THỨC TOÁN HỌC CHI TIẾT

### 3.1. Chọn lọc đấu loại (Tournament Selection)
Thay vì dùng bánh xe Roulette dễ bị trôi dạt di truyền (genetic drift) khi có cá thể quá vượt trội, hệ thống sử dụng **Tournament Selection** với kích thước bảng đấu $k = 3$:
- Chọn ngẫu nhiên $k$ cá thể từ quần thể: $\mathcal{S} = \{ \mathbf{X}_{r_1}, \mathbf{X}_{r_2}, \dots, \mathbf{X}_{r_k} \}$.
- Chọn cá thể cha/mẹ có Fitness lớn nhất:
  $$\mathbf{X}_{\text{parent}} = \arg\max_{\mathbf{X} \in \mathcal{S}} \text{Fitness}(\mathbf{X})$$

### 3.2. Lai ghép số học liên tục (Arithmetic Crossover)
Khác với GA nhị phân cắt điểm, bài toán tọa độ liên tục sử dụng phép tổ hợp lồi ngẫu nhiên (Convex Combination):
- Với xác suất lai ghép $P_c = 0.9$ (theo `GAParameters`), nếu $r \sim \mathcal{U}(0, 1) < P_c$:
  - Sinh vector trọng số ngẫu nhiên $\boldsymbol{\alpha} = [\alpha_1, \alpha_2, \dots, \alpha_D] \sim \mathcal{U}(0, 1)^D$ với $D = 12$.
  - Hai cá thể con (Offspring) được sinh ra theo công thức:
    $$\mathbf{X}_{\text{child1}} = \boldsymbol{\alpha} \odot \mathbf{X}_{\text{parent1}} + (1 - \boldsymbol{\alpha}) \odot \mathbf{X}_{\text{parent2}}$$
    $$\mathbf{X}_{\text{child2}} = (1 - \boldsymbol{\alpha}) \odot \mathbf{X}_{\text{parent1}} + \boldsymbol{\alpha} \odot \mathbf{X}_{\text{parent2}}$$
    *(trong đó $\odot$ là phép nhân từng phần tử - Hadamard product)*.
  - Sau đó cắt tỉa biên: $\mathbf{X}_{\text{child}} = \text{clip}(\mathbf{X}_{\text{child}}, \mathbf{LB}, \mathbf{UB})$.

### 3.3. Đột biến Gaussian (Gaussian Mutation)
Đột biến đóng vai trò khai phá vùng không gian mới và chống nghẽn gen:
- Với mỗi gene $j \in \{1, \dots, 12\}$ của cá thể, nếu $r_j \sim \mathcal{U}(0, 1) < P_m$ ($P_m = 0.1$, theo `GAParameters`):
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
| Cấu trúc cá thể | [`chromosome.py`](../src/algorithms/GA/chromosome.py) | `class Chromosome` |
| Khởi tạo quần thể | [`initialization.py`](../src/algorithms/GA/initialization.py) | `initialize_population()` |
| Chọn lọc cha mẹ | [`selection.py`](../src/algorithms/GA/selection.py) | `tournament_selection()` |
| Lai ghép số học | [`crossover.py`](../src/algorithms/GA/crossover.py) | `arithmetic_crossover()` |
| Đột biến Gaussian | [`mutation.py`](../src/algorithms/GA/mutation.py) | `gaussian_mutation()` |
| Chiến lược Elitism | [`replacement.py`](../src/algorithms/GA/replacement.py) | `elitism_replacement()` |
| Bộ điều khiển vòng lặp | [`optimizer.py`](../src/algorithms/GA/optimizer.py) | `class GAOptimizer.optimize()` |

---

## 5. Trạng thái thực nghiệm và diễn giải

Các số liệu và phần trả lời phản biện dựa trên kết quả cũ đã được rút khỏi tài liệu. Chưa có log benchmark theo FE để xác nhận thứ hạng hoặc quy nguyên nhân cho từng cơ chế. Không kết luận thuật toán này vượt thuật toán khác từ mô tả toán tử. Xem [báo cáo tổng hợp](REPORT.md), [ablation](ABLATION.md), [độ nhạy](SENSITIVITY.md) và [thống kê](STATISTICS.md).

## 7. Tài liệu tham khảo dự kiến — cần sinh viên tự xác minh

Danh mục kế thừa từ bản cũ; thông tin thư mục và mức độ phù hợp cần sinh viên tự đọc xác minh. Không coi các chú giải bên dưới là bằng chứng đã kiểm chứng hoặc nguồn của toàn bộ Fitness. Xem quy tắc trích dẫn trong [REPORT.md](REPORT.md).
1. **Holland, J. H. (1975).** *Adaptation in Natural and Artificial Systems*. University of Michigan Press. *(Nền tảng lý thuyết GA và cơ chế chọn lọc tự nhiên)*.
2. **Herrera, F., Lozano, M., & Verdegay, J. L. (1998).** "Tackling real-coded genetic algorithms: Operators and tools for behavioural analysis". *Artificial Intelligence Review*, vol. 12, no. 4, pp. 265–319. DOI: [`10.1023/A:1006504901164`](https://doi.org/10.1023/A:1006504901164). *(Cơ sở cho toán tử Arithmetic Crossover liên tục trong `crossover.py`)*.
3. **Michalewicz, Z. (1996).** *Genetic Algorithms + Data Structures = Evolution Programs*. Springer. *(Đột biến Gaussian và chiến lược Elitism)*.
