#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BẢNG GIÁ TRỊ KIẾN TẠO (construct validity) cho 22 YCCĐ lớp 10.

HAI VẾ ANH VĂN ĐẶT, phải trả lời tách bạch:
  (1) THAO TÁC thực thi có CHỨNG MINH ĐƯỢC yêu cầu cần đạt không?
  (2) MỤC ĐÍCH đó có PHÙ HỢP không?

Vế (1) chấm bằng bằng chứng lấy TỪ MÃ: mỗi YCCĐ gom thành danh sách bằng chứng
(trạm, loại thao tác, có được chấm + ghi nhật ký không), rồi đối chiếu với ĐỘNG TỪ của YCCĐ
trong nguyên văn Khung 2422 (đã verify 22/22 bởi tools/verify_yccd.py).

VÌ SAO CÓ BẢN NÀY. Bản đầu của công cụ này lưu claim dưới dạng CHUỖI "(log bt13.js)" rồi so
với tập tên trạm "v-*". Chuỗi không bao giờ khớp tên trạm, nên ba phán quyết sai: 10.C4.MR1
bị kết luận "CHƯA RÕ/không xếp được" dù nó có nhật ký chấm điểm thật trong nhamay_tram01.js;
10.C2.3 bị kết luận "PHỦ DANH NGHĨA" dù bt13.js có ghi log cho nó. Một công cụ kêu oan thì
người đọc bỏ qua luôn phần đúng của nó, nên bản này lưu bằng chứng CÓ CẤU TRÚC thay vì chuỗi.

THANG PHÁN QUYẾT
  · PHỦ THẬT       — có thao tác bắt học sinh TỰ XUẤT RA (gõ prompt, chỉ đúng chỗ sai, chỉnh
                     tham số rồi đối chiếu dự đoán với kết quả thật) và thao tác đó được chấm,
                     được ghi nhật ký theo YCCĐ.
  · PHỦ MỘT PHẦN   — có thao tác được chấm nhưng chỉ ở mức NHẬN DIỆN (chọn 1 trong N) trong khi
                     động từ đòi TỰ NÊU (kể tên, liệt kê, mô tả, phân biệt). Đo được, nhưng yếu
                     hơn động từ — phải nói rõ trong hồ sơ, không được đánh đồng.
  · PHỦ DANH NGHĨA — mã YCCĐ có xuất hiện, nhưng nơi xuất hiện chỉ HIỆN NỘI DUNG ĐỂ ĐỌC:
                     0 nút, 0 ô nhập, 0 sự kiện, không có gì được chấm hay ghi nhật ký.
  · CHƯA PHỦ       — không tìm thấy bằng chứng nào trong mã.

GIỚI HẠN PHẢI NÓI: phân bậc động từ là SUY TỪ CHỮ trong Khung 2422, KHÔNG phải thang Bloom do
Bộ công bố (Khung không kèm thang đó). Nó dùng để đặt câu hỏi đúng, không phải căn cứ pháp lý.
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.abspath(os.path.join(HERE, "..", ".."))
R = os.path.dirname(S)


def doc(p):
    return io.open(os.path.join(S, p), encoding="utf-8").read()


RE_MA = r"10\.[A-D]\d?\.(?:MR)?\d+"

# ---------- tệp JS -> trạm (view) mà nó phục vụ ----------
# muc3.js phục vụ cả hai trạm: BT-06/07/08 ở Nhà máy, BT-10/12 ở Tình huống.
FILE_TRAM = {
    "kienthuc.js": ["v-kienthuc"],
    "bt13.js": ["v-kienthuc"],
    "tinhhuong.js": ["v-tinhhuong"],
    "nhamay_tram01.js": ["v-nhamay"],
    "nhamay_text.js": ["v-nhamay"],
    "pipeline3d.js": ["v-pipe3d"],
    "lab3d.js": ["v-lab3d"],
    "lab.js": ["v-lab"],
    "duDoan.js": ["v-lab3d", "v-nhamay"],
    "muc3.js": ["v-nhamay", "v-tinhhuong"],
    "logic.js": ["v-logic"],
    "kichban.js": ["v-kichban"],
}

# ---------- loại thao tác mỗi trạm, đo từ mã (probe đã xác nhận) ----------
THAO_TAC = {
    "v-home": ("điều hướng", "doc"),
    "v-nhap": ("KHÔNG CÓ NỘI DUNG — <section> rỗng, không có hien('v-nhap') trong app.js", "doc"),
    "v-lab": ("chọn phương án có sẵn (đối chiếu nhãn, học máy giám sát)", "nhan_dien"),
    "v-dautruong": ("CHỈ ĐÚNG CHỖ SAI trong văn bản (claimDung) + đoán loại lỗi", "tu_xuat"),
    "v-baocao": ("xem báo cáo cá nhân", "doc"),
    "v-logic": ("chọn phương án (lôgic)", "nhan_dien"),
    "v-kienthuc": ("hỗn hợp: 4 khối chỉ đọc + 1 ô GÕ prompt + quiz chọn", "hon_hop"),
    "v-lab3d": ("CHỈNH slider (tỉ lệ ảnh ngày / số ảnh) -> DỰ ĐOÁN TRƯỚC -> ĐỐI CHIẾU kết quả thật",
                "tu_xuat"),
    "v-pipe3d": ("ĐOÁN trạm hỏng trong ống dẫn AI", "nhan_dien"),
    "v-nhamay": ("GÕ prompt tự do (n-gram chạy thật trong máy) + PHÁN QUYẾT 'có căn cứ'/'bịa'",
                 "tu_xuat"),
    "v-tinhhuong": ("chọn nhóm tính năng / vi phạm / yêu cầu cho từng tình huống (nút dựng động)",
                    "nhan_dien"),
    "v-kichban": ("XEM cảnh hoạt hình (1 nút 'tiếp'), không chấm", "doc"),
    "v-gioithieu": ("đọc giới thiệu sản phẩm", "doc"),
}

# khối CHỈ ĐỌC bên trong v-kienthuc (đo bằng probe: 0 nút, 0 ô nhập, 0 sự kiện)
KHOI_CHI_DOC = {
    "veLuat": ["10.A3.1"],
    "veUngDung": ["10.C2.2"],
    "veSoSanh": ["10.C3.3"],
    "veTieuChiPrompt": ["10.C3.1"],
}
# khối CÓ THAO TÁC bên trong v-kienthuc
KHOI_THAO_TAC = {
    "veBaiTapPrompt": (["10.C3.2"], "tu_xuat", "ô nhập -> học sinh tự gõ prompt, chamPrompt chấm"),
    "veQuiz": ([], "nhan_dien", "chọn 1 trong N phương án, có xáo vị trí"),
}

DOI_TU_NEU = re.compile(r"^(Kể tên|Liệt kê|Mô tả|Trình bày|Nêu|Giải thích|Phân biệt)", re.I)
DOI_TAO_TAC = re.compile(r"^(Thực hành|Sử dụng|Phân tích|Xác định|Nhận biết)", re.I)


def main():
    # ===== 1. 22 YCCĐ + động từ =====
    sach = json.load(io.open(os.path.join(S, "data-source/yccd_lop10_sach.json"), encoding="utf-8"))
    if isinstance(sach, dict):
        sach = list(sach.values())
    YCCD = {}
    for it in sach:
        ma, txt = it["ma"], it["text"]
        m = re.match(r"\s*(.+?được)", txt)
        YCCD[ma] = {"text": txt, "dongtu": (m.group(1).strip() if m else txt[:30]),
                    "loai": it.get("loai", ""), "chuDe": it.get("chuDe", "")}
    print("đã nạp " + str(len(YCCD)) + " YCCĐ từ data-source/yccd_lop10_sach.json")

    # ===== 2. bằng chứng CÓ CẤU TRÚC: ma -> [ {tram, nguon, thao_tac, muc, co_cham_log} ] =====
    bc = {ma: [] for ma in YCCD}
    idx, app = doc("index.html"), doc("js/app.js")

    # 2a. mã YCCĐ nhúng trong HTML từng <section id="v-*">
    pos = [(m.start(), m.group(1)) for m in re.finditer(r'<section[^>]*id="(v-[^"]+)"', idx)]
    for k, (i, vid) in enumerate(pos):
        j = pos[k + 1][0] if k + 1 < len(pos) else len(idx)
        for ma in set(re.findall(RE_MA, idx[i:j])):
            if ma in bc:
                bc[ma].append({"tram": vid, "nguon": "index.html (HTML tĩnh)",
                               "thao_tac": THAO_TAC.get(vid, ("?", "doc"))[0],
                               "muc": THAO_TAC.get(vid, ("?", "doc"))[1], "co_cham_log": False})

    # 2b. nhật ký CÓ chấm điểm trong các tệp JS — bằng chứng mạnh nhất
    for f, trams in FILE_TRAM.items():
        try:
            s = doc("js/" + f)
        except Exception:
            continue
        for m in re.finditer(r'yccd\s*:\s*"([^"]+)"', s):
            nganh = re.sub(r"\s+", " ", s[max(0, m.start() - 520):m.end() + 260])
            co_cham = bool(re.search(r"\bdiem\s*:|\bdung\s*:", nganh))
            is_log = "logSuKien" in nganh or "ghiLog" in nganh
            for ma in set(re.findall(RE_MA, m.group(1))):
                if ma not in bc:
                    continue
                for vid in trams:
                    muc = THAO_TAC.get(vid, ("?", "doc"))[1]
                    # v-kienthuc là trạm hỗn hợp: mức thật phụ thuộc khối nào mang mã này
                    if vid == "v-kienthuc":
                        if ma == "10.C3.2":
                            muc = "tu_xuat"
                        elif any(ma in ds for ds in KHOI_CHI_DOC.values()):
                            muc = "doc"
                        else:
                            muc = "nhan_dien"
                    bc[ma].append({
                        "tram": vid,
                        "nguon": "js/" + f + (" (logSuKien CÓ chấm điểm)" if (co_cham and is_log)
                                              else " (ánh xạ trong mã)"),
                        "thao_tac": THAO_TAC.get(vid, ("?", "doc"))[0],
                        "muc": muc,
                        "co_cham_log": bool(co_cham and is_log),
                    })

    # 2c. quiz trong data/kienthuc.js: câu nào gắn YCCĐ nào (thao tác chọn, có chấm)
    dk = doc("data/kienthuc.js")
    i = dk.find("quiz:")
    quiz_seg = dk[i:]
    # Mỗi câu quiz là object có ngoặc LỒNG (luaChon:[{...},{...}]) nên KHÔNG cắt được bằng
    # \{[^{}]*\}. Bản đầu cắt vậy và ra RỖNG, kéo theo 10.A3.1/10.C2.2 bị kết luận 'CHƯA RÕ'
    # oan — cùng lớp lỗi 'rule out your own script' đã gặp nhiều lần. Lấy thẳng từng yccd trong
    # vùng quiz rồi ghép cauHoi kế sau nó (trong object, yccd đứng trước cauHoi).
    quiz_yccd = {}
    for m in re.finditer(r'yccd\s*:\s*"([^"]*)"', quiz_seg):
        q = re.search(r'cauHoi\s*:\s*"([^"]{8,160})', quiz_seg[m.end():m.end() + 400])
        for ma in re.findall(RE_MA, m.group(1)):
            quiz_yccd.setdefault(ma, []).append(q.group(1) if q else "?")
    print("quiz gắn YCCĐ: " + ", ".join(sorted(quiz_yccd)))
    for ma, cau in quiz_yccd.items():
        if ma in bc:
            bc[ma].append({"tram": "v-kienthuc", "nguon": "data/kienthuc.js quiz ("
                           + str(len(cau)) + " câu, có chấm)",
                           "thao_tac": "chọn 1 trong N phương án (đã xáo vị trí)",
                           "muc": "nhan_dien", "co_cham_log": True})

    # 2d. GIẢI MỨC cho v-kienthuc. Trạm này là HỖN HỢP: 4 khối chỉ đọc, 1 ô gõ prompt, 1 quiz.
    # Quét HTML chỉ biết "hon_hop" nên không phán quyết được; phải giải theo TỪNG YCCĐ, và phải
    # làm SAU bước 2c vì cần biết quiz phủ mã nào. Bản đầu để nguyên 'hon_hop' chảy vào phán
    # quyết -> 10.A3.1 và 10.C2.2 ra 'CHƯA RÕ / không xếp được' dù cả hai CÓ câu quiz được chấm.
    for ma in bc:
        for b in bc[ma]:
            if b["muc"] != "hon_hop" or b["tram"] != "v-kienthuc":
                continue
            if ma == "10.C3.2":
                b["muc"] = "tu_xuat"
                b["thao_tac"] = "GÕ prompt vào ô nhập (veBaiTapPrompt), chamPrompt chấm rồi log"
                b["co_cham_log"] = True
                b["nguon"] = "js/kienthuc.js veBaiTapPrompt (ô nhập + chấm)"
            elif ma in quiz_yccd:
                b["muc"] = "nhan_dien"
                b["thao_tac"] = "chọn 1 trong 4 phương án của câu quiz (đã xáo vị trí)"
                b["co_cham_log"] = True
                b["nguon"] = "data/kienthuc.js quiz (" + str(len(quiz_yccd[ma])) + " câu, có chấm)"
            else:
                b["muc"] = "doc"
                khoi = [fn for fn, ds in KHOI_CHI_DOC.items() if ma in ds]
                b["thao_tac"] = ("chỉ HIỆN nội dung để đọc (" + ", ".join(khoi) + ")")
                b["co_cham_log"] = False

    # 2e. KHAI BÁO TĨNH trong app.js: bảng NM_TRAM ánh xạ view->yccd. Đây là app TỰ NÓI
    # "trạm này phủ mã đó" — một lời KHAI, KHÔNG phải một phép ĐO. Bản đầu của công cụ bỏ sót
    # app.js (không nằm trong FILE_TRAM) nên 10.C2.MR2 bị kết luận 'CHƯA PHỦ' oan: nó ĐƯỢC khai
    # báo tĩnh ở v-lab3d/v-pipe3d nhưng không có thao tác nào được chấm theo mã. Phải tách
    # 'chưa được khai báo' khỏi 'được khai báo mà không đo' — đúng câu hỏi anh Văn đặt.
    app_static = 0
    for mau in (r'\{[^{}]*?view\s*:\s*"(v-[^"]+)"[^{}]*?yccd\s*:\s*"([^"]+)"[^{}]*\}',
                r'\{[^{}]*?yccd\s*:\s*"([^"]+)"[^{}]*?view\s*:\s*"(v-[^"]+)"[^{}]*\}'):
        for m in re.finditer(mau, app):
            a, b_ = m.group(1), m.group(2)
            vid, ystr = (a, b_) if a.startswith("v-") else (b_, a)
            for ma in set(re.findall(RE_MA, ystr)):
                if ma in bc and not any(x["muc"] == "claim_tinh" and x["tram"] == vid for x in bc[ma]):
                    bc[ma].append({"tram": vid, "nguon": "app.js bảng view→yccd (khai báo tĩnh)",
                                   "thao_tac": "KHAI BÁO TĨNH — không phải thao tác được chấm",
                                   "muc": "claim_tinh", "co_cham_log": False})
                    app_static += 1
    print("khai báo tĩnh app.js bắt được: " + str(app_static) + " cặp view→yccd")

    # 2f. MÃ NHẮC TRONG COMMENT / tài liệu trong tệp trạm. Loại bằng chứng này YẾU HƠN khai báo
    # tĩnh: nó nói "trạm này nhằm vào mã đó" nhưng không có đường nào đưa mã vào nhật ký.
    # Bản đầu của công cụ bỏ sót nó vì bước 2b chỉ quét trường `yccd:"..."`. Hệ quả: 10.C2.MR2
    # bị phán 'CHƯA PHỦ' oan dù mã có trong comment của js/nhamay_text.js và trạm đó CÓ thao tác
    # được log (app.js:1510 suKien:"ungDung", prompt). Đó là âm tính giả của chính công cụ đo,
    # cùng lớp lỗi 'rule out your own script' đã gặp nhiều lần ở dự án này.
    nhac = 0
    for f, trams in FILE_TRAM.items():
        try:
            s2 = doc("js/" + f)
        except Exception:
            continue
        for m in re.finditer(RE_MA, s2):
            ma = m.group(0)
            if ma not in bc:
                continue
            truoc = s2[max(0, m.start() - 90):m.start()]
            if re.search(r'yccd\s*:\s*"?$', truoc):
                continue  # đã bắt ở bước 2b (ánh xạ thật)
            for vid in trams:
                if any(x["muc"] == "nhac_comment" and x["tram"] == vid for x in bc[ma]):
                    continue
                ln = s2[:m.start()].count("\n") + 1
                bc[ma].append({
                    "tram": vid,
                    "nguon": "js/" + f + ":" + str(ln) + " (nhắc trong comment/chú giải)",
                    "thao_tac": THAO_TAC.get(vid, ("?", "doc"))[0],
                    "muc": "nhac_comment",
                    "co_cham_log": False,
                })
                nhac += 1
    print("mã nhắc trong comment tệp trạm: " + str(nhac) + " cặp")

    # ===== 3. phán quyết =====
    def phan_quyet(ma):
        ds = bc[ma]
        if not ds:
            return "CHƯA PHỦ", "không tìm thấy mã này ở bất kỳ tệp mã nguồn / dữ liệu / nhật ký nào", []
        that = [b for b in ds if b["muc"] == "tu_xuat"]
        nd = [b for b in ds if b["muc"] == "nhan_dien"]
        doc_ = [b for b in ds if b["muc"] == "doc"]
        claim_tinh = [b for b in ds if b["muc"] == "claim_tinh"]
        nhac_comment = [b for b in ds if b["muc"] == "nhac_comment"]
        dt = YCCD[ma]["dongtu"]
        # ưu tiên bằng chứng CÓ chấm + log
        that_cham = [b for b in that if b["co_cham_log"]]
        nd_cham = [b for b in nd if b["co_cham_log"]]
        if that:
            k = "PHỦ THẬT"
            l = "có thao tác TỰ XUẤT RA: " + ", ".join(sorted({b["tram"] for b in that}))
            if that_cham:
                l += " (được chấm + ghi nhật ký theo YCCĐ: " + \
                     ", ".join(sorted({b["nguon"] for b in that_cham}))[:150] + ")"
            else:
                l += " — LƯU Ý: chưa thấy nhật ký chấm điểm gắn mã này, nên chưa quy được về từng học sinh"
            if not DOI_TAO_TAC.match(dt):
                l += " | động từ '" + dt + "' chỉ đòi nêu/giải thích nên thao tác này là đủ mạnh"
            else:
                l += " | khớp động từ '" + dt + "'"
            return k, l, ds
        if nd:
            k = "PHỦ MỘT PHẦN"
            l = "chỉ đo ở mức NHẬN DIỆN (chọn 1 trong N có sẵn): " + \
                ", ".join(sorted({b["tram"] for b in nd}))
            if nd_cham:
                l += " (có chấm + log)"
            if DOI_TU_NEU.match(dt):
                l += " | động từ '" + dt + "' đòi học sinh TỰ NÊU, chọn phương án yếu hơn một bậc"
            return k, l, ds
        if doc_:
            return ("PHỦ DANH NGHĨA",
                    "chỉ có nơi HIỆN NỘI DUNG ĐỂ ĐỌC (0 nút / 0 ô nhập / 0 sự kiện, không chấm, "
                    "không ghi nhật ký): " + ", ".join(sorted({b["tram"] for b in doc_})) +
                    " · nguồn: " + ", ".join(sorted({b["nguon"] for b in doc_}))[:120], ds)
        if nhac_comment:
            tram_co_thao_tac = [b["tram"] for b in nhac_comment
                                if THAO_TAC.get(b["tram"], ("", "doc"))[1] == "tu_xuat"]
            if tram_co_thao_tac:
                return ("PHỦ MỘT PHẦN",
                        "trạm CÓ thao tác tự xuất ra và CÓ ghi nhật ký, nhưng mã YCCĐ chỉ được nhắc "
                        "trong comment, không đi theo bản ghi nào: " + ", ".join(sorted(set(tram_co_thao_tac))) +
                        " — nên giáo viên không quy được kết quả đó về mã này cho từng học sinh", ds)
            return ("PHỦ DANH NGHĨA",
                    "mã chỉ được NHẮC trong comment/chú giải của tệp trạm, trạm đó không có thao tác "
                    "nào được chấm: " + ", ".join(sorted({b["tram"] for b in nhac_comment})) +
                    " — nguồn: " + ", ".join(sorted({b["nguon"] for b in nhac_comment}))[:120], ds)
        if claim_tinh:
            return ("PHỦ DANH NGHĨA",
                    "chỉ có KHAI BÁO TĨNH trong app.js (bảng view→yccd nói trạm này phủ mã đó) "
                    "mà KHÔNG có thao tác nào được chấm hay ghi nhật ký theo mã: " +
                    ", ".join(sorted({b["tram"] for b in claim_tinh})) +
                    " — đúng khoảng cách giữa 'có nhắc tới' và 'đo được'", ds)
        return "CHƯA RÕ", "không xếp được loại thao tác", ds

    print("\n" + "=" * 100)
    print("BẢNG GIÁ TRỊ KIẾN TẠO — 22 YCCĐ LỚP 10 (Khung 2422/QĐ-BGDĐT, bản đã verify 22/22)")
    print("=" * 100)
    dem, dong = {}, []
    for ma in sorted(YCCD):
        tt = YCCD[ma]
        ket, ly, ds = phan_quyet(ma)
        dem[ket] = dem.get(ket, 0) + 1
        dong.append({"ma": ma, "loai": tt["loai"], "dongtu": tt["dongtu"], "text": tt["text"],
                     "phan_quyet": ket, "ly_do": ly,
                     "bang_chung": [{"tram": b["tram"], "muc": b["muc"],
                                    "co_cham_log": b["co_cham_log"], "nguon": b["nguon"]}
                                   for b in ds]})
        print("\n" + ma + "  [" + tt["loai"] + "]  động từ: " + tt["dongtu"])
        print("   bằng chứng (" + str(len(ds)) + "): " + "; ".join(
            sorted({b["tram"] + "/" + b["muc"] + ("/có-log" if b["co_cham_log"] else "")
                    for b in ds})) or "   bằng chứng: —")
        print("   PHÁN QUYẾT: " + ket)
        print("   vì sao    : " + ly)

    print("\n" + "=" * 100)
    print("TỔNG HỢP")
    print("=" * 100)
    for k in ("PHỦ THẬT", "PHỦ MỘT PHẦN", "PHỦ DANH NGHĨA", "CHƯA PHỦ", "CHƯA RÕ"):
        if k in dem:
            print("  " + k.ljust(18) + ": " + str(dem[k]) + "/22")
    for k in ("PHỦ DANH NGHĨA", "CHƯA PHỦ", "CHƯA RÕ", "PHỦ MỘT PHẦN"):
        d = [x["ma"] for x in dong if x["phan_quyet"] == k]
        if d:
            print("    " + k + " (" + str(len(d)) + "): " + ", ".join(d))

    # ===== 4. ghi bằng chứng =====
    os.makedirs(os.path.join(S, "data-source"), exist_ok=True)
    out = os.path.join(S, "data-source", "bang_gia_tri_kien_tao.json")
    io.open(out, "w", encoding="utf-8").write(json.dumps(
        {"ngay": "2026-10-11",
         "cong_cu": "tools/tests/bang_gia_tri_kien_tao.py (chạy lại được, không gõ tay)",
         "nguon_yccd": "data-source/yccd_lop10_sach.json — tools/verify_yccd.py xác nhận 22/22 "
                       "câu khớp nguyên văn Khung 2422",
         "gioi_han": "Phân bậc động từ SUY TỪ CHỮ trong Khung 2422, không phải thang Bloom do Bộ "
                     "công bố (Khung không kèm thang). 'PHỦ MỘT PHẦN' nghĩa là đo được nhưng ở mức "
                     "nhận diện, yếu hơn động từ đòi TỰ NÊU — hồ sơ phải nói rõ, không đánh đồng "
                     "với PHỦ THẬT.",
         "tong_hop": dem, "bang": dong},
        ensure_ascii=False, indent=2))
    print("\nĐã ghi: " + os.path.relpath(out, R))
    return 0


if __name__ == "__main__":
    sys.exit(main())
