/* AInatomy — MODULE KIẾN THỨC NỀN (phủ 6 YCCĐ cốt lõi lớp 10)
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
 *
 * CẤU TRÚC DỮ LIỆU THEO KHỐI LỚP (cập nhật 26/10):
 *   window.MX_KT.lop[soLop].baiHoc[maBai] = {
 *     ten: tên bài học,
 *     yccd: mã YCCĐ,
 *     kienThucNen: nội dung kiến thức nền (HTML),
 *     baiTap: [{ten, de, dapAn, giaiThich}],
 *     huongDan: hướng dẫn làm bài,
 *     baiTapBoSung: [{ten, de, dapAn, giaiThich}]
 *   }
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
      lienHe: "Khi đăng nội dung lên mạng, người đăng chịu trách nhiệm về nội dung đó theo luật này.",
      nguon: "vanban.chinhphu.vn (Luật số 24/2018/QH14). Năm 2025 Quốc hội thông qua Luật An ninh mạng sửa đổi (số 116/2025/QH15) — baochinhphu.vn 10/12/2025."
    },
    {
      ten: "Luật Dữ liệu",
      so: "60/2024/QH15",
      ngay: "Quốc hội thông qua 30/11/2024, hiệu lực 01/7/2025",
      baoVe: "Đạo luật đầu tiên quy định toàn diện về dữ liệu số (5 chương, 46 điều), bao gồm xây dựng, phát triển, bảo vệ, quản trị, xử lí và sử dụng dữ liệu; Cơ sở dữ liệu tổng hợp quốc gia.",
      lienHe: "Dữ liệu tạo ra khi học (bài làm, nhật ký học tập) cũng là dữ liệu số và được luật điều chỉnh.",
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
      tinhHuong: "Chụp ảnh bài giải viết tay, hệ đọc chữ trong ảnh rồi gán bài đó vào một trong ba nhóm có sẵn: \"đã hiểu\", \"cần xem lại\", \"chưa đạt\".",
      nhomDung: "phan_loai",
      dauVaoMau: "Ảnh chụp bài giải viết tay của học sinh (cùng một tập nhãn cố định 3 nhóm).",
      dauRaMau: "Một nhãn trong ba nhãn có sẵn — ví dụ \"cần xem lại\". Không sinh ra nội dung mới nào.",
      tuKhoaVao: ["ảnh", "bài giải", "chụp", "viết tay", "chữ", "bài làm"],
      tuKhoaRa: ["nhãn", "nhóm", "một trong ba", "xếp", "gán", "đã hiểu", "cần xem lại", "chưa đạt"],
      viSao: "Đối tượng được gán vào một nhóm CÓ SẴN, nên đây là phân loại. Dấu hiệu nhận biết: nếu hệ chỉ chọn đáp án trong danh sách đã có thì là phân loại.",
      canhBao: "Hệ đọc chữ viết tay có thể sai với chữ xấu hoặc ảnh mờ. Ngưỡng sai này cần được biết trước khi tin kết quả."
    },
    {
      id: "ht-02",
      tinhHuong: "Hệ đọc bảng điểm giữa kì ở các môn, so với điểm các tuần trước, rồi cảnh báo môn nào có nguy cơ sa sút trong tháng tới.",
      nhomDung: "du_doan",
      dauVaoMau: "Bảng điểm quá khứ của học sinh theo thời gian (dữ liệu đã có, không phải dữ liệu tương lai).",
      dauRaMau: "Một tỉ lệ hoặc mức nguy cơ cho từng môn — ví dụ \"môn Toán: nguy cơ sa sút 62%\".",
      tuKhoaVao: ["điểm", "bảng điểm", "các tuần", "quá khứ", "giữa kì", "kết quả cũ"],
      tuKhoaRa: ["nguy cơ", "tỉ lệ", "dự báo", "phần trăm", "xác suất", "mức độ", "cảnh báo"],
      viSao: "Đầu ra là một ước lượng về chuyện CHƯA xảy ra, tính từ dữ liệu đã xảy ra, nên đây là dự đoán. Dấu hiệu nhận biết: có chữ \"sẽ\", \"nguy cơ\", \"dự báo\" đi kèm một con số.",
      canhBao: "Dự đoán không phải bản án. Một con số nguy cơ cao không có nghĩa chắc chắn sẽ sa sút, nó chỉ nói dữ liệu hiện có giống những trường hợp trước đây."
    },
    {
      id: "ht-03",
      tinhHuong: "Nhờ trợ lý AI soạn 10 câu luyện tập MỚI về chương đang học, kèm lời giải, để tự làm thêm ở nhà.",
      nhomDung: "tao_sinh",
      dauVaoMau: "Câu mô tả yêu cầu của học sinh (chương nào, dạng bài nào, mức độ khó) và tài liệu được dán vào.",
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
      dauRaMau: "Một quy luật lặp lại: nhóm học sinh nào hay sai dạng câu nào — không phải điểm của một học sinh.",
      tuKhoaVao: ["nhật ký", "nhiều", "cả lớp", "nhiều lượt", "dữ liệu lớn", "lịch sử làm bài"],
      tuKhoaRa: ["quy luật", "nhóm học sinh", "lặp lại", "xu hướng", "phân cụm", "hay sai"],
      viSao: "Việc cần làm là TÌM QUY LUẬT LẶP LẠI trong dữ liệu lớn, chứ không phải gán nhãn cho một bài hay đoán một con số, nên đây là nhận dạng mẫu.",
      canhBao: "Quy luật tìm trên dữ liệu của lớp mình có thể không đúng cho lớp khác. Mẫu tìm được là giả thuyết để kiểm, không phải kết luận."
    },
    {
      id: "ht-05",
      tinhHuong: "Dán một bài đọc tiếng Anh vào trợ lý AI, nhờ dịch sang tiếng Việt và tóm tắt còn 5 gạch đầu dòng để kịp đọc trước giờ học.",
      nhomDung: "xu_li_ngon_ngu",
      dauVaoMau: "Văn bản tiếng Anh được dán vào (ngôn ngữ tự nhiên, có thể dài).",
      dauRaMau: "Bản dịch tiếng Việt và bản tóm tắt 5 gạch đầu dòng.",
      tuKhoaVao: ["bài đọc", "tiếng anh", "văn bản", "dán", "đoạn văn"],
      tuKhoaRa: ["dịch", "tiếng việt", "tóm tắt", "gạch đầu dòng", "bản dịch"],
      viSao: "Việc cần làm là HIỂU và SINH ngôn ngữ tự nhiên (dịch, tóm tắt), nên đây là xử lí ngôn ngữ. Dấu hiệu nhận biết: đầu vào và đầu ra đều là chữ của con người.",
      canhBao: "Bản dịch có thể trôi chảy nhưng lệch nghĩa ở câu khó. Với bài đọc quan trọng, cần đối chiếu lại vài câu then chốt."
    },
    {
      id: "ht-06",
      tinhHuong: "Hệ nhận thời gian trống trong tuần và hạn nộp của từng bài, rồi gợi ý một thời khóa biểu tự học, xếp việc gấp lên trước.",
      nhomDung: "toi_uu",
      dauVaoMau: "Các ràng buộc: thời gian trống từng ngày, hạn nộp từng bài, thời lượng mỗi việc cần.",
      dauRaMau: "Một phương án lịch cụ thể cho cả tuần — chọn trong vô số cách xếp, theo tiêu chí đã đặt.",
      tuKhoaVao: ["thời gian trống", "hạn nộp", "ràng buộc", "lịch", "thời lượng", "mấy giờ"],
      tuKhoaRa: ["thời khóa biểu", "phương án", "xếp lịch", "tối ưu", "gợi ý lịch", "cách sắp xếp"],
      viSao: "Việc cần làm là CHỌN PHƯƠNG ÁN TỐT NHẤT trong nhiều cách xếp, dưới các ràng buộc, nên đây là tối ưu và ra quyết định.",
      canhBao: "Lịch do hệ xếp tối ưu theo tiêu chí của hệ, không theo sức học của từng người. Người học vẫn là người quyết định có theo hay không."
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
    { id: "kiem_chung", ten: "Yêu cầu KIỂM CHỨNG / nêu nguồn", viDu: "'cho biết mỗi thông tin lấy từ đâu', 'đánh dấu chỗ nào chưa chắc'" }
  ],

  /* ============ 10.C3.2 — BÀI THỰC HÀNH ĐẶT PROMPT (chấm theo rubric, offline) ============ */
  promptDe: [
    {
      id: "p-01",
      ten: "Yêu cầu AI giải thích một khái niệm Tin học",
      tinhHuong: "Cần nhờ trợ lý AI giải thích khái niệm 'thiên kiến dữ liệu' (data bias) để hiểu trước khi vào bài học, sao cho một bạn lớp 10 chưa biết gì về AI cũng hiểu được.",
      goiY: "Hãy viết prompt có đủ việc cần làm, đối tượng đọc, độ dài, định dạng, và điều phải tránh.",
      /* tiêu chí BẮT BUỘC phải có mặt trong prompt của HS (từ khoá chấp nhận được) */
      batBuoc: ["muc_tieu", "boi_canh", "dinh_dang"],
      tuKhoa: {
        muc_tieu: ["giải thích", "nêu", "trình bày", "cho biết", "định nghĩa", "mô tả"],
        boi_canh: ["lớp 10", "học sinh", "chưa biết", "mới học", "người mới", "bạn cùng lớp", "tuổi"],
        dinh_dang: ["gạch đầu dòng", "bảng", "chữ", "từ", "đoạn văn", "ví dụ", "ngắn", "dòng", "mục"],
        du_lieu: ["dữ liệu", "ví dụ sau", "đoạn văn", "thông tin sau", "cho sẵn"],
        rang_buoc: ["không", "tránh", "đừng", "chỉ", "không được", "hạn chế"],
        kiem_chung: ["nguồn", "không chắc", "kiểm tra", "trích dẫn", "chắc chắn", "nếu không biết"]
      },
      giaiThich: "Prompt tối thiểu cần: MỤC TIÊU (giải thích khái niệm gì) + BỐI CẢNH (cho ai, trình độ nào) + ĐỊNH DẠNG (dài bao nhiêu, dạng gì). Thiếu bối cảnh, AI sẽ trả lời quá hàn lâm; thiếu định dạng, kết quả nhận về là một bài dài không dùng được."
    },
    {
      id: "p-02",
      ten: "Yêu cầu AI xử lí dữ liệu lớp học (không bịa)",
      tinhHuong: "Lớp có bảng điểm 40 bạn (điểm giữa kì môn Tin). Cần AI gợi ý bạn nào cần được hỗ trợ thêm và lí do, nhưng KHÔNG được bịa số và không được tiết lộ thông tin cá nhân.",
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
      giaiThich: "Đây là bài tập gắn với Luật Bảo vệ dữ liệu cá nhân (91/2025/QH15). Khi đưa dữ liệu học sinh cho một công cụ AI, phải ẨN DANH trước (dùng mã thay vì họ tên) và phải ràng buộc để AI không suy diễn ngoài dữ liệu. Prompt tốt = prompt có ràng buộc."
    },
    {
      id: "p-03",
      ten: "Yêu cầu AI giúp kiểm tra một thông tin đáng ngờ",
      tinhHuong: "Đọc được trên mạng câu này, '97,3% học sinh Việt Nam từng bị đánh cắp tài khoản trong năm 2025'. Cần nhờ AI kiểm tra thông tin này có đáng tin không.",
      goiY: "Hãy viết prompt khiến AI phải nêu rõ mức độ chắc chắn và cách tự kiểm chứng, thay vì khẳng định bừa.",
      batBuoc: ["muc_tieu", "kiem_chung", "rang_buoc"],
      tuKhoa: {
        muc_tieu: ["kiểm tra", "xác minh", "đánh giá", "cho biết", "xem", "có đúng", "đáng tin"],
        boi_canh: ["97,3", "học sinh", "Việt Nam", "2025", "trên mạng"],
        dinh_dang: ["bảng", "các bước", "liệt kê", "kết luận", "ngắn"],
        du_lieu: ["thông tin sau", "câu sau", "nguyên văn", "cho sẵn"],
        rang_buoc: ["không", "tránh", "đừng", "nếu không biết", "không chắc", "chỉ"],
        kiem_chung: ["nguồn", "ở đâu", "tự kiểm", "kiểm chứng", "trang chính thức", "mức độ chắc chắn", "nói rõ"]
      },
      giaiThich: "Đây chính là kĩ năng kiểm chứng thông tin mà Khung QĐ 2422 đặt làm mục tiêu ('rèn luyện tư duy phản biện, khả năng kiểm chứng thông tin'). Một prompt tốt trong trường hợp này phải ÉP AI nói rõ mức độ chắc chắn và chỉ cách tự tra cứu, thay vì để AI tự khẳng định."
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
  ],

  /* ============ CẤU TRÚC THEO KHỐI LỚP VÀ BÀI HỌC (cập nhật 26/10) ============ */
  lop: {
    10: {
      ten: "Lớp 10",
      baiHoc: {
        "bai-1": {
          ten: "Bài 1: Luật bảo vệ người dùng trong không gian số",
          yccd: "10.A3.1",
          kienThucNen: "<p><b>Mục tiêu:</b> Kể tên được các quy định, luật bảo vệ người dùng trong không gian số.</p><p><b>Nội dung chính:</b></p><ul><li>Luật An ninh mạng 24/2018/QH14</li><li>Luật Dữ liệu 60/2024/QH15</li><li>Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15</li><li>Luật Trí tuệ nhân tạo 134/2025/QH15</li></ul><p><b>Điểm quan trọng:</b> Dữ liệu cá nhân của trẻ em chỉ được xử lí khi có sự đồng ý của cha mẹ hoặc người giám hộ. AI phục vụ con người, không thay thế thẩm quyền và trách nhiệm của con người.</p>",
          baiTap: [
            {
              ten: "Câu 1: Luật nào quy định về dữ liệu cá nhân của trẻ em?",
              de: "Văn bản nào sau đây quy định rằng dữ liệu cá nhân của TRẺ EM chỉ được xử lí khi có sự đồng ý của cha mẹ hoặc người giám hộ?",
              dapAn: "a",
              giaiThich: "Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (Quốc hội thông qua 26/6/2025, hiệu lực 01/01/2026) quy định về quyền của chủ thể dữ liệu và việc xử lí dữ liệu cá nhân của trẻ em."
            },
            {
              ten: "Câu 2: Nguyên tắc nền tảng của Luật AI",
              de: "Luật Trí tuệ nhân tạo của Việt Nam (số 134/2025/QH15) khẳng định nguyên tắc nền tảng nào?",
              dapAn: "b",
              giaiThich: "Nguyên tắc 'AI phục vụ con người, không thay thế thẩm quyền và trách nhiệm của con người' là nền tảng của Luật Trí tuệ nhân tạo 134/2025/QH15."
            }
          ],
          huongDan: "Đọc kỹ nội dung kiến thức nền, sau đó làm các câu hỏi trắc nghiệm. Mỗi câu hỏi có giải thích chi tiết để hiểu rõ hơn về luật.",
          baiTapBoSung: [
            {
              ten: "Bài tập mở rộng: Tìm hiểu thêm về Luật Dữ liệu",
              de: "Luật Dữ liệu 60/2024/QH15 có hiệu lực từ ngày nào? Nêu 3 nội dung chính của luật này.",
              dapAn: "Luật có hiệu lực từ 01/7/2025. Ba nội dung chính: (1) xây dựng và phát triển dữ liệu, (2) bảo vệ và quản trị dữ liệu, (3) xử lí và sử dụng dữ liệu.",
              giaiThich: "Đây là đạo luật đầu tiên quy định toàn diện về dữ liệu số tại Việt Nam, bao gồm 5 chương và 46 điều."
            }
          ]
        },
        "bai-2": {
          ten: "Bài 2: Ứng dụng AI theo tính năng của hệ thống",
          yccd: "10.C2.2",
          kienThucNen: "<p><b>Mục tiêu:</b> Liệt kê được các ứng dụng AI theo tính năng của hệ thống.</p><p><b>6 nhóm tính năng AI:</b></p><ul><li><b>Phân loại:</b> Gán đối tượng vào một nhóm có sẵn (ví dụ: lọc thư rác, nhận diện khuôn mặt)</li><li><b>Dự đoán:</b> Ước lượng giá trị hoặc sự kiện tương lai (ví dụ: dự báo thời tiết)</li><li><b>Tạo sinh:</b> Tạo ra nội dung MỚI (ví dụ: trợ lý ảo viết văn bản, tạo ảnh)</li><li><b>Nhận dạng mẫu:</b> Tìm quy luật lặp lại trong dữ liệu lớn</li><li><b>Xử lí ngôn ngữ:</b> Hiểu và sinh ngôn ngữ tự nhiên (dịch, tóm tắt)</li><li><b>Tối ưu & ra quyết định:</b> Chọn phương án tốt nhất theo ràng buộc</li></ul>",
          baiTap: [
            {
              ten: "Câu 3: Hệ thống phân loại bài làm",
              de: "Một hệ thống tự động đọc ảnh chụp bài làm của học sinh rồi xếp vào 3 nhóm 'đạt / cần cố gắng / chưa đạt' thuộc loại tính năng AI nào?",
              dapAn: "b",
              giaiThich: "Hệ thống gán đối tượng (bài làm) vào một nhóm nhãn CÓ SẴN — đó là bài toán phân loại."
            }
          ],
          huongDan: "Học thuộc 6 nhóm tính năng AI. Khi gặp một ứng dụng, hãy xác định xem nó thuộc nhóm nào dựa trên đầu vào và đầu ra.",
          baiTapBoSung: [
            {
              ten: "Bài tập thực hành: Phân loại ứng dụng",
              de: "Hãy liệt kê 3 ứng dụng AI bạn thường dùng và xác định chúng thuộc nhóm tính năng nào.",
              dapAn: "Ví dụ: (1) Google Dịch - Xử lí ngôn ngữ, (2) ChatGPT - Tạo sinh, (3) Camera nhận diện khuôn mặt - Phân loại.",
              giaiThich: "Một ứng dụng có thể kết hợp nhiều nhóm tính năng. Hãy phân tích kỹ đầu vào và đầu ra để xác định nhóm chính."
            }
          ]
        },
        "bai-3": {
          ten: "Bài 3: AI tạo sinh vs AI phân loại/dự đoán",
          yccd: "10.C3.3",
          kienThucNen: "<p><b>Mục tiêu:</b> Phân biệt được AI tạo sinh với AI phân loại/dự đoán.</p><p><b>So sánh:</b></p><table border='1' style='border-collapse:collapse;width:100%'><tr><th>Tiêu chí</th><th>AI Phân loại/Dự đoán</th><th>AI Tạo sinh</th></tr><tr><td>Nhiệm vụ</td><td>Chọn đáp án từ tập nhãn CÓ SẴN</td><td>Tạo nội dung MỚI chưa tồn tại</td></tr><tr><td>Đầu ra</td><td>Một nhãn hoặc một con số</td><td>Văn bản, hình ảnh, âm thanh, mã lệnh</td></tr><tr><td>Kiểm tra đúng/sai</td><td>DỄ: so với nhãn đúng đã biết</td><td>KHÓ: có thể trôi chảy nhưng sai sự thật</td></tr><tr><td>Lỗi điển hình</td><td>Thiên kiến do dữ liệu huấn luyện lệch</td><td>Bịa đặt (hallucination), đạo văn</td></tr></table><p><b>Kết luận:</b> AI tạo sinh khó kiểm chứng hơn vì đầu ra không có nhãn đúng sẵn.</p>",
          baiTap: [
            {
              ten: "Câu 4: Vì sao AI tạo sinh khó kiểm chứng?",
              de: "Vì sao nội dung do AI TẠO SINH khó kiểm chứng hơn kết quả của AI PHÂN LOẠI?",
              dapAn: "b",
              giaiThich: "AI phân loại có tập nhãn cố định nên đo được độ chính xác. AI tạo sinh tạo nội dung mới — không có sẵn 'đáp án đúng' để so, nên có thể viết rất tự tin mà vẫn bịa số liệu hoặc bịa nguồn."
            }
          ],
          huongDan: "Khi sử dụng AI tạo sinh (như ChatGPT), luôn kiểm chứng thông tin bằng cách đối chiếu với nguồn đáng tin cậy.",
          baiTapBoSung: [
            {
              ten: "Bài tập tình huống: Kiểm chứng thông tin",
              de: "Bạn dùng ChatGPT để viết bài luận về lịch sử Việt Nam. Hãy nêu 3 cách kiểm chứng thông tin trong bài luận đó.",
              dapAn: "(1) Đối chiếu với sách giáo khoa, (2) Tra cứu thêm từ các nguồn chính thức (ví dụ: trang web của Bộ Giáo dục), (3) Hỏi giáo viên hoặc chuyên gia.",
              giaiThich: "AI tạo sinh có thể bịa đặt thông tin nghe có vẻ hợp lý. Việc kiểm chứng là bắt buộc trước khi sử dụng."
            }
          ]
        }
      }
    },
    11: {
      ten: "Lớp 11",
      baiHoc: {
        "bai-1": {
          ten: "Bài 1: Mô hình AI hoạt động như thế nào?",
          yccd: "11.A1.1",
          kienThucNen: "<p><b>Mục tiêu:</b> Hiểu được quy trình huấn luyện, kiểm thử và đánh giá mô hình AI.</p><p><b>Ba bước chính:</b></p><ul><li><b>Bước 1 — Chuẩn bị dữ liệu:</b> Thu thập ảnh, văn bản, âm thanh... rồi gán nhãn (ví dụ: ảnh chó/mèo). Dữ liệu càng nhiều và đa dạng, mô hình càng học tốt.</li><li><b>Bước 2 — Huấn luyện:</b> Máy tính tìm quy luật từ dữ liệu. Quá trình này lặp đi lặp lại hàng nghìn lần để mô hình 'khôn' dần.</li><li><b>Bước 3 — Đánh giá:</b> Cho mô hình làm bài trên dữ liệu mới (chưa từng thấy). Đo độ chính xác, độ chính xác (precision), độ bao phủ (recall).</li></ul><p><b>Điểm quan trọng:</b> Mô hình AI không 'hiểu' như người — nó chỉ khớp mẫu. Nếu dữ liệu huấn luyện lệch, mô hình sẽ dự đoán lệch.</p>",
          baiTap: [
            {
              ten: "Câu 1: Tại sao cần dữ liệu kiểm thử riêng?",
              de: "Trong quy trình huấn luyện AI, tại sao phải chia dữ liệu thành 'tập huấn luyện' và 'tập kiểm thử' riêng biệt?",
              dapAn: "b",
              giaiThich: "Nếu dùng cùng dữ liệu để huấn luyện và kiểm thử, ta không biết mô hình thực sự 'học' hay chỉ 'học vẹt'. Tập kiểm thử phải là dữ liệu mới, chưa từng thấy, để đo khả năng tổng quát hóa."
            },
            {
              ten: "Câu 2: Precision và Recall",
              de: "Một mô hình phát hiện bệnh hiếm gặp: nó báo đúng 9/10 người bệnh (recall 90%) nhưng cứ 100 lần báo thì có 50 lần báo nhầm (precision 50%). Nên ưu tiên chỉ số nào?",
              dapAn: "a",
              giaiThich: "Với bệnh hiếm, bỏ sót người bệnh (recall thấp) nguy hiểm hơn báo nhầm (precision thấp). Ưu tiên recall cao để không bỏ sót, sau đó tối ưu precision."
            }
          ],
          huongDan: "Hãy tưởng tượng bạn dạy em nhỏ nhận biết trái cây: cho xem nhiều ảnh táo, cam (huấn luyện), rồi đưa quả mới để kiểm tra (kiểm thử). Nếu em chỉ nhớ đúng quả đã xem, đó là 'học vẹt' — mô hình AI cũng vậy.",
          baiTapBoSung: [
            {
              ten: "Bài tập thực hành: Thiết kế tập dữ liệu",
              de: "Bạn muốn xây dựng AI phân loại rác (nhựa, giấy, kim loại). Hãy liệt kê: (1) ít nhất 5 loại dữ liệu cần thu thập, (2) cách gán nhãn, (3) cách chia tập huấn luyện/kiểm thử theo tỉ lệ 80/20.",
              dapAn: "(1) Ảnh chai nhựa, báo cũ, lon nhôm, túi nilon, hộp giấy... chụp ở nhiều góc, ánh sáng. (2) Gán nhãn bằng tay: mỗi ảnh ghi 'nhựa'/'giấy'/'kim loại'. (3) Xáo trộn ngẫu nhiên, lấy 80% để huấn luyện, 20% giữ lại kiểm thử — đảm bảo cả hai tập đều có đủ 3 loại.",
              giaiThich: "Chia dữ liệu ngẫu nhiên giúp tránh thiên kiến (ví dụ: tất cả ảnh nhựa đều chụp buổi sáng). Kiểm thử trên dữ liệu đa dạng mới đo được khả năng thực tế."
            }
          ]
        },
        "bai-2": {
          ten: "Bài 2: Thiên kiến (bias) trong AI",
          yccd: "11.A2.1",
          kienThucNen: "<p><b>Mục tiêu:</b> Nhận diện được thiên kiến trong dữ liệu và mô hình AI.</p><p><b>Thiên kiến là gì?</b> Khi mô hình AI đối xử không công bằng với một nhóm người vì dữ liệu huấn luyện không đại diện.</p><p><b>Ví dụ thực tế:</b></p><ul><li>AI nhận diện khuôn mặt nhận diện người da trắng tốt hơn người da màu, vì dữ liệu huấn luyện chủ yếu là ảnh người da trắng.</li><li>AI tuyển dụng tự động loại hồ sơ ứng viên nữ, vì dữ liệu lịch sử cho thấy nam giới được tuyển nhiều hơn.</li></ul><p><b>Cách giảm thiên kiến:</b></p><ul><li>Thu thập dữ liệu đa dạng (đủ giới tính, độ tuổi, vùng miền...).</li><li>Kiểm tra mô hình trên từng nhóm riêng biệt.</li><li>Con người giám sát quyết định cuối cùng.</li></ul>",
          baiTap: [
            {
              ten: "Câu 3: Phát hiện thiên kiến",
              de: "Một AI chấm điểm tín dụng cho vay ngân hàng: người từ vùng nông thôn bị từ chối nhiều hơn người thành phố, dù thu nhập tương đương. Đây có phải thiên kiến không?",
              dapAn: "a",
              giaiThich: "Có — mô hình học từ dữ liệu lịch sử, trong đó người nông thôn có thể bị từ chối nhiều hơn vì định kiến (không phải vì họ thực sự rủi ro hơn). Đây là thiên kiến địa lý, cần được hiệu chỉnh bằng cách thu thập dữ liệu công bằng hơn hoặc thêm biến giải thích."
            },
            {
              ten: "Câu 4: Cách giảm thiên kiến",
              de: "Để giảm thiên kiến giới tính trong AI tuyển dụng, biện pháp nào HIỆU QUẢ NHẤT?",
              dapAn: "c",
              giaiThich: "Thu thập dữ liệu cân bằng (50% nam, 50% nữ) giải quyết gốc rễ. Các biện pháp khác (chỉ dùng ảnh nam, bỏ hoàn toàn giới tính) không khả thi hoặc mất thông tin hữu ích. Giám sát con người là lớp bảo vệ cuối cùng."
            }
          ],
          huongDan: "Khi gặp một hệ thống AI, hãy tự hỏi: 'Dữ liệu huấn luyện có đại diện cho tất cả mọi người không?' Nếu chỉ có ảnh người trẻ, AI sẽ không nhận diện được người già. Thiên kiến không phải lỗi cố ý — nó đến từ dữ liệu không cân bằng.",
          baiTapBoSung: [
            {
              ten: "Bài tập tình huống: AI nhận diện giọng nói",
              de: "Một trợ lý giọng nói hiểu tốt giọng miền Bắc nhưng hay nhầm giọng miền Nam và miền Trung. (1) Nguyên nhân có thể là gì? (2) Đề xuất 2 cách khắc phục.",
              dapAn: "(1) Dữ liệu huấn luyện chủ yếu là giọng miền Bắc. (2) Cách khắc phục: (a) Thu thập thêm dữ liệu giọng miền Nam/Trung với số lượng tương đương, (b) Huấn luyện mô hình riêng cho từng vùng rồi kết hợp, hoặc dùng mô hình đa vùng.",
              giaiThich: "Thiên kiến vùng miền phổ biến trong AI giọng nói vì dữ liệu thường tập trung vào giọng chuẩn (Hà Nội/TP.HCM). Giải pháp là đa dạng hóa dữ liệu hoặc thiết kế mô hình thích ứng."
            }
          ]
        },
        "bai-3": {
          ten: "Bài 3: Đạo đức và trách nhiệm khi sử dụng AI",
          yccd: "11.A3.1",
          kienThucNen: "<p><b>Mục tiêu:</b> Hiểu được trách nhiệm của người sử dụng AI.</p><p><b>Nguyên tắc đạo đức AI:</b></p><ul><li><b>Minh bạch:</b> Cho người dùng biết họ đang tương tác với AI, không phải người thật.</li><li><b>Trách nhiệm giải trình:</b> Khi AI gây hại, ai chịu trách nhiệm? Người phát triển, người triển khai, hay người sử dụng?</li><li><b>Tôn trọng quyền riêng tư:</b> Không thu thập dữ liệu cá nhân khi chưa được đồng ý.</li><li><b>Không gây hại:</b> AI không được tạo nội dung lừa đảo, phân biệt đối xử, hoặc nguy hiểm.</li></ul><p><b>Trách nhiệm của bạn:</b></p><ul><li>Không dùng AI để gian lận học tập.</li><li>Kiểm chứng thông tin AI đưa ra trước khi tin.</li><li>Báo cáo nếu phát hiện AI gây hại.</li></ul>",
          baiTap: [
            {
              ten: "Câu 5: Trách nhiệm khi AI gây hại",
              de: "Một bác sĩ dùng AI hỗ trợ chẩn đoán, AI gợi ý sai khiến bệnh nhân bị điều trị sai. Ai chịu trách nhiệm CHÍNH?",
              dapAn: "b",
              giaiThich: "Bác sĩ chịu trách nhiệm chính vì AI chỉ là công cụ hỗ trợ, quyết định cuối cùng thuộc về con người. Nhà phát triển AI có thể chịu trách nhiệm phụ nếu AI có lỗi kỹ thuật, nhưng bác sĩ phải kiểm tra và xác nhận kết quả trước khi áp dụng."
            },
            {
              ten: "Câu 6: Sử dụng AI trong học tập",
              de: "Bạn dùng ChatGPT để viết bài luận nộp cho giáo viên. Hành động nào SAU ĐÂY là đúng?",
              dapAn: "c",
              giaiThich: "Dùng AI để gợi ý ý tưởng, dàn bài, hoặc kiểm tra ngữ pháp là hợp lý. Nhưng nộp nguyên văn bài AI viết là gian lận — bạn không học được gì và vi phạm quy định học thuật. Luôn ghi rõ nguồn nếu sử dụng AI."
            }
          ],
          huongDan: "Hãy nhớ: AI là công cụ, không phải người thay thế. Bạn chịu trách nhiệm cho mọi quyết định dựa trên AI. Khi nghi ngờ, hãy hỏi: 'Nếu AI sai, ai sẽ chịu hậu quả?' — câu trả lời thường là BẠN.",
          baiTapBoSung: [
            {
              ten: "Bài tập thảo luận: Quy tắc sử dụng AI",
              de: "Hãy đề xuất 5 quy tắc sử dụng AI trong lớp học mà bạn nghĩ là công bằng và hiệu quả. Giải thích lý do cho mỗi quy tắc.",
              dapAn: "Ví dụ: (1) Được dùng AI để gợi ý ý tưởng, không được nộp nguyên văn. (2) Phải ghi rõ đã dùng AI ở phần nào. (3) Không dùng AI trong bài kiểm tra trên lớp. (4) Kiểm chứng mọi thông tin AI đưa ra. (5) Chia sẻ cách dùng AI hiệu quả với bạn bè.",
              giaiThich: "Quy tắc tốt cân bằng giữa tận dụng công nghệ và đảm bảo học thật. Mục tiêu là dùng AI để học tốt hơn, không phải để đối phó."
            }
          ]
        }
      }
    },
    12: {
      ten: "Lớp 12",
      baiHoc: {
        "bai-1": {
          ten: "Bài 1: Ứng dụng AI trong thực tiễn",
          yccd: "12.A1.1",
          kienThucNen: "<p><b>Mục tiêu:</b> Liệt kê được các ứng dụng AI trong đời sống và phân tích tác động.</p><p><b>Các lĩnh vực ứng dụng AI:</b></p><ul><li><b>Y tế:</b> Chẩn đoán bệnh từ ảnh X-quang, dự đoán nguy cơ bệnh tim mạch, hỗ trợ phẫu thuật robot.</li><li><b>Giao thông:</b> Xe tự lái, tối ưu lộ trình, dự báo tắc đường.</li><li><b>Giáo dục:</b> Hệ thống học thích ứng (adaptive learning), chấm bài tự động, trợ lý ảo.</li><li><b>Tài chính:</b> Phát hiện gian lận, chấm điểm tín dụng, giao dịch tự động.</li><li><b>Nông nghiệp:</b> Dự báo thời tiết, phát hiện sâu bệnh từ ảnh drone, tối ưu tưới tiêu.</li></ul><p><b>Tác động hai mặt:</b></p><ul><li><b>Tích cực:</b> Tăng hiệu quả, giảm chi phí, giải quyết bài toán phức tạp.</li><li><b>Tiêu cực:</b> Mất việc làm, thiên kiến, rủi ro bảo mật, phụ thuộc công nghệ.</li></ul>",
          baiTap: [
            {
              ten: "Câu 1: Phân tích ứng dụng AI",
              de: "Một bệnh viện triển khai AI chẩn đoán ung thư phổi từ ảnh CT. Ưu điểm và rủi ro lớn nhất là gì?",
              dapAn: "a",
              giaiThich: "Ưu điểm: phát hiện sớm, chính xác cao, giảm tải cho bác sĩ. Rủi ro: AI có thể bỏ sót trường hợp hiếm (false negative) hoặc báo nhầm (false positive), cần bác sĩ kiểm tra lại. Không thể thay thế hoàn toàn bác sĩ vì AI không hiểu ngữ cảnh lâm sàng."
            },
            {
              ten: "Câu 2: AI và việc làm",
              de: "AI tự động hóa nhiều công việc lặp lại. Ngành nào SAU ĐÂY có nguy cơ bị thay thế CAO NHẤT?",
              dapAn: "c",
              giaiThich: "Nhân viên nhập liệu — công việc lặp đi lặp lại, dễ tự động hóa. Giáo viên, bác sĩ, nghệ sĩ cần sáng tạo, tương tác người, ra quyết định phức tạp — AI khó thay thế hoàn toàn, chỉ hỗ trợ."
            }
          ],
          huongDan: "Khi phân tích ứng dụng AI, hãy cân nhắc cả lợi ích và rủi ro. Không có công nghệ nào hoàn hảo — quan trọng là dùng đúng cách và có con người giám sát.",
          baiTapBoSung: [
            {
              ten: "Bài tập nghiên cứu: AI trong lĩnh vực bạn quan tâm",
              de: "Chọn một lĩnh vực bạn quan tâm (thể thao, âm nhạc, thời trang...). Tìm hiểu và viết 1 trang về: (1) AI đang được dùng như thế nào trong lĩnh vực đó, (2) Ưu điểm và hạn chế, (3) Dự đoán xu hướng trong 5 năm tới.",
              dapAn: "Ví dụ (thể thao): (1) AI phân tích video trận đấu, dự đoán chấn thương cầu thủ, tối ưu chiến thuật. (2) Ưu: phân tích nhanh, chính xác. Hạn chế: cần dữ liệu lớn, không thay thế trực giác huấn luyện viên. (3) Xu hướng: AI cá nhân hóa chương trình tập luyện cho từng vận động viên.",
              giaiThich: "Bài tập này giúp bạn kết nối kiến thức AI với sở thích cá nhân, đồng thời rèn kỹ năng nghiên cứu và trình bày."
            }
          ]
        },
        "bai-2": {
          ten: "Bài 2: Xây dựng hệ thống AI đơn giản",
          yccd: "12.A2.1",
          kienThucNen: "<p><b>Mục tiêu:</b> Hiểu được các bước xây dựng một hệ thống AI hoàn chỉnh.</p><p><b>Quy trình 6 bước:</b></p><ol><li><b>Xác định bài toán:</b> Phân loại, dự đoán, hay tạo sinh? Đầu vào/đầu ra là gì?</li><li><b>Thu thập dữ liệu:</b> Càng nhiều càng tốt, đảm bảo đa dạng và chất lượng.</li><li><b>Tiền xử lý dữ liệu:</b> Làm sạch (xóa nhiễu, điền khuyết), chuẩn hóa (cùng đơn vị, kích thước), gán nhãn.</li><li><b>Chọn mô hình:</b> Cây quyết định, mạng neural, SVM... tùy bài toán và dữ liệu.</li><li><b>Huấn luyện và đánh giá:</b> Chia tập train/test, huấn luyện, đo độ chính xác, điều chỉnh siêu tham số.</li><li><b>Triển khai và giám sát:</b> Đưa vào sử dụng, theo dõi hiệu suất, cập nhật khi cần.</li></ol><p><b>Công cụ phổ biến:</b> Python + thư viện scikit-learn, TensorFlow, PyTorch.</p>",
          baiTap: [
            {
              ten: "Câu 3: Thứ tự các bước",
              de: "Sắp xếp đúng thứ tự các bước xây dựng hệ thống AI: (a) Huấn luyện mô hình, (b) Thu thập dữ liệu, (c) Triển khai, (d) Xác định bài toán, (e) Tiền xử lý dữ liệu.",
              dapAn: "b",
              giaiThich: "Thứ tự đúng: (d) Xác định bài toán → (b) Thu thập dữ liệu → (e) Tiền xử lý → (a) Huấn luyện → (c) Triển khai. Phải biết bài toán trước khi thu thập dữ liệu, phải làm sạch dữ liệu trước khi huấn luyện."
            },
            {
              ten: "Câu 4: Chọn mô hình",
              de: "Bài toán dự đoán giá nhà dựa trên diện tích, vị trí, số phòng. Mô hình nào PHÙ HỢP NHẤT?",
              dapAn: "a",
              giaiThich: "Hồi quy tuyến tính (linear regression) phù hợp vì đầu ra là giá trị liên tục (giá nhà). Phân loại (classification) dùng cho bài toán nhãn rời rạc (chó/mèo). CNN dùng cho ảnh. RNN dùng cho chuỗi thời gian."
            }
          ],
          huongDan: "Xây dựng AI không chỉ là code — quan trọng nhất là hiểu bài toán và chuẩn bị dữ liệu tốt. Dữ liệu xấu → mô hình tồi, dù thuật toán xịn. Hãy dành 70% thời gian cho dữ liệu, 30% cho mô hình.",
          baiTapBoSung: [
            {
              ten: "Bài tập thực hành: Thiết kế hệ thống AI",
              de: "Thiết kế hệ thống AI phân loại email spam/không spam. Trình bày: (1) Đầu vào/đầu ra, (2) Cách thu thập dữ liệu, (3) Tiền xử lý (làm gì với email?), (4) Chọn mô hình, (5) Đánh giá bằng chỉ số nào.",
              dapAn: "(1) Đầu vào: nội dung email (tiêu đề + thân). Đầu ra: 'spam' hoặc 'không spam'. (2) Thu thập từ hộp thư của bạn, gán nhãn thủ công. (3) Tiền xử lý: xóa HTML, chuyển về chữ thường, loại bỏ từ dừng (của, là, và...), trích xuất đặc trưng (TF-IDF). (4) Mô hình: Naive Bayes hoặc SVM. (5) Đánh giá: precision, recall, F1-score — ưu tiên precision để không nhầm email quan trọng thành spam.",
              giaiThich: "Đây là bài toán kinh điển trong xử lý ngôn ngữ. Bạn có thể thử với thư viện scikit-learn trong Python — chỉ cần ~50 dòng code."
            }
          ]
        },
        "bai-3": {
          ten: "Bài 3: Tương lai của AI và chuẩn bị cho sự nghiệp",
          yccd: "12.A3.1",
          kienThucNen: "<p><b>Mục tiêu:</b> Hiểu được xu hướng AI và cách chuẩn bị bản thân.</p><p><b>Xu hướng AI 2025-2030:</b></p><ul><li><b>AI tạo sinh (Generative AI):</b> ChatGPT, Midjourney, Sora... tạo văn bản, ảnh, video chất lượng cao.</li><li><b>AI đa phương thức:</b> Một mô hình hiểu cả văn bản, ảnh, âm thanh.</li><li><b>AI cá nhân hóa:</b> Trợ lý ảo hiểu sở thích, thói quen của từng người.</li><li><b>AI biên (Edge AI):</b> Chạy trên điện thoại, thiết bị IoT, không cần internet.</li><li><b>AI đáng tin cậy (Trustworthy AI):</b> Minh bạch, giải thích được, bảo vệ quyền riêng tư.</li></ul><p><b>Kỹ năng cần chuẩn bị:</b></p><ul><li><b>Kỹ năng kỹ thuật:</b> Lập trình Python, toán (đại số, xác suất), hiểu nguyên lý AI.</li><li><b>Kỹ năng mềm:</b> Tư duy phản biện, sáng tạo, giao tiếp, làm việc nhóm.</li><li><b>Hiểu biết đạo đức:</b> Nhận diện thiên kiến, bảo vệ quyền riêng tư, sử dụng AI có trách nhiệm.</li></ul><p><b>Cơ hội nghề nghiệp:</b> Kỹ sư AI, nhà khoa học dữ liệu, chuyên gia đạo đức AI, quản lý sản phẩm AI...</p>",
          baiTap: [
            {
              ten: "Câu 5: Kỹ năng thời đại AI",
              de: "Trong thời đại AI, kỹ năng nào TRỞ NÊN QUAN TRỌNG HƠN cho con người?",
              dapAn: "b",
              giaiThich: "Tư duy phản biện và sáng tạo — vì AI giỏi làm việc lặp lại, tính toán, nhưng kém về sáng tạo, đánh giá ngữ cảnh, ra quyết định đạo đức. Kỹ năng lập trình vẫn cần nhưng không còn là lợi thế duy nhất."
            },
            {
              ten: "Câu 6: Chuẩn bị cho tương lai",
              de: "Bạn muốn trở thành kỹ sư AI. Lộ trình nào HỢP LÝ NHẤT?",
              dapAn: "c",
              giaiThich: "Học toán (đại số, xác suất) + lập trình Python → học machine learning cơ bản → thực hành với dự án nhỏ → chuyên sâu vào lĩnh vực cụ thể (NLP, computer vision...). Không cần đợi đến đại học — có thể bắt đầu từ bây giờ với các khóa online miễn phí."
            }
          ],
          huongDan: "AI không thay thế con người — nhưng người biết dùng AI sẽ thay thế người không biết. Hãy bắt đầu học từ bây giờ, không cần phải là thiên tài toán hay lập trình siêu đẳng. Quan trọng là tò mò, kiên nhẫn, và không sợ sai.",
          baiTapBoSung: [
            {
              ten: "Bài tập lập kế hoạch: Lộ trình học AI của bạn",
              de: "Viết kế hoạch 6 tháng để học AI cơ bản. Bao gồm: (1) Mục tiêu cụ thể, (2) Tài nguyên học (sách, khóa online, YouTube), (3) Thời gian biểu hàng tuần, (4) Dự án thực hành, (5) Cách đánh giá tiến độ.",
              dapAn: "Ví dụ: Tháng 1-2: Học Python cơ bản (khóa Codecademy, 5h/tuần). Tháng 3-4: Học machine learning (khóa Coursera Andrew Ng, 6h/tuần). Tháng 5: Thực hành dự án phân loại ảnh chó/mèo với TensorFlow. Tháng 6: Viết blog chia sẻ kiến thức, tham gia cộng đồng AI. Đánh giá: hoàn thành bài tập hàng tuần, chạy được dự án cuối khóa.",
              giaiThich: "Kế hoạch tốt phải cụ thể, đo được, và linh hoạt. Đừng tham lam học nhiều thứ cùng lúc — tập trung vào một thứ, làm xong rồi mới chuyển sang thứ khác."
            }
          ]
        }
      }
    }
  }
};
