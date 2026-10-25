"""Generate documentation evidence ledger from existing audit CSVs, never test fixtures."""
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/'implementation/docs'


def main():
    rows=[]
    def add(claim,kind,source,line,column,value,status):
        rows.append(dict(claim=claim,kind=kind,source_file=source,source_line=line,
                         source_column=column,value=value,status=status))
    audit='reports/fitness_audit.csv'
    with (ROOT/audit).open(encoding='utf-8-sig',newline='') as stream:
        for line,row in enumerate(csv.DictReader(stream),2):
            for column in ['coverage','energy','overlap','fitness','status']:
                add('audit:'+row['case'],'code_check_not_benchmark',audit,line,column,row[column],'audit_only')
    reconciliation='reports/fitness_report_reconciliation.csv'
    with (ROOT/reconciliation).open(encoding='utf-8-sig',newline='') as stream:
        for line,row in enumerate(csv.DictReader(stream),2):
            for column in ['coverage','interference','fitness','inferred_energy']:
                add('historical_tuple:'+column,'user_input_or_derived_not_new_result',reconciliation,
                    line,column,row[column],'historical_unverified')
    samples='reports/fitness_energy_samples.csv'
    with (ROOT/samples).open(encoding='utf-8-sig',newline='') as stream:
        for line,row in enumerate(csv.DictReader(stream),2):
            add('energy_random_sample:'+row['sample_id'],'code_check_not_benchmark',samples,
                line,'energy',row['energy'],'audit_only')
    for name in ['coverage_all_users','rank_by_ue','part1_vs_part2','batch_speed',
                 'ablation_effect','generalization','weight_sensitivity','statistical_superiority']:
        add(name,'benchmark_result_required','','','','','missing_real_logs_do_not_claim')
    destination=DOCS/'REPORT_EVIDENCE.csv'
    with destination.open('w',newline='',encoding='utf-8-sig') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    text='''# Danh sách kiểm tra truy xuất số liệu

Sinh bằng `python implementation/scripts/build_report_evidence.py`.
CSV kèm theo chỉ rõ file, dòng CSV (header là dòng đầu), cột, giá trị và
phân loại. Không dùng dữ liệu trong statistics_test_artifacts làm nguồn.

- [x] Rút các số liệu benchmark cũ khỏi các chương DW.
- [x] Phân biệt tham số/công thức định trước với kết quả đo.
- [x] Log kiểm toán truy được đến từng dòng, nhưng không phải benchmark.
- [x] Bộ số liệu lịch sử do người dùng cung cấp được đánh dấu chưa xác minh.
- [x] Không đồng nhất độ phủ gần toàn bộ với mọi UE đạt ngưỡng.
- [x] Không khẳng định thứ hạng hoặc nguyên nhân từ mô tả toán tử.
- [ ] Có runs.csv benchmark FE thật và manifest đầy đủ.
- [ ] Mỗi ô kết quả mới truy đến tập dòng nguồn sau lọc/gộp, kèm script,
  hash dữ liệu và cấu hình; không chỉ dẫn tới một bảng trung gian.
- [ ] Có ue_pass/ue_total cho từng run và cách gộp rõ ràng.
- [ ] Có CPU/worker/wall/CPU tổng/FE và phạm vi đo từ batch thật.
- [ ] Có kiểm định, CI và effect size cho kết luận so sánh.
- [ ] Sinh viên xác nhận đọc nguồn trước khi đưa trích dẫn vào bản nộp.

**Giới hạn:** báo cáo tổng hợp hiện chưa đưa số đo benchmark vào nên chưa
thể hoàn tất các mục còn trống. Đây là ledger kiểm toán đầu vào hiện có,
không tự chứng nhận mọi số trong toàn bộ tài liệu dự án. Các số trong
công thức và mã giả là định nghĩa; cần dẫn code/cấu hình, không gán giả
cho một dòng log thực nghiệm.

Chi tiết: [REPORT_EVIDENCE.csv](REPORT_EVIDENCE.csv).
'''
    (DOCS/'REPORT_EVIDENCE.md').write_text(text,encoding='utf-8')


if __name__=='__main__':main()
