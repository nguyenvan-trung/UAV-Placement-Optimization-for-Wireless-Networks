# Tối ưu vị trí UAV cho mạng không dây

Tìm vị trí ba chiều cho các UAV phát sóng để phục vụ một tập người dùng cố định. Người đọc có thể theo dõi dự án theo thứ tự: **bài toán → mô hình → thuật toán → thiết kế thí nghiệm → kết quả có nguồn**.

**Trạng thái:** study mới 500 CSV / 30 trường hợp / 100 vòng chưa chạy; seed chưa chốt. Đọc [rà soát trước chạy](implementation/docs/PRE_RUN_REVIEW.md) để biết các phần cần xử lý. Không có thứ hạng thực nghiệm mới trong trang này.

## Mục lục

1. [Mô hình tổng quan](#tong-quan)
2. [Đầu vào, đầu ra và một ví dụ](#dau-vao)
3. [Cách chấm một phương án](#fitness)
4. [Sáu thuật toán và 30 trường hợp](#thuat-toan)
5. [Ba luồng thực thi](#luong-chay)
6. [Bản đồ thư mục](#thu-muc)
7. [Lộ trình đọc tài liệu](#lo-trinh)
8. [Nguồn và trạng thái kiểm chứng](#nguon)

<a id="tong-quan"></a>

## 1. Mô hình tổng quan

![Mô hình tổng quan: dữ liệu user, bài toán, thuật toán, fitness, lưu task và tổng hợp](implementation/docs/assets/overview.svg)

**Cách đọc sơ đồ:** bắt đầu từ tọa độ user; tạo bài toán đặt UAV; thuật toán liên tục đề xuất cấu hình và nhận điểm fitness; cuối cùng lưu lịch sử để tổng hợp. Khối “đánh giá” được gọi nhiều lần trong tìm kiếm, không phải chỉ một lần sau khi thuật toán kết thúc.

| Khối | Giải thích |
|---|---|
| Dữ liệu user | Cùng một CSV được dùng cho mọi case và seed; thuật toán không di chuyển user |
| Bài toán | Xác định nghiệm hợp lệ và dùng chung cách chấm |
| Thuật toán | Khác nhau ở cách tạo/cập nhật ứng viên |
| Fitness | Cùng mô hình để đối chứng có ý nghĩa |
| Task | Một bộ dataset–case–seed; là đơn vị lưu/tiếp tục |
| Báo cáo | Đọc artifact; không lấy ảnh minh họa làm số đo thuật toán |

Sơ đồ do dự án biên soạn từ [runner notebook](implementation/src/notebook_study.py) và [bài toán](implementation/src/problem/objective.py), không phải hình lấy từ bài báo.

<a id="dau-vao"></a>

## 2. Đầu vào, đầu ra và một ví dụ

**Đầu vào:** một CSV có cột user_id, x_m, y_m, z_m, demand. Tọa độ dùng mét. Bộ hiện có gồm 500 file, 10 mức từ 50 đến 500 user, mỗi mức 50 file. User có độ cao 0–132 m theo rà soát, nên không gọi toàn bộ bộ dữ liệu là user mặt đất.

**Một nghiệm:** vector ghép tọa độ N UAV. Với N=4, nghiệm có D=12 số:

`X = [x1, y1, z1, x2, y2, z2, x3, y3, z3, x4, y4, z4]`.

**Ví dụ minh họa:** dataset 100 user, một ứng viên chứa vị trí của cả bốn UAV. Quần thể P=25 nghĩa là có 25 cấu hình bốn UAV, không phải 25 UAV. Sau 100 vòng, lưu best đã đánh giá và các mốc lịch sử. Đây là diễn giải cấu trúc, không phải số đo của một lần chạy.

Định dạng đầy đủ: [DATA_FORMAT](implementation/docs/DATA_FORMAT.md).

<a id="fitness"></a>

## 3. Cách chấm một phương án

`F = 0,6 × C − 0,2 × E − 0,2 × I`, cực đại hóa.

| Thành phần | Định nghĩa dễ đọc | Chiều mong muốn |
|---|---|---|
| C | Tỷ lệ user được ít nhất một UAV phủ theo ngưỡng SNR | Cao |
| E | Proxy công suất trung bình chuẩn hóa theo độ cao | Thấp |
| I | Tỷ lệ user có từ hai liên kết SNR đạt ngưỡng | Thấp |

E chưa phải năng lượng Joule; I chưa phải công suất nhiễu. Trọng số là lựa chọn thiết kế, không phải tỷ lệ chuẩn của ngành. Công thức có bảng ký hiệu, đơn vị và nguồn tại [REPORT](implementation/docs/REPORT.md); bảng truy nguồn tại [SOURCES](implementation/docs/SOURCES.md).

<a id="thuat-toan"></a>

## 4. Sáu thuật toán và 30 trường hợp

| Thuật toán chính | Ý tưởng | Giải thích chi tiết |
|---|---|---|
| GA | Chọn cha mẹ, lai ghép, đột biến và giữ elite | [DWGA](implementation/docs/DWGA.md) |
| PSO | Di chuyển theo vận tốc, pbest và gbest | [DWPSO](implementation/docs/DWPSO.md) |
| WOA | Bao vây, khám phá hoặc xoắn ốc quanh best | [DWWOA](implementation/docs/DWWOA.md) |
| H-PSO-GA | Bước PSO rồi crossover/mutation | [DWH_PSO_GA](implementation/docs/DWH_PSO_GA.md) |
| H-WOA-PSO | Trộn hai đề xuất trên mỗi cá thể | [DWH_WOA_PSO](implementation/docs/DWH_WOA_PSO.md) |
| I-WOA | WOA thêm K-Means, OBL và Lévy | [DWI_WOA](implementation/docs/DWI_WOA.md) |

Study mở rộng thành 24 case của ba họ WOA/PSO/GA, hai bản lai đầy đủ và bốn case ablation bản lai: **30 case duy nhất**. Một case có thể xuất hiện trong nhiều bảng nhưng không phải chạy lại. Xem bảng bật/tắt trong [NOTEBOOK_STUDY](implementation/docs/NOTEBOOK_STUDY.md).

<a id="luong-chay"></a>

## 5. Ba luồng thực thi

| Luồng | Đầu vào | Ngân sách và phạm vi |
|---|---|---|
| Notebook hiện tại | 500 CSV có sẵn | 30 case, 100 vòng, P=25, N=4 |
| Benchmark FE | Dữ liệu sinh từ YAML/manifest | Mặc định 3030 FE, P=30; schema riêng |
| Script CSV legacy | CSV có sẵn | Một dataset hoặc batch sáu thuật toán theo vòng |

FE là một lần đánh giá fitness. Cùng vòng không bảo đảm cùng FE, đặc biệt khi có OBL/Lévy. Không gộp ba luồng như cùng giao thức. Hướng dẫn môi trường và thực thi: [REPRODUCE](REPRODUCE.md).

<a id="thu-muc"></a>

## 6. Bản đồ thư mục

| Đường dẫn từ gốc repository | Chứa gì? |
|---|---|
| configs/ | Cấu hình notebook và FE |
| data/stores/ | Tọa độ user đầu vào |
| data/views/ | Ảnh quan sát input |
| implementation/src/ | Mô hình và thuật toán |
| implementation/notebooks/ | Notebook study và trình bày |
| implementation/scripts/ | Điểm vào CLI/analyzer |
| implementation/docs/ | Phương pháp, thiết kế, nguồn và hướng dẫn |
| implementation/docs/assets/ | Sơ đồ SVG nhúng vào Markdown |
| implementation/tests/ | Kiểm tra mã |
| implementation/results/ | Đầu ra khi được thực thi |
| documents/ | Danh mục tài liệu học thuật |
| plan/ | Kế hoạch/phân công |
| figures/, reports/, tmp_audit/ | Minh họa, kiểm toán, kiểm tra; xác minh nguồn trước khi dùng |

<a id="lo-trinh"></a>

## 7. Lộ trình đọc tài liệu

| Thứ tự | Tài liệu | Sau khi đọc cần hiểu |
|---|---|---|
| 1 | README hiện tại | Dự án làm gì và đang ở đâu |
| 2 | [NOTE](NOTE.md) | Câu hỏi nghiên cứu, logic thiết kế |
| 3 | [REPORT](implementation/docs/REPORT.md) | Cách tính điểm và giới hạn |
| 4 | Các chương thuật toán ở mục 4 | Vì sao mỗi phương pháp tạo ứng viên khác nhau |
| 5 | [NOTEBOOK_STUDY](implementation/docs/NOTEBOOK_STUDY.md) | Đối chứng và các bảng sẽ được tạo |
| 6 | [REPRODUCE](REPRODUCE.md) | Cách chuẩn bị và thực thi khi được duyệt |
| 7 | [TALK](TALK.md) | Cách kể lại toàn bộ dự án và trả lời phản biện |

[Mục lục toàn bộ tài liệu](implementation/docs/README.md) có các nhánh chuyên sâu về thuật ngữ, thống kê, độ nhạy và bằng chứng.

<a id="nguon"></a>

## 8. Nguồn và trạng thái kiểm chứng

[SOURCES](implementation/docs/SOURCES.md) tách nguồn học thuật, lựa chọn riêng của nhóm và mã triển khai. Mỗi chương công thức dẫn về phần tương ứng; không quy toàn bộ phương pháp cho một bài báo.

Hiện có mã và thiết kế, chưa có study mới hoàn tất. Notebook còn mục cần xử lý trong PRE_RUN_REVIEW; chưa bật ô chạy và chưa tự chọn seed. Người đọc có thể xem toàn bộ tài liệu mà không thực thi Python.

Nhóm: Nguyễn Văn Trung, Hoàng Văn Trường, Nguyễn Minh Hiếu.
