# 🦅 DWPSO: TÀI LIỆU KỸ THUẬT & CÔNG THỨC TỐI ƯU HÓA BẦY ĐÀN (PSO)
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
  - $w = 0.7$: **Trọng số quán tính (Inertia Weight)**. Cân bằng giữa khám phá diện rộng (Exploration) và khai thác cục bộ (Exploitation).
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
| Cấu trúc hạt (Hạt & Vận tốc) | [`particle.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/PSO/particle.py) | `class Particle` |
| Khởi tạo bầy hạt ngẫu nhiên | [`initialization.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/PSO/initialization.py) | `initialize_swarm()` |
| Cập nhật vận tốc $v(t+1)$ | [`velocity_update.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/PSO/velocity_update.py) | `update_velocity()` |
| Cập nhật vị trí $x(t+1)$ | [`position_update.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/PSO/position_update.py) | `update_position()` |
| Cập nhật $P_{\text{best}}, G_{\text{best}}$ | [`best_update.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/PSO/best_update.py) | `update_bests()` |
| Xử lý va chạm biên | [`boundary_handler.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/PSO/boundary_handler.py) | `handle_boundaries()` |
| Bộ điều khiển tối ưu hóa | [`optimizer.py`](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/src/algorithms/PSO/optimizer.py) | `class PSOOptimizer.optimize()` |

---

## 5. 📊 ĐÁNH GIÁ THỰC NGHIỆM TRONG BÀI TOÁN UAV
- **Part 1 (35 vòng lặp):** Fitness TB = `0.4426` (Xếp hạng 2/6, chỉ sau H-WOA-PSO). Thời gian chạy siêu nhanh (**0.72s**). PSO chứng minh tốc độ hội tụ cực nhanh ở giai đoạn đầu.
- **Part 2 (80 vòng lặp):** Fitness TB = `0.4459` (Tụt xuống hạng 3/6). Mức tăng trưởng rất thấp (**$+0.0033$**).
- **Điểm yếu then chốt:** Hiện tượng **mắc kẹt cực trị địa phương (Premature Convergence)**. Khi toàn bộ bầy hạt bị kéo quá mạnh về $G_{\text{best}}$, vận tốc của bầy tiệm cận về 0 khiến bầy bị "đóng băng" (stagnant), không thể tìm được nghiệm tốt hơn dù có tăng số vòng lặp lên 80 hay 100.

---

## 6. 🎓 BỘ CÂU HỎI THẦY CÔ VẤN ĐÁP & CÂU TRẢ LỜI MẪU

### ❓ Câu 1: *"Hệ số $w$, $c_1$, $c_2$ trong công thức vận tốc có vai trò gì và em chọn bao nhiêu?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, 3 hệ số này điều khiển tính cân bằng của PSO:
> - $w = 0.7$ (Quán tính): kiểm soát khả năng bay tự do khám phá không gian mới.
> - $c_1 = 1.5$ (Nhận thức): kéo hạt về vị trí tốt nhất trong quá khứ của chính nó.
> - $c_2 = 1.5$ (Xã hội): kéo hạt về vị trí tốt nhất của cả bầy đàn.
> Em chọn bộ thông số chuẩn theo khuyến nghị của Clerc & Kennedy ($w \approx 0.7, c_1 = c_2 = 1.5$) để đảm bảo bầy hạt dao động hội tụ ổn định mà không bị phát tán vô hạn."*

### ❓ Câu 2: *"Tại sao phải đặt giới hạn $V_{\max}$ cho vận tốc?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, nếu không có $V_{\max}$, ở các vòng lặp đầu khi khoảng cách giữa hạt và $G_{\text{best}}$ còn rất xa, thành phần gia tốc $(g^* - x)$ sẽ cực lớn, làm vận tốc hạt tăng vọt theo cấp số nhân (Swarm Explosion). Hạt sẽ bay vọt qua vùng nghiệm tối ưu và liên tục đâm vào biên bản đồ. $V_{\max} = 0.2 \times (UB - LB)$ giúp bước nhảy của hạt được kiểm soát nhịp nhàng trong phạm vi $200\text{ m}$."*

### ❓ Câu 3: *"Tại sao PSO lại chạy rất tốt ở 35 vòng lặp nhưng lại bị I-WOA vượt mặt ở 80 vòng lặp?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, vì cơ chế gia tốc hướng về $G_{\text{best}}$ giúp PSO dồn toàn lực bầy đàn hội tụ rất nhanh trong 20-30 vòng lặp đầu. Tuy nhiên, khi bầy hạt đã dồn lại một chỗ, tính đa dạng quần thể giảm về 0 và vận tốc triệt tiêu, PSO không có cơ chế đột biến để nhảy ra ngoài. Trong khi đó, I-WOA có **bước nhảy Levy** và **học đối kháng OBL** nên liên tục tạo đột phá toàn cục khi chạy sâu, từ đó vượt qua PSO ở 80 vòng lặp."*

---

## 7. 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT (ACADEMIC REFERENCES)
1. **Kennedy, J., & Eberhart, R. (1995).** "Particle swarm optimization". *Proceedings of ICNN'95*, vol. 4, pp. 1942–1948. DOI: [`10.1109/ICNN.1995.488968`](https://doi.org/10.1109/ICNN.1995.488968). *(Bài báo gốc phát minh thuật toán PSO)*.
2. **Shi, Y., & Eberhart, R. (1998).** "A modified particle swarm optimizer". *IEEE ICEC Proceedings*, pp. 69–73. DOI: [`10.1109/ICEC.1998.699146`](https://doi.org/10.1109/ICEC.1998.699146). *(Công thức vận tốc quán tính $w=0.7$ trong `velocity_update.py`)*.
3. **Clerc, M., & Kennedy, J. (2002).** "The particle swarm - explosion, stability, and convergence in a multidimensional complex space". *IEEE Transactions on Evolutionary Computation*, vol. 6, no. 1, pp. 58–73. DOI: [`10.1109/4235.985692`](https://doi.org/10.1109/4235.985692). *(Lý giải cơ chế giới hạn $V_{\max}$)*.

