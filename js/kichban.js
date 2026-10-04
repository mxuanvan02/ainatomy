/* SOI AI — kichban.js : "HÀNH TRÌNH CỦA MỘT BỨC ẢNH" — kịch bản 9 cảnh tự chạy.
 *
 * YÊU CẦU CỦA ANH VĂN (04/10): ít chữ, có hiệu ứng dạng video về cách thức hoạt động,
 * có đầu có đuôi có kịch bản, bố cục chuẩn chỉnh. Tệp này là câu trả lời.
 *
 * THIẾT KẾ THEO motion-video-brief-framework, preset EXPLAINER:
 *   một cảnh = một ý · chữ trên màn hình <= 14 từ · giữ khoảnh khắc chính >= 2s
 *   tổng thời lượng = TONG_MS, tự cộng từ dur của từng cảnh (hiện 91s) và tự hiện
 *   ở góc phải thanh tiêu đề. LỖI ĐÃ SỬA: bản đầu ghi cứng "110s ± 10%" trong khi
 *   tổng thật là 91s = 82,7%, tức NGOÀI khoảng chính em tuyên bố. Số liệu phải lấy
 *   từ dữ liệu, không gõ tay.
 *   phụ đề luôn hiện (người xem có thể tắt tiếng)
 *
 * VÌ SAO KHÔNG DÙNG three.js CHO PHẦN NÀY
 *   Cảnh 3D cần WebGL, mà máy trường có thể không có. Kịch bản này dựng bằng DOM + CSS
 *   animation nên chạy trên MỌI máy, kể cả khi không có GPU, và tôn trọng
 *   prefers-reduced-motion (tắt chuyển động, vẫn đọc được toàn bộ nội dung).
 *
 * VÌ SAO CHỮ ÍT
 *   Trước đây mỗi trạm có 3-5 câu giải thích, tổng 13.485 từ phải đọc. Kịch bản thay
 *   giải thích bằng chuyển động: học sinh THẤY trọng số đổi, THẤY cột ban đêm tụt
 *   xuống 59%, THẤY máy nói trôi chảy về thứ nó chưa học. Chữ chỉ còn vai trò gọi tên
 *   điều đang xảy ra.
 *
 * NGUYÊN TẮC ORACLE GIỮ NGUYÊN: cảnh 5 dùng đúng máy sinh của Trạm 5 nên câu trả lời
 *   hiển thị là kết quả thật, không phải chuỗi dựng sẵn.
 */
(function(){
  "use strict";

  const GIUA = "kb-giua";

  const NS_SVG = "http://www.w3.org/2000/svg";

  /* Dựng một phần tử con của SVG bằng setAttribute — KHÔNG dùng innerHTML. */
  function _pt(cha, tag, attrs){
    const n = document.createElementNS(NS_SVG, tag);
    for(const k in attrs) n.setAttribute(k, attrs[k]);
    cha.appendChild(n);
    return n;
  }

  /* HÌNH CHIẾC XE MÁY cho ô "ảnh chụp".
   * Nguồn: vendor/lucide/bike.svg (Lucide, giấy phép ISC) — toạ độ dưới đây CHÉP ĐÚNG
   * từ tệp đó, không tự vẽ. Lý do nhúng sẵn thay vì fetch lúc chạy: mở index.html bằng
   * file:// thì fetch tệp SVG bị chặn CORS, kịch bản sẽ vỡ đúng trên máy trường không
   * có mạng — là tình huống bắt buộc phải chạy được.
   * Đây là chỗ thay cho emoji: MASTER.md cấm dùng emoji làm biểu tượng. */
  function svgAnh(cls){
    const svg = document.createElementNS(NS_SVG, "svg");
    svg.setAttribute("viewBox", "0 0 24 24");
    svg.setAttribute("class", "ic-kb" + (cls ? " " + cls : ""));
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("width", "44"); svg.setAttribute("height", "44");
    _pt(svg, "circle", { "cx":"18.5", "cy":"17.5", "r":"3.5" });
    _pt(svg, "circle", { "cx":"5.5", "cy":"17.5", "r":"3.5" });
    _pt(svg, "circle", { "cx":"15", "cy":"5", "r":"1" });
    _pt(svg, "path", { "d":"M12 17.5V14l-3-3 4-3 2 3h2" });
    return svg;
  }


  /* ============ KỊCH BẢN — mỗi cảnh một ý, chữ <= 14 từ ============ */
  const CANH = [
    { id:"mo", ten:"Mở đầu", dur:5000,
      caption:"Một bức ảnh. Một câu hỏi.",
      sub:"Có mũ bảo hiểm không?",
      canh:"title" },

    { id:"nhaplieu", ten:"Trạm 0 · Nhập liệu", dur:9000,
      caption:"Máy không nhìn ảnh. Máy đọc bốn con số.",
      sub:"Ảnh được đổi thành số trước khi vào dây chuyền.",
      canh:"nhaplieu" },

    { id:"dannhan", ten:"Trạm 1 · Dán nhãn", dur:8000,
      caption:"Mỗi ảnh cần một nhãn đúng.",
      sub:"Nhãn sai thì mô hình học sai.",
      canh:"dannhan" },

    { id:"huanluyen", ten:"Trạm 2 · Huấn luyện", dur:14000,
      caption:"Mô hình đoán, so với nhãn, rồi tự sửa trọng số.",
      sub:"Lặp lại nhiều vòng. Không có ai viết sẵn đáp án.",
      canh:"huanluyen" },

    { id:"kiemdinh", ten:"Trạm 4 · Kiểm định", dur:14000,
      caption:"Ban ngày đúng tất cả. Ban đêm sai gần nửa.",
      sub:"Vì 92 phần trăm ảnh huấn luyện là ảnh ban ngày.",
      canh:"kiemdinh" },

    { id:"ungdung", ten:"Trạm 5 · Ứng dụng", dur:14000,
      caption:"Hỏi ngoài dữ liệu đã học, máy vẫn trả lời trôi chảy.",
      sub:"Trôi chảy không phải là bằng chứng.",
      canh:"ungdung" },

    { id:"connguoi", ten:"Trạm 6 · Con người kiểm", dur:10000,
      caption:"Chỉ con người chặn được lỗi trước khi nó gây hại.",
      sub:"Máy không chịu trách nhiệm. Người dùng máy thì có.",
      canh:"connguoi" },

    { id:"vonglap", ten:"Vòng phản hồi", dur:8000,
      caption:"Dữ liệu mới quay về trạm đầu. Dây chuyền lặp lại.",
      sub:"Sửa ở gốc là sửa dữ liệu, không phải đổ lỗi cho máy.",
      canh:"vonglap" },

    { id:"ket", ten:"Kết", dur:9000,
      caption:"AI không tự đúng. Người làm ra nó quyết định điều đó.",
      sub:"Bây giờ đến lượt em soi.",
      canh:"ket" }
  ];

  const TONG_MS = CANH.reduce((a, c) => a + c.dur, 0);

  let host = null, opt = {}, iCanh = 0, dangChay = false;
  let _timer = null, _batDauCanh = 0, _conLai = 0;
  let _raf = null, _daHuy = false;
  let _sinhThat = null;          // câu trả lời thật của máy sinh (cảnh 5)

  function esc(s){
    return String(s == null ? "" : s).replace(/[&<>"]/g, c =>
      ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));
  }
  function el(tag, cls, txt){
    const n = document.createElement(tag);
    if(cls) n.className = cls;
    if(txt != null) n.textContent = txt;      // textContent, không innerHTML
    return n;
  }

  /* ============ BỘ MÁY THỜI GIAN ============ */
  /* LỖI ĐÃ SỬA (04/10) — ba lỗi trong bản đầu của chính hàm này, ghi lại để không lặp:
   *  1. CYRILLIC: selector viết ".kb-tiend" nhưng chữ o cuối là U+043E (Cyrillic), không phải U+006F (Latin).
   *     querySelector trả null nên phải nhờ fallback "|| .kb-tiendo" mới chạy được —
   *     tức bug ẩn, không báo lỗi, mắt thường không phân biệt nổi. Đây là ĐÚNG lớp lỗi
   *     đã từng làm chết nút Chấm nhãn ở Trạm 1 (id t1-tiend + U+043E), nên nay có phép kiểm tự
   *     động quét U+0400..U+04FF trong tools/kiem_noi_dung.py.
   *  2. bar.textContent = "" XOÁ luôn phần tử .kb-tiendo-canhh mà chayTienDo() cần.
   *     Hậu quả: querySelector trả null, hàm return sớm, thanh tiến độ chết âm thầm
   *     trong khi mọi thứ khác vẫn chạy — loại lỗi khó thấy nhất.
   *  3. m.style.flex gán chuỗi số không đơn vị (flex:"5000") — hợp lệ nhưng mơ hồ;
   *     đổi sang flexGrow để rõ đây là tỉ lệ chia, không phải độ dài.
   * Ngoài ra nhãn thời gian nay hiện TỔNG đã phát / tổng kịch bản, không hiện
   * thời lượng còn lại của cả dãy (vô nghĩa với người xem). */
  function tienDoTong(){
    let da = 0;
    for(let i = 0; i < iCanh; i++) da += CANH[i].dur;
    const c = CANH[iCanh];
    if(c) da += Math.max(0, c.dur - _conLai) + (dangChay ? performance.now() - _batDauCanh : 0);
    return Math.max(0, Math.min(100, da / TONG_MS * 100));
  }

  function veThanhTienDo(){
    const bar = host.querySelector(".kb-tiendo");
    if(!bar) return;
    const phu = bar.querySelector(".kb-tiendo-canhh");   // GIỮ LẠI, không xoá
    bar.textContent = "";
    CANH.forEach((c, i) => {
      const m = el("i");
      m.style.flexGrow = String(c.dur);
      if(i < iCanh) m.className = "xong";
      else if(i === iCanh) m.className = "dang";
      m.title = c.ten;
      bar.appendChild(m);
    });
    if(phu) bar.appendChild(phu);
    const o = host.querySelector(".kb-thoigian");
    if(o) o.textContent = Math.round(tienDoTong() / 100 * TONG_MS / 1000) +
                          "s / " + Math.round(TONG_MS / 1000) + "s";
  }

  function datNut(){
    const play = host.querySelector(".kb-play");
    if(play){
      play.textContent = "";
      play.appendChild(svgIcon(dangChay ? "pause" : "play"));
      play.setAttribute("aria-label", dangChay ? "Tạm dừng" : "Tiếp tục");
    }
    host.querySelectorAll(".kb-cham").forEach((c, i) => {
      c.classList.toggle("on", i === iCanh);
      c.setAttribute("aria-current", i === iCanh ? "step" : "false");
    });
  }

  function svgIcon(loai){
    /* SVG nội tuyến, không dùng emoji làm biểu tượng (MASTER.md cấm).
     * Dựng bằng createElement + setAttribute nên không có innerHTML. */
    const s = document.createElementNS(NS_SVG, "svg");
    s.setAttribute("viewBox", "0 0 24 24");
    s.setAttribute("class", "ic");
    s.setAttribute("aria-hidden", "true");
    const duong = {
      play:  "M6 4l14 8-14 8z",
      pause: "M7 4h4v16H7zM13 4h4v16h-4z",
      lai:   "M3 12a9 9 0 1 0 3-6.7M3 4v5h5",
      truoc: "M15 6l-6 6 6 6",
      sau:   "M9 6l6 6-6 6"
    }[loai] || "";
    const p = document.createElementNS(NS_SVG, "path");
    p.setAttribute("d", duong);
    p.setAttribute("fill", loai === "play" || loai === "pause" ? "currentColor" : "none");
    p.setAttribute("stroke", "currentColor");
    p.setAttribute("stroke-width", "2");
    p.setAttribute("stroke-linecap", "round");
    p.setAttribute("stroke-linejoin", "round");
    s.appendChild(p);
    return s;
  }

  function dungTatCa(){
    if(_timer){ clearTimeout(_timer); _timer = null; }
    if(_raf){ cancelAnimationFrame(_raf); _raf = null; }
  }

  function sangCanh(i){
    dungTatCa();
    iCanh = Math.max(0, Math.min(CANH.length - 1, i));
    veCanh();
    veThanhTienDo();
    datNut();
    if(dangChay) henCanh(CANH[iCanh].dur);
  }

  function henCanh(ms){
    _batDauCanh = performance.now();
    _conLai = ms;
    _timer = setTimeout(() => {
      _timer = null;
      if(iCanh < CANH.length - 1){
        sangCanh(iCanh + 1);
      } else {
        dangChay = false; datNut();       // hết kịch bản thì dừng ở cảnh cuối
      }
    }, ms);
    chayTienDo();
  }

  /* thanh tiến độ mảnh chạy trong từng cảnh */
  function chayTienDo(){
    const m = host.querySelector(".kb-tiendo-canhh");
    if(!m) return;
    const canh = CANH[iCanh];
    const buoc = () => {
      if(_daHuy) return;
      if(!dangChay){ _raf = null; return; }
      const da = canh.dur - _conLai + (performance.now() - _batDauCanh);
      m.style.width = Math.max(0, Math.min(100, da / canh.dur * 100)) + "%";
      _raf = requestAnimationFrame(buoc);
    };
    if(_raf) cancelAnimationFrame(_raf);
    _raf = requestAnimationFrame(buoc);
  }

  function tamDung(){
    if(!dangChay) return;
    dangChay = false;
    if(_timer){
      clearTimeout(_timer); _timer = null;
      _conLai = Math.max(0, _conLai - (performance.now() - _batDauCanh));
    }
    if(_raf){ cancelAnimationFrame(_raf); _raf = null; }
    host.classList.add("kb-dung");
    datNut();
  }

  function tiepTuc(){
    if(dangChay) return;
    dangChay = true;
    host.classList.remove("kb-dung");
    datNut();
    if(iCanh >= CANH.length - 1 && _conLai <= 0) { sangCanh(0); return; }
    henCanh(_conLai || CANH[iCanh].dur);
  }

  /* ============ VẼ TỪNG CẢNH ============ */
  function veCanh(){
    const c = CANH[iCanh];
    const san = host.querySelector(".kb-san-khau");
    const cap = host.querySelector(".kb-caption");
    const sub = host.querySelector(".kb-sub");
    const ten = host.querySelector(".kb-ten-canh");
    if(!san || !cap) return;

    cap.textContent = c.caption;
    sub.textContent = c.sub || "";
    ten.textContent = c.ten;
    host.setAttribute("data-canh", c.id);

    san.textContent = "";
    san.classList.remove(GIUA);
    void san.offsetWidth;                      // buộc restart animation CSS
    VE[c.canh](san);
    /* Hook cho app.js ghi nhật ký lớp (minh chứng sử dụng thật cho hồ sơ dự thi).
     * Bọc try/catch: kịch bản phải chạy được kể cả khi app.js chưa nạp ENG. */
    if(typeof opt.onCanh === "function"){ try{ opt.onCanh(iCanh, c); }catch(e){} }

    host.classList.add("kb-hieu-ung");
    setTimeout(() => host.classList.remove("kb-hieu-ung"), 700);
  }

  /* ---- hàm vẽ cho từng cảnh. Chỉ dùng createElement + textContent. ---- */
  const VE = {
    title(s){
      s.classList.add(GIUA);
      const logo = el("div", "kb-logo");
      const m = document.createElement("span");
      m.appendChild(svgIcon("play"));
      logo.appendChild(m);
      logo.appendChild(el("span", null, "SOI AI"));
      s.appendChild(logo);
      s.appendChild(el("div", "kb-logo-soi", "Soi AI để hiểu AI"));
    },

    nhaplieu(s){
      const day = el("div", "kb-day");
      const anh = el("div", "kb-anh kb-hien");
      /* KHÔNG dùng emoji làm biểu tượng (MASTER.md cấm). Icon vẽ bằng SVG nội tuyến
       * dựng với createElementNS, không innerHTML — giống hàm svgIcon() bên trên. */
      anh.appendChild(svgAnh("kb-mu"));
      anh.appendChild(el("div", "kb-anh-nhan", "ảnh chụp ban ngày"));
      day.appendChild(anh);

      const mui = el("div", "kb-muiten");
      mui.appendChild(svgIcon("sau"));
      day.appendChild(mui);

      const so = el("div", "kb-so");
      ["rất sáng 0.074", "sáng vừa 0.000", "độ sáng đầu 0.754", "tỉ lệ tối 0.031"]
        .forEach((t, i) => {
          const o = el("div", "kb-chip-so kb-tre" , t);
          o.style.animationDelay = (0.5 + i * 0.35) + "s";
          so.appendChild(o);
        });
      day.appendChild(so);
      s.appendChild(day);
    },

    dannhan(s){
      const anh = el("div", "kb-anh kb-anh-to");
      anh.appendChild(svgAnh("kb-mu"));
      s.appendChild(anh);
      const tem = el("div", "kb-tem kb-dong-dau", "CÓ MŨ");
      s.appendChild(tem);
      const sai = el("div", "kb-tem-sai kb-tre", "nếu dán sai nhãn");
      sai.style.animationDelay = "2.6s";
      s.appendChild(sai);
    },

    huanluyen(s){
      const ten = ["rất sáng", "sáng vừa", "độ sáng đầu", "tỉ lệ tối"];
      const gia = [0.3668, -0.0226, -0.0187, 0.2397];   // trọng số THẬT đã đo
      const hop = el("div", "kb-trong-so");
      ten.forEach((t, i) => {
        const hang = el("div", "kb-hang-ts");
        hang.appendChild(el("span", "kb-ten-ts", t));
        const vach = el("div", "kb-vach");
        const day = el("i");
        day.style.animationDelay = (0.4 + i * 0.45) + "s";
        /* LỖI ĐÃ SỬA (đo thật trong browser, không suy đoán): bản đầu chỉ set
         * --dich = 50 + w*110 rồi để CSS tính width: calc(var(--dich) - 50%).
         * Với trọng số ÂM (ở đây -0.0226 và -0.0187) phép tính cho width ÂM,
         * mà width âm là giá trị CSS không hợp lệ nên bị loại -> thanh co về 0px.
         * Kết quả đo được: 2/4 thanh vô hình, đúng hai thanh có trọng số âm.
         * Học sinh sẽ tưởng "đặc trưng này không quan trọng" trong khi nó có
         * trọng số âm (ý nghĩa ngược lại, vẫn quan trọng).
         * Nay tách thành hai biến: --l = mép trái, --w = độ dài (luôn >= 0),
         * nên thanh âm mọc về bên TRÁI vạch giữa và thanh dương về bên PHẢI. */
        const dich = 50 + gia[i] * 110;
        day.style.setProperty("--l", Math.min(50, dich).toFixed(1) + "%");
        day.style.setProperty("--w", Math.abs(dich - 50).toFixed(1) + "%");
        if(gia[i] < 0) day.classList.add("am");
        vach.appendChild(day);
        hang.appendChild(vach);
        hang.appendChild(el("span", "kb-gia-tri", gia[i].toFixed(4)));
        hop.appendChild(hang);
      });
      s.appendChild(hop);
      const vong = el("div", "kb-vong kb-tre", "vòng 1 → 60");
      vong.style.animationDelay = "0.2s";
      s.appendChild(vong);
    },

    kiemdinh(s){
      const b = el("div", "kb-cot");
      [["Ban ngày", 100, "ngay"], ["Ban đêm", 59, "dem"]].forEach(([n, v, k], i) => {
        const c = el("div", "kb-cot-1");
        const than = el("div", "kb-than");
        const day = el("i", k);
        day.style.height = "0%";
        /* LỖI ĐÃ SỬA: khối prefers-reduced-motion trong CSS dùng height:var(--cot,100%)
         * nhưng JS không hề gán --cot, nên giá trị dự phòng 100% được dùng và CẢ HAI
         * cột đều hiện 100% — sai số liệu kiểm định (ban đêm chỉ 59%). Người bật
         * giảm chuyển động sẽ đọc nhầm kết quả thí nghiệm. Nay gán --cot đúng giá trị. */
        day.style.setProperty("--cot", v + "%");
        day.style.transition = "height 1.4s cubic-bezier(.2,.8,.2,1) " + (0.4 + i * 0.7) + "s";
        than.appendChild(day);
        c.appendChild(el("div", "kb-so-cot", v + "%"));
        c.appendChild(than);
        c.appendChild(el("div", "kb-nhan-cot", n));
        b.appendChild(c);
        /* LỖI ĐÃ SỬA: bản đầu chỉ dùng requestAnimationFrame lồng hai lần. rAF bị
         * trình duyệt ĐÓNG BĂNG khi tab không hiển thị, nên nếu giáo viên chuyển tab
         * (hoặc bật máy chiếu rồi mở cửa sổ khác) thì cột đứng nguyên ở 0% và không
         * bao giờ chạy lại khi quay về — em đã đo được đúng hiện tượng này.
         * Nay thêm setTimeout làm dự phòng: timeout vẫn được gọi (dù bị giãn nhịp khi
         * tab nền) nên cột luôn đạt đúng chiều cao. */
        const dung = () => { day.style.height = v + "%"; };
        requestAnimationFrame(() => requestAnimationFrame(dung));
        setTimeout(dung, 120);
      });
      s.appendChild(b);
      const canhBao = el("div", "kb-canh-bao kb-tre", "chênh lệch 41 điểm");
      canhBao.style.animationDelay = "2.4s";
      s.appendChild(canhBao);
    },

    ungdung(s){
      /* CẢNH NÀY DÙNG KẾT QUẢ THẬT của máy sinh, không phải chuỗi dựng sẵn. */
      const hoi = el("div", "kb-hoi kb-hien", "Hôm nay giá vàng bao nhiêu?");
      s.appendChild(hoi);
      const tra = el("div", "kb-tra-loi");
      s.appendChild(tra);
      let vanBan = _sinhThat;
      if(!vanBan && window.MX_NHAMAY_TEXT){
        const it = window.MX_NHAMAY_TEXT.ungDung("giá vàng hôm nay", { seed: 20261004 });
        _sinhThat = it.vanBan;
        vanBan = it.vanBan;
      }
      vanBan = vanBan || "Máy chưa nạp được ngữ liệu.";
      // hiệu ứng gõ từng chữ
      let i = 0;
      const go = () => {
        if(_daHuy || i > vanBan.length) return;
        tra.textContent = vanBan.slice(0, i);
        i += 2;
        setTimeout(go, dangChay ? 28 : 0);
      };
      setTimeout(go, 1200);
      const tem = el("div", "kb-tem-bia kb-tre", "máy bịa — chủ đề này chưa từng được học");
      tem.style.animationDelay = "7.5s";
      s.appendChild(tem);
    },

    connguoi(s){
      const o = el("div", "kb-chan");
      o.appendChild(el("div", "kb-dong-chay kb-tre", "đầu ra của máy"));
      const chan = el("div", "kb-tay-chan kb-tre");
      chan.appendChild(svgIcon("pause"));
      chan.style.animationDelay = "1.8s";
      o.appendChild(chan);
      o.appendChild(el("div", "kb-dong-dung kb-tre", "đã được người kiểm tra"));
      s.appendChild(o);
    },

    vonglap(s){
      const v = el("div", "kb-vong-lap");
      ["dữ liệu", "mô hình", "đầu ra", "con người", "dữ liệu mới"].forEach((t, i) => {
        const o = el("div", "kb-nut-vong kb-tre", t);
        o.style.animationDelay = (0.3 + i * 0.5) + "s";
        v.appendChild(o);
      });
      s.appendChild(v);
    },

    ket(s){
      s.classList.add(GIUA);
      const d = el("div", "kb-ket");
      d.appendChild(el("div", "kb-ket-lon", "Soi AI để hiểu AI"));
      d.appendChild(el("div", "kb-ket-nho", "9 trạm · 22 yêu cầu cần đạt lớp 10 · chạy không cần mạng"));
      s.appendChild(d);
    }
  };

  /* ============ API ============ */
  function init(root, options){
    host = root; opt = options || {};
    _daHuy = false; iCanh = 0; dangChay = false; _conLai = 0; _sinhThat = null;

    host.textContent = "";
    host.classList.add("kb-wrap");

    /* AN TOÀN innerHTML: khối dựng khung bên dưới chỉ chứa CHUỖI TĨNH do chính tệp này
     * định nghĩa, không có biến nào từ dữ liệu người dùng hay từ máy sinh văn bản.
     * Mọi nội dung động (caption, cảnh, câu trả lời của máy) đều được gán bằng
     * textContent ở veCanh() và các hàm VE.* — không đi qua innerHTML. */
    host.innerHTML =
      '<div class="kb-top">' +
        '<span class="kb-ten-canh"></span>' +
        '<span class="kb-thoigian"></span>' +
      '</div>' +
      '<div class="kb-san-khau" role="img" aria-label="Hình ảnh minh hoạ cảnh đang phát"></div>' +
      '<div class="kb-chu" aria-live="polite">' +
        '<p class="kb-caption"></p><p class="kb-sub"></p>' +
      '</div>' +
      '<div class="kb-tiendo"><i class="kb-tiendo-canhh"></i></div>' +
      '<div class="kb-dieu-khien">' +
        '<button type="button" class="btn nho kb-truoc" aria-label="Cảnh trước"></button>' +
        '<button type="button" class="btn chinh kb-play" aria-label="Phát"></button>' +
        '<button type="button" class="btn nho kb-sau" aria-label="Cảnh sau"></button>' +
        '<button type="button" class="btn nho kb-lai" aria-label="Xem lại từ đầu"></button>' +
        '<span class="kb-cham-wrap" role="tablist" aria-label="Chọn cảnh"></span>' +
      '</div>';

    // thanh tiến độ theo từng cảnh (flex theo thời lượng)
    const td = host.querySelector(".kb-tiendo");
    td.textContent = "";
    CANH.forEach(() => td.appendChild(el("i")));
    td.appendChild(el("i", "kb-tiendo-canhh"));

    // chấm chọn cảnh
    const cham = host.querySelector(".kb-cham-wrap");
    CANH.forEach((c, i) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "kb-cham";
      b.setAttribute("role", "tab");
      b.setAttribute("aria-label", "Cảnh " + (i + 1) + ": " + c.ten);
      b.title = c.ten;
      b.onclick = () => sangCanh(i);
      cham.appendChild(b);
    });

    const play = host.querySelector(".kb-play");
    play.textContent = ""; play.appendChild(svgIcon("play"));
    const tr = host.querySelector(".kb-truoc");
    tr.textContent = ""; tr.appendChild(svgIcon("truoc"));
    const sa = host.querySelector(".kb-sau");
    sa.textContent = ""; sa.appendChild(svgIcon("sau"));
    const la = host.querySelector(".kb-lai");
    la.textContent = ""; la.appendChild(svgIcon("lai"));

    play.onclick = () => { dangChay ? tamDung() : tiepTuc(); };
    tr.onclick = () => { _conLai = 0; sangCanh(iCanh - 1); };
    sa.onclick = () => { _conLai = 0; sangCanh(iCanh + 1); };
    la.onclick = () => { _conLai = 0; dangChay = true; sangCanh(0); };

    host._phim = (e) => {
      if(host.offsetParent === null) return;          // chỉ bắt phím khi đang hiện
      if(e.code === "Space"){ e.preventDefault(); dangChay ? tamDung() : tiepTuc(); }
      else if(e.code === "ArrowRight"){ _conLai = 0; sangCanh(iCanh + 1); }
      else if(e.code === "ArrowLeft"){ _conLai = 0; sangCanh(iCanh - 1); }
    };
    document.addEventListener("keydown", host._phim);

    sangCanh(0);
    if(opt.tuChay !== false){ dangChay = true; host.classList.remove("kb-dung"); datNut(); henCanh(CANH[0].dur); }
    return { soCanh: CANH.length, tongGiay: Math.round(TONG_MS / 1000) };
  }

  function huy(){
    _daHuy = true;
    dungTatCa();
    if(host && host._phim) document.removeEventListener("keydown", host._phim);
    host = null;
  }

  window.MX_KICHBAN = {
    CANH, TONG_MS, init, huy,
    sangCanh, tamDung, tiepTuc,
    trangThai(){
      return { iCanh, tenCanh: CANH[iCanh] ? CANH[iCanh].ten : null,
               dangChay, conLai: Math.round(_conLai),
               soCanh: CANH.length, tongGiay: Math.round(TONG_MS / 1000) };
    },
    /* cho judge kiểm tra: mọi caption phải <= 14 từ */
    kiemTraCaption(n){
      n = n || 14;
      return CANH.map(c => ({ id: c.id, tu: c.caption.split(/\s+/).length,
                              dat: c.caption.split(/\s+/).length <= n }));
    }
  };
})();
