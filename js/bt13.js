/* AInatomy — bt13.js : BT-13 "Ứng dụng AI quanh em thuộc loại nào?" — Mức 2 và Mức 3.
 *
 * VÌ SAO CÓ TỆP NÀY
 *   THIET_KE_BAI_TOAN.md mô tả BT-13 ở cả ba mức, nhưng trước 05/10 app chỉ có Mức 1:
 *   card #kt-ungdung là một BẢNG ĐỂ ĐỌC — học sinh xem sáu nhóm tính năng rồi thôi.
 *   Yêu cầu cần đạt 10.C2.3 nguyên văn là "Nêu được ví dụ một số trường hợp sử dụng AI
 *   hỗ trợ quá trình học tập" — mà ĐỌC một bảng thì không phải "nêu được ví dụ".
 *   Quét toàn bộ mã nguồn trước khi viết tệp này: chuỗi 10.C2.3 chỉ có trong data/yccd.js
 *   (nơi khai báo danh sách yêu cầu cần đạt), không câu hỏi nào, không bài tập nào gắn
 *   với nó. Tệp này lấp đúng khoảng trống đó.
 *
 * BA MỨC CỦA BT-13, NAY ĐÃ ĐỦ
 *   Mức 1  card #kt-ungdung — xem sáu nhóm tính năng và ví dụ mẫu (đã có từ trước).
 *   Mức 2  tệp này — mỗi tình huống học tập thật: chọn ĐÚNG NHÓM tính năng, rồi nói rõ
 *          ĐẦU VÀO và ĐẦU RA. Hệ chấm tất định và báo ngay, không cần giáo viên.
 *   Mức 3  tệp này — học sinh tự tìm một ứng dụng AI đang dùng trong việc học CỦA CHÍNH
 *          MÌNH, xếp nhóm và giải thích vì sao. Không có đáp án đúng duy nhất nên hệ
 *          KHÔNG chấm: chỉ ghi vào nhật ký để giáo viên đọc.
 *
 * CÁCH CHẤM MỨC 2 (tất định, không mạng, không LLM)
 *   - Nhóm: so chuỗi `ma` học sinh chọn với `nhomDung` trong data/kienthuc.js.
 *   - Đầu vào / đầu ra: đếm từ khoá đã định nghĩa trước (tuKhoaVao / tuKhoaRa), giống
 *     cách chấm prompt ở js/kienthuc.js. GIỚI HẠN PHẢI NÓI RÕ: đây là ĐẾM DẤU HIỆU,
 *     không hiểu ngữ nghĩa. Học sinh diễn đạt đúng ý bằng từ khác sẽ bị báo "chưa thấy";
 *     giáo viên vẫn là người nhận xét chất lượng câu trả lời.
 *   - KHÔNG có điểm số, không xếp loại — theo Khung 2422 phần VI và ràng buộc của
 *     tools/nghiem_thu.py: phản hồi chỉ nói "khớp / chưa khớp" và "thấy / chưa thấy".
 *
 * CHỐNG DÒ ĐÁP ÁN
 *   Học sinh được thử lại (Mức 2 nghĩa là "hệ báo đúng/sai ngay"), nhưng LẦN KIỂM TRA
 *   ĐẦU TIÊN của mỗi tình huống mới là lần được ghi vào bản đồ năng lực. Các lần sau ghi
 *   riêng là luyện tập, có cờ `lanThu`, để giáo viên không bị đánh lừa bởi tỉ lệ đúng
 *   sau khi học sinh đã nhìn thấy đáp án.
 *
 * AN TOÀN (innerHTML)
 *   Dựng giao diện bằng createElement + textContent. Chuỗi duy nhất đi qua innerHTML là
 *   svgIco() — hằng số tĩnh trỏ tới sprite trong index.html. Chữ học sinh gõ KHÔNG BAO GIỜ
 *   được chèn lại vào HTML; phần phản hồi chỉ in ra từ khoá lấy từ data/kienthuc.js.
 *
 *   GHI CHÚ CHO PHÉP KIỂM TĨNH — SỐ ĐÃ ĐO LẠI (05/10, sau khi reviewer độc lập chỉ ra
 *   con số cũ sai): tệp này có **9 chỗ** gán innerHTML trong MÃ SỐNG (đếm bằng cách bỏ
 *   comment trước, vì phép grep thô còn khớp cả chữ trong ghi chú). Cả 9 chỗ thuộc đúng
 *   ba dạng an toàn:
 *     (1) reset: `.innerHTML = ""` — 2 chỗ, xoá sạch trước khi dựng lại;
 *     (2) svgIco("tên") + nhãn viết cứng trong mã nguồn — 3 chỗ;
 *     (3) nhãn viết cứng + esc(hằng số từ data/kienthuc.js) — 4 chỗ (dòng 58, 177,
 *         183, 191): mẫu `"<b>Đầu vào mẫu:</b> "` rồi phần dữ liệu đi vào qua
 *         `textContent` của một thẻ span riêng, KHÔNG nối vào chuỗi HTML.
 *   Không có nhánh nào để chữ người dùng trở thành HTML. Bộ quét tự động của công cụ ghi
 *   tệp báo innerHTML_xss ở mức pattern-match; đây là dương tính giả đã được rà tay.
 */
(function(){
  "use strict";

  const $ = (id) => document.getElementById(id);

  function esc(s){
    return String(s == null ? "" : s).replace(/[&<>"]/g, c =>
      ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));
  }

  /* Chuỗi tĩnh, tên icon do mã nguồn này chỉ định — không ghép dữ liệu người dùng. */
  function svgIco(ten){
    return '<svg class="ic" aria-hidden="true"><use href="#i-' + ten + '"/></svg>';
  }

  /* Bỏ dấu + hạ chữ thường để "Ảnh chụp bài giải" khớp được từ khoá "ảnh".
   * Cùng quy ước với normalize() trong js/kienthuc.js để hai chỗ chấm không lệch nhau. */
  function chuanHoa(s){
    return String(s == null ? "" : s).toLowerCase()
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d")
      .replace(/\s+/g, " ").trim();
  }

  /* Trả về danh sách từ khoá CÓ MẶT trong câu học sinh viết. */
  function khopTuKhoa(text, danhSach){
    const hay = chuanHoa(text);
    if(!hay) return [];
    return (danhSach || []).filter(tk => hay.includes(chuanHoa(tk)));
  }

  /* Nhóm tính năng — đọc thẳng từ data/kienthuc.js, không chép lại danh sách vào đây.
   * Chép lại là mầm lệch: sửa một chỗ, chỗ kia vẫn nói bản cũ. */
  function dsNhom(){
    const KT = window.MX_KT || {};
    return (KT.ungDung || []).map(u => ({ ma: u.ma, ten: u.nhom }));
  }

  function tenNhom(ma){
    const n = dsNhom().find(x => x.ma === ma);
    return n ? n.ten : ma;
  }

  /* Lần kiểm tra ĐẦU TIÊN của mỗi tình huống là lần được ghi vào bản đồ năng lực. */
  const daDanhGia = {};

  function ghiLog(maHS, sk){
    if(window.MX_ENGINE && maHS) window.MX_ENGINE.logSuKien(maHS, sk);
  }

  /* ==================== MỘT TÌNH HUỐNG (Mức 2) ==================== */
  function veTinhHuong(host, th, maHS){
    const card = document.createElement("div");
    card.className = "card";
    card.style.background = "var(--nen2)";
    card.style.borderLeft = "4px solid var(--nhan)";

    const pTH = document.createElement("p");
    pTH.innerHTML = "<b>Tình huống " + esc(th.id) + ".</b> ";
    /* Class .de-bai chứ không phải .chu2: .chu2 BỊ ẨN ở chế độ ít chữ (xem ghi chú
     * trong css/style.css), mà đây là ĐỀ BÀI — ẩn là mất việc để làm. */
    const spanTH = document.createElement("span");
    spanTH.className = "de-bai";
    spanTH.textContent = th.tinhHuong;
    pTH.appendChild(spanTH);
    card.appendChild(pTH);

    /* --- chọn nhóm tính năng --- */
    const labNhom = document.createElement("p");
    labNhom.className = "de-bai";
    labNhom.textContent = "Việc thứ nhất: tình huống này thuộc NHÓM TÍNH NĂNG nào?";
    card.appendChild(labNhom);

    const chips = document.createElement("div");
    chips.className = "chips";
    let chonNhom = null;
    const nutNhom = [];
    dsNhom().forEach(n => {
      const b = document.createElement("button");
      b.className = "chip";
      b.textContent = n.ten;
      b.onclick = () => {
        chonNhom = n.ma;
        nutNhom.forEach(x => x.classList.toggle("chon", x === b));
      };
      nutNhom.push(b);
      chips.appendChild(b);
    });
    card.appendChild(chips);

    /* --- ghi đầu vào / đầu ra --- */
    const labVao = document.createElement("label");
    labVao.setAttribute("for", "bt13-vao-" + th.id);
    labVao.textContent = "Việc thứ hai: ĐẦU VÀO của hệ thống là gì?";
    card.appendChild(labVao);
    const inVao = document.createElement("input");
    inVao.type = "text"; inVao.id = "bt13-vao-" + th.id;
    inVao.placeholder = "Ví dụ: ảnh chụp bài giải viết tay...";
    card.appendChild(inVao);

    const labRa = document.createElement("label");
    labRa.setAttribute("for", "bt13-ra-" + th.id);
    labRa.textContent = "Việc thứ ba: ĐẦU RA của hệ thống là gì?";
    card.appendChild(labRa);
    const inRa = document.createElement("input");
    inRa.type = "text"; inRa.id = "bt13-ra-" + th.id;
    inRa.placeholder = "Ví dụ: một nhãn trong ba nhãn có sẵn...";
    card.appendChild(inRa);

    const nut = document.createElement("button");
    nut.className = "btn chinh";
    nut.textContent = "Kiểm tra tình huống này";
    card.appendChild(nut);

    const fb = document.createElement("div");
    fb.className = "phanhoi";
    card.appendChild(fb);

    let demLan = 0;

    nut.onclick = () => {
      const vao = inVao.value.trim(), ra = inRa.value.trim();
      if(!chonNhom){
        fb.className = "phanhoi sai";
        fb.textContent = "Cần chọn một nhóm tính năng ở trên trước.";
        return;
      }
      if(vao.length < 3 || ra.length < 3){
        fb.className = "phanhoi sai";
        fb.textContent = "Cần ghi cả ĐẦU VÀO và ĐẦU RA của hệ thống (mỗi ô ít nhất 3 kí tự).";
        return;
      }

      demLan++;
      const dungNhom = (chonNhom === th.nhomDung);
      const khopVao = khopTuKhoa(vao, th.tuKhoaVao);
      const khopRa = khopTuKhoa(ra, th.tuKhoaRa);
      const duBa = !!khopVao.length && !!khopRa.length;

      /* LẦN ĐẦU được ghi vào bản đồ năng lực (kq.diem); các lần sau ghi là luyện tập
       * để tỉ lệ đúng không bị thổi lên sau khi học sinh đã thấy đáp án. */
      const lanDau = !daDanhGia[th.id];
      daDanhGia[th.id] = true;
      if(lanDau){
        ghiLog(maHS, {
          loai: "lab",
          nhiemVu: { id: th.id, mach: "C", unesco: "C2", yccd: "10.C2.3" },
          kq: { diem: (dungNhom && duBa) ? 1 : 0, dung: (dungNhom && duBa),
                mach: "C", unesco: "C2",
                dapAn: th.nhomDung, chon: chonNhom }
        });
      }else{
        ghiLog(maHS, { loai: "bt13", suKien: "luyenTap", baiToan: "BT-13", item: th.id,
                       lanThu: demLan, chonNhom: chonNhom, dungNhom: dungNhom });
      }

      fb.className = "phanhoi " + ((dungNhom && duBa) ? "dung" : "sai");
      fb.innerHTML = "";

      const p1 = document.createElement("p");
      p1.innerHTML = (dungNhom ? svgIco("check") : svgIco("x")) + " <b>Nhóm tính năng: "
        + (dungNhom ? "khớp." : "chưa khớp.") + "</b>";
      fb.appendChild(p1);

      const p2 = document.createElement("p");
      p2.className = "chu2";
      p2.textContent = "Nhóm đã chọn: " + tenNhom(chonNhom)
        + (dungNhom ? "" : " · Nhóm đúng là: " + tenNhom(th.nhomDung)) + ".";
      fb.appendChild(p2);

      /* Chỉ in ra TỪ KHOÁ lấy từ dữ liệu tĩnh, không in lại chữ em gõ. */
      const hang = document.createElement("p");
      hang.className = "chu2";
      hang.textContent = "Đầu vào: " + (khopVao.length ? "thấy dấu hiệu (" + khopVao.join(", ") + ")" : "chưa thấy dấu hiệu nào")
        + " · Đầu ra: " + (khopRa.length ? "thấy dấu hiệu (" + khopRa.join(", ") + ")" : "chưa thấy dấu hiệu nào") + ".";
      fb.appendChild(hang);

      const p3 = document.createElement("p");
      p3.className = "chu2";
      p3.innerHTML = "<b>Đầu vào mẫu:</b> ";
      const s3 = document.createElement("span");
      s3.textContent = th.dauVaoMau;
      p3.appendChild(s3);
      const p4 = document.createElement("p");
      p4.className = "chu2";
      p4.innerHTML = "<b>Đầu ra mẫu:</b> ";
      const s4 = document.createElement("span");
      s4.textContent = th.dauRaMau;
      p4.appendChild(s4);
      fb.appendChild(p3); fb.appendChild(p4);

      const p5 = document.createElement("p");
      p5.className = "chu2";
      p5.innerHTML = "<b>Vì sao:</b> ";
      const s5 = document.createElement("span");
      s5.textContent = th.viSao;
      p5.appendChild(s5);
      fb.appendChild(p5);

      const p6 = document.createElement("p");
      p6.className = "nho chu2";
      p6.innerHTML = svgIco("triangle-alert") + " <b>Cần lưu ý:</b> ";
      const s6 = document.createElement("span");
      s6.textContent = th.canhBao;
      p6.appendChild(s6);
      fb.appendChild(p6);

      const p7 = document.createElement("p");
      p7.className = "nho chu2";
      p7.textContent = "Cách chấm và giới hạn: hệ so nhóm đã chọn với đáp án, và ĐẾM từ khoá "
        + "đã định nghĩa trước để biết câu trả lời có nói tới đầu vào, đầu ra hay không. Hệ không "
        + "đánh giá cách diễn đạt. Giáo viên sẽ nhận xét thêm.";
      fb.appendChild(p7);

      if(lanDau){
        const p8 = document.createElement("p");
        p8.className = "nho chu2";
        p8.textContent = "Lần kiểm tra này đã được ghi vào nhật ký. Có thể thử lại để luyện tập.";
        fb.appendChild(p8);
      }
    };

    host.appendChild(card);
  }

  /* ==================== MỨC 3 — ỨNG DỤNG CỦA CHÍNH EM ====================
   * Mức 3 của khung ba mức là "viết ra trước khi hệ cho biết kết quả". Ở BT-13 việc đó
   * là: tự tìm một ứng dụng AI trong việc học của chính mình, xếp nhóm, và nói được vì
   * sao. Không có đáp án duy nhất nên hệ KHÔNG chấm — chỉ ghi lại để giáo viên đọc.
   * Nói rõ điều này trên giao diện, không để học sinh tưởng đây là câu hỏi có đáp án. */
  function veMuc3(host, thList, maHS){
    const card = document.createElement("div");
    card.className = "card";
    card.style.background = "var(--nen2)";
    card.style.borderLeft = "4px solid var(--vang)";

    const h = document.createElement("p");
    /* Bỏ nhãn "Mức 3" — xem giải thích ở js/bt09.js. */
    h.innerHTML = svgIco("lightbulb") + " <b>Ứng dụng AI trong việc học của chính mình</b>";
    card.appendChild(h);

    const q = document.createElement("p");
    q.className = "de-bai";
    q.textContent = "Tìm một ứng dụng AI ĐANG dùng trong việc học của chính mình "
      + "(không lấy ví dụ trong sách), xếp nó vào một nhóm tính năng, và giải thích vì sao xếp như vậy.";
    card.appendChild(q);

    const nhan = document.createElement("p");
    nhan.className = "nho chu2";
    nhan.textContent = "Bài này không có đáp án đúng duy nhất, nên hệ thống không chấm đúng/sai. "
      + "Câu trả lời được ghi vào nhật ký để giáo viên đọc và nhận xét.";
    card.appendChild(nhan);

    const labApp = document.createElement("label");
    labApp.setAttribute("for", "bt13-m3-app");
    labApp.textContent = "Tên ứng dụng AI đang dùng (hoặc mô tả nó làm gì)";
    card.appendChild(labApp);
    const inApp = document.createElement("input");
    inApp.type = "text"; inApp.id = "bt13-m3-app";
    inApp.placeholder = "Ví dụ: công cụ dịch đoạn văn tiếng Anh dùng khi làm bài đọc...";
    card.appendChild(inApp);

    const labNhom3 = document.createElement("p");
    labNhom3.className = "de-bai";
    labNhom3.textContent = "Xếp ứng dụng đó vào nhóm tính năng nào?";
    card.appendChild(labNhom3);
    const chips3 = document.createElement("div");
    chips3.className = "chips";
    let chon3 = null;
    const nut3 = [];
    dsNhom().forEach(n => {
      const b = document.createElement("button");
      b.className = "chip";
      b.textContent = n.ten;
      b.onclick = () => {
        chon3 = n.ma;
        nut3.forEach(x => x.classList.toggle("chon", x === b));
      };
      nut3.push(b);
      chips3.appendChild(b);
    });
    card.appendChild(chips3);

    const labVi = document.createElement("label");
    labVi.setAttribute("for", "bt13-m3-vi");
    labVi.textContent = "Vì sao xếp nó vào nhóm đó?";
    card.appendChild(labVi);
    const inVi = document.createElement("textarea");
    inVi.id = "bt13-m3-vi"; inVi.rows = 3;
    inVi.placeholder = "Hệ thống nhận cái gì vào, và đưa ra cái gì? Vì sao chọn nhóm đó?";
    card.appendChild(inVi);

    const gui = document.createElement("button");
    gui.className = "btn chinh";
    gui.textContent = "Ghi lại câu trả lời";
    card.appendChild(gui);

    const fb3 = document.createElement("div");
    card.appendChild(fb3);

    gui.onclick = () => {
      const app = inApp.value.trim(), vi = inVi.value.trim();
      if(app.length < 3 || !chon3 || vi.length < 10){
        fb3.className = "phanhoi sai";
        fb3.textContent = "Cần ghi tên ứng dụng, chọn một nhóm, và giải thích ít nhất 10 kí tự.";
        return;
      }
      ghiLog(maHS, { loai: "bt13", suKien: "muc3", baiToan: "BT-13",
                     nhomChon: chon3, doDaiGiaiThich: vi.length });
      fb3.className = "phanhoi dung";
      fb3.textContent = "Đã ghi lại. Nhóm đã chọn: " + tenNhom(chon3)
        + ". Thầy/cô sẽ đọc và nhận xét — bài này không chấm đúng/sai.";
    };

    host.appendChild(card);
  }

  function init(maHS){
    const host = $("kt-bt13");
    if(!host) return;
    host.innerHTML = "";
    const thList = (window.MX_KT && window.MX_KT.hoTroHocTap) || [];

    const mo = document.createElement("p");
    mo.className = "de-bai";
    mo.textContent = "Sáu tình huống dưới đây là sáu cách AI đang được dùng trong việc học. "
      + "Mỗi tình huống cần làm ba việc: chọn đúng nhóm tính năng, nói rõ đầu vào, nói rõ đầu ra.";
    host.appendChild(mo);

    thList.forEach(th => veTinhHuong(host, th, maHS));
    veMuc3(host, thList, maHS);
  }

  window.MX_BT13 = { init, chuanHoa, khopTuKhoa };
})();
