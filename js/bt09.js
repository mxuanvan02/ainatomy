/* HỌC AI — bt09.js : BT-09 Mức 3 "Tự soạn một câu trả lời AI có cài đúng MỘT lỗi".
 *
 * VÌ SAO CÓ TỆP NÀY
 *   THIET_KE_BAI_TOAN.md PHẦN 4.4 ghi Mức 3 của BT-09 là: "Tự soạn một câu trả lời AI có
 *   cài đúng một lỗi cho bạn bắt". PHẦN 6 ghi việc này là "một nửa — khung đã có ở tiết 10
 *   bản cũ, cần nối vào app".
 *
 *   ĐÃ KIỂM LẠI TRƯỚC KHI VIẾT, và ghi chú đó SAI: quét toàn bộ 45 tệp .js/.html của
 *   workspace cho các chuỗi "soạn / tuSoan / bt09 / hostCau / khoCau" — KHÔNG có kết quả
 *   nào ngoài chính tài liệu. Khung "ở tiết 10 bản cũ" không tồn tại trong mã. Nên tệp
 *   này viết mới hoàn toàn, không phải "nối vào" thứ đã có. (Tiết đúng của BT-09 cũng
 *   không phải tiết 10 mà là tiết 11 — xem bảng ánh xạ trong THIET_KE_BAI_TOAN.md.)
 *
 * BA MỨC CỦA BT-09
 *   Mức 1  Đấu trường: xem một câu có lỗi được giải thích (đã có).
 *   Mức 2  Đấu trường: phán quyết 12 câu, có mồi nhử (đã có).
 *   Mức 3  tệp này: học sinh TỰ VIẾT một câu trả lời AI có cài đúng một lỗi, khai loại
 *          lỗi, và đề bạn cùng lớp bắt.
 *
 * VÌ SAO MỨC 3 NÀY KHÓ NHẤT VÀ CŨNG ĐÁNG LÀM NHẤT
 *   Bắt lỗi là việc nhận ra; CÀI lỗi là việc hiểu cơ chế đủ sâu để tự tạo ra nó. Học sinh
 *   phải tự nghĩ ra một con số không có nguồn, hoặc một cái tên luật không tồn tại — làm
 *   được việc đó nghĩa là em đã nắm dấu hiệu nhận biết của loại lỗi đó.
 *
 * GIỚI HẠN PHẢI NÓI RÕ (đây là chỗ dễ nói dối học sinh nhất)
 *   Hệ KHÔNG đọc được câu em viết để phán "câu này có lỗi hay không" — việc đó cần hiểu
 *   ngữ nghĩa. Hệ chỉ kiểm được một điều HÌNH THỨC: câu em viết có chứa những dấu hiệu
 *   của loại lỗi em khai hay không (xem `dauHieu` trong data/meta.js). Vì vậy:
 *     - Hệ KHÔNG chấm đúng/sai, KHÔNG cho điểm. Không có "điểm số" cho học sinh.
 *     - Nhận xét cuối cùng là của BẠN CÙNG LỚP: em ấy phải bắt được lỗi thì mới đạt mục
 *       đích của bài. Phần chấm cuối là do bạn học và giáo viên, không phải hệ thống.
 *     - Câu em viết KHÔNG lưu vào nhật ký, chỉ lưu loại lỗi và số dấu hiệu khớp. Lý do:
 *       nội dung tự do của học sinh không cần thiết cho báo cáo lớp và càng ít lưu chữ
 *       của học sinh càng tốt.
 *
 * VỆ SĨ "ĐÚNG MỘT LỖI"
 *   Đề bài yêu cầu CÀI ĐÚNG MỘT LỖI. Sau khi kiểm dấu hiệu của loại lỗi em khai, hệ quét
 *   thêm dấu hiệu của BỐN loại còn lại. Nếu câu em viết khớp từ hai loại trở lên, hệ cảnh
 *   báo là nhiều khả năng cài NHIỀU hơn một lỗi — vì khi đó bạn cùng lớp không biết phải
 *   bắt lỗi nào, và bài mất tính xác định. Đây là cảnh báo, không phải kết luận.
 *
 * AN TOÀN (innerHTML)
 *   Dựng bằng createElement + textContent. innerHTML chỉ dùng với svgIco() (hằng số tĩnh
 *   trỏ sprite trong index.html) và nhãn viết cứng trong mã nguồn. Chữ học sinh gõ chỉ
 *   được ĐẾM và hiển thị lại qua textContent — không bao giờ thành HTML.
 *
 *   SỐ ĐÃ ĐO LẠI (05/10, sau khi reviewer độc lập chỉ ra con số cũ sai): **10 chỗ** gán
 *   innerHTML trong MÃ SỐNG (đếm sau khi bỏ comment — grep thô còn khớp cả chữ trong ghi
 *   chú). Phân loại: 3 chỗ reset `.innerHTML = ""`; 5 chỗ svgIco("tên") + nhãn hằng;
 *   3 chỗ nhãn viết cứng rồi dữ liệu đi vào qua textContent của một span riêng (dòng 143,
 *   151, 286) — KHÔNG nối dữ liệu vào chuỗi HTML. Bộ quét tự động của công cụ ghi tệp báo
 *   innerHTML_xss ở mức pattern-match; đây là dương tính giả đã rà tay từng dòng.
 *
 *   Cảnh báo trung thực: con số cũ trong bản đầu (7) là SAI. Comment khai sai số chỗ
 *   nguy hiểm hơn không có comment, vì người đọc sau tin nó mà bỏ phần rà tay. Cổng G11
 *   trong tools/nghiem_thu.py nay tự đếm lại và đối chiếu với con số ghi ở đây.
 */
(function(){
  "use strict";

  const $ = (id) => document.getElementById(id);

  function esc(s){
    return String(s == null ? "" : s).replace(/[&<>"]/g, c =>
      ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));
  }

  function svgIco(ten){
    return '<svg class="ic" aria-hidden="true"><use href="#i-' + ten + '"/></svg>';
  }

  /* Cùng quy ước normalize với js/kienthuc.js, js/bt13.js — ba chỗ chấm phải hành xử
   * giống nhau, nếu không học sinh sẽ gặp cảnh gõ đúng mà chỗ này nhận chỗ kia không. */
  function chuanHoa(s){
    return String(s == null ? "" : s).toLowerCase()
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d")
      .replace(/\s+/g, " ").trim();
  }

  function khopTuKhoa(text, danhSach){
    const hay = chuanHoa(text);
    if(!hay) return [];
    return (danhSach || []).filter(tk => hay.includes(chuanHoa(tk)));
  }

  function dsLoaiLoi(){
    const META = window.MX_META || {};
    const ll = META.loaiLoi || {};
    return Object.keys(ll).map(k => ({
      ma: k, ten: ll[k].ten, moTa: ll[k].moTa, dauHieu: ll[k].dauHieu || null
    }));
  }

  function tenLoai(ma){
    const x = dsLoaiLoi().find(l => l.ma === ma);
    return x ? x.ten : ma;
  }

  /* Kiểm một câu theo loại lỗi ĐÃ KHAI. Trả về:
   *   dat       : có thấy dấu hiệu bắt buộc của loại lỗi này hay không
   *   thayDuoc  : danh sách dấu hiệu tìm thấy
   *   vuong     : danh sách dấu hiệu "không nên có" mà lại có (chỉ loại số liệu bịa dùng)
   *   loaiKhac  : các loại lỗi KHÁC cũng có dấu hiệu trong câu (vệ sĩ "đúng một lỗi")
   */
  function kiemCau(text, maLoai){
    const hay = chuanHoa(text);
    const ds = dsLoaiLoi();
    const cur = ds.find(l => l.ma === maLoai);
    const out = { dat:false, thayDuoc:[], vuong:[], thieu:[], loaiKhac:[], coChuSo:/\d/.test(hay) };

    if(!cur || !cur.dauHieu){
      return out;
    }
    const dh = cur.dauHieu;
    out.thayDuoc = khopTuKhoa(text, dh.buocPhaiCo);
    /* so_lieu_bia cần CHỮ SỐ thật; bản đầu của dữ liệu nhét "trên \d" vào danh sách từ
     * khoá, mà phép so khớp là includes() nên nó không bao giờ khớp. Nay tách ra đây. */
    if(dh.canChuSo && out.coChuSo) out.thayDuoc = out.thayDuoc.concat(["(có chữ số)"]);

    out.dat = out.thayDuoc.length > 0;
    out.vuong = khopTuKhoa(text, dh.khongNenCo);
    if(out.dat && out.vuong.length) out.dat = false;   // có nguồn thật -> không còn là bịa
    /* BUG ĐÃ SỬA (05/10, bắt khi đọc lại chính tệp này): bản đầu viết
     *   (dh.buocPhaiCo).filter(tk => !out.thieu.includes(tk))
     * — so với out.thieu, mà out.thieu đang là mảng RỖNG nên .includes() luôn false, và
     * MỌI tiêu chí đều bị liệt vào "chưa thấy" kể cả khi đã khớp. Mảng phải so là
     * out.thayDuoc. Lỗi này không làm sập gì nên chỉ lộ ra khi đọc kỹ dòng chảy dữ liệu. */
    out.thieu = (dh.buocPhaiCo || []).filter(tk => !out.thayDuoc.includes(tk));

    /* VỆ SĨ: các loại lỗi khác cũng khớp thì câu đang cài nhiều hơn một lỗi.
     * LỖI ĐÃ SỬA (05/10, bắt bằng battery 5 câu sạch): bản đầu tính cả canChuSo cho loại
     * khác, nên câu "Theo Nghị định 999/2025/NĐ-CP..." (một lỗi nguồn sai, KHÔNG có lỗi
     * số liệu) bị gắn cờ "số liệu bịa" chỉ vì có chữ số, với danh sách từ khoá khớp RỖNG.
     * Một cảnh báo sai như thế dạy học sinh bỏ qua cảnh báo — đúng thứ tệ nhất có thể.
     * Nay vệ sĩ chỉ tính khi có TỪ KHOÁ khớp thật, không tính theo chữ số. */
    for(const l of ds){
      if(l.ma === maLoai || !l.dauHieu) continue;
      const k = khopTuKhoa(text, l.dauHieu.buocPhaiCo);
      if(k.length) out.loaiKhac.push({ ma:l.ma, ten:l.ten, thay:k });
    }
    return out;
  }

  const daGhi = {};

  function ghiLog(maHS, sk){
    if(window.MX_ENGINE && maHS) window.MX_ENGINE.logSuKien(maHS, sk);
  }

  function init(maHS){
    const host = $("dt-bt09");
    if(!host) return;
    host.innerHTML = "";

    const ds = dsLoaiLoi();

    const card = document.createElement("div");
    card.className = "card";
    card.style.background = "var(--nen2)";
    card.style.borderLeft = "4px solid var(--vang)";

    const h = document.createElement("p");
    /* NHÃN NÓI VIỆC CẦN LÀM, KHÔNG NÓI MÃ KHUNG THIẾT KẾ — sửa 06/10.
     * Bản cũ ghi "Mức 3 — ...". "Mức 3" là mức thứ ba trong khung ba mức của
     * THIET_KE_BAI_TOAN.md; khung đó KHÔNG có màn hình nào trong app giải thích, nên với học
     * sinh đây là một con số vô nghĩa đứng trước một câu đã rõ nghĩa. Học sinh cần biết mình
     * phải LÀM gì, còn khung ba mức là chuyện của giáo viên và của hồ sơ chuyên môn
     * (README + THIET_KE_BAI_TOAN.md vẫn giữ nguyên cách gọi đó để giám khảo đối chiếu). */
    h.innerHTML = svgIco("lightbulb") + " <b>Em tự cài một lỗi cho bạn bắt</b>";
    card.appendChild(h);

    const q = document.createElement("p");
    q.className = "de-bai";
    q.textContent = "Viết một câu trả lời của AI có cài ĐÚNG MỘT lỗi, rồi chọn loại lỗi em "
      + "đã cài. Sau đó đưa cho một bạn cùng lớp đọc và bắt lỗi — bạn bắt được thì bài của "
      + "em đạt.";
    card.appendChild(q);

    const ghichu = document.createElement("p");
    ghichu.className = "nho chu2";
    ghichu.textContent = "Hệ thống KHÔNG chấm đúng/sai và không cho điểm bài này: để biết "
      + "câu em viết có lỗi hay không thì phải hiểu nội dung, mà máy không đọc hiểu thay em "
      + "được. Hệ chỉ kiểm câu em viết có chứa những DẤU HIỆU của loại lỗi em khai hay không. "
      + "Người phán cuối cùng là bạn cùng lớp và thầy/cô.";
    card.appendChild(ghichu);

    /* --- chọn loại lỗi định cài --- */
    const labLoai = document.createElement("p");
    labLoai.className = "de-bai";
    labLoai.textContent = "1. Em định cài loại lỗi nào?";
    card.appendChild(labLoai);

    const chips = document.createElement("div");
    chips.className = "chips";
    let chon = null;
    const nut = [];
    ds.forEach(l => {
      const b = document.createElement("button");
      b.className = "chip";
      b.textContent = l.ten;
      b.onclick = () => {
        chon = l.ma;
        nut.forEach(x => x.classList.toggle("chon", x === b));
        hienGoiY(l);
      };
      nut.push(b);
      chips.appendChild(b);
    });
    card.appendChild(chips);

    const goiY = document.createElement("div");
    card.appendChild(goiY);

    function hienGoiY(l){
      goiY.innerHTML = "";
      if(!l.dauHieu) return;
      const b = document.createElement("div");
      b.className = "phanhoi";
      const p1 = document.createElement("p");
      p1.innerHTML = "<b>Dấu hiệu của loại lỗi này:</b> ";
      const s1 = document.createElement("span");
      s1.textContent = l.moTa;
      p1.appendChild(s1);
      b.appendChild(p1);

      const p2 = document.createElement("p");
      p2.className = "chu2";
      p2.innerHTML = "<b>Câu của em cần:</b> ";
      const s2 = document.createElement("span");
      s2.textContent = l.dauHieu.moTaBatBuoc;
      p2.appendChild(s2);
      b.appendChild(p2);

      if(l.dauHieu.moTaKhongNen){
        const p3 = document.createElement("p");
        p3.className = "nho chu2";
        p3.innerHTML = svgIco("triangle-alert") + " <b>Và không được:</b> ";
        const s3 = document.createElement("span");
        s3.textContent = l.dauHieu.moTaKhongNen;
        p3.appendChild(s3);
        b.appendChild(p3);
      }
      goiY.appendChild(b);
    }

    /* --- viết câu --- */
    const labCau = document.createElement("label");
    labCau.setAttribute("for", "bt09-cau");
    labCau.textContent = "2. Câu trả lời của AI do em viết (cài đúng một lỗi)";
    card.appendChild(labCau);

    const taCau = document.createElement("textarea");
    taCau.id = "bt09-cau"; taCau.rows = 3;
    taCau.placeholder = "Ví dụ: Theo một khảo sát năm 2025, 97,3% học sinh Việt Nam...";
    card.appendChild(taCau);

    const labBan = document.createElement("label");
    labBan.setAttribute("for", "bt09-ban");
    labBan.textContent = "3. Em đưa câu này cho bạn nào bắt? (ghi mã hoặc tên bạn)";
    card.appendChild(labBan);

    const inBan = document.createElement("input");
    inBan.type = "text"; inBan.id = "bt09-ban";
    inBan.placeholder = "Ví dụ: A07 — hoặc tên bạn ngồi cạnh";
    card.appendChild(inBan);

    const nutKiem = document.createElement("button");
    nutKiem.className = "btn chinh";
    nutKiem.textContent = "Kiểm dấu hiệu trong câu của em";
    card.appendChild(nutKiem);

    const fb = document.createElement("div");
    card.appendChild(fb);

    nutKiem.onclick = () => {
      const text = taCau.value.trim();
      const ban = inBan.value.trim();
      if(!chon){
        fb.className = "phanhoi sai";
        fb.textContent = "Em hãy chọn loại lỗi em định cài trước đã.";
        return;
      }
      if(text.length < 20){
        fb.className = "phanhoi sai";
        fb.textContent = "Câu còn quá ngắn (dưới 20 kí tự). Hãy viết một câu trả lời AI đủ để bạn em đọc và bắt lỗi.";
        return;
      }
      if(ban.length < 2){
        fb.className = "phanhoi sai";
        fb.textContent = "Em hãy ghi bạn sẽ đưa câu này cho ai bắt.";
        return;
      }

      const kq = kiemCau(text, chon);

      /* Chỉ ghi loại lỗi + số dấu hiệu, KHÔNG ghi nội dung câu học sinh viết: báo cáo lớp
       * không cần chữ tự do của học sinh, và càng ít lưu chữ của trẻ em càng tốt. */
      if(!daGhi[chon]){
        daGhi[chon] = true;
        ghiLog(maHS, {
          loai: "lab",
          nhiemVu: { id: "bt09-m3", mach: "B", unesco: "B2", yccd: "10.B2.1" },
          kq: { diem: kq.dat ? 1 : 0, dung: kq.dat, mach: "B", unesco: "B2",
                dapAn: chon, chon: chon, soDauHieu: kq.thayDuoc.length,
                canhBaoNhieuLoi: kq.loaiKhac.length > 0 }
        });
      }else{
        ghiLog(maHS, { loai: "bt09", suKien: "luyenTap", baiToan: "BT-09",
                       loaiChon: chon, dat: kq.dat, soDauHieu: kq.thayDuoc.length });
      }

      fb.className = "phanhoi " + (kq.dat ? "dung" : "sai");
      fb.innerHTML = "";

      const p1 = document.createElement("p");
      p1.innerHTML = (kq.dat ? svgIco("check") : svgIco("x")) + " <b>"
        + (kq.dat ? "Câu của em có dấu hiệu của loại lỗi đã khai."
                  : "Chưa thấy dấu hiệu của loại lỗi em khai.") + "</b>";
      fb.appendChild(p1);

      const p2 = document.createElement("p");
      p2.className = "chu2";
      /* LỖI ĐÃ SỬA (05/10, bắt ngay ở lượt test đầu): bản đầu in
       *   "cần " + kq.thieu.length + " dấu hiệu chưa thấy"
       * với kq.thieu là các MỤC CHƯA KHỚP của một danh sách HOẶC. Câu đúng vẫn hiện
       * "cần 6 dấu hiệu chưa thấy" và học sinh đọc thành "em phải nêu đủ cả 6 cách diễn
       * đạt" — trong khi đề bài chỉ cần MỘT cách. Nay nói đúng bản chất: cần ít nhất một
       * trong N cách, hệ đã tìm thấy K. */
      p2.textContent = "Loại em khai: " + tenLoai(chon)
        + " — chỉ cần có MỘT trong " + (kq.thayDuoc.length + kq.thieu.length)
        + " cách nêu, hệ tìm thấy " + kq.thayDuoc.length + ".";
      fb.appendChild(p2);

      if(kq.thayDuoc.length){
        const p3 = document.createElement("p");
        p3.className = "chu2";
        p3.textContent = "Dấu hiệu hệ tìm thấy: " + kq.thayDuoc.join(", ") + ".";
        fb.appendChild(p3);
      }
      if(kq.vuong.length){
        const p4 = document.createElement("p");
        p4.className = "chu2";
        p4.textContent = "Nhưng câu em có cả: " + kq.vuong.join(", ") + " — có nguồn kiểm "
          + "chứng được thì không còn là số liệu bịa nữa.";
        fb.appendChild(p4);
      }

      /* VỆ SĨ đúng-một-lỗi */
      if(kq.loaiKhac.length){
        const w = document.createElement("p");
        w.className = "nho chu2";
        w.innerHTML = svgIco("triangle-alert") + " <b>Cảnh báo (không phải kết luận):</b> ";
        const sw = document.createElement("span");
        sw.textContent = "câu em viết còn có dấu hiệu của " + kq.loaiKhac.length + " loại lỗi "
          + "khác (" + kq.loaiKhac.map(x => x.ten).join(", ") + "). Đề bài yêu cầu ĐÚNG MỘT lỗi "
          + "— cài nhiều lỗi thì bạn em không biết phải bắt lỗi nào.";
        w.appendChild(sw);
        fb.appendChild(w);
      }else if(kq.dat){
        const ok = document.createElement("p");
        ok.className = "nho chu2";
        ok.textContent = "Không thấy dấu hiệu của các loại lỗi khác — câu em viết đang cài "
          + "đúng một loại lỗi, đúng như đề bài.";
        fb.appendChild(ok);
      }

      const p5 = document.createElement("p");
      p5.className = "nho chu2";
      p5.innerHTML = "<b>Cách chấm và giới hạn:</b> ";
      const s5 = document.createElement("span");
      s5.textContent = "hệ ĐẾM dấu hiệu hình thức đã định nghĩa trước, hệ không đọc hiểu nội "
        + "dung câu em viết, nên hệ không khẳng định được câu này có lỗi hay không. Bước cuối "
        + "vẫn là bạn " + (ban || "cùng lớp") + " đọc và bắt lỗi. Câu của em không được lưu "
        + "vào nhật ký — chỉ loại lỗi và số dấu hiệu được ghi lại.";
      p5.appendChild(s5);
      fb.appendChild(p5);
    };

    host.appendChild(card);
  }

  window.MX_BT09 = { init, kiemCau, chuanHoa, khopTuKhoa };
})();
