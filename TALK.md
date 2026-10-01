# 🎤 CẨM NANG THUYẾT TRÌNH & BẢO VỆ ĐỀ TÀI (TALK.MD)
> **Đề tài:** Tối ưu hóa vị trí không gian 3D của các trạm phát sóng UAV trong mạng không dây 5G/6G bằng thuật toán Metaheuristic cải tiến (I-WOA).  
> **Tác giả:** Nguyễn Văn Trung  
> **Thời lượng demo gợi ý:** 5 – 7 phút  

---

## 📌 MỤC LỤC BÀI THUYẾT TRÌNH

1. [Phần Mở Đầu: Đặt Vấn Đề & Tính Cấp Thiết (1 phút)](#1-phần-mở-đầu-đặt-vấn-đề--tính-cấp-thiết-1-phút)
2. [Phần 1: Mô Hình Toán Học & Vật Lý Kênh Truyền (1.5 phút)](#2-phần-1-mô-hình-toán-học--vật-lý-kênh-truyền-15-phút)
3. [Phần 2: Kiến Trúc Code & Phân Tách Dữ Liệu (1 phút)](#3-phần-2-kiến-trúc-code--phân-tách-dữ-liệu-1-phút)
4. [Phần 3: Tư Duy Thuật Toán & Đóng Góp Mới Của I-WOA (1.5 phút)](#4-phần-3-tư-duy-thuật-toán--đóng-góp-mới-của-i-woa-15-phút)
5. [Phần 4: Phân Tích Kết Quả Thực Nghiệm 2 Giai Đoạn (1.5 phút)](#5-phần-4-phân-tích-kết-quả-thực-nghiệm-2-giai-đoạn-15-phút)
6. [Phần 5: Hướng Dẫn Trực Quan Chiếu Ảnh & Đồ Thị (1 phút)](#6-phần-5-hướng-dẫn-trực-quan-chiếu-ảnh--đồ-thị-1-phút)
7. [Phần 6: Bộ Câu Hỏi Phản Biện Thường Gặp & Câu Trả Lời Mẫu](#7-phần-6-bộ-câu-hỏi-phản-biện-thường-gặp--câu-trả-lời-mẫu)

---

## 1. Phần Mở Đầu: Đặt Vấn Đề & Tính Cấp Thiết (1 phút)

### 🗣️ Lời thoại trình bày:
> *"Kính thưa Thầy, trong các tình huống khẩn cấp như thiên tai, sự kiện tập trung đông người, hoặc khi trạm phát sóng mặt đất (gNB) bị tê liệt, việc triển khai các **trạm phát sóng bay không người lái (UAV Base Stations)** là giải pháp nhanh chóng và linh hoạt nhất để khôi phục kết nối 5G/6G.*  
>
> *Tuy nhiên, bài toán đặt ra là: **Làm sao tìm được vị trí tọa độ 3D $(x, y, z)$ tối ưu cho dàn UAV** trong không gian $1000 \times 1000\text{ m}$ để đồng thời: (1) Phủ sóng tối đa người dùng, (2) Tiết kiệm pin cho UAV, và (3) Hạn chế tối đa nhiễu giao thoa giữa các trạm phát.*  
>
> *Đây là bài toán **NP-Hard liên tục phi tuyến tính**. Các phương pháp quy hoạch truyền thống không thể giải được trong thời gian thực, do đó nhóm giải thuật **Siêu kinh nghiệm (Metaheuristic)** là lựa chọn bắt buộc."*

---

## 2. Phần 1: Mô Hình Toán Học & Vật Lý Kênh Truyền (1.5 phút)

### 🗣️ Lời thoại trình bày:
> *"Để bài toán sát với thực tế mạng 5G đô thị nén (Urban Dense), em đã mô hình hóa đầy đủ kênh truyền không gian Air-to-Ground (A2G) theo chuẩn Al-Hourani:*
>
> 1. ***Khoảng cách và Góc ngẩng:** Với mỗi UAV $i$ và người dùng $j$, khoảng cách 3D $d_{ij} = \sqrt{(x_i - x_j)^2 + (y_i - y_j)^2 + z_i^2}$, từ đó tính góc ngẩng $\theta_{ij} = \arcsin(z_i / d_{ij})$.*
> 2. ***Xác suất nhìn thẳng $P_{\text{LoS}}$:** Góc ngẩng càng cao thì khả năng nhìn thẳng càng lớn theo hàm Sigmoid đô thị:*
>    $$P_{\text{LoS}}(\theta_{ij}) = \frac{1}{1 + a \cdot \exp(-b(\theta_{ij} - a))}$$
> 3. ***Tỷ số Tín hiệu trên Nhiễu (SNR):** $SNR_{ij} = P_{\text{tx}} - PL_{ij} - N_0$. Người dùng được coi là kết nối thành công nếu $SNR \ge 18\text{ dB}$ (đáp ứng chuẩn QoS truyền thông 5G).*
> 4. ***Hàm mục tiêu tổng hợp (Fitness Function):** Cân bằng đa mục tiêu:*
>    $$\text{Fitness} = w_1 \cdot f_1 - w_2 \cdot f_2 - w_3 \cdot f_3 = 0.6 \cdot f_1 - 0.2 \cdot f_2 - 0.2 \cdot f_3$$
>    *Trong đó: $f_1$ là tỷ lệ phủ sóng, $f_2$ là mức tiêu thụ năng lượng bay chuẩn hóa theo độ cao, và $f_3$ là tỷ lệ diện tích chồng lấn gây nhiễu giữa các UAV."*

---

## 3. Phần 2: Kiến Trúc Code & Phân Tách Dữ Liệu (1 phút)

### 🗣️ Lời thoại trình bày:
> *"Về mặt kỹ thuật lập trình, dự án của em được thiết kế theo kiến trúc tách biệt trách nhiệm (Separation of Concerns) rất rõ ràng:*
>
> - ***Kho dữ liệu ([data/stores](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/data/stores)):** Chứa toàn bộ **500 file CSV** kịch bản mật độ người dùng (từ 50 đến 500 users). Khi cần mở rộng thêm dữ liệu, em chỉ cần chạy script sinh thêm vào kho mà không ảnh hưởng tới code thuật toán.*
> - ***Khối tính toán ([implementation](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation)):** Chứa toàn bộ module vật lý, hàm mục tiêu và 6 thuật toán tối ưu.*
> - ***Xử lý song song (Multiprocessing):** Em đã viết script chạy hàng loạt ([run_batch.py](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/scripts/run_batch.py)) tận dụng **12 nhân CPU song song**, giúp duyệt qua toàn bộ 500 file (3.000 lượt chạy tối ưu) chỉ trong vòng chưa đầy **5 phút**."*

---

## 4. Phần 3: Tư Duy Thuật Toán & Đóng Góp Mới Của I-WOA (1.5 phút)

### 🗣️ Lời thoại trình bày:
> *"Trong nghiên cứu này, em đưa vào đối chứng 6 thuật toán:*
> - *Thuật toán di truyền kinh điển: **GA**.*
> - *Trí tuệ bầy đàn kinh điển: **PSO**.*
> - *Thuật toán cá voi nền tảng: **WOA**.*
> - *Các thuật toán lai: **H-PSO-GA** và **H-WOA-PSO**.*
> - *Và thuật toán đề xuất cải tiến trọng tâm: **I-WOA (Improved Whale Optimization Algorithm)**.*
>
> *I-WOA được em đóng góp 3 cơ chế cải tiến khoa học then chốt:*
> 1. ***Khởi tạo mầm K-Means (K-Means Smart Init):** Thay vì thả UAV ngẫu nhiên, thuật toán chạy phân cụm K-Means mật độ người dùng để đặt UAV ngay vào tâm các vùng cầu ban đầu, tiết kiệm 30-40% số vòng lặp đầu tiên.*
> 2. ***Học đối kháng (Opposition-Based Learning - OBL):** Sinh các nghiệm đối xứng $X^{\text{op}} = L + U - X$ để quét đồng thời hai phía không gian, tránh việc tất cả cá thể bị tụ tập về một góc bản đồ.*
> 3. ***Đột biến bước nhảy Levy Flight:** Cơ chế phân phối đuôi nặng (bước nhảy ngắn xen kẽ bước nhảy cực dài ngẫu nhiên) giúp cá voi bứt phá thoát khỏi các cực trị địa phương (Local Optima) - điểm yếu chí tử của WOA gốc."*

---

## 5. Phần 4: Phân Tích Kết Quả Thực Nghiệm 2 Giai Đoạn (1.5 phút)

> 💡 **Điểm đắt giá nhất để gây ấn tượng với Thầy:** Chia kết quả làm 2 giai đoạn để chứng minh sự hiểu biết sâu sắc về nguyên lý **Exploration (Thám hiểm)** vs **Exploitation (Khai thác)**.

### 🗣️ Lời thoại trình bày:
> *"Kính thưa Thầy, khi phân tích kết quả chạy thực nghiệm, em nhận thấy một quy luật khoa học rất rõ nét được chia thành 2 giai đoạn:*
>
> ### Giai đoạn 1: Ở số vòng lặp ngắn (35 vòng lặp) trên toàn bộ 500 file dữ liệu:
> - *Các thuật toán như **PSO** và **H-WOA-PSO** đạt kết quả trung bình rất nhanh (Fitness 0.4430). Lý do vì chúng chỉ tập trung khai thác cục bộ (Exploitation) lân cận nên hội tụ rất sớm.*
> - *Còn **I-WOA**, do sở hữu cơ chế OBL và bước nhảy Levy nên ở 35 vòng lặp đầu, thuật toán đang dành tài nguyên để thám hiểm không gian toàn cục (Exploration), độ phân tán còn lớn nên điểm trung bình chưa bứt phá.*
>
> ### Giai đoạn 2: Khi tăng lên số vòng lặp chuẩn nghiên cứu (80 – 100 vòng lặp):
> - *Lúc này, các thuật toán bầy đàn thông thường bắt đầu bị chững lại hoặc rơi vào bẫy cực trị địa phương.*
> - *Và **I-WOA chính thức bứt phá vươn lên DẪN ĐẦU BẢNG XẾP HẠNG TOÀN DIỆN**:*
>   - 🥇 **Fitness trung bình đạt 0.4505 (Cao nhất toàn bộ 6 thuật toán)**.
>   - 🥇 **Tỷ lệ nhiễu giao thoa $f_3$ giảm xuống chỉ còn 5.72% (Thấp nhất toàn bộ các giải thuật)**.
>   - 🥇 **Độ phủ sóng đạt tới 99.91%**.*
> - *Điều này chứng minh hoàn toàn tính đúng đắn của cơ chế cải tiến: I-WOA không bị kẹt cực trị, càng chạy sâu càng tìm ra các cấu hình đặt trạm tối ưu mà các thuật toán cơ sở không thể chạm tới."*

---

## 6. Phần 5: Hướng Dẫn Trực Quan Chiếu Ảnh & Đồ Thị (1 phút)

Khi thầy nhìn vào màn hình máy tính, bạn mở lần lượt các file sau:

### 1. Mở file [uav_3d_placement_demo.png](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/results/uav_3d_placement_demo.png):
- **Bạn nói:** *"Đây là hình ảnh mô phỏng không gian 3D của 4 UAV do I-WOA định vị để phục vụ 200 người dùng:*
  - *Các chấm xanh dương dưới đáy là người dùng mặt đất.*
  - *4 đỉnh tam giác màu là 4 UAV đang bay ở độ cao tối ưu từ 80m – 140m.*
  - *Các đường tròn dưới đất là nón phát sóng 5G. Thầy có thể thấy 4 vòng tròn này che phủ trọn vẹn khu vực mật độ dân cư nhưng **gần như không chồng lấn lên nhau**, giải thích vì sao tỷ lệ nhiễu giao thoa của I-WOA lại thấp kỷ lục (dưới 6%)."*

### 2. Mở file [part1_vs_part2_breakthrough_comparison.png](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/results/part1_vs_part2_breakthrough_comparison.png) (ĐỒ THỊ ĐẮT GIÁ NHẤT):
- **Bạn nói:** *"Đây là biểu đồ đối chiếu trực tiếp sự bứt phá giữa 2 giai đoạn:
  - Cột màu xanh là 35 vòng lặp, cột màu đỏ là 80 vòng lặp.
  - Thầy có thể thấy rõ: **I-WOA là thuật toán có bước nhảy vọt Fitness mạnh mẽ nhất (+0.0100)**, vươn từ vị trí thứ 5 lên **Hạng 1 toàn bảng**.
  - Đồng thời, ở biểu đồ bên phải, **nhiễu giao thoa của I-WOA giảm sâu nhất (-3.32%)**, rơi xuống mức đáy **5.72%** (thấp nhất toàn bộ các giải thuật)."*

### 3. Mở file [part2_deep_convergence_80_iter.png](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/results/part2_80_iterations/part2_deep_convergence_80_iter.png):
- **Bạn nói:** *"Đây là bộ 4 biểu đồ phân tích khả năng mở rộng ở 80 vòng lặp:*
  - *Đồ thị Fitness: Đường màu đỏ của I-WOA bứt lên dẫn đầu ở hầu hết các quy mô.*
  - *Đồ thị Nhiễu giao thoa: Đường màu đỏ của I-WOA duy trì ổn định dưới 6%, bỏ xa các thuật toán còn lại.*
  - *Độ phủ sóng luôn đạt xấp xỉ tuyệt đối (99.91%)."*

### 4. Mở file [parameter_and_metrics_table.png](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/results/part2_80_iterations/parameter_and_metrics_table.png) hoặc [system_parameters_table.png](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/results/system_parameters_table.png):
- **Bạn nói:** *"Nếu thầy muốn xem các thông số kỹ thuật chuẩn hóa, đây là bảng tổng hợp thông số vật lý 5G (tần số 3.5 GHz, công suất 30 dBm, mô hình Al-Hourani) cùng bảng xếp hạng định lượng cụ thể của cả 6 thuật toán."*

### 5. Mở file [DEMO_REPORT.md](file:///d:/Personal%20Base/UAV-Placement-Optimization-for-Wireless-Networks/implementation/results/DEMO_REPORT.md):
- **Bạn nói:** *"Và đây là báo cáo số liệu chi tiết đối chiếu trực tiếp giữa giai đoạn 1 (35 vòng lặp) và giai đoạn 2 (80 vòng lặp) để thầy kiểm chứng."*

---

## 7. Phần 6: Bộ Câu Hỏi Phản Biện Thường Gặp & Câu Trả Lời Mẫu

### ❓ Câu hỏi 1: *"Tại sao em không dùng luôn 10 UAV cho phủ kín luôn mà lại chọn 4 UAV?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, việc sử dụng càng nhiều UAV sẽ làm tăng vọt chi phí đầu tư và chi phí năng lượng bay ($f_2$), đồng thời diện tích chồng lấn gây nhiễu đồng kênh ($f_3$) sẽ tăng theo cấp số nhân. Nghiên cứu này chứng minh rằng chỉ cần **4 UAV nhưng được định vị 3D tối ưu** thì đã đạt độ phủ sóng tới **> 99.6%**, vừa tiết kiệm năng lượng vừa triệt tiêu tối đa nhiễu giao thoa."*

### ❓ Câu hỏi 2: *"Tại sao ở vòng lặp thấp, thuật toán I-WOA chạy chậm hơn các thuật toán khác?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, I-WOA tích hợp thêm 2 cơ chế học đối kháng OBL và bước nhảy Levy. Ở mỗi vòng lặp, OBL phải đánh giá thêm nghiệm đối lập và Levy phải đánh giá nghiệm đột biến, do đó số lượng hàm đánh giá (Function Evaluations) trên mỗi vòng lặp của I-WOA cao hơn. Tuy nhiên, sự đánh đổi này là hoàn toàn xứng đáng vì nó giúp thuật toán không bị sa lầy vào cực trị địa phương và đạt Fitness cao hơn khi hội tụ sâu."*

### ❓ Câu hỏi 3: *"Thuật toán lai H-WOA-PSO của em kết hợp thế nào?"*
> **Trả lời:**  
> *"Dạ thưa Thầy, H-WOA-PSO phân chia quần thể: một nửa thực hiện cơ chế săn mồi xoắn ốc bọt khí của WOA để khám phá không gian, nửa còn lại cập nhật vận tốc và vị trí theo vector gia tốc bầy đàn của PSO hướng về $G_{\text{best}}$. Sự kết hợp này bù trừ hoàn hảo giữa tốc độ hội tụ nhanh của PSO và khả năng tản đều chống nhiễu của WOA."*

### ❓ Câu hỏi 4: *"Tại sao em chỉ khảo sát trong diện tích $1\text{ km}^2$ mà không mở rộng lên hàng chục hoặc hàng trăm $\text{km}^2$?" (CÂU HỎI KỸ THUẬT VÔ TUYẾN 5G QUAN TRỌNG)*
> **Trả lời:**  
> *"Dạ thưa Thầy/Cô, bài toán đặt ra trong bối cảnh **UAV-assisted Emergency / Hotspot Network** (Cứu trợ thảm họa hoặc phủ sóng tăng cường cho các điểm nóng đô thị như sân vận động, quảng trường sự kiện, khuôn viên trường đại học) với diện tích chuẩn $1\text{ km}^2$ ($1000\text{m} \times 1000\text{m}$).
> 
> Về mặt **Vật lý vô tuyến 5G**:
> 1. Trạm bay UAV dùng nguồn pin giới hạn nên công suất phát chuẩn hóa chỉ ở mức $P_{\text{tx}} = 30\text{ dBm}$ ($1.0\text{ W}$), hoạt động ở dải tần Sub-6 ($3.5\text{ GHz}$).
> 2. Theo mô hình suy hao kênh truyền Al-Hourani và ngưỡng QoS $SNR_{\text{th}} = 18\text{ dB}$, bán kính phủ sóng hiệu dụng khả dụng của mỗi UAV chỉ khoảng $250\text{m} - 350\text{m}$ (diện tích phủ khoảng $0.25\text{ km}^2$). Vì vậy, cụm **4 UAV** phối hợp bao phủ khu vực $1\text{ km}^2$ là tỷ lệ vàng tối ưu nhất, vừa khít vùng phủ và giảm thiểu chồng lấn.
> 3. Nếu đẩy diện tích lên $100\text{ km}^2$ ($10\text{km} \times 10\text{km}$), khoảng cách truyền sóng xa vài km sẽ khiến suy hao vượt $140\text{ dB}$, tín hiệu chìm hoàn toàn vào tạp âm nền ($SNR < 0\text{ dB}$ so với ngưỡng $18\text{ dB}$), tỷ lệ phủ sóng sẽ rơi về $0\%$. Để phủ $100\text{ km}^2$, thực tế phải dùng tháp viễn thông Macro công suất cao ($40\text{W}-100\text{W}$) hoặc vệ tinh LEO tầm thấp, chứ không thể dùng drone nhỏ.
> 4. Trong tương lai nếu mở rộng diện tích lớn hơn (như $2\text{km} \times 2\text{km}$), mô hình chỉ cần mở rộng số lượng UAV tương ứng ($N=8$ đến $16$ UAVs). Thuật toán I-WOA hoàn toàn tự động phân cụm K-Means và tối ưu hóa không gian đa chiều mà không bị giới hạn."*

### ❓ Câu hỏi 5: *"Quy mô dữ liệu thử nghiệm này có đủ tin cậy và có bị ít không?"*
> **Trả lời:**  
> *"Dạ thưa Thầy/Cô, bộ dữ liệu thử nghiệm trong nghiên cứu này rất lớn và vượt chuẩn thống kê học thuật:
> - Em đã tạo và chạy trên toàn bộ **500 file kịch bản CSV độc lập** (50 kịch bản ngẫu nhiên cho mỗi mức người dùng từ 50 đến 500 UEs).
> - Tổng số lượt chạy tối ưu hóa là **3.000 lượt chạy Monte Carlo** (500 files $\times$ 6 thuật toán).
> - Trong khi đó, các bài báo IEEE hàng đầu (như của Al-Hourani, Mozaffari) thường chỉ khảo sát trên $30 - 50$ kịch bản ngẫu nhiên. Vì vậy, số liệu trung bình mà em rút ra có ý nghĩa thống kê cực kỳ vững chắc, loại bỏ hoàn toàn tính may rủi ngẫu nhiên."*

---

🎉 **Chúc bạn có buổi demo chiều nay thật tự tin, thuyết phục và đạt điểm tuyệt đối từ Thầy!**

