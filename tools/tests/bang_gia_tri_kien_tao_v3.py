#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""BẢNG GIÁ TRỊ KIẾN TẠO v3 — truy vết CHUỖI BẰNG CHỨNG thay vì quét chuỗi.

VÌ SAO CÓ BẢN NÀY (hai bản trước sai, và reviewer độc lập bắt được).
  Bản v1/v2 tìm bằng chứng bằng regex `yccd\s*:\s*"..."` — chỉ bắt giá trị LITERAL. Nhưng app
  ghi nhật ký bằng BIẾN: `yccd: q.yccd` (app.js:1145, app.js:1274), còn mã thật nằm trong tệp
  dữ liệu (js/tinhhuong.js, js/nhamay_tram01.js, data/kienthuc.js). Hệ quả đo được:
    · 10.A2.1 bị ghi co_cham_log=False dù nó CÓ chuỗi log chấm điểm thật (reviewer A bác đúng);
    · 7 mã bị phán "PHỦ THẬT" trong khi 0 bằng chứng của chúng có log — tự mâu thuẫn với chính
      định nghĩa "PHỦ THẬT = được chấm và ghi nhật ký" mà docstring bản v2 viết ra.
  Ngoài ra bản v2 gán loại thao tác theo TRẠM (v-nhamay = "tự xuất"), mà một trạm có nhiều kiểu
  tương tác: trạm Nhà máy vừa có ô GÕ prompt vừa có câu hỏi TRẮC NGHIỆM tram0. 10.C2.1 được phủ bởi
  tram0 (chọn 1 trong N) nên bị nâng oan lên "tự xuất" (reviewer B bác đúng).

CÁCH LÀM CỦA BẢN NÀY — đơn vị bằng chứng là LOG CALL SITE, không phải tệp, không phải trạm.
  Mỗi lời gọi logSuKien() chính là MỘT thao tác của học sinh được ghi lại, nên nó là đơn vị đúng:
    1. quét mọi log call site trong js/, cắt payload bằng CÂN BẰNG NGOẶC (không regex thô);
    2. với mỗi site, ghi nhận: có trường `diem` không, `yccd` là LITERAL hay BIẾN, hàm bao ngoài;
    3. nếu là BIẾN thì truy ngược: hàm bao ngoài tham chiếu `window.MX_*` nào -> mô-đun đó được
       gán ở tệp nào -> tệp dữ liệu đó khai những mã YCCĐ nào. Đó là chuỗi data -> log -> CSV.
    4. loại thao tác gán THEO SITE (chọn phương án / gõ tự do / chỉ chỗ sai / dự đoán-đối chiếu),
       không theo trạm.

HAI TRỤC, VÌ MỘT TRỤC KHÔNG ĐỦ.
  Trục A — THAO TÁC: tự xuất ra (gõ, chỉ chỗ, dự đoán) mạnh hơn nhận diện (chọn 1 trong N).
  Trục B — QUY VỀ MÃ: bản ghi có mang mã YCCĐ tới tệp CSV của giáo viên không.
  Hai trục này ĐỘC LẬP, và sản phẩm này đang ngược chiều nhau: những thao tác mạnh nhất đều
  được chấm nhưng KHÔNG mang mã, còn những thao tác yếu (trắc nghiệm) lại mang mã. Phải in cả
  hai trục ra, không được gộp thành một nhãn "PHỦ".

GIẢ ĐỊNH PHẢI NÓI RÕ: khi một site log dùng biến `q.yccd`, công cụ này coi MỌI mã khai trong tệp
dữ liệu của mô-đun đó là đi qua site ấy. Đúng khi mô-đun render cả danh sách item qua một callback
duy nhất (tinhhuong.js veTinhHuong, nhamay_tram01.js tram0, data/kienthuc.js quiz) — đã kiểm bằng
mắt trên ba tệp đó. Nếu sau này có mô-đun chỉ render một phần danh sách qua site có log, phép quy
này sẽ phóng đại; khi đó phải truy từng item.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.abspath(os.path.join(HERE, "..", ".."))

RE_MA = r"10\.[A-D]\d?\.(?:MR)?\d+"

# ---- loại thao tác THEO TỪNG LOG SITE (không theo trạm) ----
# khoá: (loai, suKien hoặc hàm bao ngoài). Giá trị: (nhãn, mức)
THAO_TAC = {
    ("tinhHuong", "traLoi"): ("chọn nhóm tính năng / vi phạm / yêu cầu cho tình huống", "nhan_dien"),
    ("nhamay", "tram0"): ("chọn đáp án trắc nghiệm về vị trí khâu trong hệ thống", "nhan_dien"),
    ("lab", "veQuiz"): ("chọn 1 trong 4 phương án quiz (đã xáo vị trí)", "nhan_dien"),
    ("lab", "veBaiTapPrompt"): ("GÕ prompt tự do vào ô nhập, chấm bằng rubric từ khoá", "tu_xuat"),
    ("dauTruong", "nop"): ("CHỈ ĐÚNG CHỖ SAI trong văn bản + đoán loại lỗi", "tu_xuat"),
    ("duDoan", "doiChieu"): ("DỰ ĐOÁN kết quả TRƯỚC khi chạy rồi ĐỐI CHIẾU với kết quả thật", "tu_xuat"),
    ("duDoan", "chot"): ("chốt dự đoán (chưa đối chiếu)", "tu_xuat"),
    ("lab3d", "taoDuLieu"): ("chỉnh slider tỉ lệ ảnh ngày / số ảnh rồi tạo bộ dữ liệu", "tu_xuat"),
    ("lab3d", "danhGia"): ("đánh giá mô hình trên bộ dữ liệu vừa chỉnh", "tu_xuat"),
    ("pipe3d", "doan"): ("đoán trạm nào hỏng trong ống dẫn AI", "nhan_dien"),
    ("nhamay", "ungDung"): ("gõ prompt cho máy n-gram rồi phán quyết 'có căn cứ' / 'bịa'", "tu_xuat"),
    ("nhamay", "phanQuyet"): ("phán quyết câu trả lời là có căn cứ hay bịa đặt", "nhan_dien"),
    ("nhamay", "tram1"): ("dán nhãn dữ liệu (chọn nhãn đúng/sai)", "nhan_dien"),
    ("kichBan", "xemCanh"): ("XEM cảnh hoạt hình, không chấm", "doc"),
    ("phien", ""): ("tổng kết phiên pre/post", "doc"),
}


def doc(p):
    return io.open(os.path.join(S, p), encoding="utf-8").read()


def cat_payload(s, i_call):
    """cắt đối số của logSuKien( ... ) bằng cân bằng ngoặc — regex thô không vượt được ngoặc lồng."""
    j = s.find("(", i_call)
    d = 0
    for k in range(j, len(s)):
        if s[k] == "(":
            d += 1
        elif s[k] == ")":
            d -= 1
            if d == 0:
                return s[j + 1:k], j
    return "", j


def than_ham(s, ten):
    """cắt thân hàm `function ten(...){...}` bằng CÂN BẰNG NGOẶC, không cắt theo số ký tự.

    VÌ SAO: bản đầu của công cụ này quét `window.MX_*` trong cửa sổ 6000 ký tự kể từ đầu hàm,
    nên một hàm nằm cạnh các hàm khác bị gom nhầm mô-đun của hàm bên cạnh. Đo được trên
    site app.js:1274 (nmKhoiDongTram0): hàm đó chỉ dùng MỘT mô-đun `const M = window.MX_NHAMAY01`
    và `q` đến từ `M.veCauHoiT0(...)`, nhưng công cụ in ra 'biến -> js/duDoan.js+js/nhamay_text.js
    +js/nhamay_tram01.js' và quy 6 mã thay vì 4. Hệ quả: 10.C2.MR2 được phán 'PHỦ MỘT PHẦN' qua
    site tram0 trong khi nhamay_tram01.js không hề chứa mã đó.
    """
    i = s.find("function " + ten + "(")
    if i < 0:
        return ""
    j = s.find("{", i)
    if j < 0:
        return ""
    d = 0
    for k in range(j, len(s)):
        if s[k] == "{":
            d += 1
        elif s[k] == "}":
            d -= 1
            if d == 0:
                return s[i:k + 1]
    return s[i:]


def ham_bao_ngoai(s, pos):
    head = s[:pos]
    m = list(re.finditer(r"function\s+(\w+)\s*\(", head))
    return m[-1].group(1) if m else "?"


def main():
    # ===== 1. sổ đăng ký mô-đun: window.MX_* -> tệp =====
    mx = {}
    for sub in ("js", "data"):
        d = os.path.join(S, sub)
        for f in sorted(os.listdir(d)):
            if not f.endswith(".js"):
                continue
            s = doc(sub + "/" + f)
            for m in re.finditer(r"window\.(MX_[A-Z0-9_]+)\s*=", s):
                mx.setdefault(m.group(1), sub + "/" + f)
    print("sổ mô-đun window.MX_*: " + str(len(mx)) + " -> "
          + ", ".join(k + "=" + v for k, v in sorted(mx.items())[:8]) + " ...")

    # ===== 2. quét mọi log call site =====
    sites = []
    for f in sorted(os.listdir(os.path.join(S, "js"))):
        if not f.endswith(".js"):
            continue
        s = doc("js/" + f)
        for m in re.finditer(r"logSuKien\s*\(", s):
            pay, _ = cat_payload(s, m.start())
            if not pay:
                continue
            ln = s[:m.start()].count("\n") + 1
            loai = (re.search(r'loai\s*:\s*"([^"]+)"', pay) or [None, ""])[1]
            sk = (re.search(r'suKien\s*:\s*"([^"]+)"', pay) or [None, ""])[1]
            ham = ham_bao_ngoai(s, m.start())
            co_diem = bool(re.search(r"\bdiem\s*:", pay))
            ym = re.search(r"yccd\s*:\s*([^,\n}]{1,80})", pay)
            yval = ym.group(1).strip() if ym else ""
            sites.append({"tep": "js/" + f, "dong": ln, "loai": loai, "suKien": sk,
                          "ham": ham, "co_diem": co_diem, "yccd_expr": yval,
                          "payload": pay})
    print("tổng số log call site: " + str(len(sites)))
    print("  site CÓ trường yccd : " + str(sum(1 for x in sites if x["yccd_expr"])))
    print("  site CÓ điểm        : " + str(sum(1 for x in sites if x["co_diem"])))
    print("  site CÓ cả hai      : " + str(sum(1 for x in sites
                                               if x["yccd_expr"] and x["co_diem"])))

    # ===== 3. truy vết mã YCCĐ cho từng site =====
    def ma_cua_site(st):
        """trả về (danh_sách_mã, nguồn_quy)"""
        v = st["yccd_expr"]
        if not v:
            return [], "KHÔNG có trường yccd"
        lit = re.findall(RE_MA, v)
        if lit:
            return sorted(set(lit)), "literal trong payload"
        # dạng BIẾN: truy ngược qua window.MX_* TRONG ĐÚNG THÂN HÀM bao ngoài, và chỉ nhận
        # mô-đun DỮ LIỆU ĐẦU TIÊN có khai `yccd:`. Hai luật này sửa đúng lỗi quy quá tay:
        #   · MX_ENGINE là mô-đun GHI LOG, không phải nguồn dữ liệu item — nó có `yccd` trong
        #     header CSV nên nếu nhận nó thì mọi site đều bị quy thêm 10.C4.1. Phải loại.
        #   · một trạm có thể tham chiếu vài mô-đun; chỉ mô-đun CẤP `q` (mô-đun dữ liệu đầu
        #     tiên có yccd theo thứ tự xuất hiện trong hàm) mới là nguồn mã thật.
        s = doc(st["tep"])
        vung = than_ham(s, st["ham"]) if st["ham"] != "?" else ""
        if not vung:
            # không cắt được thân hàm thì thu hẹp quanh site thay vì lấy 6000 ký tự
            i = s.find('suKien:"' + st["suKien"] + '"') if st["suKien"] else 0
            vung = s[max(0, i - 1500):i + 500] if i else s[:5000]
        refs = [r for r in re.findall(r"window\.(MX_[A-Z0-9_]+)", vung) if r != "MX_ENGINE"]
        for r in refs:
            tf = mx.get(r)
            if not tf:
                continue
            nd = doc(tf)
            if not re.search(r"yccd\s*:", nd):
                continue
            out = sorted(set(re.findall(RE_MA, nd)))
            if out:
                return out, "biến -> " + tf
        if refs:
            return [], ("biến nhưng các mô-đun trong hàm (" + ",".join(refs[:3])
                        + ") không khai yccd nào")
        # fallback: mọi mã trong chính tệp site
        nd = s
        out2 = sorted(set(re.findall(RE_MA, nd)))
        if out2:
            return out2, "biến -> chính tệp " + st["tep"] + " (KHÔNG truy được mô-đun)"
        return [], "biến nhưng KHÔNG truy ra mã nào"

    # ===== 4. dựng chuỗi bằng chứng theo từng mã =====
    sach = json.load(io.open(os.path.join(S, "data-source/yccd_lop10_sach.json"), encoding="utf-8"))
    if isinstance(sach, dict):
        sach = list(sach.values())
    YCCD = {}
    for it in sach:
        m = re.match(r"\s*(.+?được)", it["text"])
        YCCD[it["ma"]] = {"text": it["text"], "dongtu": (m.group(1).strip() if m else it["text"][:30]),
                          "loai": it.get("loai", "")}

    chuoi = {ma: [] for ma in YCCD}
    print("\n=== 4. CHUỖI BẰNG CHỨNG theo log site ===")
    for st in sites:
        ma_list, nguon = ma_cua_site(st)
        key = (st["loai"], st["suKien"])
        if key not in THAO_TAC:
            key = (st["loai"], st["ham"])
        nhan, muc = THAO_TAC.get(key, ("? (chưa phân loại)", "?"))
        print("  " + st["tep"] + ":" + str(st["dong"])
              + " loai=" + st["loai"] + " suKien=" + (st["suKien"] or "-")
              + " diem=" + ("CÓ" if st["co_diem"] else "KHÔNG")
              + " thao_tac=" + muc
              + " -> " + str(len(ma_list)) + " mã [" + nguon[:52] + "]")
        if not ma_list:
            continue
        for ma in ma_list:
            if ma in chuoi:
                chuoi[ma].append({
                    "site": st["tep"] + ":" + str(st["dong"]),
                    "loai_su_kien": st["loai"], "su_kien": st["suKien"] or st["ham"],
                    "thao_tac": nhan, "muc_thao_tac": muc,
                    "co_diem": st["co_diem"], "nguon_ma": nguon,
                })

    # ===== 5. thao tác MẠNH nhưng KHÔNG mang mã (trục B bị đứt) =====
    print("\n=== 5. THAO TÁC MẠNH ĐƯỢC CHẤM NHƯNG KHÔNG MANG MÃ YCCĐ ===")
    dut = []
    for st in sites:
        if st["yccd_expr"]:
            continue
        key = (st["loai"], st["suKien"])
        if key not in THAO_TAC:
            key = (st["loai"], st["ham"])
        nhan, muc = THAO_TAC.get(key, ("? (chưa phân loại)", "?"))
        if muc == "tu_xuat" and st["co_diem"]:
            dut.append((st["tep"] + ":" + str(st["dong"]), st["loai"], st["suKien"], nhan))
            print("  ✗ " + st["tep"] + ":" + str(st["dong"]) + " " + st["loai"] + "/"
                  + (st["suKien"] or st["ham"]) + " — " + nhan)
    if not dut:
        print("  (không có)")

    # ===== 6. phán quyết 2 trục =====
    print("\n" + "=" * 104)
    print("BẢNG v3 — HAI TRỤC ĐỘC LẬP: (A) loại thao tác · (B) mã có tới được CSV của giáo viên không")
    print("=" * 104)
    dem = {}
    dong = []
    for ma in sorted(YCCD):
        ds = chuoi[ma]
        dt = YCCD[ma]["dongtu"]
        co_diem = [x for x in ds if x["co_diem"]]
        tu_xuat = [x for x in co_diem if x["muc_thao_tac"] == "tu_xuat"]
        nhan_dien = [x for x in co_diem if x["muc_thao_tac"] == "nhan_dien"]
        if tu_xuat:
            pq = "A:PHỦ THẬT"
            ly = ("thao tác TỰ XUẤT RA được chấm và bản ghi CÓ mang mã: "
                  + ", ".join(sorted({x["site"] + " (" + x["thao_tac"][:34] + ")" for x in tu_xuat})))
        elif nhan_dien:
            pq = "B:PHỦ MỘT PHẦN"
            ly = ("chỉ đo ở mức NHẬN DIỆN (chọn 1 trong N) dù có chấm + mang mã: "
                  + ", ".join(sorted({x["site"] + " (" + x["thao_tac"][:34] + ")" for x in nhan_dien})))
            if re.match(r"^(Kể tên|Liệt kê|Mô tả|Trình bày|Nêu|Giải thích|Phân biệt)", dt):
                ly += " | động từ '" + dt + "' đòi TỰ NÊU nên đây là đo yếu hơn một bậc"
        elif co_diem:
            pq = "C:LOG KHÔNG ĐIỂM"
            ly = "có bản ghi mang mã nhưng không kèm điểm, nên không tính được đạt/không"
        elif ds:
            pq = "D:KHÔNG CHẤM"
            ly = "mã có đi theo bản ghi nhưng bản ghi không được chấm"
        else:
            # không có chuỗi nào: mã chỉ tồn tại ở data/comment/khai báo tĩnh
            pq = "E:ĐỨT CHUỖI"
            ly = ("KHÔNG có log call site nào mang mã này tới CSV. Mã chỉ xuất hiện trong dữ liệu/"
                  "khai báo tĩnh/comment, trong khi các thao tác mạnh của trạm tương ứng (xem mục 5) "
                  "lại được chấm mà không mang mã")
        dem[pq] = dem.get(pq, 0) + 1
        dong.append({"ma": ma, "loai": YCCD[ma]["loai"], "dongtu": dt, "text": YCCD[ma]["text"],
                     "phan_quyet": pq, "ly_do": ly,
                     "so_site": len(ds), "so_site_co_diem": len(co_diem),
                     "chuoi": ds})
        print("\n" + ma + "  [" + YCCD[ma]["loai"] + "]  động từ: " + dt)
        print("   chuỗi: " + str(len(ds)) + " site (" + str(len(co_diem)) + " có điểm)"
              + " · " + ", ".join(sorted({x["loai_su_kien"] + "/" + x["su_kien"] for x in ds}))[:88])
        print("   PHÁN QUYẾT: " + pq)
        print("   vì sao    : " + ly[:210])

    print("\n" + "=" * 104)
    print("TỔNG HỢP v3")
    print("=" * 104)
    for k in sorted(dem):
        print("  " + k.ljust(20) + ": " + str(dem[k]) + "/22")
    for k in sorted(dem):
        d = [x["ma"] for x in dong if x["phan_quyet"] == k]
        print("    " + k + ": " + ", ".join(d))

    print("\n=== SO SÁNH với bản v2 đã công bố (để thấy instrument cũ sai ở đâu) ===")
    try:
        v2 = json.load(io.open(os.path.join(S, "data-source/bang_gia_tri_kien_tao.json"),
                               encoding="utf-8"))
        v2map = {x["ma"]: x["phan_quyet"] for x in v2["bang"]}
        doi = 0
        for x in dong:
            cu = v2map.get(x["ma"], "?")
            if (cu == "PHỦ THẬT") != x["phan_quyet"].startswith("A:"):
                doi += 1
                print("  " + x["ma"] + ": v2='" + cu + "'  ->  v3='" + x["phan_quyet"] + "'")
        print("  tổng số mã ĐỔI nhãn: " + str(doi) + "/22")
    except Exception as e:
        print("  không so được: " + repr(e))

    out = os.path.join(S, "data-source", "bang_gia_tri_kien_tao_v3.json")
    io.open(out, "w", encoding="utf-8").write(json.dumps(
        {"ngay": "2026-10-11",
         "cong_cu": "tools/tests/bang_gia_tri_kien_tao_v3.py",
         "vi_sao_co_ban_nay": "v1/v2 quét regex literal nên bỏ sót `yccd: q.yccd` (dạng biến) và "
                              "gán loại thao tác theo TRẠM thay vì theo log site. Ba reviewer độc "
                              "lập bắt được cả hai lỗi. Bản này lấy LOG CALL SITE làm đơn vị bằng "
                              "chứng và truy ngược biến qua sổ window.MX_*.",
         "hai_truc": "A = loại thao tác (tự xuất / nhận diện / chỉ đọc). "
                     "B = mã có đi theo bản ghi được chấm tới CSV của giáo viên không. "
                     "Hai trục độc lập; sản phẩm này đang ngược chiều: thao tác mạnh nhất đều "
                     "được chấm nhưng KHÔNG mang mã, thao tác trắc nghiệm lại mang mã.",
         "gia_dinh": "site log dùng biến q.yccd thì mọi mã khai trong tệp dữ liệu của mô-đun đó "
                     "được coi là đi qua site ấy. Đúng với 3 mô-đun đã kiểm bằng mắt "
                     "(tinhhuong.js, nhamay_tram01.js, data/kienthuc.js) vì chúng render cả danh "
                     "sách qua một callback duy nhất.",
         "thao_tac_manh_khong_mang_ma": dut,
         "tong_hop": dem, "bang": dong},
        ensure_ascii=False, indent=2))
    print("\nĐã ghi: " + os.path.relpath(out, S))
    return 0


if __name__ == "__main__":
    sys.exit(main())
