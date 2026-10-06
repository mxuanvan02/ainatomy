/* SOI AI — muc3.js : MỨC 3 CHO BẢY BÀI CÒN LẠI (BT-01, 03, 06, 07, 08, 10, 12).
 *
 * VÌ SAO CÓ TỆP NÀY
 *   THIET_KE_BAI_TOAN.md PHẦN 4.4 định nghĩa ba mức, Mức 3 = "EM DỰ ĐOÁN TRƯỚC".
 *   Trước tệp này, phép đo trên mã sống cho thấy chỉ 6/13 bài có Mức 3 vẽ ra cho học sinh:
 *     đã có: BT-02, BT-04, BT-05, BT-11 (ô dự đoán số/phương án — js/duDoan.js)
 *            BT-09 (học sinh tự cài một lỗi cho bạn bắt — js/bt09.js)
 *            BT-13 (học sinh tự tìm ứng dụng AI của chính em — js/bt13.js)
 *   Bảy bài còn thiếu nằm ở đây.
 *
 * BA DẠNG Ô, CHỌN THEO BẢN CHẤT CỦA BÀI — không ép mọi bài vào một khuôn
 *   veChon   (BT-01, BT-07)  dự đoán một PHƯƠNG ÁN; hệ biết đáp án nên chấm tất định.
 *   veTruot  (BT-03, BT-06)  dự đoán một CON SỐ %; hệ so với kết quả thật của chính
 *                            mô hình vừa huấn luyện, ngưỡng khớp ±10 điểm %.
 *   veTuLuan (BT-08, 10, 12) bài viết tự do, KHÔNG có đáp án đúng duy nhất.
 *
 * VÌ SAO BT-08/10/12 DÙNG Ô TỰ LUẬN MÀ KHÔNG PHẢI TRẮC NGHIỆM
 *   PHẦN 4.5 của thiết kế ghi rõ: "ở chặng 2 và 3 thì BT-10 và BT-12 KHÔNG còn đáp án
 *   duy nhất". BT-08 yêu cầu viết prompt cho một việc chưa từng làm; BT-10 yêu cầu đề
 *   xuất biện pháp cho dự án của CHÍNH NHÓM EM; BT-12 yêu cầu viết nguyên tắc dùng AI
 *   của RIÊNG EM. Bịa một "đáp án đúng" cho ba việc đó là làm giả phép chấm.
 *   Ba bài này chấm theo cách khác mà vẫn tất định: đếm xem bài viết có CHẠM các phương
 *   diện bắt buộc không (đếm từ khoá trên chuỗi đã bỏ dấu — cùng cơ chế với rubric prompt
 *   ở js/nhamay_text.js hàm danhGiaPrompt). Kết quả hiện là "chạm N/M phương diện",
 *   KHÔNG phải điểm số — đúng phần VI Khung 2422 ("không xác lập đầu điểm riêng").
 *
 * HAI CHỖ LỆCH SO VỚI NGUYÊN VĂN THIẾT KẾ — ghi rõ để người sau không tưởng đã làm đúng chữ
 *   1. BT-03: PHẦN 4.4 viết "dự đoán vòng thứ 30 lỗi còn bao nhiêu". Đo đúng giữa chuỗi 60
 *      vòng thì phải chèn móc vào vòng lặp hocHet() của js/lab.js. Bản này đo ở MỐC CUỐI
 *      (độ chính xác trên chính bộ dữ liệu vừa học), vì đó là mốc mã hiện có và nó rèn CÙNG
 *      một hiểu biết: mô hình học thuộc dữ liệu huấn luyện nên điểm trên đó cao hơn hẳn điểm
 *      trên ảnh mới. Muốn đúng nguyên văn thì phải sửa js/lab.js phát sự kiện giữa chuỗi.
 *   2. BT-08: PHẦN 4.4 viết "tự chấm trước khi hệ chấm". Ô này chấm 6 phương diện TRÙNG với
 *      6 tiêu chí rubric của hệ (js/nhamay_text.js RUBRIC_PROMPT), nên học sinh tự chấm rồi
 *      đối chiếu được — nhưng hai phép chấm KHÔNG dùng chung mã, nên có thể lệch nhau một
 *      chút. Không đồng bộ mã vì rubric của hệ là phép kiểm của sản phẩm, sửa nó là sửa
 *      phép nghiệm thu (vi phạm ranh giới của chính dự án).
 *
 * CHỐNG DÒ ĐÁP ÁN: mọi ô chỉ chốt được MỘT lần; muốn dự đoán tiếp phải tạo lại bộ dữ liệu
 *   hoặc lượt chơi mới, khi đó đáp án cũng đổi theo. Cơ chế nằm trong js/duDoan.js.
 *
 * AN TOÀN: chữ học sinh gõ KHÔNG bao giờ trở thành HTML. Mọi nội dung động đi qua
 *   MX_DUDOAN (module đó dựng bằng createElement + textContent, chỉ dùng innerHTML cho
 *   svgIco() hằng số). Bản thân tệp này có **1 chỗ** gán innerHTML: dòng
 *   `host.innerHTML = ""` trong hàm mo(), để XOÁ SẠCH host trước khi dựng lại ô. Chuỗi
 *   được gán là hằng số rỗng nên không có đường nào cho dữ liệu đi vào.
 *   (Ghi chú này từng khai "KHÔNG dùng innerHTML" trong khi mã sống có 1 chỗ — cổng G11d
 *   bắt được vì nó đếm trên mã sống chứ không tin ghi chú. Số ở đây là số ĐO ĐƯỢC.)
 */
(function(){
  "use strict";

  const D = () => window.MX_DUDOAN;

  /* ===== GHI NHẬT KÝ LỚP — tách ra để tệp này KHÔNG phụ thuộc engine.js =====
   * app.js gắn hàm vào MX_MUC3.ghiLog, vì chỉ app.js biết maHS (mã ẩn danh) và có
   * ENG.logSuKien. Nếu tệp này tự gọi ENG.logSuKien thì nó hỏng khi engine.js chưa nạp
   * — đúng lớp lỗi mà cổng G11a đang bắt (thứ tự nạp script). */
  let GHI = null;
  /* Tập mã bài ĐÃ chốt dự đoán trong phiên đăng nhập hiện tại.
   * VÌ SAO CẦN (lỗi tìm được khi test end-to-end 06/10): một ô Mức 3 có thể bị DỰNG LẠI
   * (mo() gọi lần nữa khi giao diện vẽ lại bước tiếp theo), và bản dựng mới có `chot = null`.
   * Nếu sau đó có lời gọi doiChieu trên bản mới, hàm gốc trả null — và nhánh "học sinh bỏ
   * qua" sẽ ghi oan cho một em ĐÃ dự đoán. Đã xảy ra thật: mã A901 chốt 65, có cả sự kiện
   * doiChieu, rồi vẫn bị ghi thêm boQua.
   * Tập này chặn ca đó: đã chốt rồi thì không bao giờ ghi "bỏ qua" cho mã ấy nữa.
   * Được XOÁ khi ghiLog() gọi lại (tức lúc đăng nhập), nên không lẫn giữa hai học sinh
   * dùng chung máy — đúng chu kỳ sống của một phiên. */
  let DA_CHOT = new Set();

  function ghi(ma, giaTri, suKien, kqBoSung){
    if(!GHI) return;
    if((suKien || "chot") === "chot") DA_CHOT.add(ma);
    try { GHI(ma, giaTri, suKien || "chot", kqBoSung || null); }
    catch(e) { /* log lỗi không được làm hỏng bài học */ }
  }

  /* Ghi KẾT QUẢ ĐỐI CHIẾU — thêm 06/10.

     LỖI ĐÃ SỬA: trước đây các ô Mức 3 chỉ ghi sự kiện lúc học sinh BẤM CHỐT
     (suKien:"chot", kq:{duDoan:...}), còn kết quả so với đáp án thật thì KHÔNG ghi.
     Đồng thời engine.js cũng không có nhánh nào đọc sự kiện "duDoan". Hai đầu cùng hở
     nên 13 ô Mức 3 không đóng góp gì vào Bản đồ năng lực lẫn báo cáo lớp — giáo viên
     không biết học sinh dự đoán đúng hay sai, và CSV không phân biệt được "dự đoán sai"
     với "không thèm dự đoán".

     CHUẨN HOÁ MỘT DẠNG cho cả ba loại ô, vì mỗi loại trả về hình dạng khác nhau:
       ô trượt  (veTruot)  -> { khop, duDoan, ketQua, lech }
       ô chọn   (veChon)   -> { khop, duDoan, dapAn }
       ô tự luận(veTuLuan) -> { cham, dat, tong, tiLe }   (không có "đúng/sai")
     Bên đọc (engine.js tongHop) chỉ cần một trường `dung` boolean, nên việc suy ra nó
     phải làm Ở ĐÂY, ngay chỗ biết rõ hình dạng dữ liệu — không đẩy việc đoán cho nơi đọc.
     Ô tự luận không có đáp án đúng duy nhất, nên lấy ngưỡng 60% phương diện đã chạm
     (đúng ngưỡng mà giao diện veTuLuan đang dùng để tô màu phản hồi).

     `diem` 0/1 được ghi kèm vì tools/gop_csv.py đọc cột `diem` theo tên — có nó thì báo
     cáo gộp đa máy tự tính được, không phải sửa công cụ gộp. */
  /* ĐỔI PHẦN LẺ -> PHẦN TRĂM cho ô trượt, để hai sự kiện nói cùng một thứ tiếng.

     LỖI ĐÃ SỬA (06/10, tìm được bằng test end-to-end chứ không phải bằng đọc): với BT-03,
     một lần dự đoán sinh ra HAI sự kiện và hai sự kiện đó ghi hai đơn vị khác nhau cho
     CÙNG một câu trả lời:
       sự kiện "chot"     -> 65    (vì muc3.js ghi Math.round(v * 100))
       sự kiện "doiChieu" -> 0.65  (vì duDoan.js trả dc.duDoan = chot, và chot được tính
                                    bằng parseInt(inp.value,10)/100 tức phần lẻ 0..1)
     Giáo viên mở CSV sẽ thấy dòng trên ghi 65, dòng dưới ghi 0.65 cho một em — không biết
     tin dòng nào, và nếu tính trung bình thì sai hẳn. Chuẩn hoá về phần trăm vì đó là đơn vị
     mà giao diện đang hiện ("Đã chốt: 65%") và là đơn vị mà các chỗ ghi khác đang dùng.

     Chỉ đổi khi giá trị là SỐ nằm trong [0,1]. Ba loại ô trả về ba hình dạng khác nhau:
       ô trượt   -> số (phần lẻ 0..1)      -> đổi
       ô chọn    -> chuỗi id ("b")         -> giữ nguyên (không phải số)
       ô tự luận -> không có, ta dựng "6/6" -> giữ nguyên
     `dapAn` cũng đi qua hàm này: với ô trượt nó là độ chính xác thật (0..1), và test đã ghi
     ra `dapAn: 1` cho ca 100% — nếu không đổi thì "dự đoán 65, đáp án 1" đọc như sai 64 điểm
     trong khi thật ra là sai 35 điểm. */
  function pct(v){
    if(typeof v === "number" && v >= 0 && v <= 1) return Math.round(v * 100);
    return v;
  }

  function ghiDoiChieu(ma, dc){
    if(!dc) return;
    const dung = (dc.khop !== undefined) ? !!dc.khop
               : (dc.tiLe !== undefined ? dc.tiLe >= 0.6 : false);
    const duDoan = (dc.duDoan !== undefined) ? pct(dc.duDoan)
                 : (dc.dat !== undefined ? (dc.dat + "/" + dc.tong) : "");
    const dapAn  = (dc.dapAn !== undefined) ? pct(dc.dapAn)
                 : (dc.ketQua !== undefined ? pct(dc.ketQua) : "");
    ghi(ma, duDoan, "doiChieu", {
      duDoan: duDoan, dapAn: dapAn,
      diem: dung ? 1 : 0, dung: dung,
      phuongDienCham: dc.dat !== undefined ? dc.dat : "",
      phuongDienTong: dc.tong !== undefined ? dc.tong : ""
    });
  }

  /* Chấm NGAY khi học sinh chốt, cho bốn bài có đáp án tính được từ mã.
   * `tl` là hàm do app.js truyền vào, trả về:
   *    số 0..1            -> ô trượt, so với kết quả thật (BT-03, BT-06)
   *    {dapAn, giaiThich} -> ô chọn, so với đáp án (BT-01, BT-07)
   * KHÔNG chấm bằng hằng số viết tay: hàm này gọi `tl()` để app.js TÍNH đáp án từ dữ
   * liệu thật của bài (vector đặc trưng, độ chính xác mô hình...). Nếu viết đáp án cứng
   * ở đây thì khi dữ liệu đổi, ô dự đoán vẫn "chấm" theo ký ức — sai âm thầm. */
  function chamSau(api, tl){
    if(!api || !tl) return;
    if(api.daDoiChieu) return;      // đã đối chiếu rồi thì không chấm lại
    let r;
    try { r = tl(); } catch(e){ return; }
    if(r == null) return;
    if(typeof r === "number") { api.doiChieu(r); return; }
    if(r.so != null)         { api.doiChieu(r.so); return; }
    if(r.dapAn != null)      { api.doiChieu(r.dapAn, r.giaiThich); }
  }

  /* ====================== BT-01 · Với máy, một bức ảnh là gì? ====================
   * Định vị: Trạm 0 NHẬP LIỆU (#nm-tram0), ngay TRƯỚC bảng đặc trưng.
   *
   * ĐỔI CÂU HỎI SO VỚI BẢN NHÁP ĐẦU — ghi rõ vì sao, để người sau không tưởng là tuỳ tiện:
   *   Bản nháp hỏi "ảnh bị làm THÔ đi thì máy còn phân biệt được không", bám theo nguyên
   *   văn PHẦN 4.4 ("ảnh 8px"). Nhưng khi đọc mã thật thì `t0-so` là SỐ ẢNH (8–24 tấm),
   *   KHÔNG phải số điểm ảnh — app không có nút chỉnh độ phân giải. Hỏi một điều mà app
   *   không làm được thì không có gì để đối chiếu, và ô dự đoán thành trang trí.
   *   Câu hỏi mới vẫn rèn ĐÚNG hiểu biết của BT-01 (máy chỉ thấy con số, không "hiểu" ảnh)
   *   và đối chiếu được bằng số thật: so bốn đặc trưng của một ảnh ban ngày với một ảnh
   *   ban đêm CÙNG nhãn "CÓ mũ". Nếu bốn số khác nhau thì đáp án là "khac".
   *   Đáp án do mã tính (hàm traLoiBT01 trong app.js), không do người viết tay. */
  function bt01(host, tl){
    const api = D().veChon(host, {
      cauHoi: "Hai bức ảnh CÙNG một đối tượng (cùng nhãn), chỉ khác nhau ở điều kiện sáng "
        + "(một chụp ban ngày, một chụp ban đêm). Theo em, bốn con số mà máy đọc được "
        + "từ hai ảnh đó có GIỐNG nhau không?",
      phuongAn: [
        { id: "giong", text: "Giống nhau — cùng là 'có mũ' thì máy phải đọc ra như nhau" },
        { id: "khac",  text: "Khác nhau — máy chỉ đọc con số, mà con số phụ thuộc ánh sáng" }
      ],
      onChot(v){ ghi("BT-01", v); chamSau(api, tl); }
    });
    return api;
  }
  /* Đáp án BT-01 = "khac". Bốn đặc trưng (xem dacTrung/vec trong js/lab.js) đều là ĐẠI LƯỢNG
   * ÁNH SÁNG: tỉ lệ điểm rất sáng, tỉ lệ sáng vừa, độ sáng vùng đầu, tỉ lệ tối. Ảnh ban đêm
   * cho bộ số khác hẳn ảnh ban ngày dù cùng nhãn — đó là gốc rễ của thiên kiến ngày/đêm mà
   * cả Tầng 1 điều tra. app.js tự so hai vector đặc trưng rồi gọi doiChieu() với đáp án ĐO ĐƯỢC. */

  /* ====================== BT-03 · Máy học bằng cách nào? ==========================
   * Định vị: Tầng 1, bước 2 (#lab-b2) — học sinh dự đoán TRƯỚC khi bấm "Huấn luyện".
   * Kết quả đối chiếu = kqTrain.doChinhXac, tính xong ngay trong labHuanLuyen(). */
  function bt03(host, tl){
    const api = D().veTruot(host, {
      cauHoi: "Sắp tới hệ huấn luyện 60 vòng trên bộ dữ liệu LỆCH. "
        + "Theo em, độ chính xác của mô hình trên CHÍNH bộ dữ liệu nó vừa học là bao nhiêu?",
      dungSai: 0.10,
      ghiChu: "Đây là điểm trên dữ liệu nó vừa học — thường CAO hơn hẳn điểm trên ảnh mới. "
        + "Chốt TRƯỚC khi bấm 'Huấn luyện mô hình AI'. Ngưỡng khớp ±10 điểm %.",
      onChot(v){ ghi("BT-03", Math.round(v * 100)); chamSau(api, tl); }
    });
    return api;
  }

  /* ====================== BT-06 · Sửa thiên kiến bằng cách nào? ====================
   * Định vị: Tầng 1, bước 3 (#lab-b3), ngay TRƯỚC nút "Thử lại với bộ dữ liệu CÂN BẰNG".
   * Kết quả đối chiếu = lab.kqDemC2.doChinhXac (lần huấn luyện cân bằng), tất định. */
  function bt06(host, tl){
    const api = D().veTruot(host, {
      cauHoi: "Sắp tới hệ huấn luyện LẠI với bộ dữ liệu ĐÃ CÂN BẰNG ngày/đêm. "
        + "Theo em, độ chính xác trên ảnh BAN ĐÊM sẽ thành bao nhiêu?",
      dungSai: 0.10,
      ghiChu: "Ban đêm đang rất thấp. Câu hỏi là nó lên tới đâu sau khi bổ sung dữ liệu. "
        + "Chốt TRƯỚC khi bấm nút cân bằng. Ngưỡng khớp ±10 điểm %.",
      onChot(v){ ghi("BT-06", Math.round(v * 100)); chamSau(api, tl); }
    });
    return api;
  }

  /* ====================== BT-07 · Khi AI nói trôi chảy mà không có căn cứ ==========
   * Định vị: Trạm 5 (#nm-tram5), ngay TRÊN ô nhập câu hỏi.
   * Hệ biết trước chủ đề nào có trong ngữ liệu (nhanDienChuDe của js/nhamay_text.js),
   * nên đáp án tất định — không cần giáo viên đọc câu trả lời. */
  function bt07(host, tl){
    const api = D().veChon(host, {
      cauHoi: "Hệ này chỉ được học bốn chủ đề: nông nghiệp, y tế, giáo dục, môi trường. "
        + "Nếu em hỏi một việc NGOÀI cả bốn chủ đề đó (ví dụ giá vàng hôm nay), "
        + "theo em hệ sẽ làm gì?",
      phuongAn: [
        { id: "biao",    text: "Vẫn trả lời trôi chảy, nhưng nội dung là bịa — không có căn cứ trong dữ liệu đã học" },
        { id: "tuuchoi", text: "Từ chối thẳng: 'tôi không biết chủ đề này'" },
        { id: "hoc",     text: "Tự tìm trên mạng rồi trả lời đúng" }
      ],
      onChot(v){ ghi("BT-07", v); chamSau(api, tl); }
    });
    return api;
  }
  /* Đáp án BT-07 = "biao". Đây là điểm mấu chốt của cả chặng 3: học sinh phải hình dung
   * TRƯỚC rằng máy không biết là mình không biết. app.js gọi doiChieu("biao", ...) sau khi
   * hệ đã sinh câu trả lời — khi đó chẩn đoán căn cứ đã có thật. */

  /* ====================== BT-08 · Viết một prompt có mục tiêu ======================
   * Định vị: Trạm 5, ngay dưới ô prompt và bảng rubric của hệ.
   * Sáu phương diện dưới đây soi ĐÚNG sáu tiêu chí mà rubric của hệ dùng. */
  function bt08(host){
    return D().veTuLuan(host, {
      cauHoi: "Hãy viết một prompt cho một việc em CHƯA TỪNG làm, rồi TỰ CHẤM xem prompt "
        + "của em có đủ các ý dưới đây không — trước khi bấm nút để hệ chấm.",
      goiY: "Ví dụ: 'Hãy liệt kê 3 ứng dụng AI trong nông nghiệp ở Việt Nam, trình bày dạng bảng có 2 cột'...",
      soTuToiThieu: 12,
      tuChamNgay: true,
      phuongDien: [
        { ma: "muc-tieu", moTa: "nói rõ em muốn gì (mục tiêu của việc)", tuKhoa: ["liệt kê", "viết", "tạo", "giải thích", "so sánh", "mô tả", "tính", "tìm", "gợi ý", "hãy"] },
        { ma: "ngu-canh", moTa: "nêu ngữ cảnh (cho ai, ở đâu, tình huống nào)", tuKhoa: ["cho học sinh", "cho lớp", "ở việt nam", "trong trường", "cho phụ huynh", "ngữ cảnh", "bối cảnh", "của em", "cho em"] },
        { ma: "dinh-dang", moTa: "yêu cầu định dạng đầu ra (bảng, danh sách, số câu)", tuKhoa: ["dạng bảng", "bảng", "danh sách", "gạch đầu dòng", "câu", "đoạn văn", "dạng cột", "dạng sơ đồ"] },
        { ma: "gioi-han", moTa: "nêu giới hạn hoặc điều KHÔNG được làm", tuKhoa: ["không được", "đừng", "chỉ dùng", "không quá", "tối đa", "giới hạn"] },
        { ma: "nguon", moTa: "nói rõ lấy thông tin từ đâu", tuKhoa: ["theo dữ liệu", "trong kho", "dựa trên", "nguồn", "trích"] },
        { ma: "tu-danh-gia", moTa: "nói em sẽ kiểm lại kết quả thế nào", tuKhoa: ["kiểm tra", "kiểm lại", "đối chiếu", "xác minh", "tự chấm", "so lại"] }
      ],
      onChot(v){ ghi("BT-08", String(v).slice(0, 400)); }
    });
  }

  /* ====================== BT-10 · Tình huống có thật ở trường Việt Nam ==============
   * Định vị: view v-tinhhuong, dưới danh sách 12 tình huống.
   * Mức 3 KHÔNG có đáp án duy nhất (PHẦN 4.5). Chấm bằng đếm phương diện, không bịa đáp án. */
  function bt10(host){
    return D().veTuLuan(host, {
      cauHoi: "Nghĩ về MỘT dự án AI mà nhóm em hoặc trường em đang làm (hoặc định làm). "
        + "Hãy đề xuất biện pháp hạn chế rủi ro cho dự án đó.",
      goiY: "Ví dụ: 'Dự án điểm danh bằng nhận diện khuôn mặt...' rồi nêu biện pháp cụ thể.",
      soTuToiThieu: 30,
      tuChamNgay: true,
      phuongDien: [
        { ma: "rui-ro", moTa: "nêu rủi ro cụ thể của dự án (cho ai, hậu quả gì)", tuKhoa: ["rủi ro", "có thể bị", "hậu quả", "ảnh hưởng", "thiệt", "sai sót"] },
        { ma: "du-lieu", moTa: "nói về dữ liệu: dùng gì, của ai, xin phép thế nào", tuKhoa: ["dữ liệu", "xin phép", "đồng ý", "ẩn danh", "mã hóa", "lưu trữ"] },
        { ma: "minh-bach", moTa: "nói về minh bạch: người dùng biết hệ dựa vào đâu", tuKhoa: ["minh bạch", "công bố", "giải thích", "cho biết", "nói rõ"] },
        { ma: "con-nguoi", moTa: "nêu vai trò người kiểm / người quyết định cuối", tuKhoa: ["con người", "giáo viên", "quyết định cuối", "kiểm tra lại", "giám sát", "thầy cô"] },
        { ma: "pham-vi", moTa: "nói rõ phạm vi áp dụng và giới hạn của hệ", tuKhoa: ["phạm vi", "giới hạn", "chỉ dùng khi", "không dùng cho", "áp dụng cho"] },
        { ma: "du-phong", moTa: "có phương án thay thế khi hệ sai", tuKhoa: ["phương án", "thủ công", "dự phòng", "thay thế", "nếu hệ sai", "kiểm tra tay"] }
      ],
      onChot(v){ ghi("BT-10", String(v).slice(0, 400)); }
    });
  }

  /* ====================== BT-12 · Ai chịu trách nhiệm khi đầu ra sai? ==============
   * Định vị: view v-tinhhuong, dưới ô BT-10.
   * Cũng là Mức 3 không có đáp án duy nhất: nguyên tắc dùng AI của RIÊNG EM. */
  function bt12(host){
    return D().veTuLuan(host, {
      cauHoi: "Hãy viết MỘT nguyên tắc dùng AI của riêng em — và trong nguyên tắc đó phải "
        + "nói rõ: khi đầu ra của AI sai thì AI, em, hay thầy cô chịu trách nhiệm?",
      goiY: "Ví dụ: 'Em chỉ dùng AI để gợi ý, mọi kết quả phải do em kiểm lại. Nếu em nộp bài mà không kiểm thì CHÍNH EM chịu trách nhiệm...'",
      soTuToiThieu: 25,
      tuChamNgay: true,
      phuongDien: [
        { ma: "nguyen-tac", moTa: "phát biểu được một nguyên tắc rõ ràng, không chung chung", tuKhoa: ["em sẽ", "em chỉ", "em không", "nguyên tắc", "luôn", "phải", "cam kết"] },
        { ma: "trach-nhiem", moTa: "chỉ rõ AI hay người chịu trách nhiệm (và vì sao)", tuKhoa: ["chịu trách nhiệm", "trách nhiệm thuộc", "do em", "do người", "ai chịu"] },
        { ma: "kiem-tra", moTa: "nói mình sẽ kiểm lại đầu ra thế nào", tuKhoa: ["kiểm", "đối chiếu", "xác minh", "tra lại", "đọc lại", "so lại", "soát"] },
        { ma: "khai-bao", moTa: "nói rõ khi nào phải khai báo đã dùng AI", tuKhoa: ["khai báo", "nói rõ", "ghi rõ", "thừa nhận", "báo", "nêu"] },
        { ma: "gioi-han", moTa: "nêu việc KHÔNG giao cho AI", tuKhoa: ["không giao", "không để", "không dùng", "không nhờ"] },
        { ma: "hau-qua", moTa: "nói điều sẽ làm nếu phát hiện đầu ra sai", tuKhoa: ["nếu sai", "khi sai", "sửa lại", "sửa", "báo lại", "xin lỗi", "chịu"] }
      ],
      onChot(v){ ghi("BT-12", String(v).slice(0, 400)); }
    });
  }

  /* Bảng tra — app.js gọi MX_MUC3.mo("<mã bài>", hostEl) rồi giữ api để gọi doiChieu()
   * ĐÚNG LÚC kết quả thật đã có. Không đoán trước kết quả. */
  const BANG = {
    "BT-01": bt01, "BT-03": bt03, "BT-06": bt06, "BT-07": bt07,
    "BT-08": bt08, "BT-10": bt10, "BT-12": bt12
  };

  /* Dựng ô Mức 3 cho một bài. `tl` là hàm TÍNH đáp án/ kết quả thật, do app.js truyền vào
   * (app.js là nơi biết trạng thái bài học: bộ dữ liệu, mô hình, câu trả lời vừa sinh).
   * Giữ `tl` trên api để app.js gọi lại được lúc kết quả thật ĐÃ CÓ — vd BT-03 chỉ biết độ
   * chính xác sau khi huấn luyện xong, mà học sinh chốt dự đoán TRƯỚC đó. */
  function mo(ma, host, tl){
    if(!host || !D()) return null;
    const f = BANG[ma];
    if(!f) return null;
    host.innerHTML = "";          // dựng lại sạch: mỗi lần vào là một lượt mới
    const api = f(host, tl);
    if(!api) return null;
    /* api.tl phải được gắn LẠI ở đây: hàm cham() bên dưới gọi
     * `chamSau(api, api && api.tl)` và chamSau() return sớm nếu tl rỗng.
     * Đã từng bị mất khi bọc doiChieu (06/10) — mất nó thì 4 ô tự chấm
     * (BT-02, BT-05, BT-07, BT-11) không chấm nữa mà KHÔNG báo lỗi nào,
     * vì cú pháp vẫn hợp lệ. Cổng G11f chỉ kiểm "hàm tồn tại", không kiểm
     * "hàm có tác dụng", nên lỗi này phải được giữ bằng chú thích ở đây. */
    api.tl = tl;
    api.ma = ma;

    /* BỌC doiChieu ĐỂ GHI NHẬT KÝ KẾT QUẢ — thêm 06/10.
     * VÌ SAO BỌC Ở ĐÂY thay vì thêm lời gọi ghi vào từng ô: có ba loại ô và HAI đường dẫn
     * dẫn tới đối chiếu — ô số/ô chọn được app.js gọi MX_MUC3.cham() khi kết quả thật đã
     * có, còn ô tự luận TỰ gọi api.doiChieu() qua setTimeout (tuChamNgay). Thêm lời gọi
     * ghi vào từng hàm btXX thì sẽ sót đường tự chấm, và ai thêm ô mới sau này cũng sẽ
     * quên. Bọc ở đúng một chỗ duy nhất mà cả hai đường đều đi qua thì không sót được.
     * `api.doiChieu` được tra cứu qua đối tượng tại THỜI ĐIỂM GỌI (bên trong duDoan.js
     * viết `api.doiChieu()`), nên bản bọc này có hiệu lực với cả lời gọi nội bộ. */
    const goc = api.doiChieu;
    if(typeof goc === "function"){
      api.doiChieu = function(){
        const r = goc.apply(api, arguments);
        if(r){ ghiDoiChieu(ma, r); return r; }

        /* r == null ⟺ HỌC SINH BẤM CHẠY MÀ CHƯA CHỐT DỰ ĐOÁN — thêm 06/10.
         * Đã kiểm bằng đọc mã, không suy đoán: trong js/duDoan.js, `doiChieu` chỉ có
         * MỘT chỗ trả null là `if(chot === null) return null;` (dòng 129, 207, 321 — ba
         * loại ô). Các `return null` khác (dòng 64, 162, 250) là `if(!host)` nằm trong
         * hàm DỰNG ô, không nằm trong doiChieu. Nên null ở đây chỉ có một nghĩa duy nhất
         * và ghi "bỏ qua" là không ghi oan.
         *
         * VÌ SAO PHẢI CÓ CỜ daGhiBoQua: nhánh null KHÔNG set `api.daDoiChieu` (cờ đó nằm
         * sau dòng return null), nên mỗi lần HS bấm chạy lại là doiChieu lại được gọi và
         * lại trả null. Không có cờ thì một HS bấm 5 lần bị đếm 5 lần bỏ qua — số liệu
         * phồng theo số lần bấm, đúng loại lỗi mà cổng này tồn tại để chặn.
         *
         * GIỚI HẠN (nói thật, không che): ô TỰ LUẬN (BT-10, BT-12) không bao giờ ghi
         * "bỏ qua", vì doiChieu của chúng chỉ được gọi từ bên trong onclick của nút
         * "Chốt bài viết" (duDoan.js:313) — HS không bấm nút thì không có lời gọi nào
         * để mà bắt. Muốn đếm được cả ca đó thì phải móc vào nút chạy của bài tập bên
         * dưới, là việc lớn hơn và cần làm riêng. */
        if(!api.daGhiBoQua && !DA_CHOT.has(ma)){
          api.daGhiBoQua = true;
          ghi(ma, "", "boQua", null);
        }
        return r;
      };
    }
    return api;
  }

  /* Chấm lại bằng kết quả thật hiện có — app.js gọi khi dữ liệu đã sẵn sàng.
   * KHÔNG chấm hai lần: chamSau tự bỏ qua nếu ô đã đối chiếu. */
  function cham(api){
    chamSau(api, api && api.tl);
  }

  window.MX_MUC3 = {
    mo, cham, DS: Object.keys(BANG),
    /* app.js gắn hàm ghi nhật ký lớp vào đây (xem giải thích ở đầu tệp).
     * PHẢI xoá DA_CHOT ở đây: app.js gọi ghiLog() mỗi lần ĐĂNG NHẬP, nên đây đúng là
     * ranh giới giữa hai phiên học sinh. Không xoá thì hai em dùng chung một máy (phòng
     * lab 20 HS/40 máy, chuyện thường) sẽ kế thừa nhau: em trước đã chốt BT-03 thì em sau
     * bỏ qua BT-03 cũng không bị ghi "bỏ qua" — số liệu tham gia của lớp phồng lên mà không
     * có dấu hiệu nào để phát hiện.
     * Đã từng có comment khai rằng DA_CHOT được xoá ở đây trong khi hàm KHÔNG xoá (06/10).
     * Sai chỗ đó nguy hiểm hơn là không có comment: người đọc sau sẽ tin và không kiểm lại. */
    ghiLog(fn){ GHI = fn; DA_CHOT = new Set(); }
  };
})();
