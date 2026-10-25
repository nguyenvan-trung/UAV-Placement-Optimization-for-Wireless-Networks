# 🚀 DWI_WOA: TÀI LIỆU KỸ THUẬT & CÔNG THỨC THUẬT TOÁN I-WOA (ĐỀ XUẤT)

[Mục lục](README.md) · [Thuật ngữ](GLOSSARY.md) · [Mô hình chung](REPORT.md) · [Biến thể và study 100 vòng](NOTEBOOK_STUDY.md)

Trang này giải thích cơ chế baseline/bản đầy đủ. Các cờ K/O/L mới của GA/PSO và ablation bản lai được mô tả tại NOTEBOOK_STUDY; không suy ra hiệu quả thực nghiệm từ tên toán tử. Đọc mô hình và thuật ngữ trước, rồi xem thiết kế study sau chương này.


> Tài liệu phương pháp; các kết luận thực nghiệm cũ đã được rút. Không có bảng xếp hạng mới khi chưa có log FE. Mô hình chung: [REPORT.md](REPORT.md).

> **Mục đích:** Hướng dẫn toàn diện công thức toán học, cấu trúc mã nguồn, cơ chế cải tiến và kịch bản trả lời phản biện xuất sắc dành cho thuật toán **Improved Whale Optimization Algorithm (I-WOA)** — đóng góp khoa học cốt lõi của đề tài tối ưu hóa vị trí 3D trạm phát sóng UAV.

---

## 1. 💡 ĐỘNG LỰC NGHIÊN CỨU & 3 TRỤ CỘT CẢI TIẾN
I-WOA kết hợp K-Means, OBL và Lévy trên lõi WOA. Mục tiêu thiết kế là khảo sát ảnh hưởng của khởi tạo và đề xuất nghiệm bổ sung. Chưa có ablation theo FE để kết luận từng thành phần có lợi hoặc hiệu quả cộng dồn.

## 2. 🎯 BIỂU DIỄN NGHIỆM TRONG BÀI TOÁN UAV
Mỗi cá thể cá voi $\mathbf{X}_i$ mã hóa tọa độ 3D của $N = 4$ trạm phát sóng UAV:

$$\mathbf{X}_i = [x_1, y_1, z_1, \; x_2, y_2, z_2, \; x_3, y_3, z_3, \; x_4, y_4, z_4]^T \in \mathbb{R}^{12}$$

- Giới hạn không gian: $x_k, y_k \in [0, 1000]\text{ m}$, $z_k \in [50, 300]\text{ m}$.
- Hàm mục tiêu đánh giá chất lượng vị trí:
  $$\text{Fitness}(\mathbf{X}) = 0.6 \cdot f_1(\mathbf{X}) - 0.2 \cdot f_2(\mathbf{X}) - 0.2 \cdot f_3(\mathbf{X})$$

---

## 3. 📐 CÔNG THỨC TOÁN HỌC CÁC CƠ CHẾ CẢI TIẾN

### 3.1. Trụ cột 1: Khởi tạo định hướng theo phân cụm K-Means
Thay vì thả rơi 4 UAV ngẫu nhiên khắp khu vực $1\text{ km}^2$, I-WOA phân tích tọa độ của toàn bộ $M$ người dùng mặt đất $\mathcal{U} = \{(x_m, y_m)\}_{m=1}^M$ bằng thuật toán K-Means ($K = 4$ cụm):

- Phân hoạch người dùng thành 4 cụm $\mathcal{S}_1, \mathcal{S}_2, \mathcal{S}_3, \mathcal{S}_4$ tối thiểu hóa tổng bình phương khoảng cách:
  $$\arg\min_{\mathcal{S}} \sum_{k=1}^K \sum_{\mathbf{u} \in \mathcal{S}_k} \|\mathbf{u} - \mathbf{c}_k\|^2$$
- Tọa độ trọng tâm cụm thứ $k$:
  $$\mathbf{c}_k = (c_{x,k}, c_{y,k}) = \frac{1}{|\mathcal{S}_k|} \sum_{\mathbf{u} \in \mathcal{S}_k} \mathbf{u}$$
- Cá thể "hạt giống" đầu tiên $\mathbf{X}_{\text{seed}}$ được gán vào tâm cụm với độ cao gợi ý mặc định ($z_0 = 100\text{ m}$), rồi clip theo miền. Đây là lựa chọn khởi tạo, không phải độ cao đã chứng minh an toàn hoặc tối ưu:
  $$\mathbf{X}_{\text{seed}} = [c_{x,1}, c_{y,1}, 100, \; \dots, \; c_{x,4}, c_{y,4}, 100]^T$$
- Code khởi tạo cả quần thể ngẫu nhiên đều; chỉ thay cá thể đầu bằng gợi ý K-Means. Không sinh Gaussian quanh tâm cụm. Độ cao gợi ý được clip vào miền bài toán. Nguồn: `../src/preprocessing/kmeans_init.py` và `../src/algorithms/I_WOA/optimizer.py`.

---

### 3.2. Trụ cột 2: Cơ chế học đối kháng đa chiều (Opposition-Based Learning - OBL)
OBL tạo nghiệm đối xứng để đánh giá bổ sung; không bảo đảm nghiệm đối lập có chất lượng cao hơn:

- Với mỗi cá thể $\mathbf{X}_i = [x_{i,1}, \dots, x_{i,D}]^T$, vector đối lập $\mathbf{X}_i^{\text{op}}$ được định nghĩa:
  $$x_{i,d}^{\text{op}} = LB_d + UB_d - x_{i,d}, \quad \forall d \in \{1, \dots, D\}$$
- **Quy trình chọn lọc OBL:**
  1. Từ quần thể hiện tại $\mathcal{P} = \{\mathbf{X}_1, \dots, \mathbf{X}_{PopSize}\}$, sinh quần thể đối lập $\mathcal{P}^{\text{op}} = \{\mathbf{X}_1^{\text{op}}, \dots, \mathbf{X}_{PopSize}^{\text{op}}\}$.
  2. Giữ Fitness của quần thể gốc đã tính, chỉ đánh giá thêm $PopSize$ nghiệm đối lập rồi ghép $\mathcal{P}_{\text{all}} = \mathcal{P} \cup \mathcal{P}^{\text{op}}$.
  3. Sắp xếp giảm dần theo Fitness và chọn ra $PopSize$ cá thể ưu tú nhất:
     $$\mathcal{P}_{\text{new}} = \text{Top}_{PopSize}(\mathcal{P} \cup \mathcal{P}^{\text{op}})$$
- **Ý nghĩa hình học:** Với biên toàn miền [0,1000] m, tọa độ [0,200] m được phản chiếu sang [800,1000] m. Ví dụ chỉ mô tả phép đối xứng, không bảo đảm phủ toàn bộ miền. OBL động dùng biên quần thể nên không nhất thiết phản chiếu quanh tâm toàn miền.

---

### 3.3. Trụ cột 3: Đột biến bước nhảy phân phối đuôi nặng Levy Flight
Để khảo sát việc bổ sung đề xuất bước nhảy, I-WOA áp dụng toán tử đột biến **Levy Flight** (dựa trên thuật toán Mantegna):

- **Độ lệch chuẩn Mantegna $\sigma_u$:**
  $$\sigma_u = \left( \frac{\Gamma(1 + \beta) \cdot \sin\left(\frac{\pi \beta}{2}\right)}{\Gamma\left(\frac{1 + \beta}{2}\right) \cdot \beta \cdot 2^{\frac{\beta - 1}{2}}} \right)^{\frac{1}{\beta}}, \quad \text{với } \beta = 1.5$$
- **Sinh bước nhảy ngẫu nhiên $s$:**
  $$u \sim \mathcal{N}(0, \sigma_u^2), \quad v \sim \mathcal{N}(0, 1)$$
  $$s = \frac{u}{|v|^{1/\beta}}$$
- **Cập nhật vị trí đột biến bứt phá:**
  $$\mathbf{X}_i^{\text{new}} = \mathbf{X}_i + \alpha \cdot \mathbf{s} \odot \boldsymbol{\Delta}_i$$
  Trong đó:
  - $\alpha = 0.05$: Hệ số kích thước bước nhảy (Step size scaling).
  - $\boldsymbol{\Delta}_i$: Vector độ lệch định hướng:
    $$\boldsymbol{\Delta}_i = \begin{cases} \mathbf{X}_i - \mathbf{X}^* & \text{nếu từng tọa độ có } |X_{i,d}-X^*_d| > 10^{-3} \\ 0.1 \times (\mathbf{UB} - \mathbf{LB}) & \text{nếu bầy đã quá gần hội tụ (kích hoạt nhảy vùng)} \end{cases}$$
- **Đặc trưng:** Phân phối Lévy có đuôi nặng, cho phép có bước nhảy dài; không bảo đảm thoát mọi cực trị. Code kích hoạt theo xác suất levy_rate=0,3, không có bộ phát hiện chắc chắn “đang kẹt”; chỉ nhận đề xuất nếu cải thiện ứng viên. Dynamic OBL có xác suất 0,2 mỗi vòng khi bật.

---

## 4. 🗺️ BẢN ĐỒ MÃ NGUỒN (CODE MAPPING)

| Module cải tiến | File mã nguồn tương ứng | Hàm / Class chính |
| :--- | :--- | :--- |
| Phân cụm K-Means khởi tạo | [`kmeans_init.py`](../src/preprocessing/kmeans_init.py) | `generate_kmeans_uav_initial_guess()` |
| Cơ chế học đối kháng (OBL) | [`obl.py`](../src/algorithms/I_WOA/obl.py) | `generate_opposite_position()`, `apply_obl_population()` |
| Bước nhảy Levy Flight | [`levy_flight.py`](../src/algorithms/I_WOA/levy_flight.py) | `compute_levy_sigma()`, `apply_levy_flight()` |
| Tham số I-WOA | [`parameters.py`](../src/algorithms/I_WOA/parameters.py) | `class IWOAParameters` |
| Bộ điều khiển I-WOA | [`optimizer.py`](../src/algorithms/I_WOA/optimizer.py) | `class IWOAOptimizer.optimize()` |

---

## 5. Trạng thái thực nghiệm và diễn giải

Các số liệu và phần trả lời phản biện dựa trên kết quả cũ đã được rút khỏi tài liệu. Chưa có log benchmark theo FE để xác nhận thứ hạng hoặc quy nguyên nhân cho từng cơ chế. Không kết luận thuật toán này vượt thuật toán khác từ mô tả toán tử. Xem [báo cáo tổng hợp](REPORT.md), [ablation](ABLATION.md), [độ nhạy](SENSITIVITY.md) và [thống kê](STATISTICS.md).

## 7. Tài liệu tham khảo dự kiến — cần sinh viên tự xác minh

Danh mục kế thừa từ bản cũ; thông tin thư mục và mức độ phù hợp cần sinh viên tự đọc xác minh. Không coi các chú giải bên dưới là bằng chứng đã kiểm chứng hoặc nguồn của toàn bộ Fitness. Xem quy tắc trích dẫn trong [REPORT.md](REPORT.md).
1. **Mirjalili, S., & Lewis, A. (2016).** "The Whale Optimization Algorithm". *Advances in Engineering Software*, vol. 95, pp. 51–67. DOI: [`10.1016/j.advengsoft.2016.01.008`](https://doi.org/10.1016/j.advengsoft.2016.01.008). *(Thuật toán nền tảng WOA)*.
2. **Tizhoosh, H. R. (2005).** "Opposition-Based Learning: A New Scheme for Machine Intelligence". *IEEE CIMCA Proceedings*, pp. 695–701. DOI: [`10.1109/CIMCA.2005.1631345`](https://doi.org/10.1109/CIMCA.2005.1631345). *(Cơ sở toán học cho toán tử OBL trong `obl.py`)*.
3. **Mantegna, R. N. (1994).** "Fast, accurate algorithm for numerical simulation of Lévy stable stochastic processes". *Physical Review E*, vol. 49, no. 5, pp. 4677–4683. DOI: [`10.1103/PhysRevE.49.4677`](https://doi.org/10.1103/PhysRevE.49.4677). *(Thuật toán Mantegna tính $\sigma_u$ cho bước nhảy Levy trong `levy_flight.py`)*.
4. **Yang, X. S., & Deb, S. (2009).** "Cuckoo Search via Lévy Flights". *IEEE NaBIC Proceedings*, pp. 210–214. DOI: [`10.1109/NABIC.2009.5393690`](https://doi.org/10.1109/NABIC.2009.5393690). *(Ứng dụng bước nhảy Levy trong tối ưu hóa metaheuristics)*.
5. **Ling, Y., Zhou, Y., & Luo, Q. (2017).** "Lévy Flight Trajectory-Based Whale Optimization Algorithm for Global Optimization". *IEEE Access*, vol. 5, pp. 6168–6186. DOI: [`10.1109/ACCESS.2017.2695498`](https://doi.org/10.1109/ACCESS.2017.2695498). *(Chứng minh Levy Flight giải quyết bài toán kẹt cực trị của WOA)*.
6. **Lyu, J., Zeng, Y., Zhang, R., & Lim, T. J. (2017).** "Placement optimization of UAV-mounted mobile base stations". *IEEE Communications Letters*, vol. 21, no. 3, pp. 604–607. DOI: [`10.1109/LCOMM.2016.2633342`](https://doi.org/10.1109/LCOMM.2016.2633342). *(K-Means định hướng vị trí trạm bay UAV)*.

