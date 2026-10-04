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
  const pct = (x) => x===null||x===undefined ? "—" : Math.round(x*100) + "%";

  /* ================= ĐIỀU HƯỚNG ================= */
  function hien(view){
    ["v-home","v-nhap","v-lab","v-dautruong","v-baocao","v-logic","v-kienthuc","v-gioithieu"].forEach(id=>{
      $(id).style.display = (id===view) ? "" : "none";
    });
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
          fb.innerHTML = (kq.dung ? "✅ <b>Chính xác!</b> " : "❌ <b>Chưa đúng.</b> ") + esc(nv.giaiThich);
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
      b.textContent = v==="co_loi" ? "⚠️ Có lỗi" : "✅ Không có lỗi";
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
    let head = kq.diem ? "✅ <b>Chính xác!</b> " : "❌ <b>Chưa đúng.</b> ";
    if(kq.batOan) head += "Câu này ĐÚNG — em đã 'bắt oan'. ";
    if(kq.boSot) head += "Câu này CÓ lỗi (" + META.loaiLoi[item.loaiLoi].ten + ") — em đã bỏ sót. ";
    box.innerHTML = head + esc(item.giaiThich);
    $("dt-nop").disabled = true;
    $("dt-tiep").style.display = "";
    $("dt-tiep").textContent = (dt.i < dt.ds.length-1) ? "Câu tiếp theo →" : "Xem kết quả của em 🏁";
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
      <p><button class="btn" id="btn-csv">⬇ Xuất CSV nhật ký lớp (minh chứng)</button>
         <button class="btn" id="btn-json">⬇ Xuất JSON đầy đủ</button>
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

  /* ================= KHỞI ĐỘNG ================= */
  window.addEventListener("DOMContentLoaded", ()=>{
    // Gộp ngân hàng mở rộng (nếu có) vào ngân hàng chính — 1 lần duy nhất
    if(window.MX_BANK_MORE && window.MX_BANK_MORE.length && !window.MX_BANK._merged){
      window.MX_BANK = window.MX_BANK.concat(window.MX_BANK_MORE);
      Object.defineProperty(window.MX_BANK, "_merged", {value:true});
    }
    $("btn-vao").onclick = dangNhap;
    $("btn-ve-home").onclick = ()=>hien("v-home");
    $("btn-lab").onclick = ()=>{ hien("v-lab"); labBuoc(1); };
    $("btn-dautruong").onclick = ()=>{ hien("v-dautruong"); dtBatDau("luyen"); };
    $("dt-btn-luyen").onclick = ()=>dtBatDau("luyen");
    $("dt-btn-pre").onclick   = ()=>dtBatDau("pre");
    $("dt-btn-post").onclick  = ()=>dtBatDau("post");
    $("btn-baocao").onclick = ()=>{ hien("v-baocao"); veBaoCao(); };
    $("btn-logic").onclick = ()=>{ hien("v-logic"); window.MX_LOGIC.init(maHS); };
    $("btn-kienthuc").onclick = ()=>{ hien("v-kienthuc"); window.MX_KIEN_THUC.init(maHS); };
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
