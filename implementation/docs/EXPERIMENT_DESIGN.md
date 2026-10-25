# Thiết kế đối chứng FE

## Mục lục

1. [Phạm vi và các tệp liên quan](#doc-section-01)
2. [Cơ chế đếm và dừng](#doc-section-02)


[Mục lục](README.md) · [Người mới](PROJECT_GUIDE.md) · [Thuật ngữ](GLOSSARY.md) · [Study notebook](NOTEBOOK_STUDY.md)


Mục đích: mô tả hành vi chế độ FE; hạ tầng bổ sung ngày 24/10/2026. Đây là giao thức riêng, không phải notebook 100 vòng.

<a id="doc-section-01"></a>

## Phạm vi và các tệp liên quan

[benchmark.yaml](../../configs/benchmark.yaml) khai báo quần thể 30, max_fe=3030, các mức UE/phân bố và số instance/run. [run_benchmark.py](../scripts/run_benchmark.py) sinh dữ liệu từ manifest rồi gọi optimizer. Tọa độ không lấy trực tiếp từ 500 CSV. Các giá trị trong YAML là thiết kế, chưa phải kết quả đã đo.

Notebook hiện tại dùng 500 CSV, quần thể 25 và 100 vòng, xem [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md). Hai luồng có schema và phạm vi thời gian khác nhau. Cách chạy khi có yêu cầu: [REPRODUCE](../../REPRODUCE.md); cách đọc log: [DATA_FORMAT](DATA_FORMAT.md).

<a id="doc-section-02"></a>

## Cơ chế đếm và dừng

`optimize(problem)` giữ chế độ legacy. `optimize(problem,max_fe=...,
initial_population=...)` bật wrapper trong algorithms/base/budget.py.
Wrapper truyền CountedProblem vào lõi, nên mọi problem.evaluate trong
khởi tạo, GA, PSO, WOA và hybrid đều qua FitnessCounter. OBL/Lévy được gắn
nhãn riêng. Không có phép tính Fitness ngầm trong K-Means.

| Phần | Cách tính FE |
|---|---|
| Khởi tạo mỗi thuật toán | Một FE mỗi cá thể, kể cả không khả thi |
| GA offspring | Một FE mỗi con được đánh giá; quần thể lẻ có thể tạo dư một con, vẫn tính FE |
| PSO/WOA/hybrid core | Một FE mỗi vị trí mới sau xử lý biên |
| OBL | Một FE mỗi nghiệm đối lập, khởi tạo và dynamic đều có nhãn obl |
| Lévy | Một FE mỗi đề xuất được đánh giá, không chỉ nghiệm được chấp nhận |
| K-Means | Không tăng FE riêng; thay cá thể đầu trước đánh giá, nhưng có chi phí thời gian |
| So sánh best | Không đánh giá thêm |
| Final C/E/I và khả thi | Hàm gốc, ngoài FE tìm kiếm; tính trong thời gian task được công bố |

Counter giữ best của **mọi nghiệm đã đánh giá**, kể cả nghiệm cuối khi bị
ngắt giữa quần thể/OBL. BudgetExhausted chặn trước lời gọi vượt ngân sách.
Không early-stop khi đạt target. FE cuối có trong lịch sử dù không chia hết
cho chu kỳ log. Best âm vô cùng nghĩa không tìm được nghiệm khả thi; log
ghi feasible=false và metric trống, không biến thành nghiệm hợp lệ.

Lịch a của WOA theo tiến độ FE tại mỗi đề xuất; quán tính PSO/hybrid lấy
tiến độ FE lúc bắt đầu sweep. Vì vậy quán tính không đổi giữa các cá thể
trong cùng sweep, nhưng không còn dùng t/MaxIter trong chế độ FE.
iterations_done đếm sweep hoàn tất, không đếm sweep đang dở.

Quần thể nền sinh từ một stream riêng của algo_seed, dùng chung cho mọi
thuật toán/biến thể/cấu hình. PSO vẫn có vận tốc riêng. K-Means cố ý thay
cá thể đầu khi bật: không tuyên bố quần thể hiệu dụng sau cải tiến giống
hệt baseline. solutions JSON lưu nền và hash để kiểm chứng.

Seed manifest tạo bằng SeedSequence; mỗi instance có data_seed, mỗi run
có algo_seed. Hai loại seed và hai purpose không giao nhau trong manifest
được sinh; runner đối chiếu toàn bộ manifest với config trước khi chạy.

Khác biệt chế độ FE về lịch điều khiển, khởi tạo ghép cặp và giữ mọi best
là thay đổi giao thức tối ưu được yêu cầu, không phải thay công thức Fitness.
Không gộp kết quả iterations cũ vào kết quả FE mới.

Resume dựa trên task ID + hash source/config/manifest/worker. Không hỗ trợ
hai coordinator đồng thời ghi cùng output. Target Fitness chưa chốt: null
được lưu thiếu trong CSV, không được diễn giải thành tỷ lệ thất bại.
