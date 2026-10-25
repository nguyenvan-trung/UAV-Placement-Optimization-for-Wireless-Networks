# 🧬🦅 DWH_PSO_GA: TÀI LIỆU KỸ THUẬT & CÔNG THỨC THUẬT TOÁN LAI H-PSO-GA

[Mục lục](README.md) · [Thuật ngữ](GLOSSARY.md) · [Mô hình chung](REPORT.md) · [Biến thể và study 100 vòng](NOTEBOOK_STUDY.md)

Trang này giải thích cơ chế baseline/bản đầy đủ. Các cờ K/O/L mới của GA/PSO và ablation bản lai được mô tả tại NOTEBOOK_STUDY; không suy ra hiệu quả thực nghiệm từ tên toán tử. Đọc mô hình và thuật ngữ trước, rồi xem thiết kế study sau chương này.


> Tài liệu phương pháp; các kết luận thực nghiệm cũ đã được rút. Không có bảng xếp hạng mới khi chưa có log FE. Mô hình chung: [REPORT.md](REPORT.md).

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
  - Tham số: $w$ giảm tuyến tính theo vòng lặp trong code hiện tại; $c_1 = 1.5, c_2 = 1.5$.
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

- **File triển khai chính:** [`hybrid_pso_ga.py`](../src/algorithms/hybrid/hybrid_pso_ga.py)
- **Tái sử dụng các module:**
  - Vận tốc & Vị trí PSO: [`velocity_update.py`](../src/algorithms/PSO/velocity_update.py), [`position_update.py`](../src/algorithms/PSO/position_update.py).
  - Lai ghép & Đột biến GA: [`crossover.py`](../src/algorithms/GA/crossover.py), [`mutation.py`](../src/algorithms/GA/mutation.py).

---

## 5. Trạng thái thực nghiệm và diễn giải

Các số liệu và phần trả lời phản biện dựa trên kết quả cũ đã được rút khỏi tài liệu. Chưa có log benchmark theo FE để xác nhận thứ hạng hoặc quy nguyên nhân cho từng cơ chế. Không kết luận thuật toán này vượt thuật toán khác từ mô tả toán tử. Xem [báo cáo tổng hợp](REPORT.md), [ablation](ABLATION.md), [độ nhạy](SENSITIVITY.md) và [thống kê](STATISTICS.md).

## 7. Tài liệu tham khảo dự kiến — cần sinh viên tự xác minh

Danh mục kế thừa từ bản cũ; thông tin thư mục và mức độ phù hợp cần sinh viên tự đọc xác minh. Không coi các chú giải bên dưới là bằng chứng đã kiểm chứng hoặc nguồn của toàn bộ Fitness. Xem quy tắc trích dẫn trong [REPORT.md](REPORT.md).
1. **Juang, C. F. (2004).** "A hybrid of genetic algorithm and particle swarm optimization for recurrent network design". *IEEE Transactions on Systems, Man, and Cybernetics, Part B*, vol. 34, no. 2, pp. 997–1006. DOI: [`10.1109/TSMCB.2003.818557`](https://doi.org/10.1109/TSMCB.2003.818557). *(Nguyên lý lai ghép PSO với các toán tử di truyền GA)*.
2. **Shi, X. H., Lu, Y. H., Shen, C. G., & Wang, L. X. (2005).** "A hybrid algorithm of genetic algorithm and particle swarm optimization for TSP". *Fourth International Conference on Machine Learning and Cybernetics*, pp. 4941–4946.
3. **Robinson, J., Sinton, S., & Rahmat-Samii, Y. (2002).** "Particle swarm, genetic algorithm, and their hybrids: optimization of a profiled corrugated horn antenna". *IEEE Antennas and Propagation Society International Symposium*, vol. 1, pp. 314–317.

