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
    # Hai site gọi qua wrapper ghiLog — bản quét đầu bỏ sót cả hai.
    # bt09 (BT-09 Mức 3): học sinh VIẾT một câu trả lời AI đủ dài (>= 20 kí tự, có kiểm tra ở
    # bt09.js:286) rồi tự cài lỗi cho bạn cùng lớp bắt, kiemCau(text, chon) chấm theo số dấu
    # hiệu. Đây là thao tác TỰ XUẤT có chấm, và nó mang yccd:"10.B2.1" lồng trong nhiemVu.
    ("lab", "hienGoiY"): ("VIẾT câu trả lời AI có cài lỗi cho bạn bắt (tự do, >=20 kí tự)", "tu_xuat"),
    # bt13 (BT-13 Mức 2): chọn nhóm + nối khớp đầu vào/đầu ra của tình huống -> nhận diện.
    ("lab", "veTinhHuong"): ("chọn nhóm và nối khớp đầu vào/đầu ra của tình huống", "nhan_dien"),
    # SÁU SITE dưới đây được phân loại SAU KHI ĐỌC MÃ THẬT (app.js các dòng 203/267/287/326/
    # 586/1064), không suy từ tên hàm. Ba site trong đó là những thao tác quan trọng nhất của
    # sản phẩm mà bản quét đầu để thành '?' — một dấu hỏi im lặng trong bảng bằng chứng thì
    # tệ hơn một nhãn sai, vì không ai biết mà hỏi lại.
    #   · app.js:203 là KÊNH GHI CHUNG của các ô Mức 3: `M3().ghiLog((ma,giaTri,suKien,kqBoSung)
    #     => ENG.logSuKien(...))`. Nó không có suKien literal (suKien là tham số) nên khoá tra
    #     rơi về tên hàm bao ngoài là dangNhap. Học sinh tự đưa ra một con số dự đoán rồi đối
    #     chiếu với kết quả thật -> mức tu_xuat.
    ("duDoan", "dangNhap"): ("CHỐT DỰ ĐOÁN rồi ĐỐI CHIẾU với kết quả thật (kênh ghi chung "
                             "của các ô Mức 3)", "tu_xuat"),
    #   · app.js:267/287: học sinh bấm nút để CHẠY huấn luyện, con số ghi lại là độ chính xác
    #     do hệ thống tính. Đây không phải chọn phương án cũng không phải tạo ra sản phẩm ngôn
    #     ngữ của học sinh, nên nó là mức RIÊNG: van_hanh. Gộp nó vào nhan_dien sẽ nói sai bản
    #     chất, gộp vào tu_xuat sẽ phóng đại.
    ("huanLuyen", "labHuanLuyen"): ("bấm HUẤN LUYỆN trên bộ dữ liệu LỆCH (92% ảnh ban ngày), "
                                    "hệ thống in độ chính xác train/ngày/đêm", "van_hanh"),
    ("huanLuyen", "labSoSanh"): ("bấm CÂN BẰNG dữ liệu rồi huấn luyện lại, so độ chính xác "
                                 "với lần lệch", "van_hanh"),
    ("lab", "labCauHoi"): ("chọn đáp án cho câu hỏi nhiệm vụ của xưởng huấn luyện", "nhan_dien"),
    #   · app.js:586 = THAO TÁC MẠNH NHẤT của sản phẩm: phán quyết câu có lỗi hay không, rồi
    #     CHỈ VÀO ĐÚNG CHỖ SAI trong văn bản (claimDung). Payload là `{loai:"dauTruong", kq}`
    #     nên co_diem phải dò qua biến (xem diem_co_that), và site này KHÔNG mang yccd.
    ("dauTruong", "dtNop"): ("phán quyết có lỗi/không + CHỈ ĐÚNG CHỖ SAI trong văn bản "
                             "(claimDung)", "tu_xuat"),
    ("pipe3d", "batDauLuot"): ("bắt đầu một lượt đoán trạm hỏng — đánh dấu phiên, không chấm",
                               "doc"),
    # NĂM SITE cuối, phân loại sau khi đọc mã thật ngày 11/10:
    #   · app.js:1308 hàm nmT0TaoLai(): bấm tạo lại bộ dữ liệu theo slider số ảnh + tỉ lệ ngày,
    #     log ghi soAnh/tiLeNgay. Cùng bản chất với hai site huanLuyen -> van_hanh.
    ("nhamay", "tram0TaoDuLieu"): ("bấm TẠO LẠI bộ dữ liệu theo slider (số ảnh, tỉ lệ ảnh ngày)",
                                   "van_hanh"),
    #   · bt09.js:309 và bt13.js:204 là NHÁNH ELSE của cùng một khối if: lần làm đầu tiên được
    #     ghi có điểm (bt09:301 mang 10.B2.1, bt13:196 mang 10.C2.3), các lần sau ghi là
    #     'luyenTap' và CỐ Ý không mang điểm — comment bt13.js:191 nói rõ lý do: "để tỉ lệ đúng
    #     không bị thổi lên sau khi học sinh đã thấy đáp án". Đây là thiết kế đúng, không phải
    #     chỗ đứt, nên nó có mức riêng thay vì bị gộp vào nhan_dien.
    ("bt09", "luyenTap"): ("làm LẠI bài BT-09 sau lần đầu (cố ý không tính điểm, chống thổi "
                           "tỉ lệ sau khi đã thấy đáp án)", "luyen_tap"),
    ("bt13", "luyenTap"): ("làm LẠI bài BT-13 sau lần đầu (cố ý không tính điểm)", "luyen_tap"),
    #   · bt13.js:359 là chỗ DUY NHẤT học sinh viết tự do mà máy KHÔNG chấm: gõ tên ứng dụng
    #     (>= 3 kí tự), chọn một nhóm, giải thích (>= 10 kí tự); giao diện in rõ "Thầy/cô sẽ đọc
    #     và nhận xét — bài này không chấm đúng/sai". Nó là mức riêng: tự xuất nhưng do GIÁO
    #     VIÊN chấm, không phải máy chấm. Gộp nó vào tu_xuat sẽ làm bảng nói dối rằng sản phẩm
    #     tự chấm được việc này.
    ("bt13", "muc3"): ("VIẾT tên ứng dụng + chọn nhóm + giải thích tự do (>= 10 kí tự); máy "
                       "KHÔNG chấm, giáo viên đọc và nhận xét", "tu_xuat_gv"),
    #   · logic.js:195 trong veBaiTap(): chọn đáp án cho bài tập lôgic, có chấm đúng/sai.
    ("lab", "veBaiTap"): ("chọn đáp án bài tập lôgic (có chấm đúng/sai)", "nhan_dien"),
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


def xoa_comment(s):
    """thay nội dung comment bằng khoảng trắng CÙNG ĐỘ DÀI để giữ nguyên offset và số dòng.

    Vì sao không xoá hẳn: mọi phép tính số dòng trong công cụ này đều dựa vào
    `s[:pos].count("\\n")`. Xoá comment sẽ xê dịch toàn bộ số dòng phía sau, và báo cáo sẽ
    trỏ sai dòng — một bằng chứng trỏ sai dòng thì không kiểm chứng lại được.
    """
    out = []
    i, n = 0, len(s)
    while i < n:
        c = s[i]
        if c == "/" and i + 1 < n and s[i + 1] == "*":
            j = s.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out.append(re.sub(r"[^\n]", " ", s[i:j]))
            i = j
        elif c == "/" and i + 1 < n and s[i + 1] == "/":
            j = s.find("\n", i)
            j = n if j < 0 else j
            out.append(" " * (j - i))
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out)


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


def cat_obj_arg(s, i_call):
    """trả về tham số là OBJECT LITERAL của lời gọi tại i_call, hoặc "" nếu không có.

    VÌ SAO HÀM NÀY TỒN TẠI — và vì sao bộ lọc trước nó là một lỗi nghiêm trọng.
    Lời gọi thật trong app có dạng `ENG.logSuKien(maHS, {loai:…, kq:{…}})`: THAM SỐ THỨ NHẤT
    LÀ maHS, object sự kiện là tham số THỨ HAI. Bộ lọc đầu tiên đòi `payload.lstrip()` bắt đầu
    bằng `{`, tức đòi object ở ngay tham số thứ nhất, nên nó loại SẠCH 100% site thật và công cụ
    in ra "tổng số log call site: 0" rồi phán "E:ĐỨT CHUỖI 22/22" — một kết quả trông như phát
    hiện nghiêm trọng nhưng thật ra là bộ lọc hỏng. Tệ hơn, nó vẫn ghi JSON, mà khối [15] của
    tools/thu_thap_so_lieu.py đọc đúng tệp đó rồi đưa số vào slide nộp.

    Cách làm đúng: cắt đối số ở DẤU PHẨY BẬC 0 (bỏ qua phẩy nằm trong ngoặc hoặc trong object
    lồng), rồi chọn phần nào bắt đầu bằng `{`. Quy tắc này vẫn loại được ba thứ cần loại:
      · forwarder    `logSuKien(maHS, sk)`        -> các phần là maHS / sk, không có `{`
      · registration `M3().ghiLog((ma,giaTri,…) => ENG.logSuKien(maHS, {…}))`
        -> lời gọi NGOÀI chỉ có một tham số là arrow function (bắt đầu bằng `(`) -> loại;
           lời gọi logSuKien BÊN TRONG thân arrow được bắt riêng, đúng một lần
      · method def   `ghiLog(fn){ GHI = fn; }`    -> cat_payload lấy cặp ngoặc của `(fn)` -> loại
    """
    pay, j = cat_payload(s, i_call)
    if not pay:
        return ""
    parts, d, cur = [], 0, []
    for ch in pay:
        if ch in "([{":
            d += 1
        elif ch in ")]}":
            d -= 1
        if ch == "," and d == 0:
            parts.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
    parts.append("".join(cur))
    for p in parts:
        if p.lstrip().startswith("{"):
            return p.strip()
    return ""


_JS_CACHE = {}


def noi_dung_js(ten):
    if ten not in _JS_CACHE:
        try:
            _JS_CACHE[ten] = doc("js/" + ten)
        except Exception:
            _JS_CACHE[ten] = ""
    return _JS_CACHE[ten]


def diem_co_that(payload, sach, pos):
    """(co_diem, nguon) — phát hiện trường `diem` kể cả khi nó nằm trong BIẾN kq.

    LỖI THỨ TƯ CỦA CÔNG CỤ NÀY, tự bắt khi phân loại 6 site chưa có nhãn thao tác.
    app.js:586 ghi `ENG.logSuKien(maHS, { loai:"dauTruong", kq })` — dạng shorthand, nên
    payload không chứa chữ `diem:` nào, trong khi kq do `chamDauTruong()` trả về CÓ trường
    diem (engine.js). Bản đầu chỉ dò literal nên coi site này là "không được chấm"; và vì
    mục 5 đòi `co_diem=True`, thao tác MẠNH NHẤT của sản phẩm (phán quyết có lỗi + chỉ đúng
    chỗ sai) biến mất khỏi danh sách "đứt chuỗi" — tức công cụ báo cáo lạc quan hơn sự thật.

    Cách dò: nếu payload không có `diem:` literal nhưng có `kq` (shorthand hoặc gán biến),
    tìm phép gán `kq = ...` gần nhất TRƯỚC site trong cùng hàm, lấy tên hàm được gọi, rồi mở
    thân hàm đó trong js/ và hỏi nó có trả `diem:` không. Không đoán, không hardcode.
    """
    if re.search(r"\bdiem\s*:", payload):
        return True, "literal trong payload"
    if not re.search(r"(?:\bkq\b\s*[,}]|\bkq\s*:\s*[A-Za-z_$][\w$]*\s*[,}])", payload):
        return False, "không có diem literal, cũng không có kq dạng biến"
    head = sach[:pos]
    gan = list(re.finditer(r"\b(?:const|let|var)\s+kq\s*=\s*([^;\n]{0,140})", head))
    if not gan:
        return False, "kq là biến nhưng không tìm thấy phép gán trong hàm"
    rhs = gan[-1].group(1)
    callee = re.search(r"(?:\w+\.)?(\w+)\s*\(", rhs)
    if not callee:
        return False, "kq gán từ biểu thức không phải lời gọi hàm: " + rhs.strip()[:40]
    ten = callee.group(1)
    for f in sorted(os.listdir(os.path.join(S, "js"))):
        if not f.endswith(".js"):
            continue
        s2 = noi_dung_js(f)
        if "function " + ten + "(" not in s2:
            continue
        than = than_ham(s2, ten)
        if not than:
            continue
        # `diem:` là dạng thường, nhưng JS cho phép SHORTHAND `{ diem, batOan }` khi biến cùng
        # tên. chamDauTruong() trong engine.js trả về đúng dạng shorthand
        # `{ itemId:…, dungVerdict, dungLoai, diem, batOan, boSot, claimChon, claimDung }`,
        # nên bộ dò chỉ tìm `diem:` kết luận site app.js:586 KHÔNG được chấm — và vì mục 5 đòi
        # co_diem=True, thao tác mạnh nhất của sản phẩm biến mất khỏi danh sách đứt chuỗi.
        # Nhận cả hai dạng, nhưng chỉ xét trong object của lệnh `return` để không khớp nhầm
        # một biến `diem` ở chỗ khác trong thân hàm.
        for r in re.finditer(r"return\s*\{([^;]{0,700})\}", than):
            khoi = r.group(1)
            if re.search(r"\bdiem\s*:", khoi) or re.search(r"\bdiem\s*[,}]", khoi):
                return True, ("biến kq -> " + ten + "() trong " + f
                              + " CÓ trả diem"
                              + (" (shorthand)" if not re.search(r"\bdiem\s*:", khoi) else ""))
    return False, "biến kq -> không tìm thấy " + ten + "() trả diem"


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
    # BA LỖI CỦA BẢN QUÉT ĐẦU, cả ba do reviewer độc lập + tự kiểm bắt được ngày 11/10:
    #   (1) chỉ tìm `logSuKien(` nên BỎ SÓT các site gọi qua WRAPPER `ghiLog(maHS, sk)` — mà
    #       wrapper đó chuyển tiếp nguyên vẹn sang logSuKien (bt09.js:147, bt13.js:98). Hai
    #       site bị sót lại mang mã: bt09.js:301 (10.B2.1) và bt13.js:196 (10.C2.3). Site bt09
    #       là thao tác TỰ XUẤT thật (học sinh viết câu trả lời AI >= 20 kí tự có cài lỗi cho
    #       bạn bắt, kiemCau(text, chon) chấm) — nên bỏ sót nó làm mất bằng chứng mạnh nhất
    #       của 10.B2.1.
    #   (2) đếm trùng: app.js:203 là `M3().ghiLog((ma,...) => ENG.logSuKien(maHS, {...}))` nên
    #       khớp CẢ HAI mẫu và bị tính hai lần.
    #   (3) đếm nhầm cả THÂN WRAPPER (bt09.js:148, bt13.js:99) và hàm ĐĂNG KÝ (muc3.js:418
    #       `ghiLog(fn){ GHI = fn; ... }`) thành log site, cùng các dòng nằm trong comment.
    #
    # QUY TẮC PHÂN BIỆT (một luật giải được cả ba lỗi): payload của lời gọi PHẢI LÀ OBJECT
    # LITERAL `{`. Khi đó:
    #   · forwarder `logSuKien(maHS, sk)`          -> payload là `sk`      -> LOẠI
    #   · registration `M3().ghiLog((ma,...) => …)` -> payload là `(ma,…) =>` -> LOẠI
    #     (nhưng lời gọi logSuKien BÊN TRONG thân arrow vẫn được bắt riêng, đúng một lần)
    #   · method def `ghiLog(fn){ GHI = fn; }`     -> payload là `fn`      -> LOẠI
    #   · site thật `logSuKien(maHS, {loai:…})`    -> payload là `{…}`     -> NHẬN
    # Comment bị vô hiệu bằng cách thay nội dung comment bằng khoảng trắng CÙNG ĐỘ DÀI, để số
    # dòng và offset không bị xê dịch (muc3.js:67,79 là chữ trong comment).
    # MỘT vòng lặp với alternation, KHÔNG phải `for ten in ("logSuKien","ghiLog")` lồng ngoài.
    # Bản đầu lồng hai cấp và đẩy `pay`/`ln` xuống indent 16 trong khi phần thân còn lại vẫn ở
    # indent 12 — thân đó rơi vào vòng NGOÀI, nơi `pay` chưa hề được gán, nên nổ
    # UnboundLocalError ngay lần chạy đầu. Một vòng lặp thì indent thân không đổi.
    #
    # LOOKBEHIND là `(?<!\w)`, KHÔNG phải `(?<![\w.$])`. Thêm `.` vào lookbehind nghe có vẻ
    # chặt hơn nhưng lại LOẠI SẠCH các site thật, vì app gọi qua đối tượng: `ENG.logSuKien(...)`
    # và `window.MX_ENGINE.logSuKien(...)` đều có dấu chấm ngay trước tên hàm. Mục tiêu thật của
    # lookbehind chỉ là tránh khớp một tên dài hơn có chứa chuỗi đó (kiểu `xxxlogSuKien`), và
    # `\w` là đủ cho việc ấy.
    RE_SITE = re.compile(r"(?<!\w)(?:logSuKien|ghiLog)\s*\(")
    sites = []
    seen = set()
    for f in sorted(os.listdir(os.path.join(S, "js"))):
        if not f.endswith(".js"):
            continue
        s = doc("js/" + f)
        sach = xoa_comment(s)
        for m in RE_SITE.finditer(sach):
            # lấy tham số OBJECT, không phải cả danh sách tham số — xem cat_obj_arg()
            pay = cat_obj_arg(sach, m.start())
            if not pay:
                continue                      # forwarder / registration / method def
            ln = s[:m.start()].count("\n") + 1
            if (f, ln) in seen:
                continue                      # chống đếm trùng app.js:203
            seen.add((f, ln))
            loai = (re.search(r'loai\s*:\s*"([^"]+)"', pay) or [None, ""])[1]
            sk = (re.search(r'suKien\s*:\s*"([^"]+)"', pay) or [None, ""])[1]
            ham = ham_bao_ngoai(sach, m.start())
            co_diem, nguon_diem = diem_co_that(pay, sach, m.start())
            ym = re.search(r"yccd\s*:\s*([^,\n}]{1,80})", pay)
            yval = ym.group(1).strip() if ym else ""
            sites.append({"tep": "js/" + f, "dong": ln, "loai": loai, "suKien": sk,
                          "ham": ham, "co_diem": co_diem, "nguon_diem": nguon_diem,
                          "yccd_expr": yval, "payload": pay})
    print("tổng số log call site (tham số là object literal): " + str(len(sites)))
    # CHẶN KẾT QUẢ RỖNG — bài học của chính lần chạy trước.
    # Repo này có 25+ lời gọi logSuKien nên "0 site" là BẤT KHẢ THI về mặt dữ liệu; nó chỉ xảy
    # ra khi BỘ LỌC của công cụ hỏng. Nếu vẫn ghi JSON thì số rác (22/22 ĐỨT CHUỖI) chảy thẳng
    # vào so_lieu_ho_so.json rồi vào slide nộp, và trông hoàn toàn giống một phát hiện khoa học.
    # Một công cụ đo phải kêu to khi nó không đo được gì, thay vì trả về kết quả bi quan.
    if len(sites) < 10:
        print("\n✗ CHỈ THẤY " + str(len(sites)) + " log site trong khi app có 25+ lời gọi — "
              "BỘ LỌC CỦA CÔNG CỤ HỎNG, không ghi JSON.")
        print("  Kết quả rỗng sẽ bị đọc nhầm thành 'cả 22 mã đứt chuỗi'. Sửa bộ lọc trước.")
        return 1
    chua_phan_loai = []
    for st in sites:
        k1 = (st["loai"], st["suKien"])
        k2 = (st["loai"], st["ham"])
        if k1 not in THAO_TAC and k2 not in THAO_TAC:
            chua_phan_loai.append(st["tep"] + ":" + str(st["dong"]) + " " + st["loai"]
                                   + "/" + (st["suKien"] or st["ham"]))
    if chua_phan_loai:
        print("  ⚠ SITE CHƯA PHÂN LOẠI THAO TÁC (sẽ thành '?', phải bổ sung THAO_TAC):")
        for x in chua_phan_loai:
            print("      " + x)
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
    print("  (co_diem dò được cả khi `diem` nằm trong biến kq — xem diem_co_that())")
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
        elif muc == "tu_xuat_gv":
            dut.append((st["tep"] + ":" + str(st["dong"]), st["loai"], st["suKien"], nhan))
            print("  ✗ " + st["tep"] + ":" + str(st["dong"]) + " " + st["loai"] + "/"
                  + (st["suKien"] or st["ham"]) + " — " + nhan
                  + "  [máy KHÔNG chấm: giáo viên đọc và nhận xét]")
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
        # `van_hanh` (bấm nút chạy huấn luyện, hệ thống in số) yếu hơn `tu_xuat` nhưng khác
        # bản chất với `nhan_dien` (chọn 1 trong N). Cả hai đều chỉ đủ cho mức PHỦ MỘT PHẦN,
        # nên gộp vào một nhóm xét — nhưng nhãn in ra vẫn nói rõ là loại nào.
        do_duoc = [x for x in co_diem if x["muc_thao_tac"] in ("van_hanh", "nhan_dien")]
        if tu_xuat:
            pq = "A:PHỦ THẬT"
            ly = ("thao tác TỰ XUẤT RA được chấm và bản ghi CÓ mang mã: "
                  + ", ".join(sorted({x["site"] + " (" + x["thao_tac"][:34] + ")" for x in tu_xuat})))
        elif do_duoc:
            pq = "B:PHỦ MỘT PHẦN"
            ly = ("có chấm + mang mã nhưng thao tác chỉ ở mức NHẬN DIỆN/VẬN HÀNH, không phải "
                  "tự xuất ra: "
                  + ", ".join(sorted({x["site"] + " (" + x["thao_tac"][:34] + ")" for x in do_duoc})))
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
