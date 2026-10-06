/* SOI AI — MODULE "LÔGIC & AI"
 * Cầu nối trực tiếp với Bài 5 Tin học 10 "Dữ liệu lôgic" (KNTT & CTST, Chủ đề 1, 2 tiết).
 * Ý tưởng sư phạm: toàn bộ luật chơi của "Đấu trường bắt lỗi AI" VỐN LÀ một biểu thức lôgic.
 * Vì vậy dạy Bài 5 không cần ví dụ xa lạ — dùng chính kết quả của học sinh làm vật liệu.
 *
 * Ánh xạ Bài 5 → sản phẩm:
 *   Giá trị chân lí (TRUE/FALSE)  → phán quyết "Có lỗi / Không có lỗi"
 *   Phép AND                      → "Câu trả lời AI ĐÚNG" = (c1 ĐÚNG) AND (c2 ĐÚNG) AND (c3 ĐÚNG)
 *   Phép OR                       → "Có lỗi" = (c1 SAI) OR (c2 SAI) OR (c3 SAI)
 *   Phép NOT                      → đảo phán quyết: NOT(Có lỗi) = Không có lỗi
 *   Bảng chân lí                  → BẢNG NHẦM LẪN của chính học sinh (bắt đúng/bắt oan/bỏ sót/xác nhận đúng)
 *   Biểu diễn dữ liệu lôgic       → perceptron: z = w·x + b, nếu z ≥ 0 thì TRUE (có mũ)
 */
(function(){
  "use strict";

  const $ = (id) => document.getElementById(id);

  /* ============ 1. BẢNG CHÂN LÍ TƯƠNG TÁC ============ */
  const opState = { a: true, b: false, n: true };

  function veDen(el, on){
    el.textContent = on ? "TRUE (1)" : "FALSE (0)";
    el.className = "den " + (on ? "on" : "off");
  }

  function capNhatPhep(){
    const { a, b, n } = opState;
    $("out-and").textContent = String(a && b);
    $("out-or").textContent  = String(a || b);
    $("out-not").textContent = String(!n);
    $("in-a").textContent = a ? "TRUE" : "FALSE";
    $("in-b").textContent = b ? "TRUE" : "FALSE";
    $("in-n").textContent = n ? "TRUE" : "FALSE";
    ["and","or"].forEach(k=>{
      const val = k==="and" ? (a&&b) : (a||b);
      $("lamp-"+k) && veDen($("lamp-"+k), val);
    });
    $("lamp-not") && veDen($("lamp-not"), !n);
    // dòng biểu thức
    $("expr-and").textContent = `${a?1:0} AND ${b?1:0} = ${(a&&b)?1:0}`;
    $("expr-or").textContent  = `${a?1:0} OR ${b?1:0} = ${(a||b)?1:0}`;
    $("expr-not").textContent = `NOT ${n?1:0} = ${(!n)?1:0}`;
  }

  function ganNut(){
    const toggle = (id, key) => {
      const el = $(id);
      if(!el) return;
      el.onclick = () => { opState[key] = !opState[key]; capNhatPhep(); };
    };
    toggle("sw-a","a"); toggle("sw-b","b"); toggle("sw-n","n");
  }

  /* ============ 2. LUẬT CHƠI = MỘT BIỂU THỨC LÔGIC ============ */
  function veBieuThuc(){
    const box = $("logic-bieuthuc");
    if(!box) return;
    box.innerHTML = `
      <p><b>Câu trả lời của trợ lý AI gồm 3 câu (claim).</b> Gọi giá trị chân lí của mỗi câu là
      <code>c1, c2, c3</code> (TRUE = câu đó đúng).</p>
      <div class="ai-box" style="border-left-color:var(--dung)">
        <b>Câu trả lời AI là ĐÚNG</b> ⟺ <code>c1 AND c2 AND c3</code><br>
        <span class="nho chu2">Chỉ cần MỘT câu sai → phép AND cho FALSE → cả câu trả lời là sai.
        Đó là lí do trong Đấu trường em chỉ cần tìm đúng 1 câu có lỗi.</span>
      </div>
      <div class="ai-box" style="border-left-color:var(--sai)">
        <b>Câu trả lời AI CÓ LỖI</b> ⟺ <code>(NOT c1) OR (NOT c2) OR (NOT c3)</code><br>
        <span class="nho chu2">Phép OR: có lỗi nếu câu 1 sai HOẶC câu 2 sai HOẶC câu 3 sai.</span>
      </div>
      <div class="ai-box" style="border-left-color:var(--vang)">
        <b>Phán quyết của em</b> là một biến lôgic: <code>P = TRUE</code> nghĩa là "Có lỗi".<br>
        <span class="nho chu2">Đảo phán quyết bằng phép NOT: <code>NOT P</code> = "Không có lỗi".</span>
      </div>
      <table>
        <tr><th>c1</th><th>c2</th><th>c3</th><th>c1 AND c2 AND c3</th><th>AI đúng?</th><th>Em phải phán quyết</th></tr>
        <tr><td>T</td><td>T</td><td>T</td><td>TRUE</td><td class="ok">Đúng</td><td>Không có lỗi</td></tr>
        <tr><td>T</td><td>T</td><td><b>F</b></td><td>FALSE</td><td class="ko">Sai</td><td>Có lỗi</td></tr>
        <tr><td>T</td><td><b>F</b></td><td>T</td><td>FALSE</td><td class="ko">Sai</td><td>Có lỗi</td></tr>
        <tr><td><b>F</b></td><td>T</td><td>T</td><td>FALSE</td><td class="ko">Sai</td><td>Có lỗi</td></tr>
        <tr><td>F</td><td>F</td><td>F</td><td>FALSE</td><td class="ko">Sai</td><td>Có lỗi</td></tr>
      </table>
      <p class="nho chu2">Nhận xét: với phép AND, <b>chỉ 1/5 dòng</b> cho kết quả TRUE.
      Một câu trả lời AI "nghe rất hợp lí" vẫn sai nếu chỉ một chi tiết bịa — đây chính là
      kĩ năng kiểm chứng thông tin mà Khung giáo dục AI (QĐ 2422/QĐ-BGDĐT) yêu cầu rèn luyện.</p>`;
  }

  /* ============ 3. BẢNG NHẦM LẪN TỪ CHÍNH DỮ LIỆU CỦA HS ============ */
  function veBangNhamLan(maHS){
    const box = $("logic-nhamlan");
    if(!box) return;
    const bl = window.MX_ENGINE.bangNhamLan(maHS);
    if(!bl.tong){
      box.innerHTML = `<p class="chu2">Chưa có dữ liệu. Em hãy vào <b>Đấu trường bắt lỗi AI</b>
        làm vài câu rồi quay lại đây — bảng này sẽ hiện chính kết quả của em dưới dạng bảng chân lí.</p>`;
      return;
    }
    const tp = bl.TP, fp = bl.FP, fn = bl.FN, tn = bl.TN;
    box.innerHTML = `
      <p>Đặt <code>T</code> = "thật sự CÓ lỗi", <code>P</code> = "em phán quyết CÓ lỗi".
      Bốn ô dưới đây là <b>bảng chân lí của chính em</b> (${bl.tong} câu đã làm):</p>
      <table>
        <tr><th></th><th>Thật sự CÓ lỗi (T)</th><th>Thật sự ĐÚNG (NOT T)</th></tr>
        <tr>
          <th>Em nói "Có lỗi" (P)</th>
          <td class="ok"><b>${tp}</b> — bắt đúng<br><span class="nho">P AND T = TRUE (true positive)</span></td>
          <td class="vang"><b>${fp}</b> — bắt oan<br><span class="nho">P AND (NOT T) (false positive)</span></td>
        </tr>
        <tr>
          <th>Em nói "Không lỗi" (NOT P)</th>
          <td class="ko"><b>${fn}</b> — bỏ sót<br><span class="nho">(NOT P) AND T (false negative)</span></td>
          <td class="ok"><b>${tn}</b> — xác nhận đúng<br><span class="nho">(NOT P) AND (NOT T) (true negative)</span></td>
        </tr>
      </table>
      <div class="grid g3" style="margin-top:10px">
        <div class="kpi"><div class="so">${pct(bl.tiLeDung)}</div><div class="nhan">phán quyết đúng<br>(TP+TN) / tổng</div></div>
        <div class="kpi"><div class="so ko">${bl.tiLeBoSot===null?"—":pct(bl.tiLeBoSot)}</div><div class="nhan">tỉ lệ bỏ sót<br>FN / (TP+FN)</div></div>
        <div class="kpi"><div class="so vang">${bl.tiLeBatOan===null?"—":pct(bl.tiLeBatOan)}</div><div class="nhan">tỉ lệ bắt oan<br>FP / (FP+TN)</div></div>
      </div>
      <p class="nho chu2" style="margin-top:10px"><b>Vì sao "bắt oan" nguy hiểm hơn "bỏ sót" trong đời thật?</b>
      Một hệ thống AI từ chối hồ sơ của người vô tội (false positive) gây hại trực tiếp cho người đó.
      Học sinh thấy con số của chính mình nên hiểu được đánh đổi này — đây là nội dung mạch
      <i>Đạo đức AI</i> và <i>Tư duy lấy con người làm trung tâm</i> của Khung QĐ 2422.</p>`;
  }

  const pct = (x) => x===null||x===undefined ? "—" : Math.round(x*100)+"%";

  /* ============ 4. PERCEPTRON = MÁY TÍNH GIÁ TRỊ CHÂN LÍ CÓ TRỌNG SỐ ============ */
  function vePerceptron(){
    const box = $("logic-perceptron");
    if(!box) return;
    box.innerHTML = `
      <p>Ở <b>Xưởng huấn luyện AI</b>, mô hình quyết định "có mũ bảo hiểm hay không" bằng một
      <b>giá trị chân lí có trọng số</b>:</p>
      <div class="ai-box"><code>z = w₁·x₁ + w₂·x₂ + w₃·x₃ + w₄·x₄ + b</code><br>
      <b>nếu z ≥ 0 → TRUE (có mũ)</b>, ngược lại → FALSE (không mũ)</div>
      <p>Với <code>x</code> là các đặc trưng của ảnh (tỉ lệ điểm ảnh rất sáng ở vùng đầu, độ sáng vùng đầu, tỉ lệ ảnh tối...),
      <code>w</code> là trọng số mô hình <b>học được</b> từ dữ liệu.</p>
      <p class="vang"><b>Điểm mấu chốt của bài học:</b> dấu "<code>z ≥ 0</code>" là một <b>phép so sánh lôgic</b>.
      Bên trong mọi hệ thống AI phân loại đều là: tính một con số, rồi biến nó thành TRUE/FALSE.
      Vì vậy khi dữ liệu huấn luyện lệch (toàn ảnh ban ngày), trọng số <code>w</code> học sai
      → phép so sánh cho FALSE hàng loạt với ảnh ban đêm.</p>
      <p class="nho chu2">So sánh với Bài 5: biểu thức lôgic thông thường do con người viết ra và luôn đúng như nhau;
      còn biểu thức trong AI có <b>trọng số học từ dữ liệu</b> — nên nó có thể sai, và sai có hệ thống.
      Đó là lí do cần người kiểm định.</p>`;
  }

  /* ============ 5. BÀI TẬP VẬN DỤNG (Bài 5) ============
   * GHI CHÚ AN TOÀN (innerHTML): app 100% offline, nội dung lấy từ data/bai5_logic.js
   * (hằng số tĩnh của chính sản phẩm). Chuỗi động đều đi qua esc() trước khi chèn.
   * Không có input từ mạng/người dùng → không có vectơ XSS. */
  const btState = {};   // id -> true (đã trả lời)

  function veBaiTap(maHS){
    const box = $("logic-baitap");
    if(!box) return;
    const ds = window.MX_BAI5 || [];
    box.innerHTML = "";
    ds.forEach((bt, idx)=>{
      const c = document.createElement("div");
      c.className = "card";
      c.style.background = "var(--nen2)";
      c.innerHTML = `<p><b>Câu ${idx+1}.</b> ${esc(bt.cauHoi).replace(/\n/g,"<br>")}</p>
        <div class="chips" id="bt-chip-${bt.id}"></div>
        <div id="bt-fb-${bt.id}"></div>`;
      box.appendChild(c);
      const chips = c.querySelector(".chips");
      /* XÁO VỊ TRÍ + CHỮ CÁI THEO VỊ TRÍ (06/10). Hai lỗi phải sửa CÙNG LÚC:
       * (1) thứ tự phương án cố định trong dữ liệu;
       * (2) chữ cái in ra lấy từ `l.id` — tức nhãn cố định. Nếu chỉ xáo thứ tự mà vẫn in
       *     l.id thì đáp án vẫn luôn hiện chữ B, học sinh vẫn "luôn bấm B" được.
       * Nên chữ cái phải sinh theo VỊ TRÍ sau khi xáo (MX_ENGINE.chuCai), còn `l.id` chỉ
       * dùng để so với bt.dapAn và ghi log. Chi tiết: js/engine.js hàm xaoLuaChon. */
      const ds = window.MX_ENGINE.xaoLuaChon(bt.luaChon, bt.id);
      ds.forEach((l,i)=>{
        const b = document.createElement("button");
        b.className = "chip";
        b.innerHTML = `<b>${window.MX_ENGINE.chuCai(i)}.</b> ${esc(l.text)}`;
        b.style.textAlign = "left";
        b.onclick = ()=>{
          if(btState[bt.id]) return;
          btState[bt.id] = true;
          const dung = (l.id === bt.dapAn);
          [...chips.children].forEach((ch,j)=>{
            ch.style.cursor = "default";
            if(ds[j].id === bt.dapAn) ch.style.borderColor = "var(--dung)";
            if(ds[j].id === l.id && !dung) ch.style.borderColor = "var(--sai)";
          });
          const fb = document.createElement("div");
          fb.className = "phanhoi " + (dung ? "dung" : "sai");
          fb.innerHTML = (dung ? svgIco("check") + " <b>Chính xác!</b> "
                        : svgIco("x") + " <b>Chưa đúng.</b> ") + esc(bt.giaiThich);
          c.querySelector(`#bt-fb-${bt.id}`).appendChild(fb);
          // ghi log như một nhiệm vụ (dùng chung kênh 'lab' để vào bản đồ năng lực)
          window.MX_ENGINE.logSuKien(maHS, {
            loai: "lab",
            nhiemVu: { id: bt.id, mach: bt.mach, unesco: bt.unesco },
            kq: { diem: dung?1:0, dung: dung, mach: bt.mach, unesco: bt.unesco, dapAn: bt.dapAn, chon: l.id }
          });
        };
        chips.appendChild(b);
      });
    });
  }

  const esc = (s) => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]));

  /* Trả về chuỗi SVG nội tuyến trỏ tới một symbol trong sprite của index.html.
   * CHUỖI TĨNH — tên icon do chính mã nguồn này chỉ định, không ghép dữ liệu người
   * dùng, nên dùng bên trong innerHTML là an toàn.
   * Tồn tại để thay emoji: MASTER.md cấm dùng emoji làm biểu tượng vì chúng render
   * khác nhau giữa Windows/macOS/Android và mất nét khi phóng to trên máy chiếu. */
  function svgIco(ten){
    return '<svg class="ic" aria-hidden="true"><use href="#i-' + ten + '"/></svg>';
  }

  /* ============ KHỞI ĐỘNG MODULE ============ */
  window.MX_LOGIC = {
    init: function(maHS){
      ganNut(); capNhatPhep(); veBieuThuc(); vePerceptron(); veBangNhamLan(maHS); veBaiTap(maHS);
    },
    capNhatNhamLan: veBangNhamLan
  };
})();
