# Định hướng slide báo cáo sản phẩm ứng dụng — AInatomy

**Mục đích:** thiết kế lại bài trình chiếu theo đúng dạng hồ sơ sản phẩm ứng dụng của Giải thưởng Tiên phong Ứng dụng AI trong Giáo dục Việt Nam 2026.

## 1. Kết luận nghiên cứu

Bài trình chiếu không nên giống đề cương nghiên cứu hay tài liệu kỹ thuật. Trọng tâm phải là:

1. Sản phẩm giải quyết vấn đề gì trong lớp học.
2. Người dùng thao tác với sản phẩm như thế nào.
3. Sản phẩm đã được dùng/kiểm tra đến đâu.
4. Minh chứng nhìn thấy được là gì.
5. Sản phẩm có thể tiếp tục dùng và nhân rộng ra sao.

**Tỷ lệ đề xuất:**

- 60–70% diện tích slide: ảnh chụp màn hình, chuỗi thao tác, đầu ra, bảng minh chứng.
- 20–30%: lời giải thích ngắn, dễ nói trong video 5 phút.
- Tối đa 10%: căn cứ chính sách và thông tin kỹ thuật cần thiết.

## 2. Căn cứ từ thể lệ

Trang giải thưởng iEEAI 2026 nêu 5 nhóm nội dung cần trình bày:

1. Bối cảnh và vấn đề cần giải quyết.
2. Ý tưởng/giải pháp và công cụ AI được sử dụng.
3. Quá trình triển khai trong thực tế.
4. Kết quả và tác động đạt được.
5. Tính bền vững và khả năng mở rộng.

Hội đồng đánh giá theo 5 tiêu chí:

- Tính thực tiễn.
- Tính sáng tạo.
- Tác động và kết quả thực tiễn.
- Tính bền vững và khả năng nhân rộng.
- Chất lượng trình bày.

Bài trình chiếu tối đa 15 slide, xuất PDF, tối đa 100 MB.

Nguồn: https://ieeai.net/giaithuong

## 3. Storyboard đề xuất — 13 slide

### Slide 1 — Sản phẩm trong một câu

**Tiêu đề:** AInatomy — Phòng thí nghiệm AI offline cho học sinh phổ thông

**Hình ảnh:** ảnh trang chủ sản phẩm toàn chiều rộng; logo hai đơn vị ở header.

**Chữ tối thiểu:**

> Học sinh không chỉ hỏi AI. Các em học cách quan sát, kiểm tra và bắt lỗi AI.

Thông tin cuối slide: GV Mai Xuân Văn · Trường THPT Thuận Hoá · Trường Đại học Sư Phạm, Đại học Huế.

### Slide 2 — Vấn đề trong lớp học

**Bố cục:** 3 ảnh/3 tình huống ngắn.

- Khái niệm AI khó nhìn thấy.
- Công cụ trực tuyến không phù hợp mọi phòng máy.
- Học sinh dễ nhận đáp án mà không kiểm chứng.

**Không đưa code.** Chỉ nói nhu cầu lớp học và điều kiện sử dụng.

### Slide 3 — Cách sản phẩm giải quyết vấn đề

**Bố cục:** sơ đồ một luồng lớn:

`Tình huống → Học sinh dự đoán → Thao tác → Nhận phản hồi → Tự rút ra kết luận`

**Hình ảnh:** ghép 3 ảnh thật: màn hình chính → màn hình thao tác → màn hình kết quả.

Một câu nhấn:

> AInatomy biến “AI là hộp đen” thành một chuỗi hoạt động có thể quan sát.

### Slide 4 — Một phiên học diễn ra như thế nào?

**Bố cục:** chuỗi 4 ảnh có đánh số, mỗi ảnh 1 caption.

1. Vào hoạt động.
2. Đọc tình huống hoặc dữ liệu.
3. Đưa ra phán đoán/câu trả lời.
4. Xem phản hồi và giải thích.

**Ảnh ưu tiên:** `out/an_hoc_sinh/03...`, `05...`, `06...`, `08...` hoặc ảnh từ `shot_sang/`.

### Slide 5 — Tính năng 1: Đấu trường bắt lỗi AI

**Bố cục:** ảnh màn hình lớn bên trái, 3 chú thích bên phải.

- Học sinh gặp đầu ra AI có lỗi cố ý.
- Học sinh chọn “có lỗi/không có lỗi” và phân loại lỗi.
- Hệ thống phản hồi ngay, không cần tài khoản hay API.

**Minh chứng:** ảnh tình huống, ảnh câu trả lời, ảnh phản hồi.

### Slide 6 — Tính năng 2: Nhà máy AI

**Bố cục:** ảnh `3-tram0-nhap-lieu.png` và `4-tram5-ung-dung.png` thành một chuỗi trước/sau.

Caption cần trả lời: học sinh nhìn thấy bước nào của hệ AI, thao tác gì, rút ra điều gì.

Không viết “7 trạm” nếu slide không có hình/sơ đồ 7 trạm. Nếu có, dùng sơ đồ 7 bước thật và đánh dấu bước đang minh họa.

### Slide 7 — Tính năng 3: Xưởng huấn luyện và thiên kiến dữ liệu

**Bố cục:** 2 ảnh trước/sau hoặc ảnh giao diện + biểu đồ nhỏ.

- Dữ liệu lệch ngày/đêm.
- Mô hình cho kết quả khác nhau giữa hai nhóm ảnh.
- Học sinh quan sát, cân bằng dữ liệu và so sánh lại.

**Lưu ý:** 59%/100% là số đo mô phỏng của hệ thống, phải ghi “kết quả trong mô phỏng”, không gọi là kết quả học sinh.

### Slide 8 — Tích hợp vào chương trình Tin học 10

**Bố cục:** một bản đồ/chains đơn giản, không bảng chữ dày.

- 28 bài SGK được đối chiếu.
- 22/22 YCCĐ lớp 10 được ánh xạ.
- 12 tiết đề xuất.

Bên phải đặt 1–2 ảnh hoạt động minh họa để chứng minh “đối chiếu” đã chuyển thành hoạt động cụ thể.

### Slide 9 — Sản phẩm tạo ra cho giáo viên

**Bố cục:** ảnh màn hình báo cáo/xuất dữ liệu + ảnh phiếu/biên bản nếu có.

Nêu ngắn:

- Theo dõi hoạt động theo mã ẩn danh.
- Xuất CSV/JSON làm minh chứng.
- Không cần chấm thủ công ở các nhiệm vụ có nhãn đúng cố định.

Không trình bày tên biến, localStorage, manifest hay đường dẫn mã nguồn.

### Slide 10 — Minh chứng kiểm thử sản phẩm

**Bố cục:** 4 số lớn + 2 ảnh nhỏ.

- 97/97 tiêu chí nghiệm thu.
- 22/22 YCCĐ được phủ.
- 0 lỗi nội dung theo cổng kiểm.
- Chạy offline.

Các số này là **minh chứng kiểm thử sản phẩm**, không phải tác động học tập của học sinh.

### Slide 11 — Triển khai và giới hạn hiện tại

**Bố cục:** hai cột “Đã có” và “Cần làm tiếp”.

**Đã có:**

- Bản chạy thử công khai.
- Bộ ảnh thao tác sản phẩm.
- Video demo nháp.
- Chạy offline/USB/mạng nội bộ.

**Cần làm tiếp / chưa được khai là đã có:**

- Dữ liệu từ lớp học thật.
- Phản hồi học sinh và giáo viên khác.
- Đo tác động trước/sau.

Slide này tăng độ tin cậy vì nói rõ ranh giới bằng chứng.

### Slide 12 — Bền vững và khả năng nhân rộng

**Bố cục:** 3 bước triển khai bằng icon/ảnh.

`Chép thư mục → Mở trên máy trường → Giáo viên tổ chức hoạt động`

Nêu:

- Không cần tài khoản học sinh.
- Không phụ thuộc API trong giờ học.
- Có thể dùng trong phòng máy cấu hình thấp.
- Nội dung có thể bổ sung theo chương trình.

### Slide 13 — Kết luận và lời mời trải nghiệm

**Bố cục:** ảnh giao diện đẹp nhất + QR/link demo + 3 câu kết.

1. Sản phẩm đã chạy và có thể trải nghiệm.
2. Giá trị cốt lõi là dạy học sinh kiểm chứng AI.
3. Bước tiếp theo là triển khai lớp học và thu dữ liệu tác động thật.

## 4. Các ảnh đã có và cách dùng

### Ảnh giao diện desktop

- `/home/hitokiri/ieeai2026/shot_sang/1-trang-chu.png` — trang chủ.
- `/home/hitokiri/ieeai2026/shot_sang/3-tram0-nhap-lieu.png` — trạm nhập liệu.
- `/home/hitokiri/ieeai2026/shot_sang/4-tram5-ung-dung.png` — trạm ứng dụng.
- `/home/hitokiri/ieeai2026/shot_sang/6-tinh-huong.png` — tình huống.

### Ảnh thao tác học sinh/luồng tương tác

- `/home/hitokiri/ieeai2026/out/an_hoc_sinh/02_menu.jpg`
- `/home/hitokiri/ieeai2026/out/an_hoc_sinh/03_man1_doan1_doc_va_doan.jpg`
- `/home/hitokiri/ieeai2026/out/an_hoc_sinh/05_man1_doan1_viet_du.jpg`
- `/home/hitokiri/ieeai2026/out/an_hoc_sinh/06_man1_doan1_dap_an.jpg`
- `/home/hitokiri/ieeai2026/out/an_hoc_sinh/08_man1_bang_dau_hieu.jpg`
- `/home/hitokiri/ieeai2026/out/an_hoc_sinh/17_man4_da_chon_va_viet_lai.jpg`
- `/home/hitokiri/ieeai2026/out/an_hoc_sinh/25_da_gui_tep.jpg`

## 5. Những gì phải bỏ khỏi bản slide cũ

- Mô hình 3 tầng kỹ thuật.
- Tên thư viện, file, router, manifest, hash.
- Mutation test trình bày như thành tựu chính.
- Các đoạn căn cứ pháp lý dài.
- Các slide card chỉ có chữ nhưng không có ảnh sản phẩm.
- Khẳng định “tác động học tập” khi chưa có dữ liệu lớp thật.

## 6. Nguyên tắc trình bày mới

- Một slide = một câu hỏi của giám khảo.
- Một ảnh lớn = một thao tác có thể kiểm chứng.
- Caption phải nói rõ: **ai thao tác, thao tác gì, nhận được gì**.
- Ảnh sản phẩm chiếm tối thiểu 45% diện tích slide nội dung.
- Mỗi slide tối đa 35–45 từ ngoài caption.
- Không dùng ảnh minh họa chung chung thay cho ảnh chụp sản phẩm.
- Không khai “đã triển khai lớp học” nếu chưa có ảnh/lớp/biên bản/dữ liệu thật.
