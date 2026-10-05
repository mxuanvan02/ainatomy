/* SOI AI — scene3d.js : wrapper three.js dùng chung cho mọi cảnh 3D.
 *
 * RÀNG BUỘC THIẾT KẾ (đã verify, không phải phỏng đoán):
 *  1. three.js r137.5 bản UMD được vendor trong repo (vendor/three/). KHÔNG dùng CDN
 *     vì trường vùng khó có thể mất mạng; KHÔNG dùng ES module vì bị CORS chặn trên file://.
 *     Đã probe thật trên file://: THREE.REVISION=137, OrbitControls gắn vào THREE, render OK.
 *  2. Máy trường có thể KHÔNG có WebGL → không bao giờ được hiện màn hình trắng.
 *     `hoTro3D()` trả false thì caller phải rơi về bản 2D (js/lab.js) kèm 1 dòng thông báo.
 *  3. requestAnimationFrame bị throttle khi tab ẩn (đã đo được lúc probe) → mỗi scene
 *     phải có `veMotLan()` render ĐỒNG BỘ để test được và để tab ẩn không tốn pin.
 *  4. Đổi tab phải `huy()` để giải phóng GPU — nhiều scene tạo/diệt liên tục sẽ rò rỉ bộ nhớ.
 */
(function(){
  "use strict";

  /* Bảng màu 3D cho NỀN SÁNG — mọi giá trị đã đo tương phản WCAG 1.4.11 (>= 3.0:1)
   * trên nền cảnh #F8FAFC bằng tools/nghiem_thu.py. Màu cũ của giao diện tối bị loại
   * vì đo được: vàng #FFD43B = 1.43:1, xanh #4DABF7 = 2.48:1, đỏ #FF6B6B = 2.78:1. */
  const MAU = {
    nen:   0xF8FAFC,   // nền cảnh (sáng)
    the:   0xFFFFFF,   // --the
    vien:  0x7C8598,   // viền/lưới: 3.71:1 trên #FFFFFF, 3.54:1 trên nền cảnh
                       // (đã loại #8B90A8 vì chỉ 3.02:1 trên nền cảnh — dư 0.02, quá mỏng)
    nhan:  0x1D4ED8,   // ảnh BAN ĐÊM   — 6.41:1
    vang:  0xB45309,   // ảnh BAN NGÀY  — 4.80:1
    dung:  0x15803D,   // AI đoán ĐÚNG  — 4.79:1
    sai:   0xB91C1C,   // AI đoán SAI   — 6.18:1
    chu:   0x1E1B4B    // chữ trên nền sáng
  };

  let _kiemTra = null;

  /** Máy này có chạy được 3D không? (kết quả được cache, chỉ dò 1 lần) */
  function hoTro3D(){
    if(_kiemTra !== null) return _kiemTra;
    try{
      if(typeof THREE === "undefined") { _kiemTra = { ok:false, liDo:"three.js chưa nạp" }; return _kiemTra; }
      const c = document.createElement("canvas");
      const gl = c.getContext("webgl") || c.getContext("experimental-webgl");
      if(!gl){ _kiemTra = { ok:false, liDo:"trình duyệt/máy không có WebGL" }; return _kiemTra; }
      _kiemTra = { ok:true, gl: gl.getParameter(gl.VERSION) || "WebGL", rev: THREE.REVISION };
    }catch(e){
      _kiemTra = { ok:false, liDo:"lỗi khi dò WebGL: " + e.message };
    }
    return _kiemTra;
  }

  /** Người dùng có bật "giảm chuyển động" trong hệ điều hành không? */
  function giamChuyenDong(){
    try{ return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches; }
    catch(e){ return false; }
  }

  /**
   * Tạo một cảnh 3D cơ bản gắn vào <canvas>.
   * @param {HTMLCanvasElement} canvas
   * @param {Object} opt { cameraPos:[x,y,z], controls:true, pixelRatioCap:2 }
   * @returns {Object|null} scene handle, hoặc null nếu không chạy được 3D
   */
  function tao(canvas, opt){
    const k = hoTro3D();
    if(!k.ok) return null;
    opt = opt || {};

    const renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: opt.antialias !== false && !giamChuyenDong(),
      alpha: false
    });
    // máy yếu: giới hạn tỉ lệ điểm ảnh để không phải vẽ 4K trên màn retina
    const cap = opt.pixelRatioCap || 2;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, cap));

    const scene = new THREE.Scene();
    scene.background = new THREE.Color(MAU.nen);

    const camera = new THREE.PerspectiveCamera(50, 1, 0.1, 200);
    const cp = opt.cameraPos || [7, 5.5, 9];
    camera.position.set(cp[0], cp[1], cp[2]);

    let controls = null;
    if(opt.controls !== false && typeof THREE.OrbitControls === "function"){
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.08;
      if(opt.target) controls.target.set(opt.target[0], opt.target[1], opt.target[2]);
      controls.update();
    }

    const h = {
      renderer, scene, camera, controls, canvas, MAU,
      _raf: null, _chay: false, _frames: 0, _onTick: null,

      /** Đổi kích thước theo khung chứa (gọi khi init và khi cửa sổ đổi size) */
      doiKichThuoc(){
        const w = canvas.clientWidth || canvas.parentNode.clientWidth || 640;
        const ht = canvas.clientHeight || canvas.parentNode.clientHeight || 420;
        renderer.setSize(w, ht, false);
        camera.aspect = w / Math.max(1, ht);
        camera.updateProjectionMatrix();
        this.veMotLan();
      },

      /** Đăng ký hàm chạy mỗi frame (hoạt ảnh). Không bắt buộc. */
      khiTick(fn){ this._onTick = fn; },

      /** Render ĐỒNG BỘ 1 frame — dùng cho test và cho tab ẩn */
      veMotLan(dt){
        if(this._onTick) this._onTick(dt || 0.016);
        if(this.controls) this.controls.update();
        this.renderer.render(this.scene, this.camera);
        this._frames++;
      },

      /** Bật vòng hoạt ảnh. Tự dừng khi tab ẩn để không tốn pin/CPU. */
      batVong(){
        if(this._chay) return;
        if(giamChuyenDong()){ this.veMotLan(); return; }   // tôn trọng prefers-reduced-motion
        this._chay = true;
        let last = performance.now();
        const loop = (now) => {
          if(!this._chay) return;
          /* BUG ĐÃ SỬA (05/10, bắt bằng monkey-patch getPoint + stack thật): timestamp
           * của rAF là thời điểm BẮT ĐẦU frame, có thể nhỏ hơn performance.now() vừa
           * gán cho `last` (gọi sau) → dt ÂM ở frame đầu/tab vừa hiện lại. dt âm làm
           * vị trí hạt trong pipeline3d tụt xuống t < 0 → curve.getPoint(t<0) ném
           * TypeError giết vòng render. Math.max(0,...) chặn tận gốc cho MỌI scene. */
          const dt = Math.max(0, Math.min(0.05, (now - last) / 1000)); last = now;
          // tab ẩn thì rAF tự ngừng; thêm chốt an toàn để không vẽ vô ích
          if(!document.hidden) this.veMotLan(dt);
          this._raf = requestAnimationFrame(loop);
        };
        this._raf = requestAnimationFrame(loop);
      },

      dungVong(){
        this._chay = false;
        if(this._raf) cancelAnimationFrame(this._raf);
        this._raf = null;
      },

      /** Giải phóng GPU. BẮT BUỘC gọi khi rời tab. */
      huy(){
        this.dungVong();
        try{
          this.scene.traverse(o => {
            if(o.geometry) o.geometry.dispose();
            if(o.material){
              (Array.isArray(o.material) ? o.material : [o.material]).forEach(m => {
                if(m.map) m.map.dispose();
                m.dispose();
              });
            }
          });
          if(this.controls) this.controls.dispose();
          this.renderer.dispose();
        }catch(e){ console.warn("huy 3D:", e); }
        this._huy = true;
      }
    };

    // tự co giãn theo khung
    h.doiKichThuoc();
    window.addEventListener("resize", () => { if(!h._huy) h.doiKichThuoc(); });

    return h;
  }

  /** Raycaster: tìm vật thể 3D mà người học vừa bấm */
  function vatDuoiConTro(canvas, camera, ev, danhSach){
    const r = canvas.getBoundingClientRect();
    const mouse = new THREE.Vector2(
      ((ev.clientX - r.left) / Math.max(1, r.width)) * 2 - 1,
      -((ev.clientY - r.top) / Math.max(1, r.height)) * 2 + 1
    );
    const rc = new THREE.Raycaster();
    rc.setFromCamera(mouse, camera);
    const hits = rc.intersectObjects(danhSach, false);
    return hits.length ? hits[0].object : null;
  }

  window.MX_SCENE = { tao, hoTro3D, giamChuyenDong, vatDuoiConTro, MAU };
})();
