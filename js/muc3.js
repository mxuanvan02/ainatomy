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
  function ghi(ma, giaTri){
    if(!GHI) return;
    try { GHI(ma, giaTri); } catch(e) { /* log lỗi không được làm hỏng bài học */ }
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
    if(api) api.tl = tl;
    return api;
  }

  /* Chấm lại bằng kết quả thật hiện có — app.js gọi khi dữ liệu đã sẵn sàng.
   * KHÔNG chấm hai lần: chamSau tự bỏ qua nếu ô đã đối chiếu. */
  function cham(api){
    chamSau(api, api && api.tl);
  }

  window.MX_MUC3 = {
    mo, cham, DS: Object.keys(BANG),
    /* app.js gắn hàm ghi nhật ký lớp vào đây (xem giải thích ở đầu tệp). */
    ghiLog(fn){ GHI = fn; }
  };
})();
