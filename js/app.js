/* SOI AI — app chính: điều hướng + 3 tầng giao diện.
 * Chạy hoàn toàn offline qua file:// (mở bằng trình duyệt từ USB/máy trường).
 * GHI CHÚ AN TOÀN (innerHTML): app 100% offline, không có nội dung từ mạng.
 * Chuỗi do người dùng nhập (mã HS/lớp) luôn đi qua esc() trước khi chèn vào innerHTML;
 * dữ liệu còn lại là hằng số tĩnh từ data/*.js của chính sản phẩm → không có vectơ XSS. */
(function(){
  "use strict";
  const META = window.MX_META, ENG = window.MX_ENGINE, LAB = window.MX_LAB;

  let maHS = "", maLop = "";
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
  const pct = (x) => x===null||x===undefined ? "—" : Math.round(x*100) + "%";

  /* ================= ĐIỀU HƯỚNG ================= */
  const CAC_VIEW = ["v-home","v-nhap","v-lab","v-dautruong","v-baocao","v-logic",
                    "v-kienthuc","v-tinhhuong","v-lab3d","v-pipe3d","v-nhamay","v-kichban","v-gioithieu"];
  function hien(view){
    CAC_VIEW.forEach(id=>{
      const el = $(id); if(el) el.style.display = (id===view) ? "" : "none";
    });
    /* 3D tốn GPU: khi rời scene thì giải phóng, vào lại thì dựng mới.
     * Đây là lí do mỗi scene có init/huy riêng — tránh rò rỉ bộ nhớ khi đổi tab liên tục. */
    /* Kịch bản có setTimeout + requestAnimationFrame: rời view thì phải tạm dừng, nếu
     * không timer vẫn chạy ngầm, vừa tốn pin vừa làm cảnh tự chuyển khi quay lại. */
    if(view !== "v-kichban" && kbDaNap){ try{ window.MX_KICHBAN.tamDung(); }catch(e){} }
    if(view !== "v-lab3d" && lab3dDaKhoiTao){ try{ window.MX_LAB3D.huy(); }catch(e){} lab3dDaKhoiTao = false; }
    if(view !== "v-pipe3d" && pipe3dDaKhoiTao){ try{ window.MX_PIPE3D.huy(); }catch(e){} pipe3dDaKhoiTao = false; }
    window.scrollTo(0,0);
  }

  function dangNhap(){
    const hs = $("in-maHS").value.trim();
    const lop = $("in-maLop").value.trim();
    if(!hs){ alert("Em hãy nhập mã của mình (ví dụ A001)."); return; }
    maHS = hs.toUpperCase(); maLop = lop.toUpperCase() || maLop;
    ENG.vaoLop(maHS, maLop);
    $("lbl-user").textContent = `${maHS}${maLop? " · "+maLop : ""}`;
    hien("v-home");
  }

  /* ================= TẦNG 1 — XƯỞNG HUẤN LUYỆN ================= */
  const lab = { model:null, train:null, testNgay:null, testDem:null, kqTrain:null, kqNgay:null, kqDem:null,
                trainC2:null, kqDemC2:null, daTraLoi:{} };

  function veThumb(ds, n, where){
    where.innerHTML = "";
    for(let i=0;i<Math.min(n, ds.length);i++){
      const w = document.createElement("div"); w.className="thumb";
      const c = ds[i].canvas.cloneNode(); c.width=ds[i].canvas.width; c.height=ds[i].canvas.height;
      c.getContext("2d").drawImage(ds[i].canvas,0,0);
      w.appendChild(c);
      const t = document.createElement("div");
      t.className="nho chu2";
      t.textContent = (ds[i].kind==="mbh"?"có mũ":"không mũ") + " · " + ds[i].light;
      w.appendChild(t);
      where.appendChild(w);
    }
  }

  function labBuoc(b){
    [1,2,3,4].forEach(i=>{
      $("lab-b"+i).style.display = (i===b) ? "" : "none";
      const s = $("st-"+i); if(s) s.className = "step" + (i<=b?" on":"");
    });
  }

  function labTaoDuLieu(){
    lab.train = LAB.taoDuLieu({ soLuong: 60, lechAnhSang: true, seed: 20261004 });
    lab.testNgay = LAB.taoDuLieu({ soLuong: 10, light: "ngay", seed: 777 });
    lab.testDem  = LAB.taoDuLieu({ soLuong: 10, light: "dem",  seed: 888 });
    // thống kê lệch
    const ngay = lab.train.filter(d=>d.light==="ngay").length;
    $("lab-thongke").innerHTML =
      `Bộ dữ liệu huấn luyện: <b>${lab.train.length} ảnh</b> — trong đó <b class="vang">${ngay} ảnh ban ngày (${pct(ngay/lab.train.length)})</b> và chỉ <b>${lab.train.length-ngay} ảnh ban đêm</b>.<br>` +
      `Bộ kiểm thử: ${lab.testNgay.length} ảnh ban NGÀY và ${lab.testDem.length} ảnh ban ĐÊM (giữ riêng, mô hình chưa từng thấy).`;
    veThumb(lab.train, 10, $("lab-thumbs"));
    labBuoc(2);
  }

  function labHuanLuyen(){
    lab.model = new LAB.Perceptron();
    lab.model.hoc({ duLieu: lab.train.map(d=>({ f: d.f, nhan: d.nhan })), vong: LAB.EPOCHS });
    lab.kqTrain = LAB.kiemTra(lab.model, lab.train);
    lab.kqNgay  = LAB.kiemTra(lab.model, lab.testNgay);
    lab.kqDem   = LAB.kiemTra(lab.model, lab.testDem);
    $("kq-train").textContent = pct(lab.kqTrain.doChinhXac);
    $("kq-ngay").textContent  = pct(lab.kqNgay.doChinhXac);
    $("kq-dem").textContent   = pct(lab.kqDem.doChinhXac);
    $("bar-dem").style.width = Math.round(lab.kqDem.doChinhXac*100)+"%";
    $("bar-ngay").style.width = Math.round(lab.kqNgay.doChinhXac*100)+"%";
    ENG.logSuKien(maHS, { loai:"huanLuyen", cheDo:"lech", doChinhXacTrain: lab.kqTrain.doChinhXac, ngay: lab.kqNgay.doChinhXac, dem: lab.kqDem.doChinhXac });
    labBuoc(3);
  }

  function labSoSanh(){
    lab.trainC2 = LAB.taoDuLieu({ soLuong: 60, lechAnhSang: false, seed: 31071975 });
    const m2 = new LAB.Perceptron();
    m2.hoc({ duLieu: lab.trainC2.map(d=>({f:d.f, nhan:d.nhan})), vong: LAB.EPOCHS });
    lab.kqDemC2 = LAB.kiemTra(m2, lab.testDem);
    $("kq-dem-c2").textContent = pct(lab.kqDemC2.doChinhXac);
    $("bar-dem2").style.width = Math.round(lab.kqDemC2.doChinhXac*100)+"%";
    $("lab-sosanh").style.display = "";
    ENG.logSuKien(maHS, { loai:"huanLuyen", cheDo:"canBang", dem: lab.kqDemC2.doChinhXac });
  }

  function labCauHoi(){
    const box = $("lab-cauhoi"); box.innerHTML = "";
    LAB.nhiemVu.forEach((nv, idx)=>{
      const c = document.createElement("div"); c.className="card";
      c.innerHTML = `<h3>Câu ${idx+1}. ${esc(nv.ten)}</h3>
        <p class="chu2">${esc(nv.noiDung)}</p>
        <p><b>${esc(nv.cauHoi)}</b></p>
        <div class="chips" id="chip-${nv.id}"></div>
        <div id="fb-${nv.id}"></div>`;
      box.appendChild(c);
      const chips = c.querySelector(".chips");
      nv.luaChon.forEach(l=>{
        const b = document.createElement("button"); b.className="chip"; b.textContent = l.text;
        b.onclick = ()=>{
          if(lab.daTraLoi[nv.id]) return;
          lab.daTraLoi[nv.id] = true;
          const kq = ENG.chamLab(nv, l.id);
          [...chips.children].forEach((ch,i)=>{
            ch.classList.remove("chon");
            if(nv.luaChon[i].id === nv.dapAn) ch.style.borderColor = "var(--dung)";
            if(nv.luaChon[i].id === l.id && l.id !== nv.dapAn) ch.style.borderColor = "var(--sai)";
            ch.style.cursor = "default";
          });
          const fb = c.querySelector(".fb") || (()=>{ const d=document.createElement("div"); d.className="fb"; c.querySelector("[id^=fb-]").appendChild(d); return d; })();
          fb.className = "phanhoi " + (kq.dung ? "dung" : "sai");
          fb.innerHTML = (kq.dung ? svgIco("check") + " <b>Chính xác!</b> "
                            : svgIco("x") + " <b>Chưa đúng.</b> ") + esc(nv.giaiThich);
          ENG.logSuKien(maHS, { loai:"lab", nhiemVu:{id:nv.id, mach:nv.mach, unesco:nv.unesco}, kq });
        };
        chips.appendChild(b);
      });
    });
    labBuoc(4);
  }

  /* ================= TẦNG 2 — ĐẤU TRƯỜNG BẮT LỖI AI ================= */
  const dt = { ds:[], i:0, traLoi:{ verdict:null, loaiLoi:null, claimChon:-1 }, ketQua:[], seedNgay:null, mode:"luyen" };

  /* Chọn phiên 12 câu phân tầng: đủ 5 loại lỗi + ~1/3 câu đúng (đo "bắt oan").
     Tất định theo seed → tái lập được cho pre/post và cho báo cáo hồ sơ. */
  function dtChonPhien(seed){
    const bank = window.MX_BANK;
    let s = seed >>> 0;
    const rnd = () => (s = (s*1664525 + 1013904223) >>> 0) / 4294967296;
    const shuffle = (a)=>{ a=a.slice(); for(let i=a.length-1;i>0;i--){ const j=Math.floor(rnd()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; } return a; };
    const byType = {};
    for(const k of Object.keys(META.loaiLoi)) byType[k] = [];
    const dung = [];
    for(const it of bank){
      if(it.loai === "dung") dung.push(it);
      else if(byType[it.loaiLoi]) byType[it.loaiLoi].push(it);
    }
    const pick = [];
    // Phân tầng CHÍNH XÁC: mỗi loại lỗi lấy tối thiểu 1 câu (5), sau đó bù luân phiên
    // theo loại cho đến khi đủ 8 câu lỗi → 8 lỗi + 4 đúng = 12 câu, không vỡ tầng.
    const typeKeys = shuffle(Object.keys(byType));
    const queues = {};
    for(const k of typeKeys) queues[k] = shuffle(byType[k]);
    // vòng 1: mỗi loại 1 câu
    for(const k of typeKeys){ if(queues[k].length) pick.push(queues[k].shift()); }
    // vòng 2: bù luân phiên đến 8 câu lỗi
    let ti = 0;
    while(pick.length < 8){
      const k = typeKeys[ti % typeKeys.length]; ti++;
      if(queues[k].length) pick.push(queues[k].shift());
      else if(ti > 50) break; // an toàn: ngân hàng quá mỏng
    }
    // 4 câu đúng (mồi nhử)
    pick.push(...shuffle(dung).slice(0,4));
    return shuffle(pick).slice(0,12);
  }

  function dtBatDau(mode){
    dt.mode = mode || "luyen";
    const today = new Date();
    // seed: pre/post dùng mã phiên khác nhau để không học thuộc vị trí
    dt.seedNgay = today.getFullYear()*10000 + (today.getMonth()+1)*100 + today.getDate()
      + maHS.split("").reduce((a,c)=>a+c.charCodeAt(0),0)*31
      + (dt.mode==="pre" ? 101 : dt.mode==="post" ? 202 : 0);
    dt.ds = dtChonPhien(dt.seedNgay);
    dt.i = 0; dt.ketQua = [];
    // khôi phục UI nếu phiên trước đã kết thúc (nút nộp bị ẩn, onclick bị đổi)
    $("dt-nop").style.display = "";
    $("dt-tiep").onclick = dtTiep;
    $("dt-mode").textContent = dt.mode==="pre" ? "Khảo sát ĐẦU VÀO (pre-test)" : dt.mode==="post" ? "Khảo sát ĐẦU RA (post-test)" : "Luyện tập";
    dtHienCau();
  }

  function dtHienCau(){
    const item = dt.ds[dt.i];
    $("dt-tien-do").textContent = `Câu ${dt.i+1} / ${dt.ds.length}`;
    $("dt-boicanh").textContent = item.boiCanh;
    const box = $("dt-claims"); box.innerHTML = "";
    dt.traLoi = { verdict:null, loaiLoi:null, claimChon:-1 };
    item.claims.forEach((cl, idx)=>{
      const p = document.createElement("p");
      p.className = "claim"; p.textContent = cl; p.title = "Bấm vào câu em nghi là SAI (nếu có)";
      p.onclick = ()=>{
        if($("dt-nop").disabled === false && $("dt-kq").style.display !== "none") return; // đã nộp
        box.querySelectorAll(".claim").forEach(e=>e.classList.remove("chon"));
        p.classList.add("chon");
        dt.traLoi.claimChon = idx;
      };
      box.appendChild(p);
    });
    $("dt-chips-verdict").innerHTML = "";
    ["co_loi","dung"].forEach(v=>{
      const b = document.createElement("button"); b.className="chip";
      b.innerHTML = v==="co_loi" ? svgIco("triangle-alert") + " Có lỗi"
                                 : svgIco("check") + " Không có lỗi";
      b.onclick = ()=>{
        $("dt-chips-verdict").querySelectorAll(".chip").forEach(e=>e.classList.remove("chon"));
        b.classList.add("chon"); dt.traLoi.verdict = v;
        $("dt-chips-loai").style.display = (v==="co_loi") ? "" : "none";
        dtKiemTraNut();
      };
      $("dt-chips-verdict").appendChild(b);
    });
    $("dt-chips-loai").innerHTML = ""; $("dt-chips-loai").style.display="none";
    Object.keys(META.loaiLoi).forEach(k=>{
      const b = document.createElement("button"); b.className="chip";
      b.style.borderColor = META.loaiLoi[k].mau;
      b.textContent = META.loaiLoi[k].ten;
      b.onclick = ()=>{
        $("dt-chips-loai").querySelectorAll(".chip").forEach(e=>e.classList.remove("chon"));
        b.classList.add("chon"); dt.traLoi.loaiLoi = k; dtKiemTraNut();
      };
      $("dt-chips-loai").appendChild(b);
    });
    $("dt-kq").style.display = "none";
    $("dt-nop").disabled = true;
    $("dt-tiep").style.display = "none";
  }

  function dtKiemTraNut(){
    const t = dt.traLoi;
    const hopLe = t.verdict && (t.verdict==="dung" || t.loaiLoi);
    $("dt-nop").disabled = !hopLe;
  }

  function dtNop(){
    const item = dt.ds[dt.i];
    const kq = ENG.chamDauTruong(item, dt.traLoi);
    dt.ketQua.push(kq);
    ENG.logSuKien(maHS, { loai:"dauTruong", kq });
    const box = $("dt-kq"); box.style.display="";
    box.className = "phanhoi " + (kq.diem ? "dung" : "sai");
    let head = kq.diem ? svgIco("check") + " <b>Chính xác!</b> "
                       : svgIco("x") + " <b>Chưa đúng.</b> ";
    if(kq.batOan) head += "Câu này ĐÚNG — em đã 'bắt oan'. ";
    if(kq.boSot) head += "Câu này CÓ lỗi (" + META.loaiLoi[item.loaiLoi].ten + ") — em đã bỏ sót. ";
    box.innerHTML = head + esc(item.giaiThich);
    $("dt-nop").disabled = true;
    $("dt-tiep").style.display = "";
    $("dt-tiep").innerHTML = (dt.i < dt.ds.length-1) ? "Câu tiếp theo →"
                             : svgIco("flag") + " Xem kết quả của em";
  }

  function dtTiep(){
    if(dt.i < dt.ds.length-1){ dt.i++; dtHienCau(); return; }
    dtTongKet();
  }

  function dtTongKet(){
    const dung = dt.ketQua.filter(k=>k.diem).length;
    const batOan = dt.ketQua.filter(k=>k.batOan).length;
    const boSot = dt.ketQua.filter(k=>k.boSot).length;
    // ghi sự kiện tổng kết phiên (pre/post) để báo cáo tiến trình
    ENG.logSuKien(maHS, { loai:"phien", cheDo: dt.mode, tong: dt.ketQua.length,
                          dung: dung, batOan: batOan, boSot: boSot });
    $("dt-tien-do").textContent = "Hoàn thành!";
    $("dt-boicanh").textContent = "";
    $("dt-claims").innerHTML = `
      <div class="grid g3">
        <div class="kpi"><div class="so">${dung}/${dt.ketQua.length}</div><div class="nhan">phán quyết đúng</div></div>
        <div class="kpi"><div class="so ko">${boSot}</div><div class="nhan">lỗi bỏ sót</div></div>
        <div class="kpi"><div class="so vang">${batOan}</div><div class="nhan">câu đúng bị 'bắt oan'</div></div>
      </div>
      <p class="chu2 nho">Kết quả của em đã được ghi vào nhật ký lớp (chỉ lưu mã ${esc(maHS)}, không lưu tên). Thầy/cô sẽ xem báo cáo tổng hợp của cả lớp.</p>`;
    ["dt-chips-verdict","dt-chips-loai"].forEach(id=>$(id).innerHTML="");
    $("dt-kq").style.display="none"; $("dt-nop").style.display="none";
    $("dt-tiep").textContent = "↻ Chơi lại lượt mới";
    $("dt-tiep").onclick = ()=>{ $("dt-nop").style.display=""; $("dt-tiep").onclick = dtTiep; dtBatDau(); };
  }

  /* ================= TẦNG 3 — BÁO CÁO ================= */
  function veBaoCao(){
    const th = ENG.tongHop(maHS);
    const nx = ENG.taoNhanXet(th);
    const box = $("bc-noi-dung");
    let html = `
      <div class="grid g3">
        <div class="kpi"><div class="so">${th.dauTruong.tong}</div><div class="nhan">câu đã phán quyết</div></div>
        <div class="kpi"><div class="so">${pct(th.dauTruong.tiLe)}</div><div class="nhan">mức độ đáp ứng<br><span class="nho chu2">(minh chứng, không phải điểm)</span></div></div>
        <div class="kpi"><div class="so">${th.lab.tong}</div><div class="nhan">nhiệm vụ phòng lab</div></div>
      </div>
      <h3>Khả năng phát hiện theo từng loại lỗi AI</h3>`;
    html += `<table><tr><th>Loại lỗi</th><th>Phát hiện đúng</th><th>Tỉ lệ (recall)</th><th>Bắt oan</th></tr>`;
    for(const r of th.recallTheoLoai){
      html += `<tr><td><span style="color:${META.loaiLoi[r.maLoai].mau}">●</span> ${esc(r.ten)}</td>
        <td>${r.phatHien}/${r.tongCoLoi}</td><td>${pct(r.recall)}</td><td>${r.batOan}</td></tr>`;
    }
    /* ---- BẢN ĐỒ NĂNG LỰC: TRỤC CHÍNH = 13 CHỦ ĐỀ CỦA KHUNG 2422 (QĐ 2422/QĐ-BGDĐT) ----
     * Vì sao đổi trục: giám khảo là người của Bộ, đối chiếu theo mã của Bộ
     * ([lớp].[chủ đề].[thứ tự]). UNESCO AI CFS 2024 chỉ 4 aspects × 3 levels = 12 khối,
     * KHÔNG có C4/C5 nên ánh xạ 1-1 là sai về kĩ thuật → nay chỉ dùng làm cột đối chiếu.
     * NGÔN TỪ: Khung phần VI quy định "không xác lập đầu điểm riêng cho nội dung GD AI"
     * → bảng này chỉ nói "MỨC ĐỘ ĐÁP ỨNG", tuyệt đối không gọi là điểm/xếp loại. */
    const mucDat = (tiLe) => tiLe===null ? '<span class="chu2">chưa có dữ liệu</span>'
      : tiLe>=0.7 ? '<span style="color:var(--dung)"><b>Đáp ứng tốt</b></span>'
      : tiLe>=0.4 ? '<span style="color:var(--vang)"><b>Đáp ứng một phần</b></span>'
                  : '<span style="color:var(--sai)"><b>Cần luyện thêm</b></span>';
    const bar = (tiLe) => tiLe===null ? ''
      : `<div class="bar"><i style="width:${Math.round(tiLe*100)}%;background:${tiLe>=0.7?'var(--dung)':tiLe>=0.4?'var(--vang)':'var(--sai)'}"></i></div>`;

    // dồn số liệu theo chủ đề của Bộ (A1..D2) từ các sự kiện đã ghi mã unesco cũ
    const theoChuDe = {};
    (th.banDoUNESCO||[]).forEach(b=>{ if(b.khoi) theoChuDe[b.khoi] = b; });

    html += `</table>
      <h3>Bản đồ năng lực theo 13 chủ đề — Khung 2422/QĐ-BGDĐT</h3>
      <p class="nho chu2">Trục chính là mã chủ đề của Bộ (lớp 10 có yêu cầu cần đạt ở 10/13 chủ đề).
      Đây là <b>minh chứng mức độ đáp ứng</b>, không phải điểm số và không dùng để xếp loại.</p>
      <table><tr><th>Chủ đề</th><th>Tên chủ đề (nguyên văn Khung)</th><th>Mạch</th><th>Minh chứng</th><th>Mức độ đáp ứng</th></tr>`;
    const Y = window.MX_YCCD;
    if(Y && Y.chuDe){
      for(const cd of Object.keys(Y.chuDe)){
        const b = theoChuDe[cd];
        const coYCCD = (Y.theoChuDe(cd)||[]).length > 0;
        const tenUN = Y.unescoDoiChieu && Y.unescoDoiChieu[cd];
        html += `<tr${coYCCD?'':' style="opacity:.55"'}>
          <td><b>${cd}</b></td>
          <td>${esc(Y.chuDe[cd])}${coYCCD?'':' <span class="nho chu2">(lớp 10 không có YCCĐ)</span>'}</td>
          <td class="nho">${esc(Y.mach[cd[0]]||'')}</td>
          <td>${b? b.dung+'/'+b.tong : '<span class="chu2">—</span>'} ${bar(b?b.tiLe:null)}</td>
          <td>${mucDat(b?b.tiLe:null)}${tenUN?` <span class="nho chu2">· UNESCO ${tenUN}</span>`:''}</td></tr>`;
      }
    } else {
      // dự phòng nếu data/yccd.js chưa nạp: vẫn hiện theo dữ liệu cũ
      for(const b of (th.banDoUNESCO||[])){
        html += `<tr><td>${b.khoi}</td><td>${esc(b.ten||'')}</td><td>${esc(META.mach[b.aspect]||'')}</td>
          <td>${b.dung}/${b.tong} ${bar(b.tiLe)}</td><td>${mucDat(b.tiLe)}</td></tr>`;
      }
    }
    html += `</table>
      <div class="card" style="background:var(--nen2)"><b>Nhận xét tự động:</b><br>${esc(nx.nhanXet)}</div>`;
    box.innerHTML = html;

    // Báo cáo lớp (giáo viên)
    const lop = ENG.tongHopLop(maLop || null);
    const bcL = $("bc-lop");
    if(lop && lop.soHS>0){
      let h2 = `<p class="nho chu2">Tổng hợp ${lop.soHS} học sinh${maLop? " lớp "+esc(maLop):""} — dữ liệu ẩn danh, lưu cục bộ trên máy này.</p>
      <div class="grid g3">
        <div class="kpi"><div class="so">${lop.dauTruong.tong}</div><div class="nhan">tổng phán quyết</div></div>
        <div class="kpi"><div class="so">${pct(lop.tiLe)}</div><div class="nhan">tỉ lệ đúng cả lớp</div></div>
        <div class="kpi"><div class="so">${lop.lab.tong}</div><div class="nhan">nhiệm vụ lab</div></div>
      </div>
      <table><tr><th>Loại lỗi</th><th>Cả lớp phát hiện</th><th>Recall</th><th>Bắt oan</th></tr>`;
      for(const k of Object.keys(lop.recall)){
        const r = lop.recall[k];
        h2 += `<tr><td><span style="color:${META.loaiLoi[k].mau}">●</span> ${META.loaiLoi[k].ten}</td>
          <td>${r.phatHien}/${r.tongCoLoi}</td><td>${pct(r.tongCoLoi? r.phatHien/r.tongCoLoi : null)}</td><td>${r.batOan}</td></tr>`;
      }
      h2 += `</table>
      <p><button class="btn" id="btn-csv">${svgIco("download")} Xuất CSV nhật ký lớp (minh chứng)</button>
         <button class="btn" id="btn-json">${svgIco("download")} Xuất JSON đầy đủ</button>
         <button class="btn nho" id="btn-xoa" style="border-color:var(--sai)">Xóa dữ liệu trên máy này</button></p>`;
      bcL.innerHTML = h2; bcL.style.display="";
      $("btn-csv").onclick = ()=> taiFile(ENG.xuatCSV(maLop||null), `soiai_nhatky_${maLop||'lop'}_${Date.now()}.csv`, "text/csv");
      $("btn-json").onclick = ()=> taiFile(ENG.xuatJSON(), `soiai_nhatky_${Date.now()}.json`, "application/json");
      $("btn-xoa").onclick = ()=>{ if(confirm("Xóa toàn bộ nhật ký trên máy này? Chỉ dùng khi kết thúc đợt thu dữ liệu.")) { ENG.xoaHet(); veBaoCao(); } };
    } else {
      bcL.innerHTML = '<p class="chu2 nho">Chưa có dữ liệu lớp trên máy này.</p>';
      bcL.style.display="";
    }
  }

  function taiFile(noiDung, ten, mime){
    const b = new Blob(["\ufeff"+noiDung], {type: mime+";charset=utf-8"});
    const a = document.createElement("a");
    a.href = URL.createObjectURL(b); a.download = ten; a.click();
    setTimeout(()=>URL.revokeObjectURL(a.href), 4000);
  }

  /* ================= SCENE ② PHÒNG 3D — SOI MÔ HÌNH =================
   * Dùng DỮ LIỆU THẬT + PERCEPTRON THẬT của Tầng 1 (MX_LAB), không vẽ minh hoạ.
   * Con số hiển thị là kết quả huấn luyện thật → giữ đúng nguyên tắc oracle. */
  let lab3dDaKhoiTao = false;
  /* Ô dự đoán Mức 3 (js/duDoan.js): ddDem = BT-05, ddDiem = BT-04 */
  let ddDem = null, ddDiem = null;
  function lab3dMo(){
    hien("v-lab3d");
    if(lab3dDaKhoiTao) return;
    const r = window.MX_LAB3D.init({
      canvas: $("c-lab3d"), root: $("lab3d-fallback"), tiLeNgay: 92, seed: 20261004,
      onChonDiem: (d)=>{
        $("lab3d-note").innerHTML = svgIco("search") + " " + esc(d.ten)
          + " · đặc trưng: <code>" + esc(d.f.map(x=>x.toFixed(3)).join(", ")) + "</code>";
      }
    });
    if(!r || !r.ok){
      $("btn-lab3d").disabled = true;   // máy không có 3D → ẩn lối vào, bản chữ vẫn còn ở fallback
      $("lab3d-tile").disabled = $("lab3d-so").disabled = true;
      ["lab3d-tao","lab3d-hoc","lab3d-danhgia"].forEach(id=>$(id).disabled = true);
      return;
    }
    lab3dDaKhoiTao = true;
    lab3dHud();
    /* vào lại phòng 3D: xoá ô dự đoán cũ (dữ liệu cũ đã bị huỷ, dự đoán cũ vô nghĩa) */
    ddDem = null; ddDiem = null;
    if($("lab3d-duDoan")) $("lab3d-duDoan").innerHTML = "";
    if($("lab3d-duDoanDiem")) $("lab3d-duDoanDiem").innerHTML = "";

    $("lab3d-tile").oninput = e=>{ $("lab3d-tile-so").textContent = e.target.value + "%"; };
    $("lab3d-so").oninput   = e=>{ $("lab3d-so-num").textContent = e.target.value; };

    $("lab3d-tao").onclick = ()=>{
      window.MX_LAB3D.doiTiLeNgay(parseInt($("lab3d-tile").value, 10));
      const n = window.MX_LAB3D.dungDuLieu(parseInt($("lab3d-so").value, 10));
      $("lab3d-tao").innerHTML = svgIco("image") + " Tạo lại bộ dữ liệu";
      $("lab3d-hoc").disabled = false;
      $("lab3d-danhgia").disabled = true;
      $("lab3d-kq").style.display = "none";
      $("lab3d-note").innerHTML = "Đã tạo <b>" + n + "</b> ảnh. Bấm <b>Huấn luyện từng vòng</b> "
        + "để xem mặt phẳng quyết định dịch dần khi trọng số thay đổi.";
      lab3dHud();
      /* BT-05 Mức 3: dựng ô dự đoán tỉ lệ đúng BAN ĐÊM sau khi có bộ dữ liệu mới.
       * Bộ dữ liệu mới -> dự đoán cũ vô nghĩa -> dựng lại ô mới (chốt được một lần). */
      ddDem = null;
      if($("lab3d-duDoan") && window.MX_DUDOAN){
        const tileHienTai = parseInt($("lab3d-tile").value, 10);
        ddDem = window.MX_DUDOAN.veTruot($("lab3d-duDoan"), {
          cauHoi: "Với " + tileHienTai + "% ảnh ban ngày trong dữ liệu huấn luyện, em dự đoán sau khi học xong mô hình sẽ trả lời ĐÚNG bao nhiêu % ảnh BAN ĐÊM trên bộ ảnh mới?",
          dungSai: 0.10,
          ghiChu: "Chốt dự đoán TRƯỚC khi bấm 'Đánh giá trên bộ ảnh MỚI'. Ngưỡng khớp: ±10 điểm %.",
          onChot(g){
            if(ENG) ENG.logSuKien(maHS, { loai:"duDoan", suKien:"chot", baiToan:"BT-05",
              tiLeNgay: tileHienTai, kq:{ duDoan: Math.round(g*100) } });
          }
        });
      }
      /* BT-04: điểm dự đoán cũ thuộc bộ dữ liệu cũ — xoá, chờ học xong mới dựng lại */
      ddDiem = null;
      if($("lab3d-duDoanDiem")) $("lab3d-duDoanDiem").innerHTML = "";
      if(ENG) ENG.logSuKien(maHS, { loai:"lab3d", suKien:"taoDuLieu",
        soDiem:n, tiLeNgay:parseInt($("lab3d-tile").value,10) });
    };

    $("lab3d-hoc").onclick = ()=>{
      $("lab3d-hoc").disabled = true;
      let lan = 0;
      window.MX_LAB3D.hocHet((kq, xong)=>{
        if(!kq) return;
        lan++;
        if(lan % 5 === 0 || xong){
          $("lab3d-trongso").textContent =
            "w = [" + kq.w.map(x=>x.toFixed(4)).join(", ") + "]  ·  b = " + kq.b.toFixed(4)
            + "  ·  vòng " + kq.epoch + "/" + (window.MX_LAB ? window.MX_LAB.EPOCHS : 60)
            + "  ·  lỗi ở vòng này: " + kq.loi;
          lab3dHud();
        }
        if(xong){
          $("lab3d-danhgia").disabled = false;
          $("lab3d-hoc").disabled = false;
          $("lab3d-note").innerHTML = "Học xong. Mặt phẳng đỏ là ranh giới mô hình vừa học được. "
            + "Bấm <b>Đánh giá trên bộ ảnh MỚI</b> để xem nó đúng/sai ở đâu.";
          /* BT-04 Mức 3: sau khi học xong, hệ chọn MỘT điểm trong bộ dữ liệu và hỏi
           * học sinh dự đoán mô hình sẽ gán nhãn gì cho nó — TRƯỚC khi tiết lộ.
           * Đáp án = dự đoán của chính mô hình thật (state.model.dudoan), tất định. */
          ddDiem = null;
          const host = $("lab3d-duDoanDiem");
          if(host && window.MX_DUDOAN && window.MX_LAB3D.chonDiemNgauNhien){
            const d = window.MX_LAB3D.chonDiemNgauNhien();
            if(d){
              ddDiem = window.MX_DUDOAN.veChon(host, {
                cauHoi: "Hệ chọn ảnh số " + (d.index + 1) + " (ảnh chụp "
                  + (d.light === "ngay" ? "BAN NGÀY" : "BAN ĐÊM") + ") trong bộ dữ liệu. "
                  + "Theo em, MÔ HÌNH VỪA HỌC sẽ đoán ảnh này là CÓ mũ hay KHÔNG mũ?",
                phuongAn: [
                  { id:"co",  text:"CÓ mũ bảo hiểm" },
                  { id:"khong", text:"KHÔNG mũ bảo hiểm" }
                ],
                onChot(chon){
                  if(ENG) ENG.logSuKien(maHS, { loai:"duDoan", suKien:"chot", baiToan:"BT-04",
                    diem: d.index + 1, kq:{ duDoan: chon } });
                  /* tiết lộ NGAY sau khi chốt: nhãn máy đoán + nhãn thật */
                  const mayDoan = window.MX_LAB3D.dudoanDiem(d.index);
                  const that = window.MX_LAB3D.layNhanDiem(d.index);
                  const dc = ddDiem.doiChieu(
                    mayDoan === 1 ? "co" : "khong",
                    "Máy đoán: " + (mayDoan === 1 ? "CÓ mũ" : "KHÔNG mũ")
                      + ". Nhãn thật của ảnh: " + (that === 1 ? "CÓ mũ" : "KHÔNG mũ")
                      + (mayDoan === that ? " — máy đoán đúng ảnh này." : " — máy đoán SAI ảnh này: vì đặc trưng của nó nằm gần mặt phẳng quyết định, hoặc vì dữ liệu lệch khiến ranh giới bị nghiêng.")
                  );
                  if(dc && ENG) ENG.logSuKien(maHS, { loai:"duDoan", suKien:"doiChieu", baiToan:"BT-04",
                    diem: d.index + 1,
                    kq:{ diem: dc.khop?1:0, dung: dc.khop, mach:"C", unesco:"C4",
                         dapAn: dc.dapAn, chon: dc.duDoan, nhanThat: that } });
                }
              });
            }
          }
        }
      });
    };

    $("lab3d-danhgia").onclick = ()=>{
      const kq = window.MX_LAB3D.danhGia();
      if(!kq) return;
      $("lab3d-kq").style.display = "";
      /* BT-05 Mức 3: đối chiếu dự đoán tỉ lệ đúng ban đêm với kết quả THẬT */
      if(ddDem && ddDem.daChot() && !ddDem.daDoiChieu){
        const dc = ddDem.doiChieu(kq.dem.tiLe);
        if(dc && ENG) ENG.logSuKien(maHS, { loai:"duDoan", suKien:"doiChieu", baiToan:"BT-05",
          tiLeNgay: parseInt($("lab3d-tile").value, 10),
          kq:{ diem: dc.khop?1:0, dung: dc.khop, mach:"C", unesco:"C4",
               dapAn: Math.round(dc.ketQua*100), chon: Math.round(dc.duDoan*100), lech: Math.round(dc.lech*100) } });
      }
      const p = x => x==null ? "—" : Math.round(x*100) + "%";
      $("lab3d-kpi").innerHTML =
        `<div class="kpi"><div class="so">${kq.dung}/${kq.tong}</div><div class="nhan">đúng trên bộ ảnh MỚI</div></div>`
      + `<div class="kpi"><div class="so" style="color:var(--vang)">${p(kq.ngay.tiLe)}</div><div class="nhan">ảnh BAN NGÀY<br>${kq.ngay.dung}/${kq.ngay.tong}</div></div>`
      + `<div class="kpi"><div class="so ${kq.dem.tiLe<0.75?'ko':''}">${p(kq.dem.tiLe)}</div><div class="nhan">ảnh BAN ĐÊM<br>${kq.dem.dung}/${kq.dem.tong}</div></div>`;

      const tile = parseInt($("lab3d-tile").value, 10);
      // Giải thích bám đúng YCCĐ 10.C4.1 (chất lượng dữ liệu -> chất lượng AI)
      let gt;
      if(tile >= 85)      gt = "Dữ liệu gần như toàn ảnh ban ngày nên mô hình hầu như chưa học gì về ban đêm — "
                             + "chấm đỏ sẽ dồn ở cụm xanh. Đây là <b>thiên kiến dữ liệu</b> (YCCĐ 10.C4.1, 10.B3.1).";
      else if(tile <= 15) gt = "Đảo ngược: giờ mô hình chỉ biết ban đêm và hỏng ở ban ngày. "
                             + "Vấn đề không nằm ở cái máy mà ở <b>người chọn dữ liệu</b>.";
      else                 gt = "Dữ liệu đã cân bằng nên mô hình học được cả hai nhóm. "
                             + "Đây chính là <b>ý nghĩa của việc khắc phục</b> (YCCĐ 10.D2.2). Sửa ở gốc là sửa dữ liệu.";
      $("lab3d-giaithich").innerHTML = gt;
      $("lab3d-note").innerHTML = "Chấm <b>đỏ</b> = AI đoán sai. Nhìn xem chúng nằm ở cụm nào?";

      if(ENG) ENG.logSuKien(maHS, { loai:"lab3d", suKien:"danhGia", tiLeNgay:tile,
        ketQua:{ tong:kq.tong, dung:kq.dung,
                 ngay:Math.round(kq.ngay.tiLe*1000)/10, dem:Math.round(kq.dem.tiLe*1000)/10 },
        // ánh xạ vào chủ đề của Bộ để bản đồ năng lực tính được (xem veBaoCao)
        kq:{ diem: kq.dem.tiLe>=0.75 && kq.ngay.tiLe>=0.75 ? 1:0, dung: kq.dem.tiLe>=0.75 && kq.ngay.tiLe>=0.75,
             mach:"C", unesco:"C4", dapAn:"canBang", chon: tile>=85?"lech":(tile<=15?"lechDao":"canBang") } });
    };

    $("lab3d-nhe").onclick = ()=>{
      if(window.MX_SCENE && window.MX_SCENE.handle) {}
      // chuyển sang chế độ nhẹ: dựng lại scene với antialias tắt + không hoạt ảnh
      try{ window.MX_LAB3D.huy(); }catch(e){}
      lab3dDaKhoiTao = false;
      const r = window.MX_LAB3D.init({ canvas:$("c-lab3d"), root:$("lab3d-fallback"),
                                       tiLeNgay:parseInt($("lab3d-tile").value,10) || 92, nhe:true });
      lab3dDaKhoiTao = !!(r && r.ok);
      $("lab3d-nhe").innerHTML = svgIco("zap") + " Đã bật chế độ nhẹ — bấm để thử lại 3D đầy đủ";
      lab3dHud();
    };
  }
  function lab3dHud(){
    const t = window.MX_LAB3D.trangThai();
    if(!t){ $("lab3d-hud").innerHTML = ""; return; }
    const k = window.MX_SCENE.hoTro3D();
    $("lab3d-hud").innerHTML =
      `three.js r${k.rev} · ${t.soDiem} ảnh · ngày ${t.tiLeNgay}% · vòng ${t.epoch}`
      + (t.w ? ` · w=[${t.w.map(x=>x.toFixed(2)).join(", ")}]` : "")
      + (t.coMatPhang ? " · <b>có mặt phẳng quyết định</b>" : "");
  }

  /* ================= SCENE ③ ỐNG DẪN — SOI LUỒNG AI =================
   * Hệ chọn NGẪU NHIÊN trạm hỏng -> đáp án biết trước -> chấm tất định, không cần GV.
   * Phủ YCCĐ 10.D1.1 (mối liên hệ mục tiêu - thành phần) mà bản 2D chưa phủ. */
  let pipe3dDaKhoiTao = false;
  /* BT-11 Mức 3: ô dự đoán hiện tượng đầu ra (js/duDoan.js) */
  let ddPipe = null;
  function pipe3dMo(){
    hien("v-pipe3d");
    if(!pipe3dDaKhoiTao){
      const r = window.MX_PIPE3D.init({
        canvas: $("c-pipe3d"), root: $("pipe3d-fallback"),
        onChonTram: (t)=> pipe3dChiTiet(t)
      });
      if(!r || !r.ok){
        // không có 3D: vẫn dạy được bằng bảng chữ (MX_PIPE3D.bangTinh đã in vào fallback)
        $("pipe3d-note").innerHTML = "Máy này không chạy 3D — em vẫn làm được bài ở bảng dưới dạng chữ.";
      } else {
        pipe3dDaKhoiTao = true;
      }
      // dựng sẵn nút đoán cho 5 trạm
      const chips = $("pipe3d-chips");
      chips.innerHTML = "";
      window.MX_PIPE3D.TRAM.forEach(t=>{
        const b = document.createElement("button");
        b.className = "chip"; b.textContent = t.ten;
        b.onclick = ()=> pipe3dDoan(t.id);
        chips.appendChild(b);
      });
      /* BT-11 Mức 3: dự đoán HIỆN TƯỢNG Ở ĐẦU RA trước khi hệ làm hỏng trạm.
       * Oracle = hành vi thật trong pipeline3d.js: vòng tick kẹp hạt lại ngay trước
       * trạm hỏng và đổi màu hạt sang đỏ (h.material.color.setHex(M.sai)) — hằng số
       * trong mã nguồn, không phụ thuộc trạm nào bị hỏng nên không lộ đáp án của
       * trò đoán trạm bên dưới. */
      ddPipe = null;
      const hostDD = $("pipe3d-duDoan");
      if(hostDD && window.MX_DUDOAN){
        ddPipe = window.MX_DUDOAN.veChon(hostDD, {
          cauHoi: "TRƯỚC KHI hệ làm hỏng một trạm: em dự đoán hiện tượng gì sẽ xuất hiện trên dòng hạt sáng (đầu ra của ống dẫn)?",
          phuongAn: [
            { id:"ket",   text:"Hạt sáng kẹt lại ngay trước trạm hỏng và đổi màu đỏ" },
            { id:"mat",   text:"Hạt sáng biến mất hoàn toàn khỏi ống dẫn" },
            { id:"nhanh", text:"Hạt sáng chạy nhanh hơn bình thường" },
            { id:"binhThuong", text:"Không có gì thay đổi — hệ vẫn báo lỗi bằng chữ" }
          ],
          onChot(chon){
            if(ENG) ENG.logSuKien(maHS, { loai:"duDoan", suKien:"chot", baiToan:"BT-11",
              kq:{ duDoan: chon } });
          }
        });
      }
    }
    pipe3dHud();
  }
  function pipe3dHong(){
    const r = window.MX_PIPE3D.batDauLuot();
    $("pipe3d-doan").style.display = "";
    $("pipe3d-kq").innerHTML = "";
    /* BT-11 Mức 3: hệ ĐÃ làm hỏng trạm — đối chiếu dự đoán hiện tượng với hành vi thật */
    if(ddPipe && ddPipe.daChot() && !ddPipe.daDoiChieu){
      const dc = ddPipe.doiChieu("ket",
        "Trong mã nguồn pipeline3d.js, mỗi hạt có vị trí t trên đường ống; khi một trạm hỏng, "
        + "vòng lặp hoạt ảnh kẹp t của mọi hạt dừng lại NGAY TRƯỚC trạm đó và tô hạt màu đỏ. "
        + "Hạt không biến mất và không nhanh lên — chúng ùn tắc, giống hàng hoá kẹt trước "
        + "một dây chuyền hỏng. Hiện tượng ở đầu ra luôn là dấu hiệu đầu tiên để SOI ra chỗ hỏng.");
      if(dc && ENG) ENG.logSuKien(maHS, { loai:"duDoan", suKien:"doiChieu", baiToan:"BT-11",
        kq:{ diem: dc.khop?1:0, dung: dc.khop, mach:"D", unesco:"D1",
             dapAn: dc.dapAn, chon: dc.duDoan } });
    }
    $("pipe3d-note").innerHTML = "Có <b>" + r.soTram + "</b> trạm trong hệ thống. Một trạm vừa bị làm hỏng — "
      + "quan sát các hạt sáng rồi đoán xem trạm nào.";
    if(ENG) ENG.logSuKien(maHS, { loai:"pipe3d", suKien:"batDauLuot" });
    pipe3dHud();
  }
  function pipe3dDoan(tramId){
    const r = window.MX_PIPE3D.doan(tramId);
    if(!r || !r.ok){ $("pipe3d-kq").innerHTML = `<p class="chu2">${esc(r && r.liDo || "")}</p>`; return; }
    const hop = $("pipe3d-kq");
    hop.className = "phanhoi " + (r.dung ? "dung" : "sai");
    /* AN TOÀN innerHTML: r.doan/r.dungLa đến từ hằng số TRAM trong pipeline3d.js
     * (không phải dữ liệu người dùng); vẫn escape toàn bộ cho chắc. */
    hop.innerHTML = (r.dung
        ? `<p>${svgIco("check")} <b>Chính xác!</b> Trạm <b>${esc(r.dungLa.ten)}</b> đang hỏng.</p>`
        : `<p>${svgIco("x")} <b>Chưa đúng.</b> Em đoán <b>${esc(r.doan.ten)}</b>, nhưng trạm hỏng là <b>${esc(r.dungLa.ten)}</b>.</p>`)
      + `<p class="chu2"><b>Vì sao hỏng trạm này lại gây ra hiện tượng đó:</b> ${esc(r.dungLa.khiHong)}</p>`
      + `<p class="nho chu2"><b>Ví dụ:</b> ${esc(r.dungLa.viDu)}</p>`
      + `<p class="nho chu2">YCCĐ liên quan: ${esc(r.dungLa.yccd)} · bấm vào từng trạm trong hình để xem vai trò của nó.</p>`;
    if(ENG) ENG.logSuKien(maHS, {
      loai:"pipe3d", suKien:"doan",
      kq:{ diem: r.dung?1:0, dung: r.dung, mach:"D", unesco:"D1",
           dapAn: r.dungLa.id, chon: tramId },
      tramHong: r.dungLa.id, doan: tramId
    });
    pipe3dHud();
  }
  function pipe3dChiTiet(t){
    $("pipe3d-chitiet").innerHTML =
      `<div class="card" style="background:var(--nen2)">
         <h3>${esc(t.ten)} <span class="nho chu2">(YCCĐ ${esc(t.yccd)})</span></h3>
         <p>${esc(t.moTa)}</p>
         <p class="chu2"><b>Vai trò:</b> ${esc(t.vaiTro)}</p>
         <p class="chu2"><b>Nếu trạm này hỏng:</b> ${esc(t.khiHong)}</p>
       </div>`;
  }
  function pipe3dHud(){
    const t = window.MX_PIPE3D.trangThai();
    const k = window.MX_SCENE.hoTro3D();
    $("pipe3d-hud").innerHTML = t
      ? `three.js r${k.rev} · ${t.soHat} hạt · ` + (t.tramHong!==null
          ? (t.daCham ? "đã đoán" : "có 1 trạm hỏng — hãy đoán")
          : "hệ thống đang chạy bình thường")
      : "";
  }

  /* ============ TÌNH HUỐNG & TRÁCH NHIỆM — phủ 5 YCCĐ còn trống ============
   * 10.A2.1, 10.A2.MR1, 10.B2.1, 10.C2.MR1, 10.C3.MR1.
   * Danh sách chỉ dựng MỘT lần: dựng lại mỗi lần vào view sẽ xoá trạng thái đã trả lời
   * và cho phép học sinh bấm lại vô hạn để dò đáp án. */
  /* --- KỊCH BẢN 9 CẢNH (js/kichban.js) ---
   * Cờ kbDaNap giống thDaNap của tình huống: chỉ init MỘT lần, vào lại thì giữ trạng
   * thái đang xem. Init lặp lại sẽ dựng chồng DOM và nhân đôi listener phím. */
  let kbDaNap = false;
  function kbMo(){
    hien("v-kichban");
    const M = window.MX_KICHBAN;
    if(!M) return;
    if(kbDaNap) { try{ M.tiepTuc(); }catch(e){} return; }
    const host = $("kb-host");
    if(!host) return;
    M.init(host, {
      /* Ghi nhật ký từng cảnh vào log lớp. Đây là MINH CHỨNG SỬ DỤNG THẬT cho hồ sơ
       * dự thi (nút "Xuất CSV nhật ký lớp" đã có sẵn trong app). */
      onCanh(i, c){
        if(ENG && maHS) ENG.logSuKien(maHS, {
          loai:"kichBan", suKien:"xemCanh",
          kq:{ canh: i + 1, tenCanh: c.ten, giay: Math.round(c.dur / 1000) }
        });
      }
    });
    kbDaNap = true;
  }

  let thDaNap = false;
  function thMo(){
    hien("v-tinhhuong");
    const M = window.MX_TINH_HUONG;
    if(!M) return;
    if(thDaNap) return;
    M.veTinhHuong($("th-danh-sach"), (q, chon, dapUng) => {
      /* Trường `diem` là TÊN TRƯỜNG NỘI BỘ mà engine.js dùng để tổng hợp
       * (tongHop() đếm kq.diem). Giao diện KHÔNG hiển thị nó dưới dạng điểm số —
       * chỉ hiện "đáp ứng / chưa đáp ứng" theo phần VI Khung 2422. */
      if(ENG) ENG.logSuKien(maHS, {
        loai:"tinhHuong", suKien:"traLoi",
        kq:{ diem: dapUng?1:0, dung: dapUng, mach:q.mach, unesco:q.chuDe,
             dapAn:q.dapAn, chon: chon },
        yccd: q.yccd
      });
    });
    const info = M.thongTin();
    $("th-thong-ke").textContent =
      info.soTinhHuong + " tình huống · phủ " + info.yccdPhu.length
      + " yêu cầu cần đạt: " + info.yccdPhu.join(", ");
    thDaNap = true;
  }

  /* ================= NHÀ MÁY AI — DÂY CHUYỀN 7 TRẠM =================
   * Kiến trúc: các module đã có không bị bỏ đi mà trở thành TRẠM của dây chuyền.
   * Trạm 5 (ỨNG DỤNG) là trạm mới, dùng MX_NHAMAY_TEXT — máy sinh văn bản n-gram
   * huấn luyện ngay trong trình duyệt (đo thật: train 2.7 ms, 0 MB, 0.59 ms/câu).
   *
   * NGUYÊN TẮC GIỮ NGUYÊN: mọi trạm chấm được bằng nhãn hệ biết trước.
   * Ở trạm 5, hệ biết trước chủ đề nào có trong ngữ liệu nên biết trước câu trả lời
   * nào có căn cứ và câu nào là bịa — không cần giáo viên, không cần người kiểm chứng. */
  const NM_TRAM = [
    { id:0, so:"TRẠM 0", ten:"NHẬP LIỆU", anDuy:"nguyên liệu thô",
      moTa:"Ba dạng dữ liệu: ảnh (hệ tự vẽ), văn bản, và tín hiệu số. Mở nắp để xem máy thật sự đọc những CON SỐ nào từ mỗi dạng.",
      yccd:"10.C4.MR1 · 10.C2.1 · 10.D2.1", view:"nhamay0", trangThai:"co" },
    { id:1, so:"TRẠM 1", ten:"DÁN NHÃN", anDuy:"sơ chế",
      moTa:"Chính em dán nhãn cho từng ảnh. Hệ huấn luyện hai mô hình — một từ nhãn của em, một từ nhãn đúng — rồi so trên cùng bộ ảnh mới. Nhãn sai thì mô hình sai có hệ thống.",
      yccd:"10.C4.1", view:"nhamay1", trangThai:"co" },
    { id:2, so:"TRẠM 2", ten:"HUẤN LUYỆN", anDuy:"dây chuyền sản xuất",
      moTa:"Mô hình so dự đoán với nhãn đúng, đo lỗi, rồi tự chỉnh trọng số. Lặp lại nhiều vòng.",
      yccd:"10.C4.1 · 10.C5", view:"v-lab", trangThai:"co" },
    { id:3, so:"TRẠM 3", ten:"MÔ HÌNH", anDuy:"thành phẩm bán thành",
      moTa:"Mở nắp mô hình: xem trọng số thật trong không gian 3 chiều và mặt phẳng quyết định nó vừa học được.",
      yccd:"10.D2.1 · 10.C5", view:"v-lab3d", trangThai:"co" },
    { id:4, so:"TRẠM 4", ten:"KIỂM ĐỊNH", anDuy:"KCS — kiểm tra chất lượng",
      moTa:"Thử mô hình trên bộ dữ liệu MỚI mà nó chưa từng học. Tách riêng ban ngày và ban đêm để thấy thiên kiến.",
      yccd:"10.D2.2 · 10.C4.1", view:"v-lab3d", trangThai:"co" },
    { id:5, so:"TRẠM 5", ten:"ỨNG DỤNG", anDuy:"xuất xưởng — em dùng AI thật",
      moTa:"Em đặt câu hỏi cho một hệ AI chạy ngay trong máy này, rồi tự kiểm định xem nó nói có căn cứ hay bịa.",
      yccd:"10.C2.MR2 · 10.C3.1 · 10.C3.2 · 10.B2.MR1", view:"nhamay5", trangThai:"co" },
    { id:6, so:"TRẠM 6", ten:"CON NGƯỜI KIỂM", anDuy:"KCS cuối + vòng phản hồi",
      moTa:"Con người rà soát đầu ra và chịu trách nhiệm. Dữ liệu mới từ đây quay vòng về Trạm 0.",
      yccd:"10.A1.2 · 10.D1.1 · 10.D2.1", view:"v-pipe3d", trangThai:"co" }
  ];
  let nmTramDaMo = null;

  function nmVeSoDo(){
    const box = $("nm-so-do");
    if(!box) return;
    /* Dùng createElement + textContent (không innerHTML) cho sơ đồ dây chuyền
     * vì đây là nội dung sinh từ dữ liệu, dù dữ liệu là hằng số trong file này. */
    box.innerHTML = "";
    NM_TRAM.forEach((t, i) => {
      if(i > 0){
        const mui = document.createElement("span");
        mui.className = "nm-mui"; mui.setAttribute("aria-hidden", "true");
        mui.textContent = "→";
        box.appendChild(mui);
      }
      const b = document.createElement("button");
      b.className = "nm-tram" + (nmTramDaMo === t.id ? " dang-mo" : "")
                  + (t.trangThai === "xong" ? " xong" : "");
      b.type = "button";
      const so = document.createElement("span"); so.className = "so"; so.textContent = t.so;
      const ten = document.createElement("span"); ten.className = "ten"; ten.textContent = t.ten;
      const ad = document.createElement("span"); ad.className = "an-duy"; ad.textContent = t.anDuy;
      b.append(so, ten, ad);
      b.onclick = () => nmMoTram(t.id);
      box.appendChild(b);
    });
  }

  function nmMoTram(id){
    const t = NM_TRAM.find(x => x.id === id);
    if(!t) return;
    nmTramDaMo = id;
    nmVeSoDo();
    $("nm-ten-tram").textContent = `${t.so} · ${t.ten} — ${t.anDuy}`;
    $("nm-yccd").textContent = "Yêu cầu cần đạt: " + t.yccd;

    const nd = $("nm-noi-dung");
    nd.textContent = "";
    const p = document.createElement("p"); p.className = "chu2"; p.textContent = t.moTa;
    nd.appendChild(p);

    /* Ba trạm có bảng điều khiển ngay trong khung nhìn nhà máy: 0, 1 và 5.
     * Các trạm còn lại mở khung nhìn chuyên biệt (lab / lab3d / pipe3d). */
    ["nm-tram0", "nm-tram1", "nm-tram5"].forEach(id => {
      const el = $(id); if(el) el.style.display = "none";
    });

    if(t.view === "nhamay0"){ nmKhoiDongTram0(); return; }
    if(t.view === "nhamay1"){ nmKhoiDongTram1(); return; }
    if(t.view === "nhamay5"){ nmKhoiDongTram5(); return; }

    const b = document.createElement("button");
    b.className = "btn chinh"; b.type = "button";
    b.textContent = "Mở trạm này →";
    b.onclick = () => {
      if(t.view === "v-lab")   { hien("v-lab"); labBuoc(1); }
      if(t.view === "v-lab3d") lab3dMo();
      if(t.view === "v-pipe3d") pipe3dMo();
    };
    nd.appendChild(b);
  }

  /* ---------- TRẠM 0: NHẬP LIỆU (3 dạng dữ liệu, mở nắp xem máy đọc số gì) ---------- */
  let nmT0DaNap = false;
  function nmKhoiDongTram0(){
    const M = window.MX_NHAMAY01;
    if(!M){ return; }
    $("nm-tram0").style.display = "";

    M.khoiDongT0(parseInt($("t0-so").value, 10), parseInt($("t0-tile").value, 10));
    M.veAnhVaDacTrung($("t0-anh"));
    M.veVanBan($("t0-vanban"));
    M.veSo($("t0-so-lieu"));

    /* Câu hỏi chỉ dựng MỘT lần: nếu dựng lại mỗi lần vào trạm thì trạng thái
     * đã trả lời bị mất và học sinh có thể bấm lại vô hạn để dò đáp án. */
    if(!nmT0DaNap){
      M.veCauHoiT0($("t0-cauhoi"), (q, chon, dung) => {
        if(ENG) ENG.logSuKien(maHS, {
          loai:"nhamay", suKien:"tram0", tram:0,
          kq:{ diem: dung?1:0, dung: dung, mach:q.mach, unesco:q.chuDe,
               dapAn:q.dapAn, chon: chon },
          yccd:q.yccd
        });
        if(dung) nmTramXong(0);
      });
      nmT0DaNap = true;
    }
  }

  function nmT0TaoLai(){
    const M = window.MX_NHAMAY01;
    if(!M) return;
    M.khoiDongT0(parseInt($("t0-so").value, 10), parseInt($("t0-tile").value, 10));
    M.veAnhVaDacTrung($("t0-anh"));
    if(ENG) ENG.logSuKien(maHS, { loai:"nhamay", suKien:"tram0TaoDuLieu",
      soAnh: parseInt($("t0-so").value,10), tiLeNgay: parseInt($("t0-tile").value,10) });
  }

  /* ---------- TRẠM 1: DÁN NHÃN (học sinh tự dán -> thấy hậu quả bằng số) ---------- */
  /* BT-02 Mức 3: ô dự đoán độ chính xác mô hình A trước khi chấm (js/duDoan.js) */
  let ddT1 = null;
  function nmKhoiDongTram1(taoMoi){
    const M = window.MX_NHAMAY01;
    if(!M){ return; }
    $("nm-tram1").style.display = "";
    if(taoMoi !== false){
      M.khoiDongT1(10);
      $("t1-kq").innerHTML = "";
      /* bộ ảnh mới -> dự đoán cũ vô nghĩa, dựng ô mới */
      ddT1 = null;
      const host = $("t1-duDoan");
      if(host && window.MX_DUDOAN){
        ddT1 = window.MX_DUDOAN.veTruot(host, {
          cauHoi: "Mô hình A sẽ học từ NHÃN DO EM DÁN. Em dự đoán mô hình A đạt độ chính xác bao nhiêu trên bộ ảnh kiểm tra mới? (Mô hình B học từ nhãn đúng thường đạt ~100%.)",
          dungSai: 0.10,
          ghiChu: "Chốt dự đoán TRƯỚC khi bấm 'Chấm nhãn'. Ngưỡng khớp: ±10 điểm %. Mỗi bộ ảnh chỉ dự đoán được một lần.",
          onChot(g){
            if(ENG) ENG.logSuKien(maHS, { loai:"duDoan", suKien:"chot", baiToan:"BT-02",
              kq:{ duDoan: Math.round(g*100) } });
          }
        });
      }
    }
    M.veAnhDanNhan($("t1-anh"));
    M.capNhatTienDoT1();
  }

  function nmT1Cham(){
    const M = window.MX_NHAMAY01;
    if(!M) return;
    const r = M.chamT1();
    if(!r) return;
    M.veKetQuaT1($("t1-kq"), r);
    /* BT-02 Mức 3: đối chiếu dự đoán với độ chính xác THẬT của mô hình A */
    if(ddT1 && ddT1.daChot() && !ddT1.daDoiChieu){
      const dc = ddT1.doiChieu(r.hocTrenNhanHS.doChinhXac);
      if(dc && ENG) ENG.logSuKien(maHS, { loai:"duDoan", suKien:"doiChieu", baiToan:"BT-02",
        kq:{ diem: dc.khop?1:0, dung: dc.khop, mach:"C", unesco:"C4",
             dapAn: Math.round(dc.ketQua*100), chon: Math.round(dc.duDoan*100), lech: Math.round(dc.lech*100) } });
    }
    if(ENG) ENG.logSuKien(maHS, {
      loai:"nhamay", suKien:"tram1", tram:1,
      kq:{ /* nhãn đúng = đáp án hệ biết trước, nên chấm tất định */
           diem: r.nhanSai === 0 ? 1 : 0, dung: r.nhanSai === 0,
           mach:"C", unesco:"C4", dapAn:"nhanDung",
           chon: r.nhanDung + "/" + r.soAnh },
      soAnh:r.soAnh, nhanDung:r.nhanDung, nhanSai:r.nhanSai,
      tiLeNhanDung: Math.round(r.tiLeNhanDung*1000)/10,
      thietHaiDoChinhXac: Math.round(r.thietHai*1000)/10,
      moHinhA_nhanHS: Math.round(r.hocTrenNhanHS.doChinhXac*1000)/10,
      moHinhB_nhanThat: Math.round(r.hocTrenNhanThat.doChinhXac*1000)/10
    });
    if(r.nhanSai === 0) nmTramXong(1);
    nmT1HienNhanThat();
  }

  /** Sau khi chấm mới tiết lộ nhãn thật — tránh để học sinh dò đáp án trước. */
  function nmT1HienNhanThat(){
    const M = window.MX_NHAMAY01;
    const host = $("t1-anh");
    if(!host) return;
    const anhs = host.querySelectorAll(".anh-nhan");
    const st = M.trangThai().t1;
    if(!st) return;
    // đọc nhãn thật từ chính module để không phải đoán
    anhs.forEach((w, i) => {
      if(w.querySelector(".nhan-that")) return;
      const tag = document.createElement("span");
      tag.className = "nhan-that";
      tag.textContent = "…";
      w.style.position = "relative";
      w.insertBefore(tag, w.firstChild);
    });
    // dùng phép so sánh trực tiếp: yêu cầu module trả về nhãn thật
    const that = M.layNhanThat ? M.layNhanThat() : null;
    if(that){
      anhs.forEach((w, i) => {
        const o = w.querySelector(".nhan-that");
        if(o && that[i] != null){
          o.textContent = that[i] === 1 ? "CÓ mũ" : "không mũ";
        }
      });
    }
  }

  function nmKhoiDongTram5(){
    const N = window.MX_NHAMAY_TEXT;
    if(!N){ $("nm-tram5").style.display = "none"; return; }

    // thông tin máy: minh bạch theo yêu cầu của Khung (nói rõ AI làm gì, chạy ở đâu)
    const info = N.thongTin();
    $("nm-thong-tin-may").innerHTML =
      `<b>${svgIco("search")} Mở nắp máy — đây là cách nó hoạt động</b><br>` +
      `<span class="nho">Loại mô hình: <b>${esc(info.loai)}</b> · bậc n = ${info.n} · ` +
      `số ngữ cảnh học được: <b>${info.soNguoiCanh}</b> · độ dài ngữ liệu: ${info.doDaiNguLieu} kí tự · ` +
      `số chủ đề đã học: <b>${info.soChuDeHoc}</b> · tải về: <b>${esc(info.taiVe)}</b> · ` +
      `cần mạng: <b>${info.canMang ? "có" : "không"}</b></span><br>` +
      `<span class="nho chu2">Các chủ đề máy ĐÃ học: ${esc(N.tenChuDe.join(" · "))}. ` +
      `Hỏi ngoài các chủ đề này, máy vẫn trả lời trôi chảy — nhưng đó là bịa.</span>`;

    // nút gợi ý: 2 câu trong ngữ liệu + 1 câu ngoài ngữ liệu (để HS tự khám phá)
    const goiY = [
      "Hãy liệt kê 3 ứng dụng AI trong nông nghiệp ở Việt Nam, trình bày dạng bảng",
      "Bác sĩ dùng AI chẩn đoán bệnh như thế nào?",
      "Cho tôi biết giá vàng hôm nay là bao nhiêu?"
    ];
    const chips = $("nm-goi-y"); chips.innerHTML = "";
    goiY.forEach(q => {
      const b = document.createElement("button");
      b.className = "chip"; b.type = "button"; b.textContent = q;
      b.onclick = () => { $("nm-prompt").value = q; nmDanhGiaPrompt(); };
      chips.appendChild(b);
    });

    $("nm-prompt").oninput = nmDanhGiaPrompt;
    nmDanhGiaPrompt();
  }

  /* Chấm chất lượng prompt theo rubric (10.C3.1) — tất định, không cần LLM */
  function nmDanhGiaPrompt(){
    const N = window.MX_NHAMAY_TEXT;
    const p = $("nm-prompt").value.trim();
    const box = $("nm-rubric");
    if(!p){ box.innerHTML = ""; return; }
    const r = N.danhGiaPrompt(p);
    box.innerHTML =
      `<div class="card" style="background:var(--nen2)">
         <b>Prompt của em đạt ${r.diem}/${r.tong} tiêu chí — ${esc(r.muc)}</b><br>
         <span class="nho">Đạt: ${esc(r.dat.join(", ") || "chưa có")} ·
         Thiếu: ${esc(r.thieu.join(", ") || "không")}</span><br>
         <span class="nho chu2">Một prompt tốt nêu rõ <b>mục tiêu</b>, có <b>ngữ cảnh</b>,
         và yêu cầu <b>định dạng đầu ra</b>. (Yêu cầu cần đạt 10.C3.1)</span>
       </div>`;
  }

  let nmItem = null;
  function nmSinh(){
    const N = window.MX_NHAMAY_TEXT;
    const p = $("nm-prompt").value.trim();
    if(!p){ alert("Em hãy viết câu hỏi trước đã."); return; }
    const t0 = performance.now();
    nmItem = N.ungDung(p, { seed: (Date.now() % 99991) + 1 });
    const ms = (performance.now() - t0);

    // Dùng textContent cho nội dung máy sinh ra — TUYỆT ĐỐI không innerHTML,
    // vì đây là chuỗi do mô hình sinh, không phải hằng số của nhà phát triển.
    $("nm-van-ban").textContent = nmItem.vanBan;
    $("nm-chan-doan").textContent =
      `Máy sinh câu này trong ${ms.toFixed(2)} ms · seed ${nmItem.seed} (cùng seed sẽ cho cùng kết quả) · `
      + `chủ đề máy nhận ra: ${nmItem.chuDe || "không nằm trong ngữ liệu đã học"}`;
    $("nm-dau-ra").style.display = "";
    $("nm-kq5").innerHTML = "";
    $("nm-can-cu").classList.remove("chon"); $("nm-bia").classList.remove("chon");
    if(ENG) ENG.logSuKien(maHS, { loai:"nhamay", suKien:"ungDung", prompt:p,
      chuDe: nmItem.maChuDe, trongNguLieu: nmItem.trongNguLieu, ms: +ms.toFixed(2) });
  }

  function nmPhanQuyet(coCanCu){
    if(!nmItem){ alert("Em hãy sinh câu trả lời trước đã."); return; }
    const N = window.MX_NHAMAY_TEXT;
    const kq = N.chamUngDung(nmItem, { coCanCu });
    (coCanCu ? $("nm-can-cu") : $("nm-bia")).classList.add("chon");

    /* AN TOÀN innerHTML: nmItem.chuDe đến từ hằng số CHU_DE trong nhamay_text.js;
     * văn bản máy sinh KHÔNG được chèn vào đây (đã hiển thị bằng textContent ở trên). */
    const box = $("nm-kq5");
    box.className = "phanhoi " + (kq.dung ? "dung" : "sai");
    box.innerHTML = kq.dung
      ? `<p>${svgIco("check")} <b>Chính xác.</b> ${nmItem.trongNguLieu
          ? `Chủ đề <b>${esc(nmItem.chuDe)}</b> CÓ trong ngữ liệu máy đã học, nên câu trả lời có căn cứ.`
          : `Chủ đề em hỏi <b>không có</b> trong ngữ liệu máy đã học, nên đây là lời bịa.`}</p>`
      : `<p>${svgIco("x")} <b>Chưa đúng.</b> ${nmItem.trongNguLieu
          ? `Thật ra câu này CÓ căn cứ: chủ đề <b>${esc(nmItem.chuDe)}</b> nằm trong ngữ liệu máy đã học.`
          : `Thật ra đây là lời bịa: chủ đề em hỏi không có trong ngữ liệu, máy chỉ ghép chữ nghe cho xuôi.`}</p>`;
    box.innerHTML +=
      `<p class="chu2"><b>Bài học của trạm này:</b> một hệ AI có thể trả lời rất trôi chảy về một chủ đề
       mà nó chưa từng được học. Giọng điệu tự tin không phải là bằng chứng. Cách kiểm tra là
       <b>hỏi xem nó học từ đâu</b> và <b>đối chiếu với nguồn thật</b>.</p>`
      + `<p class="nho chu2">Yêu cầu cần đạt 10.B2.MR1: nhận biết dấu hiệu của nội dung do AI tạo sinh
         và nhận xét mức độ minh bạch. · 10.C2.MR2: sử dụng được một số ứng dụng AI trong học tập.</p>`;

    if(ENG) ENG.logSuKien(maHS, { loai:"nhamay", suKien:"phanQuyet",
      kq:{ diem: kq.dung ? 1 : 0, dung: kq.dung, mach:"C", unesco:"C2",
           dapAn: nmItem.trongNguLieu ? "coCanCu" : "bia", chon: coCanCu ? "coCanCu" : "bia" },
      boSot: !!kq.boSot, baoDong: !!kq.baoDong });
    nmTramXong(5);
  }

  function nmTramXong(id){
    const t = NM_TRAM.find(x => x.id === id);
    if(t && t.trangThai !== "xong"){ t.trangThai = "xong"; nmVeSoDo(); }
  }

  /* ================= KHỞI ĐỘNG ================= */
  window.addEventListener("DOMContentLoaded", ()=>{
    // Gộp ngân hàng mở rộng (nếu có) vào ngân hàng chính — 1 lần duy nhất
    if(window.MX_BANK_MORE && window.MX_BANK_MORE.length && !window.MX_BANK._merged){
      window.MX_BANK = window.MX_BANK.concat(window.MX_BANK_MORE);
      Object.defineProperty(window.MX_BANK, "_merged", {value:true});
    }
    $("btn-vao").onclick = dangNhap;
    /* --- CHẾ ĐỘ ÍT CHỮ ---
     * Lưu trạng thái bằng localStorage để lần sau mở vẫn giữ nguyên lựa chọn.
     * Quên bước này thì giáo viên phải bấm lại trên từng máy của lớp.
     * KHÔNG xoá nội dung: chỉ thêm class lên <body> để CSS ẩn phụ chú. */
    const IT_CHU_KEY = "***";
    const itChuDat = (on) => {
      document.body.classList.toggle("it-chu", on);
      const b = $("btn-it-chu");
      if(b){ b.setAttribute("aria-pressed", on ? "true" : "false"); }
      const l = $("lbl-it-chu");
      if(l) l.textContent = on ? "Đầy đủ chữ" : "Ít chữ";
    };
    let itChuBat = false;
    try { itChuBat = localStorage.getItem(IT_CHU_KEY) === "1"; } catch(e){}
    itChuDat(itChuBat);
    const _bItChu = $("btn-it-chu");
    if(_bItChu) _bItChu.onclick = () => {
      itChuBat = !itChuBat;
      itChuDat(itChuBat);
      try { localStorage.setItem(IT_CHU_KEY, itChuBat ? "1" : "0"); } catch(e){}
    };
    /* để judge và test đọc được trạng thái */
    window.MX_IT_CHU = { bat: () => itChuBat, dat: itChuDat };

    $("btn-ve-home").onclick = ()=>hien("v-home");
    $("btn-lab").onclick = ()=>{ hien("v-lab"); labBuoc(1); };
    $("btn-dautruong").onclick = ()=>{ hien("v-dautruong"); dtBatDau("luyen");
      /* BT-09 Mức 3 nằm cùng view với Đấu trường nhưng ở tệp riêng js/bt09.js, vì phần
       * này có trạng thái riêng (nhớ loại lỗi nào đã ghi) còn Đấu trường chỉ chạy phiên.
       * Gọi ở đây để mỗi lần mở view đều dựng lại với đúng mã học sinh đang dùng. */
      const _b09 = window.MX_BT09; if(_b09) _b09.init(maHS); };
    $("dt-btn-luyen").onclick = ()=>dtBatDau("luyen");
    $("dt-btn-pre").onclick   = ()=>dtBatDau("pre");
    $("dt-btn-post").onclick  = ()=>dtBatDau("post");
    $("btn-baocao").onclick = ()=>{ hien("v-baocao"); veBaoCao(); };
    $("btn-logic").onclick = ()=>{ hien("v-logic"); window.MX_LOGIC.init(maHS); };
    $("btn-kienthuc").onclick = ()=>{ hien("v-kienthuc"); window.MX_KIEN_THUC.init(maHS);
      /* BT-13 Mức 2 + Mức 3 (10.C2.3) nằm trong cùng view Kiến thức nền nhưng ở tệp
       * riêng js/bt13.js, vì phần này có trạng thái (nhớ lần kiểm tra đầu của từng
       * tình huống) còn js/kienthuc.js chỉ render bảng tĩnh. Gọi ở đây để mỗi lần mở
       * view đều dựng lại phần tình huống với đúng mã học sinh đang dùng. */
      const _b13 = window.MX_BT13; if(_b13) _b13.init(maHS); };
    $("btn-tinhhuong").onclick = ()=> thMo();
    /* Nút kịch bản có thể chưa tồn tại nếu index.html bị revert một phần, nên kiểm
     * null thay vì gán thẳng như các nút cũ — gán thẳng sẽ ném lỗi và CHẶN toàn bộ
     * đoạn nối nút phía sau. */
    const _bKb = $("btn-kichban"); if(_bKb) _bKb.onclick = ()=> kbMo();
    $("btn-lab3d").onclick = ()=> lab3dMo();
    $("btn-pipe3d").onclick = ()=> pipe3dMo();
    /* NHÀ MÁY AI — dây chuyền 7 trạm (điều hướng chính mới) */
    $("btn-nhamay").onclick = ()=>{ hien("v-nhamay"); nmVeSoDo(); nmMoTram(0); };
    /* --- Trạm 0: NHẬP LIỆU --- */
    $("t0-tao").onclick = ()=> nmT0TaoLai();
    $("t0-tile").oninput = e=>{ $("t0-tile-so").textContent = e.target.value + "%"; };
    $("t0-so").oninput   = e=>{ $("t0-so-num").textContent = e.target.value; };
    /* --- Trạm 1: DÁN NHÃN --- */
    $("t1-tao").onclick   = ()=> nmKhoiDongTram1(true);
    $("t1-cham").onclick  = ()=> nmT1Cham();
    $("t1-lamlai").onclick= ()=> nmKhoiDongTram1(true);
    /* --- Trạm 5: ỨNG DỤNG --- */
    $("nm-sinh").onclick  = ()=> nmSinh();
    $("nm-xoa5").onclick  = ()=>{ nmItem = null; $("nm-prompt").value = "";
      $("nm-dau-ra").style.display = "none"; $("nm-rubric").innerHTML = "";
      $("nm-kq5").innerHTML = ""; $("nm-van-ban").textContent = ""; };
    $("nm-can-cu").onclick = ()=> nmPhanQuyet(true);
    $("nm-bia").onclick    = ()=> nmPhanQuyet(false);
    $("pipe3d-hong").onclick = ()=> pipe3dHong();
    $("pipe3d-reset").onclick = ()=>{ window.MX_PIPE3D.datLai(); $("pipe3d-doan").style.display="none";
      $("pipe3d-chitiet").innerHTML=""; $("pipe3d-note").innerHTML="Đã đặt lại. Bấm <b>Làm hỏng một trạm</b> để chơi lượt mới."; pipe3dHud(); };
    $("btn-gioithieu").onclick = ()=>hien("v-gioithieu");
    $("btn-tao-dulieu").onclick = labTaoDuLieu;
    $("btn-huanluyen").onclick = labHuanLuyen;
    $("btn-sosanh").onclick = labSoSanh;
    $("btn-lab-cauhoi").onclick = labCauHoi;
    $("dt-nop").onclick = dtNop;
    $("dt-tiep").onclick = dtTiep;
    hien("v-home");
  });
})();
