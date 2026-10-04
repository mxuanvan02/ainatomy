/* SOI AI — TẦNG 2: ENGINE CHẤM TỰ ĐỘNG (oracle) + TẦNG 3: LOG & BẢN ĐỒ NĂNG LỰC
 * Nguyên tắc: đáp án đúng đã biết TRƯỚC từ lúc thiết kế (lỗi do hệ cài sẵn),
 * nên việc chấm là phép so sánh tất định — không cần giáo viên, không cần LLM khi chạy.
 * Toàn bộ dữ liệu lưu trong trình duyệt (localStorage), ẩn danh theo MÃ HỌC SINH,
 * không thu thập họ tên, không gửi gì ra ngoài. Có nút xuất CSV cho giáo viên.
 */
(function(){
  "use strict";

  const META = window.MX_META;
  const KEY = "soiai_dulieu_v1";

  /* ============ LOG (Tầng 3) ============ */
  function doc(){
    try{ return JSON.parse(localStorage.getItem(KEY) || "{}"); }catch(e){ return {}; }
  }
  function ghi(d){
    try{ localStorage.setItem(KEY, JSON.stringify(d)); }
    catch(e){ console.warn("Không lưu được dữ liệu:", e); }
  }

  function vaoLop(maHS, maLop){
    const d = doc();
    const now = Date.now();
    d[maHS] = d[maHS] || { maHS, maLop: maLop || "", tao: now, suKien: [] };
    if(maLop) d[maHS].maLop = maLop;
    ghi(d);
    return d[maHS];
  }

  /* Ghi một sự kiện; loai: "dauTruong" | "lab" | "huanLuyen" */
  function logSuKien(maHS, sk){
    const d = doc();
    if(!d[maHS]) return null;
    sk.t = Date.now();
    d[maHS].suKien.push(sk);
    ghi(d);
    return sk;
  }

  /* ============ CHẤM TẦNG 2 (Đấu trường bắt lỗi AI) ============
   * item: phần tử MX_BANK; traLoi: { verdict:'co_loi'|'dung', loaiLoi?:key }
   * Trả về kết quả chấm tất định.
   */
  function chamDauTruong(item, traLoi){
    const dungVerdict = (traLoi.verdict === item.loai);
    let dungLoai = null;
    if(item.loai === "co_loi" && traLoi.verdict === "co_loi"){
      dungLoai = (traLoi.loaiLoi === item.loaiLoi);
    }
    // Bắt oan: nói "có lỗi" trên câu đúng
    const batOan = (item.loai === "dung" && traLoi.verdict === "co_loi");
    // Bỏ sót: nói "không lỗi" trên câu có lỗi
    const boSot = (item.loai === "co_loi" && traLoi.verdict === "dung");

    const diem = dungVerdict && (item.loai === "dung" || dungLoai === true) ? 1 : 0;

    return {
      itemId: item.id,
      mach: item.mach,
      unesco: item.unesco,
      loaiThat: item.loai,
      loaiLoiThat: item.loaiLoi || null,
      traLoiVerdict: traLoi.verdict,
      traLoiLoai: traLoi.loaiLoi || null,
      dungVerdict, dungLoai, diem,
      batOan, boSot,
      giaiThich: item.giaiThich
    };
  }

  /* ============ CHẤM TẦNG 1 (nhiệm vụ lab có đáp án cứng) ============ */
  function chamLab(nhiemVu, chon){
    const dung = (chon === nhiemVu.dapAn);
    return {
      nhiemVuId: nhiemVu.id, mach: nhiemVu.mach, unesco: nhiemVu.unesco,
      chon, dapAn: nhiemVu.dapAn, diem: dung ? 1 : 0, dung,
      giaiThich: nhiemVu.giaiThich
    };
  }

  /* ============ BẢN ĐỒ NĂNG LỰC (Tầng 3) ============ */
  /* Tổng hợp từ log → ma trận 12 khối UNESCO × 4 mạch QĐ 2422 + recall theo loại lỗi */
  function tongHop(maHS){
    const d = doc();
    const hs = maHS ? d[maHS] : null;
    const suKien = hs ? hs.suKien : [];

    const khoi = {};              // unesco -> {dung, tong}
    for(const k in META.unesco) khoi[k] = { dung:0, tong:0 };
    const theoLoai = {};          // loaiLoi -> {phatHien, tongCoLoi, batOan}
    for(const l in META.loaiLoi) theoLoai[l] = { phatHien:0, tongCoLoi:0, batOan:0 };
    let dtTong=0, dtDung=0, labTong=0, labDung=0, hlTong=0;

    for(const sk of suKien){
      if(sk.loai === "dauTruong" && sk.kq){
        const kq = sk.kq;
        dtTong++;
        if(kq.diem) dtDung++;
        if(kq.unesco && khoi[kq.unesco]){ khoi[kq.unesco].tong++; if(kq.diem) khoi[kq.unesco].dung++; }
        if(kq.loaiThat === "co_loi"){
          const t = theoLoai[kq.loaiLoiThat];
          if(t){ t.tongCoLoi++; if(kq.diem) t.phatHien++; }
        }else if(kq.loaiThat === "dung" && kq.batOan){
          // "bắt oan" phân bổ vào loại lỗi HS đã chọn sai
          const t = theoLoai[kq.traLoiLoai];
          if(t) t.batOan++;
        }
      }
      if(sk.loai === "lab" && sk.kq){
        labTong++;
        if(sk.kq.diem) labDung++;
        const u = sk.nhiemVu && sk.nhiemVu.unesco;
        if(u && khoi[u]){ khoi[u].tong++; if(sk.kq.diem) khoi[u].dung++; }
      }
      if(sk.loai === "huanLuyen") hlTong++;
    }

    const tiLeDT = dtTong ? dtDung/dtTong : 0;
    return {
      maHS: maHS || "(tất cả)",
      soSuKien: suKien.length,
      dauTruong: { tong: dtTong, dung: dtDung, tiLe: tiLeDT },
      lab: { tong: labTong, dung: labDung },
      huanLuyenSoLan: hlTong,
      recallTheoLoai: Object.keys(theoLoai).map(k => ({
        maLoai: k, ten: META.loaiLoi[k].ten,
        phatHien: theoLoai[k].phatHien, tongCoLoi: theoLoai[k].tongCoLoi,
        batOan: theoLoai[k].batOan,
        recall: theoLoai[k].tongCoLoi ? theoLoai[k].phatHien/theoLoai[k].tongCoLoi : null
      })),
      banDoUNESCO: Object.keys(khoi).map(k => ({
        khoi: k, ten: META.unesco[k].ten, aspect: META.unesco[k].aspect,
        dung: khoi[k].dung, tong: khoi[k].tong,
        tiLe: khoi[k].tong ? khoi[k].dung/khoi[k].tong : null
      })),
      diemManh: null, diemYeu: null, nhanXet: ""
    };
  }

  /* Nhận xét tự động (tất định theo template — không cần LLM khi chạy) */
  function taoNhanXet(th){
    const co = th.recallTheoLoai.filter(r => r.tongCoLoi > 0);
    if(!co.length) return { diemManh:null, diemYeu:null, nhanXet:"Chưa có đủ dữ liệu để nhận xét. Hãy làm phần Đấu trường bắt lỗi AI trước." };
    const sx = co.slice().sort((a,b)=> b.recall - a.recall);
    const manh = sx[0], yeu = sx[sx.length-1];
    const tpl = th.dauTruong.tiLe >= 0.75 ? META.nhanXetMau.gioi
              : th.dauTruong.tiLe >= 0.5  ? META.nhanXetMau.kha
                                          : META.nhanXetMau.canCoGang;
    return {
      diemManh: manh.ten, diemYeu: yeu.ten,
      nhanXet: tpl.replace("{manh}", manh.ten).replace("{yeu}", yeu.ten)
    };
  }

  /* ============ Tổng hợp theo LỚP (aggregate, cho slide/poster) ============ */
  function tongHopLop(maLop){
    const d = doc();
    let gop = null, n = 0;
    for(const k in d){
      if(maLop && d[k].maLop && d[k].maLop !== maLop) continue;
      const th = tongHop(k);
      if(!th.dauTruong.tong) continue;
      n++;
      if(!gop){
        gop = {
          dauTruong:{tong:0,dung:0}, lab:{tong:0,dung:0},
          recall: {}, soHS: 0
        };
        for(const l in META.loaiLoi) gop.recall[l] = {phatHien:0, tongCoLoi:0, batOan:0};
      }
      gop.dauTruong.tong += th.dauTruong.tong;
      gop.dauTruong.dung += th.dauTruong.dung;
      gop.lab.tong += th.lab.tong;
      gop.lab.dung += th.lab.dung;
      for(const r of th.recallTheoLoai){
        gop.recall[r.maLoai].phatHien += r.phatHien;
        gop.recall[r.maLoai].tongCoLoi += r.tongCoLoi;
        gop.recall[r.maLoai].batOan += r.batOan;
      }
    }
    if(!gop) return null;
    gop.soHS = n;
    gop.tiLe = gop.dauTruong.tong ? gop.dauTruong.dung/gop.dauTruong.tong : 0;
    return gop;
  }

  /* ============ BẢNG NHẦM LẪN (confusion matrix) — phục vụ Bài 5 "Dữ liệu lôgic" ============
   * T = "thật sự CÓ lỗi", P = "HS phán quyết CÓ lỗi". Đếm 4 ô từ log, tất định, không cần người chấm.
   *   TP (bắt đúng)      : T ∧ P        → loaiThat='co_loi', verdict='co_loi'
   *   FP (bắt oan)       : ¬T ∧ P       → loaiThat='dung',   verdict='co_loi'  (= cờ batOan)
   *   FN (bỏ sót)        : T ∧ ¬P       → loaiThat='co_loi', verdict='dung'    (= cờ boSot)
   *   TN (xác nhận đúng) : ¬T ∧ ¬P      → loaiThat='dung',   verdict='dung'
   */
  function bangNhamLan(maHS){
    const d = doc();
    const hs = maHS ? d[maHS] : null;
    let TP=0, FP=0, FN=0, TN=0;
    const dem = (sk) => {
      const kq = sk.kq || {};
      if(kq.batOan) FP++;
      else if(kq.boSot) FN++;
      else if(kq.loaiThat === "co_loi" && kq.traLoiVerdict === "co_loi") TP++;
      else if(kq.loaiThat === "dung" && kq.traLoiVerdict === "dung") TN++;
    };
    if(hs) hs.suKien.filter(s => s.loai === "dauTruong").forEach(dem);
    else for(const k in d) d[k].suKien.filter(s => s.loai === "dauTruong").forEach(dem);
    const tong = TP+FP+FN+TN;
    const thatCoLoi = TP+FN, thatDung = FP+TN;
    return {
      TP, FP, FN, TN, tong,
      tiLeDung:   tong ? (TP+TN)/tong : null,
      tiLeBoSot:  thatCoLoi ? FN/thatCoLoi : null,   // false negative rate
      tiLeBatOan: thatDung  ? FP/thatDung  : null    // false positive rate
    };
  }

  /* ============ XUẤT DỮ LIỆU (cho giáo viên làm bằng chứng hồ sơ) ============ */
  function xuatCSV(maLop){
    const d = doc();
    const rows = [["ma_hs","ma_lop","loai_su_kien","item_id","mach","unesco","dap_an_dung","loai_loi_that","tra_loi","tra_loi_loai","diem","bat_oan","bo_sot","che_do","phien_tong","phien_dung","phien_bat_oan","phien_bo_sot","thoi_gian_ISO"]];
    for(const k in d){
      if(maLop && d[k].maLop && d[k].maLop !== maLop) continue;
      for(const sk of d[k].suKien){
        const kq = sk.kq || {};
        rows.push([
          k, d[k].maLop || "", sk.loai,
          kq.itemId || sk.nhiemVuId || "", kq.mach || (sk.nhiemVu?sk.nhiemVu.mach:"") || "",
          kq.unesco || (sk.nhiemVu?sk.nhiemVu.unesco:"") || "",
          kq.loaiThat || kq.dapAn || "", kq.loaiLoiThat || "",
          kq.traLoiVerdict || kq.chon || "", kq.traLoiLoai || "",
          kq.diem!==undefined?kq.diem:"", kq.batOan?1:0, kq.boSot?1:0,
          sk.cheDo || "", sk.tong!==undefined?sk.tong:"", sk.dung!==undefined?sk.dung:"",
          sk.batOan!==undefined?sk.batOan:"", sk.boSot!==undefined?sk.boSot:"",
          new Date(sk.t).toISOString()
        ]);
      }
    }
    return rows.map(r => r.map(x => {
      const s = String(x===undefined||x===null?"":x);
      return /[",\n]/.test(s) ? '"' + s.replace(/"/g,'""') + '"' : s;
    }).join(",")).join("\n");
  }

  function xuatJSON(){ return JSON.stringify(doc(), null, 1); }

  function xoaHet(){ localStorage.removeItem(KEY); }

  window.MX_ENGINE = {
    doc, ghi, vaoLop, logSuKien,
    chamDauTruong, chamLab,
    tongHop, taoNhanXet, tongHopLop, bangNhamLan,
    xuatCSV, xuatJSON, xoaHet
  };
})();
