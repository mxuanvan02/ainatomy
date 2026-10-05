/* SOI AI — pipeline3d.js : CẢNH ③ "ỐNG DẪN SOI LUỒNG AI" (3D).
 *
 * YCCĐ phủ (nguyên văn Khung 2422/QĐ-BGDĐT, lớp 10 — đã verify 22/22):
 *   10.D1.1  Nêu được ví dụ cụ thể, xác định nhiệm vụ hoặc mục tiêu cụ thể mà một hệ
 *            thống AI cần thực hiện, nêu được MỐI LIÊN HỆ giữa mục tiêu đó với các
 *            THÀNH PHẦN CHÍNH của hệ thống.
 *   10.D2.1  Mô tả được các THÀNH PHẦN CƠ BẢN của hệ thống AI (dữ liệu, mô hình,
 *            thuật toán, đầu ra, phản hồi) phù hợp với nhiệm vụ cụ thể.
 *   10.B2.MR1 Nhận biết dấu hiệu nội dung do AI tạo sinh; nhận xét MỨC ĐỘ MINH BẠCH.
 *   10.A1.2  Giải thích được tại sao việc CON NGƯỜI KIỂM SOÁT AI là quan trọng.
 *
 * Đây là YCCĐ 10.D1.1 mà bản 2D CHƯA PHỦ — cảnh này sinh ra để phủ nó.
 *
 * CƠ CHẾ TỰ CHẤM (không cần giáo viên):
 *   Hệ làm hỏng NGẪU NHIÊN một trạm, học sinh phải đoán trạm nào. Trạm bị hỏng
 *   do HỆ chọn nên đáp án đã biết trước → chấm bằng phép so sánh tất định.
 *   Kết quả ghi vào nhật ký lớp như mọi hoạt động khác (ENG.logSuKien).
 *
 * Kĩ thuật: hạt photon chạy theo CatmullRomCurve3, không cần vật lý.
 * innerHTML chỉ dùng với HẰNG SỐ TĨNH trong file này — không có dữ liệu người dùng.
 */
(function(){
  "use strict";

  const S = () => window.MX_SCENE;
  const CHIEU_DAI = 18;          // chiều dài ống theo trục x
  const SO_HAT = 26;             // số hạt photon (giới hạn để máy yếu vẫn mượt)

  /* 5 trạm của một hệ thống AI — tên trạm bám đúng chữ của YCCĐ 10.D2.1
     (dữ liệu, mô hình, thuật toán, đầu ra, phản hồi)

     MÀU TRẠM — ĐÃ ĐỔI (04/10). Màu cũ kế thừa từ giao diện tối, đo trên nền cảnh
     sáng #F8FAFC thì 4/5 FAIL ngưỡng 3.0:1 của WCAG 1.4.11:
       #ffd43b = 1.36 · #4dabf7 = 2.37 · #51cf66 = 1.92 · #ff6b6b = 2.65  (#9c36b5 đạt 5.56)
     Bộ mới được chọn bằng tối ưu max-min diversity trên pool 20 màu đạt >= 4.0:1
     (khoảng cách RGB nhỏ nhất giữa hai trạm bất kì = 114.4, so với 58.4 nếu chọn tay
     — chọn tay khiến trạm DỮ LIỆU nâu và trạm CON NGƯỜI đỏ gần như trùng nhau).
     Mọi giá trị được tools/nghiem_thu.py phép G1i kiểm tra tự động, không ước lượng. */
  const TRAM = [
    { id:"dulieu", ten:"DỮ LIỆU", mau:0xA16207, yccd:"10.C4.1",
      moTa:"Nơi thu thập và chuẩn bị dữ liệu huấn luyện — ảnh, âm thanh, văn bản, số liệu.",
      vaiTro:"Mô hình chỉ học được những gì có trong dữ liệu. Dữ liệu lệch thì mô hình lệch.",
      khiHong:"AI chưa từng thấy trường hợp này trong dữ liệu → nó đoán mò và sai có HỆ THỐNG với đúng nhóm bị thiếu.",
      viDu:"Bộ ảnh nhận diện mũ bảo hiểm có 92% là ảnh ban ngày → ban đêm AI sai gần một nửa." },
    { id:"huanluyen", ten:"HUẤN LUYỆN", mau:0x1D4ED8, yccd:"10.C5",
      moTa:"Thuật toán lặp đi lặp lại — so dự đoán với nhãn đúng, đo lỗi, chỉnh trọng số.",
      vaiTro:"Đây là chỗ mô hình thật sự 'học'. Không có bước này thì chỉ là một hàm số do người viết sẵn.",
      khiHong:"Trọng số không hội tụ. Mô hình đoán gần như ngẫu nhiên dù dữ liệu tốt. Độ chính xác dao động, không ổn định.",
      viDu:"Học mãi trên đúng bộ dữ liệu lệch không sửa được thiên kiến — nó chỉ củng cố thêm thiên kiến." },
    { id:"mohinh", ten:"MÔ HÌNH", mau:0x9333EA, yccd:"10.D2.1",
      moTa:"Bộ trọng số đã học được — chính là 'kiến thức' mà AI mang theo.",
      vaiTro:"Mô hình là thứ được triển khai. Nó quyết định mọi đầu ra sau này.",
      khiHong:"Mô hình quá đơn giản so với bài toán → bỏ sót mẫu phức tạp; hoặc quá phức tạp → học thuộc lòng dữ liệu cũ, gặp dữ liệu mới là sai.",
      viDu:"Một đường thẳng không thể phân biệt được ảnh mũ bảo hiểm chụp nghiêng." },
    { id:"daura", ten:"ĐẦU RA", mau:0x15803D, yccd:"10.B2.MR1",
      moTa:"Kết quả AI đưa cho người dùng — nhãn, con số, đoạn văn, hình ảnh, lời khuyên.",
      vaiTro:"Đây là thứ người dùng nhìn thấy và tin. Đầu ra trôi chảy CHƯA chắc đã đúng.",
      khiHong:"AI tạo ra nội dung nghe rất tự tin nhưng bịa số liệu, bịa nguồn trích dẫn, hoặc khuyên lộ thông tin cá nhân.",
      viDu:"AI trích 'Nghị định 999/2024/NĐ-CP' — văn bản này không tồn tại." },
    { id:"connguoi", ten:"CON NGƯỜI KIỂM", mau:0xE11D48, yccd:"10.A1.2",
      moTa:"Con người rà soát, phản hồi và chịu trách nhiệm về quyết định cuối cùng.",
      vaiTro:"Trạm duy nhất có thể CHẶN lỗi trước khi nó gây hại. Đây cũng là 'phản hồi' trong YCCĐ 10.D2.1.",
      khiHong:"Lỗi đi THẲNG tới người dùng. Tin giả lan đi, quyết định sai ảnh hưởng tới người thật, và không ai chịu trách nhiệm.",
      viDu:"Điểm số học sinh bị hạ vì AI chấm sai mà không có giáo viên nào xem lại." }
  ];

  let handle = null, st = null;

  function esc(s){
    return String(s == null ? "" : s).replace(/[&<>"]/g, c =>
      ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));
  }

  /* Trả về chuỗi SVG nội tuyến trỏ tới một symbol trong sprite của index.html.
   * CHUỖI TĨNH — tên icon do chính mã nguồn này chỉ định, không ghép dữ liệu người
   * dùng, nên dùng bên trong innerHTML là an toàn.
   * Tồn tại để thay emoji: MASTER.md cấm dùng emoji làm biểu tượng vì chúng render
   * khác nhau giữa Windows/macOS/Android và mất nét khi phóng to trên máy chiếu. */
  function svgIco(ten){
    return '<svg class="ic" aria-hidden="true"><use href="#i-' + ten + '"/></svg>';
  }

  function init(opts){
    opts = opts || {};
    const canvas = opts.canvas, root = opts.root;
    if(!canvas) return { ok:false, liDo:"không có canvas" };

    const k = S().hoTro3D();
    if(!k.ok){
      /* AN TOÀN innerHTML: HTML dưới đây là HẰNG SỐ TĨNH; chỉ `k.liDo` là động
       * và đã escape bằng esc(). Không có dữ liệu người dùng nào chảy vào. */
      if(root) root.innerHTML =
        `<div class="card" style="border-left:4px solid var(--vang)">
           <b>${svgIco("triangle-alert")} Máy này không chạy được đồ hoạ 3D</b> <span class="nho chu2">(${esc(k.liDo)})</span><br>
           <span class="chu2">Nội dung bài học vẫn còn nguyên ở dạng chữ ngay bên dưới.</span>
         </div>` + bangTinh();
      return { ok:false, liDo:k.liDo, vanHocDuoc:true };
    }

    handle = S().tao(canvas, { cameraPos:[0, 5.5, 15], target:[0, 0, 0] });
    if(!handle) return { ok:false, liDo:"không tạo được renderer" };
    const M = handle.MAU;

    st = { canvas, root, opts, hat: [], tram: [], curve: null,
           tramHong: null, biKet: false, doanCuaHS: null, daCham:false };

    // đường cong nối 5 trạm
    const diem = TRAM.map((t, i) =>
      new THREE.Vector3(-CHIEU_DAI/2 + i*(CHIEU_DAI/(TRAM.length-1)),
                        Math.sin(i*1.1)*0.85, 0));
    st.curve = new THREE.CatmullRomCurve3(diem);

    // ống dẫn (hình trụ mỏng mờ dọc theo đường cong)
    const ongGeo = new THREE.TubeGeometry(st.curve, 60, 0.28, 8, false);
    const ongMat = new THREE.MeshBasicMaterial({ color:M.vien, transparent:true, opacity:0.32 });
    handle.scene.add(new THREE.Mesh(ongGeo, ongMat));

    // 5 trạm: hộp + nhãn
    TRAM.forEach((t, i) => {
      const pos = diem[i];
      const hop = new THREE.Mesh(
        new THREE.BoxGeometry(2.1, 2.1, 2.1),
        new THREE.MeshBasicMaterial({ color:t.mau, transparent:true, opacity:0.30 })
      );
      hop.position.copy(pos);
      hop.userData = { tramId:t.id, index:i };
      handle.scene.add(hop);

      const vien = new THREE.LineSegments(
        new THREE.EdgesGeometry(hop.geometry),
        new THREE.LineBasicMaterial({ color:t.mau })
      );
      vien.position.copy(pos);
      handle.scene.add(vien);

      st.tram.push({ def:t, hop, vien, pos, index:i });
    });

    // hạt photon
    const geoHat = new THREE.SphereGeometry(0.16, 8, 8);
    for(let i = 0; i < SO_HAT; i++){
      const m = new THREE.Mesh(geoHat, new THREE.MeshBasicMaterial({ color:M.chu }));
      m.userData = { t: i / SO_HAT, tocDo: 0.10 + (i % 5) * 0.012 };
      handle.scene.add(m);
      st.hat.push(m);
    }

    handle.khiTick(dt => {
      for(const h of st.hat){
        h.userData.t += dt * h.userData.tocDo;
        /* BUG THỨ HAI CÙNG GỐC (05/10): bản cũ viết `if(t > 1) t -= 1` — chỉ trừ MỘT lần.
         * Khi tab bị throttle (chạy nền), dt của một tick có thể hàng chục giây, t nhảy
         * lên 2–3; trừ một lần vẫn > 1 → curve.getPoint(t>1) ném TypeError trong three.js
         * và giết vòng render. Modulo đưa t về [0,1) với MỌI dt. */
        if(h.userData.t > 1) h.userData.t %= 1;
        // trạm hỏng: hạt kẹt lại ngay trước trạm đó và đổi màu đỏ
        /* BUG ĐÃ SỬA (05/10, bắt được bằng hook rAF + stack thật): khi trạm hỏng là
         * trạm ĐẦU TIÊN (index 0), vị trí kẹt = 0/(5-1) − 0.02 = −0.02. CatmullRomCurve3
         * .getPoint(t) với t < 0 ném "Cannot read properties of undefined (reading 'x')"
         * trong three.js, exception lọt ra ngoài callback rAF làm CHẾT cả vòng render —
         * cảnh 3D đứng hình vĩnh viễn mà console chỉ hiện "Script error." (file:// che
         * stack). Xác suất trúng ≈ 1/5 lượt chơi. Sửa: clamp vị trí kẹt vào [0, 1). */
        const tKet = Math.max(0, st.tramHong/(TRAM.length-1) - 0.02);
        if(st.biKet && st.tramHong !== null && h.userData.t >= tKet){
          h.userData.t = tKet;
          h.material.color.setHex(M.sai);
        } else {
          h.material.color.setHex(M.chu);
        }
        /* Lớp phòng vệ thứ hai: dù dt đã được chặn >= 0 ở scene3d.js, vẫn kẹp t vào
         * [0, 1] ngay trước getPoint — curve này là CatmullRom không khép kín, mọi t
         * ngoài miền đều ném TypeError bên trong three.js (đã chứng kiến 05/10). */
        h.userData.t = Math.max(0, Math.min(1, h.userData.t));
        const p = st.curve.getPoint(h.userData.t);
        h.position.copy(p);
      }
      // trạm hỏng nhấp nháy để học sinh thấy có gì đó không ổn (không chỉ rõ trạm nào)
      st.tram.forEach(tr => {
        tr.hop.material.opacity = 0.30;
      });
    });
    handle.batVong();

    canvas.addEventListener("click", ev => {
      const o = S().vatDuoiConTro(canvas, handle.camera, ev, st.tram.map(t => t.hop));
      if(o && o.userData && opts.onChonTram) opts.onChonTram(TRAM[o.userData.index]);
    });

    return { ok:true, info:k, frames: () => handle._frames,
             veMotLan: () => handle.veMotLan() };
  }

  /* ---------------- chế độ chơi: hệ làm hỏng NGẪU NHIÊN một trạm ---------------- */
  function batDauLuot(seed){
    if(!st) return null;
    seed = seed || (Date.now() & 0xffff);
    const idx = (seed * 2654435761 >>> 0) % TRAM.length;
    st.tramHong = idx;
    st.biKet = true;
    st.daCham = false;
    st.doanCuaHS = null;
    if(handle) handle.veMotLan();
    return { soTram: TRAM.length, daHong: true };
  }

  /** Học sinh đoán trạm nào hỏng. Trả về kết quả chấm TẤT ĐỊNH (oracle = st.tramHong). */
  function doan(tramId){
    if(!st || st.tramHong === null) return { ok:false, liDo:"chưa bắt đầu lượt chơi" };
    const idx = TRAM.findIndex(t => t.id === tramId);
    if(idx < 0) return { ok:false, liDo:"mã trạm không tồn tại" };
    st.doanCuaHS = idx;
    const dung = idx === st.tramHong;
    st.daCham = true;
    // hết kẹt → hạt chạy tiếp nếu đoán đúng (phản hồi trực quan)
    if(dung) st.biKet = false;
    if(handle) handle.veMotLan();
    /* BUG ĐÃ SỬA (04/10) — Trạm 6 chết hoàn toàn ở tương tác chính:
     * nhánh thành công này trả về {dung, doan, dungLa} mà KHÔNG có `ok:true`,
     * trong khi pipe3dDoan() kiểm `if(!r || !r.ok){ ...return; }`. r.ok === undefined
     * là falsy nên LUÔN rơi vào nhánh báo lỗi sớm, không bao giờ chấm hay ghi log.
     * Thêm ok:true để phân biệt với hai nhánh lỗi ở trên (vốn có ok:false). */
    return { ok:true, dung, doan: TRAM[idx], dungLa: TRAM[st.tramHong] };
  }

  function datLai(){
    if(!st) return;
    st.tramHong = null; st.biKet = false; st.daCham = false; st.doanCuaHS = null;
    if(handle) handle.veMotLan();
  }

  /* ---------------- bản chữ cho máy không có 3D (KHÔNG mất bài học) ---------------- */
  function bangTinh(){
    let h = `<div class="card"><h3>5 thành phần của một hệ thống AI (Khung 2422, YCCĐ 10.D2.1)</h3>
      <table><tr><th>Trạm</th><th>Vai trò</th><th>Hậu quả nếu trạm này hỏng</th></tr>`;
    TRAM.forEach(t => {
      h += `<tr><td><b>${esc(t.ten)}</b><br><span class="nho chu2">${esc(t.yccd)}</span></td>
            <td>${esc(t.vaiTro)}</td><td>${esc(t.khiHong)}</td></tr>`;
    });
    return h + `</table></div>`;
  }

  function huy(){ if(handle) handle.huy(); handle = null; st = null; }
  function trangThai(){
    return st ? { tramHong: st.tramHong, biKet: st.biKet, daCham: st.daCham,
                  doanCuaHS: st.doanCuaHS, soHat: st.hat.length,
                  frames: handle ? handle._frames : 0 } : null;
  }

  window.MX_PIPE3D = { init, batDauLuot, doan, datLai, bangTinh, huy, trangThai, TRAM,
                       veMotLan: () => handle && handle.veMotLan() };
})();
