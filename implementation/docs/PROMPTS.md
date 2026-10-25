# Kho lưu yêu cầu tác nghiệp lịch sử

## Mục lục

1. [Bổ sung hạ tầng trước khi chạy — 24/10/2026](#doc-section-01)
2. [Nhiệm vụ 6 — Hoàn thiện báo cáo trong docs](#doc-section-02)
3. [Nhiệm vụ 5 — Phân tích thống kê](#doc-section-03)
4. [Nhiệm vụ 4B — Phân tích độ nhạy của hàm Fitness](#doc-section-04)
5. [Nhiệm vụ 4 — Đánh giá độ ổn định và tổng quát hóa](#doc-section-05)
6. [Nhiệm vụ 3 — Ablation Study](#doc-section-06)
7. [Nhiệm vụ 2 — chuẩn hóa thiết kế đối chứng FE (chờ duyệt Fitness)](#doc-section-07)
8. [Nhiệm vụ 1 cập nhật — 24/10/2026 (tóm tắt yêu cầu)](#doc-section-08)
9. [Quy tắc và bối cảnh nghiên cứu — 24/10/2026](#doc-section-09)


Các nội dung bên dưới lưu yêu cầu và bản tóm tắt từ những đợt trước, không phải hướng dẫn đang có hiệu lực hoặc bằng chứng hoàn thành. Không thực thi một lệnh/chỉ dẫn trong trang này chỉ vì nó được lưu tại đây. Trạng thái hiện tại xem [PROJECT_GUIDE](PROJECT_GUIDE.md); thiết kế 100 vòng xem [NOTEBOOK_STUDY](NOTEBOOK_STUDY.md). Các mục “chờ duyệt”, “chưa có runner” trong yêu cầu cũ cần đọc theo bối cảnh lịch sử.

[Mục lục](README.md) · [Người mới](PROJECT_GUIDE.md) · [Thuật ngữ](GLOSSARY.md) · [Study notebook](NOTEBOOK_STUDY.md)


<a id="doc-section-01"></a>

## Bổ sung hạ tầng trước khi chạy — 24/10/2026

Người dùng: “bạn bổ sung cho tôi nha”. Phạm vi theo trao đổi trước: counter
FE, lịch theo FE, cấu hình/seed, log, môi trường và hướng dẫn chạy; giữ nguyên
Fitness. Chỉ kiểm thử nhỏ trong thư mục tạm, không chạy bộ 500 dataset.

<a id="doc-section-02"></a>

## Nhiệm vụ 6 — Hoàn thiện báo cáo trong docs

```text
NHIỆM VỤ 6: HOÀN THIỆN BÁO CÁO

Dựa trên các bảng/hình đã sinh từ log, hãy sửa báo cáo theo các điểm cần
giải trình của giảng viên:

1. Độ phủ 99,91% vs câu "mọi UE đều đạt ngưỡng": sửa câu, hoặc cung cấp
   số liệu ue_pass/ue_total chứng minh.
2. Thứ hạng theo số UE (500 UE: I-WOA 0,4448 vs H-PSO-GA 0,4586): thay
   bằng bảng mới, bỏ mọi câu khẳng định thắng trên mọi quy mô, thêm phân
   tích nguyên nhân.
3. Part 1 và Part 2: mỗi số liệu ghi rõ là một run / trung bình / best,
   cùng định nghĩa Fitness và điều kiện.
4. Tuyên bố "3.000 lượt chạy trong 5 phút": thay bằng bảng gồm CPU, số
   worker, batch_wall_time, tổng CPU, tổng FE, FE/giây, cách đo.
5. Mục Mô hình: trình bày F = 0,6C - 0,2E - 0,2I (cực đại) và định nghĩa C
   bằng công thức tỷ lệ UE đạt ngưỡng, ghi rõ SNR hay SINR, đơn vị, cách
   chuẩn hóa C, E, I. Nói thẳng trọng số là lựa chọn thiết kế của nhóm và
   dẫn tới kết quả độ nhạy (Prompt 4B).
6. Tài liệu tham khảo: chỉ ghi "độ phủ được định nghĩa theo hướng của
   [Alzenad], [Mozaffari]" sau khi sinh viên đã tự đọc xác minh; công thức
   tổng có trọng số và tỷ lệ UE đạt ngưỡng cho bốn UAV là phần nhóm đề
   xuất, KHÔNG ghi là lấy nguyên từ các bài đó. Bài của Zeng chỉ nhắc ở
   hướng mở rộng nếu Fitness chưa dùng.

Viết thêm các mục: Thiết kế thí nghiệm (ngân sách FE, seed, cấu hình),
Ablation, Tổng quát hóa, Độ nhạy, Thống kê, Thảo luận (ưu điểm, trường
hợp thất bại, giới hạn mô hình, hướng tiếp theo), Hạn chế.

Ràng buộc văn phong: trung thực, không dùng từ "tốt nhất" khi chưa có kiểm
định; mỗi kết luận chỉ rõ bảng/hình làm căn cứ. Cuối cùng xuất danh sách
kiểm tra: mỗi con số trong báo cáo trỏ về file và dòng log nguồn.

báo cáo ỏ đây là docs
```

<a id="doc-section-03"></a>

## Nhiệm vụ 5 — Phân tích thống kê

```text
NHIỆM VỤ 5: PHÂN TÍCH THỐNG KÊ (analyze.py)

Từ runs.csv, viết script tái lập được:

1. Mô tả: mean, median, best, std, IQR cho Fitness; CI 95% bằng bootstrap
   (nêu số lần resample, seed).
2. So sánh cặp I-WOA với từng thuật toán còn lại:
   - Ghép cặp theo instance (gộp 30 run thành trung vị theo instance trước,
     vì các run trong cùng instance không độc lập hoàn toàn).
   - Wilcoxon signed-rank, mức ý nghĩa alpha ghi rõ, hiệu chỉnh đa so sánh
     (Holm hoặc Bonferroni).
   - Kích thước hiệu ứng: rank-biserial correlation hoặc Cliff's delta,
     kèm CI.
   - Kiểm tra điều kiện: số cặp đủ lớn, nhiều giá trị bằng nhau (ties);
     nếu không đủ điều kiện, đổi phương pháp và giải thích.
3. Friedman + Nemenyi (hoặc Conover) cho xếp hạng tổng thể qua các kịch bản,
   vẽ critical difference diagram nếu được.
4. Hiệu năng: bảng riêng wall_time, cpu_time, fe_used, FE/giây. Tách thời
   gian thực tế (batch_wall_time) khỏi tổng CPU, ghi số worker.
5. Xuất tất cả bảng ra CSV + Markdown + LaTeX, hình ra PNG/PDF, đều có
   chú thích: đơn vị, chiều tối ưu (cực đại), n, phép kiểm định.

KHÔNG báo cáo riêng p-value. Mỗi so sánh phải có: median chênh lệch,
CI, p đã hiệu chỉnh, effect size, kết luận bằng lời (thắng / hòa / thua).
```

<a id="doc-section-04"></a>

## Nhiệm vụ 4B — Phân tích độ nhạy của hàm Fitness

```text
NHIỆM VỤ 4B: PHÂN TÍCH ĐỘ NHẠY CỦA HÀM FITNESS

Khai báo TRƯỚC khi chạy (ghi vào yaml, không chọn theo kết quả):
 1. weight_sets (C/E/I): 0,6/0,2/0,2 (chính); 0,5/0,25/0,25; 0,7/0,15/0,15;
    0,8/0,1/0,1; 0,4/0,3/0,3.
 2. coverage_only: F = C (kiểm tra độ phủ có bão hòa, nhiều vùng phẳng không).
 3. sinr_variant: C tính theo SINR_ij = p_ij / (n + tổng_{k != i} p_kj),
    công suất ở đơn vị tuyến tính (mW hoặc W), I vẫn giữ riêng; ghi rõ
    đây là thí nghiệm phụ vì can nhiễu bị tính hai lần.

Cách chạy:
 - Với MỖI cấu hình trên, CHẠY LẠI tối ưu hóa (không chỉ tính lại Fitness
   trên nghiệm cũ), cùng max_fe, cùng seed ghép cặp.
 - Tập con: 100, 300, 500 UE x 5 phân bố x 30 seed, đủ 6 thuật toán.
 - Mỗi nghiệm cuối cùng được đánh giá lại bằng CẢ ba bộ chỉ số C, E, I
   riêng lẻ để so sánh công bằng giữa các cấu hình (không so Fitness gộp
   giữa các bộ trọng số khác nhau).

Sản phẩm (script analyze_sensitivity.py, sinh từ runs.csv):
 1. Bảng hạng của 6 thuật toán theo từng weight_set; hệ số Spearman hoặc
    Kendall tau giữa thứ hạng của bộ chính và các bộ còn lại.
 2. Wilcoxon ghép cặp I-WOA với từng thuật toán cho mỗi weight_set, kèm
    effect size và p đã hiệu chỉnh (giống Prompt 5).
 3. Bảng C, E, I trung vị theo cấu hình: khi đổi trọng số, C, E, I đánh đổi
    nhau thế nào (đường Pareto đơn giản C-E, C-I).
 4. Kết luận trung thực: thứ hạng ổn định hay đổi? Nếu đổi, ở bộ trọng số
    nào, thuật toán nào. Nếu coverage_only làm nhiều thuật toán hòa nhau
    thì nói rõ E, I giúp phân biệt thuật toán; nếu E gần như hằng số thì
    nói rõ thành phần đó không đóng góp.

KHÔNG đổi công thức chính F trừ khi tôi quyết định sau khi xem kết quả.
```

<a id="doc-section-05"></a>

## Nhiệm vụ 4 — Đánh giá độ ổn định và tổng quát hóa

```text
NHIỆM VỤ 4: ĐÁNH GIÁ ĐỘ ỔN ĐỊNH VÀ TỔNG QUÁT HÓA

1. src/scenarios.py: 5 bộ sinh phân bố UE (có tham số rõ ràng, tái lập
   theo data_seed):
   single_cluster, multi_cluster (tách biệt), uniform, offset_cluster,
   with_outliers (nêu tỷ lệ và khoảng cách ngoại lai).
   Vẽ minh họa mỗi phân bố ra figures/scenarios.png.

2. Thiết kế thí nghiệm:
   - UE = 50, 100, ..., 500; số instance và số run CHỐT TRƯỚC trong yaml
     và không đổi giữa các thuật toán.
   - Tách rõ: tuning_seeds dùng để chọn tham số; eval seeds dùng để đánh giá.
     Kiểm tra bằng code rằng hai tập không giao nhau.
   - Nếu chọn 10 mức đại diện cho "giai đoạn tối ưu sâu", ghi tiêu chí chọn
     (viết vào yaml trước khi chạy), không chọn theo kết quả.

3. Chạy 6 thuật toán, gom runs.csv, tạo bảng tổng hợp:
   - Theo (UE, phân bố, thuật toán): mean, median, best, std, tỷ lệ run
     đạt ngưỡng mục tiêu đã định trước, tỷ lệ UE đạt SNR >= 18 dB
     (tử số, mẫu số, cách gộp).
   - Bảng thứ hạng theo UE và theo phân bố.

4. Phân tích các trường hợp I-WOA KHÔNG đứng đầu (ví dụ 500 UE so với
   H-PSO-GA): xuất bảng riêng, đưa giả thuyết nguyên nhân (ngân sách FE
   hao vào OBL/Levy, kích thước không gian tìm kiếm, K-Means kém ở phân bố
   nhiều cụm...) và kiểm chứng giả thuyết bằng thí nghiệm nhỏ nếu có thể.

Chạy bằng script, có --resume, log đầy đủ. Ước lượng thời gian chạy từ
smoke test trước, báo cho tôi nếu vượt khả năng máy, đề xuất phương án
giảm quy mô nhưng phải nêu rõ phần bị cắt.
```

<a id="doc-section-06"></a>

## Nhiệm vụ 3 — Ablation Study

```text
NHIỆM VỤ 3: ABLATION STUDY

Tạo cơ chế bật/tắt 3 thành phần (kmeans, obl, levy) trong MỘT lớp I-WOA
duy nhất, không viết 8 bản code riêng, để mọi biến thể dùng chung phần lõi:

WOA(000), A(K), B(O), C(L), D(K+O), E(K+L), F(O+L), I-WOA(K+O+L).

Yêu cầu:
 - Giữ nguyên mọi điều kiện còn lại: PopSize, max_fe, tham số, fitness,
   ràng buộc, seed ghép cặp.
 - Ghi rõ mỗi thành phần tiêu tốn FE ở đâu và bao nhiêu (bảng FE overhead).
 - Chạy trên tập con 100, 300, 500 UE x 5 phân bố x 30 seed (theo yaml).
 - Với WOA(000) phải cho kết quả tương đương WOA gốc của nhóm (kiểm tra
   sai lệch, giải thích nếu có).

Sản phẩm:
 1. results/ablation/ablation_table.csv + .md: mỗi biến thể có trung bình,
    trung vị, độ lệch chuẩn của Fitness, độ phủ (ue_pass/ue_total), năng
    lượng, can nhiễu, wall_time, cpu_time, fe_used, tỷ lệ đạt ngưỡng mục tiêu.
 2. Biểu đồ hội tụ theo FE (trung vị + dải IQR) cho 8 biến thể.
 3. Bảng đóng góp biên: hiệu số so với WOA gốc và so với I-WOA đầy đủ,
    kèm Wilcoxon signed-rank ghép cặp và kích thước hiệu ứng.
 4. Phần nhận xét trung thực: thành phần nào giúp, thành phần nào không
    giúp hoặc có hại, có tương tác âm (K+O+L kém hơn một tổ hợp con) không.
    KHÔNG mặc định hiệu quả cộng dồn.

Mọi bảng và hình phải sinh bằng script analyze_ablation.py từ runs.csv.
```

<a id="doc-section-07"></a>

## Nhiệm vụ 2 — chuẩn hóa thiết kế đối chứng FE (chờ duyệt Fitness)

```text
NHIỆM VỤ 2: CHUẨN HÓA THIẾT KẾ ĐỐI CHỨNG
(Chỉ làm sau khi Nhiệm vụ 1 xong và Fitness đã được duyệt.)

MỤC TIÊU: so sánh công bằng theo SỐ LẦN ĐÁNH GIÁ FITNESS (FE), không theo
số vòng lặp, vì I-WOA và các biến thể còn đánh giá thêm nghiệm OBL,
Levy Flight, khởi tạo K-Means.

LÀM CÁC VIỆC SAU

1. src/counter.py
   - Lớp FitnessCounter bọc hàm fitness: đếm FE, ném BudgetExhausted khi
     vượt max_fe, ghi best-so-far theo FE (mỗi 50 FE), đúng chiều maximize.
   - Mọi thuật toán (6 thuật toán + 8 biến thể ablation) PHẢI gọi fitness
     qua counter. Rà toàn bộ code, liệt kê mọi chỗ gọi fitness trực tiếp
     (khởi tạo, đánh giá lại best, OBL, Levy, sau repair) và sửa.
   - Thuật toán dừng giữa vòng khi hết ngân sách và trả về best hiện có.
   - Tham số phụ thuộc vòng lặp (hệ số a của WOA, trọng số quán tính PSO...)
     tính theo fe_count/max_fe.
   - Đánh giá cuối cùng để báo cáo dùng hàm gốc, không tính vào FE.

2. configs/benchmark.yaml (có chú thích tiếng Việt)
   - problem: num_uav=4, kênh Al-Hourani, 3,5 GHz, snr_threshold_db=18,
     fitness: {maximize: true, weights: {C: 0.6, E: 0.2, I: 0.2},
     coverage_quantity: SNR, normalization: <mô tả cận cố định>}.
   - scenarios (50..500 UE; 5 dạng phân bố), budget (max_fe =
     N*(1+MaxIter_WOA), stop_on: fe, early_stop: false, extra_budget_levels),
     common (population_size), tham số riêng từng thuật toán, ablation
     variants, seeds, parallel, output.
   - sensitivity: weight_sets, coverage_only, sinr_variant (khai báo trước,
     chạy ở Prompt 4B).
   - Mọi giá trị lấy từ code thật, giá trị chưa biết để TODO rõ ràng.

3. seeds/seeds.csv + script sinh seed
   - Tách data_seed (sinh UE, kênh) và algo_seed (khởi tạo thuật toán).
   - Cột: scenario_id, ue_count, distribution, instance_k, data_seed,
     run_id, algo_seed, purpose (tuning|eval).
   - tuning_seeds tách hoàn toàn khỏi eval seeds.
   - Dùng np.random.default_rng + SeedSequence, KHÔNG dùng np.random.seed
     toàn cục. Các thuật toán trong cùng (instance, run) nhận cùng quần thể
     khởi tạo ban đầu để ghép cặp.

4. run_benchmark.py
   - Đọc yaml, chạy theo seeds.csv, ghi runs.csv với các cột: định danh,
     fitness, C, E, I, ue_pass, ue_total, feasible, violation, fe_used,
     iterations_done, wall_time_s, cpu_time_s (process_time), worker_id,
     batch_wall_time_s, batch_total_cpu_s, n_workers, hit_target, fe_to_target.
   - Ghi convergence theo FE vào results/.../convergence/.
   - Chạy song song bằng multiprocessing, threads_per_worker = 1
     (đặt OMP/MKL/OPENBLAS_NUM_THREADS=1, cả K-Means của sklearn).
   - Hỗ trợ --smoke (1 instance, max_fe nhỏ) và --resume.

5. env.json tự động: git commit, cờ dirty, SHA256 của yaml, phiên bản
   Python/numpy/scipy/scikit-learn, pip freeze -> requirements.lock.txt,
   CPU, số nhân, RAM, OS, biến môi trường luồng, dòng lệnh.

6. REPRODUCE.md: các lệnh chạy lại từng bước từ git checkout.

7. tests/test_budget.py:
   - fe_used == max_fe cho cả 6 thuật toán và 8 biến thể.
   - Cùng seed chạy hai lần cho kết quả giống hệt (cả khi chạy song song).
   - Không còn lời gọi fitness nằm ngoài counter.

TIÊU CHÍ ĐẠT: smoke test pass; 4 sản phẩm (yaml, seeds.csv, ngân sách FE,
REPRODUCE.md) tồn tại; báo cáo ngắn nêu mỗi thuật toán đếm FE theo cách nào.
```

<a id="doc-section-08"></a>

## Nhiệm vụ 1 cập nhật — 24/10/2026 (tóm tắt yêu cầu)

Kiểm toán code, không đổi F=0,6C-0,2E-0,2I và C dùng max SNR của bốn UAV, ngưỡng >=18 dB. Báo cáo đủ 12 mục: khoảng cách 3D; góc ngẩng; LoS/NLoS và hằng số; suy hao; đơn vị SNR; ngưỡng; max-SNR và mẫu số UE; chuẩn hóa cố định; chiều tối ưu và tổng trọng số; biến thiên E trên 1000 nghiệm; ràng buộc và xử lý thống nhất; khớp báo cáo và suy ngược E từ C=0,9991, I=0,0572, F=0,4505. Tạo pytest tối thiểu 10 tình huống có oracle độc lập và log CSV. Sản phẩm: reports/fitness_audit.csv, reports/fitness_audit.md, danh sách lỗi theo mức độ và kết quả phải chạy lại, patch diff chưa áp dụng. Bản này lưu tóm tắt, không phải trích nguyên văn prompt; chi tiết thực thi nằm trong báo cáo và bộ test.

Lưu nguyên văn prompt người dùng từ ngày 24/10/2026. Các prompt tiếp theo được bổ sung theo thứ tự; không thay thế nội dung cũ.

<a id="doc-section-09"></a>

## Quy tắc và bối cảnh nghiên cứu — 24/10/2026

```text
Bạn là kỹ sư nghiên cứu tối ưu hóa, đang hỗ trợ sinh viên hoàn thiện đồ án
"Tối ưu vị trí 3D của 4 UAV-BS trong mạng 5G bằng I-WOA".

BỐI CẢNH
- Mô hình kênh Al-Hourani, 3,5 GHz, ngưỡng QoS SNR >= 18 dB.
- Fitness (bài toán CỰC ĐẠI): F = 0,6*C - 0,2*E - 0,2*I, trong đó C là độ phủ
  (càng cao càng tốt), E là năng lượng và I là can nhiễu (càng thấp càng tốt),
  cả ba đã chuẩn hóa về cùng thang [0, 1].
- Độ phủ: C(X) = (1/M) * tổng_j 1[ max_{i=1..4} SNR_ij(X) >= gamma_th ],
  tức tỷ lệ UE có SNR tốt nhất từ 4 UAV đạt ngưỡng. Bản chính dùng SNR;
  SINR chỉ là thí nghiệm phụ (tránh tính can nhiễu hai lần vì I đã riêng).
- Trọng số 0,6/0,2/0,2 là lựa chọn thiết kế của nhóm, KHÔNG phải kết quả
  chứng minh; phải biện minh bằng phân tích độ nhạy.
- I-WOA = WOA + K-Means + OBL + Levy Flight.
- So sánh 6 thuật toán: GA, PSO, WOA, H-PSOGA, H-WOA-PSO, I-WOA.
- Giảng viên yêu cầu: so sánh công bằng, tái lập được, kết luận phải dựa
  trên số liệu, không nhập tay số liệu.

QUY TẮC LÀM VIỆC (áp dụng cho mọi bước sau)
1. Đọc kỹ code thực tế được đính kèm trước khi sửa. Không đoán tên hàm,
   tên file; nếu thiếu thông tin thì liệt kê câu hỏi ở cuối thay vì tự bịa.
2. Không thay đổi hành vi thuật toán hay công thức Fitness nếu tôi chưa yêu
   cầu. Mỗi thay đổi phải nêu: file, dòng, lý do, tác động.
3. Mọi con số trong báo cáo phải sinh ra được từ log (CSV), không hard-code.
4. Nếu phát hiện lỗi làm kết quả cũ mất giá trị, báo ngay ở đầu câu trả lời.
5. Không khẳng định nguồn tham khảo nào đã được xác minh nếu bạn chưa đọc
   được nó; ghi rõ "cần sinh viên tự xác minh".
6. Trả lời bằng tiếng Việt, code và tên biến bằng tiếng Anh.
7. Cuối mỗi bước: liệt kê (a) file đã tạo/sửa, (b) cách chạy kiểm tra,
   (c) điều còn chưa chắc chắn.

Xác nhận bạn đã hiểu, rồi hỏi tôi những thông tin còn thiếu về cấu trúc
code trước khi bắt đầu.
( nhớ lưu các prompt lại trong doc nha
```
