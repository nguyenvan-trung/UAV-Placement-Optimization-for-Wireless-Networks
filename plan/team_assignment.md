# Phân công và quy tắc review

[Kế hoạch](README.md) · [Lộ trình](weekly_plan.md) · [Mục lục kỹ thuật](../implementation/docs/README.md)

Bảng là phạm vi trách nhiệm của nhóm, không phải xác nhận các thành viên đã hoàn tất hoặc duyệt mọi thay đổi.

| Thành viên | Phụ trách chính | Tài liệu liên quan |
|---|---|---|
| Nguyễn Văn Trung | Tích hợp, I-WOA, giao thức thí nghiệm, báo cáo | [DWI_WOA](../implementation/docs/DWI_WOA.md), [NOTEBOOK_STUDY](../implementation/docs/NOTEBOOK_STUDY.md) |
| Hoàng Văn Trường | GA, H-PSO-GA, quản lý/kiểm tra dataset | [DWGA](../implementation/docs/DWGA.md), [DWH_PSO_GA](../implementation/docs/DWH_PSO_GA.md) |
| Nguyễn Minh Hiếu | PSO, WOA, H-WOA-PSO, trực quan hóa | [DWPSO](../implementation/docs/DWPSO.md), [DWWOA](../implementation/docs/DWWOA.md), [DWH_WOA_PSO](../implementation/docs/DWH_WOA_PSO.md) |

## Công việc chung

Thống nhất định nghĩa C/E/I; chốt seed trước chạy; review tính khả thi, FE, logging và schema. Xem biến thể trong NOTEBOOK_STUDY để không bỏ qua các case GA/PSO mới.

Người review đối chiếu code, config và tài liệu; không chỉ kiểm tra đồ thị đẹp. Báo cáo phải dẫn nguồn artifact, mô tả phép gộp và nêu giới hạn. Không giao nhiệm vụ chứng minh trước một thuật toán thắng.

Trạng thái triển khai ở [PROJECT_GUIDE](../implementation/docs/PROJECT_GUIDE.md); hướng dẫn thuyết trình ở [TALK](../TALK.md).
