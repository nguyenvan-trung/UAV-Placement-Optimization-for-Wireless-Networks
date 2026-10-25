# Kiểm toán mô hình và Fitness — Nhiệm vụ 1

**Cảnh báo kết quả cũ:** Các lượt chạy trước khi bổ sung khoảng cách UAV không chứng minh được chất lượng cho mô hình có ràng buộc hiện tại. Cần chạy lại cả sáu thuật toán ở Part 1, Part 2, batch và Monte Carlo nếu muốn kết luận theo mô hình mới. Nếu đổi mô hình năng lượng/nhiễu, phải chạy lại toàn bộ đối chứng. Các kết quả cũ đã được xóa theo yêu cầu, không thể đối chiếu trực tiếp các con số lịch sử.

Phạm vi: mã đang có trên workspace, bao gồm các sửa lỗi đã áp dụng ở lượt trước. Lượt kiểm toán này chỉ tạo test, báo cáo và patch; không chỉnh mã sản xuất. PASS là đúng theo hợp đồng hiện tại, không chứng minh mô hình đúng ngoài thực tế.

## A. Bảng kết luận

Các đường dẫn dưới đây tương đối từ gốc dự án; trích dòng theo bản được kiểm toán. Hash gộp nguồn nằm trong mỗi dòng CSV.

| Mục | Kết luận | Bằng chứng code và nhận xét |
|---|---|---|
| 1. Euclid 3D | ĐÚNG | `implementation/src/physics/channel.py:32-34`: `diff = uav_coords[:, np.newaxis, :] - ue_coords[np.newaxis, :, :]`, `sqrt(sum(diff**2))`. Có dùng z của cả UE và UAV; sàn khoảng cách là bảo vệ số học. |
| 2. Góc ngẩng | KHÔNG RÕ | `channel.py:53-56`: `delta_z`, `clip(..., 0.0, 1.0)`, `degrees(arcsin(...))`. Đơn vị độ nhất quán với LoS, đúng khi UAV cao hơn UE; UE cao hơn UAV bị ép góc về không. Chưa có căn cứ mở rộng mô hình ground-user cho UE trong nhà cao tầng. |
| 3. LoS/NLoS | KHÔNG RÕ | `channel.py:66-69`: `1.0 / (1.0 + a * exp(...))`; `network.py:17-20`: a,b,eta. Dạng logistic đúng với [1]; NLoS dùng `1-p_los` ở dòng 89. Nguồn chính xác/hiệu chuẩn bộ tham số và mô tả “dense urban” chưa được xác minh; không kết luận cả bộ hằng số đúng chỉ vì công thức đúng. |
| 4. Suy hao | ĐÚNG | `channel.py:86-89`: FSPL theo mét/Hz và excess loss theo dB. Tương ứng suy hao trung bình dB trong [1], không phải trung bình công suất tuyến tính hay mô phỏng ngẫu nhiên từng liên kết. |
| 5. SNR | ĐÚNG | `channel.py:98-99`: `p_tx_dbm - path_loss - noise_dbm`; `network.py:23-24`: Ptx và noise cùng dBm. Không trộn tuyến tính và dB trong đường tính SNR. Chưa biết băng thông/noise figure giải thích noise, và đây không phải SINR. |
| 6. Ngưỡng | ĐÚNG | `metrics.py:52`: `snr_matrix >= snr_th`; `network.py:25` đặt ngưỡng dB. Comment gọi đây là “chuẩn QoS 5G” không có nguồn; chỉ phép so sánh và đơn vị được xác nhận. |
| 7. Độ phủ max SNR | ĐÚNG | `metrics.py:52-54,110-113,120`: any(SNR >= threshold) tương đương max(SNR) >= threshold. Mẫu số là toàn bộ UE; mặc định bốn UAV. Không dùng SINR; không có phép gán serving UAV, chỉ kiểm tra tồn tại liên kết đạt ngưỡng. |
| 8. Chuẩn hóa | KHÔNG RÕ | `metrics.py:54,72-78,89-91`: C và I là trung bình mask UE; E là công suất trung bình chia công suất tối đa giả định. Cận cố định theo cấu hình bài toán, không lấy từ quần thể. Các giá trị nằm trong [0,1] với đầu vào hợp lệ nhưng E không trải hết [0,1]. Thiếu nguồn vật lý cho E không đồng nghĩa lỗi chuẩn hóa số học. |
| 9. Chiều tối ưu | ĐÚNG | `metrics.py:118`: `w1 * f1 - w2 * f2 - w3 * f3`; sáu thuật toán chọn cực đại. `network.py:33-35`: trọng số mặc định cộng bằng một. Constructor chưa kiểm tra trọng số tùy chỉnh. |
| 10. Biến thiên E | ĐÚNG | `metrics.py:70-78`: E phụ thuộc z, không phụ thuộc x,y. n=1000; variance(ddof=1)=0.002318725227; std=0.04815314348; min=0.6937154479; max=0.98045101. Near-constant threshold=1e-8; near_constant=False. Uniform independent box samples; seed and coordinates in fitness_energy_samples.csv. Feasibility recorded, not rejection-sampled. This does not measure variation after convergence. |
| 11. Ràng buộc | ĐÚNG | `objective.py:80-84,101-105,119-131`: kiểm tra shape, clip miền rồi kiểm tra khoảng cách. `constraints.py:6-7`: Euclid UAV-UAV; số UAV mặc định là bốn, API cho phép cấu hình số khác. Sáu thuật toán gọi chung problem.evaluate. Va chạm nhận -inf; detailed báo ValueError. is_feasible xét nghiệm gốc, evaluate xét nghiệm sau repair. Khoảng cách mặc định là giả định chưa được thầy xác nhận. |
| 12. Khớp báo cáo | KHÔNG RÕ | `objective.py:87-97,108-117` cùng hàm tính; `run_batch.py:131-147` ghi Fitness từ optimizer và thành phần từ detailed. Kiểm tra trên cùng nghiệm đạt; chưa có log thực nghiệm mới. E=(0.6*C-0.2*I-F)/0.2=0.6876. Source: user-supplied historical tuple in fitness_report_reconciliation.csv. Requires same runs and aggregation for C,I,F. Original reported E unavailable; comparison UNVERIFIED. |

## B. Kết quả từ CSV

CSV: 12/12 tình huống đạt kiểm tra hành vi hiện tại.

| Case | Test | Khả thi trước repair | Fitness trả về |
|---|---|---|---|
| cluster_center | PASS | True | 0.26622516556291387 |
| far_from_users | PASS | True | -0.1337748344370861 |
| low_altitude | PASS | True | 0.26622516556291387 |
| high_altitude | PASS | True | 0.2000000002649006 |
| too_close | PASS | False | -inf |
| partly_uncovered | PASS | True | 0.06622516556291388 |
| out_of_xy | PASS | False | 0.26622516556291387 |
| out_of_altitude | PASS | False | 0.26622516556291387 |
| coincident_uavs | PASS | False | -inf |
| wrong_uav_count | PASS | ValueError | ValueError |
| separation_boundary | PASS | True | 0.26622516556291387 |
| custom_altitude | PASS | True | 0.26622516556291387 |

CSV lưu đầu vào, cấu hình, nghiệm sau repair, tính khả thi trước/sau repair, C/E/I, Fitness, kỳ vọng và phương pháp xác minh. Với sai số UAV hoặc va chạm, API không trả thành phần: ghi N/A. Trường expected chứa giá trị scalar giả định trên tọa độ repair để chẩn đoán, **không phải** Fitness kỳ vọng hợp lệ của nghiệm va chạm/sai số lượng; expected_behavior chỉ rõ ValueError/-inf. Nghiệm ngoài miền được kỳ vọng repair, không tự chuyển sang penalty để làm test đạt.

Oracle dùng vòng lặp scalar, atan2 và math; không gọi lại hàm vật lý/Fitness sản xuất. Hằng số trong oracle là đầu vào đặc tả của thí nghiệm, không phải kết quả báo cáo nhập tay. Bộ này kiểm tra số học mô hình hiện tại, không xác thực giả định hover tăng theo độ cao.

## C. Lỗi, mức độ, đề xuất và tác động

| Mức | Vị trí | Vấn đề và đề xuất | Kết quả phải chạy lại |
|---|---|---|---|
| Cao | `metrics.py:72-78` | Hover tăng tuyến tính theo độ cao với hệ số giả định, không có thời gian. Chưa gọi đây là năng lượng vật lý; cần nguồn/hiệu chuẩn hoặc thiết kế mô hình mới có đơn vị. Không tự thay công thức. | Tất cả nếu thay mô hình E; hiện chỉ chứng minh tối ưu proxy. |
| Cao | `metrics.py:89-91`; `run_batch.py:363-365` | I là tỷ lệ UE được phủ bởi nhiều UAV, không công suất nhiễu; biểu đồ gọi “nhiễu giao thoa” dễ gây hiểu nhầm. Đổi mô tả thành chỉ số chồng lấn; muốn SINR cần chốt mô hình đồng kênh/anten/tài nguyên. | Đổi nhãn không cần chạy; đổi công thức phải chạy tất cả. |
| Cao | `channel.py:54`; `synthetic_generator.py:73-90` | Dataset cho phép UE cao hơn UAV nhưng góc bị cắt về không. Chốt phạm vi ground-user hoặc mô hình UE trên cao/indoor thích hợp; không tự lấy abs(delta_z). | Các bộ có UE trên cao nếu đổi mô hình hoặc dữ liệu. |
| Trung bình | `objective.py:56-57` | Cho NaN/âm/trọng số không chuẩn hóa và ngưỡng không hữu hạn. Patch đề xuất kiểm tra đầu vào. | Cấu hình mặc định hợp lệ không đổi; lượt dùng cấu hình sai phải loại/chạy lại. |
| Trung bình | `network.py:16,25` | Nhãn môi trường và tuyên bố “chuẩn QoS 5G” thiếu xác minh. Patch chỉ sửa mô tả, không đổi hằng số. | Không cần nếu chỉ đổi mô tả; nếu đổi tham số cần chạy tất cả. |
| Trung bình | `objective.py:36,83-84`; `run_batch.py:132` | Khoảng cách mặc định là giả định. Nếu toàn bộ nghiệm không khả thi, optimizer có thể trả -inf và bước xuất detailed lỗi. Cần chốt khoảng cách và xử lý thất bại khả thi trong runner trước batch lớn. | Lượt thất bại không được nhập vào thống kê như nghiệm hợp lệ. |
| Thấp | `metrics.py:72` | Mẫu số cộng epsilon khiến biên trên hơi dưới một; là regularizer số học, không phải lỗi dấu. Có thể bỏ epsilon sau khi kiểm tra max>min ở API helper; chưa đề xuất đổi để tránh thay số học ngoài phạm vi. | Nếu đổi cần ghi phiên bản; không gộp điểm cũ/mới thiếu giải trình. |

**Đã sửa trước lượt này:** lỗi truyền biên độ cao (`objective.py:94-95,115-116`) và thiếu khoảng cách (`constraints.py:5-7`). Lượt cũ dùng biên mặc định không bị lỗi truyền biên; lượt dùng biên tùy chỉnh phải chạy lại. Các lượt trước có ràng buộc khác phải chạy lại để đánh giá bài toán mới, không khẳng định mọi con số cũ sai số học.

## Patch đề xuất — chưa áp dụng

`reports/fitness_audit_proposed.patch` chỉ kiểm tra threshold/trọng số và sửa comment tham số. `objective.py:38` được đề xuất đổi để chuyển input sang ndarray trước kiểm tra shape. Tác động: list được chấp nhận, cấu hình sai bị từ chối; cấu hình ndarray mặc định không đổi. Không có patch vật lý cho E/I vì chưa đủ căn cứ chọn mô hình thay thế.

Đọc diff trước khi duyệt. Kiểm tra khả năng áp dụng: `git apply --check reports/fitness_audit_proposed.patch`. Không chạy `git apply` khi chưa có duyệt.

## Cách chạy và tái tạo

```powershell
python -m pytest implementation/tests/test_fitness.py -q -p no:cacheprovider
python implementation/scripts/build_fitness_audit_report.py
```

CSV được fixture ghi lại kể cả khi assertion thất bại; không chạy pytest-xdist với writer này. Hai test bổ sung ngưỡng và hình học không ghi dòng CSV. Hash nguồn trong CSV ràng buộc kết quả với nội dung source; chạy lại sau khi source thay đổi. Chưa chạy lại thí nghiệm lớn.

## Nguồn và giới hạn

- [1] Alzenad et al., mục II, (1)-(3): https://arxiv.org/pdf/1705.03415 — LoS theo góc độ và suy hao trung bình dB. Mục tiêu phủ UE với công suất phát thấp; không cung cấp Fitness ba thành phần hiện tại.
- [2] Mozaffari et al., mục III: https://arxiv.org/pdf/1606.01962 — độ phủ có xét SINR và nhiễu; không phải công thức đếm UE chồng lấn hiện tại.
- [3] Zeng et al.: https://arxiv.org/pdf/1804.02238 — công suất đẩy và năng lượng theo thời gian; không bảo vệ luật hover tuyến tính theo độ cao đang dùng.

Chưa chắc chắn: nguồn hiệu chuẩn bộ tham số môi trường ở tần số đang dùng; cơ sở ngưỡng QoS và noise; cách dùng UE trên cao; mô hình E/I; khoảng cách an toàn; log thực nghiệm mới. Cần chốt trước khi thay mô hình. Không tuyên bố hoàn thành xác thực vật lý chỉ từ test đạt.
