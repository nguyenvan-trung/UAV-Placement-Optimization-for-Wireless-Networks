# 🐋 DWWOA: TÀI LIỆU KỸ THUẬT & CÔNG THỨC THUẬT TOÁN BẦY CÁ VOI (WOA GỐC)
> **Mục đích:** Hướng dẫn chi tiết công thức toán học, cấu trúc mã nguồn và kịch bản trả lời phản biện dành cho thuật toán **Whale Optimization Algorithm (WOA)** trong bài toán tối ưu hóa vị trí 3D trạm phát sóng UAV.

---

## 1. 💡 Ý TƯỞNG CỐT LÕI & CẢM HỨNG TỰ NHIÊN
- **Cảm hứng sinh học:** WOA do Seyedali Mirjalili và Andrew Lewis đề xuất năm 2016, mô phỏng chiến thuật săn mồi bằng lưới bọt khí độc đáo (Bubble-net hunting strategy) của loài **cá voi lưng gù (Humpback whale)**.
- **Hành vi săn mồi:** Đàn cá voi lặn sâu xuống dưới đàn cá nhỏ hoặc nhuyễn thể, vừa bơi vòng xoắn ốc hướng lên mặt nước vừa nhả ra những cột bọt khí hình tròn bao vây con mồi và dồn ép chúng vào tâm bẫy để nuốt trọn.
- **Chiến lược tìm kiếm:** Được chia thành 3 cơ chế toán học rõ rệt:
  1. **Bao vây con mồi (Encircling Prey):** Thu hẹp dần bán kính bao quanh vị trí tốt nhất.
  2. **Tấn công xoắn ốc lưới bọt (Spiral Bubble-net Attack):** Mô phỏng đường bơi xoắn ốc 3D tiến về phía con mồi.
  3. **Thám hiểm tìm mồi toàn cục (Search for Prey):** Bơi ngẫu nhiên theo một cá thể bất kỳ trong bầy để mở rộng không gian tìm kiếm.

---

## 2. 🎯 BIỂU DIỄN CÁ VOI TRONG BÀI TOÁN UAV (WHALE STATE)
Mỗi con cá voi $i$ đại diện cho một phương án phối hợp 4 UAV trong không gian 3 chiều:

$$\mathbf{X}_i(t) = [x_1, y_1, z_1, \; x_2, y_2, z_2, \; x_3, y_3, z_3, \; x_4, y_4, z_4]^T \in \mathbb{R}^{12}$$

- Con mồi mục tiêu $\mathbf{X}^*(t)$ chính là cấu hình 4 UAV đạt giá trị hàm mục tiêu Fitness cao nhất trong bầy tại vòng lặp $t$:
  $$\mathbf{X}^*(t) = \arg\max_{i=1,\dots,PopSize} \text{Fitness}(\mathbf{X}_i(t))$$

---

## 3. 📐 CÔNG THỨC TOÁN HỌC CỐT LÕI

### 3.1. Các hệ số điều khiển thích nghi ($a, \mathbf{A}, \mathbf{C}, l, p$)
Tại mỗi vòng lặp $t$ ($t = 0, \dots, MaxIter - 1$):
- **Hệ số $a$:** Giảm tuyến tính từ 2 về 0 để chuyển dịch dần từ giai đoạn Thám hiểm (Exploration) sang Khai thác (Exploitation):
  $$a = 2.0 - 2.0 \cdot \left(\frac{t}{MaxIter - 1}\right)$$
- **Vector hệ số $\mathbf{A}$:** 
  $$\mathbf{A} = 2 a \cdot \mathbf{r}_1 - a, \quad \mathbf{r}_1 \sim \mathcal{U}(0, 1)^D$$
  *(Biên độ dao động của $A$ nằm trong đoạn $[-a, a]$. Khi $|A| < 1$, cá voi tập trung khai thác; khi $|A| \ge 1$, cá voi thám hiểm toàn cục)*.
- **Vector hệ số dao động $\mathbf{C}$:**
  $$\mathbf{C} = 2 \cdot \mathbf{r}_2, \quad \mathbf{r}_2 \sim \mathcal{U}(0, 1)^D$$
  *(Cung cấp trọng số ngẫu nhiên cho con mồi, tăng cường tính đa dạng)*.
- **Biến xoắn ốc $l$:** Một số thực ngẫu nhiên $l \sim \mathcal{U}(-1, 1)$.
- **Xác suất lựa chọn cơ chế $p$:** Số thực ngẫu nhiên $p \sim \mathcal{U}(0, 1)$.

---

### 3.2. Cơ chế 1: Bao vây con mồi (Encircling Prey)
Được kích hoạt khi **$p < 0.5$** và **$|A| < 1$** (khoảng cách thu hẹp về con mồi tốt nhất $\mathbf{X}^*$):

$$\mathbf{D} = \left| \mathbf{C} \odot \mathbf{X}^*(t) - \mathbf{X}_i(t) \right|$$
$$\mathbf{X}_i(t+1) = \mathbf{X}^*(t) - \mathbf{A} \odot \mathbf{D}$$

---

### 3.3. Cơ chế 2: Bơi xoắn ốc lưới bọt khí (Spiral Bubble-net Attacking)
Được kích hoạt khi **$p \ge 0.5$**. Cá voi bơi theo quỹ đạo xoắn ốc logarithmic hướng về con mồi:

$$\mathbf{D}' = \left| \mathbf{X}^*(t) - \mathbf{X}_i(t) \right|$$
$$\mathbf{X}_i(t+1) = \mathbf{D}' \odot e^{b l} \cos(2\pi l) + \mathbf{X}^*(t)$$

- **Ý nghĩa tham số:**
  - $b = 1.0$: Hằng số định hình độ cong của đường xoắn ốc logarithmic.
  - $l \in [-1, 1]$: Xác định khoảng cách tương đối giữa cá voi và con mồi trên quỹ đạo xoắn. Khi $l \to 0$, $e^{bl} \cos(2\pi l) \to 1$, vị trí cá voi tiến sát con mồi.

---

### 3.4. Cơ chế 3: Thám hiểm tìm mồi toàn cục (Search for Prey)
Được kích hoạt khi **$p < 0.5$** và **$|A| \ge 1$**. Thay vì hướng về con đầu đàn $\mathbf{X}^*$, cá voi sẽ bơi dạt ra xa theo một con cá voi ngẫu nhiên $\mathbf{X}_{\text{rand}}$ trong quần thể:

$$\mathbf{D} = \left| \mathbf{C} \odot \mathbf{X}_{\text{rand}} - \mathbf{X}_i(t) \right|$$
$$\mathbf{X}_i(t+1) = \mathbf{X}_{\text{rand}} - \mathbf{A} \odot \mathbf{D}$$

---

## 4. 🗺️ BẢN ĐỒ MÃ NGUỒN (CODE MAPPING)

| Thành phần thuật toán | File mã nguồn tương ứng | Hàm / Class chính |
| :--- | :--- | :--- |
| Cấu trúc cá thể cá voi | [`whale.py`](..\src\algorithms\WOA\whale.py) | `class Whale` |
| Khởi tạo bầy cá voi | [`initialization.py`](..\src\algorithms\WOA\initialization.py) | `initialize_whales()` |
| Cập nhật hệ số $a, A, C, l$ | [`coefficient_update.py`](..\src\algorithms\WOA\coefficient_update.py) | `update_coefficients()` |
| Bao vây con mồi | [`encircling.py`](..\src\algorithms\WOA\encircling.py) | `encircle_prey()` |
| Bơi xoắn ốc bọt khí | [`spiral_update.py`](..\src\algorithms\WOA\spiral_update.py) | `spiral_update()` |
| Thám hiểm tìm mồi | [`exploration.py`](..\src\algorithms\WOA\exploration.py) | `search_for_prey()` |
| Xử lý giới hạn biên | [`boundary_handler.py`](..\src\algorithms\WOA\boundary_handler.py) | `handle_boundaries()` |
| Bộ điều khiển tối ưu hóa | [`optimizer.py`](..\src\algorithms\WOA\optimizer.py) | `class WOAOptimizer.optimize()` |

---

## 5. 📊 ĐÁNH GIÁ THỰC NGHIỆM TRONG BÀI TOÁN UAV
- **Part 1 (35 vòng lặp):** Fitness TB = `0.4425` (Xếp hạng 3/6). Tỷ lệ nhiễu giao thoa thấp rất ấn tượng (**8.47%**, thấp nhất trong các thuật toán cổ điển). Đường bơi xoắn ốc giúp bầy UAV tản đều rất tốt trên không gian 3D.
- **Part 2 (80 vòng lặp):** Fitness TB = `0.4437` (Tụt xuống hạng 5/6, chỉ tăng $+0.0012$).
- **Nguyên nhân tụt hạng:** WOA gốc dựa vào cơ chế giảm tuyến tính $a = 2 \to 0$. Khi vòng lặp lớn ($t > 40$), $a < 1$ nên $|A|$ hầu như luôn bé hơn 1, bầy cá voi **mất hoàn toàn khả năng thám hiểm toàn cục (Search for prey)** và chỉ bơi xoắn ốc cục bộ quanh nghiệm tốt nhất. Do đó, WOA gốc dễ dàng bị mắc kẹt tại cực trị địa phương.

---

## 6. 🎓 BỘ CÂU HỎI THẦY CÔ VẤN ĐÁP & CÂU TRẢ LỜI MẪU

### ❓ Câu 1: *"Cơ chế bơi xoắn ốc logarithmic của WOA có ưu thế gì so với cơ chế vận tốc tuyến tính của PSO?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, trong PSO, hạt di chuyển thẳng theo vector vận tốc $v = w v + c_1 r_1 \Delta x_1 + c_2 r_2 \Delta x_2$, rất dễ khiến các UAV đâm dồn cục vào nhau tại một vị trí (gây nhiễu giao thoa cao). Trong khi đó, **quỹ đạo xoắn ốc $e^{bl} \cos(2\pi l)$ của WOA** quét không gian theo hình lốc xoáy 3 chiều xung quanh con mồi, giúp các UAV vừa tiến gần về vùng phủ sóng tốt vừa giữ được khoảng cách phân tán tự nhiên, giảm can nhiễu."*

### ❓ Câu 2: *"Ý nghĩa của hệ số $A$ và điều kiện $|A| \ge 1$ là gì?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, $|A|$ là ngưỡng phân định giữa Thám hiểm (Exploration) và Khai thác (Exploitation):
> - Khi $|A| < 1$: Cá voi bơi co cụm lại gần con mồi hiện tại (Khai thác sâu).
> - Khi $|A| \ge 1$: Bước di chuyển bị phóng đại ra xa, cá voi bắt buộc phải chọn một cá thể ngẫu nhiên $X_{\text{rand}}$ thay vì con đầu đàn $X^*$ để bơi theo. Điều này giúp bầy cá voi tản rộng khắp bản đồ, tránh sa bẫy vào vùng nghiệm giả."*

### ❓ Câu 3: *"Tại sao em phải cải tiến WOA thành I-WOA mà không dùng luôn WOA gốc?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, thực nghiệm ở Phần 2 chứng minh WOA gốc bị nghẽn: khi số vòng lặp tăng từ 35 lên 80, Fitness của WOA gốc hầu như dậm chân tại chỗ (chỉ tăng $+0.0012$, tụt xuống hạng 5) vì sau nửa chặng đường, hệ số $a$ suy giảm làm $|A| < 1$ triệt tiêu khả năng nhảy vùng. Để giải quyết dứt điểm điểm yếu này, em đã đề xuất thuật toán cải tiến **I-WOA** bổ sung **K-Means**, **Học đối kháng OBL** và **Bước nhảy Levy Flight**."*

---

## 7. 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT (ACADEMIC REFERENCES)
1. **Mirjalili, S., & Lewis, A. (2016).** "The Whale Optimization Algorithm". *Advances in Engineering Software*, vol. 95, pp. 51–67. DOI: [`10.1016/j.advengsoft.2016.01.008`](https://doi.org/10.1016/j.advengsoft.2016.01.008). *(Bài báo gốc đề xuất thuật toán WOA và cơ chế săn mồi lưới bọt khí xoắn ốc)*.
2. **Mohammed, H., et al. (2020).** "A comprehensive survey on Whale Optimization Algorithm: Variants, applications, and hybridizations". *Neurocomputing*, vol. 410, pp. 397–433. DOI: [`10.1016/j.neucom.2020.04.110`](https://doi.org/10.1016/j.neucom.2020.04.110). *(Khảo sát hạn chế kẹt cực trị địa phương của WOA)*.
3. **Gharsallah, A., et al. (2021).** "Whale optimization algorithm for 3D deployment of UAV base stations in wireless communication systems". *Applied Soft Computing*, vol. 103, p. 107147. *(Ứng dụng WOA trong tối ưu hóa vị trí 3D UAV)*.

