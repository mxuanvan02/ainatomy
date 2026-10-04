# SOI AI — Hướng dẫn giáo viên (v0.2.0)

Phòng thí nghiệm AI **offline, tiếng Việt, không tài khoản, không thu phí** cho học sinh phổ thông.
Bám Khung nội dung giáo dục AI (QĐ 2422/QĐ-BGDĐT 18/8/2026) — 4 mạch × 12 khối năng lực UNESCO.
Học sinh **bắt lỗi AI** thay vì hỏi AI; hệ thống **tự chấm** vì lỗi do chính hệ cài sẵn.

## 1. Chạy (3 cách, không cần Internet)

| Cách | Làm gì | Dùng khi |
|---|---|---|
| **USB** | Chép cả thư mục `soi-ai/` vào USB → mở `index.html` bằng Chrome/Edge/Firefox | Phòng máy bất kỳ |
| **Máy chủ lớp** | Đặt thư mục trên 1 máy, chia sẻ qua mạng LAN hoặc phát WiFi cục bộ | Trường có 1 máy chủ |
| **Máy cá nhân** | Giải nén, mở `index.html` | Học ở nhà, không cần mạng |

Yêu cầu: trình duyệt bất kỳ (Chrome 60+, Firefox 60+, Edge). Máy cấu hình yếu vẫn chạy.
**Không cài đặt gì thêm. Không tài khoản. Không gửi dữ liệu ra ngoài.**

## 2. Tổ chức 1 tiết học (45 phút)

1. **Phát mã**: GV phát mỗi HS một mã ẩn danh (A001, A002... — KHÔNG dùng họ tên) + mã lớp (10A1).
2. **Vào app**: HS mở `index.html`, nhập mã → vào Trang chủ.
3. **Chọn hoạt động**:
   - 🧪 **Tầng 1 — Xưởng huấn luyện**: tạo dữ liệu → huấn luyện mô hình nhận diện mũ bảo hiểm → phát hiện mô hình "giỏi ban ngày, dốt ban đêm" → sửa bằng dữ liệu cân bằng → làm 4 nhiệm vụ phân tích. *(~20 phút — dạy khái niệm thiên kiến dữ liệu, mạch C+D)*
   - 🕵️ **Tầng 2 — Đấu trường bắt lỗi AI**: phiên 12 câu (8 câu có lỗi thuộc 5 loại + 4 câu đúng mồi nhử). HS đọc câu trả lời của "trợ lý AI", bấm vào câu nghi sai, phán quyết có lỗi/không + chọn loại lỗi. Hệ chấm ngay và giải thích. *(~15 phút)*
   - 📊 **Tầng 3 — Bản đồ năng lực**: HS xem recall theo 5 loại lỗi + tiến trình theo 12 khối năng lực + nhận xét tự động. *(~5 phút)*
4. **Pre/post**: đầu chuyên đề bấm **📋 Pre-test**, cuối chuyên đề bấm **🏁 Post-test** (cùng hệ đo, phiên khác nhau — đo tiến bộ).
5. **Thu dữ liệu**: cuối tiết, trên mỗi máy bấm **Báo cáo → ⬇ Xuất CSV**, GV gom file vào USB (mỗi máy 1 file).

## 3. Không có phòng máy? (phương án in — đúng tinh thần CV 5588 "phiên bản in ấn")

- GV chạy app trên 1 laptop + máy chiếu, cả lớp quan sát Tầng 1.
- Tầng 2: in "thẻ phán quyết" (mỗi thẻ 1 tình huống + 5 loại lỗi để tick) — xuất từ `data/cauhoi.js`.
- Kết quả vẫn ghi được: GV nhập thay 1 máy, hoặc HS luân phiên lên máy duy nhất.

## 4. Gộp dữ liệu cả lớp (sau khi thu CSV từ các máy)

```bash
python3 tools/gop_csv.py <thư_mục_chứa_các_file_CSV> -o <thư_mục_báo_cáo>
```

Xuất 3 file: `nhatky_gop.csv` (toàn bộ sự kiện), `baocao_lop.csv` (recall 5 loại lỗi + tiến trình pre/post + bản đồ 12 khối), `baocao_ca_nhan.csv` (từng mã HS).
Chạy được trên Python 3.8+, không cần thư viện ngoài.

## 5. Quyền riêng tư & đạo đức (nói với phụ huynh/BGH khi được hỏi)

- Chỉ thu **mã ẩn danh** GV phát — không họ tên, không ngày sinh, không ảnh.
- Dữ liệu lưu **cục bộ trong trình duyệt của từng máy** (localStorage) — không có máy chủ, không gửi gì ra Internet.
- GV toàn quyền: có nút **Xuất** (làm bằng chứng) và nút **Xóa dữ liệu trên máy này**.
- Báo cáo công bố dạng **tổng hợp (aggregate)**.
- Khuyến nghị: có ý kiến BGH bằng văn bản 1 trang trước khi thu dữ liệu (mẫu trong `ho-so/`).

## 6. Dạy đủ 12 tiết

Xem `ke-hoach-12-tiet.md` (thư mục cha): phân bổ 12 tiết × 4 mạch × 12 khối UNESCO, cấu trúc tiết 45 phút, 4 tiết pilot khuyến nghị (6, 7, 8, 10), phương án không phòng máy.

## 7. Cấu trúc mã nguồn (cho GV Tin muốn tùy biến)

```
soi-ai/
├── index.html            # toàn bộ giao diện (mở file này)
├── css/style.css
├── data/meta.js          # 4 mạch QĐ 2422, 5 loại lỗi, 12 khối UNESCO, template nhận xét
├── data/cauhoi.js        # ngân hàng gốc 22 item (tác giả viết tay, đã duyệt)
├── data/cauhoi_moRong.js # 56 item sinh bằng LLM + QC tự động (đang chờ tác giả duyệt nhãn 100%)
├── js/lab.js             # Tầng 1: sinh ảnh canvas + perceptron học thật + 4 nhiệm vụ oracle
├── js/engine.js          # Tầng 2+3: chấm tất định, log localStorage, báo cáo, xuất CSV/JSON
└── js/app.js             # điều hướng + UI 3 tầng + chọn phiên phân tầng 12 câu
```

Thêm câu hỏi mới: chép 1 item trong `data/cauhoi.js`, sửa nội dung, giữ nguyên cấu trúc khóa
(`id, mach, unesco, loai, loaiLoi, claimLoi, boiCanh, claims[3], giaiThich`).
Quy tắc: đúng 1 claim chứa lỗi khi `loai="co_loi"`; cả 3 claim đúng khi `loai="dung"`.

## 8. Trạng thái phiên bản

- **v0.2.0** (04/10/2026): 78 item (22 gốc + 56 LLM có QC), phiên phân tầng 12 câu, pre/post-test, CSV 19 cột có sự kiện phiên, script gộp đa máy. Đã smoke-test toàn bộ 3 tầng + pre/post + gộp CSV trên trình duyệt thật.
- **v0.1.0** (04/10/2026): bản đầu 3 tầng, 22 item.
- Git: mỗi phiên bản có commit + SHA256SUMS (bằng chứng mốc thời gian & toàn vẹn).

## 9. Căn cứ chương trình

- QĐ 2422/QĐ-BGDĐT (18/8/2026) — Khung nội dung giáo dục AI cho HS phổ thông (4 mạch, 12 tiết/lớp/năm).
- CV 5588/BGDĐT-GDPT (19/8/2026) — triển khai đại trà 2026–2027; yêu cầu không tài khoản cá nhân, không phụ thuộc nhà cung cấp, ưu tiên mã nguồn mở/miễn phí, có phiên bản ngoại tuyến.
- UNESCO AI Competency Framework for Students (2024) — 12 khối = 4 aspects × 3 levels.

Liên hệ tác giả: xem trong hồ sơ dự thi Giải thưởng Tiên phong Ứng dụng AI trong Giáo dục Việt Nam 2026.
