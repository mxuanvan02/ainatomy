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
    let ddTong=0, ddKhop=0, ddBoQua=0;

    for(const sk of suKien){
      /* ---- MỨC 3 (DỰ ĐOÁN TRƯỚC KHI CHẠY) — thêm 06/10 ----
       * LỖI ĐÃ SỬA: 13 ô Mức 3 có ghi sự kiện `loai:"duDoan"` nhưng hàm này KHÔNG có
       * nhánh nào đọc nó (grep -c "duDoan" js/engine.js trả về 0 trước khi sửa). Hệ quả:
       * dự đoán không xuất hiện trong Bản đồ năng lực, không có trong baocao_lop, và CSV
       * của giáo viên không phân biệt được "học sinh dự đoán sai" với "học sinh không
       * thèm dự đoán". Toàn bộ công sức thiết kế 13 ô chết ở khâu báo cáo — đúng chỗ mà
       * giáo viên cần nó nhất để biết lớp hiểu bài tới đâu.
       *
       * Hai dạng sự kiện được đọc:
       *   suKien:"doiChieu" + kq.dung  -> đã dự đoán và đã đối chiếu với kết quả thật
       *   suKien:"boQua"               -> bấm nút chạy mà CHƯA chốt dự đoán (ghi để CSV
       *                                   nói thật; không có sự kiện này thì số liệu trông
       *                                   đẹp hơn thực tế vì chỉ đếm người có tham gia)
       * `kq.dung` do bên ghi chuẩn hoá sẵn (ô số/ô chọn: khop; ô tự luận: chạm >= 60%
       * phương diện), nên ở đây chỉ đọc một dạng, không phải đoán hình dạng dữ liệu. */
      if(sk.loai === "duDoan"){
        if(sk.suKien === "doiChieu" && sk.kq && sk.kq.dung !== undefined){
          ddTong++;
          if(sk.kq.dung) ddKhop++;
        } else if(sk.suKien === "boQua"){
          ddBoQua++;
        }
      }
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
      /* Mức 3: ddTong = số lần dự đoán ĐÃ đối chiếu với kết quả thật;
       * ddBoQua = số lần bấm chạy mà không chốt dự đoán. Cả hai đều phải hiện ra:
       * chỉ báo ddTong thì một lớp toàn người bỏ qua trông như "chưa dạy tới",
       * còn báo cả hai thì giáo viên thấy đúng mức độ tham gia. */
      duDoan: { tong: ddTong, khop: ddKhop, boQua: ddBoQua,
                tiLe: ddTong ? ddKhop/ddTong : null },
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
      /* ĐIỀU KIỆN VÀO MẪU — sửa 06/10. Bản cũ là `if(!th.dauTruong.tong) continue;`, tức
       * một HS CHỈ dự đoán Mức 3 mà chưa vào đấu trường thì bị bỏ hẳn khỏi báo cáo lớp,
       * và không được đếm vào soHS. Đó là tái tạo đúng lỗ hổng đang sửa ("Mức 3 vô hình
       * trong báo cáo") ở một tầng khác: dữ liệu có, nhưng bị lọc mất trước khi cộng.
       * Nay nhận HS có bất kỳ dấu vết tham gia nào trong ba loại. */
      const coDauVet = th.dauTruong.tong || th.lab.tong
                    || th.duDoan.tong || th.duDoan.boQua;
      if(!coDauVet) continue;
      n++;
      if(!gop){
        gop = {
          dauTruong:{tong:0,dung:0}, lab:{tong:0,dung:0},
          /* duDoan phải được khởi tạo Ở ĐÂY: bản vá đầu tiên chỉ thêm phép tính
           * `gop.duDoan.tiLe = ...` ở cuối hàm mà quên khai trường này, nên gop.duDoan
           * là undefined và dòng đó ném TypeError. Lỗi không lộ khi đọc lướt vì cú pháp
           * hợp lệ — chỉ chạy thật mới nổ. */
          duDoan:{tong:0,khop:0,boQua:0},
          recall: {}, soHS: 0
        };
        for(const l in META.loaiLoi) gop.recall[l] = {phatHien:0, tongCoLoi:0, batOan:0};
      }
      gop.dauTruong.tong += th.dauTruong.tong;
      gop.dauTruong.dung += th.dauTruong.dung;
      gop.lab.tong += th.lab.tong;
      gop.lab.dung += th.lab.dung;
      gop.duDoan.tong   += th.duDoan.tong;
      gop.duDoan.khop   += th.duDoan.khop;
      gop.duDoan.boQua  += th.duDoan.boQua;
      for(const r of th.recallTheoLoai){
        gop.recall[r.maLoai].phatHien += r.phatHien;
        gop.recall[r.maLoai].tongCoLoi += r.tongCoLoi;
        gop.recall[r.maLoai].batOan += r.batOan;
      }
    }
    if(!gop) return null;
    gop.soHS = n;
    gop.tiLe = gop.dauTruong.tong ? gop.dauTruong.dung/gop.dauTruong.tong : 0;
    /* GỘP MỨC 3 LÊN CẤP LỚP — thêm 06/10. Trước đây hàm này cộng dauTruong, lab và recall
     * nhưng KHÔNG cộng duDoan, nên dù tongHop() của từng HS đã có số liệu Mức 3 thì báo cáo
     * cấp lớp vẫn mù — mà báo cáo lớp mới là thứ giáo viên nhìn để nhận xét cả lớp.
     * tiLe = null (không phải 0) khi chưa ai đối chiếu, để giao diện in "—" thay vì in
     * "0%" và khiến giáo viên tưởng cả lớp dự đoán sai hết. */
    gop.duDoan.tiLe = gop.duDoan.tong ? gop.duDoan.khop/gop.duDoan.tong : null;
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
    /* CỘT `su_kien` — thêm 06/10. Trước đây ba trạng thái của Mức 3 (chot / doiChieu /
     * boQua) được ghi vào localStorage nhưng CSV KHÔNG có cột nào chứa chúng, nên tệp GV
     * tải về không phân biệt được "dự đoán sai" với "không thèm dự đoán" — đúng lỗ hổng
     * mà phản biện vòng 9 chỉ ra. Thêm cột thay vì nhét vào cột sẵn có, vì nhét thì mất
     * nghĩa của cột cũ.
     *
     * ĐẶT CUỐI BẢNG (không chèn giữa): tools/gop_csv.py đọc CSV bằng dict(zip(head, row))
     * tức THEO TÊN CỘT nên chèn đâu cũng được, nhưng tệp CSV mà GV đã tải về trước đây có
     * header 19 cột; đặt cột mới ở cuối thì tệp cũ và tệp mới cùng được đọc đúng theo tên,
     * không phải lo thứ tự. */
    const rows = [["ma_hs","ma_lop","loai_su_kien","item_id","mach","unesco","dap_an_dung","loai_loi_that","tra_loi","tra_loi_loai","diem","bat_oan","bo_sot","che_do","phien_tong","phien_dung","phien_bat_oan","phien_bo_sot","thoi_gian_ISO","su_kien","phai_lap"]];
    for(const k in d){
      if(maLop && d[k].maLop && d[k].maLop !== maLop) continue;
      for(const sk of d[k].suKien){
        const kq = sk.kq || {};
        rows.push([
          k, d[k].maLop || "", sk.loai,
          /* item_id: sự kiện Mức 3 không có kq.itemId (nó không phải nhiệm vụ đấu trường)
           * mà mang mã bài ở sk.baiToan ("BT-10"...). Không fallback thì cả 13 ô đổ về
           * item_id rỗng và tools/gop_csv.py khử trùng lặp theo (ma_hs, item_id, thoi_gian)
           * sẽ coi chúng là bản sao của nhau. */
          kq.itemId || sk.nhiemVuId || sk.baiToan || "",
          kq.mach || (sk.nhiemVu?sk.nhiemVu.mach:"") || "",
          kq.unesco || (sk.nhiemVu?sk.nhiemVu.unesco:"") || "",
          kq.loaiThat || kq.dapAn || "", kq.loaiLoiThat || "",
          /* tra_loi: với Mức 3 câu trả lời của HS là kq.duDoan (con số dự đoán, id phương
           * án, hoặc "6/6" với ô tự luận). Không fallback thì cột trả lời của 13 ô trống. */
          kq.traLoiVerdict || kq.chon || kq.duDoan || "", kq.traLoiLoai || "",
          kq.diem!==undefined?kq.diem:"", kq.batOan?1:0, kq.boSot?1:0,
          sk.cheDo || "", sk.tong!==undefined?sk.tong:"", sk.dung!==undefined?sk.dung:"",
          sk.batOan!==undefined?sk.batOan:"", sk.boSot!==undefined?sk.boSot:"",
          new Date(sk.t).toISOString(),
          sk.suKien || "",
          /* CỘT `phai_lap` — thêm 07/10, và đây là lỗi do CHÍNH đợt vá trước tạo ra.
           * Ở commit trước tôi cho dtBatDau() loại những câu học sinh đã gặp, và khi ngân
           * hàng cạn thì ghi `phaiLap: 1` vào sự kiện phiên, kèm lời hứa NGUYÊN VĂN trong
           * comment: "ghi cờ phaiLap vào nhật ký để tools/gop_csv.py và bất kỳ ai đọc số liệu
           * sau này lọc bỏ được những phiên không còn là phép đo sạch".
           * NHƯNG hàm xuất CSV này không có cột nào mang cờ đó — nên lời hứa không thành sự
           * thật: công cụ gộp không có gì để lọc, và những phiên phải lặp câu vẫn bị trộn vào
           * hiệu pre/post như thường. Writer ghi một trường mà reader không xuất thì trường đó
           * không tồn tại với người dùng cuối — cùng lớp lỗi với việc engine.js từng không đọc
           * sự kiện duDoan, và cùng lớp với G14c từng có một chiều là code chết.
           * Đặt CUỐI bảng để tệp CSV cũ (19 và 20 cột) vẫn đọc đúng theo tên. */
          sk.phaiLap !== undefined ? sk.phaiLap : ""
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

  /* ================= XÁO VỊ TRÍ PHƯƠNG ÁN (chống mẹo không cần đọc hiểu) =========
   *
   * VÌ SAO CÓ HÀM NÀY (06/10) — số đo trên chính dữ liệu của repo, không phỏng đoán:
   *   js/tinhhuong.js : đáp án là "b" ở 11/12 câu, và "b" đồng thời là phương án DÀI
   *                     NHẤT ở 11/12 câu  -> mẹo "luôn bấm B" đạt 92%.
   *   js/lab.js       : đáp án là "b" ở 4/4 câu, và là phương án dài nhất ở 4/4 câu
   *                     -> mẹo đó đạt 100%.
   *   data/cauhoi.js + cauhoi_moRong.js : claim sai nằm ở vị trí giữa 26/53 item.
   * Một học sinh KHÔNG ĐỌC câu hỏi vẫn đạt 92–100%. Điều đó phá đúng tuyên bố cốt lõi
   * của sản phẩm ("tự chấm khách quan bằng oracle"): con số thu về không còn đo năng
   * lực, nên pre/post và recall đều vô nghĩa nếu học sinh phát hiện ra mẹo.
   *
   * HÀM NÀY SỬA ĐƯỢC GÌ VÀ KHÔNG SỬA ĐƯỢC GÌ — nói rõ để không ai tưởng đã xong:
   *   SỬA ĐƯỢC  mẹo "luôn bấm chữ B". Sau khi xáo, chữ cái hiển thị của đáp án thay đổi
   *             theo câu và theo học sinh, nên không còn vị trí cố định để lợi dụng.
   *   KHÔNG SỬA ĐƯỢC mẹo "chọn phương án dài nhất". Đó là lỗi NỘI DUNG: phương án nhiễu
   *             được viết ngắn hơn đáp án. Không phép xáo trộn nào thay đổi được độ dài
   *             tương đối. Muốn diệt phải VIẾT LẠI phương án nhiễu cho cân độ dài — việc
   *             của tác giả, không phải của mã. Cổng G12 đo cả hai con số và in ra để
   *             khoản nợ này không bị quên.
   *
   * TẤT ĐỊNH theo (mã phiên + id câu): cùng một học sinh mở lại trang vẫn thấy thứ tự cũ
   * (không xáo giữa chừng khi làm lại một câu), nhưng hai học sinh khác nhau thấy thứ tự
   * khác nhau nên không thể chuyền nhau "câu 3 đáp án B". Đặt mã phiên trên window để
   * phép kiểm tự động ghim lại được khi cần tái lập.
   */
  function bamDuong(s){
    let h = 0x811c9dc5;
    for(let i = 0; i < s.length; i++){ h ^= s.charCodeAt(i); h = (h * 0x01000193) >>> 0; }
    return h >>> 0;
  }

  function maPhien(){
    if(window.MX_SEED_PHIEN != null) return String(window.MX_SEED_PHIEN);
    if(!window.__SOIAI_PHIEN){
      window.__SOIAI_PHIEN = String((Date.now() ^ Math.floor(Math.random() * 0xffffffff)) >>> 0);
    }
    return window.__SOIAI_PHIEN;
  }

  function xaoLuaChon(ds, mam){
    if(!ds) return [];
    if(ds.length < 2) return ds.slice();
    /* cùng bộ số LCG đã dùng ở js/nhamay_tram01.js — giữ nhất quán trong repo */
    let seed = bamDuong(maPhien() + "|" + String(mam == null ? "" : mam));
    const rnd = () => (seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296;
    const a = ds.slice();
    for(let i = a.length - 1; i > 0; i--){
      const j = Math.floor(rnd() * (i + 1));
      const t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  }

  /* Chữ cái hiển thị theo VỊ TRÍ sau khi xáo (0 -> A). Phải lấy theo vị trí chứ không
   * lấy `l.id`: id là nhãn cố định trong dữ liệu, nếu in nó ra thì đáp án vẫn luôn hiện
   * là chữ B dù các phương án đã đổi chỗ — xáo trộn thành vô nghĩa. */
  function chuCai(i){ return String.fromCharCode(65 + i); }

  window.MX_ENGINE = {
    doc, ghi, vaoLop, logSuKien,
    chamDauTruong, chamLab,
    tongHop, taoNhanXet, tongHopLop, bangNhamLan,
    xuatCSV, xuatJSON, xoaHet,
    xaoLuaChon, chuCai, maPhien
  };
})();
