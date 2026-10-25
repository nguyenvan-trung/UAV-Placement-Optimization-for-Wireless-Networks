# Rà soát trước khi chạy study

## Mục lục

1. [Các kiểm tra đã làm](#doc-section-01)
2. [Cần xử lý/duyệt trước study](#doc-section-02)
3. [Xác minh tiếp theo cần thống nhất](#doc-section-03)
4. [Trạng thái sau rà soát](#doc-section-04)


[Mục lục](README.md) · [Thiết kế](NOTEBOOK_STUDY.md) · [Cấu hình](../../configs/notebook_study.json)

Ngày rà soát: 25/10/2026. Chỉ đọc mã/dữ liệu, kiểm tra cú pháp, schema notebook, requirements và liên kết tài liệu. Không cài thư viện, sửa nguồn/cấu hình, chạy optimizer, pytest hoặc study trong lượt này.

<a id="doc-section-01"></a>

## Các kiểm tra đã làm

| Phạm vi | Kết quả |
|---|---|
| Python trong src/scripts/tests | 111 file phân tích cú pháp được; không chứng minh đúng hành vi |
| Dữ liệu CSV | 500 file, qua loader/validator; mỗi mức 50–500 user có 50 file |
| User trùng ID | Không có file mất dòng khi bỏ ID trùng |
| Độ cao user | 0–132 m; không phải toàn bộ user mặt đất |
| Registry | 30 case duy nhất; tạo được đối tượng optimizer, không gọi optimize |
| Notebook | 15 ô, schema/cú pháp hợp lệ; chưa có ô thực thi |
| Dependencies hiện tại | Import được các thư viện tính toán, pytest, nbformat, ipykernel được kiểm tra |
| Markdown | 35 file, 393 liên kết tệp nội bộ, không có đích tệp bị thiếu |
| Kết quả study | Chưa có; results chỉ có README và .gitkeep |

<a id="doc-section-02"></a>

## Cần xử lý/duyệt trước study

### 1. Danh sách seed chưa có

configs/notebook_study.json đang seeds=[]. run_study từ chối chạy nếu ít hơn hai seed. Cần chốt số seed và danh sách trước khi có kết quả. Khối lượng là 15.000 task/seed: 5 seed tương ứng 75.000 task, 30 seed tương ứng 450.000 task. Đây là số lượt dự kiến, chưa phải số đã chạy.

### 2. Requirements có dòng sai cú pháp

implementation/requirements.txt dòng 11: `scikit-learn --Required by I-WOA and K-Means`. Bộ phân tích requirement từ chối dòng này; pip sẽ không hiểu nó như chú thích hợp lệ. scikit-learn đã có ở dòng riêng phía trên. Đề xuất bỏ dòng trùng hoặc chuyển nội dung giải thích thành comment bắt đầu bằng `#`.

Môi trường hiện tại đã import được sklearn; lỗi file requirements chủ yếu chặn cài đặt/tái lập môi trường sạch, không phải bằng chứng optimizer hiện tại sẽ lỗi import.

### 3. Notebook còn lỗi tiếng Việt

13/15 ô có chuỗi tiếng Việt bị thay bằng dấu hỏi. Cú pháp Python và schema vẫn hợp lệ nhưng nội dung không đạt yêu cầu đọc hiểu. Đề xuất viết lại phần Markdown/nhãn/thông báo bằng UTF-8, giữ nguyên code tính toán và khóa chạy mặc định.

### 4. Cần củng cố kiểm tra task khi resume và tổng hợp

Trong notebook_study.py, resume hiện bỏ qua task dựa trên file tồn tại. Kết thúc runner kiểm tra số dòng và trùng khóa; build_tables đối chiếu tập khóa và mốc iteration. Chưa kiểm tra đầy đủ identity/giá trị hữu hạn/khả thi/tính nhất quán result-history của mỗi artifact cũ trước khi dùng.

Đề xuất validator chung cho task: đúng dataset–case–seed, 101 mốc, fitness hữu hạn và không giảm, FE/thời gian hợp lệ, nghiệm/metric cuối nhất quán. Task lỗi phải được báo rõ và từ chối dùng; không tự bỏ dữ liệu hay tự đánh dấu complete.

Đây là lỗ hổng xác minh khi file cũ hỏng hoặc bị sửa, không phải tuyên bố các task hỏng đang tồn tại.

<a id="doc-section-03"></a>

## Xác minh tiếp theo cần thống nhất

Sau khi duyệt sửa các phần trên: kiểm tra hồi quy và chạy thử có giới hạn trên các case mới, ghi output kiểm tra riêng, không gọi đó là kết quả nghiên cứu. Chỉ sau khi đạt kiểm tra và đã chốt seed mới chạy 500 CSV. Mã hiện chưa được xác minh toàn trình cho study 30 case.

Giữ nguyên 500 CSV đã chọn, gồm độ cao user hiện có; không chuyển z về 0 hoặc đổi sang bộ sinh scenario. Nếu muốn thí nghiệm toàn user mặt đất thì phải là một thiết kế mới.

Metadata môi trường notebook còn ít hơn runner FE; kiểm định/CI cho 30 case cũng chưa có. Các bảng hiện tại chỉ cho kết luận mô tả, không tự chứng minh khác biệt có ý nghĩa thống kê.

<a id="doc-section-04"></a>

## Trạng thái sau rà soát

Chờ duyệt phương án sửa và lựa chọn seed. Chưa khởi chạy benchmark.
