# 🐋🦅 DWH_WOA_PSO: TÀI LIỆU KỸ THUẬT & CÔNG THỨC THUẬT TOÁN LAI H-WOA-PSO

[Mục lục](README.md) · [Thuật ngữ](GLOSSARY.md) · [Mô hình chung](REPORT.md) · [Biến thể và study 100 vòng](NOTEBOOK_STUDY.md)

Trang này giải thích cơ chế baseline/bản đầy đủ. Các cờ K/O/L mới của GA/PSO và ablation bản lai được mô tả tại NOTEBOOK_STUDY; không suy ra hiệu quả thực nghiệm từ tên toán tử. Đọc mô hình và thuật ngữ trước, rồi xem thiết kế study sau chương này.


> Tài liệu phương pháp; các kết luận thực nghiệm cũ đã được rút. Không có bảng xếp hạng mới khi chưa có log FE. Mô hình chung: [REPORT.md](REPORT.md).

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
 │    x_new = clip(0.5*x_woa + 0.5*(x+v), LB, UB)          │
 └──────────────────────────┬─────────────────────────────┘
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ 4. ĐÁNH GIÁ FITNESS & CẬP NHẬT pbest, gbest            │
 └────────────────────────────────────────────────────────┘
```

---

## 3. 📐 CÔNG THỨC TOÁN HỌC CỐT LÕI

Mỗi cá thể thực hiện cả đề xuất WOA và bước vận tốc PSO trước khi trộn, không chia đôi quần thể. Điều kiện |A| trong nhánh WOA được code tính bằng norm(A)/sqrt(D). Các case bỏ pbest/gbest chỉ tắt lực hút tương ứng trong vận tốc; nhánh WOA vẫn giữ best. Xem [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md).

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
$$\mathbf{X}_i(t+1) = \text{clip}\left((1-\beta) \mathbf{X}_{i}^{\text{woa}} + \beta (\mathbf{X}_i(t)+\mathbf{V}_i(t+1)), \; \mathbf{LB}, \; \mathbf{UB}\right)$$
*(với $\beta = 0.5$ là hệ số điều phối)*.

---

## 4. 🗺️ BẢN ĐỒ MÃ NGUỒN (CODE MAPPING)

- **File triển khai chính:** [`hybrid_woa_pso.py`](../src/algorithms/hybrid/hybrid_woa_pso.py)
- **Tái sử dụng các module:**
  - Toán tử WOA: [`spiral_update.py`](../src/algorithms/WOA/spiral_update.py), [`encircling.py`](../src/algorithms/WOA/encircling.py), [`exploration.py`](../src/algorithms/WOA/exploration.py).
  - Khởi tạo & Vận tốc: [`initialization.py`](../src/algorithms/WOA/initialization.py), [`velocity_update.py`](../src/algorithms/PSO/velocity_update.py).

---

## 5. Trạng thái thực nghiệm và diễn giải

Các số liệu và phần trả lời phản biện dựa trên kết quả cũ đã được rút khỏi tài liệu. Chưa có log benchmark theo FE để xác nhận thứ hạng hoặc quy nguyên nhân cho từng cơ chế. Không kết luận thuật toán này vượt thuật toán khác từ mô tả toán tử. Xem [báo cáo tổng hợp](REPORT.md), [ablation](ABLATION.md), [độ nhạy](SENSITIVITY.md) và [thống kê](STATISTICS.md).

## 7. Tài liệu tham khảo dự kiến — cần sinh viên tự xác minh

Danh mục kế thừa từ bản cũ; thông tin thư mục và mức độ phù hợp cần sinh viên tự đọc xác minh. Không coi các chú giải bên dưới là bằng chứng đã kiểm chứng hoặc nguồn của toàn bộ Fitness. Xem quy tắc trích dẫn trong [REPORT.md](REPORT.md).
1. **Elhosseini, M. A., et al. (2019).** "A novel hybrid whale optimization algorithm with particle swarm optimization for global optimization". *Journal of Computational Science*, vol. 37, p. 101031. *(Nguyên lý lai ghép đường bơi xoắn ốc WOA với vận tốc PSO)*.
2. **Kaur, G., & Arora, S. (2018).** "Chaotic whale optimization algorithm with particle swarm optimization for global numerical optimization". *International Journal of Computer Applications*, vol. 180, no. 31, pp. 24–31.
3. **Mozaffari, M., et al. (2016).** "Efficient deployment of multiple unmanned aerial vehicles for optimal wireless coverage". *IEEE Communications Letters*, vol. 20, no. 8, pp. 1647–1650. DOI: [`10.1109/LCOMM.2016.2578312`](https://doi.org/10.1109/LCOMM.2016.2578312).

