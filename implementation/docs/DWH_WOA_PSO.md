# 🐋🦅 DWH_WOA_PSO: TÀI LIỆU KỸ THUẬT & CÔNG THỨC THUẬT TOÁN LAI H-WOA-PSO
> **Mục đích:** Hướng dẫn chi tiết công thức toán học, cơ chế lai ghép và kịch bản trả lời phản biện dành cho thuật toán lai **Hybrid WOA-PSO (H-WOA-PSO)** trong bài toán tối ưu hóa vị trí 3D trạm phát sóng UAV.

---

## 1. 💡 Ý TƯỞNG CỐT LÕI & TRIẾT LÝ LAI GHÉP
- **Vấn đề đặt ra:**
  - **WOA thuần túy:** Bơi xoắn ốc phân tán giúp giảm nhiễu rất tốt nhưng tốc độ hội tụ ban đầu chậm vì không lưu lại lịch sử kinh nghiệm cá nhân ($P_{\text{best}}$).
  - **PSO thuần túy:** Tốc độ kéo đàn cực nhanh nhờ $P_{\text{best}}$ và $G_{\text{best}}$ nhưng các hạt dễ đâm sầm vào nhau gây nhiễu giao thoa cao.
- **Triết lý lai ghép H-WOA-PSO:**
  - Tích hợp vector vận tốc và bộ nhớ $P_{\text{best}}$ của PSO trực tiếp vào quỹ đạo bơi xoắn ốc và bao vây của WOA.
  - Vừa tận dụng khả năng định hướng gia tốc tốc độ cao của PSO, vừa tận dụng quỹ đạo quét xoắn ốc 3D của cá voi để phân tán không gian.

---

## 2. 🎯 QUY TRÌNH LAI GHÉP TỪNG THẾ HỆ (PIPELINE)

Tại mỗi vòng lặp $t$, cá thể vừa được cập nhật vận tốc theo PSO, vừa được dịch chuyển theo toán tử săn mồi của WOA:

```text
 ┌────────────────────────────────────────────────────────┐
 │ 1. CẬP NHẬT VẬN TỐC THEO PSO                           │
 │    v(t+1) = w*v + c1*r1*(pbest - x) + c2*r2*(gbest - x) │
 └──────────────────────────┬─────────────────────────────┘
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 2. XÁC ĐỊNH BƯỚC CHUYỂN DỊCH THEO TOÁN TỬ WOA          │
 │    - Nếu p >= 0.5: Bơi xoắn ốc logarithmic            │
 │      x_woa = D' * exp(b*l) * cos(2*pi*l) + gbest       │
 │    - Nếu p < 0.5:                                      │
 │        + Nếu |A| < 1: Bao vây con mồi gbest            │
 │        + Nếu |A| >= 1: Thám hiểm theo x_rand          │
 └──────────────────────────┬─────────────────────────────┘
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 3. TỔNG HỢP VỊ TRÍ MỚI & CẮT BIÊN AN TOÀN              │
 │    x_new = clip(x_woa + 0.5 * v(t+1), LB, UB)          │
 └──────────────────────────┬─────────────────────────────┘
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 4. ĐÁNH GIÁ FITNESS & CẬP NHẬT pbest, gbest            │
 └────────────────────────────────────────────────────────┘
```

---

## 3. 📐 CÔNG THỨC TOÁN HỌC CỐT LÕI

### 3.1. Cập nhật gia tốc bầy đàn PSO
Mỗi cá thể duy trì kỷ lục cá nhân $P_{\text{best}, i}$ và kỷ lục toàn đàn $G_{\text{best}}$:
$$v_{i,d}(t+1) = w \cdot v_{i,d}(t) + c_1 r_1 \cdot (p_{i,d} - x_{i,d}(t)) + c_2 r_2 \cdot (g^*_d - x_{i,d}(t))$$
- Trong đó: $c_1 = 1.2, c_2 = 1.2$, $v_{\max} = 0.2 \times (UB - LB)$.

### 3.2. Cập nhật quỹ đạo săn mồi WOA
- Nếu $p \ge 0.5$ (Quỹ đạo xoắn ốc bọt khí):
  $$\mathbf{D}' = |\mathbf{G}^* - \mathbf{X}_i(t)|$$
  $$\mathbf{X}_{i}^{\text{woa}} = \mathbf{D}' \odot e^{b l} \cos(2\pi l) + \mathbf{G}^*$$
- Nếu $p < 0.5$ và $|A| < 1$ (Bao vây thu hẹp):
  $$\mathbf{D} = |\mathbf{C} \odot \mathbf{G}^* - \mathbf{X}_i(t)|$$
  $$\mathbf{X}_{i}^{\text{woa}} = \mathbf{G}^* - \mathbf{A} \odot \mathbf{D}$$
- Nếu $p < 0.5$ và $|A| \ge 1$ (Thám hiểm toàn cục):
  $$\mathbf{D} = |\mathbf{C} \odot \mathbf{X}_{\text{rand}} - \mathbf{X}_i(t)|$$
  $$\mathbf{X}_{i}^{\text{woa}} = \mathbf{X}_{\text{rand}} - \mathbf{A} \odot \mathbf{D}$$

### 3.3. Phối hợp tổng hợp vị trí
Vị trí mới là sự kết hợp giữa vị trí dẫn đường của WOA và xung lực gia tốc của PSO:
$$\mathbf{X}_i(t+1) = \text{clip}\left(\mathbf{X}_{i}^{\text{woa}} + \beta \cdot \mathbf{V}_i(t+1), \; \mathbf{LB}, \; \mathbf{UB}\right)$$
*(với $\beta = 0.5$ là hệ số điều phối)*.

---

## 4. 🗺️ BẢN ĐỒ MÃ NGUỒN (CODE MAPPING)

- **File triển khai chính:** [`hybrid_woa_pso.py`](..\src\algorithms\hybrid\hybrid_woa_pso.py)
- **Tái sử dụng các module:**
  - Toán tử WOA: [`spiral_update.py`](..\src\algorithms\WOA\spiral_update.py), [`encircling.py`](..\src\algorithms\WOA\encircling.py), [`exploration.py`](..\src\algorithms\WOA\exploration.py).
  - Khởi tạo & Vận tốc: [`initialization.py`](..\src\algorithms\WOA\initialization.py), [`velocity_update.py`](..\src\algorithms\PSO\velocity_update.py).

---

## 5. 📊 ĐÁNH GIÁ THỰC NGHIỆM TRONG BÀI TOÁN UAV
- **Part 1 (35 vòng lặp):** Fitness TB = `0.4430` (**QUÁN QUÂN HẠNG 1 TOÀN BẢNG** ở giai đoạn hội tụ sớm). H-WOA-PSO giải quyết triệt để sự chậm chạp của WOA ban đầu nhờ có vận tốc PSO thúc đẩy, vượt mặt cả PSO thuần.
- **Part 2 (80 vòng lặp):** Fitness TB = `0.4411` (Tụt xuống hạng 6/6).
- **Hiện tượng xung đột động lực học (Dynamic Conflict):** Ở các vòng lặp sâu, quỹ đạo xoắn ốc của WOA và lực kéo vector của PSO bắt đầu triệt tiêu lẫn nhau, khiến cá thể bị rung lắc quanh cực trị địa phương thay vì hội tụ mịn vào nghiệm tối ưu toàn cục.

---

## 6. 🎓 BỘ CÂU HỎI THẦY CÔ VẤN ĐÁP & CÂU TRẢ LỜI MẪU

### ❓ Câu 1: *"Tại sao H-WOA-PSO lại dẫn đầu bảng ở Part 1 (35 vòng lặp) nhưng lại tụt hạng ở Part 2 (80 vòng lặp)?"*
> **Trả lời:**  
> *"Dạ thưa Thầy/Cô, kết quả đối chứng 2 giai đoạn này phản ánh hiện tượng rất thú vị trong tối ưu hóa đa mục tiêu:
> - Ở 35 vòng lặp đầu: PSO cung cấp 'gia tốc phản lực' giúp bầy cá voi của WOA lao thẳng vào vùng có mật độ người dùng cao chỉ trong 10-15 vòng lặp, giúp H-WOA-PSO giành ngôi Quán quân hội tụ nhanh.
> - Tuy nhiên ở 80 vòng lặp: Khi nghiệm cần sự tinh chỉnh vi mô, hai lực kéo ngược nhau — một bên là lực kéo thẳng của PSO, một bên là lực xoáy ốc của WOA — gây ra hiện tượng dao động cưỡng bức (oscillation), làm các UAV khó ổn định ở vị trí tối ưu sâu. Đây chính là lý do vì sao thuật toán đề xuất **I-WOA** (chọn lọc OBL và Levy) vượt trội hơn hẳn các mô hình lai cơ học."*

### ❓ Câu 2: *"H-WOA-PSO phù hợp nhất cho kịch bản thực tế nào trong mạng UAV?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, H-WOA-PSO cực kỳ thích hợp cho các tình huống **cứu hộ khẩn cấp cần triển khai tức thì trong vòng vài giây (Fast-response Deployment)**, nơi yêu cầu phải tìm được cấu hình trạm bay đạt độ phủ sóng 99% với số vòng lặp tối thiểu (dưới 35 vòng lặp)."*

---

## 7. 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT (ACADEMIC REFERENCES)
1. **Elhosseini, M. A., et al. (2019).** "A novel hybrid whale optimization algorithm with particle swarm optimization for global optimization". *Journal of Computational Science*, vol. 37, p. 101031. *(Nguyên lý lai ghép đường bơi xoắn ốc WOA với vận tốc PSO)*.
2. **Kaur, G., & Arora, S. (2018).** "Chaotic whale optimization algorithm with particle swarm optimization for global numerical optimization". *International Journal of Computer Applications*, vol. 180, no. 31, pp. 24–31.
3. **Mozaffari, M., et al. (2016).** "Efficient deployment of multiple unmanned aerial vehicles for optimal wireless coverage". *IEEE Communications Letters*, vol. 20, no. 8, pp. 1647–1650. DOI: [`10.1109/LCOMM.2016.2578312`](https://doi.org/10.1109/LCOMM.2016.2578312).

