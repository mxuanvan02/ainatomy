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
    h.innerHTML = svgIco("circle-help") + " <b>Dự đoán trước khi chạy (Mức 3)</b>";
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
        p1.innerHTML = (khop ? svgIco("check") : svgIco("target"))
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
    h.innerHTML = svgIco("circle-help") + " <b>Dự đoán trước khi chạy (Mức 3)</b>";
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

  window.MX_DUDOAN = { veTruot, veChon, pct, esc, svgIco };
})();
