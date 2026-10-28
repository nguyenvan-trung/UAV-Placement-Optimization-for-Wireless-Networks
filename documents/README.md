# Danh mục tài liệu tham khảo cần đọc và xác minh

## Mục lục

1. [📑 Danh mục các nhóm tài liệu](#doc-section-01)
2. [📡 1. Mô hình Kênh truyền Vô tuyến & Tối ưu hóa vị trí UAV 3D (Foundation)](#doc-section-02)
3. [🐋 2. Thuật toán Bầy cá voi (WOA) & Cải tiến (I-WOA) (Core Contribution)](#doc-section-03)
4. [🦅 3. Tối ưu hóa bầy đàn (PSO) & Thuật toán bầy đàn (Benchmark)](#doc-section-04)
5. [🧬 4. Thuật toán Di truyền (GA - Genetic Algorithms)](#doc-section-05)
6. [🔀 5. Các kỹ thuật lai ghép Metaheuristic (Hybrid Methods)](#doc-section-06)
7. [🔍 Hướng dẫn tải tài liệu nhanh:](#doc-section-07)


[Trang đầu](../README.md) · [Mục lục kỹ thuật](../implementation/docs/README.md) · [Mô hình thực sự triển khai](../implementation/docs/REPORT.md) · [Nguồn theo công thức](../implementation/docs/SOURCES.md)

SOURCES chỉ rõ phần đã đối chiếu, giới hạn truy cập toàn văn và công thức riêng. Danh mục mở rộng dưới đây không thay bảng truy nguồn cho từng phương trình.

Danh mục kế thừa phục vụ tìm nguồn, chưa phải xác nhận đã kiểm tra toàn văn/DOI của mọi mục. Các chú giải chỉ nêu hướng liên hệ cần đối chiếu; không dùng một bài báo như chứng cứ cho toàn bộ fitness, trọng số hoặc thứ hạng dự án. Lượt chỉnh tài liệu này không tải/đọc lại bài báo bên ngoài.

Khi dùng một nguồn, ghi rõ công thức/trang được kế thừa, phần nhóm tự thiết kế và khác biệt với code. C/E/I hiện tại có các proxy riêng; đặc biệt I không phải diện tích giao nhau. Xem [FITNESS_AUDIT](../implementation/docs/FITNESS_AUDIT.md) và [REPORT_EVIDENCE](../implementation/docs/REPORT_EVIDENCE.md).

> **Dự án:** Tối ưu hóa vị trí 3D trạm phát sóng UAV trong mạng không dây 5G sử dụng thuật toán bầy cá voi cải tiến (I-WOA)  
> **Hướng dẫn tải:** Bạn có thể copy tên bài báo hoặc mã DOI dán vào [Google Scholar](https://scholar.google.com/), [IEEE Xplore](https://ieeexplore.ieee.org/), hoặc [ResearchGate](https://www.researchgate.net/) để tải file PDF toàn văn.

---

<a id="doc-section-01"></a>

## 📑 Danh mục các nhóm tài liệu

- [1. Mô hình kênh và vị trí UAV](#foundation)
- [2. WOA và các cơ chế cải tiến](#woa)
- [3. PSO](#pso)
- [4. GA](#ga)
- [5. Thuật toán lai](#hybrid)

---

<a id="foundation"></a>

<a id="doc-section-02"></a>

## 📡 1. Mô hình Kênh truyền Vô tuyến & Tối ưu hóa vị trí UAV 3D (Foundation)

Đây là các bài báo kinh điển đặt nền móng cho mô hình vật lý vô tuyến ($P_{\text{LoS}}$, Path Loss, SNR) và bài toán bố trí trạm bay UAV trong đề tài:

### [1.1] Optimal LAP Altitude for Maximum Coverage (Bài báo quan trọng nhất về kênh Al-Hourani)
- **Tác giả:** A. Al-Hourani, S. Kandeepan, and S. Lardner
- **Tạp chí:** *IEEE Wireless Communications Letters*, vol. 3, no. 6, pp. 569–572, Dec. 2014.
- **DOI:** [`10.1109/LWC.2014.2342736`](https://doi.org/10.1109/LWC.2014.2342736)
- **Đóng góp vào đề tài:** Cung cấp hàm xác suất nhìn thẳng tầm mắt $P_{\text{LoS}}(\theta) = \frac{1}{1 + a \exp(-b(\theta - a))}$ và các tham số môi trường đô thị ($a=9.61, b=0.16, \eta_{\text{LoS}}=1.0\text{ dB}, \eta_{\text{NLoS}}=20.0\text{ dB}$) được cài đặt trong `src/physics/channel.py`.

### [1.2] Efficient Deployment of Multiple Unmanned Aerial Vehicles for Optimal Wireless Coverage
- **Tác giả:** M. Mozaffari, W. Saad, M. Bennis, and M. Debbah
- **Tạp chí:** *IEEE Communications Letters*, vol. 20, no. 8, pp. 1647–1650, Aug. 2016.
- **DOI:** [`10.1109/LCOMM.2016.2578312`](https://doi.org/10.1109/LCOMM.2016.2578312)
- **Hướng đối chiếu:** Bố trí nhiều UAV và mô hình nhiễu/vùng phủ. Không đồng nhất diện tích chồng lấn của bài báo với f3 hiện tại, vốn đếm tỷ lệ user có từ hai liên kết SNR đạt ngưỡng.

### [1.3] A Tutorial on UAVs for Wireless Networks: Applications, Challenges, and Open Problems
- **Tác giả:** M. Mozaffari, W. Saad, M. Bennis, Y.-H. Nam, and M. Debbah
- **Tạp chí:** *IEEE Communications Surveys & Tutorials*, vol. 21, no. 3, pp. 2334–2360, 2019.
- **DOI:** [`10.1109/COMST.2019.2902862`](https://doi.org/10.1109/COMST.2019.2902862)
- **Đóng góp vào đề tài:** Khảo sát bối cảnh ứng dụng UAV 5G cứu trợ thảm họa (Disaster Relief) và bổ sung dung lượng điểm nóng (Hotspot Capacity Injection).

### [1.4] Wireless Communications with Unmanned Aerial Vehicles: Opportunities and Challenges
- **Tác giả:** Y. Zeng, R. Zhang, and T. J. Lim
- **Tạp chí:** *IEEE Communications Magazine*, vol. 54, no. 5, pp. 36–42, May 2016.
- **DOI:** [`10.1109/MCOM.2016.7470933`](https://doi.org/10.1109/MCOM.2016.7470933)

---

<a id="woa"></a>

<a id="doc-section-03"></a>

## 🐋 2. Thuật toán Bầy cá voi (WOA) & Cải tiến (I-WOA) (Core Contribution)

### [2.1] The Whale Optimization Algorithm (Bài báo gốc của WOA)
- **Tác giả:** Seyedali Mirjalili and Andrew Lewis
- **Tạp chí:** *Advances in Engineering Software*, vol. 95, pp. 51–67, 2016.
- **DOI:** [`10.1016/j.advengsoft.2016.01.008`](https://doi.org/10.1016/j.advengsoft.2016.01.008)
- **Đóng góp vào đề tài:** Cơ sở lý thuyết cho 3 toán tử: Bao vây con mồi ($|A|<1$), Bơi xoắn ốc bọt khí logarithmic ($p \ge 0.5$) và Thám hiểm toàn cục ($|A| \ge 1$), triển khai trong `src/algorithms/WOA/`.

### [2.2] Opposition-Based Learning: A New Scheme for Machine Intelligence (Cơ chế OBL)
- **Tác giả:** Hamid R. Tizhoosh
- **Hội nghị:** *International Conference on Computational Intelligence for Modelling, Control and Automation (CIMCA)*, 2005.
- **DOI:** [`10.1109/CIMCA.2005.1631345`](https://doi.org/10.1109/CIMCA.2005.1631345)
- **Đóng góp vào đề tài:** Công thức tạo nghiệm đối xứng $X^{\text{op}} = LB + UB - X$, giúp I-WOA mở rộng không gian tìm kiếm đối xứng, chống lệch góc bản đồ (`src/algorithms/I_WOA/obl.py`).

### [2.3] Cuckoo Search via Lévy Flights (Cơ chế Mantegna's Levy Flight)
- **Tác giả:** Xin-She Yang and Suash Deb
- **Hội nghị:** *World Congress on Nature & Biologically Inspired Computing (NaBIC)*, pp. 210–214, 2009.
- **DOI:** [`10.1109/NABIC.2009.5393690`](https://doi.org/10.1109/NABIC.2009.5393690)
- **Đóng góp vào đề tài:** Thuật toán Mantegna tính bước nhảy phân phối đuôi nặng (Heavy-tailed Levy distribution), cho phép I-WOA bứt phá văng khỏi các cực trị địa phương (`src/algorithms/I_WOA/levy_flight.py`).

### [2.4] Lévy Flight Trajectory-Based Whale Optimization Algorithm for Global Optimization
- **Tác giả:** Y. Ling, Y. Zhou, and Q. Luo
- **Tạp chí:** *IEEE Access*, vol. 5, pp. 6168–6186, 2017.
- **DOI:** [`10.1109/ACCESS.2017.2695498`](https://doi.org/10.1109/ACCESS.2017.2695498)
- **Hướng đối chiếu:** Biến thể WOA dùng Lévy; cần đọc điều kiện thí nghiệm và cách triển khai trước khi liên hệ với dự án. Không suy ra bảo đảm thoát mọi cực trị hoặc ưu thế của study chưa chạy.

---

<a id="pso"></a>

<a id="doc-section-04"></a>

## 🦅 3. Tối ưu hóa bầy đàn (PSO) & Thuật toán bầy đàn (Benchmark)

### [3.1] Particle Swarm Optimization (Bài báo phát minh PSO)
- **Tác giả:** James Kennedy and Russell Eberhart
- **Hội nghị:** *Proceedings of ICNN'95 - International Conference on Neural Networks*, vol. 4, pp. 1942–1948, 1995.
- **DOI:** [`10.1109/ICNN.1995.488968`](https://doi.org/10.1109/ICNN.1995.488968)
- **Đóng góp vào đề tài:** Phương trình vận tốc bầy đàn hướng về $P_{\text{best}}$ và $G_{\text{best}}$ cài đặt trong `src/algorithms/PSO/velocity_update.py`.

### [3.2] A Modified Particle Swarm Optimizer (Trọng số quán tính w)
- **Tác giả:** Yuhui Shi and Russell Eberhart
- **Hội nghị:** *IEEE International Conference on Evolutionary Computation (ICEC)*, pp. 69–73, 1998.
- **DOI:** [`10.1109/ICEC.1998.699146`](https://doi.org/10.1109/ICEC.1998.699146)
- **Đóng góp vào đề tài:** Giới thiệu trọng số quán tính $w = 0.7$ điều hòa khả năng bay của hạt.

---

<a id="ga"></a>

<a id="doc-section-05"></a>

## 🧬 4. Thuật toán Di truyền (GA - Genetic Algorithms)

### [4.1] Adaptation in Natural and Artificial Systems
- **Tác giả:** John H. Holland
- **Nhà xuất bản:** *University of Michigan Press (1975) / MIT Press (1992)*.
- **Ý nghĩa:** Khởi nguồn của lý thuyết thuật toán tiến hóa (Evolutionary Computation) và toán tử chọn lọc tự nhiên.

### [4.2] Real-Coded Genetic Algorithms for Continuous Global Optimization
- **Tác giả:** F. Herrera, M. Lozano, and J. L. Verdegay
- **Tạp chí:** *Artificial Intelligence Review*, vol. 12, pp. 265–325, 1998.
- **DOI:** [`10.1023/A:1006504901164`](https://doi.org/10.1023/A:1006504901164)
- **Đóng góp vào đề tài:** Cơ sở cho phép lai ghép số học tổ hợp lồi (Arithmetic Crossover) trong không gian số thực 12D (`src/algorithms/GA/crossover.py`).

---

<a id="hybrid"></a>

<a id="doc-section-06"></a>

## 🔀 5. Các kỹ thuật lai ghép Metaheuristic (Hybrid Methods)

### [5.1] Hybridizing Particle Swarm Optimization with Genetic Algorithm
- **Tác giả:** Y.-T. Juang, C.-M. Lu, et al.
- **Tạp chí:** *IEEE Transactions on Systems, Man, and Cybernetics*, 2004 / 2008.
- **Đóng góp vào đề tài:** Ý tưởng lai ghép H-PSO-GA: dùng PSO hội tụ nhanh ở pha đầu và dùng lai ghép/đột biến GA để phục hồi tính đa dạng khi bầy hạt bị kẹt (`src/algorithms/hybrid/hybrid_pso_ga.py`).

### [5.2] A Hybrid Whale Optimization Algorithm with Particle Swarm Optimization
- **Tác giả:** M. A. Elhosseini et al.
- **Tạp chí:** *Journal of Computational Science*, 2019.
- **Hướng đối chiếu:** Ý tưởng kết hợp WOA và PSO; phiên bản triển khai riêng được mô tả trong [DWH_WOA_PSO](../implementation/docs/DWH_WOA_PSO.md). Không có kết luận thứ hạng mới khi chưa có log study.

---

<a id="doc-section-07"></a>

## 🔍 Hướng dẫn tải tài liệu nhanh:
1. Mở trang tìm kiếm [Google Scholar](https://scholar.google.com/).
2. Copy tiêu đề bài báo (ví dụ: *"Optimal LAP Altitude for Maximum Coverage"*) và nhấn Tìm kiếm.
3. Nhấp vào liên kết PDF bên tay phải để tải bài báo về máy.
4. Bạn có thể lưu các file PDF tải được vào các thư mục con tương ứng:
   - `documents/GA/`: Các bài báo về GA
   - `documents/PSO/`: Các bài báo về PSO
   - `documents/WOA/`: Các bài báo về WOA
   - `documents/I_WOA/`: Các bài báo về I-WOA, OBL và Levy Flight
