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

  const MAU = {
    nen:   0x0f1115,   // --nen
    the:   0x1d222c,   // --the
    vien:  0x2b3240,   // --vien
    nhan:  0x4dabf7,   // --nhan  (xanh)  = ảnh BAN ĐÊM
    vang:  0xffd43b,   // --vang  (vàng)  = ảnh BAN NGÀY
    dung:  0x51cf66,   // --dung  (xanh lá) = đoán đúng
    sai:   0xff6b6b,   // --sai   (đỏ)    = đoán sai
    chu:   0xe8ecf3
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
          const dt = Math.min(0.05, (now - last) / 1000); last = now;
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
