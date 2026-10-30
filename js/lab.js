/* AInatomy — TẦNG 1: "XƯỞNG HUẤN LUYỆN AI GIẢ LẬP"
 * Mô phỏng có kiểm soát: perceptron HỌC THẬT (trọng số cập nhật theo lỗi thật) trên
 * đặc trưng ảnh trích từ canvas. Dữ liệu + ánh sáng do hệ kiểm soát nên hệ biết
 * trước mô hình sẽ thiên kiến ở đâu → oracle tự chấm (không cần người kiểm chứng).
 *
 * Câu chuyện sư phạm: bộ dữ liệu huấn luyện 100% ảnh BAN NGÀY → mô hình
 * "đạt độ chính xác cao" nhưng gần như vô dụng với ảnh BAN ĐÊM (đoán mò 50%).
 * Học sinh phải tìm ra nguyên nhân gốc (dữ liệu không có ảnh đêm) và chứng kiến
 * việc bổ sung dữ liệu cân bằng sửa được vấn đề.
 *
 * Đặc trưng (minh bạch, giải thích được cho HS):
 *  - tiLeRatSang:  % pixel RẤT SÁNG (>220) trong vùng đầu người → tín hiệu mũ TRẮNG ban ngày
 *  - tiLeTrungBinh: % pixel SÁNG VỪA (100–180) trong vùng đầu → tín hiệu mũ XÁM ban đêm
 *  - doSangVungDau / tiLeToi: đặc trưng ngữ cảnh (ngày/đêm), không mang tín hiệu mũ
 * Khi huấn luyện chỉ bằng ảnh ngày, trọng số của tiLeTrungBinh không bao giờ được
 * cập nhật (giá trị luôn ~0 trong dữ liệu ngày) → đó chính là cơ chế của thiên kiến.
 */
(function(){
  "use strict";

  const LR = 0.25;        // tốc độ học
  const EPOCHS = 60;      // số vòng lặp (đo thực nghiệm: hội tụ ổn định trên cả 2 chế độ dữ liệu)

  /* ---------- Sinh ảnh tổng hợp (vẽ bằng canvas, không cần file ảnh/mạng) ---------- */
  // kind: 'mbh' (có mũ) | 'khong' (không mũ); light: 'ngay' | 'dem' | 'hoangHon' | số (0-100)
  // Nếu light là số: 0-30 = đêm, 30-70 = hoàng hôn, 70-100 = ngày (nội suy mượt)
  function veXeMay(w, h, kind, light, seed){
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    const g = c.getContext("2d");
    let s = seed >>> 0;
    const rnd = () => (s = (s*1664525 + 1013904223) >>> 0) / 4294967296;

    // Chuyển đổi light số sang 3 trạng thái nếu cần
    let lightMode = light;
    let lightValue = 1.0; // 0 = tối hoàn toàn, 1 = sáng hoàn toàn
    if(typeof light === "number"){
      lightValue = light / 100;
      if(light <= 30) lightMode = "dem";
      else if(light <= 70) lightMode = "hoangHon";
      else lightMode = "ngay";
    } else if(typeof light === "string"){
      /* BẢN VÁ: chuỗi "dem"/"hoangHon"/"ngay" phải map sang lightValue TƯƠNG ỨNG.
       * Trước đây lightValue mặc định 1.0 cho MỌI chuỗi -> ảnh ban đêm có mũ TRẮNG
       * y hệt ban ngày -> không còn thiên kiến dữ liệu -> Tầng 1 mất ý nghĩa. */
      if(light === "dem")      { lightMode = "dem";      lightValue = 0.0;  }
      else if(light === "hoangHon") { lightMode = "hoangHon"; lightValue = 0.5;  }
      else                      { lightMode = "ngay";     lightValue = 1.0;  }
    }

    // NỀN TRỜI: nội suy màu sắc mượt mà
    const grad = g.createLinearGradient(0, 0, 0, h*0.72);
    if(lightMode === "ngay"){
      // Nội suy từ hoàng hôn sang ngày
      const t = (lightValue - 0.7) / 0.3; // 0-1 trong vùng ngày
      const r1 = Math.round(255 * (1-t) + 135 * t); // FF -> 87
      const g1 = Math.round(107 * (1-t) + 206 * t); // 6B -> CE
      const b1 = Math.round(53 * (1-t) + 235 * t);  // 35 -> EB
      const r2 = Math.round(247 * (1-t) + 176 * t); // F7 -> B0
      const g2 = Math.round(147 * (1-t) + 224 * t); // 93 -> E0
      const b2 = Math.round(30 * (1-t) + 230 * t);  // 1E -> E6
      grad.addColorStop(0, `rgb(${r1},${g1},${b1})`);
      grad.addColorStop(1, `rgb(${r2},${g2},${b2})`);
    } else if(lightMode === "hoangHon"){
      // Nội suy từ đêm sang hoàng hôn
      const t = (lightValue - 0.3) / 0.4; // 0-1 trong vùng hoàng hôn
      const r1 = Math.round(10 * (1-t) + 255 * t);  // 0A -> FF
      const g1 = Math.round(14 * (1-t) + 107 * t);  // 0E -> 6B
      const b1 = Math.round(26 * (1-t) + 53 * t);   // 1A -> 35
      const r2 = Math.round(26 * (1-t) + 247 * t);  // 1A -> F7
      const g2 = Math.round(31 * (1-t) + 147 * t);  // 1F -> 93
      const b2 = Math.round(46 * (1-t) + 30 * t);   // 2E -> 1E
      grad.addColorStop(0, `rgb(${r1},${g1},${b1})`);
      grad.addColorStop(0.5, `rgb(${Math.round(26*(1-t)+247*t)},${Math.round(31*(1-t)+147*t)},${Math.round(46*(1-t)+30*t)})`);
      grad.addColorStop(1, `rgb(${r2},${g2},${b2})`);
    } else {
      // Đêm: nội suy độ sáng trong vùng đêm
      const t = lightValue / 0.3; // 0-1 trong vùng đêm
      const r1 = Math.round(5 * t + 10);
      const g1 = Math.round(7 * t + 14);
      const b1 = Math.round(13 * t + 26);
      const r2 = Math.round(13 * t + 26);
      const g2 = Math.round(18 * t + 31);
      const b2 = Math.round(30 * t + 46);
      grad.addColorStop(0, `rgb(${r1},${g1},${b1})`);
      grad.addColorStop(1, `rgb(${r2},${g2},${b2})`);
    }
    g.fillStyle = grad;
    g.fillRect(0,0,w,h);

    // MẶT ĐƯỜNG: nội suy màu sắc
    const roadR = lightMode === "ngay" ? Math.round(74 + (1-lightValue)*20) : (lightMode === "hoangHon" ? Math.round(45 + (1-lightValue)*30) : Math.round(10 + lightValue*20));
    const roadG = lightMode === "ngay" ? Math.round(79 + (1-lightValue)*20) : (lightMode === "hoangHon" ? Math.round(45 + (1-lightValue)*30) : Math.round(11 + lightValue*20));
    const roadB = lightMode === "ngay" ? Math.round(86 + (1-lightValue)*20) : (lightMode === "hoangHon" ? Math.round(45 + (1-lightValue)*30) : Math.round(13 + lightValue*20));
    g.fillStyle = `rgb(${roadR},${roadG},${roadB})`;
    g.fillRect(0, h*0.72, w, h*0.28);
    // Đường kẻ giữa đường
    const lineR = lightMode === "ngay" ? 255 : (lightMode === "hoangHon" ? Math.round(136 + (1-lightValue)*50) : Math.round(51 + lightValue*50));
    const lineG = lineR, lineB = lineR;
    g.strokeStyle = `rgb(${lineR},${lineG},${lineB})`;
    g.lineWidth = 3;
    g.setLineDash([10, 10]);
    g.beginPath();
    g.moveTo(0, h*0.86);
    g.lineTo(w, h*0.86);
    g.stroke();
    g.setLineDash([]);

    // VỊ TRÍ XE CỐ ĐỊNH
    const cx = w*0.5, cy = h*0.65;

    // BÁNH XE TO RÕ (tăng 1.5x)
    g.fillStyle = "#1a1a1a";
    g.beginPath(); g.arc(cx-w*0.18, cy+h*0.15, h*0.15, 0, 7); g.fill();
    g.beginPath(); g.arc(cx+w*0.18, cy+h*0.15, h*0.15, 0, 7); g.fill();
    // Viền bánh xe
    const wheelBorderR = lightMode === "ngay" ? 51 : (lightMode === "hoangHon" ? Math.round(26 + (1-lightValue)*30) : Math.round(lightValue*40));
    const wheelBorderG = wheelBorderR, wheelBorderB = wheelBorderR;
    g.strokeStyle = `rgb(${wheelBorderR},${wheelBorderG},${wheelBorderB})`;
    g.lineWidth = 3;
    g.beginPath(); g.arc(cx-w*0.18, cy+h*0.15, h*0.15, 0, 7); g.stroke();
    g.beginPath(); g.arc(cx+w*0.18, cy+h*0.15, h*0.15, 0, 7); g.stroke();
    // Nan hoa
    const spokeR = lightMode === "ngay" ? 102 : (lightMode === "hoangHon" ? Math.round(68 + (1-lightValue)*40) : Math.round(34 + lightValue*40));
    const spokeG = spokeR, spokeB = spokeR;
    g.strokeStyle = `rgb(${spokeR},${spokeG},${spokeB})`;
    g.lineWidth = 2;
    for(let i = 0; i < 4; i++){
      const angle = i * Math.PI / 2;
      g.beginPath();
      g.moveTo(cx-w*0.18, cy+h*0.15);
      g.lineTo(cx-w*0.18 + Math.cos(angle)*h*0.13, cy+h*0.15 + Math.sin(angle)*h*0.13);
      g.stroke();
      g.beginPath();
      g.moveTo(cx+w*0.18, cy+h*0.15);
      g.lineTo(cx+w*0.18 + Math.cos(angle)*h*0.13, cy+h*0.15 + Math.sin(angle)*h*0.13);
      g.stroke();
    }

    // THÂN XE TO HƠN: nội suy màu đỏ theo điều kiện sáng
    const bodyR = lightMode === "ngay" ? 196 : (lightMode === "hoangHon" ? Math.round(139 + (1-lightValue)*50) : Math.round(90 + lightValue*50));
    const bodyG = lightMode === "ngay" ? 30 : (lightMode === "hoangHon" ? Math.round(21 + (1-lightValue)*20) : Math.round(15 + lightValue*10));
    const bodyB = lightMode === "ngay" ? 58 : (lightMode === "hoangHon" ? Math.round(40 + (1-lightValue)*20) : Math.round(26 + lightValue*20));
    g.fillStyle = `rgb(${bodyR},${bodyG},${bodyB})`;
    g.fillRect(cx-w*0.25, cy-h*0.05, w*0.50, h*0.18);
    const bodyBorderR = lightMode === "ngay" ? 138 : (lightMode === "hoangHon" ? Math.round(90 + (1-lightValue)*50) : Math.round(58 + lightValue*40));
    const bodyBorderG = lightMode === "ngay" ? 21 : (lightMode === "hoangHon" ? Math.round(15 + (1-lightValue)*20) : Math.round(10 + lightValue*10));
    const bodyBorderB = lightMode === "ngay" ? 40 : (lightMode === "hoangHon" ? Math.round(26 + (1-lightValue)*20) : Math.round(16 + lightValue*20));
    g.strokeStyle = `rgb(${bodyBorderR},${bodyBorderG},${bodyBorderB})`;
    g.lineWidth = 2;
    g.strokeRect(cx-w*0.25, cy-h*0.05, w*0.50, h*0.18);

    // NGƯỜI LÁI TO RÕ: nội suy màu xanh theo điều kiện sáng
    const driverR = lightMode === "ngay" ? 37 : (lightMode === "hoangHon" ? Math.round(30 + (1-lightValue)*20) : Math.round(30 + lightValue*10));
    const driverG = lightMode === "ngay" ? 99 : (lightMode === "hoangHon" ? Math.round(64 + (1-lightValue)*30) : Math.round(58 + lightValue*20));
    const driverB = lightMode === "ngay" ? 235 : (lightMode === "hoangHon" ? Math.round(175 + (1-lightValue)*40) : Math.round(138 + lightValue*30));
    g.fillStyle = `rgb(${driverR},${driverG},${driverB})`;
    g.fillRect(cx-w*0.08, cy-h*0.32, w*0.16, h*0.30);
    const driverBorderR = lightMode === "ngay" ? 30 : (lightMode === "hoangHon" ? Math.round(23 + (1-lightValue)*20) : Math.round(23 + lightValue*10));
    const driverBorderG = lightMode === "ngay" ? 64 : (lightMode === "hoangHon" ? Math.round(37 + (1-lightValue)*20) : Math.round(37 + lightValue*10));
    const driverBorderB = lightMode === "ngay" ? 175 : (lightMode === "hoangHon" ? Math.round(84 + (1-lightValue)*40) : Math.round(84 + lightValue*20));
    g.strokeStyle = `rgb(${driverBorderR},${driverBorderG},${driverBorderB})`;
    g.lineWidth = 2;
    g.strokeRect(cx-w*0.08, cy-h*0.32, w*0.16, h*0.30);

    // ĐẦU TO RÕ (tăng 1.6x): nội suy màu da theo điều kiện sáng
    const headR = lightMode === "ngay" ? 251 : (lightMode === "hoangHon" ? Math.round(217 + (1-lightValue)*40) : Math.round(146 + lightValue*70));
    const headG = lightMode === "ngay" ? 191 : (lightMode === "hoangHon" ? Math.round(119 + (1-lightValue)*50) : Math.round(64 + lightValue*50));
    const headB = lightMode === "ngay" ? 36 : (lightMode === "hoangHon" ? Math.round(6 + (1-lightValue)*20) : Math.round(14 + lightValue*10));
    g.fillStyle = `rgb(${headR},${headG},${headB})`;
    g.beginPath(); g.arc(cx, cy-h*0.40, h*0.10, 0, 7); g.fill();
    const headBorderR = lightMode === "ngay" ? 217 : (lightMode === "hoangHon" ? Math.round(146 + (1-lightValue)*50) : Math.round(120 + lightValue*30));
    const headBorderG = lightMode === "ngay" ? 119 : (lightMode === "hoangHon" ? Math.round(14 + (1-lightValue)*40) : Math.round(64 + lightValue*30));
    const headBorderB = lightMode === "ngay" ? 6 : (lightMode === "hoangHon" ? Math.round(14 + (1-lightValue)*10) : Math.round(14 + lightValue*10));
    g.strokeStyle = `rgb(${headBorderR},${headBorderG},${headBorderB})`;
    g.lineWidth = 2;
    g.stroke();

    // MŨ BẢO HIỂM RÕ RỆT (tăng 1.6x): nội suy màu mũ theo điều kiện sáng
    // Công thức đảm bảo: ngày (100%) = trắng 255, hoàng hôn (50%) = xám sáng 220, đêm (0%) = xám tối 150
    if(kind === "mbh"){
      // Nội suy tuyến tính: helmet = 150 + lightValue * 105 (150→255)
      const helmetVal = Math.round(150 + lightValue * 105);
      g.fillStyle = `rgb(${helmetVal},${helmetVal},${helmetVal})`;
      g.beginPath(); g.arc(cx, cy-h*0.44, h*0.13, Math.PI, 0); g.fill();
      // Vành mũ
      g.fillRect(cx-h*0.13, cy-h*0.45, h*0.26, h*0.03);
      // Viền mũ đậm: nội suy từ 75 (đêm) → 128 (ngày)
      const borderVal = Math.round(75 + lightValue * 53);
      g.strokeStyle = `rgb(${borderVal},${borderVal},${borderVal})`;
      g.lineWidth = 3;
      g.beginPath(); g.arc(cx, cy-h*0.44, h*0.13, Math.PI, 0); g.stroke();
      g.strokeRect(cx-h*0.13, cy-h*0.45, h*0.26, h*0.03);
    }
    /* NHIỄU PIXEL: rnd() được khai báo nhưng TRƯỚC ĐÂY KHÔNG DÙNG trong veXeMay
     * -> mọi ảnh cùng (kind, light) giống hệt nhau. 60 "ảnh" thực chất chỉ là
     * 4 ảnh lặp lại, nên ảnh đêm trong tập huấn luyện trùng ĐÚNG ảnh đêm trong
     * bộ kiểm thử -> 100% là NHỚ, không phải khái quát. Nay thêm nhiễu ±13 mức
     * xám để mỗi ảnh khác nhau thật sự, đặc trưng ban đêm mới chưa từng được học. */
    const img = g.getImageData(0, 0, w, h);
    const px = img.data;
    for (let i = 0; i < px.length; i += 4) {
      const n = (rnd() - 0.5) * 26;
      px[i]     = Math.max(0, Math.min(255, px[i]     + n));
      px[i + 1] = Math.max(0, Math.min(255, px[i + 1] + n));
      px[i + 2] = Math.max(0, Math.min(255, px[i + 2] + n));
    }
    g.putImageData(img, 0, 0);
    return c;
  }

  /* ---------- Trích đặc trưng (vùng đầu + mũ bảo hiểm) ---------- */
  function dacTrung(canvas){
    const g = canvas.getContext("2d");
    const W = canvas.width, H = canvas.height;
    const d = g.getImageData(0,0,W,H).data;
    // VÙNG TRÍCH XUẤT: bao gồm cả mũ bảo hiểm (vẽ ở h*0.08-h*0.21) và đầu (h*0.15-h*0.35)
    // Sửa 29/10: y0 từ H*0.24 → H*0.08 để bao gồm mũ, giúp đặc trưng ① (điểm ảnh rất sáng)
    // phát hiện được mũ trắng ban ngày. Trước đó mũ nằm ngoài vùng trích xuất → ① luôn = 0.
    const x0=Math.floor(W*0.25), x1=Math.ceil(W*0.75);
    const y0=Math.floor(H*0.08), y1=Math.ceil(H*0.45);
    let n=0, ratSang=0, trungBinh=0, sumVung=0, dark=0, nWhole=0;
    for(let y=0;y<H;y++){
      for(let x=0;x<W;x++){
        const i=(y*W+x)*4;
        const lum = 0.299*d[i] + 0.587*d[i+1] + 0.114*d[i+2];
        nWhole++;
        if(lum<60) dark++;
        if(x>=x0 && x<x1 && y>=y0 && y<y1){
          n++; sumVung += lum;
          if(lum>220) ratSang++;
          if(lum>=100 && lum<=180) trungBinh++;
        }
      }
    }
    return {
      tiLeRatSang:   ratSang/n,
      tiLeTrungBinh: trungBinh/n,
      doSangVungDau: sumVung/n/255,
      tiLeToi:       dark/nWhole
    };
  }

  function vec(f){ return [f.tiLeRatSang, f.tiLeTrungBinh, f.doSangVungDau, f.tiLeToi]; }

  /* ---------- Perceptron: học thật, trọng số thật ---------- */
  function Perceptron(){
    this.w = [0,0,0,0]; this.b = 0; this.lr = LR;
  }
  Perceptron.prototype.dudoan = function(f){
    const x = vec(f);
    let z = this.b;
    for(let i=0;i<4;i++) z += this.w[i]*x[i];
    return z >= 0 ? 1 : 0;   // 1 = có mũ, 0 = không
  };
  Perceptron.prototype.hoc = function(mau){
    let loi = 0;
    for(let v=0; v<mau.vong; v++){
      for(const d of mau.duLieu){
        const pred = this.dudoan(d.f);
        const err = d.nhan - pred;
        if(err !== 0) loi++;
        const x = vec(d.f);
        for(let i=0;i<4;i++) this.w[i] += this.lr*err*x[i];
        this.b += this.lr*err;
      }
    }
    return loi;
  };

  /* ---------- Bộ dữ liệu: opts {soLuong, light:'ngay'|'dem'|null, lechAnhSang, seed} ---------- */
  function taoDuLieu(opts){
    const ds = [];
    let seed = opts.seed || 12345;
    // FIX: 1013904223 - LCG constant for random number generation
    const rnd = () => (seed = (seed*1664525+1013904223)>>>0)/4294967296;
    for(let i=0;i<opts.soLuong;i++){
      const kind = (i%2===0) ? "mbh" : "khong";
      let light;
      if(opts.light) light = opts.light;
      else if(opts.lechAnhSang) light = "ngay";  // LỆCH TUYỆT ĐỐI: 100% ngày, 0% đêm -> mô hình không học được ban đêm
      else light = rnd() < 0.5 ? "ngay" : "dem";  // CÂN BẰNG: 50/50
      const c = veXeMay(160,120,kind,light, (seed>>>0)+i*7919);
      const f = dacTrung(c);
      ds.push({ canvas:c, f:f, nhan: kind==="mbh"?1:0, light:light, kind:kind });
    }
    return ds;
  }

  function kiemTra(model, ds){
    let dung=0, ngayDung=0, ngayTong=0, demDung=0, demTong=0;
    for(const d of ds){
      const p = model.dudoan(d.f);
      const ok = (p===d.nhan);
      if(ok) dung++;
      if(d.light==="ngay"){ ngayTong++; if(ok) ngayDung++; }
      else { demTong++; if(ok) demDung++; }
    }
    return {
      tong: ds.length, dung: dung,
      doChinhXac: ds.length? dung/ds.length : 0,
      ngay: ngayTong? {dung:ngayDung, tong:ngayTong, tiLe:ngayDung/ngayTong} : {dung:0,tong:0,tiLe:0},
      dem:  demTong ? {dung:demDung,  tong:demTong,  tiLe:demDung/demTong}   : {dung:0,tong:0,tiLe:0}
    };
  }

  /* ---------- Nhiệm vụ có oracle (đáp án cứng, hệ tự chấm) ---------- */
  window.MX_LAB = {
    veXeMay, dacTrung, Perceptron, taoDuLieu, kiemTra, vec, EPOCHS,

    nhiemVu: [
      {
        id: "lab-01", mach: "D", unesco: "D1",
        ten: "Vì sao AI 'giỏi' ban ngày mà 'dốt' ban đêm?",
        noiDung: "Mô hình báo độ chính xác rất cao trên dữ liệu huấn luyện, nhưng sai gần hết ảnh ban đêm.",
        cauHoi: "Nguyên nhân GỐC của việc AI sai hàng loạt vào ban đêm là gì?",
        luaChon: [
          { id:"a", text:"Vì camera điện thoại chụp đêm luôn bị mờ, không AI nào khắc phục được." },
          { id:"b", text:"Vì dữ liệu huấn luyện gần như toàn ảnh ban ngày, nên AI chưa từng được học đặc điểm ban đêm." },
          { id:"c", text:"Vì mô hình quá đơn giản, cần mô hình lớn hơn gấp trăm lần." },
          { id:"d", text:"Vì học sinh vùng nông thôn không nên dùng AI nhận diện." }
        ],
        dapAn: "b",
        giaiThich: "Đúng. Đây là thiên kiến dữ liệu (data bias): mô hình chỉ học được những gì nó đã thấy. Dữ liệu huấn luyện lệch về ban ngày → ban đêm mô hình đoán mò. Cách sửa là BỔ SUNG dữ liệu đa dạng, không phải đổ lỗi cho thiết bị hay loại bỏ người dùng."
      },
      {
        id: "lab-02", mach: "D", unesco: "D2",
        ten: "Con số 'độ chính xác cao' có đáng tin không?",
        noiDung: "Độ chính xác tổng thể cao, nhưng tách riêng ban ngày/ban đêm thì chênh lệch rất lớn.",
        cauHoi: "Bài học quan trọng nhất khi đọc một con số 'độ chính xác' của AI là gì?",
        luaChon: [
          { id:"a", text:"Chỉ cần nhìn độ chính xác tổng thể là đủ kết luận mô hình tốt." },
          { id:"b", text:"Độ chính xác cao vẫn có thể che giấu việc mô hình thất bại hoàn toàn với một nhóm trường hợp." },
          { id:"c", text:"Độ chính xác dưới 100% nghĩa là mô hình vô dụng." },
          { id:"d", text:"Không cần quan tâm độ chính xác, cứ dùng là được." }
        ],
        dapAn: "b",
        giaiThich: "Đúng. Một con số trung bình có thể CHE GIẤU bất công: nếu dữ liệu chỉ có ảnh ban ngày, mô hình đoán đúng ban ngày đã đủ đạt điểm tổng thể cao dù sai gần hết ban đêm. Vì vậy phải tách ra xem theo từng nhóm — đây chính là kĩ năng kiểm định AI."
      },
      {
        id: "lab-03", mach: "A", unesco: "A2",
        ten: "Sửa thiên kiến bằng cách nào?",
        noiDung: "Sau khi phát hiện dữ liệu lệch, cần đề xuất cách khắc phục.",
        cauHoi: "Cách khắc phục thiên kiến này HỢP LÍ nhất là gì?",
        luaChon: [
          { id:"a", text:"Cấm dùng hệ thống này ở những nơi thiếu ánh sáng." },
          { id:"b", text:"Bổ sung thêm nhiều ảnh ban đêm vào dữ liệu huấn luyện rồi huấn luyện lại." },
          { id:"c", text:"Giấu con số ban đêm đi để báo cáo đẹp hơn." },
          { id:"d", text:"Tăng số lần huấn luyện trên đúng bộ dữ liệu cũ." }
        ],
        dapAn: "b",
        giaiThich: "Đúng. Gốc rễ nằm ở DỮ LIỆU, nên phải sửa dữ liệu: thu thập thêm mẫu đại diện cho nhóm bị bỏ sót rồi huấn luyện lại. Phương án (d) vô ích vì học lại mãi trên dữ liệu lệch chỉ củng cố thiên kiến; (c) là gian lận; (a) là loại trừ người dùng."
      },
      {
        id: "lab-04", mach: "C", unesco: "C1",
        ten: "AI học bằng cách nào?",
        noiDung: "HS quan sát mô hình sai rồi tự sửa trọng số qua mỗi vòng huấn luyện.",
        cauHoi: "Trong thí nghiệm này, mô hình 'học' bằng cách nào?",
        luaChon: [
          { id:"a", text:"AI tự hiểu thế giới giống con người nên không cần dữ liệu." },
          { id:"b", text:"Mô hình điều chỉnh dần các trọng số dựa trên lỗi giữa dự đoán và nhãn đúng trong dữ liệu huấn luyện." },
          { id:"c", text:"Mô hình tra cứu đáp án trên Internet mỗi lần gặp ảnh mới." },
          { id:"d", text:"Người lập trình viết sẵn danh sách đáp án cho từng bức ảnh." }
        ],
        dapAn: "b",
        giaiThich: "Đúng. Học máy có giám sát = mô hình so dự đoán với nhãn đúng, đo lỗi, rồi điều chỉnh trọng số để lần sau sai ít hơn. Không có 'hiểu biết' như người, và không tra mạng — đó là lí do thí nghiệm này chạy được hoàn toàn offline."
      }
    ]
  };
})();
