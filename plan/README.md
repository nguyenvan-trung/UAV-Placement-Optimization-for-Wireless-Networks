# 📅 Kế hoạch thực hiện đề tài

Đề tài: **UAV Placement Optimization for 5G Wireless Networks Using Improved Whale Optimization Algorithm (I-WOA)**.

Nhóm nghiên cứu, phát triển thuật toán đề xuất **I-WOA** (tích hợp K-Means, OBL, Levy Flight) và đối chứng toàn diện với **5 thuật toán khác** (GA, PSO, WOA gốc, Hybrid PSO-GA, Hybrid WOA-PSO) trên **500 bộ dữ liệu người dùng**, theo chiến lược thực nghiệm 2 giai đoạn (Hội tụ sớm 35 vòng lặp & Tối ưu hóa sâu 80 vòng lặp).

## 👥 Thành viên nhóm

| Họ và tên | Vai trò | Trách nhiệm chính |
|---|---|---|
| Nguyễn Văn Trung | Chủ nhóm | Quản lý dự án, kiến trúc hệ thống, phát triển I-WOA đề xuất, thực nghiệm Part 2, kịch bản TALK.md |
| Hoàng Văn Trường | Thành viên | Thuật toán GA, thuật toán lai H-PSO-GA, quản lý 500 datasets, lý thuyết di truyền DWGA.md |
| Nguyễn Minh Hiếu | Thành viên | Thuật toán PSO, WOA gốc, thuật toán lai H-WOA-PSO, trực quan hóa 2D/3D, tài liệu DWPSO/DWWOA.md |

## 📂 Các tài liệu kế hoạch & Tiến độ

- [weekly_plan.md](weekly_plan.md): Kế hoạch chi tiết 10 tuần và bảng theo dõi tiến độ thực tế (**Đã hoàn thành 100%**).
- [team_assignment.md](team_assignment.md): Bảng phân công vai trò, trách nhiệm và quy tắc review chéo chi tiết.
- [project_ideas.md](project_ideas.md): Ý tưởng, phạm vi và mô hình bài toán đa mục tiêu chuẩn 5G.
- [team_weekly_progress.xlsx](team_weekly_progress.xlsx): Sổ tay Excel theo dõi tiến độ chi tiết của từng thành viên qua 10 tuần.

## 🎯 Nguyên tắc làm việc & Kiểm chứng

1. Mỗi công việc phải có người phụ trách chính và người kiểm tra độc lập.
2. Mọi thuật toán phải dùng chung bộ 500 datasets, hàm mục tiêu đa tiêu chí ($f_1, f_2, f_3$), ràng buộc và điều kiện dừng để đảm bảo tính công bằng tuyệt đối.
3. Toàn bộ kết quả thực nghiệm được kiểm chứng qua 3.000 lượt chạy Monte Carlo trên đa tiến trình Multiprocessing.
4. Tuần 10 hoàn thiện toàn bộ báo cáo, slide, kịch bản bảo vệ và bộ tài liệu kỹ thuật DW*.md.
