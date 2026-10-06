/* SOI AI — MODULE KIẾN THỨC NỀN (phủ 6 YCCĐ cốt lõi lớp 10)
 * Nguồn: Khung nội dung giáo dục AI cho HS phổ thông, ban hành kèm QĐ 2422/QĐ-BGDĐT (18/8/2026).
 * Mã YCCĐ theo quy ước của Khung: [Lớp].[Mã chủ đề].[Số thứ tự]; tiền tố MR = nội dung mở rộng.
 *
 * Phủ:
 *   10.A3.1 (cốt lõi) — kể tên quy định/luật bảo vệ người dùng trong không gian số
 *   10.C2.2 (cốt lõi) — liệt kê ứng dụng AI theo tính năng của hệ thống
 *   10.C2.3 (cốt lõi) — nêu ví dụ sử dụng AI hỗ trợ quá trình học tập
 *   10.C3.1 (cốt lõi) — mô tả yêu cầu để đưa ra prompt phù hợp mục tiêu
 *   10.C3.2 (cốt lõi) — thực hành đặt prompt giải quyết vấn đề gần gũi
 *   10.C3.3 (cốt lõi) — phân biệt AI tạo sinh với AI phân loại/dự đoán
 * Mọi mục đều có nhãn đúng cố định → hệ tự chấm, không cần giáo viên.
 */
window.MX_KT = {

  /* ============ 10.A3.1 — LUẬT BẢO VỆ NGƯỜI DÙNG TRONG KHÔNG GIAN SỐ ============
   * Tất cả số hiệu/ngày đã tra cứu văn bản gốc (vanban.chinhphu.vn, baochinhphu.vn,
   * luatvietnam.vn, vneconomy.vn) — xem ghi chú "nguồn" của từng mục. */
  luat: [
    {
      ten: "Luật An ninh mạng",
      so: "24/2018/QH14",
      ngay: "Quốc hội thông qua 12/6/2018, hiệu lực 01/01/2019",
      baoVe: "Bảo vệ an ninh quốc gia và trật tự an toàn xã hội trên không gian mạng; quy định hành vi bị nghiêm cấm (đăng thông tin sai sự thật, xúc phạm, tấn công mạng...), trách nhiệm của doanh nghiệp cung cấp dịch vụ.",
      lienHe: "Khi em đăng nội dung lên mạng, em chịu trách nhiệm về nội dung đó theo luật này.",
      nguon: "vanban.chinhphu.vn (Luật số 24/2018/QH14). Năm 2025 Quốc hội thông qua Luật An ninh mạng sửa đổi (số 116/2025/QH15) — baochinhphu.vn 10/12/2025."
    },
    {
      ten: "Luật Dữ liệu",
      so: "60/2024/QH15",
      ngay: "Quốc hội thông qua 30/11/2024, hiệu lực 01/7/2025",
      baoVe: "Đạo luật đầu tiên quy định toàn diện về dữ liệu số (5 chương, 46 điều), bao gồm xây dựng, phát triển, bảo vệ, quản trị, xử lí và sử dụng dữ liệu; Cơ sở dữ liệu tổng hợp quốc gia.",
      lienHe: "Dữ liệu em tạo ra khi học (bài làm, nhật ký học tập) cũng là dữ liệu số và được luật điều chỉnh.",
      nguon: "luatvietnam.vn; vnetwork.vn; hcmussh.edu.vn; congan.camau.gov.vn — đồng nhất về số hiệu và ngày hiệu lực."
    },
    {
      ten: "Luật Bảo vệ dữ liệu cá nhân",
      so: "91/2025/QH15",
      ngay: "Quốc hội thông qua 26/6/2025, hiệu lực 01/01/2026",
      baoVe: "Quyền của chủ thể dữ liệu; dữ liệu cá nhân của trẻ em chỉ được xử lí khi có sự đồng ý của cha mẹ hoặc người giám hộ; thông báo sự cố; nghĩa vụ của bên xử lí dữ liệu. Thay thế Nghị định 13/2023/NĐ-CP (hết hiệu lực từ 01/01/2026).",
      lienHe: "Đây là lí do ứng dụng này CHỈ dùng mã ẩn danh, không thu họ tên học sinh.",
      nguon: "vneconomy.vn; truongvietanh.com/chinh-sach-ai; CV 5588/BGDĐT-GDPT trích Luật số 91/2025/QH15 làm căn cứ."
    },
    {
      ten: "Luật Trí tuệ nhân tạo",
      so: "134/2025/QH15",
      ngay: "hiệu lực 01/3/2026",
      baoVe: "Đạo luật đầu tiên về AI của Việt Nam. Nguyên tắc nền tảng: 'Trí tuệ nhân tạo phục vụ con người, không thay thế thẩm quyền và trách nhiệm của con người'. Quy định danh mục hệ thống AI rủi ro cao; hệ thống AI vận hành trước 01/3/2026 có lộ trình tuân thủ.",
      lienHe: "Hệ thống AI trong trường học cũng phải tuân theo luật này — nên mới cần người kiểm định.",
      nguon: "CV 5588/BGDĐT-GDPT (19/8/2026) trích làm căn cứ pháp lí; truongvietanh.com/chinh-sach-ai (Điều 4 khoản 2, Điều 35 khoản 1). MỨC: nguồn thứ cấp — giáo viên nên đối chiếu văn bản gốc trước khi dạy."
    }
  ],

  /* ============ 10.C2.2 — ỨNG DỤNG AI THEO TÍNH NĂNG HỆ THỐNG ============
   * Trường `ma` là ĐỊNH DANH MÁY ĐỌC của từng nhóm, do bài tập xếp nhóm (BT-13) dùng
   * để chấm tất định: học sinh chọn một `ma`, hệ so với `hoTroHocTap[].nhomDung`.
   * Không đổi `ma` sau khi phát hành — nhật ký đã ghi của các lớp trước dùng chuỗi này.
   */
  ungDung: [
    { ma: "phan_loai", nhom: "Phân loại (classification)", moTa: "Gán đối tượng vào một nhóm có sẵn", viDu: "Lọc thư rác; nhận diện khuôn mặt để điểm danh; phân loại ảnh y tế; hệ thống nhận diện mũ bảo hiểm trong ứng dụng này" },
    { ma: "du_doan", nhom: "Dự đoán (prediction)", moTa: "Ước lượng một giá trị hoặc sự kiện tương lai từ dữ liệu quá khứ", viDu: "Dự báo thời tiết; dự đoán điểm số có nguy cơ sa sút; gợi ý sản phẩm; dự báo sản lượng nông nghiệp" },
    { ma: "tao_sinh", nhom: "Tạo sinh (generative)", moTa: "Tạo ra nội dung MỚI chưa từng có: chữ, hình ảnh, âm thanh, mã lệnh", viDu: "Trợ lý ảo viết văn bản; tạo ảnh từ mô tả; tổng hợp giọng nói; sinh mã chương trình" },
    { ma: "nhan_dang_mau", nhom: "Nhận dạng mẫu (pattern recognition)", moTa: "Tìm quy luật lặp lại trong dữ liệu lớn", viDu: "Phát hiện gian lận giao dịch; phân cụm học sinh theo nhu cầu học; nhận dạng chữ viết tay" },
    { ma: "xu_li_ngon_ngu", nhom: "Xử lí ngôn ngữ (language)", moTa: "Hiểu và sinh ngôn ngữ tự nhiên", viDu: "Dịch máy; tóm tắt văn bản; trả lời câu hỏi; chuyển giọng nói thành chữ" },
    { ma: "toi_uu", nhom: "Tối ưu & ra quyết định (optimization)", moTa: "Chọn phương án tốt nhất theo ràng buộc", viDu: "Điều phối đèn giao thông; lập thời khóa biểu; tối ưu lộ trình vận chuyển; phân bổ nguồn lực bệnh viện" }
  ],

  /* ============ 10.C2.3 — VÍ DỤ AI HỖ TRỢ QUÁ TRÌNH HỌC TẬP ============
   * Yêu cầu cần đạt nguyên văn: "Nêu được ví dụ một số trường hợp sử dụng AI hỗ trợ
   * quá trình học tập."
   *
   * VÌ SAO CÓ KHỐI DỮ LIỆU NÀY
   *   Trước 05/10 khối `ungDung` ở trên chỉ là BẢNG ĐỂ ĐỌC: học sinh xem sáu nhóm tính
   *   năng rồi thôi. Quét toàn bộ mã nguồn cho thấy chuỗi 10.C2.3 chỉ xuất hiện trong
   *   data/yccd.js (nơi khai báo danh sách yêu cầu cần đạt) — không có câu hỏi, không có
   *   bài tập nào gắn với nó. Đọc một bảng không phải là "nêu được ví dụ".
   *   Khối dưới đây biến phần đọc thành phần LÀM: mỗi ví dụ là MỘT tình huống học tập
   *   thật, học sinh phải xếp nó vào đúng nhóm tính năng rồi nói rõ đầu vào và đầu ra.
   *
   * CÁCH CHẤM (tất định, không cần giáo viên, không cần mạng)
   *   `nhomDung` là đáp án xếp nhóm. `tuKhoaVao` / `tuKhoaRa` là từ khoá đã định nghĩa
   *   trước để nhận ra học sinh có nói tới đầu vào và đầu ra hay không — GIỐNG cách
   *   chấm prompt ở js/kienthuc.js: đếm từ khoá có mặt, KHÔNG hiểu ngữ nghĩa.
   *   Hồ sơ phải nói rõ giới hạn này: hệ đếm dấu hiệu, giáo viên vẫn là người nhận xét.
   *
   * ĐIỂM MẤU CHỐT (giữ đúng tinh thần BT-13)
   *   Mỗi tình huống dưới đây gắn với TÍNH NĂNG của hệ thống, không gắn với tên thương
   *   mại. Tên thương mại đổi mỗi năm; tính năng thì không. Cùng một tình huống có thể
   *   chạm nhiều nhóm — trường `cungLienQuan` ghi các nhóm được chấp nhận thêm, và học
   *   sinh phải nói được vì sao mình chọn nhóm đó.
   */
  hoTroHocTap: [
    {
      id: "ht-01",
      tinhHuong: "Em chụp ảnh bài giải viết tay của mình, hệ đọc chữ trong ảnh rồi gán bài đó vào một trong ba nhóm có sẵn: \"đã hiểu\", \"cần xem lại\", \"chưa đạt\".",
      nhomDung: "phan_loai",
      dauVaoMau: "Ảnh chụp bài giải viết tay của học sinh (cùng một tập nhãn cố định 3 nhóm).",
      dauRaMau: "Một nhãn trong ba nhãn có sẵn — ví dụ \"cần xem lại\". Không sinh ra nội dung mới nào.",
      tuKhoaVao: ["ảnh", "bài giải", "chụp", "viết tay", "chữ", "bài làm"],
      tuKhoaRa: ["nhãn", "nhóm", "một trong ba", "xếp", "gán", "đã hiểu", "cần xem lại", "chưa đạt"],
      viSao: "Đối tượng được gán vào một nhóm CÓ SẴN, nên đây là phân loại. Dấu hiệu nhận biết: nếu hệ chỉ chọn đáp án trong danh sách đã có thì là phân loại.",
      canhBao: "Hệ đọc chữ viết tay có thể sai với chữ xấu hoặc ảnh mờ. Em cần biết ngưỡng này tồn tại trước khi tin kết quả."
    },
    {
      id: "ht-02",
      tinhHuong: "Hệ đọc bảng điểm giữa kì của em ở các môn, so với điểm các tuần trước, rồi cảnh báo môn nào có nguy cơ sa sút trong tháng tới.",
      nhomDung: "du_doan",
      dauVaoMau: "Bảng điểm quá khứ của học sinh theo thời gian (dữ liệu đã có, không phải dữ liệu tương lai).",
      dauRaMau: "Một tỉ lệ hoặc mức nguy cơ cho từng môn — ví dụ \"môn Toán: nguy cơ sa sút 62%\".",
      tuKhoaVao: ["điểm", "bảng điểm", "các tuần", "quá khứ", "giữa kì", "kết quả cũ"],
      tuKhoaRa: ["nguy cơ", "tỉ lệ", "dự báo", "phần trăm", "xác suất", "mức độ", "cảnh báo"],
      viSao: "Đầu ra là một ước lượng về chuyện CHƯA xảy ra, tính từ dữ liệu đã xảy ra, nên đây là dự đoán. Dấu hiệu nhận biết: có chữ \"sẽ\", \"nguy cơ\", \"dự báo\" đi kèm một con số.",
      canhBao: "Dự đoán không phải bản án. Một con số nguy cơ cao không có nghĩa là em chắc chắn sẽ sa sút — nó chỉ nói dữ liệu hiện có giống những trường hợp trước đây."
    },
    {
      id: "ht-03",
      tinhHuong: "Em nhờ trợ lý AI soạn cho mình 10 câu luyện tập MỚI về chương đang học, kèm lời giải, để tự làm thêm ở nhà.",
      nhomDung: "tao_sinh",
      dauVaoMau: "Câu mô tả yêu cầu của học sinh (chương nào, dạng bài nào, mức độ khó) và tài liệu em dán vào.",
      dauRaMau: "Văn bản hoàn toàn mới: 10 câu hỏi và lời giải chưa từng tồn tại trước đó.",
      tuKhoaVao: ["yêu cầu", "mô tả", "chương", "dạng bài", "tài liệu", "dán", "nhờ"],
      tuKhoaRa: ["câu hỏi mới", "đề mới", "văn bản", "lời giải", "nội dung mới", "soạn", "sinh ra"],
      viSao: "Đầu ra là nội dung MỚI chưa từng có, không chọn từ danh sách có sẵn, nên đây là tạo sinh. Dấu hiệu nhận biết: bỏ câu trả lời đi thì hệ phải sinh lại từ đầu, không tra cứu được ở đâu.",
      canhBao: "Đây là nhóm khó kiểm chứng nhất: đề và lời giải có thể trôi chảy nhưng sai kiến thức. Phải đối chiếu với sách giáo khoa trước khi học theo."
    },
    {
      id: "ht-04",
      tinhHuong: "Hệ đọc nhật ký làm bài của cả lớp trong học kì, rồi chỉ ra rằng nhóm học sinh hay sai cùng một dạng câu hỏi về dữ liệu lệch.",
      nhomDung: "nhan_dang_mau",
      dauVaoMau: "Nhật ký làm bài của NHIỀU học sinh, nhiều lượt, tích lại theo thời gian (dữ liệu lớn).",
      dauRaMau: "Một quy luật lặp lại: nhóm học sinh nào hay sai dạng câu nào — không phải điểm của một em.",
      tuKhoaVao: ["nhật ký", "nhiều", "cả lớp", "nhiều lượt", "dữ liệu lớn", "lịch sử làm bài"],
      tuKhoaRa: ["quy luật", "nhóm học sinh", "lặp lại", "xu hướng", "phân cụm", "hay sai"],
      viSao: "Việc cần làm là TÌM QUY LUẬT LẶP LẠI trong dữ liệu lớn, chứ không phải gán nhãn cho một bài hay đoán một con số, nên đây là nhận dạng mẫu.",
      canhBao: "Quy luật tìm trên dữ liệu của lớp em có thể không đúng cho lớp khác. Mẫu tìm được là giả thuyết để kiểm, không phải kết luận."
    },
    {
      id: "ht-05",
      tinhHuong: "Em dán một bài đọc tiếng Anh vào trợ lý AI, nhờ dịch sang tiếng Việt và tóm tắt còn 5 gạch đầu dòng để kịp đọc trước giờ học.",
      nhomDung: "xu_li_ngon_ngu",
      dauVaoMau: "Văn bản tiếng Anh em dán vào (ngôn ngữ tự nhiên, có thể dài).",
      dauRaMau: "Bản dịch tiếng Việt và bản tóm tắt 5 gạch đầu dòng.",
      tuKhoaVao: ["bài đọc", "tiếng anh", "văn bản", "dán", "đoạn văn"],
      tuKhoaRa: ["dịch", "tiếng việt", "tóm tắt", "gạch đầu dòng", "bản dịch"],
      viSao: "Việc cần làm là HIỂU và SINH ngôn ngữ tự nhiên (dịch, tóm tắt), nên đây là xử lí ngôn ngữ. Dấu hiệu nhận biết: đầu vào và đầu ra đều là chữ của con người.",
      canhBao: "Bản dịch có thể trôi chảy nhưng lệch nghĩa ở câu khó. Với bài đọc quan trọng, em nên đối chiếu lại vài câu then chốt."
    },
    {
      id: "ht-06",
      tinhHuong: "Hệ nhận thời gian trống của em trong tuần và hạn nộp của từng bài, rồi gợi ý một thời khóa biểu tự học, xếp việc gấp lên trước.",
      nhomDung: "toi_uu",
      dauVaoMau: "Các ràng buộc: thời gian trống từng ngày, hạn nộp từng bài, thời lượng mỗi việc cần.",
      dauRaMau: "Một phương án lịch cụ thể cho cả tuần — chọn trong vô số cách xếp, theo tiêu chí đã đặt.",
      tuKhoaVao: ["thời gian trống", "hạn nộp", "ràng buộc", "lịch", "thời lượng", "mấy giờ"],
      tuKhoaRa: ["thời khóa biểu", "phương án", "xếp lịch", "tối ưu", "gợi ý lịch", "cách sắp xếp"],
      viSao: "Việc cần làm là CHỌN PHƯƠNG ÁN TỐT NHẤT trong nhiều cách xếp, dưới các ràng buộc, nên đây là tối ưu và ra quyết định.",
      canhBao: "Lịch do hệ xếp tối ưu theo tiêu chí của hệ, không theo sức học của em. Em vẫn là người quyết định có theo hay không."
    }
  ],

  /* ============ 10.C3.3 — AI TẠO SINH vs AI PHÂN LOẠI/DỰ ĐOÁN ============ */
  soSanh: {
    cot: ["Tiêu chí", "AI PHÂN LOẠI / DỰ ĐOÁN", "AI TẠO SINH"],
    hang: [
      ["Nhiệm vụ", "Chọn đáp án từ tập nhãn CÓ SẴN", "Tạo nội dung MỚI chưa tồn tại"],
      ["Đầu ra", "Một nhãn hoặc một con số (ví dụ: 'có mũ' / 'không mũ', 87%)", "Văn bản, hình ảnh, âm thanh, mã lệnh"],
      ["Kiểm tra đúng/sai", "DỄ: so với nhãn đúng đã biết", "KHÓ: có thể trôi chảy nhưng sai sự thật (bịa số liệu, bịa nguồn)"],
      ["Lỗi điển hình", "Thiên kiến do dữ liệu huấn luyện lệch; sai với nhóm ít dữ liệu", "Bịa đặt — máy nói nghe như thật nhưng không có thật (thuật ngữ: hallucination), đạo văn, giọng điệu tự tin nhưng vô căn cứ"],
      ["Ví dụ trong ứng dụng này", "Xưởng huấn luyện AI (Tầng 1)", "Đấu trường bắt lỗi AI (Tầng 2)"],
      ["Cách con người kiểm soát", "Kiểm tra dữ liệu huấn luyện + đo độ chính xác theo từng nhóm", "Đối chiếu với nguồn thật + không dùng kết quả khi chưa kiểm chứng"]
    ],
    ketLuan: "AI tạo sinh khó kiểm chứng hơn vì đầu ra không có nhãn đúng sẵn. Vì vậy người dùng phải tự đối chiếu nguồn — đó chính là kĩ năng 'Đấu trường bắt lỗi AI' rèn luyện."
  },

  /* ============ 10.C3.1 — TIÊU CHÍ CỦA MỘT PROMPT TỐT (chấm tự động) ============ */
  promptTieuChi: [
    { id: "muc_tieu", ten: "Nêu rõ MỤC TIÊU / việc cần làm", viDu: "'Hãy giải thích...', 'Hãy lập bảng...', 'Hãy viết đoạn văn 100 chữ...'" },
    { id: "boi_canh", ten: "Cho BỐI CẢNH và đối tượng", viDu: "'cho học sinh lớp 10', 'ở vùng nông thôn', 'để trình bày trước lớp'" },
    { id: "du_lieu", ten: "Cung cấp DỮ LIỆU / tư liệu cần dùng", viDu: "dán đoạn văn bản, số liệu, danh sách cần xử lí" },
    { id: "dinh_dang", ten: "Chỉ rõ ĐỊNH DẠNG đầu ra", viDu: "'trả lời bằng bảng 3 cột', 'liệt kê 5 gạch đầu dòng', 'tối đa 150 chữ'" },
    { id: "rang_buoc", ten: "Nêu RÀNG BUỘC và điều phải tránh", viDu: "'không bịa số liệu', 'chỉ dùng thông tin trong đoạn văn', 'nêu rõ chỗ không chắc chắn'" },
    { id: "kiem_chung", ten: "Yêu cầu KIỂM CHỨNG / nêu nguồn", viDu: "'cho biết mỗi thông tin lấy từ đâu', 'đánh dấu chỗ nào em không chắc'" }
  ],

  /* ============ 10.C3.2 — BÀI THỰC HÀNH ĐẶT PROMPT (chấm theo rubric, offline) ============ */
  promptDe: [
    {
      id: "p-01",
      ten: "Yêu cầu AI giải thích một khái niệm Tin học",
      tinhHuong: "Em muốn nhờ trợ lý AI giải thích khái niệm 'thiên kiến dữ liệu' (data bias) để hiểu trước khi vào bài học, sao cho một bạn lớp 10 chưa biết gì về AI cũng hiểu được.",
      goiY: "Hãy viết prompt có đủ việc cần làm, đối tượng đọc, độ dài, định dạng, và điều phải tránh.",
      /* tiêu chí BẮT BUỘC phải có mặt trong prompt của HS (từ khoá chấp nhận được) */
      batBuoc: ["muc_tieu", "boi_canh", "dinh_dang"],
      tuKhoa: {
        muc_tieu: ["giải thích", "nêu", "trình bày", "cho biết", "định nghĩa", "mô tả"],
        boi_canh: ["lớp 10", "học sinh", "chưa biết", "mới học", "người mới", "bạn em", "tuổi"],
        dinh_dang: ["gạch đầu dòng", "bảng", "chữ", "từ", "đoạn văn", "ví dụ", "ngắn", "dòng", "mục"],
        du_lieu: ["dữ liệu", "ví dụ sau", "đoạn văn", "thông tin sau", "cho sẵn"],
        rang_buoc: ["không", "tránh", "đừng", "chỉ", "không được", "hạn chế"],
        kiem_chung: ["nguồn", "không chắc", "kiểm tra", "trích dẫn", "chắc chắn", "nếu không biết"]
      },
      giaiThich: "Prompt tối thiểu cần: MỤC TIÊU (giải thích khái niệm gì) + BỐI CẢNH (cho ai, trình độ nào) + ĐỊNH DẠNG (dài bao nhiêu, dạng gì). Thiếu bối cảnh, AI sẽ trả lời quá hàn lâm; thiếu định dạng, em nhận về một bài dài không dùng được."
    },
    {
      id: "p-02",
      ten: "Yêu cầu AI xử lí dữ liệu lớp học (không bịa)",
      tinhHuong: "Lớp em có bảng điểm 40 bạn (điểm giữa kì môn Tin). Em muốn AI gợi ý bạn nào cần được hỗ trợ thêm và lí do, nhưng KHÔNG được bịa số và không được tiết lộ thông tin cá nhân.",
      goiY: "Hãy viết prompt đảm bảo có dữ liệu thật, có ràng buộc chống bịa đặt, và bảo vệ dữ liệu cá nhân.",
      batBuoc: ["muc_tieu", "du_lieu", "rang_buoc"],
      tuKhoa: {
        muc_tieu: ["gợi ý", "xác định", "tìm", "liệt kê", "chỉ ra", "phân tích", "đề xuất"],
        boi_canh: ["lớp", "40", "giữa kì", "môn Tin", "học sinh"],
        dinh_dang: ["bảng", "danh sách", "gạch", "lí do", "cột", "dòng"],
        du_lieu: ["bảng điểm", "điểm", "dữ liệu sau", "số liệu", "cho sẵn", "đính kèm", "dán"],
        rang_buoc: ["không bịa", "không được", "không", "tránh", "ẩn danh", "mã", "không nêu tên", "chỉ dùng", "dựa trên"],
        kiem_chung: ["giải thích", "căn cứ", "dựa vào", "nguồn", "nếu không đủ"]
      },
      giaiThich: "Đây là bài tập gắn với Luật Bảo vệ dữ liệu cá nhân (91/2025/QH15). Khi đưa dữ liệu học sinh cho một công cụ AI, em phải ẨN DANH trước (dùng mã thay vì họ tên) và phải ràng buộc để AI không suy diễn ngoài dữ liệu. Prompt tốt = prompt có ràng buộc."
    },
    {
      id: "p-03",
      ten: "Yêu cầu AI giúp kiểm tra một thông tin đáng ngờ",
      tinhHuong: "Em đọc được trên mạng câu này — '97,3% học sinh Việt Nam từng bị đánh cắp tài khoản trong năm 2025'. Em muốn nhờ AI giúp kiểm tra thông tin này có đáng tin không.",
      goiY: "Hãy viết prompt khiến AI phải nêu rõ mức độ chắc chắn và cách em tự kiểm chứng, thay vì khẳng định bừa.",
      batBuoc: ["muc_tieu", "kiem_chung", "rang_buoc"],
      tuKhoa: {
        muc_tieu: ["kiểm tra", "xác minh", "đánh giá", "cho biết", "xem", "có đúng", "đáng tin"],
        boi_canh: ["97,3", "học sinh", "Việt Nam", "2025", "trên mạng"],
        dinh_dang: ["bảng", "các bước", "liệt kê", "kết luận", "ngắn"],
        du_lieu: ["thông tin sau", "câu sau", "nguyên văn", "cho sẵn"],
        rang_buoc: ["không", "tránh", "đừng", "nếu không biết", "không chắc", "chỉ"],
        kiem_chung: ["nguồn", "ở đâu", "tự kiểm", "kiểm chứng", "trang chính thức", "mức độ chắc chắn", "nói rõ"]
      },
      giaiThich: "Đây chính là kĩ năng kiểm chứng thông tin mà Khung QĐ 2422 đặt làm mục tiêu ('rèn luyện tư duy phản biện, khả năng kiểm chứng thông tin'). Một prompt tốt trong trường hợp này phải ÉP AI nói rõ mức độ chắc chắn và chỉ cho em cách tự tra cứu, thay vì để AI tự khẳng định."
    }
  ],

  /* ============ QUIZ cho các mục kiến thức trên (oracle tự chấm) ============ */
  quiz: [
    {
      id: "kt-01", mach: "A", unesco: "A3", yccd: "10.A3.1",
      cauHoi: "Văn bản nào sau đây quy định rằng dữ liệu cá nhân của TRẺ EM chỉ được xử lí khi có sự đồng ý của cha mẹ hoặc người giám hộ?",
      luaChon: [
        { id: "a", text: "Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 (hiệu lực 01/01/2026)" },
        { id: "b", text: "Luật Giáo dục số 43/2019/QH14" },
        { id: "c", text: "Bộ luật Dân sự số 91/2015/QH13" },
        { id: "d", text: "Nghị định về xử phạt hành chính trong lĩnh vực giáo dục" }
      ],
      dapAn: "a",
      giaiThich: "Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (Quốc hội thông qua 26/6/2025, hiệu lực 01/01/2026) quy định về quyền của chủ thể dữ liệu và việc xử lí dữ liệu cá nhân của trẻ em. Luật này thay thế Nghị định 13/2023/NĐ-CP. Đây là lí do các ứng dụng giáo dục phải dùng mã ẩn danh và có ý kiến phụ huynh."
    },
    {
      id: "kt-02", mach: "A", unesco: "A3", yccd: "10.A3.1",
      cauHoi: "Luật Trí tuệ nhân tạo của Việt Nam (số 134/2025/QH15) khẳng định nguyên tắc nền tảng nào?",
      luaChon: [
        { id: "a", text: "AI phải thay thế con người trong mọi quyết định để đảm bảo khách quan." },
        { id: "b", text: "Trí tuệ nhân tạo phục vụ con người, không thay thế thẩm quyền và trách nhiệm của con người." },
        { id: "c", text: "Mọi hệ thống AI đều phải do Nhà nước trực tiếp vận hành." },
        { id: "d", text: "Chỉ doanh nghiệp lớn mới được phát triển AI." }
      ],
      dapAn: "b",
      giaiThich: "Nguyên tắc 'AI phục vụ con người, không thay thế thẩm quyền và trách nhiệm của con người' là nền tảng của Luật Trí tuệ nhân tạo 134/2025/QH15 (hiệu lực 01/3/2026), và cũng là tinh thần mạch A 'Tư duy lấy con người làm trung tâm' của Khung QĐ 2422. Trong đánh giá học sinh, điều này nghĩa là AI có thể gợi ý, nhưng giáo viên là người chịu trách nhiệm về kết quả."
    },
    {
      id: "kt-03", mach: "C", unesco: "C2", yccd: "10.C2.2",
      cauHoi: "Một hệ thống tự động đọc ảnh chụp bài làm của học sinh rồi xếp vào 3 nhóm 'đạt / cần cố gắng / chưa đạt' thuộc loại tính năng AI nào?",
      luaChon: [
        { id: "a", text: "AI tạo sinh (generative)" },
        { id: "b", text: "AI phân loại (classification)" },
        { id: "c", text: "AI tối ưu lộ trình (optimization)" },
        { id: "d", text: "AI nhận dạng giọng nói (speech)" }
      ],
      dapAn: "b",
      giaiThich: "Hệ thống gán đối tượng (bài làm) vào một nhóm nhãn CÓ SẴN (đạt / cần cố gắng / chưa đạt) — đó là bài toán phân loại. Không có nội dung mới nào được tạo ra nên không phải tạo sinh. Phân loại có nhãn đúng để đối chiếu nên kiểm tra đúng/sai DỄ hơn tạo sinh."
    },
    {
      id: "kt-04", mach: "C", unesco: "C1", yccd: "10.C3.3",
      cauHoi: "Vì sao nội dung do AI TẠO SINH khó kiểm chứng hơn kết quả của AI PHÂN LOẠI?",
      luaChon: [
        { id: "a", text: "Vì AI tạo sinh chạy chậm hơn nên khó theo dõi." },
        { id: "b", text: "Vì AI tạo sinh tạo ra nội dung mới không có nhãn đúng sẵn để đối chiếu, nên có thể trôi chảy mà vẫn sai sự thật." },
        { id: "c", text: "Vì AI phân loại không bao giờ sai." },
        { id: "d", text: "Vì AI tạo sinh chỉ dùng được bằng tiếng Anh." }
      ],
      dapAn: "b",
      giaiThich: "AI phân loại có tập nhãn cố định nên đo được độ chính xác bằng cách so với nhãn đúng. AI tạo sinh tạo nội dung mới — không có sẵn 'đáp án đúng' để so, nên có thể viết rất tự tin mà vẫn bịa số liệu hoặc bịa nguồn. Đó là lí do người dùng phải tự đối chiếu nguồn thật."
    },
    {
      id: "kt-05", mach: "C", unesco: "C2", yccd: "10.C3.1",
      cauHoi: "Prompt nào dưới đây đáp ứng ĐẦY ĐỦ nhất các yêu cầu về mục tiêu, bối cảnh, định dạng và ràng buộc?",
      luaChon: [
        { id: "a", text: "'Nói về AI đi.'" },
        { id: "b", text: "'Giải thích trí tuệ nhân tạo.'" },
        { id: "c", text: "'Hãy giải thích khái niệm thiên kiến dữ liệu cho học sinh lớp 10 chưa học về AI, trong tối đa 150 chữ, gồm 1 ví dụ thực tế ở Việt Nam; không dùng thuật ngữ chuyên ngành mà không giải thích.'" },
        { id: "d", text: "'Thiên kiến dữ liệu là gì? Trả lời nhanh.'" }
      ],
      dapAn: "c",
      giaiThich: "Prompt (c) có đủ: MỤC TIÊU (giải thích khái niệm thiên kiến dữ liệu) + BỐI CẢNH (học sinh lớp 10 chưa học AI) + ĐỊNH DẠNG (tối đa 150 chữ, 1 ví dụ Việt Nam) + RÀNG BUỘC (không dùng thuật ngữ mà không giải thích). Prompt (a) và (b) thiếu mọi thứ; (d) chỉ có mục tiêu."
    },
    {
      id: "kt-06", mach: "C", unesco: "C2", yccd: "10.C3.2",
      cauHoi: "Khi nhờ AI phân tích bảng điểm của lớp để tìm học sinh cần hỗ trợ, việc nào sau đây là CẦN LÀM TRƯỚC khi dán dữ liệu vào công cụ AI?",
      luaChon: [
        { id: "a", text: "Dán nguyên bảng có họ tên để AI phân tích chính xác hơn." },
        { id: "b", text: "Ẩn danh hoá: thay họ tên bằng mã (A001, A002...), chỉ giữ lại điểm số." },
        { id: "c", text: "Xoá hết điểm số vì đó là thông tin nhạy cảm." },
        { id: "d", text: "Chụp ảnh bảng điểm gốc cho rõ." }
      ],
      dapAn: "b",
      giaiThich: "Ẩn danh hoá là bước bắt buộc, vì dữ liệu cá nhân của trẻ em được Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 bảo vệ, và CV 5588/BGDĐT-GDPT yêu cầu không tạo rủi ro dữ liệu cho học sinh. Điểm số vẫn cần giữ vì đó là dữ liệu để phân tích; họ tên thì không cần cho việc này."
    }
  ]
};
