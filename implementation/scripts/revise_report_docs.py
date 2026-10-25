"""One-time editorial revision; preserves method sections and flags references."""
import re
from pathlib import Path

DOCS=Path(__file__).resolve().parents[1]/'docs'


def main():
    for path in DOCS.glob('DW*.md'):
        text=path.read_text(encoding='utf-8')
        text=re.sub(r'## 5\..*?(?=## 7\.|\Z)',
            '## 5. Trạng thái thực nghiệm và diễn giải\n\n'
            'Các số liệu và phần trả lời phản biện dựa trên kết quả cũ đã được rút khỏi tài liệu. '
            'Chưa có log benchmark theo FE để xác nhận thứ hạng hoặc quy nguyên nhân cho từng cơ chế. '
            'Không kết luận thuật toán này vượt thuật toán khác từ mô tả toán tử. '
            'Xem [báo cáo tổng hợp](REPORT.md), [ablation](ABLATION.md), '
            '[độ nhạy](SENSITIVITY.md) và [thống kê](STATISTICS.md).\n\n',text,flags=re.S)
        text=text.replace('## 7. 📚 TÀI LIỆU THAM KHẢO HỌC THUẬT (ACADEMIC REFERENCES)',
            '## 7. Tài liệu tham khảo dự kiến — cần sinh viên tự xác minh\n\n'
            'Danh mục kế thừa từ bản cũ; thông tin thư mục và mức độ phù hợp cần sinh viên tự đọc xác minh. '
            'Không coi các chú giải bên dưới là bằng chứng đã kiểm chứng hoặc nguồn của toàn bộ Fitness. '
            'Xem quy tắc trích dẫn trong [REPORT.md](REPORT.md).')
        text=text.replace('độ cao bay an toàn','độ cao bay mô phỏng').replace('Độ cao bay an toàn','Độ cao bay mô phỏng')
        if path.name=='DWI_WOA.md':
            start=text.index('Mặc dù thuật toán');end=text.index('## 2.')
            text=text[:start]+('I-WOA kết hợp K-Means, OBL và Lévy trên lõi WOA. '
                'Mục tiêu thiết kế là khảo sát ảnh hưởng của khởi tạo và đề xuất nghiệm bổ sung. '
                'Chưa có ablation theo FE để kết luận từng thành phần có lợi hoặc hiệu quả cộng dồn.\n\n')+text[end:]
            text=text.replace('($z_0 = 120\\text{ m}$)','($z_0 = 100\\text{ m}$)')
            text=text.replace(', 120',', 100')
            text=text.replace('- Các cá thể còn lại trong quần thể được sinh bằng nhiễu Gauss quanh hạt giống này kết hợp với ngẫu nhiên đều, giúp bầy cá voi ngay từ thế hệ 0 đã có vùng xuất phát thuận lợi.',
                '- Code khởi tạo cả quần thể ngẫu nhiên đều; chỉ thay cá thể đầu bằng gợi ý K-Means. Không sinh Gaussian quanh tâm cụm. Độ cao gợi ý được clip vào miền bài toán. Nguồn: `../src/preprocessing/kmeans_init.py` và `../src/algorithms/I_WOA/optimizer.py`.')
            text=text.replace('Đánh giá hàm Fitness cho toàn bộ $2 \\times PopSize$ cá thể trong tập kết hợp',
                'Giữ Fitness của quần thể gốc đã tính, chỉ đánh giá thêm $PopSize$ nghiệm đối lập rồi ghép')
            text=text.replace('[`kmeans.py`](..\\src\\preprocessing\\kmeans.py) | `run_kmeans_clustering()`',
                '[`kmeans_init.py`](../src/preprocessing/kmeans_init.py) | `generate_kmeans_uav_initial_guess()`')
            text=text.replace('Theo lý thuyết của Tizhoosh (2005), nếu một giải pháp đang hướng sai vùng cực trị địa phương thì giải pháp đối xứng ngược chiều của nó có xác suất tiệm cận nghiệm tối ưu toàn cục cao hơn:',
                'OBL tạo nghiệm đối xứng để đánh giá bổ sung; không bảo đảm nghiệm đối lập có chất lượng cao hơn:')
            text=text.replace('Để khắc phục triệt để hiện tượng suy giảm hệ số $a$ khiến WOA bị "đóng băng" ở nửa cuối,',
                'Để khảo sát việc bổ sung đề xuất bước nhảy,')
            text=text.replace('nếu } \\|\\mathbf{X}_i - \\mathbf{X}^*\\| > 10^{-3}',
                'nếu từng tọa độ có } |X_{i,d}-X^*_d| > 10^{-3}')
        if path.name=='DWH_WOA_PSO.md':
            text=text.replace('x_new = clip(x_woa + 0.5 * v(t+1), LB, UB)',
                'x_new = clip(0.5*x_woa + 0.5*(x+v), LB, UB)')
            text=text.replace('\\mathbf{X}_{i}^{\\text{woa}} + \\beta \\cdot \\mathbf{V}_i(t+1)',
                '(1-\\beta) \\mathbf{X}_{i}^{\\text{woa}} + \\beta (\\mathbf{X}_i(t)+\\mathbf{V}_i(t+1))')
        if path.name=='DWH_PSO_GA.md':
            text=text.replace('$w = 0.7, c_1 = 1.5, c_2 = 1.5$',
                '$w$ giảm tuyến tính theo vòng lặp trong code hiện tại; $c_1 = 1.5, c_2 = 1.5$')
        if path.name=='DWWOA.md':
            text=text.replace('Khi $l \\to 0$, $e^{bl} \\cos(2\\pi l) \\to 1$, vị trí cá voi tiến sát con mồi.',
                'Khi $l \\to 0$, hệ số tiến tới một; bước cộng vẫn chứa D\', nên không bảo đảm vị trí tiến sát con mồi.')
        first=text.find('\n')
        text=text[:first]+('\n\n> Tài liệu phương pháp; các kết luận thực nghiệm cũ đã được rút. '
            'Không có bảng xếp hạng mới khi chưa có log FE. Mô hình chung: [REPORT.md](REPORT.md).\n')+text[first:]
        path.write_text(text,encoding='utf-8')
    path=DOCS/'formulas.md';text=path.read_text(encoding='utf-8')
    text=text.replace('CSV. mmm','CSV.').replace('`f2`: năng lượng','`f2`: công suất trung bình chuẩn hóa theo proxy hiện tại')
    text=text.replace('`f3`: diện tích giao thoa','`f3`: tỷ lệ UE được từ hai UAV trở lên phủ theo ngưỡng SNR (proxy chồng lấn)')
    text=text.replace('K-Means không được đặt trong `algorithms/` vì nó là tiền xử lý dùng chung cho\n\nI-WOA và các thí nghiệm khởi tạo.',
        'K-Means nằm trong preprocessing; optimizer I-WOA gọi khi bật cờ. Không có nghĩa các baseline tự động dùng K-Means.')
    text+='\n\nMô hình, nguồn và trạng thái kết quả: [REPORT.md](REPORT.md).\n'
    path.write_text(text,encoding='utf-8')


if __name__=='__main__':main()
