# 📊 BẢNG THÔNG SỐ VÀ KẾT QUẢ THỰC NGHIỆM - PHẦN 1
> **Chế độ:** Hội tụ sớm (Early Convergence)  
> **Quy mô khảo sát:** Toàn bộ 500 file bộ dữ liệu (50 kịch bản ngẫu nhiên cho mỗi mức người dùng từ 50 đến 500 UEs)  
> **Tổng số lượt chạy:** 3.000 lượt tối ưu hóa (500 files × 6 thuật toán)  

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
| | Số vòng lặp tối đa | $MaxIter$ | **35** | vòng lặp (Khảo sát hội tụ sớm) |
| | Random Seed | $Seed$ | **42** | Tái lập kết quả |

---

## 📈 2. BẢNG KẾT QUẢ FITNESS THEO TỪNG QUY MÔ (50 -> 500 UEs)
*(Mỗi giá trị là trung bình của 50 kịch bản ngẫu nhiên)*

| Số lượng UEs | GA | PSO | WOA | H-PSO-GA | H-WOA-PSO | I-WOA | Thuật toán dẫn đầu |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **50** | 0.4399 | 0.4472 | **0.4500** | 0.4477 | 0.4485 | 0.4472 | 🏆 **WOA** |
| **100** | 0.4368 | **0.4480** | 0.4429 | 0.4477 | 0.4458 | 0.4412 | 🏆 **PSO** |
| **150** | 0.4399 | **0.4460** | 0.4439 | 0.4433 | 0.4452 | 0.4420 | 🏆 **PSO** |
| **200** | 0.4354 | 0.4435 | **0.4463** | 0.4442 | 0.4439 | 0.4448 | 🏆 **WOA** |
| **250** | 0.4376 | 0.4391 | **0.4410** | 0.4404 | 0.4403 | 0.4394 | 🏆 **WOA** |
| **300** | 0.4359 | **0.4399** | 0.4375 | 0.4372 | 0.4398 | 0.4359 | 🏆 **PSO** |
| **350** | 0.4342 | 0.4414 | 0.4414 | 0.4413 | **0.4428** | 0.4385 | 🏆 **H-WOA-PSO** |
| **400** | 0.4342 | 0.4388 | 0.4378 | 0.4337 | **0.4399** | 0.4375 | 🏆 **H-WOA-PSO** |
| **450** | 0.4384 | 0.4427 | **0.4440** | 0.4401 | 0.4428 | 0.4405 | 🏆 **WOA** |
| **500** | 0.4366 | 0.4388 | 0.4404 | 0.4401 | **0.4412** | 0.4384 | 🏆 **H-WOA-PSO** |

---

## 🏆 3. BẢNG TỔNG HỢP VÀ XẾP HẠNG TOÀN DIỆN PHẦN 1

| Hạng | Thuật toán | Fitness TB | Fitness Max | Độ Phủ Sóng TB ($f_1$) | Tỷ Lệ Nhiễu TB ($f_3$) | Năng Lượng TB ($f_2$) | Thời Gian Chạy TB |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 | **H-WOA-PSO** | **0.4430** | **0.4662** | 99.63% | 9.15% | 0.6823 | 0.77s |
| 🥈 | **PSO** | 0.4426 | **0.4662** | 99.73% | 9.85% | **0.6805** | **0.72s** |
| 🥉 | **WOA** | 0.4425 | **0.4662** | 99.54% | **8.47%** | 0.6889 | 0.72s |
| 4 | **H-PSO-GA** | 0.4416 | **0.4662** | 99.74% | 10.12% | 0.6831 | 0.78s |
| 5 | **I-WOA** | 0.4405 | **0.4662** | 99.57% | 9.04% | 0.6940 | 4.13s |
| 6 | **GA** | 0.4369 | 0.4650 | **99.79%** | 11.24% | 0.6968 | 0.89s |
