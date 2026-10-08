/* HỌC AI — lab3d.js : CẢNH ② "XƯỞNG SOI MÔ HÌNH" (3D).
 *
 * YCCĐ phủ (nguyên văn Khung 2422/QĐ-BGDĐT, lớp 10 — đã verify 22/22):
 *   10.C4.1  Phân tích được sự ảnh hưởng của chất lượng dữ liệu đến chất lượng AI.
 *   10.D2.2  Nêu được ví dụ về một số vấn đề phát sinh trong quá trình vận hành hoặc
 *            tối ưu hoá AI và trình bày được ý nghĩa của việc khắc phục các vấn đề đó.
 *   10.B3.1  Trình bày được ví dụ minh họa một số vấn đề đạo đức ... (như thiên vị dữ liệu ...)
 *   10.C4.MR1 Phân tích được các dạng dữ liệu ... được sử dụng để huấn luyện AI.
 *
 * NGUYÊN TẮC TRUNG THỰC (quan trọng nhất của file này):
 *   Cảnh 3D KHÔNG vẽ minh hoạ giả. Nó dùng ĐÚNG perceptron và ĐÚNG bộ dữ liệu ảnh
 *   của Tầng 1 (MX_LAB.taoDuLieu / MX_LAB.Perceptron / MX_LAB.kiemTra). Con số
 *   học sinh đọc được trên màn hình 3D là kết quả huấn luyện THẬT.
 *
 *   Mô hình có 4 đặc trưng nhưng không gian chỉ có 3 chiều → mặt phẳng hiển thị là
 *   LÁT CẮT của biên 4D tại giá trị TRUNG BÌNH của đặc trưng thứ 4 (tiLeToi).
 *   Đây là phép chiếu hợp lệ về mặt toán học và được ghi rõ trên HUD để không ai
 *   tưởng rằng mô hình chỉ dùng 3 đặc trưng.
 *
 *   Ánh xạ trục (đặc trưng thật → trục three.js):
 *     x = tiLeRatSang   (w0) — tín hiệu mũ TRẮNG, chỉ có ban ngày
 *     y = doSangVungDau (w2) — ngữ cảnh sáng/tối: trục này TÁCH cụm ngày khỏi cụm đêm
 *     z = tiLeTrungBinh (w1) — tín hiệu mũ XÁM, chỉ có ban đêm
 *     đặc trưng thứ 4 tiLeToi (w3) giữ ở giá trị trung bình
 */
(function(){
  "use strict";

  const S = () => window.MX_SCENE, L = () => window.MX_LAB;
  const TEN_TRUC = ["tiLeRatSang", "doSangVungDau", "tiLeTrungBinh"];
  const CHIEU_RONG = 6;   // mỗi trục trải [-3, +3] đơn vị three.js

  let handle = null, state = null;
  /* "Chế độ nhẹ": tắt hoạt ảnh vòng lặp + antialias + giảm số chấm, dành cho máy trường
   * yếu hoặc khi người học/hệ điều hành yêu cầu ít chuyển động. BẬT qua opts.nhe. */
  let cheDoNhe = false;

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

  /* ---------------- chuẩn hoá đặc trưng về [-3,3] ---------------- */
  function boChuanHoa(ds){
    const min = [Infinity, Infinity, Infinity], max = [-Infinity, -Infinity, -Infinity];
    let sumToi = 0;
    for(const d of ds){
      const f = L().vec(d.f);
      const v = [f[0], f[2], f[1]];          // đổi thứ tự theo ánh xạ trục ở đầu file
      for(let i = 0; i < 3; i++){
        if(v[i] < min[i]) min[i] = v[i];
        if(v[i] > max[i]) max[i] = v[i];
      }
      sumToi += f[3];
    }
    const scale = min.map((m, i) => {
      const span = (max[i] - m) || 1e-6;
      return CHIEU_RONG / span;
    });
    return { min, max, scale, toiTrungBinh: ds.length ? sumToi / ds.length : 0 };
  }
  const toaDo = (d, ch) => {
    const f = L().vec(d.f);
    const v = [f[0], f[2], f[1]];
    return v.map((x, i) => (x - ch.min[i]) * ch.scale[i] - CHIEU_RONG / 2);
  };

  /* ---------------- mặt phẳng quyết định từ trọng số THẬT ----------------
   * Biên thật: w0*f0 + w1*f1 + w2*f2 + w3*f3 + b = 0   (f = 4 đặc trưng thô)
   * Với f3 = toiTrungBinh và fi = min_i + (trục_i + 3)/scale_i:
   *   Σ wi*(min_i + (truc_i+3)/scale_i) + w3*toiTB + b = 0
   * → normal = (w0/scale0, w2/scale2, w1/scale1)  theo trục (x,y,z) đã ánh xạ
   * → offset = w0*min0 + w2*min2 + w1*min1 + 3*(w0/s0 + w2/s2 + w1/s1) + w3*toiTB + b
   */
  function matPhangTuTrongSo(model, ch){
    const w = model.w, b = model.b;
    const n = new THREE.Vector3(w[0] / ch.scale[0], w[2] / ch.scale[2], w[1] / ch.scale[1]);
    const offset = w[0] * ch.min[0] + w[2] * ch.min[2] + w[1] * ch.min[1]
                 + 3 * (w[0] / ch.scale[0] + w[2] / ch.scale[2] + w[1] / ch.scale[1])
                 + w[3] * ch.toiTrungBinh + b;
    const len2 = n.lengthSq() || 1e-9;
    const p0 = n.clone().multiplyScalar(-offset / len2);
    return { n, p0 };
  }

  /* ---------------- dựng cảnh ---------------- */
  function init(opts){
    opts = opts || {};
    const canvas = opts.canvas, root = opts.root;
    if(!canvas) return { ok:false, liDo:"không có canvas" };

    cheDoNhe = !!opts.nhe;

    const k = S().hoTro3D();
    if(!k.ok){
      /* AN TOÀN innerHTML: chuỗi HTML bên dưới là HẰNG SỐ TĨNH trong mã nguồn.
       * Biến động duy nhất là `k.liDo` (tên lỗi WebGL / message exception) và nó
       * đã được escape bằng esc() — không có đường nào để dữ liệu học sinh hay
       * nội dung từ ngân hàng câu hỏi chảy vào đây. */
      if(root) root.innerHTML =
        `<div class="card" style="border-left:4px solid var(--vang)">
           <b>${svgIco("triangle-alert")} Máy này không chạy được đồ hoạ 3D</b> <span class="nho chu2">(${esc(k.liDo)})</span><br>
           <span class="chu2">Không sao — <b>nội dung bài học không đổi</b>. Em hãy dùng
           <b>Tầng 1 — Xưởng huấn luyện</b> ở trang chủ: cùng một mô hình, cùng bộ dữ liệu
           và cùng con số, chỉ hiển thị dạng 2D. Mọi kết quả vẫn được ghi vào nhật ký lớp.</span>
         </div>`;
      return { ok:false, liDo:k.liDo };
    }

    handle = S().tao(canvas, { cameraPos:[8, 6, 10], target:[0, 0, 0],
                               antialias: !cheDoNhe, pixelRatioCap: cheDoNhe ? 1 : 2 });
    if(!handle) return { ok:false, liDo:"không tạo được renderer" };
    const M = handle.MAU;

    state = {
      canvas, root, opts,
      tiLeNgay: opts.tiLeNgay != null ? opts.tiLeNgay : 92,
      duLieu: null, chuan: null, model: null,
      diem: [], matPhang: null, epoch: 0, tongEpoch: 0,
      dangHoc: false, _rafHoc: null
    };

    // trục toạ độ + lưới nền
    handle.scene.add(new THREE.AxesHelper(CHIEU_RONG / 2 + 1.2));
    const luoi = new THREE.GridHelper(CHIEU_RONG + 2, 12, M.vien, M.vien);
    luoi.position.y = -CHIEU_RONG / 2 - 0.01;
    luoi.material.transparent = true; luoi.material.opacity = 0.28;
    handle.scene.add(luoi);

    // mặt phẳng quyết định (tạo rỗng, cập nhật sau khi huấn luyện)
    const pg = new THREE.PlaneGeometry(CHIEU_RONG + 2.4, CHIEU_RONG + 2.4);
    const pm = new THREE.MeshBasicMaterial({
      color: M.sai, transparent: true, opacity: 0.16,
      side: THREE.DoubleSide, depthWrite: false
    });
    state.matPhang = new THREE.Mesh(pg, pm);
    state.matPhang.visible = false;
    handle.scene.add(state.matPhang);

    // bấm vào điểm dữ liệu → xem nhãn thật vs AI đoán
    canvas.addEventListener("click", ev => {
      if(!state.diem.length) return;
      const o = S().vatDuoiConTro(canvas, handle.camera, ev, state.diem);
      if(o && o.userData && opts.onChonDiem) opts.onChonDiem(o.userData);
    });

    handle.khiTick(dt => {
      // chỉ hoạt hoạ nhẹ: quay mặt phẳng khi đang học để học sinh thấy nó dịch
      if(state.dangHoc && state.matPhang.visible) state.matPhang.rotation.z += dt * 0.05;
    });
    /* Chế độ nhẹ thì KHÔNG chạy vòng lặp rAF — chỉ render đồng bộ mỗi khi có thay đổi.
     * Tiết kiệm CPU/GPU cho máy trường yếu; bài học vẫn đầy đủ vì mọi cập nhật
     * (dungDuLieu / hocMotEpoch / danhGia) đều gọi handle.veMotLan(). */
    if(!cheDoNhe) handle.batVong(); else handle.veMotLan();

    return { ok:true, info:k, handle, cheDoNhe,
             veMotLan: () => handle.veMotLan(),
             frames: () => handle._frames };
  }

  /* ---------------- tạo/sinh lại đám mây điểm từ DỮ LIỆU THẬT ---------------- */
  function dungDuLieu(soLuong){
    if(!state) return null;
    // xoá điểm cũ
    state.diem.forEach(m => handle.scene.remove(m));
    state.diem = [];

    const ds = L().taoDuLieu({ soLuong: cheDoNhe
        ? Math.min(28, soLuong || 28)     // chế độ nhẹ: ít chấm hơn để máy yếu vẫn mượt
        : (soLuong || 48),
      seed: state.opts.seed || 20261004 });
    // áp tỉ lệ ngày/đêm do học sinh chọn (đây chính là biến số của bài học)
    const p = Math.max(0, Math.min(100, state.tiLeNgay)) / 100;
    let seed = (state.opts.seed || 777) >>> 0;
    const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;
    ds.forEach(d => {
      d.light = rnd() < p ? "ngay" : "dem";
      // vẽ lại ảnh theo điều kiện sáng mới để đặc trưng THẬT khớp với nhãn ngày/đêm
      d.canvas = L().veXeMay(160, 120, d.kind, d.light, (seed >>> 0) + 1);
      d.f = L().dacTrung(d.canvas);
    });

    state.duLieu = ds;
    state.chuan = boChuanHoa(ds);
    const M = handle.MAU;
    const geoMui = new THREE.SphereGeometry(0.13, 10, 10);      // có mũ bảo hiểm
    const geoKhong = new THREE.TetrahedronGeometry(0.17);        // không mũ

    for(const d of ds){
      const [x, y, z] = toaDo(d, state.chuan);
      const mau = d.light === "ngay" ? M.vang : M.nhan;
      const mat = new THREE.MeshBasicMaterial({ color: mau });
      const mesh = new THREE.Mesh(d.nhan === 1 ? geoMui : geoKhong, mat);
      mesh.position.set(x, y, z);
      mesh.userData = {
        kind: d.kind, light: d.light, nhan: d.nhan,
        f: L().vec(d.f),
        ten: (d.nhan === 1 ? "CÓ mũ bảo hiểm" : "KHÔNG mũ bảo hiểm")
           + " · ảnh " + (d.light === "ngay" ? "BAN NGÀY" : "BAN ĐÊM")
      };
      handle.scene.add(mesh);
      state.diem.push(mesh);
    }

    // mô hình mới, chưa học
    state.model = new (L().Perceptron)();
    state.epoch = 0;
    state.matPhang.visible = false;
    handle.veMotLan();
    return ds.length;
  }

  function capNhatMatPhang(){
    if(!state || !state.model || !state.chuan) return;
    const { n, p0 } = matPhangTuTrongSo(state.model, state.chuan);
    if(!isFinite(n.x + n.y + n.z + p0.x + p0.y + p0.z)) return;
    state.matPhang.position.copy(p0);
    state.matPhang.lookAt(p0.clone().add(n));
    state.matPhang.visible = true;
  }

  /* ---------------- huấn luyện TỪNG EPOCH, hiện trọng số thật ---------------- */
  function hocMotEpoch(){
    if(!state || !state.duLieu) return null;
    const m = state.model;
    // một epoch = 1 lượt qua toàn bộ dữ liệu, cập nhật trọng số theo lỗi thật
    let loi = 0;
    for(const d of state.duLieu){
      const pred = m.dudoan(d.f);
      const err = d.nhan - pred;
      if(err !== 0) loi++;
      const x = L().vec(d.f);
      for(let i = 0; i < 4; i++) m.w[i] += m.lr * err * x[i];
      m.b += m.lr * err;
    }
    state.epoch++;
    capNhatMatPhang();
    handle.veMotLan();
    return { epoch: state.epoch, loi, w: m.w.slice(), b: m.b };
  }

  function hocHet(cb){
    if(!state || state.dangHoc) return;
    state.dangHoc = true;
    const tong = L().EPOCHS || 60;
    state.tongEpoch = tong;
    let e = 0;
    const buoc = () => {
      if(!state){ return; }
      const r = hocMotEpoch();
      if(cb) cb(r);
      e++;
      if(e < tong) setTimeout(buoc, S().giamChuyenDong() ? 0 : 55);
      else { state.dangHoc = false; if(cb) cb(r, true); }
    };
    buoc();
  }

  /* ---------------- đánh giá THẬT: tách ngày/đêm ---------------- */
  function danhGia(){
    if(!state || !state.model) return null;
    // bộ kiểm tra CÂN BẰNG và KHÁC seed với bộ huấn luyện (không học tủ)
    const test = L().taoDuLieu({ soLuong: 60, seed: (state.opts.seed || 5) + 999 });
    const kq = L().kiemTra(state.model, test);
    // tô màu điểm theo đúng/sai để học sinh thấy lỗi nằm ở đâu
    const M = handle.MAU;
    state.diem.forEach((mesh, i) => {
      const d = state.duLieu[i];
      if(!d) return;
      const dung = state.model.dudoan(d.f) === d.nhan;
      mesh.material.color.setHex(dung ? (d.light === "ngay" ? M.vang : M.nhan) : M.sai);
    });
    handle.veMotLan();
    return kq;
  }

  function doiTiLeNgay(p){ state.tiLeNgay = p; }

  /* ---------------- BT-04 Mức 3: chọn điểm NGẪU NHIÊN để học sinh dự đoán nhãn ----
   * Trả về {index, f, light} — KHÔNG kèm nhãn, để học sinh phải tự dự đoán trước.
   * Chọn tất định theo seed của bộ dữ liệu: cùng bộ dữ liệu thì cùng một điểm,
   * không thể bấm lại liên tục để dò điểm "dễ". */
  function chonDiemNgauNhien(){
    if(!state || !state.duLieu || !state.duLieu.length) return null;
    const seed = (state.opts.seed || 20261004) >>> 0;
    const idx = (seed * 2654435761 >>> 0) % state.duLieu.length;
    const d = state.duLieu[idx];
    /* BUG ĐÃ SỬA: bản đầu viết d.f.slice() nhưng d.f là OBJECT đặc trưng đặt tên
     * (dacTrung() trả {tiLeRatSang,...}), không phải mảng — .slice() ném TypeError.
     * Chuyển về vector 4 số bằng L().vec() giống mọi nơi khác. */
    return { index: idx, f: L().vec(d.f), light: d.light };
  }
  /** Tiết lộ nhãn thật của một điểm — chỉ gọi SAU khi học sinh đã chốt dự đoán. */
  function layNhanDiem(i){
    return (state && state.duLieu && state.duLieu[i]) ? state.duLieu[i].nhan : null;
  }
  /** Mô hình đang giữ trong phòng 3D đoán điểm i là gì (1 = có mũ, 0 = không).
   * Trả null nếu chưa tạo dữ liệu / chưa học — người gọi phải thông báo, không đoán mò. */
  function dudoanDiem(i){
    if(!state || !state.duLieu || !state.duLieu[i] || !state.model) return null;
    return state.model.dudoan(state.duLieu[i].f);
  }
  function huy(){ if(handle){ handle.huy(); } handle = null; state = null; }
  function trangThai(){
    if(!state) return null;
    return {
      soDiem: state.diem.length, tiLeNgay: state.tiLeNgay, epoch: state.epoch,
      w: state.model ? state.model.w.slice() : null,
      b: state.model ? state.model.b : null,
      coMatPhang: state.matPhang ? state.matPhang.visible : false,
      frames: handle ? handle._frames : 0
    };
  }

  window.MX_LAB3D = {
    init, dungDuLieu, hocMotEpoch, hocHet, danhGia,
    doiTiLeNgay, capNhatMatPhang, trangThai, huy,
    chonDiemNgauNhien, layNhanDiem, dudoanDiem,
    veMotLan: () => handle && handle.veMotLan(),
    TEN_TRUC
  };
})();
