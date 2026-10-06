/* SOI AI — duDoan.js : Ô "DỰ ĐOÁN TRƯỚC KHI CHẠY" (Mức 3 của khung ba mức).
 *
 * VÌ SAO CÓ TỆP NÀY
 *   THIET_KE_BAI_TOAN.md PHẦN 4.4 định nghĩa Mức 3 = "EM DỰ ĐOÁN TRƯỚC": học sinh
 *   phải nói ra điều mình nghĩ TRƯỚC khi hệ chạy, rồi hệ so dự đoán với kết quả thật.
 *   Không có bước này thì học sinh chỉ bấm nút và xem — không lộ ra được mình đang
 *   hiểu mô hình đến đâu. Giáo viên cũng không có bằng chứng học sinh nghĩ gì.
 *   PHẦN 6 của tài liệu liệt kê đây là việc CHƯA CÓ; tệp này phủ bốn chỗ:
 *     BT-02  dự đoán độ chính xác mô hình A trước khi bấm "Chấm nhãn"      (Trạm 1)
 *     BT-04  dự đoán nhãn của một điểm 3D trước khi hệ tiết lộ              (Phòng 3D)
 *     BT-05  dự đoán tỉ lệ đúng ban đêm trước khi bấm "Đánh giá"            (Phòng 3D)
 *     BT-11  dự đoán hiện tượng ở đầu ra trước khi hệ làm hỏng một trạm     (Ống dẫn 3D)
 *
 * CƠ CHẾ CHẤM (giữ đúng nguyên tắc oracle của toàn sản phẩm)
 *   Dự đoán là CON SỐ hoặc PHƯƠNG ÁN học sinh chốt TRƯỚC; kết quả thật do hệ tính
 *   sau. So sánh là phép toán tất định:
 *     - dự đoán số: khớp nếu |dự đoán − kết quả| <= dungSai (mặc định 10 điểm %).
 *     - dự đoán phương án: khớp nếu chọn đúng phương án hệ đã chọn.
 *   KHÔNG có điểm số: phản hồi chỉ là "khớp" / "chênh lệch bao nhiêu", và kết quả
 *   ghi vào nhật ký lớp (ENG.logSuKien) để giáo viên xem học sinh nghĩ gì trước
 *   khi chạy — đúng ràng buộc Khung 2422 phần VI (không xác lập đầu điểm riêng).
 *
 * CHỐNG DÒ ĐÁP ÁN
 *   Mỗi ô dự đoán chỉ chốt được MỘT lần (nút khoá lại sau khi bấm). Muốn dự đoán
 *   tiếp phải tạo lại bộ dữ liệu/lượt chơi mới — khi đó đáp án cũ cũng đổi theo.
 *
 * AN TOÀN
 *   Giao diện dựng bằng createElement + textContent; chuỗi duy nhất đi qua innerHTML
 *   là svgIco() (hằng số tĩnh). Không có dữ liệu người dùng nào trở thành HTML.
 */
(function(){
  "use strict";

  function esc(s){
    return String(s == null ? "" : s).replace(/[&<>"]/g, c =>
      ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));
  }

  function svgIco(ten){
    return '<svg class="ic" aria-hidden="true"><use href="#i-' + ten + '"/></svg>';
  }

  function pct(x){
    return x == null ? "—" : Math.round(x * 100) + "%";
  }

  /* Bỏ dấu tiếng Việt + hạ chữ thường, để so khớp từ khoá không phân biệt dấu.
   * VÌ SAO CẦN: ô tự luận (veTuLuan) so chữ học sinh gõ với danh sách từ khoá.
   * Học sinh gõ "dữ liệu" hay "du lieu" đều phải khớp như nhau.
   * Bản sao CÓ CHỦ ĐÍCH của chuanHoa() trong js/bt09.js và js/bt13.js: mỗi module tự
   * chứa hàm này để không phụ thuộc thứ tự nạp script — nếu gọi hàm của module khác
   * thì tệp này hỏng khi tệp kia chưa nạp, và ong đó đúng là lớp lỗi G11a đang bắt. */
  function chuanHoa(s){
    return String(s == null ? "" : s).toLowerCase()
      .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
      .replace(/đ/g, "d").replace(/\s+/g, " ").trim();
  }

  /* ================= Ô DỰ ĐOÁN BẰNG THANH TRƯỢT (BT-02, BT-05) ============
   * opts: { cauHoi, donVi:'%', dungSai:0.10, ghiChu, onChot(giaTri0_1) }
   * Học sinh kéo thanh, bấm "Chốt dự đoán" → khoá ô, gọi onChot.
   * Trả về { giaTri(), daChot(), moKhoa() }. */
  function veTruot(host, opts){
    if(!host) return null;
    host.innerHTML = "";
    const card = document.createElement("div");
    card.className = "card";
    card.style.background = "var(--nen2)";
    card.style.borderLeft = "4px solid var(--nhan)";

    const h = document.createElement("p");
    h.innerHTML = svgIco("circle-help") + " <b>Dự đoán trước khi chạy</b>";
    card.appendChild(h);

    const q = document.createElement("p");
    q.className = "chu2";
    q.textContent = opts.cauHoi;
    card.appendChild(q);

    const lab = document.createElement("label");
    const idIn = "dd-truot-" + Math.random().toString(36).slice(2, 8);
    lab.setAttribute("for", idIn);
    lab.innerHTML = 'Dự đoán của em: <b class="dd-gia-tri">50%</b>';
    card.appendChild(lab);

    const inp = document.createElement("input");
    inp.type = "range"; inp.min = "0"; inp.max = "100"; inp.step = "1";
    inp.value = "50"; inp.id = idIn;
    const giaTriHien = lab.querySelector(".dd-gia-tri");
    inp.addEventListener("input", () => { giaTriHien.textContent = inp.value + "%"; });
    card.appendChild(inp);

    if(opts.ghiChu){
      const gc = document.createElement("p");
      gc.className = "nho chu2";
      gc.textContent = opts.ghiChu;
      card.appendChild(gc);
    }

    const nut = document.createElement("button");
    nut.className = "btn chinh";
    nut.textContent = "Chốt dự đoán";
    card.appendChild(nut);

    const fb = document.createElement("div");
    fb.className = "phanhoi";
    card.appendChild(fb);

    host.appendChild(card);

    let chot = null;
    nut.onclick = () => {
      if(chot !== null) return;                 // chống dò đáp án: chỉ chốt MỘT lần
      chot = parseInt(inp.value, 10) / 100;
      nut.disabled = true;
      inp.disabled = true;
      nut.textContent = "Đã chốt: " + inp.value + "%";
      if(opts.onChot) opts.onChot(chot);
    };

    const api = {
      giaTri: () => chot,
      daChot: () => chot !== null,
      /* true sau khi doiChieu() đã chạy — app.js dùng cờ này để biết ô đã được
       * so với kết quả thật, không đối chiếu lại lần hai ở lượt chơi sau. */
      daDoiChieu: false,
      /* So dự đoán với kết quả thật — chỉ gọi SAU khi hệ chạy xong. */
      doiChieu(ketQuaThat){
        if(chot === null) return null;
        api.daDoiChieu = true;
        const dungSai = opts.dungSai != null ? opts.dungSai : 0.10;
        const lech = Math.abs(chot - ketQuaThat);
        const khop = lech <= dungSai;
        fb.className = "phanhoi " + (khop ? "dung" : "sai");
        const p1 = document.createElement("p");
        p1.innerHTML = (khop ? svgIco("check") : svgIco("triangle-alert"))
          + " <b>" + (khop ? "Dự đoán khớp kết quả thật." : "Dự đoán lệch kết quả thật.") + "</b>";
        fb.appendChild(p1);
        const p2 = document.createElement("p");
        p2.className = "chu2";
        p2.textContent = "Em dự đoán " + pct(chot) + " · kết quả thật " + pct(ketQuaThat)
          + " · chênh " + Math.round(lech * 100) + " điểm % (ngưỡng khớp ±"
          + Math.round(dungSai * 100) + ").";
        fb.appendChild(p2);
        const p3 = document.createElement("p");
        p3.className = "nho chu2";
        p3.textContent = khop
          ? "Em đã hình dung được mô hình hoạt động thế nào trước khi thấy kết quả — đó là điều Mức 3 muốn rèn."
          : "Không sao: chỗ lệch chính là chỗ đáng soi. Hãy xem bảng kết quả bên dưới và tìm vì sao con số thật lại như vậy.";
        fb.appendChild(p3);
        return { khop, duDoan: chot, ketQua: ketQuaThat, lech };
      }
    };
    api.host = card;
    return api;
  }

  /* ================= Ô DỰ ĐOÁN BẰNG PHƯƠNG ÁN (BT-04, BT-11) =============
   * opts: { cauHoi, phuongAn:[{id,text}], onChot(id) }
   * Trả về { giaTri(), daChot(), doiChieu(dapAnId, giaiThich) }. */
  function veChon(host, opts){
    if(!host) return null;
    host.innerHTML = "";
    const card = document.createElement("div");
    card.className = "card";
    card.style.background = "var(--nen2)";
    card.style.borderLeft = "4px solid var(--vang)";

    const h = document.createElement("p");
    h.innerHTML = svgIco("circle-help") + " <b>Dự đoán trước khi chạy</b>";
    card.appendChild(h);

    const q = document.createElement("p");
    q.className = "chu2";
    q.textContent = opts.cauHoi;
    card.appendChild(q);

    const chips = document.createElement("div");
    chips.className = "chips";
    const fb = document.createElement("div");
    fb.className = "phanhoi";

    let chot = null;
    opts.phuongAn.forEach(pa => {
      const nut = document.createElement("button");
      nut.className = "btn";
      nut.textContent = pa.text;
      nut.onclick = () => {
        if(chot !== null) return;               // chống dò đáp án: chỉ chốt MỘT lần
        chot = pa.id;
        [...chips.children].forEach(c => { c.disabled = true; });
        nut.classList.add("chon");
        if(opts.onChot) opts.onChot(pa.id);
      };
      chips.appendChild(nut);
    });

    card.appendChild(chips);
    card.appendChild(fb);
    host.appendChild(card);

    const api = {
      giaTri: () => chot,
      daChot: () => chot !== null,
      daDoiChieu: false,                        // cờ như ở veTruot
      doiChieu(dapAnId, giaiThich){
        if(chot === null) return null;
        api.daDoiChieu = true;
        const khop = chot === dapAnId;
        const dung = opts.phuongAn.find(p => p.id === dapAnId);
        fb.className = "phanhoi " + (khop ? "dung" : "sai");
        const p1 = document.createElement("p");
        p1.innerHTML = (khop ? svgIco("check") : svgIco("x"))
          + " <b>" + (khop ? "Dự đoán khớp." : "Dự đoán chưa khớp.") + "</b>";
        fb.appendChild(p1);
        const p2 = document.createElement("p");
        p2.className = "chu2";
        p2.textContent = "Kết quả thật: " + (dung ? dung.text : dapAnId) + ".";
        fb.appendChild(p2);
        if(giaiThich){
          const p3 = document.createElement("p");
          p3.className = "nho chu2";
          p3.textContent = giaiThich;
          fb.appendChild(p3);
        }
        return { khop, duDoan: chot, dapAn: dapAnId };
      }
    };
    api.host = card;
    return api;
  }

  /* ============ Ô DỰ ĐOÁN BẰNG BÀI VIẾT TỰ DO (BT-10, BT-12) ==============
   * VÌ SAO CẦN DẠNG Ô THỨ BA: hai dạng trên đều so với một đáp án. Nhưng thiết kế
   * (THIET_KE_BAI_TOAN.md PHẦN 4.5) ghi rõ: "ở chặng 2 và 3 thì BT-10 và BT-12 không
   * còn đáp án duy nhất" — học sinh đề xuất biện pháp cho dự án CỦA CHÍNH MÌNH, viết
   * nguyên tắc dùng AI của riêng mình. Không có đáp án nào để so, nên nếu bịa ra một
   * "đáp án đúng" thì phép chấm thành giả.
   *
   * CÁCH CHẤM (vẫn tất định, vẫn không cần giáo viên):
   *   Không chấm "đúng/sai" mà chấm "bài viết có CHẠM các phương diện bắt buộc không".
   *   Mỗi phương diện là một danh sách cụm từ khoá; bài viết chạm được thì tính. Đây
   *   là phép đếm tất định trên chuỗi đã chuẩn hoá bỏ dấu — cùng cơ chế với rubric
   *   prompt của Trạm 5 (js/nhamay_text.js hàm danhGiaPrompt), không phải phán đoán.
   *   Kết quả là "chạm N/M phương diện", KHÔNG phải điểm số — đúng phần VI Khung 2422.
   *
   * opts: { cauHoi, goiY, soTuToiThieu, phuongDien:[{ma, moTa, tuKhoa:[...]}], onChot(text) }
   * Trả về { giaTri(), daChot(), doiChieu() }. */
  function veTuLuan(host, opts){
    if(!host) return null;
    host.innerHTML = "";
    const card = document.createElement("div");
    card.className = "card";
    card.style.background = "var(--nen2)";
    card.style.borderLeft = "4px solid var(--dung)";

    const h = document.createElement("p");
    h.innerHTML = svgIco("circle-help") + " <b>Viết ra trước khi xem gợi ý</b>";
    card.appendChild(h);

    const q = document.createElement("p");
    q.className = "chu2";
    q.textContent = opts.cauHoi;
    card.appendChild(q);

    const idTa = "dd-viet-" + Math.random().toString(36).slice(2, 8);
    const ta = document.createElement("textarea");
    ta.id = idTa; ta.rows = 5;
    ta.placeholder = opts.goiY || "Viết câu trả lời của em...";
    card.appendChild(ta);

    const dem = document.createElement("p");
    dem.className = "nho chu2";
    const toiThieu = opts.soTuToiThieu || 25;
    const demTu = () => {
      const n = ta.value.trim().split(/\s+/).filter(Boolean).length;
      dem.textContent = n + " từ" + (n < toiThieu ? " · cần thêm " + (toiThieu - n) + " từ nữa mới chốt được" : " · đủ để chốt");
    };
    demTu();
    ta.addEventListener("input", demTu);
    card.appendChild(dem);

    const nut = document.createElement("button");
    nut.className = "btn chinh";
    nut.textContent = "Chốt bài viết";
    card.appendChild(nut);

    const fb = document.createElement("div");
    fb.className = "phanhoi";
    card.appendChild(fb);

    host.appendChild(card);

    let chot = null;
    nut.onclick = () => {
      if(chot !== null) return;                 // chống dò: chỉ chốt MỘT lần
      const t = ta.value.trim();
      if(t.split(/\s+/).filter(Boolean).length < toiThieu){
        dem.className = "nho sai";
        dem.textContent = "Bài viết còn ngắn quá — hãy viết rõ hơn rồi chốt.";
        return;
      }
      chot = t;
      nut.disabled = true;
      ta.disabled = true;
      nut.textContent = "Đã chốt bài viết";
      dem.className = "nho chu2";
      demTu();
      if(opts.onChot) opts.onChot(chot);
      /* Tự chấm NGAY sau khi chốt: ô tự luận không có "kết quả thật" nào ở bên ngoài để
       * chờ — chính bài viết là dữ liệu. Dùng setTimeout 0 để chạy SAU khi hàm này trả
       * về, vì biến `api` khai báo bằng const ở dưới, lúc này mới có giá trị. */
      if(opts.tuChamNgay) setTimeout(() => api.doiChieu(), 0);
    };

    const api = {
      giaTri: () => chot,
      daChot: () => chot !== null,
      daDoiChieu: false,
      doiChieu(){
        if(chot === null) return null;
        api.daDoiChieu = true;
        const s = chuanHoa(chot);
        const cham = (opts.phuongDien || []).map(pd => ({
          ma: pd.ma, moTa: pd.moTa,
          co: (pd.tuKhoa || []).some(k => s.includes(chuanHoa(k)))
        }));
        const dat = cham.filter(c => c.co);
        const tiLe = cham.length ? dat.length / cham.length : 0;
        fb.className = "phanhoi " + (tiLe >= 0.6 ? "dung" : "sai");

        const p1 = document.createElement("p");
        p1.innerHTML = (tiLe >= 0.6 ? svgIco("check") : svgIco("triangle-alert"))
          + " <b>Bài viết của em chạm " + dat.length + "/" + cham.length
          + " phương diện.</b>";
        fb.appendChild(p1);

        const ul = document.createElement("ul");
        ul.className = "nho chu2";
        cham.forEach(c => {
          const li = document.createElement("li");
          li.textContent = (c.co ? "Đã nêu: " : "Chưa nêu: ") + c.moTa;
          ul.appendChild(li);
        });
        fb.appendChild(ul);

        const p3 = document.createElement("p");
        p3.className = "nho chu2";
        p3.textContent = "Đây KHÔNG phải điểm số và không có đáp án đúng duy nhất — "
          + "chỉ liệt kê em đã chạm những phương diện nào. Em tự đọc lại bài mình "
          + "và bổ sung nếu thấy cần (theo phần VI Khung 2422).";
        fb.appendChild(p3);
        return { cham, dat: dat.length, tong: cham.length, tiLe };
      }
    };
    api.host = card;
    return api;
  }

  window.MX_DUDOAN = { veTruot, veChon, veTuLuan, pct, esc, svgIco };
})();
