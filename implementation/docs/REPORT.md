# Báo cáo tối ưu vị trí UAV-BS — bản hiệu chỉnh theo kiểm toán

[Mục lục](README.md) · [Người mới](PROJECT_GUIDE.md) · [Thuật ngữ](GLOSSARY.md) · [Study notebook](NOTEBOOK_STUDY.md)


**Trạng thái:** chưa có kết quả benchmark theo FE. Các bảng/hình kiểm thử
và minh họa không phải bằng chứng so sánh thuật toán. Số liệu thực nghiệm cũ
đã rút khỏi tài liệu DW vì chưa truy được log và chưa đồng nhất điều kiện.
Không khẳng định I-WOA dẫn đầu hoặc tìm được tối ưu toàn cục.

## Mô hình

Đề tài xét vị trí ba chiều của bốn UAV. Mỗi nghiệm là vector ghép tọa độ
các UAV. Tham số vật lý và miền tìm kiếm là đầu vào mô phỏng, không phải
kết quả đo. Nguồn cấu hình: [network.py](../src/constants/network.py),
[objective.py](../src/problem/objective.py); nguồn từng dòng được liệt kê
trong [kiểm toán](../../reports/fitness_audit.md).

Hàm mục tiêu cực đại hóa:

\[
F(X)=0{,}6C(X)-0{,}2E(X)-0{,}2I(X).
\]

Độ phủ của bản chính dùng **SNR**, không phải SINR:

\[
C(X)=\frac{1}{M}\sum_{j=1}^{M}
\mathbf1\!\left[\max_{i=1,\ldots,4}\operatorname{SNR}_{ij}(X)
\ge18\ \mathrm{dB}\right].
\]

Mẫu số là toàn bộ UE. Mỗi UE chỉ được đếm một lần dù có nhiều liên kết
đạt ngưỡng. Đây là tiêu chí độ phủ liên kết, chưa bảo đảm dung lượng hoặc
tốc độ người dùng. SNR tính bằng công suất phát dBm trừ suy hao dB và
công suất tạp âm dBm; không có tổng công suất gây nhiễu giữa UAV trong SNR.
Ngưỡng là lựa chọn mô phỏng, không gọi là chuẩn QoS chung của mạng di động.

Khoảng cách Euclid dùng cả độ cao UE và UAV. Góc ngẩng được đổi sang độ
trước công thức LoS. Suy hao là FSPL cộng excess loss trung bình theo dB.
Khi UE cao hơn UAV, code ép góc âm về không: tính phù hợp vật lý chưa được
xác nhận. Không suy rộng kết quả ground-user sang indoor hoặc nhà cao tầng.

Thành phần E hiện là **proxy công suất trung bình chuẩn hóa**, không phải
năng lượng Joule. Với công suất hover nền P₀, công suất phát Ptx và biên
độ cao cố định của bài toán:

\[
r_i=\operatorname{clip}\left(\frac{z_i-z_{\min}}
 {z_{\max}-z_{\min}+\epsilon},0,1\right),\qquad
E=\frac{\frac1N\sum_i[P_0(1+0{,}5r_i)+P_{tx}]}
 {1{,}5P_0+P_{tx}}.
\]

Hệ số tăng hover theo độ cao là giả định chưa hiệu chuẩn, cần sinh viên
tự xác minh. E nằm trong thang đơn vị nhưng không trải toàn bộ khoảng từ
không đến một; giá trị tối thiểu dương. E thay đổi theo độ cao, không theo
tọa độ ngang, và không thể hiện tổng công suất đội UAV khi thay số UAV.

Thành phần I là **proxy chồng lấn theo UE**, không phải diện tích giao
thoa hoặc công suất nhiễu:

\[
I(X)=\frac1M\sum_j\mathbf1\left[
 \sum_i\mathbf1[\operatorname{SNR}_{ij}\ge18\ \mathrm{dB}]\ge2\right].
\]

C và I là tỷ lệ trên toàn bộ UE. Biên chuẩn hóa E cố định theo bài toán,
không lấy min/max từ quần thể hiện tại. Các trọng số là **lựa chọn thiết kế
của nhóm**, không phải tỷ lệ đã được chứng minh. Kết quả phân tích độ nhạy
chưa có; kế hoạch đã khai báo tại [sensitivity.yaml](../../configs/sensitivity.yaml).
Không viện dẫn kế hoạch đó như bằng chứng lựa chọn trọng số hợp lý.

Ràng buộc gồm miền tọa độ/độ cao, đúng kích thước nghiệm và khoảng cách
UAV. Code clip vào miền rồi kiểm tra khoảng cách; vi phạm khoảng cách
nhận Fitness âm vô cùng, không xuất như nghiệm hợp lệ. Khoảng cách an toàn
hiện là tham số mô phỏng chưa được xác nhận là tiêu chuẩn vận hành.

## Hai giao thức thí nghiệm cần phân biệt

Thiết kế hiện tại theo yêu cầu là [notebook 30 trường hợp](NOTEBOOK_STUDY.md): đọc 500 CSV có sẵn, quần thể 25, 4 UAV và 100 vòng; danh sách seed còn để trống. Lưu 101 mốc và lấy checkpoint 35/80 từ cùng lần chạy. Cùng vòng không bảo đảm cùng FE, nên báo cả FE và thời gian. Chưa có kết quả study này.

Thiết kế FE phía dưới là một luồng riêng, sinh tọa độ từ YAML/seed manifest và dừng theo FE. Nó không tự đọc 500 CSV hoặc thay thế giao thức notebook. Không gộp kết quả hai luồng.

## Thiết kế đối chứng theo FE

Yêu cầu đối chứng là cùng dữ liệu, Fitness, ràng buộc, quần thể nền, seed
ghép cặp và **ngân sách đánh giá Fitness**. Mọi đánh giá nghiệm đối lập,
Lévy và khởi tạo đều phải nằm trong ngân sách. K-Means không gọi Fitness
trực tiếp nhưng vẫn có chi phí thời gian. Không coi cùng vòng lặp là cùng FE.

**Đã bổ sung runner/counter FE và manifest theo Nhiệm vụ 2**, xem
[EXPERIMENT_DESIGN.md](EXPERIMENT_DESIGN.md) và [REPRODUCE.md](../../REPRODUCE.md).
Chưa có full benchmark theo FE; các lựa chọn thiết kế phải chốt trước khi chạy. Tuning và eval phải tách biệt;
phải lưu phiên bản mã, cấu hình, môi trường, seed và log từng lượt chạy.

## Part 1 và Part 2

Tên hai giai đoạn cũ không đại diện cho một phép so sánh đã xác minh.
Không giữ bảng cũ vì chưa biết chắc từng giá trị là một run, trung bình
hay best, cùng định nghĩa Fitness và cùng tập instance hay không.
Khi có kết quả mới, mỗi ô phải ghi rõ phép gộp, số instance/run, ngân sách
FE và cấu hình. Không so trực tiếp kết quả khác số UAV hoặc khác Fitness.

## Độ phủ và thứ hạng theo quy mô

Không viết “mọi UE đều đạt ngưỡng” nếu tỷ lệ thấp hơn toàn bộ UE. Với mỗi
run phải ghi `ue_pass/ue_total`; với tổng hợp phải phân biệt mean tỷ lệ
theo run và tỷ lệ gộp tổng tử số trên tổng mẫu số. Tổng mẫu số qua nhiều
run là số lượt UE được đánh giá, không phải số người dùng duy nhất.

Chưa có bảng thứ hạng mới theo UE/phân bố. Bảng cũ không được dùng để
khẳng định thắng trên mọi quy mô. Khi có log, dùng
[analyze_stability.py](../scripts/analyze_stability.py); đưa các trường hợp
I-WOA không đứng đầu vào bảng riêng, kể cả kết quả bất lợi. Chênh lệch mô
tả không tự chứng minh khác biệt thống kê. Overhead OBL/Lévy và ảnh hưởng
K-Means chỉ là giả thuyết cho đến khi có thí nghiệm ghép cặp.

## Thời gian và chi phí tính toán

Rút tuyên bố tốc độ cũ vì chưa có metadata phần cứng và log đầy đủ.
Chưa có các giá trị sau, không điền bằng ước lượng hoặc dữ liệu test:

| Trường cần báo cáo | Nguồn bắt buộc | Trạng thái |
|---|---|---|
| CPU, hệ điều hành, RAM | env.json của batch | Chưa có |
| Số worker, luồng mỗi worker | cấu hình và env.json | Chưa có |
| Batch wall time (s) | đồng hồ wall đo ở tiến trình điều phối | Chưa có |
| Tổng CPU time (s) | tổng process_time của các worker theo phạm vi đã công bố | Chưa có |
| Tổng FE | tổng fe_used của các run hợp lệ được chỉ rõ | Chưa có |
| FE/s của batch | tổng FE / batch wall time | Chưa có |
| FE/s mỗi run | fe_used / wall_time_s | Chưa có |

Không cộng metadata batch lặp trên mọi dòng. Tổng CPU và wall time là
hai đại lượng khác nhau; không chia tổng CPU cho số worker để suy ra wall.
Phải công bố thời gian có bao gồm khởi động, sinh dữ liệu, K-Means và ghi
log hay không. Chi phí chạy cuối để báo cáo tách khỏi FE tìm kiếm.

## Ablation

Notebook đã mở rộng tám tổ hợp K/O/L cho mỗi họ WOA, PSO và GA, kèm các case ablation cho hai bản lai; tổng 30 case duy nhất. Bảng mô tả/đóng góp được chuẩn bị nhưng chưa có số liệu. Luồng FE hiện có registry ablation riêng của I-WOA, không đồng nhất hai phạm vi.

Một lớp I-WOA dùng cờ bật/tắt K-Means, OBL và Lévy. Kiểm thử lõi tương
đương WOA khi tắt cả ba không thay thế đánh giá chất lượng theo FE.
Xem [ABLATION.md](ABLATION.md) để biết vị trí tiêu tốn FE và trạng thái.
Chưa có runs.csv ablation hoặc bảng đóng góp biên; không kết luận hiệu
quả cộng dồn và không loại khả năng tương tác âm giữa các thành phần.

## Tổng quát hóa

Các bộ sinh UE và hình [scenarios.png](../../figures/scenarios.png) chỉ
minh họa thiết kế, không chứng minh thuật toán tổng quát tốt. Nguồn hình
là các CSV scenario cùng thư mục. Xem [STABILITY.md](STABILITY.md).
Chưa chạy sáu thuật toán trên thiết kế đầy đủ nên chưa kết luận thay đổi
thứ hạng theo mật độ, phân bố hoặc ngoại lai.

## Độ nhạy

Các bộ trọng số, coverage-only và SINR phụ đã khai báo trước. Mỗi cấu
hình phải tối ưu lại, cùng FE và seed; không chỉ chấm lại nghiệm cũ.
So sánh C_snr/E/I riêng lẻ giữa cấu hình, không so điểm Fitness khác
trọng số như cùng một thang chất lượng. SINR phụ giữ I nên phản ánh nhiễu
ở cả C và I; không đổi bản chính. Xem [SENSITIVITY.md](SENSITIVITY.md).
Chưa có kết quả độ nhạy để xác nhận thứ hạng ổn định hoặc tác dụng phân biệt.

## Thống kê

[analyze.py](../scripts/analyze.py) mô tả run và kiểm định trên trung vị
theo instance, bootstrap CI cấp instance, kiểm định ghép cặp, effect size
và hiệu chỉnh đa so sánh. Xem [STATISTICS.md](STATISTICS.md) cho điều kiện,
fallback và cách đo hiệu năng. Mỗi kết luận thắng/thua cần chênh lệch,
CI, effect size và p đã hiệu chỉnh, cùng bảng/log làm căn cứ.
“Chưa đủ bằng chứng khác biệt” không phải chứng minh tương đương.
Chưa có kết luận thống kê trên benchmark thật. Dữ liệu trong thư mục test
giả lập chỉ kiểm thử script, không dùng vào phần kết quả nghiên cứu.

## Thảo luận và hạn chế

Ưu điểm hiện có là mô hình/hàm đánh giá dùng chung, mã thuật toán tách
module, các thành phần I-WOA có thể bật/tắt để kiểm tra đóng góp. Đây là
đặc tính triển khai, không phải bằng chứng chất lượng nghiệm cao hơn.

Trường hợp thất bại cần báo cáo gồm không tìm được nghiệm khả thi, không
đạt ngưỡng mục tiêu, độ phủ bão hòa nhưng E/I khác nhau và I-WOA thua đối
chứng ở cùng FE. Hiện chưa có log thật để xác định tần suất hoặc nguyên nhân.

Giới hạn: E và I là proxy; chưa mô hình hóa đầy đủ công suất đẩy, thời gian
nhiệm vụ, nhiễu đồng kênh, dung lượng, backhaul, indoor, che khuất cụ thể
hoặc điều khiển bay. Các ràng buộc mô phỏng không bảo đảm an toàn thực tế.
Không suy ra khả năng triển khai thời gian thực từ thời gian một lần chạy.

Hướng tiếp theo: chốt seed và thiết kế trước thực thi; kiểm tra optimizer khi được yêu cầu, rồi chạy study và đối chiếu artifact. Runner FE đã có mã nhưng vẫn cần xác minh đầy đủ trước khi gọi kết quả là tái lập được. Không tự chạy smoke trong lượt chỉ yêu cầu tài liệu.
Chỉ mở rộng năng lượng hoặc SINR sau khi phân biệt rõ thay đổi mô hình và
thay đổi thuật toán, đồng thời chạy lại đối chứng tương ứng.

## Tài liệu tham khảo và quyền sở hữu công thức

Công thức tổng có trọng số và tỷ lệ UE đạt ngưỡng cho bốn UAV là **phần
nhóm đề xuất**, không ghi là trích nguyên từ bài báo. Chưa có xác nhận
sinh viên tự đọc, nên chưa viết “độ phủ được định nghĩa theo hướng của”
các nguồn dưới đây như một trích dẫn đã được nhóm xác minh:

- [Alzenad và cộng sự](https://arxiv.org/pdf/1705.03415): tài liệu ứng viên
  cho mục tiêu phủ người dùng; **cần sinh viên tự đọc xác minh** phạm vi.
- [Mozaffari và cộng sự](https://arxiv.org/pdf/1606.01962): tài liệu ứng
  viên về đa UAV và nhiễu; **cần sinh viên tự đọc xác minh** phần kế thừa.
- [Zeng và cộng sự](https://arxiv.org/pdf/1804.02238): chỉ cho **hướng mở
  rộng năng lượng**; Fitness hiện tại chưa triển khai mô hình bài này.

Các danh mục thư mục học thuật trong DW là ứng viên chưa được sinh viên
xác minh. Không dùng chúng để bảo vệ trọng số hoặc khẳng định triệt để
thoát cực trị. Việc đọc của công cụ không thay xác nhận đọc của sinh viên.

## Kiểm tra truy xuất số liệu

Xem [REPORT_EVIDENCE.md](REPORT_EVIDENCE.md) và CSV kèm theo. Chỉ các giá trị
được chấp nhận có nguồn file và dòng dữ liệu. Tham số, công thức và quy
trình định trước được phân loại riêng với kết quả đo. Khi chưa có benchmark
log, không thể hoàn thiện bảng kết quả cuối hoặc xác nhận mọi con số lịch sử.
