# HƯỚNG DẪN ĐÁNH GIÁ — từ minh chứng của app đến chữ trong sổ

Tệp này trả lời một câu hỏi rất cụ thể mà phản biện độc lập vòng 9 đã nêu là **lỗ hổng vận hành
lớn nhất**: Khung 2422 nói "không xác lập đầu điểm riêng cho nội dung giáo dục AI", vậy **giáo
viên ghi gì vào sổ điểm và nhận xét cuối kỳ?**

App sinh ra minh chứng. Minh chứng không tự thành chữ trong sổ. Tệp này là phần còn thiếu đó.

Dành cho: giáo viên Tin học THPT dạy chuyên đề AI lớp 10 bằng SOI AI, kể cả người chưa từng
dạy nội dung này và không quen thuật ngữ đo lường.

---

## 1. Ba tệp giáo viên nhận được, và mỗi tệp dùng để làm gì

Sau khi gộp (`python3 tools/gop_csv.py <thư_mục> -o <báo_cáo>` — xem README §4), có ba tệp:

| Tệp | Nội dung | Dùng khi nào |
|---|---|---|
| `nhatky_gop.csv` | Mọi sự kiện của mọi học sinh, có mốc thời gian | **Lưu làm minh chứng gốc.** Không dùng để đọc trực tiếp — vài trăm dòng |
| `baocao_lop.csv` | Recall theo 5 loại lỗi · tiến trình pre/post · bản đồ 12 khối UNESCO | Chiếu cuối tiết, và viết nhận xét **cả lớp** |
| `baocao_ca_nhan.csv` | Mỗi học sinh một dòng, 10 cột | Viết nhận xét **từng em** |

Mười cột của `baocao_ca_nhan.csv`:

```
ma_hs, ma_lop, so_cau_dau_truong, so_cau_dung, ti_le_dung, so_nhiem_vu_lab,
du_doan_da_doi_chieu, du_doan_khop, ti_le_du_doan_khop, du_doan_bo_qua
```

---

## 2. QUY TẮC QUAN TRỌNG NHẤT: cột `diem` KHÔNG phải là điểm

Trong `nhatky_gop.csv` có cột tên là `diem`, giá trị 0 hoặc 1. **Đó là cờ đúng/sai của MỘT câu
hỏi**, không phải điểm số. Cụ thể:

- `diem = 1` nghĩa là "phán quyết của em ở câu này đúng".
- `diem = 0` nghĩa là "phán quyết của em ở câu này chưa đúng".
- **Không cộng cột này thành điểm. Không chia lấy trung bình rồi ghi vào sổ điểm.**

Lý do, và đây không phải là chuyện câu chữ:

1. **Phần VI Khung 2422/QĐ-BGDĐT** quy định đánh giá nội dung giáo dục AI bằng nhận xét, và
   **không xác lập đầu điểm riêng** cho nội dung này. Cộng `diem` thành một con điểm là làm
   ngược lại văn bản mà chính chuyên đề này dựa vào.
2. **Nguyên tắc 3 trong `ke-hoach-12-tiet.md`**: "Một lần làm không phải kết luận về năng lực".
   Một cột 0/1 của một câu hỏi là dữ liệu của một lần làm.
3. Về mặt đo lường, con số đó **không phải điểm số**: nó chưa được kiểm định độ khó, chưa có
   trọng số, và mỗi học sinh có thể làm số câu khác nhau (12 câu ở phiên đấu trường, cộng thêm
   các nhiệm vụ lab và các ô dự đoán).

**Được phép làm gì với cột `diem`:** đếm số câu đúng trên tổng số câu đã làm của mỗi em (đó
chính là `so_cau_dung` / `so_cau_dau_truong` trong `baocao_ca_nhan.csv`) để biết em đang mạnh
hay yếu ở nhóm lỗi nào, rồi **viết thành nhận xét**. Dùng làm căn cứ cho chữ, không dùng làm
con điểm.

Nếu trường vẫn yêu cầu đầu điểm thường xuyên cho môn Tin: lấy điểm từ các nội dung khác của
môn theo quy chế hiện hành, và dùng chuyên đề AI này làm **căn cứ viết nhận xét**, không làm
căn cứ cho điểm. Nói thẳng điều này với tổ chuyên môn trước khi dạy, để không bị động khi đến
kỳ ghi sổ.

---

## 3. Ngưỡng "Đáp ứng tốt / một phần / Cần luyện thêm" — khai rõ nguồn gốc

App hiển thị ba mức đáp ứng. **Có hai bộ ngưỡng khác nhau trong app, và cả hai đều do tác giả
chọn, không trích từ văn bản nào.** Phải nói rõ, vì nếu không thì giáo viên sẽ tưởng chúng là
chuẩn của Bộ và trích dẫn sai khi bị hỏi.

| Nơi dùng | Ngưỡng | Ý nghĩa |
|---|---|---|
| Cột "Mức độ đáp ứng" theo từng chủ đề (`js/app.js`, hàm `mucDat`) | ≥ 0,7 tốt · ≥ 0,4 một phần · dưới 0,4 cần luyện | Gắn với **chủ đề** của Khung 2422 |
| Câu "Nhận xét tự động" (`js/engine.js`, hàm `taoNhanXet`) | ≥ 0,75 tốt · ≥ 0,5 khá · dưới 0,5 cần cố gắng | Gắn với **tỉ lệ đúng toàn bộ** phiên đấu trường |

**Căn cứ của các ngưỡng này: không có.** Chúng là lựa chọn của tác giả để chia ba khoảng đọc
được, không phải ngưỡng kiểm định, không phải chuẩn của Bộ, và không có tài liệu nào đứng sau.
Việc hai nơi dùng hai bộ số khác nhau cũng là một điểm chưa thống nhất — nó không gây sai số
liệu (hai nơi đo hai thứ khác nhau: theo chủ đề và toàn cục), nhưng **có thể gây nhầm khi đọc**,
và giáo viên nên biết trước để không phải giải thích vòng vo khi bị chất vấn.

**Giáo viên được phép chỉnh ngưỡng.** Nếu tổ chuyên môn của trường muốn dùng 0,6/0,3 thì sửa
hai hằng số đó trong `js/app.js` (tìm `mucDat`) và `js/engine.js` (tìm `taoNhanXet`). Sau khi
sửa, chạy `python3 tools/nghiem_thu.py` để chắc không vỡ gì.

**Cách dùng đúng:** coi ba mức đó là **gợi ý đọc dữ liệu**, không phải kết luận. Nếu một em chỉ
làm 3 câu thì "Đáp ứng tốt" trên 3 câu không có nghĩa gì — luôn nhìn cặp **số đúng / tổng số
câu**, đừng nhìn mỗi tỉ lệ.

---

## 4. Sáu mẫu câu nhận xét — chép được ngay, chỉ điền số

Mỗi mẫu gắn với dữ liệu thật trong `baocao_ca_nhan.csv` hoặc `baocao_lop.csv`. Phần `[trong
ngoặc vuông]` là chỗ điền. Tên năm loại lỗi dùng đúng như app hiển thị: **Số liệu bịa đặt ·
Nguồn/văn bản không tồn tại · Thiên kiến, định kiến · Suy luận sai · Xúi lộ dữ liệu cá nhân**.

### Mẫu 1 — Em nhận diện lỗi tốt, đều các nhóm

> Điều kiện: `ti_le_dung` ≥ 0,7 **và** `so_cau_dau_truong` ≥ 12.

```
Em [mã HS] đã thực hiện [số] nhiệm vụ trong chuyên đề AI. Nhận diện được [số_cau_dung]/[số]
trường hợp AI đưa thông tin sai, đều ở các nhóm lỗi. Có ý thức đối chiếu kết quả của AI với
nguồn thật trước khi tin. Cần tiếp tục rèn việc chỉ ra ĐƯỢC vì sao thông tin đó sai, thay vì
chỉ nhận ra nó sai.
```

### Mẫu 2 — Em mạnh một nhóm, yếu một nhóm (mẫu hay gặp nhất)

> Điều kiện: nhìn `baocao_lop.csv` hoặc recall theo loại của em; tìm nhóm cao nhất và thấp nhất.

```
Em [mã HS] tham gia đủ [số] hoạt động của chuyên đề. Nhận diện tốt các trường hợp AI bịa
số liệu ([x]/[y] lần phát hiện đúng); còn bỏ sót các trường hợp AI suy luận sai
([a]/[b] lần). Đã biết đặt câu hỏi "con số này lấy từ đâu", cần rèn thêm câu hỏi
"từ dữ kiện này suy ra kết luận đó có hợp lí không".
```

### Mẫu 3 — Em hay "bắt oan" (phán có lỗi trên câu đúng)

> Điều kiện: cột `bat_oan` cao. Đây là lỗi đáng chú ý về mặt tư duy, không phải lỗi kỹ năng.

```
Em [mã HS] có ý thức hoài nghi kết quả do AI đưa ra, nhưng [số] lần đã phán "có lỗi" với
câu trả lời vốn đúng. Xu hướng nghi ngờ là tốt, song cần học cách kiểm tra lại bằng chứng
trước khi kết luận: hoài nghi mà không có căn cứ thì cũng là một dạng sai. Đã tiến bộ ở
nhóm [tên nhóm lỗi].
```

### Mẫu 4 — Em còn bỏ sót nhiều lỗi

> Điều kiện: `ti_le_dung` < 0,4 **và** `so_cau_dau_truong` ≥ 8 (đủ dữ liệu để nhận xét).

```
Em [mã HS] đã tham gia [số] hoạt động. Bước đầu nhận diện được [số_cau_dung] trường hợp AI
đưa thông tin sai; còn bỏ sót [số] trường hợp, nhiều nhất ở nhóm [tên nhóm lỗi]. Cần luyện
lại với các tình huống cùng loại, tập trung vào việc đọc chậm và kiểm tra từng con số, từng
nguồn được nêu. Đã có tiến bộ so với khảo sát đầu vào ([pre]% → [post]%).
```

### Mẫu 5 — Em dự đoán tốt trước khi chạy (Mức 3 — nên khen, vì đây là năng lực khó)

> Điều kiện: `ti_le_du_doan_khop` ≥ 0,6 **và** `du_doan_da_doi_chieu` ≥ 3.

```
Em [mã HS] có khả năng hình dung trước kết quả của hệ AI: dự đoán khớp với kết quả thật
[du_doan_khop]/[du_doan_da_doi_chieu] lần. Đây là biểu hiện của việc hiểu cơ chế hoạt động
bên trong chứ không chỉ biết bấm nút. Cần phát triển thêm bằng cách giải thích được vì sao
mình dự đoán như vậy.
```

### Mẫu 6 — Em tham gia nhưng chưa đi qua vòng dự đoán

> Điều kiện: `du_doan_bo_qua` ≥ 2 **hoặc** (`du_doan_da_doi_chieu` = 0 **và** `so_cau_dau_truong` > 0).

```
Em [mã HS] đã hoàn thành [số] nhiệm vụ thực hành và nhận diện được [số_cau_dung] trường hợp
AI sai. Tuy nhiên em thường bỏ qua bước dự đoán trước khi cho hệ chạy ([du_doan_bo_qua] lần),
nên chưa thấy được chỗ mình hiểu khác với thực tế. Tiết sau cần làm trọn vòng: DỰ ĐOÁN → cho
chạy → SO SÁNH, vì chính chỗ lệch nhau là chỗ cần học.
```

**Lưu ý khi dùng mẫu 6:** `du_doan_bo_qua` đo **hành vi tham gia**, không đo năng lực. Một em
bỏ qua dự đoán không có nghĩa là em yếu. Và ngược lại — đừng dùng con số này để xếp loại.

---

## 5. Nhận xét CẢ LỚP (cho biên bản tổ chuyên môn, hoặc chiếu cuối tiết)

Lấy từ `baocao_lop.csv`:

```
Lớp [10A..], [sĩ số] học sinh tham gia chuyên đề AI, thực hiện trên [số] tiết.
Cả lớp phát hiện đúng [x]/[y] trường hợp AI đưa thông tin sai ([recall]%).
Nhóm lỗi nhận diện tốt nhất: [tên nhóm] ([số]%).
Nhóm lỗi còn bỏ sót nhiều: [tên nhóm] ([số]%).
Số lượt "bắt oan" (phán có lỗi trên câu đúng): [số] — cho thấy học sinh đã có ý thức hoài
nghi kết quả của AI, nhưng cần rèn cách kiểm chứng.
Tiến trình: khảo sát đầu vào [pre]% → cuối chuyên đề [post]% (trung bình tỉ lệ phán quyết đúng).
[số] học sinh có thực hiện bước dự đoán trước khi cho hệ chạy; trong đó dự đoán khớp kết quả
thật [k]% — đây là chỉ báo của việc hiểu cơ chế, không chỉ vận hành.
```

**Ba điều phải nói kèm khi trình bày số liệu này**, nếu không sẽ bị hiểu sai:

1. **Sàn may rủi là 33%.** Mỗi phiên 12 câu gồm 8 câu có lỗi và 4 câu đúng; một học sinh chỉ
   phán "không có lỗi" cho cả 12 câu vẫn đúng được 4 câu. Vậy hiệu pre/post **dưới 33% thì
   không có ý nghĩa**, và đừng đọc 33% là "học sinh chưa biết gì". (Con số này đo bằng mô phỏng
   trên chính ngân hàng câu hỏi, không phải ước lượng.)
2. **Cột `so_phien_bi_loai_vi_lap_cau`.** Nếu khác 0 thì ngần ấy phiên đã bị loại khỏi trung
   bình pre/post, vì ngân hàng hết câu mới và hệ phải cho lặp câu học sinh đã gặp — phiên đó
   không còn đo được tiến bộ. Nói rõ số này ra, đừng để con số tiến bộ trông đẹp hơn thực tế.
3. **Không xếp hạng.** Nguyên tắc 1 của `ke-hoach-12-tiet.md`: báo cáo lớp chỉ hiện tỉ lệ theo
   loại lỗi, không hiện tên học sinh kèm kết quả.

---

## 6. Học sinh nghỉ ốm, nghỉ phép — tổng hợp thế nào?

App chỉ ra mức đáp ứng **theo từng chủ đề khi có dữ liệu**. Nếu một em nghỉ 3 tiết thì các chủ
đề của 3 tiết đó **không có dữ liệu**, và bảng sẽ hiện "chưa có dữ liệu" — không phải 0%,
không phải "Cần luyện thêm". Đây là cách app cố ý cư xử: **thiếu dữ liệu thì để trống, không
suy ra điểm kém.**

Khi viết nhận xét cho em đó:

- **Không** điền "0%" hay "chưa đạt" vào chỗ trống. Viết rõ "chưa có minh chứng ở chủ đề [...]
  do học sinh vắng".
- Nếu cần đủ minh chứng cho cả chuyên đề: cho em làm **bù** hoạt động của tiết đã nghỉ (app chạy
  offline, mở `index.html` từ USB là làm được, không cần cả lớp cùng làm).
- Nếu không thể bù: nhận xét dựa trên **những chủ đề có dữ liệu**, và ghi rõ phạm vi. Ví dụ
  "nhận xét này dựa trên 6/12 tiết chuyên đề do em vắng [...]".
- **Tuyệt đối không** lấy trung bình của cả lớp gán cho em. Đó là ghi số liệu không có thật
  vào hồ sơ.

---

## 7. Nếu bị hỏi "lấy gì minh chứng?" — trả lời thế nào

Ba thứ, theo thứ tự thuyết phục:

1. **`nhatky_gop.csv`** — có mốc thời gian cho từng sự kiện, từng mã học sinh. Đây là minh chứng
   quá trình, không phải ảnh chụp kết quả.
2. **`SHA256SUMS.txt` + `out/judge_result.json`** — mã nguồn và bộ câu hỏi có hash, và cổng
   nghiệm thu ghi lại số tiêu chí đạt cùng commit. Ai sửa nội dung câu hỏi sau khi dạy thì hash
   sẽ lệch.
3. **Bản sao lưu JSON** — mỗi lần ai đó bấm nút "Xóa dữ liệu", app tự tải một bản JSON đầy đủ
   về máy trước khi xoá. Nên kể cả khi dữ liệu trên máy bị xoá nhầm, vẫn còn bản đó.

**Câu hỏi khó nhất và cách trả lời thẳng:** "Giáo viên có chắc học sinh không nhập mã của bạn
để phá không?" — **Không chắc.** App chỉ kiểm mã không rỗng, không có danh sách mã hợp lệ và
không khoá theo máy; một học sinh nhập mã của bạn thì mọi phán quyết sẽ cộng vào nhật ký của
bạn đó. Đây là giới hạn thật của phiên bản hiện tại, và cách phòng vệ đang dùng là **quy trình**
(mỗi mã gắn một máy cố định trong cả chuyên đề, cuối tiết hỏi nhanh có máy nào nhập mã lạ
không), không phải kỹ thuật. Nói thẳng giới hạn này thuyết phục hơn là né, vì hội đồng thường
hỏi đúng chỗ yếu nhất.

---

## 8. Việc máy không làm thay được

- **Ký xác nhận.** Văn bản cho phép của BGH, chữ ký của tổ chuyên môn — xem
  `ho-so/mau_xin_phep_BGH.md`.
- **Duyệt nhãn câu hỏi sinh bằng LLM.** `data/cauhoi_moRong.js` có 56 câu sinh tự động, đã soát
  mẫu và quét schema, nhưng **chưa được tác giả duyệt nhãn 100%**. Đừng dùng 56 câu đó làm
  bằng chứng trước khi tự đọc và duyệt từng câu.
- **Dạy thật.** Mọi con số trong tệp này là năng lực của **công cụ đo**, không phải kết quả
  của một lớp học thật. Sản phẩm chưa được dạy trên lớp thật với học sinh thật, và hồ sơ phải
  nói rõ điều đó.
