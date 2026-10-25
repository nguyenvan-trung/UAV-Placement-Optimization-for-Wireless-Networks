# Nguồn tham khảo và quyền sở hữu công thức

[Mục lục](README.md) · [Mô hình](REPORT.md) · [Quy tắc biên tập](DOCUMENTATION_GUIDE.md)

Trang này trả lời: **công thức tham khảo ở đâu, phần nào là điều chỉnh của dự án, và đối chiếu mã nào?** Đối chiếu web ngày 25/10/2026 không thay việc nhóm đọc toàn văn trước khi nộp báo cáo.

## Mục lục

- [Mô hình A2G](#a2g)
- [GA](#ga)
- [PSO](#pso)
- [WOA](#woa)
- [K-Means, OBL và Lévy](#operators)
- [Hai phương pháp lai](#hybrid)
- [Các công thức riêng của dự án](#project)
- [Hiển thị trên GitHub](#github)

<a id="a2g"></a>

## A2G: LoS, suy hao và công suất thu

**[A2G-1]** M. Alzenad, A. El-Keyi, F. Lagum, H. Yanikomeroglu, *3D Placement of an Unmanned Aerial Vehicle Base Station (UAV-BS) for Energy-Efficient Maximal Coverage*, 2017. [Toàn văn tác giả trên arXiv](https://arxiv.org/html/1705.03415).

Đã đối chiếu mục II: công thức (1) xác suất LoS; (2) suy hao LoS/NLoS; (3) suy hao trung bình; (5) công suất thu. Đây là nguồn đối chiếu mô hình kênh, không phải nguồn cho toàn bộ F/C/E/I của dự án.

**[A2G-2]** A. Al-Hourani, S. Kandeepan, S. Lardner, *Optimal LAP Altitude for Maximum Coverage*, 2014. [DOI gốc](https://doi.org/10.1109/LWC.2014.2342736). Đây là nguồn mô hình nền mà A2G-1 dẫn lại; chưa đọc lại toàn văn trực tiếp trong lượt này.

**Khác biệt triển khai:** code dùng tọa độ user 3D; ép tỷ số góc âm về 0; dùng giá trị tham số trong network.py. Không suy ra các lựa chọn mở rộng này đã được xác nhận vật lý từ bài báo cho user mặt đất.

Mã: [channel.py](../src/physics/channel.py). Công thức và bảng ký hiệu: [REPORT](REPORT.md).

<a id="ga"></a>

## GA: nguyên lý tiến hóa và toán tử liên tục

**[GA-1]** F. Herrera, M. Lozano, J. L. Verdegay, *Tackling Real-Coded Genetic Algorithms: Operators and Tools for Behavioural Analysis*, Artificial Intelligence Review 12, 265–319, 1998.

- [DOI](https://doi.org/10.1023/A:1006504901164).
- [Danh mục của nhóm tác giả, mục 0067](https://sci2s.ugr.es/publications?auth=M.+Lozano&pubType=intJournal).

Đã đối chiếu thông tin thư mục trên trang nhóm tác giả; chưa xác nhận toàn bộ phép triển khai theo từng trang của toàn văn. Dùng nguồn cho nền tảng GA mã thực; công thức mô tả chính xác code hiện tại lấy từ các module GA.

Tournament k=3, arithmetic crossover theo từng tọa độ, Gaussian scale=0,1 và elite=2 là lựa chọn cụ thể của code, không khẳng định nguyên bộ tham số được trích nguyên từ GA-1.

Mã: [selection](../src/algorithms/GA/selection.py), [crossover](../src/algorithms/GA/crossover.py), [mutation](../src/algorithms/GA/mutation.py), [replacement](../src/algorithms/GA/replacement.py). Đọc [DWGA](DWGA.md).

<a id="pso"></a>

## PSO: vận tốc và bộ nhớ

**[PSO-1]** J. Kennedy, R. Eberhart, *Particle Swarm Optimization*, ICNN 1995. [DOI gốc](https://doi.org/10.1109/ICNN.1995.488968). Trang IEEE yêu cầu kiểm tra truy cập trong lượt này; chưa dùng toàn văn đó để chứng nhận từng công thức/siêu tham số.

**[PSO-2]** Y. Shi, R. C. Eberhart, *Empirical Study of Particle Swarm Optimization*, CEC 1999. [Bản PDF trên máy chủ đại học](https://faculty.washington.edu/paymana/swarm/shi99-cec.pdf). Tài liệu liên quan nghiên cứu quán tính giảm tuyến tính; không phải bằng chứng lịch 0,9→0,4 của dự án tối ưu trên mọi bài toán.

Nguồn chính xác cho công thức đang thực thi là [velocity_update.py](../src/algorithms/PSO/velocity_update.py) và [optimizer.py](../src/algorithms/PSO/optimizer.py). Giới hạn vận tốc, xử lý biên và các hệ số là cấu hình của dự án. Đọc [DWPSO](DWPSO.md).

<a id="woa"></a>

## WOA: ba cơ chế tìm kiếm

**[WOA-1]** S. Mirjalili, A. Lewis, *The Whale Optimization Algorithm*, Advances in Engineering Software 95, 51–67, 2016.

- [DOI](https://doi.org/10.1016/j.advengsoft.2016.01.008).
- [Trang WOA của tác giả](https://seyedalimirjalili.com/woa).

Đã xem trang tác giả mô tả ba toán tử: khám phá, bao vây và bubble-net; DOI bị hạn chế truy cập trong lượt này. Công thức chi tiết trong tài liệu dự án được đối chiếu code, không giả định đã xác minh từng phương trình của bản in.

Trong code, điều kiện chọn nhánh dùng norm(A)/sqrt(D); đây phải được ghi rõ thay vì nhập nhằng với trị tuyệt đối từng tọa độ. Đọc [DWWOA](DWWOA.md).

<a id="operators"></a>

## K-Means, OBL và Lévy

| Mã nguồn tham khảo | Nguồn và phạm vi |
|---|---|
| K-1 | [Tài liệu KMeans chính thức](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html): thư viện được gọi; code đặt n_clusters=N, n_init=10 và random_state |
| O-1 | H. R. Tizhoosh, *Opposition-Based Learning: A New Scheme for Machine Intelligence*, 2005; [DOI](https://doi.org/10.1109/CIMCA.2005.1631345). IEEE chặn truy cập tự động trong lượt này; công thức triển khai đối chiếu obl.py |
| L-1 | X.-S. Yang, S. Deb, *Cuckoo Search via Lévy Flights*, NaBIC 2009; [bản tác giả](https://arxiv.org/abs/1003.1594). Nguồn ý tưởng Lévy trong metaheuristic, không phải bài gốc I-WOA của dự án |

Công thức sigma/bước nhảy được mô tả theo [levy_flight.py](../src/algorithms/I_WOA/levy_flight.py). Chưa xác minh nguồn gốc thuật toán Mantegna từ bài sơ cấp trong lượt này; không gán mọi chi tiết tính sigma cho L-1.

Vị trí chèn K/O/L, xác suất 0,2/0,3, step size 0,05, việc thay một cá thể và quy tắc nhận nếu tốt hơn là quyết định triển khai. Đọc [DWI_WOA](DWI_WOA.md) và [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md).

<a id="hybrid"></a>

## Hai phương pháp lai

Trình tự PSO→crossover→mutation và tổ hợp vị trí WOA/PSO 0,5/0,5 được tài liệu hóa theo mã riêng của repository. Không khẳng định chúng sao chép nguyên vẹn một thuật toán của bài báo chỉ vì cùng tên “hybrid”.

Mã: [hybrid_pso_ga.py](../src/algorithms/hybrid/hybrid_pso_ga.py), [hybrid_woa_pso.py](../src/algorithms/hybrid/hybrid_woa_pso.py). Nguyên lý PSO/GA/WOA có nguồn phía trên. Tài liệu nghiên cứu lai bổ sung trong [documents](../../documents/README.md) cần được đọc/xác minh riêng trước khi gán công thức cụ thể.

<a id="project"></a>

## Các công thức và giả định riêng của dự án

| Nội dung | Nguồn đúng để ghi |
|---|---|
| F=0,6C−0,2E−0,2I | Định nghĩa tổng có trọng số của dự án; metrics.py |
| C=max-SNR đạt ngưỡng trên nhiều UAV | Định nghĩa triển khai của dự án, lấy cảm hứng bài toán coverage; không trích nguyên A2G-1 |
| I=tỷ lệ user có từ hai liên kết đạt ngưỡng | Proxy chồng lấn của dự án; không phải diện tích/công suất nhiễu từ nguồn khác |
| E=proxy công suất theo độ cao rồi chuẩn hóa | Giả định dự án, chưa hiệu chuẩn vật lý |
| Hover 100 W, tăng 50%, ngưỡng 18 dB | Tham số mô phỏng; chưa có nguồn xác nhận chung |
| D_min=10 m | Ràng buộc mô phỏng, không phải chuẩn an toàn bay |
| 30 case, 100 vòng và phép gộp | Giao thức nghiên cứu hiện tại; notebook_study.py |

Khi báo cáo cần ghi cả nguồn ý tưởng và khác biệt so với nguồn. Không dùng “chuẩn IEEE”, “tỷ lệ vàng”, “đảm bảo toàn cục” thay cho bằng chứng.

<a id="github"></a>

## Hiển thị trên GitHub

- [GitHub: công thức toán](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions): dùng khối $$ riêng dòng hoặc math fence; công thức trong dòng dùng $.
- [GitHub: sơ đồ](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams): Mermaid là một lựa chọn; bộ tài liệu này ưu tiên SVG tĩnh để mô hình mở trực tiếp.
- Các SVG trong [assets](assets/) do dự án biên soạn theo code, không phải ảnh chụp kết quả hoặc hình sao chép bài báo.
