# 🐋 DWWOA: TÀI LIỆU KỸ THUẬT & CÔNG THỨC THUẬT TOÁN BẦY CÁ VOI (WOA GỐC)

[Mục lục](README.md) · [Thuật ngữ](GLOSSARY.md) · [Mô hình chung](REPORT.md) · [Biến thể và study 100 vòng](NOTEBOOK_STUDY.md)

Trang này giải thích cơ chế baseline/bản đầy đủ. Các cờ K/O/L mới của GA/PSO và ablation bản lai được mô tả tại NOTEBOOK_STUDY; không suy ra hiệu quả thực nghiệm từ tên toán tử. Đọc mô hình và thuật ngữ trước, rồi xem thiết kế study sau chương này.


> Tài liệu phương pháp; các kết luận thực nghiệm cũ đã được rút. Không có bảng xếp hạng mới khi chưa có log FE. Mô hình chung: [REPORT.md](REPORT.md).

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

Trong các điều kiện dưới, ký hiệu |A| là cách viết tắt của độ lớn mà code dùng để chọn nhánh: norm(A)/sqrt(D), không phải kiểm tra riêng từng tọa độ. Best được giữ qua các vòng, không chỉ là max của quần thể hiện tại. Công thức lịch theo t áp dụng chế độ vòng lặp; ở chế độ FE, progress dùng FE đã tiêu thụ/max_fe. Xem [EXPERIMENT_DESIGN](EXPERIMENT_DESIGN.md).

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
  - $l \in [-1, 1]$: Xác định khoảng cách tương đối giữa cá voi và con mồi trên quỹ đạo xoắn. Khi $l \to 0$, hệ số tiến tới một; bước cộng vẫn chứa D', nên không bảo đảm vị trí tiến sát con mồi.

---

### 3.4. Cơ chế 3: Thám hiểm tìm mồi toàn cục (Search for Prey)
Được kích hoạt khi **$p < 0.5$** và **$|A| \ge 1$**. Thay vì hướng về con đầu đàn $\mathbf{X}^*$, cá voi sẽ bơi dạt ra xa theo một con cá voi ngẫu nhiên $\mathbf{X}_{\text{rand}}$ trong quần thể:

$$\mathbf{D} = \left| \mathbf{C} \odot \mathbf{X}_{\text{rand}} - \mathbf{X}_i(t) \right|$$
$$\mathbf{X}_i(t+1) = \mathbf{X}_{\text{rand}} - \mathbf{A} \odot \mathbf{D}$$

---

## 4. 🗺️ BẢN ĐỒ MÃ NGUỒN (CODE MAPPING)

| Thành phần thuật toán | File mã nguồn tương ứng | Hàm / Class chính |
| :--- | :--- | :--- |
| Cấu trúc cá thể cá voi | [`whale.py`](../src/algorithms/WOA/whale.py) | `class Whale` |
| Khởi tạo bầy cá voi | [`initialization.py`](../src/algorithms/WOA/initialization.py) | `initialize_whales()` |
| Cập nhật hệ số $a, A, C, l$ | [`coefficient_update.py`](../src/algorithms/WOA/coefficient_update.py) | `update_coefficients()` |
| Bao vây con mồi | [`encircling.py`](../src/algorithms/WOA/encircling.py) | `encircle_prey()` |
| Bơi xoắn ốc bọt khí | [`spiral_update.py`](../src/algorithms/WOA/spiral_update.py) | `spiral_update()` |
| Thám hiểm tìm mồi | [`exploration.py`](../src/algorithms/WOA/exploration.py) | `search_for_prey()` |
| Xử lý giới hạn biên | [`boundary_handler.py`](../src/algorithms/WOA/boundary_handler.py) | `handle_boundaries()` |
| Bộ điều khiển tối ưu hóa | [`optimizer.py`](../src/algorithms/WOA/optimizer.py) | `class WOAOptimizer.optimize()` |

---

## 5. Trạng thái thực nghiệm và diễn giải

Các số liệu và phần trả lời phản biện dựa trên kết quả cũ đã được rút khỏi tài liệu. Chưa có log benchmark theo FE để xác nhận thứ hạng hoặc quy nguyên nhân cho từng cơ chế. Không kết luận thuật toán này vượt thuật toán khác từ mô tả toán tử. Xem [báo cáo tổng hợp](REPORT.md), [ablation](ABLATION.md), [độ nhạy](SENSITIVITY.md) và [thống kê](STATISTICS.md).

## 7. Tài liệu tham khảo dự kiến — cần sinh viên tự xác minh

Danh mục kế thừa từ bản cũ; thông tin thư mục và mức độ phù hợp cần sinh viên tự đọc xác minh. Không coi các chú giải bên dưới là bằng chứng đã kiểm chứng hoặc nguồn của toàn bộ Fitness. Xem quy tắc trích dẫn trong [REPORT.md](REPORT.md).
1. **Mirjalili, S., & Lewis, A. (2016).** "The Whale Optimization Algorithm". *Advances in Engineering Software*, vol. 95, pp. 51–67. DOI: [`10.1016/j.advengsoft.2016.01.008`](https://doi.org/10.1016/j.advengsoft.2016.01.008). *(Bài báo gốc đề xuất thuật toán WOA và cơ chế săn mồi lưới bọt khí xoắn ốc)*.
2. **Mohammed, H., et al. (2020).** "A comprehensive survey on Whale Optimization Algorithm: Variants, applications, and hybridizations". *Neurocomputing*, vol. 410, pp. 397–433. DOI: [`10.1016/j.neucom.2020.04.110`](https://doi.org/10.1016/j.neucom.2020.04.110). *(Khảo sát hạn chế kẹt cực trị địa phương của WOA)*.
3. **Gharsallah, A., et al. (2021).** "Whale optimization algorithm for 3D deployment of UAV base stations in wireless communication systems". *Applied Soft Computing*, vol. 103, p. 107147. *(Ứng dụng WOA trong tối ưu hóa vị trí 3D UAV)*.

