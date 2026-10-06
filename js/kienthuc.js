/* SOI AI — MODULE KIẾN THỨC NỀN (5 YCCĐ cốt lõi lớp 10 còn thiếu)
 * GHI CHÚ AN TOÀN (innerHTML): app 100% offline/tự host, nội dung lấy từ data/kienthuc.js
 * (hằng số tĩnh của chính sản phẩm). Chuỗi do HS nhập được escape bằng esc() trước khi
 * hiển thị lại, và KHÔNG bao giờ được đưa ra máy khác. Không có vectơ XSS từ mạng.
 *
 * Chấm bài "đặt prompt" (10.C3.2): đối chiếu từ khoá theo rubric đã thiết kế sẵn.
 * Đây là chấm BẰNG TỪ KHOÁ (không phải hiểu ngữ nghĩa) — hồ sơ phải nói rõ giới hạn này:
 * hệ đếm tiêu chí có mặt, GV vẫn là người nhận xét chất lượng diễn đạt.
 */
(function(){
  "use strict";
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]));

  /* Trả về chuỗi SVG nội tuyến trỏ tới một symbol trong sprite của index.html.
   * CHUỖI TĨNH — tên icon do chính mã nguồn này chỉ định, không ghép dữ liệu người
   * dùng, nên dùng bên trong innerHTML là an toàn.
   * Tồn tại để thay emoji: MASTER.md cấm dùng emoji làm biểu tượng vì chúng render
   * khác nhau giữa Windows/macOS/Android và mất nét khi phóng to trên máy chiếu. */
  function svgIco(ten){
    return '<svg class="ic" aria-hidden="true"><use href="#i-' + ten + '"/></svg>';
  }

  function normalize(s){
    return String(s).toLowerCase()
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "")   // bỏ dấu để khớp "giai thich" ~ "giải thích"
      .replace(/đ/g, "d")
      .replace(/\s+/g, " ").trim();
  }

  /* ============ CHẤM PROMPT THEO RUBRIC TỪ KHOÁ ============
   * AN TOÀN: chữ HS nhập CHỈ được dùng để tìm từ khoá, KHÔNG BAO GIỜ được chèn lại
   * vào innerHTML. Phần hiển thị chỉ in ra các từ khoá lấy từ kho từ điển tĩnh
   * (de.tuKhoa trong data/kienthuc.js) và vẫn đi qua esc(). Không có đường nào để
   * input của người dùng trở thành HTML. */
  function chamPrompt(de, text){
    const hay = normalize(text);
    const ketQua = {};
    let datBB = 0, tongBB = de.batBuoc.length;
    const thieu = [], datDuoc = [];
    for(const tieuChi of Object.keys(de.tuKhoa)){
      const danhSach = de.tuKhoa[tieuChi] || [];
      const trung = danhSach.filter(tk => hay.includes(normalize(tk)));
      ketQua[tieuChi] = { dat: trung.length > 0, tuKhoa: trung };
      const tenTC = (window.MX_KT.promptTieuChi.find(t => t.id === tieuChi) || {ten: tieuChi}).ten;
      if(trung.length > 0) datDuoc.push(tenTC); else thieu.push(tenTC);
    }
    for(const bb of de.batBuoc){ if(ketQua[bb] && ketQua[bb].dat) datBB++; }
    const diem = datBB / tongBB;
    return { deId: de.id, diem, datBB, tongBB, ketQua, datDuoc, thieu, doDai: hay.length };
  }

  /* ============ RENDER ============ */
  function veLuat(){
    const box = $("kt-luat"); if(!box) return;
    box.innerHTML = window.MX_KT.luat.map(l => `
      <div class="card" style="background:var(--nen2);margin:10px 0">
        <h3 style="margin-top:0">${esc(l.ten)} <span class="tagline">${esc(l.so)}</span></h3>
        <p class="nho chu2">${esc(l.ngay)}</p>
        <p>${esc(l.baoVe)}</p>
        <p class="vang nho">${svgIco("lightbulb")} Liên hệ với em: ${esc(l.lienHe)}</p>
        <p class="nho chu2">Nguồn tra cứu: ${esc(l.nguon)}</p>
      </div>`).join("");
  }

  function veUngDung(){
    const box = $("kt-ungdung"); if(!box) return;
    box.innerHTML = `<table><tr><th>Nhóm tính năng</th><th>Làm gì</th><th>Ví dụ</th></tr>` +
      window.MX_KT.ungDung.map(u =>
        `<tr><td><b>${esc(u.nhom)}</b></td><td>${esc(u.moTa)}</td><td>${esc(u.viDu)}</td></tr>`
      ).join("") + `</table>
      <p class="nho chu2">Ghi chú: một hệ thống AI thực tế thường kết hợp nhiều nhóm.
      Ứng dụng "SOI AI" này dùng nhóm <b>phân loại</b> (Tầng 1) và mô phỏng đầu ra
      <b>tạo sinh</b> (Tầng 2).</p>`;
  }

  function veSoSanh(){
    const s = window.MX_KT.soSanh; const box = $("kt-sosanh"); if(!box) return;
    box.innerHTML = `<table><tr>${s.cot.map(c=>`<th>${esc(c)}</th>`).join("")}</tr>` +
      s.hang.map(r => `<tr>${r.map((c,i)=>`<td>${i===0?"<b>"+esc(c)+"</b>":esc(c)}</td>`).join("")}</tr>`).join("") +
      `</table><div class="card" style="background:var(--nen2)"><b>Kết luận:</b> ${esc(s.ketLuan)}</div>`;
  }

  function veTieuChiPrompt(){
    const box = $("kt-tieuchi"); if(!box) return;
    box.innerHTML = `<table><tr><th>#</th><th>Tiêu chí của một prompt tốt</th><th>Ví dụ cách viết</th></tr>` +
      window.MX_KT.promptTieuChi.map((t,i) =>
        `<tr><td>${i+1}</td><td><b>${esc(t.ten)}</b><br><code>${t.id}</code></td><td class="nho">${esc(t.viDu)}</td></tr>`
      ).join("") + `</table>`;
  }

  const promptState = {};

  function veBaiTapPrompt(maHS){
    const box = $("kt-prompt"); if(!box) return;
    box.innerHTML = "";
    window.MX_KT.promptDe.forEach((de, idx) => {
      const c = document.createElement("div");
      c.className = "card"; c.style.background = "var(--nen2)";
      c.innerHTML = `
        <h3 style="margin-top:0">Bài ${idx+1}. ${esc(de.ten)}</h3>
        <p class="chu2"><b>Tình huống:</b> ${esc(de.tinhHuong)}</p>
        <p class="nho">${esc(de.goiY)}</p>
        <label for="prompt-in-${de.id}">Prompt của em</label>
        <textarea id="prompt-in-${de.id}" rows="4" placeholder="Viết prompt vào đây..."></textarea>
        <p><button class="btn chinh" id="prompt-cham-${de.id}">Chấm prompt của em</button>
           <span class="nho chu2" id="prompt-count-${de.id}"></span></p>
        <div id="prompt-kq-${de.id}"></div>`;
      box.appendChild(c);

      const ta = c.querySelector(`#prompt-in-${de.id}`);
      const cnt = c.querySelector(`#prompt-count-${de.id}`);
      ta.addEventListener("input", () => { cnt.textContent = ta.value.trim().length + " kí tự"; });

      c.querySelector(`#prompt-cham-${de.id}`).onclick = () => {
        const text = ta.value.trim();
        const kqBox = c.querySelector(`#prompt-kq-${de.id}`);
        if(text.length < 20){
          kqBox.className = "phanhoi sai";
          kqBox.innerHTML = "Prompt còn quá ngắn (dưới 20 kí tự). Hãy viết đầy đủ hơn — việc cần làm, cho ai, dạng kết quả, và điều phải tránh.";
          return;
        }
        const kq = chamPrompt(de, text);
        promptState[de.id] = kq;
        const hang = window.MX_KT.promptTieuChi.map(t => {
          const r = kq.ketQua[t.id];
          const batBuoc = de.batBuoc.includes(t.id);
          return `<tr><td>${esc(t.ten)} ${batBuoc?'<span class="vang">(bắt buộc)</span>':''}</td>
            <td>${r && r.dat ? svgIco("check") + '<span class="ok"> có</span>' : svgIco("x") + '<span class="ko"> thiếu</span>'}</td>
            <td class="nho chu2">${r && r.dat ? esc(r.tuKhoa.slice(0,4).join(", ")) : ""}</td></tr>`;
        }).join("");
        kqBox.className = "phanhoi " + (kq.diem >= 1 ? "dung" : "sai");
        kqBox.innerHTML = `
          <p><b>Kết quả:</b> đạt ${kq.datBB}/${kq.tongBB} tiêu chí bắt buộc
             ${kq.diem >= 1 ? '<span class="ok">— đạt yêu cầu</span>' : '<span class="ko">— chưa đạt</span>'}</p>
          <table><tr><th>Tiêu chí</th><th>Trong prompt của em</th><th>Từ khoá tìm thấy</th></tr>${hang}</table>
          ${kq.thieu.length ? `<p class="ko">Thiếu: ${esc(kq.thieu.join("; "))}</p>` : ""}
          <p class="nho chu2"><b>Giải thích:</b> ${esc(de.giaiThich)}</p>
          <p class="nho chu2"><b>Cách chấm &amp; giới hạn:</b> hệ thống đếm TIÊU CHÍ có mặt trong prompt của em
            bằng cách tìm từ khoá đã định nghĩa trước (không đánh giá diễn đạt hay).
            Thầy/cô sẽ nhận xét thêm về tính hợp lí của cách em diễn đạt.</p>`;
        // ghi log để vào bản đồ năng lực (dùng kênh 'lab', có mã YCCĐ)
        window.MX_ENGINE.logSuKien(maHS, {
          loai: "lab",
          nhiemVu: { id: de.id, mach: "C", unesco: "C2", yccd: "10.C3.2" },
          kq: { diem: kq.diem >= 1 ? 1 : 0, dung: kq.diem >= 1, mach: "C", unesco: "C2",
                dapAn: "đạt " + kq.tongBB + " tiêu chí bắt buộc", chon: "prompt " + kq.doDai + " kí tự" }
        });
      };
    });
  }

  const quizState = {};

  function veQuiz(maHS){
    const box = $("kt-quiz"); if(!box) return;
    box.innerHTML = "";
    window.MX_KT.quiz.forEach((q, idx) => {
      const c = document.createElement("div");
      c.className = "card"; c.style.background = "var(--nen2)";
      c.innerHTML = `<p><b>Câu ${idx+1}.</b> <span class="tagline">${esc(q.yccd || "")}</span><br>${esc(q.cauHoi)}</p>
        <div class="chips" id="kt-chip-${q.id}"></div>
        <div id="kt-fb-${q.id}"></div>`;
      box.appendChild(c);
      const chips = c.querySelector(".chips");
      /* XÁO VỊ TRÍ + chữ cái theo vị trí — xem giải thích ở js/logic.js và js/engine.js.
       * Bản cũ in `l.id.toUpperCase()` nên chữ cái dính chặt với dữ liệu, và tô màu theo
       * `q.luaChon[i]` (thứ tự GỐC) — nếu chỉ xáo chỗ vẽ thì viền đúng/sai sẽ hiện sai ô. */
      const ds = window.MX_ENGINE.xaoLuaChon(q.luaChon, q.id);
      ds.forEach((l, i) => {
        const b = document.createElement("button");
        b.className = "chip"; b.style.textAlign = "left";
        b.innerHTML = `<b>${window.MX_ENGINE.chuCai(i)}.</b> ${esc(l.text)}`;
        b.onclick = () => {
          if(quizState[q.id]) return;
          quizState[q.id] = true;
          const dung = (l.id === q.dapAn);
          [...chips.children].forEach((ch,j) => {
            ch.style.cursor = "default";
            if(ds[j].id === q.dapAn) ch.style.borderColor = "var(--dung)";
            if(ds[j].id === l.id && !dung) ch.style.borderColor = "var(--sai)";
          });
          const fb = document.createElement("div");
          fb.className = "phanhoi " + (dung ? "dung" : "sai");
          fb.innerHTML = (dung ? svgIco("check") + " <b>Chính xác!</b> "
                        : svgIco("x") + " <b>Chưa đúng.</b> ") + esc(q.giaiThich);
          c.querySelector(`#kt-fb-${q.id}`).appendChild(fb);
          window.MX_ENGINE.logSuKien(maHS, {
            loai: "lab",
            nhiemVu: { id: q.id, mach: q.mach, unesco: q.unesco, yccd: q.yccd },
            kq: { diem: dung ? 1 : 0, dung, mach: q.mach, unesco: q.unesco, dapAn: q.dapAn, chon: l.id }
          });
        };
        chips.appendChild(b);
      });
    });
  }

  window.MX_KIEN_THUC = {
    init: function(maHS){
      veLuat(); veUngDung(); veSoSanh(); veTieuChiPrompt();
      veBaiTapPrompt(maHS); veQuiz(maHS);
    },
    chamPrompt
  };
})();
