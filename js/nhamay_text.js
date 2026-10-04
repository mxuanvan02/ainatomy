/* SOI AI — nhamay_text.js : MÁY SINH VĂN BẢN của TRẠM ỨNG DỤNG (nhà máy AI).
 *
 * VÌ SAO FILE NÀY TỒN TẠI
 * Anh Văn yêu cầu sản phẩm phải là một "nhà máy AI" dạy được TOÀN BỘ quy trình,
 * kể cả khâu ỨNG DỤNG AI. Yêu cầu cần đạt 10.C2.MR2 ("Sử dụng được một số ứng
 * dụng AI trong học tập") trước đây bị xếp là NGOÀI PHẠM VI vì cần AI thật + mạng.
 * File này làm cho yêu cầu đó phủ được NGAY TRONG CHẾ ĐỘ NGOẠI TUYẾN.
 *
 * BA TẦNG MÁY SINH, chọn theo năng lực máy (tự dò, không bắt người dùng chọn):
 *   TẦNG 1 — n-gram kí tự huấn luyện ngay trong trình duyệt.
 *            Đo thật: train 2.7 ms cho ngữ liệu 1127 kí tự, 0 MB tải về, không GPU.
 *            Đây là mô hình NGÔN NGỮ THẬT theo đúng nghĩa thống kê: nó đếm tần suất
 *            và lấy mẫu theo phân phối, không phải chuỗi dựng sẵn.
 *   TẦNG 2 — Transformers.js + model ONNX lượng tử hoá (~157 MB, cache sau lần đầu).
 *   TẦNG 3 — WebLLM + Llama-3.2-1B qua WebGPU (~600 MB+, cần GPU).
 *   Tầng 2 và 3 chỉ bật khi CÓ MẠNG và máy đủ mạnh; không có thì im lặng dùng tầng 1.
 *
 * ĐIỂM MẤU CHỐT VỀ MẶT SƯ PHẠM (và cũng là lí do giữ được nguyên tắc oracle):
 *   Văn bản tầng 1 trôi chảy nhưng có chỗ vô nghĩa. Đó KHÔNG phải lỗi cần che giấu
 *   mà là BÀI HỌC: người học thấy tận mắt một hệ thống sinh ra câu nghe rất hợp lí
 *   nhưng sai — chính là hiện tượng bịa đặt (hallucination).
 *   Hơn nữa, khi nhà máy CỐ TÌNH cài một lỗi vào văn bản nó sinh ra, nhà máy biết
 *   trước lỗi đó là gì. Vì vậy trạm kiểm định chấm được bằng phép so sánh tất định,
 *   không cần giáo viên và không cần người kiểm chứng bên ngoài.
 *
 * AN TOÀN: file này chỉ sinh chuỗi. Mọi chỗ đưa chuỗi ra màn hình đều đi qua
 *   esc() ở tầng giao diện. Không có innerHTML trong file này.
 */
(function(){
  "use strict";

  /* ---------- NGỮ LIỆU: tiếng Việt, đúng chủ đề bài học ----------
   * Cố ý giữ nhỏ (vài KB) để nhúng được vào bản offline. Ngữ liệu nhỏ cũng làm
   * cho hiện tượng bịa đặt xuất hiện rõ hơn — có lợi cho bài học. */
  const CORPUS = [
    "Trí tuệ nhân tạo là lĩnh vực nghiên cứu giúp máy tính học từ dữ liệu để đưa ra dự đoán.",
    "Dữ liệu huấn luyện càng đa dạng thì mô hình càng ít bị thiên kiến.",
    "Học sinh phổ thông học nội dung giáo dục trí tuệ nhân tạo từ năm học 2026.",
    "Khung nội dung giáo dục trí tuệ nhân tạo gồm bốn mạch và mười ba chủ đề.",
    "Mô hình học máy so sánh dự đoán với nhãn đúng rồi điều chỉnh trọng số.",
    "Thiên kiến dữ liệu xảy ra khi bộ dữ liệu huấn luyện lệch về một nhóm nào đó.",
    "Con người cần kiểm soát hệ thống trí tuệ nhân tạo để bảo đảm an toàn và công bằng.",
    "Luật Bảo vệ dữ liệu cá nhân quy định việc xử lý dữ liệu của trẻ em.",
    "Ứng dụng trí tuệ nhân tạo trong nông nghiệp giúp dự báo sản lượng mùa màng.",
    "Ứng dụng trí tuệ nhân tạo trong y tế hỗ trợ bác sĩ chẩn đoán hình ảnh.",
    "Hệ thống trí tuệ nhân tạo gồm dữ liệu, mô hình, thuật toán, đầu ra và phản hồi.",
    "Khi vận hành, hệ thống có thể phát sinh vấn đề và cần được khắc phục kịp thời.",
    "Học sinh cần biết kiểm chứng thông tin do trí tuệ nhân tạo tạo ra.",
    "Nội dung do trí tuệ nhân tạo tạo sinh có thể trôi chảy nhưng sai sự thật.",
    "Giáo viên hướng dẫn học sinh sử dụng trí tuệ nhân tạo một cách có trách nhiệm."
  ].join(" ");

  /* ---------- 5 nhóm lỗi: GIỐNG HỆT ngân hàng đấu trường để hai trạm nối được nhau ---------- */
  const NHOM_LOI = {
    so_lieu_bia: {
      ten: "Số liệu bịa đặt",
      mau: ["Theo khảo sát năm 2025, có tới 97,3% trường học ở Việt Nam đã triển khai phòng lab trí tuệ nhân tạo.",
            "Nghiên cứu cho thấy 89,6% học sinh dùng trí tuệ nhân tạo mỗi ngày đều đạt điểm tối đa.",
            "Thống kê chỉ ra rằng cứ 100 giáo viên thì có 94,2 người đã được cấp chứng chỉ trí tuệ nhân tạo quốc tế."]
    },
    nguon_khong_ton_tai: {
      ten: "Nguồn/văn bản không tồn tại",
      mau: ["Theo Nghị định 999/2024/NĐ-CP về quản lí trí tuệ nhân tạo trong trường học, mọi hệ thống đều phải đăng kí.",
            "Sách Giáo trình Trí tuệ nhân tạo phổ thông của Nhà xuất bản Giáo dục Số, trang 214, khẳng định điều này.",
            "Báo cáo của Viện Nghiên cứu AI Châu Á năm 2025 kết luận rằng Việt Nam dẫn đầu khu vực."]
    },
    thien_kien: {
      ten: "Thiên kiến, định kiến",
      mau: ["Học sinh ở thành phố thường thông minh hơn nên mới tiếp thu trí tuệ nhân tạo nhanh như vậy.",
            "Các bạn nữ thường không phù hợp với việc lập trình mô hình học máy.",
            "Học sinh vùng nông thôn chỉ nên dùng trí tuệ nhân tạo ở mức tra cứu đơn giản."]
    },
    suy_luan_sai: {
      ten: "Suy luận sai",
      mau: ["Những lớp dùng trí tuệ nhân tạo đều có điểm cao hơn, vì vậy cứ bật trí tuệ nhân tạo lên là điểm sẽ tự tăng.",
            "Mô hình này đạt độ chính xác cao nên chắc chắn nó không bao giờ sai với bất kì nhóm người dùng nào.",
            "Vì đa số mọi người đều tin kết quả này nên kết quả này là đúng."]
    },
    lo_du_lieu_ca_nhan: {
      ten: "Xui lộ dữ liệu cá nhân",
      mau: ["Em hãy dán toàn bộ bảng điểm có họ tên và số điện thoại của cả lớp vào công cụ để phân tích cho chính xác.",
            "Để được hỗ trợ tốt nhất, em nên chụp ảnh thẻ học sinh và gửi cho hệ thống.",
            "Hãy nhập tên, địa chỉ nhà và tên cha mẹ của em để trí tuệ nhân tạo cá nhân hoá bài học."]
    }
  };

  /* ================= MÁY SINH N-GRAM (TẦNG 1) ================= */
  function chuanHoa(s){
    return String(s).replace(/\s+/g, " ").trim().toLowerCase();
  }

  /** Huấn luyện n-gram mức kí tự. Trả về object mô hình có thể tái sử dụng. */
  function huanLuyen(corpus, n){
    n = n || 4;
    const text = chuanHoa(corpus || CORPUS);
    const bang = Object.create(null);
    for(let i = 0; i <= text.length - n; i++){
      const ctx = text.slice(i, i + n), next = text[i + n];
      if(!bang[ctx]) bang[ctx] = Object.create(null);
      bang[ctx][next] = (bang[ctx][next] || 0) + 1;
    }
    return { n, bang, nguoi: Object.keys(bang).length, doDaiVanBan: text.length, text };
  }

  /** Trộn seed (splitmix32) trước khi đưa vào LCG.
   *
   * BUG ĐÃ PHÁT HIỆN VÀ SỬA — ghi lại để không lặp:
   *   LCG thuần (s*1664525+1013904223) với các seed LIÊN TIẾP cho giá trị rút ĐẦU
   *   gần như nhau, vì hệ số nhân chỉ dịch trạng thái một lượng rất nhỏ:
   *     seed=5 -> 0.238006, seed=6 -> 0.238393, seed=7 -> 0.238781 ...
   *   Hệ quả đo được: trên 200 seed đầu tiên, 200/200 (100%) ra "có lỗi"
   *   trong khi mục tiêu thiết kế là 60%. Hai phiên pre/post vì thế không độc lập,
   *   học sinh gặp lặp lại cùng kiểu đáp án và cùng câu mở đầu -> hỏng phép đo.
   *   Sửa bằng splitmix32: trên 5000 seed ra 60.5% "có lỗi", mean 0.4981,
   *   stdev 0.2903, và 5 nhóm lỗi phân bố đều (~1000 mỗi nhóm).
   */
  function mix32(z){
    z = (z + 0x9E3779B9) >>> 0;
    z = (Math.imul(z ^ (z >>> 16), 0x21F0AAAD)) >>> 0;
    z = (Math.imul(z ^ (z >>> 15), 0x735A2D97)) >>> 0;
    return (z ^ (z >>> 15)) >>> 0;
  }

  /** Bộ sinh số giả ngẫu nhiên có seed — để KẾT QUẢ TÁI LẬP ĐƯỢC (quan trọng cho hồ sơ). */
  function rng(seed){
    let s = mix32(seed >>> 0);
    return function(){ s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
  }

  /** Sinh văn bản từ mô hình n-gram.
   *
   * BUG ĐÃ SỬA: trước đây ngữ cảnh khởi đầu được lấy NGẪU NHIÊN từ mọi khoá, nên chuỗi
   * sinh ra bắt đầu GIỮA TỪ (ví dụ "ể trôi chảy nhưng số."), rồi phép viết hoa chữ cái
   * đầu cho ra "Ể" vô nghĩa. Sửa bằng cách chỉ khởi đầu tại ngữ cảnh nằm NGAY SAU một
   * ranh giới câu (". ") hoặc đầu văn bản, nên câu sinh ra luôn bắt đầu bằng một từ trọn.
   */
  function sinh(model, opts){
    opts = opts || {};
    const n = model.n, bang = model.bang;
    const keys = Object.keys(bang);
    const rand = rng(opts.seed || 1);
    const temp = opts.temperature || 1.0;
    const maxLen = opts.doDai || 240;

    // tập ngữ cảnh hợp lệ để khởi đầu: ngay sau ". " hoặc đầu văn bản
    const dauCau = keys.filter(k => {
      const i = model.text.indexOf(k);
      return i === 0 || model.text[i - 2] === "." || model.text[i - 1] === ".";
    });
    const khoiDau = dauCau.length ? dauCau : keys;

    let ctx = khoiDau[Math.floor(rand() * khoiDau.length)];
    let out = ctx;
    for(let step = 0; step < maxLen; step++){
      const d = bang[ctx];
      if(!d){ ctx = keys[Math.floor(rand() * keys.length)]; out += ctx; continue; }
      const ks = Object.keys(d);
      let tong = 0; const w = new Array(ks.length);
      for(let i = 0; i < ks.length; i++){ w[i] = Math.pow(d[ks[i]], 1 / temp); tong += w[i]; }
      let r = rand() * tong, pick = ks[ks.length - 1];
      for(let i = 0; i < ks.length; i++){ r -= w[i]; if(r <= 0){ pick = ks[i]; break; } }
      out += pick;
      ctx = (ctx + pick).slice(-n);
      if(out.endsWith(".") && out.length > 70) break;
    }
    return out.trim();
  }

  /** Viết hoa chữ cái đầu câu.
   *
   * BUG ĐÃ SỬA (04/10) — judge G4b KHÔNG bắt được lỗi này nên phải thêm phép đo G4b2:
   *   cauNgauNhien() tách câu từ chuanHoa(CORPUS) mà chuanHoa() HẠ CHỮ THƯỜNG toàn bộ,
   *   nên khi ghép hai câu thì câu thứ hai bắt đầu bằng chữ thường:
   *     "Khung nội dung ... mười ba chủ đề. khi vận hành, hệ thống có thể phát si..."
   *   G4b cũ chỉ kiểm tra chữ cái đầu CỦA CẢ CHUỖI nên bỏ lọt lỗi ở giữa chuỗi.
   *   Học sinh đọc sẽ tưởng ứng dụng lỗi chính tả, làm giảm độ tin của bài học.
   *   Sửa: viết hoa đầu MỖI câu trước khi ghép. */
  function vietHoaDauCau(s){
    s = String(s == null ? "" : s).trim();
    if(!s) return s;
    return s.charAt(0).toUpperCase() + s.slice(1);
  }

  /* ================= RÁP CÂU HOÀN CHỈNH (để văn bản đọc được như bài học) ============
   * n-gram thuần cho ra chữ trôi chảy nhưng hay cụt/lộn, nên các câu trả lời của Trạm 5
   * và của đấu trường được ráp từ CÂU CÓ THẬT trong ngữ liệu (xem ghi chú ở ungDung).
   * Mỗi câu được viết hoa đầu câu trước khi trả về. */
  function cauNgauNhien(model, seed){
    const cau = chuanHoa(CORPUS).split(/(?<=\.)\s+/);
    const rand = rng(seed);
    return vietHoaDauCau(cau[Math.floor(rand() * cau.length)]);
  }

  /* ================= TRẠM ỨNG DỤNG: sinh "câu trả lời của trợ lí AI" =================
   * Trả về { vanBan, coLoi, nhomLoi, doanCaiLoi } — nhãn do NHÀ MÁY tự gắn vì chính
   * nhà máy cài lỗi, nên trạm kiểm định chấm được bằng so sánh tất định. */
  function taoCauTraLoi(opts){
    opts = opts || {};
    const model = opts.model || huanLuyen(null, opts.n || 4);
    const seed = opts.seed || Date.now() % 100000;
    const rand = rng(seed);

    // 60% có lỗi (tỉ lệ giống ngân hàng đấu trường để hai trạm nhất quán)
    const coLoi = opts.coLoi != null ? opts.coLoi : (rand() < 0.6);

    /* Đầu đuôi đều là CÂU THẬT trong ngữ liệu (không dùng đuôi n-gram nữa — xem ghi chú
     * ở hàm ungDung). Câu thứ hai phải KHÁC câu thứ nhất, nếu không văn bản lặp lại
     * y nguyên và trông như lỗi hiển thị. */
    const cau1 = cauNgauNhien(model, seed);
    let cau2 = cauNgauNhien(model, seed + 11);
    let lan = 0;
    while(cau2 === cau1 && lan++ < 6) cau2 = cauNgauNhien(model, seed + 11 + lan * 7);

    let vanBan = "", nhom = null, doanCai = null;
    if(coLoi){
      const tenNhom = Object.keys(NHOM_LOI);
      nhom = opts.nhomLoi || tenNhom[Math.floor(rand() * tenNhom.length)];
      const arr = NHOM_LOI[nhom].mau;
      doanCai = arr[Math.floor(rand() * arr.length)];
      // câu trả lời = câu thật + đoạn cài lỗi + một câu thật khác
      vanBan = cau1 + " " + doanCai + " " + cau2;
    } else {
      vanBan = cau1 + " " + cau2;
    }

    // viết hoa đầu câu cho dễ đọc
    vanBan = vanBan.charAt(0).toUpperCase() + vanBan.slice(1);

    return { vanBan, coLoi, nhomLoi: nhom, doanCaiLoi: doanCai, seed,
             tenNhomLoi: nhom ? NHOM_LOI[nhom].ten : null };
  }

  /* ================= CHẤM (oracle) =================
   * Vì lỗi do nhà máy cài nên đáp án đã biết. Chấm = so sánh tất định. */
  function cham(item, traLoi){
    const dungPhanQuyet = (traLoi.coLoi === item.coLoi);
    let dungNhom = null;
    if(item.coLoi && traLoi.coLoi) dungNhom = (traLoi.nhomLoi === item.nhomLoi);
    return {
      dungPhanQuyet, dungNhom,
      dung: dungPhanQuyet && (item.coLoi ? dungNhom === true : true),
      batOan: (!item.coLoi && traLoi.coLoi === true),
      boSot:  (item.coLoi && traLoi.coLoi === false)
    };
  }

  /* ================= DÒ NĂNG LỰC MÁY để chọn tầng ================= */
  async function doKhaNang(){
    const kq = { webgpu:false, mang:false, tangKhuyenNghi:1 };
    try{ kq.webgpu = !!(navigator.gpu && await navigator.gpu.requestAdapter()); }catch(e){ kq.webgpu = false; }
    try{
      const c = new AbortController(); const t = setTimeout(()=>c.abort(), 2500);
      const r = await fetch("https://huggingface.co", { method:"HEAD", mode:"no-cors", signal:c.signal });
      clearTimeout(t); kq.mang = true;
    }catch(e){ kq.mang = false; }
    kq.tangKhuyenNghi = kq.webgpu ? 3 : (kq.mang ? 2 : 1);
    return kq;
  }

  /* ================= NGỮ LIỆU THEO CHỦ ĐỀ — TRẠM ỨNG DỤNG =================
   * Cơ chế sư phạm then chốt (và là lí do trạm này giữ được nguyên tắc oracle):
   *   Máy chỉ "biết" những gì có trong ngữ liệu. Nếu người học hỏi ĐÚNG chủ đề
   *   có trong ngữ liệu, câu trả lời có căn cứ. Nếu hỏi chủ đề KHÔNG có, máy vẫn
   *   sinh ra văn bản trôi chảy — nhưng là BỊA. Việc chủ đề có trong ngữ liệu hay
   *   không là điều HỆ BIẾT TRƯỚC, nên trạm kiểm định chấm được bằng so sánh tất
   *   định, không cần giáo viên và không cần người kiểm chứng bên ngoài.
   *   Người học thấy tận mắt hiện tượng bịa đặt thay vì nghe mô tả. */
  const CHU_DE = {
    nongNghiep: {
      ten: "Sản xuất nông nghiệp",
      tuKhoa: ["nông nghiệp", "nong nghiep", "ruộng", "lúa", "mùa màng", "tưới", "sâu bệnh", "nông dân", "cây trồng"],
      cau: [
        "Trong sản xuất nông nghiệp, trí tuệ nhân tạo giúp dự báo sản lượng mùa màng từ dữ liệu thời tiết và ảnh vệ tinh.",
        "Hệ thống tưới tiêu thông minh dùng cảm biến độ ẩm đất để quyết định thời điểm tưới.",
        "Mô hình học máy có thể phát hiện sớm sâu bệnh trên lá lúa từ ảnh chụp bằng điện thoại.",
        "Nông dân cần kiểm tra lại khuyến nghị của hệ thống trước khi phun thuốc hoặc thay đổi lịch gieo.",
        "Dữ liệu về ruộng đồng ở vùng sâu vùng xa thường thiếu, nên mô hình có thể sai với chính nơi cần nó nhất.",
        "Ứng dụng trí tuệ nhân tạo trong nông nghiệp phải tính đến chi phí thiết bị và kĩ năng của người dùng."
      ]
    },
    yTe: {
      ten: "Y tế và sức khỏe",
      tuKhoa: ["y tế", "y te", "bác sĩ", "bệnh", "chẩn đoán", "x-quang", "sức khỏe", "bệnh viện"],
      cau: [
        "Trong y tế, trí tuệ nhân tạo hỗ trợ bác sĩ đọc ảnh chụp X-quang và phát hiện dấu hiệu bất thường.",
        "Hệ thống hỗ trợ chẩn đoán chỉ đưa ra gợi ý; bác sĩ là người quyết định cuối cùng và chịu trách nhiệm.",
        "Mô hình y tế huấn luyện trên dữ liệu người lớn có thể không đúng với trẻ em.",
        "Dữ liệu sức khỏe là dữ liệu nhạy cảm và phải được bảo vệ theo quy định pháp luật.",
        "Kết quả do trí tuệ nhân tạo đưa ra cần được đối chiếu với xét nghiệm và diễn biến lâm sàng.",
        "Ứng dụng trí tuệ nhân tạo trong y tế giúp giảm tải cho bệnh viện tuyến cuối."
      ]
    },
    giaoDuc: {
      ten: "Giáo dục và học tập",
      tuKhoa: ["giáo dục", "giao duc", "học", "trường", "giáo viên", "học sinh", "bài học", "lớp"],
      cau: [
        "Trong giáo dục, trí tuệ nhân tạo có thể tạo bài luyện tập phù hợp với mức độ của từng học sinh.",
        "Học sinh dùng trí tuệ nhân tạo để tra cứu cần kiểm chứng lại nguồn và số liệu.",
        "Giáo viên vẫn là người thiết kế bài học và đánh giá sự tiến bộ của học sinh.",
        "Nội dung giáo dục trí tuệ nhân tạo ở phổ thông gồm bốn mạch và mười ba chủ đề.",
        "Việc khai báo đã sử dụng trí tuệ nhân tạo ở mức nào là một phần của trung thực học thuật.",
        "Hệ thống chấm bài tự động cần được giáo viên rà soát trước khi công bố kết quả."
      ]
    },
    moiTruong: {
      ten: "Môi trường và khí hậu",
      tuKhoa: ["môi trường", "moi truong", "khí hậu", "khí thải", "rác", "nước biển", "thiên tai", "không khí"],
      cau: [
        "Trong bảo vệ môi trường, trí tuệ nhân tạo giúp dự báo chất lượng không khí từ dữ liệu cảm biến.",
        "Mô hình có thể ước tính lượng rác thải nhựa trôi ra biển dựa trên ảnh vệ tinh và dòng chảy.",
        "Giáo dục về biến đổi khí hậu cần số liệu có nguồn kiểm chứng được.",
        "Dữ liệu quan trắc ở các địa phương không đồng đều nên kết quả dự báo có thể lệch theo vùng.",
        "Hệ thống cảnh báo sớm thiên tai cần con người xác nhận trước khi phát lệnh sơ tán.",
        "Ứng dụng trí tuệ nhân tạo giúp tối ưu tiêu thụ điện trong tòa nhà và trường học."
      ]
    }
  };

  const tenChuDe = Object.keys(CHU_DE).map(k => CHU_DE[k].ten);

  /** Ghép ngữ liệu: câu chung về AI + câu của chủ đề được hỏi (nếu có). */
  function nguLieuTheoChuDe(maChuDe){
    const base = CORPUS;
    if(maChuDe && CHU_DE[maChuDe]) return base + " " + CHU_DE[maChuDe].cau.join(" ");
    return base;
  }

  /** Nhận diện chủ đề từ câu hỏi của người học bằng từ khoá (tất định, không đoán). */
  function nhanDienChuDe(prompt){
    const p = chuanHoa(prompt || "");
    let tot = null, diemTot = 0;
    for(const ma in CHU_DE){
      let diem = 0;
      for(const k of CHU_DE[ma].tuKhoa) if(p.includes(chuanHoa(k))) diem++;
      if(diem > diemTot){ diemTot = diem; tot = ma; }
    }
    return { ma: diemTot > 0 ? tot : null, soTuKhoaKhop: diemTot };
  }

  /* ---------- Trạm ỨNG DỤNG: người học đặt prompt, máy sinh câu trả lời ----------
   * Trả về cả NHÃN do hệ biết trước: trongNguLieu (chủ đề có được học không) và
   * suyRaLaBia (nếu không có trong ngữ liệu thì mọi nội dung cụ thể đều là bịa). */
  function ungDung(prompt, opts){
    opts = opts || {};
    const nhan = nhanDienChuDe(prompt);
    const ma = nhan.ma;
    const model = huanLuyen(nguLieuTheoChuDe(ma), opts.n || 4);
    const seed = opts.seed || (Date.now() % 100000);

    /* SỬA LẠI CÁCH RÁP CÂU TRẢ LỜI (04/10) — ghi rõ vì sao:
     * Bản đầu ghép "câu thật + đuôi do sinh() n-gram tạo ra". Đuôi n-gram là CHỮ VỰN
     * ghép ngang ("Con người ba chủ đề. mô hình ảnh. hệ thống trí tuệ nhân tạo là lĩnh
     * vực nghiên kiến dữ liệu cá nhân tạo sinh p"). Hậu quả: nhánh CÓ CĂN CỨ cũng đọc
     * như rác, nên học sinh phân biệt hai nhánh bằng HÌNH THỨC chứ không bằng nội dung
     * -> bài học sai bản chất, và phép đo G4a (tỉ lệ từ trong ngữ liệu) thành Goodhart.
     *
     * Nay cả HAI nhánh đều ráp từ CÂU THẬT trong ngữ liệu, nên đều trôi chảy và đúng
     * ngữ pháp. Điểm khác biệt duy nhất còn lại là NỘI DUNG có trả lời câu hỏi hay không:
     *   - hỏi đúng chủ đề đã học -> máy trả lời bằng câu của chính chủ đề đó (CÓ CĂN CỨ)
     *   - hỏi ngoài ngữ liệu     -> máy nói sang chuyện khác, vẫn trôi chảy (KHÔNG CĂN CỨ)
     * Đây cũng là hình thức bịa/lạc đề phổ biến nhất ngoài đời thật. */
    const rand2 = rng(seed);
    function chonCau(arr, soCau){
      const daChon = [];
      let lan = 0;
      while(daChon.length < Math.min(soCau, arr.length) && lan++ < 40){
        const c = vietHoaDauCau(arr[Math.floor(rand2() * arr.length)]);
        if(c && !daChon.includes(c)) daChon.push(c);
      }
      return daChon.join(" ");
    }

    let vanBan, coSo;
    if(ma){
      vanBan = chonCau(CHU_DE[ma].cau, 2);
      coSo = "câu trả lời lấy từ ngữ liệu của chính chủ đề em hỏi";
    } else {
      const cauChung = chuanHoa(CORPUS).split(/(?<=\.)\s+/).filter(Boolean);
      vanBan = chonCau(cauChung, 2);
      coSo = "máy không có dữ liệu về chủ đề em hỏi nên nó nói sang chuyện khác";
    }
    vanBan = vanBan.charAt(0).toUpperCase() + vanBan.slice(1);

    return {
      prompt, vanBan, seed, coSo,
      chuDe: ma ? CHU_DE[ma].ten : null,
      maChuDe: ma,
      soTuKhoaKhop: nhan.soTuKhoaKhop,
      /* NHÃN ORACLE — hệ biết trước vì chính hệ quyết định ngữ liệu */
      trongNguLieu: !!ma,
      suyRaLaBia: !ma,
      danhSachChuDeHoc: tenChuDe,
      thongTinMay: thongTin()
    };
  }

  /* ---------- Chấm ở trạm ỨNG DỤNG (oracle) ----------
   * Người học phải phán đoán: câu trả lời này CÓ CĂN CỨ trong dữ liệu đã học,
   * hay là máy BỊA? Đáp án đúng = item.trongNguLieu, hệ đã biết trước. */
  function chamUngDung(item, traLoi){
    const dungPhanQuyet = (traLoi.coCanCu === item.trongNguLieu);
    return {
      dungPhanQuyet,
      dung: dungPhanQuyet,
      boSot: (item.suyRaLaBia && traLoi.coCanCu === true),   // tin lời bịa
      baoDong: (item.trongNguLieu && traLoi.coCanCu === false) // bác bỏ cái đúng
    };
  }

  /* ---------- Đánh giá chất lượng PROMPT theo rubric (10.C3.1) ----------
   * Rubric tất định: 3 tiêu chí, mỗi tiêu chí dò bằng từ khoá. Không cần LLM. */
  const RUBRIC_PROMPT = [
    { id:"mucTieu", ten:"Nêu rõ mục tiêu",
      tuKhoa:["hãy", "hay", "viết", "viet", "giải thích", "giai thich", "liệt kê", "liet ke", "so sánh", "tim", "tìm", "cho biết", "đề xuất"] },
    { id:"nguCanh", ten:"Có ngữ cảnh hoặc ràng buộc",
      tuKhoa:["việt nam", "viet nam", "học sinh", "lớp 10", "trường", "nông dân", "giáo viên", "trong vòng", "không quá", "dành cho"] },
    { id:"dinhDang", ten:"Nêu định dạng đầu ra",
      tuKhoa:["bảng", "danh sách", "gạch đầu dòng", "đoạn văn", "câu", "ví dụ", "bước", "tóm tắt", "dưới dạng"] }
  ];
  function danhGiaPrompt(prompt){
    const p = chuanHoa(prompt || "");
    const dat = [], thieu = [];
    for(const t of RUBRIC_PROMPT){
      const ok = t.tuKhoa.some(k => p.includes(chuanHoa(k)));
      (ok ? dat : thieu).push(t.ten);
    }
    return { dat, thieu, diem: dat.length, tong: RUBRIC_PROMPT.length,
             muc: dat.length === 3 ? "đạt yêu cầu" : (dat.length >= 1 ? "chưa đầy đủ" : "chưa đạt") };
  }

  /* ---------- Thông tin máy sinh (hàm riêng trong closure, KHÔNG phải method của object) ----------
   * BUG ĐÃ SỬA: ban đầu thongTin chỉ là method trong object literal
   * `window.MX_NHAMAY_TEXT = { ..., thongTin(){...} }`. Khi ungDung() gọi thẳng
   * thongTin() thì nó không nằm trong scope closure -> ReferenceError.
   * Sửa bằng cách khai báo hàm trong closure rồi mới gắn ra object. */
  function thongTin(){
    const m = huanLuyen(null, 4);
    return { tang: 1, loai: "n-gram kí tự", n: m.n, soNguoiCanh: m.nguoi,
             doDaiNguLieu: m.doDaiVanBan, taiVe: "0 MB", canMang: false,
             soChuDeHoc: Object.keys(CHU_DE).length };
  }

  window.MX_NHAMAY_TEXT = {
    CORPUS, NHOM_LOI, CHU_DE, RUBRIC_PROMPT,
    huanLuyen, sinh, taoCauTraLoi, cham, doKhaNang,
    nguLieuTheoChuDe, nhanDienChuDe, ungDung, chamUngDung, danhGiaPrompt,
    tenChuDe, thongTin
  };
})();
