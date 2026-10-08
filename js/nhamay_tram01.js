/* AInatomy — nhamay_tram01.js : TRẠM 0 (NHẬP LIỆU) + TRẠM 1 (DÁN NHÃN) của nhà máy.
 *
 * VÌ SAO HAI TRẠM NÀY TỒN TẠI
 * Bản đầu của nhà máy để trống Trạm 0 và Trạm 1 ("đang xây dựng"), nghĩa là học sinh
 * bước vào dây chuyền ở khâu HUẤN LUYỆN mà chưa từng thấy nguyên liệu. Hai yêu cầu cần
 * đạt của lớp 10 bị bỏ trống vì vậy:
 *   10.C4.MR1  Phân tích được các dạng dữ liệu (hình ảnh, âm thanh, từ ngữ, …)
 *              được sử dụng để huấn luyện AI.
 *   10.C4.1    Phân tích được sự ảnh hưởng của CHẤT LƯỢNG dữ liệu đến chất lượng AI.
 * Trạm 1 là chỗ dạy 10.C4.1 sắc nhất: chính học sinh dán nhãn sai, rồi nhìn thấy mô hình
 * học sai theo một cách có hệ thống. Không ai phải tin lời giảng — con số tự nói.
 *
 * NGUYÊN TẮC ORACLE (giữ như mọi trạm khác)
 *   Trạm 0: câu hỏi có nhãn cứng.
 *   Trạm 1: nhãn đúng của ảnh do hệ sinh ra nên hệ biết trước; tỉ lệ nhãn sai của học
 *           sinh đo được trực tiếp, và mô hình huấn luyện trên nhãn của học sinh rồi
 *           đánh giá trên nhãn thật -> chênh lệch là hệ quả tất định, không cần ai chấm.
 *
 * TÁI DÙNG: ảnh và đặc trưng lấy từ MX_LAB.veXeMay / dacTrung / Perceptron (đã kiểm chứng
 * ở Tầng 1), nên hai trạm dùng CHUNG một nguồn dữ liệu với phần còn lại của nhà máy.
 *
 * AN TOÀN: mọi chuỗi do hệ sinh ra đều đi qua esc() trước khi vào innerHTML; nội dung
 * câu hỏi là hằng số trong tệp này.
 */
(function(){
  "use strict";

  const L = () => window.MX_LAB;

  function esc(s){
    return String(s == null ? "" : s).replace(/[&<>"]/g, c =>
      ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));
  }

  /* Trả về chuỗi SVG nội tuyến trỏ tới một symbol trong sprite của index.html.
   * CHUỖI TĨNH — tên icon do chính mã nguồn chỉ định, không ghép dữ liệu người dùng,
   * nên dùng bên trong innerHTML là an toàn. Dữ liệu động vẫn đi qua esc().
   * Tồn tại để thay emoji: MASTER.md cấm dùng emoji làm biểu tượng vì chúng render
   * khác nhau giữa Windows/macOS/Android và mất nét khi phóng to trên máy chiếu. */
  function svgIco(ten){
    return '<svg class="ic" aria-hidden="true"><use href="#i-' + ten + '"/></svg>';
  }
  const $ = id => document.getElementById(id);

  /* ======================================================================
   * TRẠM 0 — NHẬP LIỆU: ba dạng dữ liệu, mở nắp xem AI đọc được gì
   * ====================================================================== */

  /* Ngân hàng câu hỏi Trạm 0 — nhãn cứng, hệ tự chấm. */
  const CAU_HOI_T0 = [
    { id:"t0-1", mach:"C", chuDe:"C4", yccd:"10.C4.MR1",
      cau:"Máy tính KHÔNG đọc được bức ảnh như con người. Vậy nó đọc cái gì?",
      luaChon:[
        {id:"a", text:"Nó nhìn thấy chiếc mũ bảo hiểm và hiểu đó là mũ."},
        {id:"b", text:"Nó đọc một dãy SỐ đo từ ảnh, ví dụ tỉ lệ điểm ảnh rất sáng, tỉ lệ điểm ảnh sáng vừa, độ sáng vùng đầu."},
        {id:"c", text:"Nó tra cứu trên Internet xem ảnh này chụp ở đâu."},
        {id:"d", text:"Nó đọc chú thích ảnh do người chụp viết."}],
      dapAn:"b",
      giaiThich:"Đúng. Ảnh với máy chỉ là các con số. Ở trạm này có thể thấy tận mắt bốn đặc trưng được trích từ mỗi ảnh — tỉ lệ điểm ảnh RẤT SÁNG, tỉ lệ điểm ảnh SÁNG VỪA, độ sáng vùng đầu, và tỉ lệ điểm tối. Toàn bộ việc học diễn ra trên bốn con số đó, không có 'cái nhìn' nào cả."},
    { id:"t0-2", mach:"C", chuDe:"C4", yccd:"10.C4.MR1",
      cau:"Ba dạng dữ liệu dưới đây, dạng nào KHÔNG dùng được để huấn luyện một mô hình nhận diện mũ bảo hiểm từ ảnh?",
      luaChon:[
        {id:"a", text:"Ảnh chụp người đi xe máy."},
        {id:"b", text:"Các con số đo độ sáng trích từ ảnh."},
        {id:"c", text:"Bản nhạc nền của video quay cảnh giao thông."},
        {id:"d", text:"Nhãn 'có mũ' hoặc 'không mũ' gắn cho từng ảnh."}],
      dapAn:"c",
      giaiThich:"Đúng. Âm thanh là một dạng dữ liệu huấn luyện AI hợp lệ nói chung (nhận diện tiếng nói, phân loại âm thanh), nhưng nó không mang thông tin gì về việc có đội mũ hay không. Chọn dữ liệu là một quyết định của con người, và chọn sai thì mô hình không thể học được điều cần học — đây là mạch A, tư duy lấy con người làm trung tâm."},
    { id:"t0-3", mach:"C", chuDe:"C2", yccd:"10.C2.1",
      cau:"Theo yêu cầu cần đạt 10.C2.1, khi chọn vấn đề thực tế để ứng dụng AI thì nên ưu tiên điều gì?",
      luaChon:[
        {id:"a", text:"Vấn đề nào có nhiều dữ liệu trên thế giới nhất."},
        {id:"b", text:"Vấn đề gần gũi, cần thiết trong bối cảnh Việt Nam, chẳng hạn sản xuất nông nghiệp hoặc cộng đồng thiểu số."},
        {id:"c", text:"Vấn đề nào dễ làm nhất để nhanh có sản phẩm."},
        {id:"d", text:"Vấn đề do nước ngoài đặt hàng."}],
      dapAn:"b",
      giaiThich:"Đúng, đây là nguyên văn của Khung — ưu tiên các vấn đề gần gũi, cần thiết trong bối cảnh Việt Nam, chẳng hạn sản xuất nông nghiệp, các vấn đề liên quan đến các cộng đồng thiểu số. Nhà máy này chọn bài toán mũ bảo hiểm xe máy vì đó là vấn đề thật của giao thông Việt Nam."},
    { id:"t0-4", mach:"C", chuDe:"C4", yccd:"10.C4.1",
      cau:"Bộ dữ liệu có 92% ảnh chụp ban ngày và 8% ảnh ban đêm. Điều gì sẽ xảy ra với mô hình?",
      luaChon:[
        {id:"a", text:"Không ảnh hưởng gì, vì mô hình học từ toàn bộ dữ liệu."},
        {id:"b", text:"Mô hình học rất tốt đặc điểm ban ngày nhưng gần như không học được đặc điểm ban đêm, vì ban đêm chỉ chiếm 8% số mẫu."},
        {id:"c", text:"Mô hình sẽ từ chối dự đoán với ảnh ban đêm."},
        {id:"d", text:"Mô hình chỉ học được ban đêm vì đó là phần khó."}],
      dapAn:"b",
      giaiThich:"Đúng. Đặc trưng của ảnh ban đêm (điểm ảnh SÁNG VỪA, tín hiệu của mũ màu xám) hầu như không xuất hiện trong dữ liệu, nên trọng số tương ứng không được cập nhật. Điều này sẽ thấy tận mắt ở Trạm 2 và Trạm 4, đúng 100% ban ngày và 59% ban đêm."},
    { id:"t0-5", mach:"D", chuDe:"D2", yccd:"10.D2.1",
      cau:"Trong sơ đồ hệ thống AI, khâu NHẬP LIỆU nằm ở đâu và vì sao nó quan trọng?",
      luaChon:[
        {id:"a", text:"Nằm sau cùng, chỉ để lưu kết quả."},
        {id:"b", text:"Nằm đầu tiên: mọi khâu sau chỉ có thể tốt đến mức dữ liệu cho phép, nên lỗi ở đây sẽ lan xuống toàn bộ dây chuyền."},
        {id:"c", text:"Không thuộc hệ thống AI, vì đó là việc của con người."},
        {id:"d", text:"Chỉ cần thiết khi mô hình lớn."}],
      dapAn:"b",
      giaiThich:"Đúng. Dữ liệu là thành phần đầu tiên trong năm thành phần của hệ thống AI theo 10.D2.1 (dữ liệu, mô hình, thuật toán, đầu ra, phản hồi). Một lỗi ở khâu nhập liệu — dữ liệu lệch, nhãn sai, thiếu một nhóm — không thể được khâu sau sửa chữa. Đó là lí do nhà máy đặt trạm này đầu tiên."}
  ];

  let t0State = null;

  /** Khởi động Trạm 0: sinh ảnh mẫu, trích đặc trưng, dựng giao diện. */
  function khoiDongT0(soAnh, tiLeNgay){
    soAnh = soAnh || 12;
    tiLeNgay = (tiLeNgay == null) ? 92 : tiLeNgay;
    const ds = L().taoDuLieu({ soLuong: soAnh, seed: 20261004 });
    const p = Math.max(0, Math.min(100, tiLeNgay)) / 100;
    let seed = 4242 >>> 0;
    const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;
    ds.forEach(d => {
      d.light = rnd() < p ? "ngay" : "dem";
      d.canvas = L().veXeMay(160, 120, d.kind, d.light, (seed >>> 0) + 1);
      d.f = L().dacTrung(d.canvas);
    });
    t0State = { ds, tiLeNgay, soAnh };
    return ds;
  }

  /** Vẽ lưới ảnh kèm BẢNG ĐẶC TRƯNG — đây là phần 'mở nắp' của Trạm 0. */
  function veAnhVaDacTrung(host){
    if(!t0State) return;
    host.textContent = "";
    const ds = t0State.ds;
    let ngay = 0;
    ds.forEach(d => { if(d.light === "ngay") ngay++; });

    const tt = document.createElement("p");
    tt.className = "nho chu2";
    tt.textContent = `Bộ dữ liệu: ${ds.length} ảnh · ban ngày ${ngay} (${Math.round(ngay/ds.length*100)}%) · ban đêm ${ds.length-ngay} (${Math.round((ds.length-ngay)/ds.length*100)}%)`;
    host.appendChild(tt);

    const bang = document.createElement("table");
    /* AN TOÀN innerHTML: mọi giá trị động (số đo đặc trưng) đều là SỐ do hệ tính,
     * được ép chuỗi rồi escape; không có chuỗi nào do người dùng nhập chảy vào đây. */
    let h = `<tr><th>Ảnh</th><th>Điều kiện sáng</th><th>Nhãn thật</th>
      <th title="tỉ lệ điểm ảnh RẤT SÁNG (>220) trong vùng đầu">① rất sáng</th>
      <th title="tỉ lệ điểm ảnh SÁNG VỪA (100-180) trong vùng đầu">② sáng vừa</th>
      <th title="độ sáng trung bình vùng đầu, chuẩn hoá 0-1">③ độ sáng đầu</th>
      <th title="tỉ lệ điểm tối của TOÀN ảnh">④ tỉ lệ tối</th></tr>`;
    ds.slice(0, 8).forEach((d, i) => {
      const f = L().vec(d.f);
      h += `<tr><td><span class="thumb" id="t0-thumb-${i}"></span></td>
        <td>${d.light === "ngay" ? "ban ngày" : "ban đêm"}</td>
        <td>${d.nhan === 1 ? "CÓ mũ" : "không mũ"}</td>
        <td>${esc(f[0].toFixed(3))}</td><td>${esc(f[1].toFixed(3))}</td>
        <td>${esc(f[2].toFixed(3))}</td><td>${esc(f[3].toFixed(3))}</td></tr>`;
    });
    bang.innerHTML = h;
    host.appendChild(bang);
    // gắn canvas ảnh thật vào từng ô (không đưa canvas qua innerHTML)
    ds.slice(0, 8).forEach((d, i) => {
      const o = $("t0-thumb-" + i);
      if(o && d.canvas) o.appendChild(d.canvas);
    });
  }

  /** Dạng dữ liệu VĂN BẢN: mở nắp máy n-gram của Trạm 5 ngay từ khâu nhập liệu. */
  function veVanBan(host){
    const N = window.MX_NHAMAY_TEXT;
    if(!N){ host.textContent = "(module văn bản chưa nạp)"; return; }
    const info = N.thongTin();
    const cau = N.CORPUS.split(". ").filter(Boolean);
    host.innerHTML =
      `<p class="nho chu2">Văn bản cũng là dữ liệu huấn luyện. Bộ ngữ liệu của nhà máy gồm
       <b>${cau.length + 1}</b> câu, <b>${esc(String(info.doDaiNguLieu))}</b> kí tự.
       Máy học bằng cách đếm các chuỗi <b>${info.n} kí tự</b> liên tiếp, thu được
       <b>${esc(String(info.soNguoiCanh))}</b> ngữ cảnh khác nhau.</p>
       <table><tr><th>#</th><th>Câu trong ngữ liệu</th><th>Số kí tự</th></tr>` +
      cau.slice(0, 6).map((c, i) =>
        `<tr><td>${i + 1}</td><td>${esc(c.trim())}</td><td>${c.trim().length}</td></tr>`).join("") +
      `</table>
       <p class="nho chu2">Ba dạng dữ liệu (ảnh, văn bản, số) đều phải được đổi thành SỐ thì
       mô hình mới đọc được. Với ảnh là bốn đặc trưng ở bảng trên; với văn bản là tần suất
       các chuỗi kí tự.</p>`;
  }

  /** Dạng dữ liệu SỐ: bảng tín hiệu cảm biến. */
  function veSo(host){
    const rows = [
      ["Độ ẩm đất (%)", "42", "cảm biến ruộng", "quyết định thời điểm tưới"],
      ["Nhiệt độ (°C)", "31", "trạm thời tiết", "dự báo sâu bệnh"],
      ["Lượng mưa (mm)", "12", "trạm thời tiết", "dự báo sản lượng"],
      ["Nồng độ bụi mịn (µg/m³)", "68", "cảm biến không khí", "cảnh báo sức khỏe"],
      ["Số điểm ảnh rất sáng", "0.184", "trích từ ảnh", "tín hiệu mũ màu trắng"]
    ];
    host.innerHTML =
      `<p class="nho chu2">Dạng thứ ba là số liệu đo trực tiếp, không cần trích đặc trưng.</p>
       <table><tr><th>Đại lượng</th><th>Giá trị</th><th>Nguồn</th><th>Dùng để làm gì</th></tr>` +
      rows.map(r => `<tr>${r.map(c => `<td>${esc(c)}</td>`).join("")}</tr>`).join("") +
      `</table>`;
  }

  /* ---- Câu hỏi Trạm 0 (oracle) ---- */
  function veCauHoiT0(host, onCham){
    host.textContent = "";
    CAU_HOI_T0.forEach((q, qi) => {
      const box = document.createElement("div");
      box.className = "card";
      box.style.background = "var(--nen2)";
      box.innerHTML = `<p><b>Câu ${qi + 1}.</b> ${esc(q.cau)}</p>
        <div class="chips" id="t0-chips-${qi}"></div><div id="t0-fb-${qi}"></div>
        <p class="nho chu2">Yêu cầu cần đạt ${esc(q.yccd)} · chủ đề ${esc(q.chuDe)}</p>`;
      host.appendChild(box);
      const chips = $("t0-chips-" + qi);
      /* XÁO VỊ TRÍ (06/10): câu hỏi Trạm 0 cũng có đáp án ở vị trí cố định, nên cùng một
       * mẹo "luôn bấm ô thứ hai" áp dụng được. Chỗ này không in chữ cái nên chỉ cần xáo.
       * Seed dùng qi vì item CAU_HOI_T0 có thể không có id — xem js/engine.js xaoLuaChon. */
      const ds = window.MX_ENGINE.xaoLuaChon(q.luaChon, q.id != null ? q.id : "t0-" + qi);
      ds.forEach(l => {
        const b = document.createElement("button");
        b.className = "chip"; b.type = "button"; b.textContent = l.text;
        b.onclick = () => {
          const dung = (l.id === q.dapAn);
          const fb = $("t0-fb-" + qi);
          fb.className = "phanhoi " + (dung ? "dung" : "sai");
          fb.innerHTML = `<p>${dung ? svgIco("check") + " <b>Chính xác.</b>" : svgIco("x") + " <b>Chưa đúng.</b>"} ${esc(q.giaiThich)}</p>`;
          [...chips.children].forEach(c => c.disabled = true);
          b.classList.add("chon");
          if(onCham) onCham(q, l.id, dung);
        };
        chips.appendChild(b);
      });
    });
  }

  /* ======================================================================
   * TRẠM 1 — DÁN NHÃN: học sinh tự dán, hệ so với nhãn thật,
   *             rồi huấn luyện mô hình trên NHÃN CỦA HỌC SINH.
   * ====================================================================== */
  let t1State = null;

  function khoiDongT1(soAnh){
    soAnh = soAnh || 10;
    const ds = L().taoDuLieu({ soLuong: soAnh, seed: 5552026 });
    t1State = { ds, nhanHS: new Array(ds.length).fill(null), daCham: false };
    return ds;
  }

  /** Vẽ ảnh để học sinh dán nhãn. Chưa tiết lộ nhãn thật. */
  function veAnhDanNhan(host){
    if(!t1State) return;
    host.textContent = "";
    const ds = t1State.ds;
    const grid = document.createElement("div");
    ds.forEach((d, i) => {
      const w = document.createElement("div");
      w.className = "anh-nhan";
      w.style.cssText = "display:inline-block;margin:6px;text-align:center;vertical-align:top";
      grid.appendChild(w);
      if(d.canvas) w.appendChild(d.canvas);
      const nut = document.createElement("div");
      nut.className = "chips";
      nut.style.justifyContent = "center";
      const b1 = document.createElement("button");
      b1.className = "dl-the"; b1.type = "button"; b1.textContent = "CÓ mũ";
      b1.dataset.i = i; b1.dataset.v = "1";
      const b0 = document.createElement("button");
      b0.className = "dl-the"; b0.type = "button"; b0.textContent = "KHÔNG mũ";
      b0.dataset.i = i; b0.dataset.v = "0";
      [b1, b0].forEach(b => b.onclick = () => {
        t1State.nhanHS[i] = Number(b.dataset.v);
        [...nut.children].forEach(c => c.classList.remove("chon"));
        b.classList.add("chon");
        capNhatTienDoT1();
      });
      nut.append(b1, b0);
      w.appendChild(nut);
      // LƯU Ý: w đã được gắn vào grid ở đầu vòng lặp rồi. Bản đầu còn một dòng
      // `if(!d.canvas) grid.appendChild(w)` ở cuối — thừa và có hại: appendChild một
      // nút DOM đã có cha sẽ DI CHUYỂN nó, làm lệch thứ tự ảnh khi thiếu canvas.
    });
    host.appendChild(grid);
  }

  function capNhatTienDoT1(){
    /* BUG ĐÃ SỬA — ghi lại vì loại lỗi này mắt thường KHÔNG thấy được:
     * bản đầu viết $("t1-tiend" + U+043E), tức chữ o cuối là KÍ TỰ CYRILLIC chứ không
     * phải chữ 'o' Latin (U+006F). Selector trông y hệt nhưng không khớp id nào,
     * nên hàm trả về sớm và nút "Chấm nhãn" vĩnh viễn disabled — hỏng cả Trạm 1
     * mà không báo lỗi. Sửa bằng cách chỉ dùng MỘT id thuần ASCII và bỏ nhánh dự phòng. */
    const o = $("t1-tiendo");
    if(!o || !t1State) return;
    const done = t1State.nhanHS.filter(x => x !== null).length;
    o.textContent = `Đã dán nhãn ${done}/${t1State.ds.length} ảnh`;
    const b = $("t1-cham");
    if(b) b.disabled = (done < t1State.ds.length);
  }

  /** Chấm nhãn + huấn luyện mô hình TRÊN NHÃN CỦA HỌC SINH rồi đánh giá trên nhãn thật.
   * Đây là thí nghiệm then chốt của 10.C4.1: nhãn sai thì mô hình sai có hệ thống. */
  function chamT1(){
    if(!t1State) return null;
    const ds = t1State.ds, nhanHS = t1State.nhanHS;
    let dung = 0, sai = [];
    ds.forEach((d, i) => {
      if(nhanHS[i] === d.nhan) dung++;
      else sai.push(i);
    });
    const tiLeNhanDung = dung / ds.length;

    // (A) mô hình học trên NHÃN CỦA HỌC SINH
    const mA = new (L().Perceptron)();
    const dsA = ds.map((d, i) => ({ ...d, nhan: nhanHS[i] }));
    mA.hoc({ vong: L().EPOCHS, duLieu: dsA });

    // (B) mô hình học trên NHÃN THẬT (đối chứng)
    const mB = new (L().Perceptron)();
    mB.hoc({ vong: L().EPOCHS, duLieu: ds });

    // đánh giá CẢ HAI trên cùng bộ kiểm tra có nhãn THẬT, khác seed
    const test = L().taoDuLieu({ soLuong: 60, seed: 90210 });
    const kqA = L().kiemTra(mA, test);
    const kqB = L().kiemTra(mB, test);

    t1State.daCham = true;
    return {
      soAnh: ds.length, nhanDung: dung, nhanSai: sai.length,
      viTriSai: sai, tiLeNhanDung,
      hocTrenNhanHS: kqA, hocTrenNhanThat: kqB,
      thietHai: (kqB.doChinhXac - kqA.doChinhXac)
    };
  }

  /** Vẽ kết quả Trạm 1.
   *
   * AN TOÀN innerHTML: đối số `r` do chamT1() trả về và CHỈ chứa số nguyên, số thực,
   * mảng chỉ số và boolean — không có chuỗi nào do người dùng nhập. Hai chỗ duy nhất
   * chèn nội dung động vào HTML là `r.viTriSai.map(i=>i+1).join(", ")` (mảng số) và
   * các giá trị đã qua `p()` (số -> chuỗi "%"). Ảnh của học sinh được gắn bằng
   * appendChild(canvas), không bao giờ đi qua innerHTML. Vì vậy không có đường nào
   * để dữ liệu bên ngoài trở thành mã thực thi. */
  function veKetQuaT1(host, r){
    const p = x => x == null ? "—" : Math.round(x * 100) + "%";
    host.innerHTML =
      `<div class="grid g3">
         <div class="kpi"><div class="so">${r.nhanDung}/${r.soAnh}</div>
           <div class="nhan">nhãn dán ĐÚNG</div></div>
         <div class="kpi"><div class="so ${r.nhanSai?'ko':''}">${r.nhanSai}</div>
           <div class="nhan">nhãn dán SAI</div></div>
         <div class="kpi"><div class="so ${Math.abs(r.thietHai)>0.05?'ko':''}">${p(r.thietHai)}</div>
           <div class="nhan">độ chính xác BỊ MẤT vì nhãn sai</div></div>
       </div>
       <table>
         <tr><th>Mô hình</th><th>Học từ</th><th>Đúng trên bộ kiểm tra</th>
             <th>Ban ngày</th><th>Ban đêm</th></tr>
         <tr><td><b>A</b></td><td>nhãn tự dán</td><td>${r.hocTrenNhanHS.dung}/${r.hocTrenNhanHS.tong} = ${p(r.hocTrenNhanHS.doChinhXac)}</td>
             <td>${p(r.hocTrenNhanHS.ngay.tiLe)}</td><td>${p(r.hocTrenNhanHS.dem.tiLe)}</td></tr>
         <tr><td><b>B</b> (đối chứng)</td><td>nhãn đúng</td><td>${r.hocTrenNhanThat.dung}/${r.hocTrenNhanThat.tong} = ${p(r.hocTrenNhanThat.doChinhXac)}</td>
             <td>${p(r.hocTrenNhanThat.ngay.tiLe)}</td><td>${p(r.hocTrenNhanThat.dem.tiLe)}</td></tr>
       </table>
       <div class="phanhoi ${r.nhanSai===0?'dung':'sai'}">
         <p><b>${r.nhanSai === 0
            ? svgIco("check") + " Nhãn đã dán đúng toàn bộ."
            : `${svgIco("x")} Dán sai ${r.nhanSai} nhãn (ở các ảnh số ${r.viTriSai.map(i=>i+1).join(", ")}).`}</b></p>
         <p class="chu2">${r.nhanSai === 0
            ? "Hai mô hình A và B học từ cùng một bộ nhãn nên cho kết quả như nhau. Hãy thử dán sai vài nhãn rồi chấm lại để thấy hậu quả."
            : `Mô hình A học từ nhãn tự dán nên mất ${p(r.thietHai)} độ chính xác so với mô hình B học từ nhãn đúng. `
              + `Điều đáng chú ý là lỗi này KHÔNG ngẫu nhiên: mô hình học rất chăm chỉ và học ĐÚNG những gì được dạy, kể cả khi dạy sai.`}</p>
         <p class="nho chu2">Yêu cầu cần đạt 10.C4.1: phân tích được sự ảnh hưởng của chất lượng
            dữ liệu đến chất lượng AI. Nhãn là một phần của chất lượng dữ liệu.</p>
       </div>`;
    // hiện nhãn thật lên từng ảnh để học sinh đối chiếu
    if(t1State){
      t1State.ds.forEach((d, i) => {
        const o = $("t1-that-" + i);
        if(o) o.textContent = d.nhan === 1 ? "CÓ mũ" : "không mũ";
      });
    }
  }

  /** Trả về mảng nhãn THẬT — chỉ gọi sau khi đã chấm, để tiết lộ đáp án. */
  function layNhanThat(){
    return t1State ? t1State.ds.map(d => d.nhan) : null;
  }

  /** Trả bộ dữ liệu Trạm 0 đang dùng — để bên ngoài ĐO được bốn đặc trưng thật.
   * VÌ SAO CẦN XUẤT RA: ô dự đoán Mức 3 của BT-01 (js/app.js hàm traLoiBT01) phải so bốn
   * đặc trưng của một ảnh ban ngày với một ảnh ban đêm CÙNG nhãn. Nếu app.js tự sinh lại
   * bộ dữ liệu bằng một seed khác thì nó đo trên dữ liệu khác — phép đối chiếu thành vô
   * nghĩa mà vẫn in ra kết luận. Xuất chính mảng đang hiển thị là cách duy nhất để chắc.
   * Trả về MẢNG GỐC (không sao chép) vì chỉ dùng để đọc, không sửa. */
  function dsT0(){
    return t0State ? t0State.ds : null;
  }

  window.MX_NHAMAY01 = {
    CAU_HOI_T0,
    khoiDongT0, veAnhVaDacTrung, veVanBan, veSo, veCauHoiT0,
    khoiDongT1, veAnhDanNhan, capNhatTienDoT1, chamT1, veKetQuaT1, layNhanThat, dsT0,
    trangThai(){ return { t0: !!t0State, t1: t1State ? {
      soAnh: t1State.ds.length,
      daDan: t1State.nhanHS.filter(x => x !== null).length,
      daCham: t1State.daCham } : null }; }
  };
})();
