# AInatomy — Hướng dẫn giáo viên (v1.2.0)

Phòng thí nghiệm AI **offline, tiếng Việt, không tài khoản, không thu phí** cho học sinh phổ thông.
Bám Khung nội dung giáo dục AI (QĐ 2422/QĐ-BGDĐT 18/8/2026) — 4 mạch × 12 khối năng lực UNESCO.
Học sinh **bắt lỗi AI** thay vì hỏi AI; hệ thống **tự chấm** vì lỗi do chính hệ cài sẵn.

**Phạm vi dữ liệu đã kiểm chứng.** Phụ đề không giới hạn cấp học vì app không khoá lớp (mã lớp nhập tự do) và Khung 2422/QĐ-BGDĐT có phụ lục yêu cầu cần đạt cho cả lớp 10, 11, 12. Nhưng bản đồ yêu cầu cần đạt đang nhúng trong app là của **lớp 10** — 22 yêu cầu, trích nguyên văn, đã kiểm chứng tự động 22/22 với văn bản Bộ bằng `tools/verify_yccd.py`. Nói rõ ranh giới này để hồ sơ không khai rộng hơn dữ liệu thật; mở rộng sang lớp 11 và 12 là việc trích thêm phụ lục, không phải việc đổi chữ.

**Repo:** https://github.com/mxuanvan02/ainatomy · **Bản chạy thử:** https://mxuanvan02.github.io/ainatomy/

## 0. Repo này tự chứa (chạy được ở máy khác)

Mọi công cụ trong `tools/` tự suy gốc repo từ vị trí tệp, **không ghi cứng đường dẫn máy tác giả**:

```bash
git clone https://github.com/mxuanvan02/ainatomy.git
cd ainatomy
python3 tools/nghiem_thu.py          # nghiệm thu: dòng KẾT QUẢ phải là N/N (hai số bằng nhau)
python3 tools/kiem_noi_dung.py       # nội dung: kỳ vọng 0 lỗi
python3 tools/tinh_do_phu.py         # độ phủ YCCĐ: kỳ vọng 22/22
python3 tools/sinh_manifest.py       # chỉ-kiểm hash; thêm --ghi để sinh lại
sha256sum -c SHA256SUMS.txt          # kỳ vọng 0 dòng FAILED (mã thoát 0)
```

**Cố ý KHÔNG ghi số tiêu chí hay số tệp cụ thể ở đây.** Bản cũ ghi "kỳ vọng 52/52" rồi
"72/72" — mỗi lần cổng thêm tiêu chí hoặc repo thêm tệp là dòng đó thành sai, trong khi
người đọc vẫn tin nó. Đã xảy ra thật: README ghi "52/52" khi cổng là 53/53, rồi lại ghi
"59/59" và "89/89" khi cổng lên 59 nhưng manifest còn 88. Ghi ĐIỀU KIỆN ("hai số bằng
nhau", "0 FAILED") thì không cũ được. Muốn biết hiện trạng: chạy lệnh và đọc kết quả, hoặc
xem `out/judge_result.meta.json` (ghi số tiêu chí + commit + thời điểm của lần chạy).

Manifest phủ **mọi tệp git theo dõi** (mã, dữ liệu, công cụ đo, và `data-source/` chứa văn bản
Bộ), chỉ trừ chính nó và `out/`. Cổng `G13` kiểm điều đó: nếu một tệp mới bị bỏ sót khỏi
manifest thì cổng FAIL, nên không thể âm thầm khai thiếu bằng chứng toàn vẹn. Sinh lại bằng
`tools/sinh_manifest.py` — danh sách lấy từ `git ls-files`, không gõ tay.

Không cần cài gì ngoài Python 3.8+ và một trình duyệt. Đầu vào dùng cho các phép kiểm
nằm trong `data-source/` (Khung 2422 PDF + bản chữ, danh sách 22 YCCĐ). Kết quả kiểm
sinh ra ở `out/`.

### Cổng này tự chứng minh là nó có răng: bộ mutation test

Một cổng ĐẠT ở lần chạy đầu **không chứng minh gì** — nó có thể đang mù. Đã xảy ra thật trong
dự án này: cổng `G17b` báo 14 vi phạm và **cả 14 đều là dương tính giả**; còn cổng `G18` đạt
3/3 ngay lần đầu, phải viết bài phá cho nó mới biết nó thật sự thấy được lỗi. Nên mỗi cổng đều
có script mutation riêng, nằm ở `tools/tests/mutation/`.

```bash
cd soi-ai
python3 tools/nghiem_thu.py                          # CA 0: nguyên trạng PHẢI xanh trước đã
python3 tools/tests/mutation/mutation_g18.py         # rồi mới phá từng cổng
```

Mỗi script phá đúng thứ cổng khai là đang canh, rồi **tự khôi phục** để cây về nguyên trạng.
Điều kiện đạt, không phải con số: mọi script in `rc=0`, dòng `KẾT LUẬN` khớp số ca, và **cây
sạch sau khi chạy xong** (`git status --short` rỗng).

Đếm ca bằng `tools/tests/mutation/dem_ca.py`, **đừng đếm tay**:

```bash
cd soi-ai
mkdir -p /tmp/mut
for b in tools/tests/mutation/mutation_*.py tools/tests/mutation/mut_g12c.py; do
  python3 "$b" > "/tmp/mut/$(basename "$b" .py).log" 2>&1
done
python3 tools/tests/mutation/dem_ca.py /tmp/mut
```

Vì sao phải có công cụ đếm: trong một phiên, phép đếm tay ra **ba con số khác nhau** trên cùng
một bộ log (29 rồi 40 rồi 42, trong khi số đúng là 48) — lần nào cũng in ra trông hợp lệ. Và
`tools/tests/mutation/dem_ca.py` cũng tự kêu khi không đếm được: thư mục rỗng thì báo "CHƯA CHẠY"
(không in `0 ca`), log không khớp khuôn thì liệt kê tên và **không cộng** số của chúng vào tổng.

Hai điều bắt buộc khi đọc kết quả, vì cả hai đã gây kết luận sai:

- **Phân biệt ca PHÁ với ca ĐỐI CHỨNG ÂM.** Ca phá là ca **cổng phải kêu** (script in
  `BẮT ĐƯỢC`, `rc=1`). Ca đối chứng âm là ca **cổng phải IM** vì đầu vào hợp lệ — ví dụ
  `G18` phải bỏ qua đường dẫn cũ khi nó nằm trong docstring, hay `G10f` phải im ở chỗ `G10b`
  đã bắt. Đếm gộp hai loại thành "N/N ca phá bị bắt" là **khai quá**; chính dòng `KẾT LUẬN`
  của 5 script trong repo từng gộp như vậy, và đã sửa.
- **Đếm theo CẤP CA, không đếm dòng chứa từ khoá.** Một ca được mô tả trên nhiều dòng, nên đếm
  dòng cho ra số lớn hơn số ca thật.
- **Nếu vừa sửa `tools/`: chạy `python3 tools/sinh_manifest.py --ghi` TRƯỚC.** Cổng có phép
  kiểm toàn vẹn tệp, nên manifest cũ làm CA 0 đỏ vì lý do không phải lỗi sản phẩm — và đọc
  nhầm CA 0 đỏ thành "cổng hỏng" đã tốn hai lần chạy.

Cổng `G18` là cổng canh chính lời khai ở §0 đầu tài liệu này: `G18a` không công cụ nào ghi cứng
đường dẫn `/home/<tác giả>`, `G18b` không công cụ nào trỏ ngược ra ngoài repo bằng tên thư mục
dự án, `G18c` mọi công cụ parse được và import đủ mô-đun nó dùng. `G18c` bắt được một lỗi thật
ngay khi bật: `../tools/tao_sheet_thietke.py` (công cụ của THƯ MỤC HỒ SƠ, ngoài repo này) dùng
`os.path.join` mà không import `os` — chạy là chết, và không cổng nào thấy vì cổng chỉ tự chạy
chính nó. Ghi rõ đường dẫn `../` ở đây để không ai đi tìm nó trong repo này mà không thấy.

## 1. Chạy (3 cách, không cần Internet)

| Cách | Làm gì | Dùng khi |
|---|---|---|
| **USB** | Chép cả thư mục `ainatomy/` vào USB → mở `index.html` bằng Chrome/Edge/Firefox | Phòng máy bất kỳ |
| **Máy chủ lớp** | Đặt thư mục trên 1 máy, chia sẻ qua mạng LAN hoặc phát WiFi cục bộ | Trường có 1 máy chủ |
| **Máy cá nhân** | Giải nén, mở `index.html` | Học ở nhà, không cần mạng |

Yêu cầu: trình duyệt bất kỳ (Chrome 60+, Firefox 60+, Edge). Máy cấu hình yếu vẫn chạy.
**Không cài đặt gì thêm. Không tài khoản. Không gửi dữ liệu ra ngoài.**

## 2. Tổ chức 1 tiết học (45 phút)

**ĐỌC MỤC NÀY TRƯỚC: ba Tầng là MENU CHỌN MỘT, không phải ba việc làm liên tiếp trong một tiết.**

Bản cũ của README kê Tầng 1 ~20 phút + Tầng 2 ~15 phút + Tầng 3 ~5 phút = **40 phút thực hành**.
Nhưng `ke-hoach-12-tiet.md` (bảng "CẤU TRÚC MỘT TIẾT 45 PHÚT") chỉ dành phút **13–33 = 20 phút**
cho học sinh thực hành; 25 phút còn lại là khởi động, hình thành khái niệm, thảo luận và chốt.
Tức README hứa **gấp đôi** thời gian có thật, và giáo viên làm theo sẽ vỡ tiết ngay lần đầu.
Đã sửa thành menu theo tiết ở dưới — con số lấy từ chính bảng cấu trúc tiết, không ước lượng.

### Khung thời gian thật của một tiết (theo `ke-hoach-12-tiet.md`)

| Phút | Việc | App dùng thế nào |
|---|---|---|
| 0–5 | Khởi động: một tình huống thật | Không dùng app (giáo viên dẫn dắt) |
| 5–13 | Hình thành khái niệm của tiết | Chiếu app lên cho cả lớp xem, chưa cho làm |
| **13–33** | **Học sinh thực hành (20 phút)** | **Mỗi em một mã, làm MỘT hoạt động chọn bên dưới** |
| 33–41 | Thảo luận: dấu hiệu nào giúp em nhận ra | Học sinh nói, giáo viên ghi bảng |
| 41–45 | Chốt và nhận xét tiến trình | Chiếu **Báo cáo lớp** (Tầng 3), không đọc kết quả từng em |

### Chọn MỘT hoạt động cho 20 phút thực hành

- **Tầng 1 — Xưởng huấn luyện** *(hết ~18–20 phút nếu làm trọn; nên cắt còn tạo dữ liệu →
  huấn luyện → thấy "giỏi ban ngày, dốt ban đêm", bỏ phần cân bằng dữ liệu sang tiết sau)*.
  Dạy thiên kiến dữ liệu, mạch C+D.
- **Tầng 2 — Đấu trường bắt lỗi AI**: phiên 12 câu (8 câu có lỗi thuộc 5 loại + 4 câu đúng mồi
  nhử), ~1,5 phút/câu nếu đọc kỹ → **~18 phút**. Vừa khít 20 phút, không nên ghép thêm gì.
- **Nhà máy AI (7 trạm)**: mỗi trạm 5–8 phút → **một tiết chỉ đi 2–3 trạm**, không đi hết.
- **Phòng 3D / Ống dẫn AI**: ~10 phút mỗi cái, hợp với tiết có phần thực hành ngắn.

Tầng 3 (Bản đồ năng lực) **không phải một hoạt động 5 phút của học sinh** — nó là màn hình giáo
viên chiếu ở phút 41–45 để chốt tiết.

### Thu dữ liệu: việc này tốn thời gian hơn bạn nghĩ, hãy xếp lịch cho nó

Đo bằng thao tác thật: mở Tầng 3 → bấm **Xuất CSV nhật ký lớp (minh chứng)** → tệp rơi vào
thư mục Downloads → giáo viên phải tìm tệp rồi chép sang USB. Tối thiểu 30–60 giây/máy nếu
suôn sẻ; với 20 máy là **10–20 phút**, trong khi phút 41–45 chỉ có **4 phút**. Bản cũ của
README xếp việc thu vào "cuối tiết" mà không tính phút nào cho nó — đó là lý do giáo viên sẽ
phải thu vội và mất dữ liệu 5 phút cuối của học sinh.

**Cách làm đã kiểm:** cho học sinh **tự bấm Xuất CSV ngay khi làm xong hoạt động** (khoảng phút
30–33, khi các em xong sớm lệch nhau), tệp tự tải về máy; giáo viên chỉ đi **một vòng thu USB**
trong lúc lớp thảo luận (phút 33–41). Đừng dồn tất cả về phút 45.

Hai rủi ro phải biết trước:
- Máy phòng lab thường **đóng băng ổ** (Deep Freeze) hoặc reset profile giữa hai ca → tệp trong
  Downloads và cả localStorage **có thể biến mất**. Thu trong tiết, đừng để sang tiết sau.
- Nút **Xóa dữ liệu trên máy này** nằm trong Tầng 3 mà học sinh vào được. Nó đã được phòng vệ
  (tự tải bản JSON dự phòng về máy trước khi hỏi, và phải gõ chữ XÓA thay vì bấm một lần),
  nhưng giáo viên vẫn nên dặn lớp không bấm nút đỏ.

### Pre/post

Đầu chuyên đề bấm **Pre-test (đầu vào)**, cuối chuyên đề bấm **Post-test (đầu ra)**. Hai phiên
dùng cùng hệ đo nhưng **bộ câu khác nhau** — hệ tự loại những câu học sinh đó đã gặp, để
post-test đo tiến bộ chứ không đo trí nhớ. Số liệu chi tiết và giới hạn của phép đo: xem
`huong-dan-danh-gia.md` (cùng thư mục).

> Nhãn nút chép NGUYÊN VĂN từ giao diện. Trước đây README ghi "Pre-test" / "Post-test" /
> "Xuất CSV" (rút gọn) nên giáo viên tìm không ra nút trên màn hình. Đã bỏ luôn 7 emoji ở mục
> này vì MASTER.md cấm emoji làm biểu tượng — README là thứ giám khảo và đồng nghiệp đọc ĐẦU
> TIÊN trên GitHub, nên nó phải theo cùng chuẩn với giao diện.

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
- Khuyến nghị: có ý kiến BGH bằng văn bản 1 trang trước khi thu dữ liệu — mẫu văn bản có sẵn
  ở `ho-so/mau_xin_phep_BGH.md` (chép ra Word, điền phần trong `[NGOẶC VUÔNG]`, in 1 trang).
- Nút **Xóa dữ liệu trên máy này** tự tải một bản JSON dự phòng về máy TRƯỚC khi hỏi, và yêu
  cầu gõ chữ XÓA thay vì bấm một lần. Nút này nằm trong Tầng 3 mà học sinh vào được, nên
  phòng vệ bằng bản sao lưu chứ không phải bằng mật khẩu: app không có khái niệm "vai trò
  giáo viên", và một mật khẩu đặt ra chỉ tạo cảm giác an toàn sai.

### Giới hạn của phép đo — đọc trước khi dùng số liệu làm minh chứng

Nói thẳng ba điều, vì hồ sơ dùng các con số này làm bằng chứng:

- **Phiên đấu trường có sàn may rủi 33%.** Mỗi phiên 12 câu gồm 8 câu có lỗi và 4 câu đúng;
  học sinh chỉ phán "không có lỗi" cho cả 12 câu sẽ đúng 4 câu = 33,3%. Vậy hiệu pre/post
  dưới mức đó không có ý nghĩa, và đừng đọc 33% là "học sinh chưa biết gì". (Đo bằng mô
  phỏng trên chính `data/cauhoi.js`, không phải ước lượng.)
- **Post-test nay loại những câu học sinh đã gặp ở pre-test.** Trước đây hai phiên chỉ khác
  nhau ở seed mà bốc từ cùng một ngân hàng, nên trùng nhau trung bình 1,54/12 câu và 64% số
  cặp có ít nhất một câu trùng — tức post-test đo một phần trí nhớ câu cũ chứ không đo tiến bộ.
  Nếu ngân hàng hết câu mới, app NÓI RA ("phiên này có câu lặp lại, không dùng làm bằng chứng")
  và ghi cờ `phaiLap` vào nhật ký để lọc khi tổng hợp. Không im lặng bỏ qua.
- **Dữ liệu chỉ nằm trong trình duyệt của từng máy.** Phòng máy có phần mềm đóng băng ổ hoặc
  profile bị reset giữa hai ca thì dữ liệu biến mất. Vì vậy: cho học sinh **xuất CSV ngay sau
  mỗi hoạt động**, đừng để dồn tới cuối tiết.

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

**Bản hiện hành là v1.2.0** (09/10/2026) — đổi tên thương hiệu thành **AInatomy**, viết lại toàn bộ câu chữ giao diện sang giọng trung tính không ngôi.

Bốn điều nói rõ ở mốc này:

- **Tên mới AInatomy** = AI + Anatomy (giải phẫu), đúng việc sản phẩm làm: mở nắp từng trạm của hệ AI để xem bên trong. Đổi bằng `tools/doi_ten_ainatomy.py` (54 chỗ, kiểm kê từng chỗ, không replace toàn cục).
- **Phụ đề bỏ chữ "cấp THPT"**: nay là "Phòng thực hành Trí tuệ nhân tạo", vì sản phẩm không giới hạn cấp học. Ranh giới dữ liệu KHÔNG đổi — xem đoạn "Phạm vi dữ liệu đã kiểm chứng" ở đầu tệp. Cổng `G10b` khoá phụ đề mới ở ba nơi, cổng `G10f` nay khoá CẢ HAI đời phụ đề cũ (…lớp 10 và …cấp THPT) để không ai thêm lại vô ý.
- **Giọng văn trung tính, không ngôi**: bỏ xưng hô "em" ở toàn bộ chữ người dùng đọc (187 chỗ trong index.html và js/, data/kienthuc.js), việc nào ghi việc đó. Bốn nhóm GIỮ có chủ đích, lý do ghi trong docstring `tools/doi_giong_js.py`: từ khoá chấm bài (đổi là hỏng máy chấm), comment kỹ thuật, lời thoại hệ AI đang xúi lộ dữ liệu (bài học về thao túng), và hai ngân hàng câu hỏi ("em" nằm trong nội dung học thuật mà `giaiThich` trích nguyên văn; 56 câu đang chờ duyệt nhãn).
- **Tên repo và URL công khai ĐÃ ĐỔI** (09/10, theo quyết định của chủ sản phẩm, đảo
  quyết định 07/10 ở `THIET_KE_GIAO_DUC.md` §2.4): `soi-ai-lop10` -> `ainatomy`, trang
  công khai là `https://mxuanvan02.github.io/ainatomy/`. GitHub redirect địa chỉ kho (301)
  nhưng Pages KHÔNG redirect, đo bằng curl sau khi đổi: `github.io/soi-ai-lop10/` -> 404,
  `github.io/ainatomy/` -> 200. Mọi link trong hồ sơ đã được cập nhật và kiểm lại bằng
  `tools/quet_so_cu.py`. Thư mục mã nguồn trong repo hồ sơ vẫn tên `soi-ai/` (đường dẫn
  nội bộ, không phải slug công khai).

**Vì sao đổi tên.** Tên "SOI AI" hẹp hơn nội dung thật của sản phẩm. "Soi" là phương pháp của MỘT
phân hệ (Đấu trường bắt lỗi AI), trong khi hệ thống gồm năm phân hệ để HỌC VỀ AI: Xưởng huấn
luyện, Đấu trường bắt lỗi, Nhà máy AI 7 trạm, Lôgic & AI, và Bản đồ năng lực. Chủ sản phẩm
(giáo viên Tin học THPT) quyết định đổi ngày 08/10 — đảo ngược quyết định "giữ SOI AI" đã ghi
trong sheet quản lý dự án. Bản ghi quyết định cũ được GIỮ NGUYÊN trong
`tools/tao_sheet_thietke.py` và `tools/capnhat_sheet_cuoi.py` (viết đè nó sẽ làm bản ghi nói dối
về một câu hỏi đã được đặt ra), còn quyết định mới ghi ở đây và trong commit.

48 chỗ đã đổi bằng `tools/doi_ten_hoc_ai.py` — script có chế độ chỉ-kiểm, chốt chặn số chỗ, và
verify bốn chiều. Ba nhóm BẮT BUỘC giữ nguyên, và giữ là có lý do chứ không phải sót:

- `soiai_dulieu_v1` (khoá localStorage) và `soiai_nhatky_*.csv` — đổi khoá là XOÁ SẠCH dữ liệu học
  sinh đang lưu trong trình duyệt, không đảo ngược được.
- động từ "soi" trong nội dung dạy học ("soi mô hình", "soi ra chỗ hỏng", 25 lần) — đó là văn
  xuôi mô tả cơ chế, không phải tên.
- chuỗi `"Soi AI để hiểu AI"` trong DANH SÁCH TỪ CẤM của cổng `G10c` — đây là khẩu hiệu tiếp thị
  đã bị loại. Nếu thay thô thì chuỗi cấm biến thành "Học AI để hiểu AI" và cổng THÔI CẤM khẩu
  hiệu cũ mà vẫn in ĐẠT, tức vô hiệu hoá một tiêu chí trong im lặng.

Mốc trước đó:

Hai điều nói rõ để hồ sơ không khai quá:

- **Không có git tag cho v1.0.0.** Mốc chỉ là một commit trên `main`, không phải tag — nên đừng
  chép lệnh `git checkout v1.0.0` ở đâu cả, nó sẽ không tìm thấy gì. Muốn lấy đúng bản đó thì
  dùng hash `5c46f41`.
- **Các mục dưới đây là mốc CŨ, giữ nguyên làm lịch sử**: chúng ghi bản trước khi đổi tên, và
  tên "MỔ XẺ AI" trong đó đúng với thời điểm nó được viết.

- **v1.2.0** (09/10/2026): đổi tên thương hiệu HỌC AI -> **AInatomy** (54 chỗ, bằng
  `tools/doi_ten_ainatomy.py`); bỏ "cấp THPT" khỏi phụ đề; viết lại 187 chỗ xưng hô "em"
  sang giọng trung tính không ngôi (`tools/doi_giong_index.py`, `tools/doi_giong_js.py`);
  cổng G10f mở rộng khoá cả hai đời phụ đề cũ. Khoá localStorage, tên repo, URL,
  từ khoá chấm bài và hai ngân hàng câu hỏi giữ nguyên.
- **v1.1.0** (08/10/2026): đổi tên thương hiệu SOI AI -> **HỌC AI** (48 chỗ, bằng
  `tools/doi_ten_hoc_ai.py`). Phụ đề, đường dẫn, tên repo và URL công khai giữ nguyên. Khoá
  localStorage và động từ "soi" trong nội dung dạy học giữ nguyên.
- **v1.0.0** (04/10/2026): đổi tên thành SOI AI, trục báo cáo theo 13 chủ đề QĐ 2422, bỏ ngôn
  ngữ điểm số. Mốc: commit `5c46f41` (không có tag).
- **v0.2.0** (04/10/2026): 78 item (22 gốc + 56 LLM có QC), phiên phân tầng 12 câu,
  pre/post-test, CSV 19 cột có sự kiện phiên, script gộp đa máy. Đã smoke-test toàn bộ 3 tầng +
  pre/post + gộp CSV trên trình duyệt thật.
- **v0.1.0** (04/10/2026): bản đầu 3 tầng, 22 item.
- Git: mỗi phiên bản có commit + `SHA256SUMS` (bằng chứng mốc thời gian & toàn vẹn).

## 9. Căn cứ chương trình

- QĐ 2422/QĐ-BGDĐT (18/8/2026) — Khung nội dung giáo dục AI cho HS phổ thông (4 mạch, 12 tiết/lớp/năm).
- CV 5588/BGDĐT-GDPT (19/8/2026) — triển khai đại trà 2026–2027; yêu cầu không tài khoản cá nhân, không phụ thuộc nhà cung cấp, ưu tiên mã nguồn mở/miễn phí, có phiên bản ngoại tuyến.
- UNESCO AI Competency Framework for Students (2024) — 12 khối = 4 aspects × 3 levels.

Liên hệ tác giả: xem trong hồ sơ dự thi Giải thưởng Tiên phong Ứng dụng AI trong Giáo dục Việt Nam 2026.
