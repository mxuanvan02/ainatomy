/* HỌC AI — TẦNG 1: "XƯỞNG HUẤN LUYỆN AI GIẢ LẬP"
 * Mô phỏng có kiểm soát: perceptron HỌC THẬT (trọng số cập nhật theo lỗi thật) trên
 * đặc trưng ảnh trích từ canvas. Dữ liệu + ánh sáng do hệ kiểm soát nên hệ biết
 * trước mô hình sẽ thiên kiến ở đâu → oracle tự chấm (không cần người kiểm chứng).
 *
 * Câu chuyện sư phạm: bộ dữ liệu huấn luyện lệch 92% ảnh BAN NGÀY → mô hình
 * "đạt độ chính xác cao" nhưng gần như vô dụng với ảnh BAN ĐÊM. Học sinh phải
 * tìm ra nguyên nhân gốc (dữ liệu lệch) và chứng kiến việc bổ sung dữ liệu cân bằng
 * sửa được vấn đề.
 *
 * Đặc trưng (minh bạch, giải thích được cho HS):
 *  - tiLeRatSang:  % pixel RẤT SÁNG (>220) trong vùng đầu người → tín hiệu mũ TRẮNG ban ngày
 *  - tiLeTrungBinh: % pixel SÁNG VỪA (100–180) trong vùng đầu → tín hiệu mũ XÁM ban đêm
 *  - doSangVungDau / tiLeToi: đặc trưng ngữ cảnh (ngày/đêm), không mang tín hiệu mũ
 * Khi chỉ huấn luyện bằng ảnh ngày, trọng số của tiLeTrungBinh không bao giờ được
 * cập nhật (giá trị luôn ~0 trong dữ liệu ngày) → đó chính là cơ chế của thiên kiến.
 */
(function(){
  "use strict";

  const LR = 0.25;        // tốc độ học
  const EPOCHS = 60;      // số vòng lặp (đo thực nghiệm: hội tụ ổn định trên cả 2 chế độ dữ liệu)

  /* ---------- Sinh ảnh tổng hợp (vẽ bằng canvas, không cần file ảnh/mạng) ---------- */
  // kind: 'mbh' (có mũ) | 'khong' (không mũ); light: 'ngay' | 'dem'
  function veXeMay(w, h, kind, light, seed){
    const c = document.createElement("canvas");
    c.width = w; c.height = h;
    const g = c.getContext("2d");
    let s = seed >>> 0;
    const rnd = () => (s = (s*1664525 + 1013904223) >>> 0) / 4294967296;

    // nền trời: ngày sáng vừa phải (không vượt ngưỡng "rất sáng"), đêm rất tối
    if(light === "ngay"){
      g.fillStyle = `hsl(${200+rnd()*15}, 65%, ${72+rnd()*8}%)`;
    }else{
      g.fillStyle = `hsl(225, 40%, ${6+rnd()*5}%)`;
    }
    g.fillRect(0,0,w,h);

    // mặt đường
    g.fillStyle = light === "ngay" ? "#5a5f66" : "#14161a";
    g.fillRect(0, h*0.72, w, h*0.28);

    const cx = w*(0.35+rnd()*0.3), cy = h*0.62;

    // bánh xe
    g.fillStyle = light === "ngay" ? "#22252a" : "#0a0b0d";
    g.beginPath(); g.arc(cx-w*0.14, cy+h*0.12, h*0.09, 0, 7); g.fill();
    g.beginPath(); g.arc(cx+w*0.14, cy+h*0.12, h*0.09, 0, 7); g.fill();

    // thân xe
    g.fillStyle = light === "ngay" ? "#b02a37" : "#3a1116";
    g.fillRect(cx-w*0.16, cy-h*0.02, w*0.32, h*0.10);

    // người lái (thân áo)
    g.fillStyle = light === "ngay" ? "#2f5fa8" : "#101a2b";
    g.fillRect(cx-w*0.05, cy-h*0.22, w*0.10, h*0.22);

    // đầu
    g.fillStyle = light === "ngay" ? "#e8b48c" : "#4a3a2e";
    g.beginPath(); g.arc(cx, cy-h*0.28, h*0.06, 0, 7); g.fill();

    // mũ bảo hiểm (đặc trưng phân biệt): ngày = trắng tinh, đêm = xám vừa
    if(kind === "mbh"){
      g.fillStyle = light === "ngay" ? "#ffffff" : "#8a9099";
      g.beginPath(); g.arc(cx, cy-h*0.30, h*0.075, Math.PI, 0); g.fill();
      g.fillRect(cx-h*0.075, cy-h*0.305, h*0.15, h*0.02);
    }
    return c;
  }

  /* ---------- Trích đặc trưng (vùng đầu người lái) ---------- */
  function dacTrung(canvas){
    const g = canvas.getContext("2d");
    const W = canvas.width, H = canvas.height;
    const d = g.getImageData(0,0,W,H).data;
    const x0=Math.floor(W*0.25), x1=Math.ceil(W*0.75);
    const y0=Math.floor(H*0.24), y1=Math.ceil(H*0.45);
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
    const rnd = () => (seed = (seed*1664525+1013904223)>>>0)/4294967296;
    for(let i=0;i<opts.soLuong;i++){
      const kind = (i%2===0) ? "mbh" : "khong";
      let light;
      if(opts.light) light = opts.light;
      else if(opts.lechAnhSang) light = rnd() < 0.92 ? "ngay" : "dem";  // LỆCH: 92% ngày
      else light = rnd() < 0.5 ? "ngay" : "dem";                          // CÂN BẰNG
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
        giaiThich: "Đúng. Một con số trung bình có thể CHE GIẤU bất công: nếu 92% dữ liệu là ban ngày, mô hình đoán đúng ban ngày đã đủ đạt điểm tổng thể cao dù sai gần hết ban đêm. Vì vậy phải tách ra xem theo từng nhóm — đây chính là kĩ năng kiểm định AI."
      },
      {
        id: "lab-03", mach: "A", unesco: "A2",
        ten: "Sửa thiên kiến bằng cách nào?",
        noiDung: "Sau khi phát hiện dữ liệu lệch, nhóm em cần đề xuất cách khắc phục.",
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
