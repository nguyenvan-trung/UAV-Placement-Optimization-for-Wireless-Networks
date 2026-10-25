# 🦅 DWPSO: TÀI LIỆU KỸ THUẬT & CÔNG THỨC TỐI ƯU HÓA BẦY ĐÀN (PSO)

[Mục lục](README.md) · [Thuật ngữ](GLOSSARY.md) · [Mô hình chung](REPORT.md) · [Biến thể và study 100 vòng](NOTEBOOK_STUDY.md)

Trang này giải thích cơ chế baseline/bản đầy đủ. Các cờ K/O/L mới của GA/PSO và ablation bản lai được mô tả tại NOTEBOOK_STUDY; không suy ra hiệu quả thực nghiệm từ tên toán tử. Đọc mô hình và thuật ngữ trước, rồi xem thiết kế study sau chương này.


> Tài liệu phương pháp; các kết luận thực nghiệm cũ đã được rút. Không có bảng xếp hạng mới khi chưa có log FE. Mô hình chung: [REPORT.md](REPORT.md).

> **Mục đích:** Hướng dẫn chi tiết công thức toán học, cấu trúc mã nguồn và kịch bản trả lời phản biện dành cho thuật toán **Particle Swarm Optimization (PSO)** trong bài toán tối ưu hóa vị trí 3D trạm phát sóng UAV.

---

## 1. 💡 Ý TƯỞNG CỐT LÕI & CẢM HỨNG TỰ NHIÊN
- **Cảm hứng sinh học:** PSO do Kennedy và Eberhart phát minh năm 1995, mô phỏng hành vi di chuyển bầy đàn của đàn chim tìm mồi hoặc đàn cá bơi lội.
- **Nguyên lý bầy đàn:** Mỗi hạt (Particle) đại diện cho một phương án bố trí 4 UAV. Hạt di chuyển trong không gian tìm kiếm 12 chiều dựa trên 3 thành phần động lực học:
  1. **Quán tính (Inertia):** Duy trì quán tính vận tốc chuyển động hiện tại.
  2. **Kinh nghiệm cá nhân (Cognitive component):** Lực kéo hướng về vị trí tốt nhất mà chính hạt đó từng đi qua ($P_{\text{best}}$).
  3. **Ảnh hưởng xã hội (Social component):** Lực kéo hướng về vị trí tốt nhất của toàn bộ bầy đàn ($G_{\text{best}}$).

---

## 2. 🎯 BIỂU DIỄN HẠT TRONG BÀI TOÁN UAV (PARTICLE STATE)
Mỗi hạt $i$ ($i = 1, \dots, PopSize$) tại vòng lặp $t$ được đặc trưng bởi 3 vector 12 chiều:

1. **Vector vị trí:** 
   $$\mathbf{X}_i(t) = [x_1, y_1, z_1, \; x_2, y_2, z_2, \; x_3, y_3, z_3, \; x_4, y_4, z_4]^T \in \mathbb{R}^{12}$$
2. **Vector vận tốc:** 
   $$\mathbf{V}_i(t) = [v_{x_1}, v_{y_1}, v_{z_1}, \dots, v_{z_4}]^T \in \mathbb{R}^{12}$$
3. **Kỷ lục cá nhân (Personal Best):** 
   $$\mathbf{P}_i = \arg\max_{\tau \le t} \text{Fitness}(\mathbf{X}_i(\tau))$$
4. **Kỷ lục toàn bầy (Global Best):** 
   $$\mathbf{G}^* = \arg\max_{i=1,\dots,PopSize} \text{Fitness}(\mathbf{P}_i)$$

---

## 3. 📐 CÔNG THỨC TOÁN HỌC CỐT LÕI

### 3.1. Cập nhật vận tốc hạt (Velocity Update)
Tại mỗi vòng lặp $t+1$, thành phần vận tốc theo từng chiều $d \in \{1, \dots, 12\}$ của hạt $i$ được cập nhật theo công thức kinh điển:

$$v_{i,d}(t+1) = w \cdot v_{i,d}(t) + c_1 r_{1,d} \cdot (p_{i,d} - x_{i,d}(t)) + c_2 r_{2,d} \cdot (g^*_d - x_{i,d}(t))$$

- **Ý nghĩa các tham số:**
  - **Trọng số quán tính:** optimizer hiện giảm tuyến tính từ 0,9 tới 0,4 theo vòng lặp; không dùng giá trị cố định 0,7 của parameter class. Nguồn: `../src/algorithms/PSO/optimizer.py:54-57`. Lịch theo FE chưa triển khai.
  - $c_1 = 1.5$: **Hệ số nhận thức cá nhân (Cognitive Parameter)**. Thể hiện xu hướng hạt tin vào trải nghiệm quá khứ của chính mình.
  - $c_2 = 1.5$: **Hệ số học tập xã hội (Social Parameter)**. Thể hiện xu hướng hạt bị thu hút bởi thành công của con đầu đàn.
  - $r_{1,d}, r_{2,d} \sim \mathcal{U}(0, 1)$: Hai số ngẫu nhiên độc lập phân bố đều tạo tính ngẫu nhiên khám phá.

### 3.2. Giới hạn vận tốc cực đại ($V_{\max}$)
Để tránh hiện tượng hạt bay quá đà văng ra ngoài không gian nghiệm hợp lệ (Swarm Explosion):
$$v_{i,d}(t+1) = \text{clip}(v_{i,d}(t+1), -v_{\max, d}, v_{\max, d})$$
- Trong mã nguồn: $v_{\max, d} = 0.2 \times (UB_d - LB_d)$ (tối đa 20% dải kích thước không gian).
  - Chiều $x, y$: $v_{\max} = 0.2 \times 1000 = 200\text{ m/bước}$.
  - Chiều $z$: $v_{\max} = 0.2 \times (300 - 50) = 50\text{ m/bước}$.

### 3.3. Cập nhật vị trí hạt (Position Update)
$$x_{i,d}(t+1) = x_{i,d}(t) + v_{i,d}(t+1)$$
Sau đó kiểm tra và neo biên:
$$x_{i,d}(t+1) = \max(LB_d, \min(UB_d, x_{i,d}(t+1)))$$

### 3.4. Cập nhật Kỷ lục cá nhân và Toàn bầy ($P_{\text{best}}$ & $G_{\text{best}}$)
- Với mỗi hạt $i$:
  $$\mathbf{P}_i \leftarrow \begin{cases} \mathbf{X}_i(t+1) & \text{nếu } \text{Fitness}(\mathbf{X}_i(t+1)) > \text{Fitness}(\mathbf{P}_i) \\ \mathbf{P}_i & \text{ngược lại} \end{cases}$$
- Cập nhật toàn bầy:
  $$\mathbf{G}^* \leftarrow \arg\max_{i} \text{Fitness}(\mathbf{P}_i)$$

---

## 4. 🗺️ BẢN ĐỒ MÃ NGUỒN (CODE MAPPING)

| Thành phần thuật toán | File mã nguồn tương ứng | Hàm / Class chính |
| :--- | :--- | :--- |
| Cấu trúc hạt (Hạt & Vận tốc) | [`particle.py`](../src/algorithms/PSO/particle.py) | `class Particle` |
| Khởi tạo bầy hạt ngẫu nhiên | [`initialization.py`](../src/algorithms/PSO/initialization.py) | `initialize_swarm()` |
| Cập nhật vận tốc $v(t+1)$ | [`velocity_update.py`](../src/algorithms/PSO/velocity_update.py) | `update_velocity()` |
| Cập nhật vị trí $x(t+1)$ | [`position_update.py`](../src/algorithms/PSO/position_update.py) | `update_position()` |
| Cập nhật $P_{\text{best}}, G_{\text{best}}$ | [`best_update.py`](../src/algorithms/PSO/best_update.py) | `update_bests()` |
| Xử lý va chạm biên | [`boundary_handler.py`](../src/algorithms/PSO/boundary_handler.py) | `handle_boundaries()` |
| Bộ điều khiển tối ưu hóa | [`optimizer.py`](../src/algorithms/PSO/optimizer.py) | `class PSOOptimizer.optimize()` |

---

## 5. Trạng thái thực nghiệm và diễn giải

Các số liệu và phần trả lời phản biện dựa trên kết quả cũ đã được rút khỏi tài liệu. Chưa có log benchmark theo FE để xác nhận thứ hạng hoặc quy nguyên nhân cho từng cơ chế. Không kết luận thuật toán này vượt thuật toán khác từ mô tả toán tử. Xem [báo cáo tổng hợp](REPORT.md), [ablation](ABLATION.md), [độ nhạy](SENSITIVITY.md) và [thống kê](STATISTICS.md).

## 7. Tài liệu tham khảo dự kiến — cần sinh viên tự xác minh

Danh mục kế thừa từ bản cũ; thông tin thư mục và mức độ phù hợp cần sinh viên tự đọc xác minh. Không coi các chú giải bên dưới là bằng chứng đã kiểm chứng hoặc nguồn của toàn bộ Fitness. Xem quy tắc trích dẫn trong [REPORT.md](REPORT.md).
1. **Kennedy, J., & Eberhart, R. (1995).** "Particle swarm optimization". *Proceedings of ICNN'95*, vol. 4, pp. 1942–1948. DOI: [`10.1109/ICNN.1995.488968`](https://doi.org/10.1109/ICNN.1995.488968). *(Bài báo gốc phát minh thuật toán PSO)*.
2. **Shi, Y., & Eberhart, R. (1998).** "A modified particle swarm optimizer". *IEEE ICEC Proceedings*, pp. 69–73. DOI: [`10.1109/ICEC.1998.699146`](https://doi.org/10.1109/ICEC.1998.699146). *(Công thức vận tốc quán tính $w=0.7$ trong `velocity_update.py`)*.
3. **Clerc, M., & Kennedy, J. (2002).** "The particle swarm - explosion, stability, and convergence in a multidimensional complex space". *IEEE Transactions on Evolutionary Computation*, vol. 6, no. 1, pp. 58–73. DOI: [`10.1109/4235.985692`](https://doi.org/10.1109/4235.985692). *(Lý giải cơ chế giới hạn $V_{\max}$)*.

