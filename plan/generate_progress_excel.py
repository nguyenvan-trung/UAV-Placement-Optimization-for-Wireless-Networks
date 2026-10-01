"""Generate the Excel progress workbook with updated 10-week project progress."""

from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

OUTPUT = Path(__file__).with_name("team_weekly_progress.xlsx")
MEMBERS = ("Nguyễn Văn Trung", "Hoàng Văn Trường", "Nguyễn Minh Hiếu")
ROLES = ("Chủ nhóm", "Thành viên", "Thành viên")
STATUSES = "Chưa bắt đầu,Đang thực hiện,Hoàn thành,Bị chặn"

WEEKS = (
    (
        "Xác định bài toán & Cơ sở lý thuyết",
        "Nghiên cứu tổng quan UAV-BS 5G, phân phối vùng phủ, điều phối phạm vi",
        "Tìm hiểu thuật toán di truyền (GA) và ứng dụng tối ưu hóa liên tục",
        "Tìm hiểu giải thuật bầy đàn (PSO, WOA) và các chỉ số đo lường QoS",
        "Hoàn thành",
        "docs/overview.md"
    ),
    (
        "Nghiên cứu tài liệu & Khảo sát mô hình",
        "Nghiên cứu kênh truyền Al-Hourani (LoS/NLoS) và hàm đa mục tiêu",
        "Tổng hợp kỹ thuật mã hóa nghiệm GA liên tục (Arithmetic, Gaussian)",
        "Nghiên cứu cơ chế bơi xoắn ốc WOA và động lực học vận tốc PSO",
        "Hoàn thành",
        "documents/papers_summary.md"
    ),
    (
        "Thiết kế kiến trúc & Đề xuất I-WOA",
        "Chủ trì chốt kiến trúc module hóa; đề xuất thuật toán cải tiến I-WOA",
        "Thiết kế pipeline dữ liệu người dùng và cấu trúc module GA",
        "Đề xuất thiết kế các giải thuật lai (H-PSO-GA, H-WOA-PSO) và metric",
        "Hoàn thành",
        "implementation/docs/formulas.md"
    ),
    (
        "Xây dựng module dùng chung & Dữ liệu",
        "Cài search space, nghiệm 12D và hàm mục tiêu (f1, f2, f3)",
        "Xây dựng bộ sinh và nạp 500 file CSV dữ liệu (50 - 500 UEs)",
        "Cài đặt mô hình vật lý 5G Al-Hourani và ngưỡng SNR",
        "Hoàn thành",
        "data/stores/*.csv, src/physics/"
    ),
    (
        "Triển khai 3 thuật toán cơ sở",
        "Cài đặt bầy đàn PSO (vận tốc v, vị trí x, neo biên Vmax, pbest/gbest)",
        "Cài đặt GA (Tournament, Arithmetic Crossover, Gaussian Mutation)",
        "Cài đặt WOA gốc (Whale, hệ số thích nghi a, A, C, bơi xoắn ốc)",
        "Hoàn thành",
        "src/algorithms/GA, PSO, WOA"
    ),
    (
        "Phát triển I-WOA & Các thuật toán lai",
        "Phát triển I-WOA: tích hợp K-Means khởi tạo, OBL và bước nhảy Levy",
        "Phát triển thuật toán lai H-PSO-GA: kết hợp PSO với GA",
        "Phát triển thuật toán lai H-WOA-PSO: kết hợp xoắn ốc WOA với PSO",
        "Hoàn thành",
        "src/algorithms/I_WOA, hybrid/"
    ),
    (
        "Tích hợp hệ thống & Kiểm thử bài toán UAV",
        "Xây dựng script đa tiến trình run_batch.py, tích hợp hàm đánh giá UAV",
        "Kiểm thử tính hợp lệ nghiệm, ràng buộc độ cao z trong [50, 300]m",
        "Xây dựng công cụ trực quan hóa 3D vị trí UAV và nón sóng 5G",
        "Hoàn thành",
        "results/uav_3d_placement_demo.png"
    ),
    (
        "Thực nghiệm Part 1 (35 vòng lặp — 500 datasets)",
        "Chủ trì batch run đa tiến trình 3.000 lượt chạy (500 files x 6 thuật toán)",
        "Thu thập log dữ liệu thô, kiểm tra tính toàn vẹn kết quả",
        "Xử lý thống kê trung bình Part 1, vẽ bộ 4 biểu đồ hội tụ sớm",
        "Hoàn thành",
        "results/part1_35_iterations/"
    ),
    (
        "Thực nghiệm Part 2 (80 vòng lặp) & Đối chiếu",
        "Chạy thí nghiệm tối ưu sâu 80 vòng lặp; phân tích Top 1 của I-WOA",
        "Phân tích cơ chế thoát cực trị của I-WOA so với bão hòa của PSO/WOA",
        "Xuất báo cáo đối chiếu DEMO_REPORT.md và biểu đồ cột bứt phá",
        "Hoàn thành",
        "results/part2_80_iterations/"
    ),
    (
        "Hoàn thiện tài liệu, Báo cáo & Bảo vệ",
        "Biên soạn kịch bản bảo vệ TALK.md, tổng duyệt toàn bộ demo",
        "Biên soạn tài liệu kỹ thuật DWGA.md, DWH_PSO_GA.md",
        "Biên soạn tài liệu kỹ thuật DWPSO.md, DWWOA.md, DWH_WOA_PSO.md",
        "Hoàn thành",
        "TALK.md, docs/DW*.md"
    ),
)

NAVY, BLUE, WHITE = "1F4E78", "D9EAF7", "FFFFFF"
THIN = Side(style="thin", color="B7C9D6")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def title(cell, size=15):
    cell.font = Font(bold=True, color=WHITE, size=size)
    cell.fill = PatternFill("solid", fgColor=NAVY)
    cell.alignment = Alignment(horizontal="center", vertical="center")


def header(cells):
    for cell in cells:
        cell.font = Font(bold=True, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=NAVY)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER


def status_validation(sheet, cells):
    validation = DataValidation(type="list", formula1=f'"{STATUSES}"')
    sheet.add_data_validation(validation)
    validation.add(cells)
    colors = {"Chưa bắt đầu": "D9E1F2", "Đang thực hiện": "FFF2CC", "Hoàn thành": "C6E0B4", "Bị chặn": "F4CCCC"}
    first = str(cells).split(":")[0]
    for label, color in colors.items():
        sheet.conditional_formatting.add(str(cells), FormulaRule(formula=[f'{first}="{label}"'], fill=PatternFill("solid", fgColor=color)))


wb = Workbook()
ws = wb.active
ws.title = "Tổng quan"
ws.merge_cells("A1:E1")
ws["A1"] = "THEO DÕI TIẾN ĐỘ ĐỀ TÀI UAV PLACEMENT (10 TUẦN)"
title(ws["A1"])
ws.append(["Chủ nhóm", MEMBERS[0], "Thành viên", MEMBERS[1], MEMBERS[2]])
ws.append([])
ws.append(["Tuần", "Nội dung chính", "Trạng thái", "Ngày cập nhật", "Minh chứng / đường dẫn"])
header(ws[4])

for number, week in enumerate(WEEKS, 1):
    ws.append([number, week[0], week[4], "01/10/2026", week[5]])
    for cell in ws[number + 4]:
        cell.border = BORDER
        cell.alignment = Alignment(vertical="top", wrap_text=True)

status_validation(ws, "C5:C14")
ws.freeze_panes = "A5"
ws.auto_filter.ref = "A4:E14"
for column, width in zip("ABCDE", (9, 38, 20, 18, 45)):
    ws.column_dimensions[column].width = width

guide = wb.create_sheet("Hướng dẫn")
guide.merge_cells("A1:D1")
guide["A1"] = "HƯỚNG DẪN CẬP NHẬT"
title(guide["A1"])
steps = (
    "1. Mỗi người điền đúng dòng mang tên mình trong sheet của tuần hiện tại.",
    "2. Ghi công việc đã làm và dán link commit, Pull Request hoặc file kết quả.",
    "3. Chọn trạng thái trong danh sách có sẵn (Hoàn thành / Đang thực hiện / Chưa bắt đầu).",
    "4. Chủ nhóm điền tổng kết, kế hoạch tiếp theo và ngày xác nhận.",
    "5. Cập nhật dòng tương ứng trong sheet Tổng quan rồi lưu file.",
)
for row, text in enumerate(steps, 3):
    guide.cell(row, 1, text)
guide.column_dimensions["A"].width = 110

for number, week in enumerate(WEEKS, 1):
    sheet = wb.create_sheet(f"Tuần {number}")
    sheet.merge_cells("A1:F1")
    sheet["A1"] = f"TUẦN {number} — {week[0].upper()}"
    title(sheet["A1"], 14)
    sheet["A2"], sheet["B2"] = "Thời gian", f"Tuần {number}"
    sheet["D2"], sheet["E2"] = "Trạng thái tuần", week[4]
    status_validation(sheet, "E2")
    sheet.append([])
    sheet.append(["Thành viên", "Vai trò", "Công việc dự kiến", "Công việc đã thực hiện", "Kết quả / minh chứng", "Trạng thái"])
    header(sheet[4])
    for index, member in enumerate(MEMBERS):
        sheet.append([member, ROLES[index], week[index + 1], "Đã hoàn thành theo kế hoạch", week[5], week[4]])
        sheet.row_dimensions[5 + index].height = 55
        for cell in sheet[5 + index]:
            cell.border = BORDER
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    status_validation(sheet, "F5:F7")
    for row, label in enumerate(("Kết quả chung", "Vấn đề đã xử lý", "Kế hoạch tuần sau", "Nhận xét chủ nhóm", "Ngày xác nhận"), 9):
        sheet.cell(row, 1, label)
        sheet.cell(row, 1).font = Font(bold=True)
        sheet.cell(row, 1).fill = PatternFill("solid", fgColor=BLUE)
        sheet.merge_cells(start_row=row, start_column=2, end_row=row, end_column=6)
        for column in range(1, 7):
            sheet.cell(row, column).border = BORDER
            sheet.cell(row, column).alignment = Alignment(vertical="top", wrap_text=True)
            
    # Ghi nhận xét hoàn thành
    sheet.cell(9, 2, f"Hoàn thành các mục tiêu đề ra cho tuần {number}")
    sheet.cell(10, 2, "Đạt yêu cầu kỹ thuật và vượt qua kiểm tra độc lập")
    sheet.cell(11, 2, "Chuyển tiếp nhịp nhàng sang tuần kế tiếp")
    sheet.cell(12, 2, "Đánh giá xuất sắc, đúng tiến độ 100%")
    sheet.cell(13, 2, "01/10/2026")

    sheet.freeze_panes = "A5"
    sheet.auto_filter.ref = "A4:F7"
    for column, width in zip("ABCDEF", (23, 15, 38, 42, 42, 19)):
        sheet.column_dimensions[column].width = width

for sheet in wb.worksheets:
    sheet.sheet_view.showGridLines = False
    sheet.page_setup.orientation = "landscape"
    sheet.page_setup.fitToWidth = 1
    sheet.sheet_properties.pageSetUpPr.fitToPage = True

wb.save(OUTPUT)
print(f"Generated updated workbook: {OUTPUT}")
