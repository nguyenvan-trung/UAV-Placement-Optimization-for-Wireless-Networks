# 📊 BẢNG THÔNG SỐ VÀ KẾT QUẢ THỰC NGHIỆM - PHẦN 2
> **Chế độ:** Tối ưu hóa sâu / Toàn cục (Deep Convergence & Global Optimization)  
> **Quy mô khảo sát:** 10 mức quy mô người dùng đại diện (50, 100, 150, 200, 250, 300, 350, 400, 450, 500 UEs)  
> **Tổng số lượt chạy:** 60 lượt tối ưu hóa (10 quy mô × 6 thuật toán)  

---

## ⚙️ 1. BẢNG THÔNG SỐ THIẾT LẬP MÔ PHỎNG (SYSTEM & ALGORITHM PARAMETERS)

| Nhóm thông số | Tên thông số | Ký hiệu | Giá trị thiết lập | Đơn vị / Ý nghĩa |
| :--- | :--- | :---: | :---: | :--- |
| **Không gian mạng** | Kích thước khu vực | $W \times H$ | $1000 \times 1000$ | $\text{m}^2$ (Diện tích $1\text{ km}^2$) |
| | Độ cao UAV | $[z_{\min}, z_{\max}]$ | $[50, 300]$ | mét (Độ cao bay an toàn) |
| | Số lượng UAV | $N$ | **4** | trạm phát sóng bay |
| | Số lượng người dùng mặt đất | $M$ | **50 đến 500** | UEs (10 mức quy mô) |
| **Vật lý vô tuyến (5G)** | Tần số sóng mang | $f_c$ | **3.5** | $\text{GHz}$ (Chuẩn Sub-6 5G) |
| | Công suất phát UAV | $P_{\text{tx}}$ | **30** | $\text{dBm}$ (1.0 W) |
| | Tạp âm nền | $N_0$ | **-104** | $\text{dBm}$ |
| | Ngưỡng kết nối khả dụng | $SNR_{\text{th}}$ | **18.0** | $\text{dB}$ (Chuẩn QoS 5G) |
| | Môi trường đô thị (Al-Hourani)| $a, b$ | $9.61,\; 0.16$ | Tham số xác suất LoS đô thị |
| | Suy hao cộng thêm LoS / NLoS | $\eta_{\text{LoS}}, \eta_{\text{NLoS}}$ | $1.0,\; 20.0$ | $\text{dB}$ |
| **Hàm mục tiêu đa tiêu chí** | Trọng số Độ phủ sóng ($f_1$) | $w_1$ | **0.6** | Càng cao càng tốt |
| | Trọng số Tiết kiệm năng lượng ($f_2$) | $w_2$ | **0.2** | Càng thấp càng tốt |
| | Trọng số Nhiễu giao thoa ($f_3$) | $w_3$ | **0.2** | Càng thấp càng tốt |
| **Cấu hình thuật toán** | Kích thước quần thể | $PopSize$ | **25** | cá thể / bầy đàn |
| | **Số vòng lặp tối đa** | **$MaxIter$** | **80** | **vòng lặp (Tối ưu hóa sâu bứt phá)** |
| | Random Seed | $Seed$ | **42** | Tái lập kết quả |

---

## 📈 2. BẢNG KẾT QUẢ FITNESS THEO TỪNG QUY MÔ (80 VÒNG LẶP)

| Số lượng UEs | GA | PSO | WOA | H-PSO-GA | H-WOA-PSO | I-WOA (Đề xuất) | Thuật toán dẫn đầu |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **50** | 0.4582 | 0.4502 | **0.4622** | 0.4582 | **0.4622** | **0.4622** | 🏆 **I-WOA / WOA / H-WOA-PSO** |
| **100** | 0.4507 | 0.4569 | **0.4659** | **0.4659** | 0.4616 | 0.4590 | 🏆 **H-PSO-GA / WOA** |
| **150** | 0.4247 | 0.4222 | 0.4222 | 0.4256 | 0.4245 | **0.4594** | 🏆 **I-WOA (Áp đảo)** |
| **200** | 0.4558 | **0.4572** | 0.4558 | 0.4571 | 0.3922 | **0.4572** | 🏆 **I-WOA / PSO** |
| **250** | **0.4416** | 0.4296 | 0.4249 | 0.4277 | 0.4292 | 0.4315 | 🏆 **GA** |
| **300** | 0.4497 | **0.4542** | 0.4476 | 0.4538 | **0.4542** | 0.4504 | 🏆 **H-WOA-PSO / PSO** |
| **350** | 0.4242 | **0.4462** | 0.4388 | 0.4450 | 0.4459 | 0.4424 | 🏆 **PSO** |
| **400** | 0.4454 | 0.4360 | 0.4352 | 0.4461 | 0.4492 | **0.4497** | 🏆 **I-WOA** |
| **450** | 0.4456 | **0.4507** | 0.4481 | 0.4432 | 0.4455 | 0.4483 | 🏆 **PSO** |
| **500** | 0.4512 | 0.4562 | 0.4365 | **0.4586** | 0.4468 | 0.4448 | 🏆 **H-PSO-GA** |

---

## 🏆 3. BẢNG TỔNG HỢP VÀ XẾP HẠNG TOÀN DIỆN PHẦN 2 (80 VÒNG LẶP)

| Hạng | Thuật toán | Fitness Trung Bình | Fitness Cao Nhất | Tỷ Lệ Nhiễu TB ($f_3$) | Độ Phủ Sóng TB ($f_1$) | Năng Lượng TB ($f_2$) | Thời Gian Chạy TB |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **I-WOA (Đề xuất)** | **0.4505 🚀** | **0.4622** | **5.72% 🎯 (Thấp nhất)** | **99.91%** | 0.6876 | 4.34s |
| 🥈 | **H-PSO-GA** | 0.4481 | **0.4659** | 7.75% | **99.91%** | **0.6791** | 1.44s |
| 🥉 | **PSO** | 0.4459 | 0.4572 | 8.26% | 99.75% | 0.6800 | **1.08s** |
| 4 | **GA** | 0.4447 | 0.4582 | 8.42% | **99.91%** | 0.6895 | 1.30s |
| 5 | **WOA (Gốc)** | 0.4437 | **0.4659** | 7.78% | 99.43% | 0.6864 | 1.28s |
| 6 | **H-WOA-PSO** | 0.4411 | 0.4622 | 10.40% | 99.75% | 0.6828 | 1.44s |

---

## 💡 ĐIỂM NHẤN ĐỘT PHÁ CỦA I-WOA Ở PHẦN 2:
- **Tăng vọt lên vị trí số 1** về Fitness trung bình (**0.4505**).
- **Tỷ lệ nhiễu giao thoa giảm kỷ lục xuống 5.72%** (thấp hơn hẳn tất cả các thuật toán còn lại, chứng minh K-Means + OBL phân tán trạm bay cực kỳ chuẩn xác).
- **Độ phủ sóng đạt xấp xỉ tuyệt đối: 99.91%**.
