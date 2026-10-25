# Quy tắc biên tập và hiển thị tài liệu trên GitHub

[Mục lục](README.md) · [Nguồn](SOURCES.md)

Giữ bố cục nhất quán khi bổ sung tài liệu. Markdown phân tích được chưa chứng minh công thức hoặc mô hình đúng.

## Mục lục

1. [Bố cục một chương](#bo-cuc)
2. [Sơ đồ tổng quan](#so-do)
3. [Công thức và ký hiệu](#cong-thuc)
4. [Nguồn học thuật và mã](#nguon)
5. [Liên kết và tệp đưa lên Git](#lien-ket)
6. [Phạm vi xác minh](#kiem-tra)

<a id="bo-cuc"></a>

## 1. Bố cục một chương

Mục tiêu → mục lục → sơ đồ lớn → cách đọc → từng bước → công thức ngắn → bảng ký hiệu/đơn vị → ví dụ → nguồn/mã → giới hạn → đọc tiếp.

Không dùng chuỗi toán chứa chữ tiếng Việt dài làm sơ đồ quy trình. Không để công thức là nơi duy nhất giải thích ý tưởng.

README định hướng; NOTE giải thích logic; REPORT định nghĩa mô hình; DW giải thích thuật toán; REPRODUCE nói cách vận hành; TALK giúp trình bày.

<a id="so-do"></a>

## 2. Sơ đồ tổng quan

Dùng SVG trong assets, có alt text và giải thích dưới hình. Các hình hiện tại là quy trình, không phải dữ liệu thực nghiệm.

```markdown
![Luồng tổng quan của dự án](assets/overview.svg)
```

Đường dẫn tính từ file Markdown. README gốc dùng implementation/docs/assets/overview.svg. SVG có viewBox, title/desc, nền rõ và không phụ thuộc script/font từ mạng.

Không dùng khung ASCII rộng cần căn font cho logic chính. Nếu có mũi tên lặp, lời giải thích phải nói lặp về bước nào.

<a id="cong-thuc"></a>

## 3. Công thức và bảng ký hiệu

Dùng $$ riêng dòng cho math block. Đặt ngoài danh sách/bảng để tránh nhầm indent hoặc ký tự | với cột bảng.

Ví dụ mã nguồn:

```text
$$
F(X)=w_C C(X)-w_E E(X)-w_I I(X).
$$
```

Sau công thức có câu giải thích và bảng:

| Thành phần | Nội dung |
|---|---|
| Ký hiệu | Mỗi chữ/vector có ý nghĩa rõ trong ngữ cảnh |
| Đơn vị | Mét, giây, dB, dBm, W hoặc không đơn vị |
| Giá trị | Phân biệt mặc định code và tham số thực chạy |
| Phạm vi | Chỉ số, biên, điều kiện kích hoạt |
| Nguồn | Bài gốc hoặc định nghĩa/mã riêng |

Tách công thức dài. Bộ tài liệu không dùng dấu phân cách LaTeX dạng ngoặc vuông/ngược làm mặc định math. Không đặt công thức trong inline-code rồi mong MathJax render; code chỉ dùng để xem biểu thức thô.

Giữ cách đọc bằng lời để trình xem không có math vẫn hiểu. Nguồn: [GitHub math](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions).

<a id="nguon"></a>

## 4. Nguồn học thuật và mã

Mỗi công thức thuộc một trong ba loại: đã đối chiếu được bài nguồn; mới xác nhận nguồn nguyên lý/thư mục; hoặc quy tắc riêng theo code. Phải ghi đúng loại.

Nguồn tập trung ở [SOURCES](SOURCES.md), nhưng dẫn gần công thức để người đọc không đoán. Không viết “theo IEEE” cho tham số nhóm chọn. Hình biên soạn theo code cần chỉ rõ module. Ví dụ phải ghi là minh họa; số đo cần log/manifest/phép gộp.

<a id="lien-ket"></a>

## 5. Liên kết và tệp đưa lên Git

| Quy tắc | Lý do |
|---|---|
| Link tương đối, dùng dấu / | Mở được trên GitHub và máy khác |
| Không dùng đường dẫn ổ đĩa cá nhân trong repo | Chỉ có nghĩa trên một máy |
| Commit Markdown, SVG và file đích mới cùng nhau | Tồn tại trên máy chưa đủ |
| Giữ đúng chữ hoa/thường | GitHub không dựa vào cách Windows nới lỏng tên |
| Mục lục dùng anchor ASCII | Tránh phụ thuộc slug emoji/ký hiệu |
| Giữ báo cáo bằng chứng lịch sử | Không sửa lịch sử để giả làm hiện tại |

Không đưa bản sao tmp_audit hoặc checkpoint Jupyter vào lộ trình đọc chính.

<a id="kiem-tra"></a>

## 6. Phạm vi xác minh

Có thể kiểm tra UTF-8, parse Markdown, link/anchor, cột bảng, dấu đóng math và XML SVG mà không chạy optimizer. Chúng không thay preview cuối trên GitHub.

Đợt này kiểm tra tài liệu cục bộ, chưa đẩy nhánh hoặc xác nhận render một commit GitHub. Sau xuất bản cần xem Preview đúng branch/commit. Nếu lỗi trình xem cụ thể, ghi tên file và ảnh lỗi.
