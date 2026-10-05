#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""JUDGE ĐỘC LẬP — nghiệm thu xác định cho SOI AI (system-one-work-loop).

File này là QUAN NGHIỆM THU, không phải thợ. Nó KHÔNG build gì, chỉ đo.
Nguyên tắc: mọi tiêu chí phải chấm được bằng yes/no từ file trên đĩa hoặc HTTP,
không có "trông có vẻ ổn".

GOAL (7 tiêu chí):
  G1 NỀN SÁNG     — không còn màu nền tối; mọi cặp chữ/nền đạt WCAG 4.5:1;
                    cặp đồ hoạ đạt 3.0:1. Đo bằng công thức tương phản, không ước lượng.
  G2 ICON SVG     — 0 emoji làm biểu tượng điều khiển (nút/menu/logo);
                    sprite SVG Lucide tồn tại và mọi <use href="#..."> đều trỏ tới id có thật.
  G3 7 TRẠM       — cả 7 trạm của nhà máy có nội dung tương tác thật;
                    không trạm nào còn chữ "đang được xây dựng".
  G4 CHẤT LƯỢNG VĂN BẢN TRẠM 5 — tỉ lệ từ có nghĩa >= ngưỡng; 0 câu bắt đầu giữa từ;
                    oracle vẫn đúng; phân bố lỗi ~60%.
  G5 KHÔNG LỖI    — app chạy trên file:// và https://, 0 lỗi console,
                    mọi view điều hướng được, không còn "điểm số" ở UI kết quả.
  G6 OFFLINE      — không có request ra mạng nào bắt buộc (font CDN, thư viện CDN);
                    three.js và icon đều nằm trong repo.
  G7 DEPLOY       — Pages trả 200 cho mọi asset mới, đúng commit.
  G8 KỊCH BẢN ẢO ẢNH — caption <= 14 từ, 0 emoji/homoglyph, thời lượng lấy từ dữ liệu.
  G9 ÍT CHỮ       — chế độ "ít chữ" không được ẩn phần tử CHỨC NĂNG.
  G10 KHÔNG TIẾP THỊ — ngôn ngữ tiếp thị đã bỏ không được quay lại; tên hiển thị là
                    định danh môn/lớp; phiên bản chân trang khớp data/meta.js.
  G11 HAI MODULE MỨC 3 — bt13.js và bt09.js phải nạp trước app.js, mọi icon chúng gọi
                    phải có thật trong sprite, và KHÔNG có biến nào chứa chữ học sinh
                    đi vào innerHTML. Thêm 05/10 vì reviewer độc lập trên PR #1 phát
                    hiện cổng cũ KHÔNG nhắc tới hai tệp này lần nào: tệp không nằm
                    trong cổng thì mọi lỗi trong nó đều là "đã kiểm" theo nghĩa sai.

RANH GIỚI (không được vi phạm — kháng Goodhart):
  * Không xoá/nới bất kì phép kiểm nào trong file này để pass.
  * Không sửa ngưỡng. Nếu ngưỡng sai, phải nói rõ với anh Văn, không tự hạ.
  * Không được phá chế độ offline file://.
  * Không hiển thị "điểm"/"xếp loại" cho học sinh (Khung 2422 phần VI).
  * Không thu họ tên/ảnh/dữ liệu cá nhân.
"""
import datetime, json, os, re, subprocess, sys, urllib.request, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.environ.get("SOI_AI_SITE", "https://mxuanvan02.github.io/soi-ai-lop10")
NGUONG_TU_CO_NGHIA = 0.72      # G4: >=72% từ sinh ra phải có trong ngữ liệu
NGUONG_PHAN_BO_LOI = (0.45, 0.75)   # G4: tỉ lệ "có lỗi" phải nằm trong khoảng này


# ---------- WCAG ----------
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def L(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(a, b):
    la, lb = L(a), L(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def doc(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def than_ma_song(js):
    """Bỏ comment khỏi một tệp JS để chỉ còn MÃ SỐNG.

    VÌ SAO CẦN (bài học thật, 05/10): phép grep thô trên tệp còn comment sẽ khớp cả
    CHỮ TRONG GHI CHÚ. Tệp js/bt13.js có dòng ghi chú viết `svgIco("tên")` như một ví
    dụ mô tả quy tắc — reviewer độc lập grep thô rồi kết luận tệp gọi một icon không
    tồn tại và đề nghị CHẶN MERGE. Đó là dương tính giả toàn tập: nó khiến người đọc
    đi sửa thứ không hỏng, và tệ nhất là làm mất lòng tin vào các cảnh báo thật.
    Mọi phép đếm dấu hiệu trong mã JS phải chạy trên mã sống, không chạy trên comment.
    """
    js = re.sub(r"/\*.*?\*/", " ", js, flags=re.S)
    js = re.sub(r"(?m)//[^\n]*", " ", js)
    return js


def bien_chua_chu_hoc_sinh(js_song):
    """Tên các biến được gán từ `.value` — tức chữ do học sinh gõ vào ô nhập."""
    return set(re.findall(r"(?:const|let|var)\s+(\w+)\s*=\s*[^;\n]*\.value", js_song))


class Judge:
    def __init__(self):
        self.kq = []
        # Hai cờ phục vụ việc CHẶN ghi tệp bằng chứng phần (xem tong_ket):
        #   day_du        — lần chạy này có phải chạy ĐẦY ĐỦ mọi nhóm không
        #   nhom_da_chay  — danh sách nhóm thực sự đã chạy, để ghi vào sidecar meta
        self.day_du = False
        self.nhom_da_chay = []

    def them(self, ma, ten, dat, chi_tiet=""):
        self.kq.append({"ma": ma, "ten": ten, "dat": bool(dat), "chi_tiet": chi_tiet})
        print(f"  [{'ĐẠT ' if dat else 'LỖI'}] {ma} {ten}" + (f" — {chi_tiet}" if chi_tiet else ""))

    # ============ G1 NỀN SÁNG ============
    def g1(self):
        print("\n=== G1 NỀN SÁNG + TƯƠNG PHẢN ===")
        css = doc("css/style.css")
        # 1a. biến màu gốc phải là màu sáng
        m = re.search(r":root\{(.*?)\}", css, re.S)
        if not m:
            self.them("G1", "khai báo :root", False, "không tìm thấy :root trong style.css")
            return
        root = m.group(1)
        vars_ = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{3,8})", root))
        # màu nền tối điển hình của bản cũ
        toi = ["#0f1115", "#161a22", "#1d222c", "#11151d", "#000"]
        con_toi = [v for k, v in vars_.items() if v.lower() in toi]
        self.them("G1a", "không còn biến nền tối trong :root", not con_toi,
                  f"còn: {con_toi}" if con_toi else f"nền={vars_.get('nen')} thẻ={vars_.get('the')}")

        # 1b. nền trang/thẻ phải THẬT SỰ sáng (độ chói cao)
        nen, the = vars_.get("nen", "#fff"), vars_.get("the", "#fff")
        self.them("G1b", "nền trang đủ sáng (L>0.7)", L(nen) > 0.7, f"--nen={nen} L={L(nen):.3f}")
        self.them("G1c", "nền thẻ đủ sáng (L>0.85)", L(the) > 0.85, f"--the={the} L={L(the):.3f}")

        # 1c. mọi cặp chữ/nền phải đạt 4.5
        chu, chu2 = vars_.get("chu"), vars_.get("chu2")
        pairs = [(f"chữ chính/{nen}", chu, nen), (f"chữ chính/{the}", chu, the),
                 (f"chữ phụ/{nen}", chu2, nen), (f"chữ phụ/{the}", chu2, the)]
        # thêm các màu trạng thái trên nền thẻ
        for ten_, k in [("màu đúng", "dung"), ("màu sai", "sai"),
                        ("màu nhấn", "nhan"), ("màu vàng", "vang")]:
            if k in vars_:
                pairs.append((f"{ten_}/{the}", vars_[k], the))
        lo = []
        for ten_, fg, bg in pairs:
            if not fg or not bg:
                continue
            r = ratio(fg, bg)
            if r < 4.5:
                lo.append(f"{ten_}: {fg}/{bg}={r:.2f}")
        self.them("G1d", "mọi cặp CHỮ/nền >= 4.5:1", not lo, "; ".join(lo) or f"{len(pairs)} cặp đạt")

        # 1d. màu đồ hoạ (viền, thanh, lưới) >= 3.0
        do_hoa = []
        for k in ("vien", "nhan"):
            if k in vars_:
                r = ratio(vars_[k], the)
                if r < 3.0:
                    do_hoa.append(f"{k}={vars_[k]}:{r:.2f}")
        self.them("G1e", "viền/màu nhấn >= 3.0:1 trên nền thẻ", not do_hoa,
                  "; ".join(do_hoa) or "đạt")

        # 1e. màu hardcode trong CSS
        # SỬA LẠI PHÉP KIỂM NÀY (04/10, ghi rõ để không ai tưởng là hạ ngưỡng):
        #   Bản đầu gộp chung background/color/border-color rồi flag mọi màu có L<0.25.
        #   Phép đó SAI về bản chất: #15803D (4.79:1) và #7C3AED (5.70:1) là MÀU CHỮ
        #   hợp lệ trên nền trắng, bị flag oan; trong khi nền tối thật sự mới là lỗi.
        #   Nay tách thành 2 phép đo ĐÚNG đối tượng và CHẶT HƠN bản cũ:
        #     G1f: màu làm NỀN phải sáng (L>0.5)  -> bắt đúng leftover dark theme
        #     G1f2: màu làm CHỮ hardcode phải đạt >=4.5:1 trên nền thẻ -> bản cũ không đo
        nen_hard = re.findall(r"background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,8})", css)
        nen_toi = sorted({h for h in nen_hard if L(h) < 0.5})
        self.them("G1f", "mọi màu NỀN hardcode đều sáng (L>0.5)", not nen_toi,
                  f"nền tối còn sót: {nen_toi}" if nen_toi
                  else f"{len(set(nen_hard))} màu nền hardcode, đều sáng")

        # màu chữ hardcode: PHẢI ghép với nền của CHÍNH rule đó.
        # SỬA LẠI LẦN 2 (04/10) — và đây là sửa cho ĐÚNG, làm phép đo CHẶT HƠN:
        #   Lần 1: đo mọi `color:` với nền thẻ trắng -> flag oan chữ trắng trên nút tím.
        #   Lần 2 (bản này): resolve var(--x) về giá trị thật. Bản trước chỉ match
        #   `background:#hex` nên khi nền là var(--primary) nó fallback về #FFFFFF và
        #   đo #FFFFFF/#FFFFFF = 1.00 -> false positive, đồng thời BỎ SÓT việc kiểm tra
        #   cặp thật (chữ trắng trên #7C3AED). Nay cặp đó bị kiểm tra thật sự.
        def resolve(gia_tri, vars_):
            if not gia_tri:
                return None
            m = re.match(r"var\(--([\w-]+)\)", gia_tri.strip())
            if m:
                return vars_.get(m.group(1))
            return gia_tri if gia_tri.startswith("#") else None

        # thu thập cả khai báo dạng var()
        chu_loi, da_do = [], 0
        RE_FG = r"(?<![-\w])color\s*:\s*(#[0-9a-fA-F]{3,8}|var\(--[\w-]+\))"
        RE_BG = r"background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,8}|var\(--[\w-]+\))"
        for block in re.findall(r"\{([^{}]*)\}", css):
            mc = re.search(RE_FG, block)
            if not mc:
                continue
            mb = re.search(RE_BG, block)
            fg = resolve(mc.group(1), vars_)
            bg = resolve(mb.group(1), vars_) if mb else the
            if not fg or not bg:
                continue
            da_do += 1
            r = ratio(fg, bg)
            if r < 4.5:
                chu_loi.append(f"{fg}/{bg}={r:.2f}")
        self.them("G1f2", "mọi cặp chữ/nền hardcode >= 4.5:1 (đã resolve var())",
                  not chu_loi,
                  "; ".join(chu_loi) if chu_loi else f"{da_do} cặp đã đo, đều đạt")

        # ---------- G1f3: cặp chữ/nền KẾ THỪA (judge G1f2 bỏ lọt) ----------
        # Vì sao cần phép riêng: G1f2 ghép `color:` với `background:` TRONG CÙNG một rule.
        # Nhưng CSS có kế thừa, ví dụ:
        #   .nm-tram.xong{border-color:var(--dung);background:var(--nenDung)}
        #   .nm-tram.xong .an-duy{color:var(--dung)}      <- không có background riêng
        # -> cặp thật là --dung trên --nenDung, G1f2 không thấy nên bỏ lọt.
        # Đây chính là lỗi thật đã xảy ra: #15803D trên #E7F5EA = 4.45:1 (< 4.5).
        # Cách đo: liệt kê tường minh mọi cặp "chữ trên nền trạng thái" có trong CSS
        # và đo tất cả. Liệt kê là do người viết judge khai báo, nhưng GIÁ TRỊ MÀU
        # được đọc từ chính :root của CSS nên không thể chép sai số.
        CAP_KE_THUA = [
            ("chữ --chu2 trên nền phụ --nen2", "chu2", "nen2"),
            ("chữ --chu2 trên nền --nenDung", "chu2", "nenDung"),
            ("chữ --chu2 trên nền --nenSai", "chu2", "nenSai"),
            ("chữ --chu2 trên nền --nenChon", "chu2", "nenChon"),
            ("chữ --dung trên nền --nenDung (đèn TRUE, trạm đã xong)", "dung", "nenDung"),
            ("chữ --sai trên nền --nenSai (đèn FALSE, phản hồi sai)", "sai", "nenSai"),
            ("chữ --nhan trên nền --nenChon (chip đang chọn)", "nhan", "nenChon"),
            ("chữ --nhan trên nền phụ --nen2 (số KPI)", "nhan", "nen2"),
            ("chữ --vang trên nền --nen2", "vang", "nen2"),
            ("chữ --chu trên nền phụ --nen2 (ai-box, code)", "chu", "nen2"),
        ]
        lo_kt = []
        for ten_, kfg, kbg in CAP_KE_THUA:
            fg, bg = vars_.get(kfg), vars_.get(kbg)
            if not fg or not bg:
                lo_kt.append(f"{ten_}: thiếu biến --{kfg}/--{kbg}")
                continue
            r = ratio(fg, bg)
            if r < 4.5:
                lo_kt.append(f"{ten_}: {fg}/{bg}={r:.2f}")
        self.them("G1f3", "mọi cặp chữ/nền KẾ THỪA >= 4.5:1", not lo_kt,
                  "; ".join(lo_kt) if lo_kt else f"{len(CAP_KE_THUA)} cặp đã đo, đều đạt")

        # ---------- G1i: màu 5 TRẠM trong pipeline3d.js ----------
        # LỖ HỔNG CỦA JUDGE ĐÃ BỊT (04/10): G1h chỉ đọc bảng MAU trong scene3d.js nên
        # BỎ LỌT 5 màu trạm hardcode trong pipeline3d.js. Hậu quả thật đã xảy ra: 4/5 màu
        # trạm kế thừa từ giao diện tối và FAIL trên nền sáng —
        #   #ffd43b = 1.36 · #4dabf7 = 2.37 · #51cf66 = 1.92 · #ff6b6b = 2.65
        # Nay đo trực tiếp mọi `mau:0x......` trong pipeline3d.js trên nền cảnh.
        try:
            pp = doc("js/pipeline3d.js")
            mau_tram = re.findall(r"mau:\s*0x([0-9a-fA-F]{6})", pp)
            # BUG ĐÃ SỬA: bản đầu dùng biến `m2` ở đây nhưng m2 chỉ được gán ở khối
            # "1f. scene 3D" NẰM SAU -> NameError, cả phép G1i/G1j chết.
            # Nay tự đọc nền cảnh từ scene3d.js, không phụ thuộc thứ tự khối.
            _sc = doc("js/scene3d.js")
            _m = re.search(r"nen:\s*0x([0-9a-fA-F]{6})", _sc)
            bg3d = ("#" + _m.group(1)) if _m else "#F8FAFC"
            lo_tram = []
            for h in mau_tram:
                r = ratio("#" + h, bg3d)
                if r < 3.0:
                    lo_tram.append(f"#{h}={r:.2f}")
            self.them("G1i", "màu 5 trạm ống dẫn >= 3.0:1 trên nền cảnh",
                      len(mau_tram) == 5 and not lo_tram,
                      ("; ".join(lo_tram) if lo_tram else
                       f"{len(mau_tram)} màu trạm, đều đạt") +
                      ("" if len(mau_tram) == 5 else f" (mong đợi 5, thấy {len(mau_tram)})"))

            # khoảng cách màu: 5 trạm phải phân biệt được bằng mắt
            def rgb(hx):
                hx = hx.lstrip("#")
                return tuple(int(hx[i:i + 2], 16) for i in (0, 2, 4))
            import itertools as it
            ds = []
            for a, b in it.combinations(mau_tram, 2):
                ra, rb = rgb(a), rgb(b)
                ds.append(((ra[0]-rb[0])**2 + (ra[1]-rb[1])**2 + (ra[2]-rb[2])**2) ** 0.5)
            NGUONG_PHAN_BIET = 100.0
            self.them("G1j", f"5 màu trạm phân biệt được (khoảng cách RGB nhỏ nhất >= {NGUONG_PHAN_BIET:.0f})",
                      bool(ds) and min(ds) >= NGUONG_PHAN_BIET,
                      f"nhỏ nhất = {min(ds):.1f}" if ds else "không đo được")
        except OSError as e:
            self.them("G1i", "đọc pipeline3d.js", False, str(e)[:120])

        # 1f. scene 3D phải có nền sáng
        sc = doc("js/scene3d.js")
        m2 = re.search(r"nen:\s*0x([0-9a-fA-F]{6})", sc)
        if m2:
            hexnen = "#" + m2.group(1)
            self.them("G1g", "nền cảnh 3D sáng (L>0.7)", L(hexnen) > 0.7, f"0x{m2.group(1)} L={L(hexnen):.3f}")
        else:
            self.them("G1g", "nền cảnh 3D sáng", False, "không tìm thấy MAU.nen trong scene3d.js")

        # 1g. 4 màu dữ liệu 3D phải đạt 3.0:1 trên nền cảnh
        if m2:
            bg3d = "#" + m2.group(1)
            mau3d = dict(re.findall(r"(\w+):\s*0x([0-9a-fA-F]{6})", sc))
            can = {"vang": "ảnh ban ngày", "nhan": "ảnh ban đêm",
                   "sai": "AI đoán sai", "dung": "AI đoán đúng"}
            lo2 = []
            for k, ten_ in can.items():
                if k in mau3d:
                    r = ratio("#" + mau3d[k], bg3d)
                    if r < 3.0:
                        lo2.append(f"{ten_}=#{mau3d[k]}:{r:.2f}")
            self.them("G1h", "4 màu dữ liệu 3D >= 3.0:1 trên nền cảnh", not lo2,
                      "; ".join(lo2) or "đạt cả 4")

    # ============ G2 ICON SVG ============
    def g2(self):
        print("\n=== G2 ICON SVG (không emoji làm biểu tượng) ===")
        idx = doc("index.html")
        # sprite phải tồn tại
        SO_SYMBOL = re.findall(r'symbol id="i-', idx)
        has_sprite = "<svg" in idx and bool(SO_SYMBOL)
        self.them("G2a", "có sprite SVG nội tuyến trong index.html", has_sprite,
                  f"{len(SO_SYMBOL)} symbol" if has_sprite else "không thấy")

        # mọi <use href="#i-..."> phải trỏ tới symbol có thật
        ids = set(re.findall(r'symbol id="(i-[\w-]+)"', idx))
        uses = set(re.findall(r'<use[^>]*href="#(i-[\w-]+)"', idx))
        mo_coi = sorted(uses - ids)
        self.them("G2b", "mọi <use> trỏ tới symbol có thật", not mo_coi,
                  f"mồ côi: {mo_coi}" if mo_coi else f"{len(uses)} use / {len(ids)} symbol")

        # emoji làm biểu tượng ĐIỀU KHIỂN: trong <button>, .logo, .menu-o b, th/td đầu bảng
        # (emoji trong văn bản thân thiện với HS vẫn được phép)
        EMOJI = r"[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]"
        nut = re.findall(r"<button[^>]*>(.*?)</button>", idx, re.S)
        bi_lo = []
        for b in nut:
            # bỏ phần trong <svg>...</svg> rồi mới dò emoji
            sach = re.sub(r"<svg.*?</svg>", "", b, flags=re.S)
            e = re.findall(EMOJI, sach)
            if e:
                txt = re.sub(r"<[^>]+>", "", sach).strip()[:40]
                bi_lo.append(f"{''.join(e)} '{txt}'")
        self.them("G2c", "0 emoji trong <button>", not bi_lo,
                  f"{len(bi_lo)} nút còn emoji: {bi_lo[:5]}" if bi_lo else f"{len(nut)} nút sạch")

        logo = re.findall(r'<div class="logo">(.*?)</div>', idx, re.S)
        logo_emo = [re.findall(EMOJI, l) for l in logo]
        logo_emo = [x for x in logo_emo if x]
        self.them("G2d", "0 emoji trong .logo", not logo_emo, str(logo_emo) if logo_emo else "sạch")

    # ============ G3 7 TRẠM ============
    def g3(self):
        print("\n=== G3 NHÀ MÁY 7 TRẠM ===")
        app = doc("js/app.js")
        tram = re.findall(r'\{\s*id:(\d+),\s*so:"TRẠM \d+",\s*ten:"([^"]+)"', app)
        self.them("G3a", "khai báo đủ 7 trạm", len(tram) == 7,
                  f"{len(tram)} trạm: {[t[1] for t in tram]}")
        # không trạm nào còn "đang xây dựng"
        xd = "đang được xây dựng" in app or "đang xây dựng" in app
        self.them("G3b", "không trạm nào còn 'đang xây dựng'", not xd,
                  "còn chữ 'đang xây dựng' trong app.js" if xd else "sạch")
        # mỗi trạm phải có view thật
        views = re.findall(r'view:("?[\w-]+"?|null)', app)
        nulls = sum(1 for v in views if v == "null")
        self.them("G3c", "mọi trạm đều có view (không null)", nulls == 0,
                  f"{nulls} trạm view:null" if nulls else f"{len(views)} trạm có view")
        # module trạm 0/1 phải tồn tại và được nạp
        f01 = os.path.exists(os.path.join(ROOT, "js/nhamay_tram01.js"))
        self.them("G3d", "có js/nhamay_tram01.js", f01)
        if f01:
            nap = 'src="js/nhamay_tram01.js"' in doc("index.html")
            self.them("G3e", "nhamay_tram01.js được nạp trong index.html", nap)
            m = doc("js/nhamay_tram01.js")
            self.them("G3f", "module trạm 0/1 export window.MX_NHAMAY01",
                      "window.MX_NHAMAY01" in m)

    # ============ G4 CHẤT LƯỢNG VĂN BẢN ============
    def g4(self, node="/usr/bin/node"):
        print("\n=== G4 CHẤT LƯỢNG VĂN BẢN TRẠM 5 ===")
        probe = os.path.join("/tmp", "judge_g4.js")
        with open(probe, "w", encoding="utf-8") as f:
            f.write(r"""
global.window = {}; global.performance = { now: () => Date.now() };
require(process.argv[2]);
const N = global.window.MX_NHAMAY_TEXT;
const corpus = N.CORPUS.toLowerCase();
const tuTrongNguLieu = (s) => {
  const ws = s.toLowerCase().match(/[a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+/g) || [];
  if (!ws.length) return 0;
  let hit = 0;
  for (const w of ws) if (w.length > 1 && corpus.includes(w)) hit++;
  return hit / ws.length;
};
const out = { mau: [], tiLe: [], cun: 0, phanBo: { coLoi: 0, tong: 0 }, nhom: {},
              cauKhop: 0, cauTong: 0 };
// G4a2: tập CÂU có thật trong ngữ liệu (câu chung + câu của 4 chủ đề).
// Chuẩn hoá hai phía: gộp khoảng trắng, lowercase, bỏ dấu chấm cuối.
const norm = (s) => s.trim().replace(/\s+/g, ' ').toLowerCase().replace(/\.$/, '');
const cauThat = new Set();
N.CORPUS.split(/(?<=\.)\s+/).forEach(c => cauThat.add(norm(c)));
Object.keys(N.CHU_DE).forEach(k => N.CHU_DE[k].cau.forEach(c => cauThat.add(norm(c))));
out.soCauTrongNguLieu = cauThat.size;

// 20 mẫu: xen kẽ 10 câu hỏi CÓ trong ngữ liệu và 10 câu hỏi NGOÀI ngữ liệu
for (let s = 1; s <= 20; s++) {
  const prompt = (s % 2) ? "ứng dụng AI trong nông nghiệp ở Việt Nam" : "giá vàng hôm nay";
  const it = N.ungDung(prompt, { seed: s });
  const tl = tuTrongNguLieu(it.vanBan);
  out.tiLe.push(tl);
  // mỗi câu trong đầu ra phải là CÂU THẬT trong ngữ liệu, không phải mảnh vụn ghép ngang
  it.vanBan.split(/(?<=\.)\s+/).map(norm).filter(Boolean).forEach(c => {
    out.cauTong++;
    if (cauThat.has(c)) out.cauKhop++;
  });
  if (s <= 4) out.mauCoCanCu = (out.mauCoCanCu || []);
  if (/^[ỂỂỆẬỐỒỖỔẤỀỄẾỂẶẶ]/.test(it.vanBan) || /^[a-zàáảãạâăèéẻẽẹêìíỉĩịòóỏõọôơùúủũụưđ]/.test(it.vanBan[0])) out.cun++;
  if (s <= 6) out.mau.push(it.vanBan.slice(0, 110));
}
for (let s = 1; s <= 200; s++) {
  const it = N.taoCauTraLoi({ seed: s });
  out.phanBo.tong++;
  if (it.coLoi) { out.phanBo.coLoi++; out.nhom[it.tenNhomLoi] = (out.nhom[it.tenNhomLoi]||0)+1; }
}
// G4b2 — THÊM MỚI vì G4b bỏ lọt lỗi thật (04/10):
//   G4b chỉ kiểm tra chữ cái đầu CỦA CẢ CHUỖI, nên không bắt được câu thứ hai
//   bắt đầu bằng chữ thường khi ghép hai câu ("...mười ba chủ đề. khi vận hành...").
//   Lỗi này do chuanHoa() hạ chữ thường toàn bộ trước khi tách câu.
//   Phép đo đúng: MỌI câu trong đầu ra phải bắt đầu bằng chữ in hoa.
out.cauChuaVietHoa = 0; out.cauDaDo = 0; out.mauChuaVietHoa = [];
for (let s = 1; s <= 20; s++) {
  const it = N.ungDung(s % 2 ? "nông nghiệp" : "giá vàng", { seed: s });
  it.vanBan.split(/(?<=\.)\s+/).forEach(c => {
    const t = c.trim();
    if (!t) return;
    out.cauDaDo++;
    if (t[0] !== t[0].toUpperCase() || t[0] === t[0].toLowerCase()) {
      out.cauChuaVietHoa++;
      if (out.mauChuaVietHoa.length < 3) out.mauChuaVietHoa.push(t.slice(0, 46));
    }
  });
}
// oracle
let a=0,b=0;
for (let s=1;s<=40;s++){
  const it=N.taoCauTraLoi({seed:s});
  if (N.cham(it,{coLoi:it.coLoi, nhomLoi:it.nhomLoi}).dung) a++;
  if (!N.cham(it,{coLoi:!it.coLoi, nhomLoi:'x'}).dung) b++;
}
out.oracle = { dungDung:a, saiSai:b, tong:40 };
// trạm ứng dụng oracle
let c=0,d=0;
for (let s=1;s<=40;s++){
  const it=N.ungDung("nông nghiệp",{seed:s});
  if (N.chamUngDung(it,{coCanCu:it.trongNguLieu}).dung) c++;
  if (!N.chamUngDung(it,{coCanCu:!it.trongNguLieu}).dung) d++;
}
out.oracleUngDung = { dungDung:c, saiSai:d, tong:40 };
out.avgTiLe = out.tiLe.reduce((x,y)=>x+y,0)/out.tiLe.length;
out.minTiLe = Math.min(...out.tiLe);
out.tiLeCauTronVen = out.cauTong ? out.cauKhop/out.cauTong : 0;
out.tiLeManhVun = 1 - out.tiLeCauTronVen;
console.log(JSON.stringify(out));
"""
            )
        r = subprocess.run([node, probe, os.path.join(ROOT, "js/nhamay_text.js")],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            self.them("G4", "chạy probe nhamay_text.js", False, r.stderr[-400:])
            return
        d = json.loads(r.stdout.strip())

        # G4a — PHÉP ĐO CŨ BỊ LOẠI VÌ GOODHART (ghi rõ để không ai dùng lại):
        #   "tỉ lệ từ có trong ngữ liệu" luôn gần 1.00 với máy n-gram, vì máy sinh chữ
        #   LẤY TỪ CHÍNH ngữ liệu. Nó đo "chữ có nguồn gốc" chứ KHÔNG đo "câu có nghĩa".
        #   Bằng chứng: điểm 0.992 trong khi văn bản thật vẫn lộn xộn
        #   ("Con người ba chủ đề. mô hình ảnh. hệ thống trí tuệ nhân tạo là lĩnh vực
        #   nghiên kiến dữ liệu cá nhân tạo sinh p").
        #   Phép đo thay thế (G4a2) đo đúng thứ cần đo: đầu ra có phải là CÂU HOÀN CHỈNH
        #   lấy từ ngữ liệu hay là mảnh vụn ghép ngang.
        NGUONG_CAU_TRON_VEN = 0.80
        self.them("G4a2", f"đầu ra là câu hoàn chỉnh >= {NGUONG_CAU_TRON_VEN:.0%}",
                  d.get("tiLeCauTronVen", 0) >= NGUONG_CAU_TRON_VEN,
                  f"{d.get('tiLeCauTronVen', 0)*100:.1f}% câu trọn vẹn · "
                  f"mảnh vụn {d.get('tiLeManhVun', 0)*100:.1f}%")
        self.them("G4a", "(đã loại — metric Goodhart, xem ghi chú trong code)", True,
                  "giữ dòng này để không ai tái sử dụng 'tỉ lệ từ trong ngữ liệu'")
        self.them("G4b", "0 câu bắt đầu giữa từ / chữ thường vô nghĩa", d["cun"] == 0,
                  f"{d['cun']}/20 câu lỗi")
        # G4b2 — phép đo MỚI, bắt lỗi mà G4b bỏ lọt (xem ghi chú trong probe JS)
        self.them("G4b2", "mọi câu trong đầu ra đều viết hoa đầu câu",
                  d.get("cauChuaVietHoa", 1) == 0,
                  f"{d.get('cauChuaVietHoa')}/{d.get('cauDaDo')} câu chưa viết hoa"
                  + (f" — vd: {d.get('mauChuaVietHoa')}" if d.get("cauChuaVietHoa") else ""))
        p = d["phanBo"]["coLoi"] / max(1, d["phanBo"]["tong"])
        self.them("G4c", f"phân bố 'có lỗi' trong {NGUONG_PHAN_BO_LOI}",
                  NGUONG_PHAN_BO_LOI[0] <= p <= NGUONG_PHAN_BO_LOI[1], f"{p*100:.1f}%")
        self.them("G4d", "oracle đấu trường 40/40 cả 2 nhánh",
                  d["oracle"]["dungDung"] == 40 and d["oracle"]["saiSai"] == 40, str(d["oracle"]))
        self.them("G4e", "oracle trạm ứng dụng 40/40 cả 2 nhánh",
                  d["oracleUngDung"]["dungDung"] == 40 and d["oracleUngDung"]["saiSai"] == 40,
                  str(d["oracleUngDung"]))
        print("     mẫu văn bản sinh ra:")
        for m in d["mau"][:4]:
            print("       •", m)

    # ============ G6 OFFLINE ============
    def g6(self):
        print("\n=== G6 OFFLINE (không bắt buộc có mạng) ===")
        idx = doc("index.html")
        # không được có font CDN / thư viện CDN trong thẻ nạp tài nguyên
        cdn = re.findall(r'(?:src|href)="(https?://[^"]+)"', idx)
        self.them("G6a", "không nạp asset từ CDN trong index.html", not cdn,
                  f"còn: {cdn}" if cdn else "sạch")
        css = doc("css/style.css")
        imp = re.findall(r'@import\s+url\([\'"]?(https?://[^)\'"]+)', css)
        self.them("G6b", "không @import font từ mạng", not imp, f"còn: {imp}" if imp else "sạch")
        # three.js phải nằm trong repo
        t1 = os.path.exists(os.path.join(ROOT, "vendor/three/three.min.js"))
        t2 = os.path.exists(os.path.join(ROOT, "vendor/three/OrbitControls.js"))
        self.them("G6c", "three.js + OrbitControls nằm trong repo", t1 and t2)
        # font phải là phông hệ thống
        self.them("G6d", "dùng phông hệ thống (Segoe UI/system-ui)",
                  "system-ui" in css and "Segoe UI" in css)

    # ============ G7 DEPLOY ============
    def g7(self):
        print("\n=== G7 DEPLOY (HTTP thật) ===")
        assets = ["index.html", "css/style.css", "js/app.js", "js/nhamay_text.js",
                  "js/nhamay_tram01.js", "js/scene3d.js", "js/lab3d.js", "js/pipeline3d.js",
                  "data/yccd.js", "vendor/three/three.min.js"]
        lo = []
        for a in assets:
            try:
                u = f"{SITE}/{a}?nc={os.getpid()}"
                req = urllib.request.Request(u, headers={"Cache-Control": "no-cache"})
                code = urllib.request.urlopen(req, timeout=25).getcode()
            except Exception as e:
                code = getattr(e, "code", str(e)[:40])
            if code != 200:
                lo.append(f"{a}={code}")
        self.them("G7a", f"mọi asset trả 200 ({len(assets)} tệp)", not lo, "; ".join(lo) or "đạt cả")
        # nội dung thật trên site phải là bản sáng
        # LỖI BÁO CÁO ĐÃ SỬA (04/10): bản đầu truyền chi_tiet là một chuỗi CỐ ĐỊNH mang
        # giọng thất bại ("không thấy #FAF5FF — có thể Pages chưa build xong") trong khi
        # điều kiện lại ĐẠT. Kết quả: judge in "[ĐẠT] ... không thấy #FAF5FF" — tự mâu
        # thuẫn, và khiến người đọc tưởng deploy hỏng dù curl xác nhận biến màu có thật.
        # Nay chi_tiet được tính THEO KẾT QUẢ, kèm bằng chứng trích ra từ nội dung tải về.
        try:
            html = urllib.request.urlopen(f"{SITE}/css/style.css?nc={os.getpid()}", timeout=25).read().decode()
            m = re.search(r"--nen:\s*(#[0-9a-fA-F]{6})", html)
            dat = bool(m) and m.group(1).upper() == "#FAF5FF"
            self.them("G7b", "CSS trên site là bản nền sáng", dat,
                      f"--nen={m.group(1)} (đọc từ site)" if dat else
                      ("không tìm thấy khai báo --nen trong CSS tải về" if not m
                       else f"--nen={m.group(1)} ≠ #FAF5FF"))
        except Exception as e:
            self.them("G7b", "đọc CSS từ site", False, str(e)[:120])

    # ================= G8 — KỊCH BẢN ÍT CHỮ & 3 BÀI HỌC ẢO ẢNH TEST =================
    def g8(self):
        """Cổng G8, thêm 04/10 sau khi dựng js/kichban.js.

        Ba phép kiểm ở đây đều sinh ra từ LỖI THẬT đã xảy ra, không phải phòng xa:

        G8a  Chữ trên mỗi cảnh phải <= 14 từ. Anh Văn yêu cầu "ít chữ", và preset
             EXPLAINER của motion-video-brief-framework đặt ngưỡng này. Nếu không đo
             thì "ít chữ" chỉ là cảm giác.

        G8b  Không emoji làm biểu tượng, không ký tự đồng dạng (homoglyph). Ký tự
             Cyrillic trá hình đã 3 lần lọt vào repo (2 lần trong selector thật làm
             chết nút, 1 lần trong comment). tools/kiem_noi_dung.py quét theo mã
             Unicode nên bắt được cả loại mắt thường không phân biệt nổi.

        G8c  Không khai thời lượng gõ tay. Bản đầu ghi "110s ± 10%" trong khi
             TONG_MS thật là 91s (82,7%, ngoài khoảng chính nó tuyên bố).

        G8d  kichban.js phải nạp TRƯỚC app.js, vì app.js gọi window.MX_KICHBAN.init()
             khi bấm nút. Đảo thứ tự thì nút kịch bản im lặng không hoạt động.
        """
        kb_path = os.path.join(ROOT, "js", "kichban.js")
        idx_path = os.path.join(ROOT, "index.html")
        if not os.path.exists(kb_path):
            self.them("G8a", "kịch bản tồn tại", False, "thiếu js/kichban.js")
            return
        kb = doc("js/kichban.js")
        idx = doc("index.html")

        # G8a — độ dài caption mỗi cảnh, đo bằng regex trên mảng CANH
        caps = re.findall(r'caption\s*:\s*"([^"]*)"', kb)
        if not caps:
            self.them("G8a", "caption <= 14 từ", False, "không tìm thấy caption nào trong CANH")
        else:
            dai = [(c, len(c.split())) for c in caps if len(c.split()) > 14]
            trung_binh = round(sum(len(c.split()) for c in caps) / len(caps), 1)
            self.them("G8a", f"{len(caps)} caption <= 14 từ (TB {trung_binh} từ/cảnh)",
                      not dai,
                      "đạt" if not dai else f"{len(dai)} cảnh vượt: " +
                      "; ".join(f'"{c}" = {n} từ' for c, n in dai[:4]))

        # G8b — chạy tools/kiem_noi_dung.py làm cổng, không tự kiểm lại logic ở đây
        # LỖI ĐÃ SỬA (05/10, khi đóng gói cổng vào repo): bản đầu dò
        # os.path.dirname(ROOT) + "/tools/..." rồi mới tới một đường dẫn TUYỆT ĐỐI viết
        # cứng vào máy của tác giả. Cả hai chỗ đó đều trỏ RA NGOÀI repo, nên bản trong
        # repo chạy ở máy khác sẽ không tìm thấy tệp và cổng G8b im lặng mất hiệu lực.
        # Nay ưu tiên bản NẰM TRONG repo (ROOT/tools), chỉ rơi về bản ngoài nếu tệp
        # trong repo chưa được đồng bộ — và nói rõ đang dùng bản nào.
        tool = os.path.join(ROOT, "tools", "kiem_noi_dung.py")
        if not os.path.exists(tool):
            tool = os.path.join(os.path.dirname(ROOT), "tools", "kiem_noi_dung.py")
        try:
            r = subprocess.run([sys.executable, tool], capture_output=True, text=True, timeout=180)
            # LỖI ĐÃ SỬA TRONG CHÍNH PHÉP KIỂM NÀY (04/10): bản đầu đếm số dòng bắt đầu
            # bằng "·" trong output để ra số lỗi. Nhưng kiem_noi_dung.py chỉ in TỐI ĐA
            # 12 dòng mỗi phép rồi ghi "… và N lỗi nữa", nên G8b báo "12 lỗi" trong khi
            # con số thật là 40 — tức báo cáo THIẾU 70% số lỗi. Một cổng nghiệm thu mà
            # đếm sai số lỗi thì không dùng để quyết định được. Nay đọc đúng con số
            # TỔNG mà tool tự in ra, kèm phân rã theo từng phép K1/K2/K3.
            m = re.search(r"TỔNG:\s*(\d+)\s*lỗi", r.stdout)
            n_that = int(m.group(1)) if m else None
            nhom = re.findall(r"❌\s*(K\d[^:]*):\s*(\d+)\s*lỗi", r.stdout)
            mau = [l.strip() for l in r.stdout.splitlines() if l.strip().startswith("·")][:3]
            dat = (r.returncode == 0)
            self.them("G8b", "không emoji / không homoglyph (tools/kiem_noi_dung.py)", dat,
                      "đạt — 0 lỗi" if dat else
                      (f"{n_that if n_that is not None else '?'} lỗi "
                       f"[{'; '.join(f'{k.strip()}={v}' for k, v in nhom)}] "
                       + ("vd: " + " | ".join(x[:60] for x in mau) if mau else "")))
        except Exception as e:
            self.them("G8b", "không emoji / không homoglyph", False, f"{type(e).__name__}: {e}"[:120])

        # G8c — không khai thời lượng cứng cho NGƯỜI DÙNG xem.
        # SỬA LẠI CHO ĐÚNG BẢN CHẤT (04/10): bản đầu quét nguyên tệp kb + idx nên bắt
        # luôn chữ "110s" nằm trong COMMENT ghi chú lỗi cũ ("bản đầu ghi cứng 110s…").
        # Comment mô tả lịch sử KHÔNG phải tuyên bố với người xem; flag nó sẽ khiến
        # người sau phải xoá mất ghi chú bài học — hại nhiều hơn lợi. Nay chỉ quét
        # phần CHỮ HIỂN THỊ: bỏ <!-- --> trong HTML và bỏ /* */ + // trong JS.
        idx_hien = re.sub(r"<!--.*?-->", " ", idx, flags=re.S)
        kb_hien = re.sub(r"/\*.*?\*/", " ", kb, flags=re.S)
        kb_hien = re.sub(r"//[^\n]*", " ", kb_hien)
        cung = re.findall(r"\b(\d{2,3})\s*(?:giây|s\b)", idx_hien + "\n" + kb_hien)
        self.them("G8c", "thời lượng hiển thị lấy từ dữ liệu, không gõ tay",
                  not cung,
                  "đạt — không thấy số giây cứng trong nội dung hiển thị" if not cung else
                  f"thấy số giây gõ tay: {sorted(set(cung))} — phải để TONG_MS tự cộng từ dur")

        # G8d — thứ tự nạp script
        a, b = idx.find("js/kichban.js"), idx.find("js/app.js")
        self.them("G8d", "kichban.js nạp trước app.js",
                  a > -1 and b > -1 and a < b,
                  f"kichban @{a}, app @{b}" if (a > -1 and b > -1) else "thiếu một trong hai thẻ script")

        # G8e — section và nút phải có thật, nếu không thì kịch bản không mở được
        self.them("G8e", "có section #v-kichban + #kb-host + nút #btn-kichban",
                  all(x in idx for x in ('id="v-kichban"', 'id="kb-host"', 'id="btn-kichban"')),
                  "đạt" if all(x in idx for x in ('id="v-kichban"', 'id="kb-host"', 'id="btn-kichban"'))
                  else "thiếu một trong ba id — nút sẽ không mở được kịch bản")

    # ================= G9 — CHẾ ĐỘ ÍT CHỮ & BẢNG RESPONSIVE =================
    def g9(self):
        """Cổng G9, thêm 04/10 sau HAI BUG THẬT đo được ở 390px.

        G9a  Chế độ ít chữ không được ẩn phần tử CHỨC NĂNG.
             Bản đầu viết `body.it-chu .nho{display:none}` mà class .nho gắn trên 12 NÚT
             (kể cả chính nút #btn-it-chu), .tagline gắn trên #lbl-user và #nm-yccd,
             .legend là chú giải màu của biểu đồ. Bật ít chữ là mất nút tắt, mất mã học
             sinh, mất dòng "Yêu cầu cần đạt" và mất chú giải biểu đồ.
             Phép kiểm này đòi CSS phải có LƯỚI AN TOÀN liệt kê tường minh các phần tử
             đó với display:revert — không tin vào danh sách :not() vì dễ bị sửa hỏng.

        G9b  Ở màn hình hẹp, bảng phải tự cuộn ngang.
             Đo thật ở 390px: docW=425 > vw=390, 20 phần tử TRAN_NGANG, đều là <table>
             của Trạm 0 (4 cột) và bảng A/B Trạm 1 (5 cột). Nguyên nhân: table{width:100%}
             không chặn được độ rộng tối thiểu của nội dung. Giáo viên chiếu bằng điện
             thoại sẽ thấy chữ bị cắt mép phải.
        """
        css = doc("css/style.css")

        # G9a — lưới an toàn phải có đủ các phần tử chức năng
        can_co = ["body.it-chu button", "body.it-chu .btn", "body.it-chu .chip",
                  "body.it-chu .legend", "body.it-chu .phanhoi", "body.it-chu #lbl-user",
                  "body.it-chu #nm-yccd"]
        thieu = [c for c in can_co if c not in css]
        m = re.search(r"body\.it-chu button[^{]*\{([^}]*)\}", css)
        co_revert = bool(m and re.search(r"display\s*:\s*revert", m.group(1)))
        self.them("G9a", "ít chữ không ẩn phần tử chức năng (nút/chip/legend/lbl-user/yccd)",
                  not thieu and co_revert,
                  ("lưới an toàn đủ " + str(len(can_co)) + " selector + display:revert")
                  if (not thieu and co_revert) else
                  ("thiếu selector: " + str(thieu) if thieu
                   else "có selector nhưng KHÔNG có display:revert"))

        # G9b — media query hẹp phải cho bảng cuộn ngang
        mq = re.findall(r"@media\s*\(max-width:\s*(\d+)px\)\s*\{(.*?)\n\}", css, re.S)
        hep = [(int(w), b) for w, b in mq if int(w) <= 640]
        ok_bang = False
        for w, b in hep:
            if re.search(r"table\s*\{[^}]*display\s*:\s*block", b) and \
               re.search(r"table\s*\{[^}]*overflow-x\s*:\s*auto", b):
                ok_bang = True
                break
        self.them("G9b", "bảng tự cuộn ngang ở màn hình <=640px", ok_bang,
                  ("tìm thấy table{display:block;overflow-x:auto} trong @" + str(hep[0][0]) + "px")
                  if ok_bang else
                  ("không thấy quy tắc bảng cuộn ngang trong media query hẹp; "
                   "các media query hiện có: " + str([w for w, _ in mq])))

    # ============ G10 — NGÔN NGỮ: không tiếp thị trong giao diện học sinh ============
    def g10(self):
        r"""Cổng G10, thêm 05/10 theo chỉ đạo anh Văn: "mấy cái chữ tâng bốc này bỏ đi,
        cứ tập trung vào mục đích là sản phẩm để học trò học về AI".

        PHẠM VI HẸP VÀ CÓ LÍ DO — đây là chỗ dễ làm hỏng nhất nếu quét rộng:
          Chỉ quét index.html, data/meta.js, js/kichban.js, js/app.js — tức khung giao
          diện và lời kịch bản. KHÔNG quét data/cauhoi*.js và js/tinhhuong.js, vì hai
          nơi đó chứa claim SAI có chủ đích để học sinh bắt lỗi, ví dụ "học sinh miền
          Trung luôn giỏi tư duy thuật toán hơn hẳn học sinh miền Bắc" (thiên kiến vùng
          miền cài sẵn) hay "dịch máy đạt 99,27%" (số liệu bịa cài sẵn). Quét chúng sẽ
          báo lỗi và dẫn tới sửa mất nội dung bài học. Nên danh sách tệp là TƯỜNG MINH.

          Cùng lí do đó, từ cấm phải là CẢ CỤM chứ không phải một từ đơn. Quét từ đơn
          "hoàn toàn" sẽ bắt oan câu "một số câu hoàn toàn đúng" ở index.html:212 — đó
          là nội dung dạy học sinh phân biệt câu đúng với câu có lỗi.

        G10a  ngôn ngữ tiếp thị đã loại bỏ không được quay lại
        G10b  tên hiển thị là định danh môn/lớp, không phải khẩu hiệu
        G10c  khẩu hiệu cũ "Soi AI để hiểu AI" = 0 trong mã sống (comment ghi chú được phép)
        G10d  phiên bản ở chân trang và trong data/meta.js phải khớp
        G10e  kịch bản không nói sai số trạm (đã từng ghi "9 trạm" trong khi nhà máy có 7)
        """
        idx = doc("index.html")
        meta = doc("data/meta.js")
        kb = doc("js/kichban.js")

        def chu_hien_thi(s):
            """Chỉ giữ chữ người dùng đọc: bỏ thẻ, bỏ comment HTML."""
            s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
            s = re.sub(r"<[^>]*>", " ", s)
            return s

        idx_txt = chu_hien_thi(idx)

        # (nhóm, [cụm từ cấm]) — đều là cụm, không có từ đơn, để không bắt oan nội dung dạy học
        CAM = [
            ("so sánh với sản phẩm khác",
             ["khác các ứng dụng", "khác các công cụ", "hơn hẳn các công cụ"]),
            ("tính từ tuyệt đối / tự khen",
             ["Tiếng Việt hoàn toàn", "tuyệt vời", "duy nhất trên thị trường",
              "đẳng cấp", "số một"]),
            ("tiếp thị giá và đối tác",
             ["không thu phí", "nhà cung cấp", "miễn phí hoàn toàn"]),
            ("giải thưởng trong giao diện học sinh",
             ["dự thi", "Giải thưởng Tiên phong", "Bảng B"]),
            ("lợi ích giáo viên đặt ở chỗ học sinh đọc",
             ["thầy/cô không phải chấm", "giáo viên không phải chấm"]),
            ("khẩu hiệu",
             ["Soi AI để hiểu AI", "không hỏi AI"]),
        ]
        vi_pham = []
        for nhom, tus in CAM:
            for t in tus:
                n = idx_txt.count(t)
                if n:
                    vi_pham.append(nhom + ": '" + t + "' x" + str(n))
        self.them("G10a", "không còn ngôn ngữ tiếp thị trong index.html (6 nhóm, 17 cụm)",
                  not vi_pham,
                  "; ".join(vi_pham) if vi_pham else "sạch cả 6 nhóm")

        TEN = "Phòng thực hành Trí tuệ nhân tạo lớp 10"
        du = (TEN in idx) and (TEN in meta)
        self.them("G10b", "tên hiển thị là định danh môn/lớp", du,
                  "có trong index.html và data/meta.js" if du
                  else "thiếu ở index.html hoặc data/meta.js")

        # G10c: khẩu hiệu cũ — bỏ comment rồi mới đếm, vì comment ghi lại bài học là hợp lệ
        khau = "Soi AI để hiểu AI"
        con = 0
        for ten_f in ("index.html", "data/meta.js", "js/kichban.js", "js/app.js"):
            s = doc(ten_f)
            s = re.sub(r"/\*.*?\*/", " ", s, flags=re.S)
            s = re.sub(r"//[^\n]*", " ", s)
            s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
            con += s.count(khau)
        self.them("G10c", "khẩu hiệu cũ = 0 trong mã sống", con == 0,
                  "sạch" if con == 0 else "còn " + str(con) + " chỗ")

        m_footer = re.search(r"Phiên bản\s+([\d.]+)", idx)
        m_meta = re.search(r'phienBan\s*:\s*"([\d.]+)"', meta)
        v1 = m_footer.group(1) if m_footer else None
        v2 = m_meta.group(1) if m_meta else None
        self.them("G10d", "phiên bản chân trang khớp data/meta.js",
                  v1 is not None and v1 == v2,
                  "chân trang " + str(v1) + " / meta.js " + str(v2))

        self.them("G10e", "kịch bản ghi đúng số trạm của nhà máy",
                  ("9 trạm" not in kb) and ("7 trạm" in kb),
                  "đúng: 7 trạm" if "9 trạm" not in kb
                  else "sai: vẫn ghi '9 trạm' (nhà máy có 7 trạm, kịch bản có 9 cảnh)")

    # ============ G11 HAI MODULE MỨC 3 MỚI (bt13.js, bt09.js) ============
    def g11(self):
        """Cổng G11, thêm 05/10/2026 theo phát hiện của reviewer độc lập trên PR #1.

        Reviewer chạy `grep -c "bt13.js" tools/nghiem_thu.py` và `grep -c "bt09.js" …`
        — cả hai trả 0. Nghĩa là hai tệp mới thêm vào sản phẩm, trong đó có gọi
        innerHTML và có gọi icon, KHÔNG được cổng nào kiểm. Một tệp không nằm trong
        cổng thì mọi lỗi trong nó đều được tính là "đã kiểm" theo nghĩa sai.

        Bốn phép kiểm, mỗi phép sinh từ một lớp lỗi THẬT đã xảy ra trong repo này:
          G11a  nạp trong index.html và nạp TRƯỚC app.js — vì app.js gọi init() của
                cả hai; nạp sau là ReferenceError lúc bấm nút.
          G11b  mọi svgIco("tên") trong MÃ SỐNG phải trỏ tới symbol có thật — đúng
                lớp lỗi đã xảy ra ở js/duDoan.js với svgIco("target"), và phải đếm
                trên mã sống vì comment cũng chứa chuỗi ấy.
          G11c  KHÔNG có biến chứa chữ học sinh (.value) nào đi vào innerHTML — đây
                là điều cả hai tệp khẳng định trong ghi chú; phép kiểm bắt khẳng định
                đó phải tự chứng minh được, không tin lời ghi chú.
          G11d  con số "N chỗ innerHTML" ghi trong comment của mỗi tệp phải KHỚP số
                đếm thật. Phép kiểm này bắt được lỗi thật ngay lần chạy đầu: bt13.js
                ghi 8 trong khi mã sống có 9, bt09.js ghi 7 trong khi có 10.
        """
        print("\n=== G11 CÁC MODULE MỨC 3 (bt13.js, bt09.js, muc3.js) ===")
        idx = doc("index.html")
        sprite = set(re.findall(r'symbol id="(i-[\w-]+)"', idx))
        MODULE = ["js/bt13.js", "js/bt09.js", "js/muc3.js"]

        # ---- G11a: nạp trong index.html, TRƯỚC app.js ----
        vi_tri = {m.group(1): m.start() for m in re.finditer(r'<script src="([^"]+)"', idx)}
        app_pos = vi_tri.get("js/app.js")
        thieu_nap = [f for f in MODULE if f not in vi_tri]
        sau_app = [f for f in MODULE
                   if f in vi_tri and app_pos is not None and vi_tri[f] > app_pos]
        self.them("G11a", "bt13.js + bt09.js + muc3.js nạp trong index.html TRƯỚC app.js",
                  not thieu_nap and not sau_app,
                  (f"thiếu trong index.html: {thieu_nap}" if thieu_nap else
                   (f"nạp SAU app.js: {sau_app}" if sau_app else
                    f"{len(MODULE)} tệp, thứ tự đúng (app.js @{app_pos})")))

        # ---- G11b (MỌI js/*.js) + G11c + G11d (2 module mới) ----
        # VÌ SAO MỞ RỘNG RA MỌI TỆP js (05/10, reviewer độc lập chỉ ra tiếp sau lần vá
        # đầu): bản đầu của G11b chỉ phủ js/bt13.js và js/bt09.js. Nhưng lớp lỗi
        # "svgIco gọi tên không có trong sprite" đã TỪNG XẢY RA THẬT ở js/duDoan.js với
        # svgIco("target") — một tệp KHÔNG nằm trong 2 module mới. Một cổng bắt được
        # đúng 1 ca mà không bắt được LỚP lỗi thì lần sau lỗi tái sinh ở tệp khác là
        # cổng lại mù, và cảnh báo "đã kiểm" trở thành sai. Nay quét toàn bộ js/*.js.
        tat_ca_js = sorted("js/" + x
                           for x in os.listdir(os.path.join(ROOT, "js"))
                           if x.endswith(".js"))
        ten_icon_moi_tep = {}
        mo_coi_toan_bo = []
        for f in tat_ca_js:
            song_f = than_ma_song(doc(f))
            ten_f = set(re.findall(r'svgIco\(\s*"([\w-]+)"\s*\)', song_f))
            if not ten_f:
                continue
            ten_icon_moi_tep[f] = ten_f
            xau_f = sorted(t for t in ten_f if ("i-" + t) not in sprite)
            if xau_f:
                mo_coi_toan_bo.append(f"{f}: {xau_f}")

        tong_icon, tong_css = sum(len(v) for v in ten_icon_moi_tep.values()), 0
        van_de = []
        # Danh sách RIÊNG cho G11c. VÌ SAO KHÔNG DÙNG LẠI `van_de`: bản trước kiểm
        # `any("đi vào innerHTML" in v for v in van_de)` — tức nó suy lại "có phát hiện
        # không" từ CÂU CHỮ của thông báo. Khi thông báo đổi chữ (thêm "thẳng", đổi sang
        # "nội suy ${...}"), 2 trong 3 đường phát hiện vẫn chạy đúng nhưng dòng lọc không
        # còn khớp, nên cổng in ĐẠT trong khi đã tìm thấy lỗi — một âm tính giả ở tầng
        # BÁO CÁO, nguy hiểm hơn cả việc dò sót, vì cổng trông vẫn xanh. Cách chữa không
        # phải là đồng bộ câu chữ, mà là ĐỪNG suy lại từ câu chữ: ghi phát hiện vào một
        # danh sách riêng và kiểm chính danh sách đó.
        xau_c_toan_bo = []
        for f in MODULE:
            raw = doc(f)
            song = than_ma_song(raw)

            # G11c — chữ học sinh không được đi vào innerHTML
            # VÌ SAO VIẾT LẠI (05/10): bản cũ chỉ bắt được biến gán từ `.value` khi nó
            # xuất hiện KÈM DẤU `+` hai bên, và có một nhánh CHẾT:
            #   `re.fullmatch(r"\s*=\s*" + b + r"\s*;", seg)`
            # — `seg` được cắt từ SAU dấu `=` (dau = m.end()), nên nhánh này không bao giờ
            # khớp. Đo trên 8 đoạn mã mẫu: bản cũ MISS cả 5 dạng nguy hiểm, trong đó có
            # dạng trực tiếp `el.innerHTML = inp.value` — dạng DỄ xảy ra nhất khi viết ẩu.
            # Cổng vẫn in "0 chỗ chèn biến .value" nên trông như đang canh, thực ra là mù.
            # Bản mới bắt 3 đường: (a) `.value` đứng thẳng trong biểu thức; (b) biến gán từ
            # `.value` xuất hiện ở BẤT KỲ vị trí nào trong biểu thức (không đòi dấu `+`);
            # (c) nội suy `${...}` trong template literal chứa một trong hai thứ trên.
            bien = bien_chua_chu_hoc_sinh(song)
            xau = []
            for m in re.finditer(r"\.innerHTML\s*=", song):
                dau = m.end()
                cuoi = song.find(";", dau)
                if cuoi < 0 or cuoi - dau > 600:
                    cuoi = min(dau + 600, len(song))
                seg = song[dau:cuoi + 1]
                dong = song[:m.start()].count("\n") + 1

                # (a) `.value` đứng thẳng: el.innerHTML = inp.value
                if re.search(r"\.value\b", seg):
                    xau.append(f"{f}:{dong} giá trị .value đi thẳng vào innerHTML")

                # (b) biến gán từ `.value`, ở bất kỳ vị trí nào trong biểu thức.
                # `\b` để `t` không khớp trong `text`; loại trừ tên nằm ngay sau dấu `.`
                # (thuộc tính `obj.t`) vì đó không phải biến cục bộ.
                for b in bien:
                    if re.search(r"(?<![\w.])" + re.escape(b) + r"\b", seg):
                        xau.append(f"{f}:{dong} biến '{b}' (gán từ .value) đi vào innerHTML")

                # (c) nội suy template literal chứa .value hoặc biến chữ.
                for t in re.findall(r"\$\{([^}]*)\}", seg):
                    if re.search(r"\.value\b", t) or \
                       any(re.search(r"(?<![\w.])" + re.escape(b) + r"\b", t) for b in bien):
                        xau.append(f"{f}:{dong} nội suy ${{...}} chứa chữ học sinh: {t.strip()[:40]}")

            tong_css += len(re.findall(r"\.innerHTML\s*=", song))

            # G11d — con số ghi trong comment phải khớp số đếm thật
            # NHÁNH BỔ SUNG (05/10, khi thêm js/muc3.js): tệp KHÔNG có chỗ gán innerHTML
            # nào thì KHÔNG có gì để khai báo. muc3.js dựng toàn bộ giao diện qua
            # MX_DUDOAN nên n_that = 0 và không có dòng "**N chỗ**" — bản cũ sẽ báo LỖI
            # "không tìm thấy con số", tức phạt một tệp vì nó SẠCH hơn yêu cầu. Đó là
            # dương tính giả cùng họ với vụ grep trúng comment ở G11b.
            n_that = len(re.findall(r"\.innerHTML\s*=", song))
            m_khai = re.search(r"\*\*(\d+)\s*chỗ\*\*", raw)
            khai = int(m_khai.group(1)) if m_khai else None
            if n_that == 0 and khai is None:
                pass                                   # không có gì để khai → không có gì để sai
            elif khai is None:
                van_de.append(f"{f}: có {n_that} chỗ innerHTML nhưng ghi chú không khai số")
            elif khai != n_that:
                van_de.append(f"{f}: ghi chú khai {khai} chỗ, mã sống có {n_that} chỗ")

            van_de.extend(xau)
            xau_c_toan_bo.extend(xau)      # G11c kiểm danh sách này, không kiểm câu chữ

        ten_khac_nhau = set().union(*ten_icon_moi_tep.values()) if ten_icon_moi_tep else set()
        self.them("G11b", "mọi svgIco trong MỌI js/*.js trỏ symbol có thật (đếm trên mã sống)",
                  not mo_coi_toan_bo,
                  f"{len(tat_ca_js)} tệp js đã quét · {tong_icon} lượt gọi "
                  f"({len(ten_khac_nhau)} tên khác nhau) · {len(sprite)} symbol · 0 mồ côi"
                  if not mo_coi_toan_bo
                  else "; ".join(mo_coi_toan_bo))
        self.them("G11c", "chữ học sinh KHÔNG đi vào innerHTML (bt13/bt09/muc3)",
                  not xau_c_toan_bo,
                  f"{tong_css} chỗ innerHTML đã rà trong {len(MODULE)} module, 0 chỗ chèn chữ "
                  f"học sinh (3 đường: .value thẳng, biến gán từ .value, nội suy ${{...}})"
                  if not xau_c_toan_bo
                  else "; ".join(xau_c_toan_bo))
        self.them("G11d", "con số innerHTML ghi trong ghi chú khớp mã sống "
                          "(hoặc không khai vì tệp không dùng innerHTML)",
                  not any(("ghi chú khai" in v or "không khai số" in v
                           or "không tìm thấy con số" in v) for v in van_de),
                  f"số ghi chú = số đo được ở {len(MODULE)} module"
                  if not any(("ghi chú khai" in v or "không khai số" in v
                              or "không tìm thấy con số" in v) for v in van_de)
                  else "; ".join(v for v in van_de
                                 if "ghi chú khai" in v or "không khai số" in v
                                 or "không tìm thấy con số" in v))

        # ---- G11e: host id của các module Mức 3 phải có trong index.html ----
        # Thiếu sót #2 reviewer nêu: cổng cũ không nhắc tới kt-bt13 / dt-bt09. Đây là chỗ
        # app.js gắn kết quả của module vào trang. Một trong hai bị đổi tên hoặc bị xoá
        # thì module chạy xong mà KHÔNG hiện gì — im lặng, không exception, nên không phép
        # kiểm runtime nào bắt được. Cổng tĩnh là chỗ duy nhất bắt được nó.
        # MỞ RỘNG (05/10): thêm bảy host id của js/muc3.js. Nguồn danh sách KHÔNG gõ tay —
        # đọc từ chính các lời gọi `.mo("BT-xx", $("host"), ...)` trong app.js, nên thêm ô
        # mới mà quên host id thì cổng tự biết. Và phải khớp cả hai chiều: mỗi host id
        # trong app.js phải có trong HTML, VÀ mỗi host id của muc3 phải được app.js dùng.
        host = {"js/bt13.js": "kt-bt13", "js/bt09.js": "dt-bt09"}
        thieu_host = [f"{f} -> #{i}" for f, i in host.items() if f'id="{i}"' not in idx]
        app_js = than_ma_song(doc("js/app.js"))
        goi_mo = dict(re.findall(r'\.mo\(\s*"(BT-\d{2})"\s*,\s*\$\("([\w-]+)"\)', app_js))
        thieu_m3 = [f"{ma} -> #{hid}" for ma, hid in goi_mo.items()
                    if f'id="{hid}"' not in idx]
        self.them("G11e", f"host id trong index.html cho {len(host) + len(goi_mo)} ô Mức 3",
                  not thieu_host and not thieu_m3,
                  f"{len(host)} host cũ + {len(goi_mo)} host muc3 ({sorted(goi_mo)}) đều có trong HTML"
                  if not thieu_host and not thieu_m3
                  else "thiếu: " + "; ".join(thieu_host + thieu_m3))

        # ---- G11f MỚI: mọi hàm MX_MUC3.* mà app.js gọi phải tồn tại thật ----
        # Lớp lỗi này đã TỪNG xảy ra ở js/duDoan.js (svgIco("target")) và ở G11a: gọi một
        # tên không tồn tại, khác ở chỗ lỗi đó nằm im cho tới khi người dùng bấm nút. Với
        # bảy ô mới, tên hàm được gọi từ tệp KHÁC (app.js gọi M3().mo / M3().cham), nên nếu
        # muc3.js đổi tên hàm thì app.js trỏ vào hư không mà không cổng nào biết.
        m3_js = than_ma_song(doc("js/muc3.js"))
        xuat = set()
        m_api = re.search(r"window\.MX_MUC3\s*=\s*\{(.*?)\};", m3_js, re.S)
        if m_api:
            # VÌ SAO KHÔNG DÙNG `(\w+)\s*[,:]` NHƯ BẢN ĐẦU: bản đầu bỏ sót hàm viết dạng
            # shorthand `ghiLog(fn){ ... }` — JS hợp lệ, nhưng không có dấu `:` nên regex
            # cũ không thấy, và cổng báo oan "app.js gọi hàm KHÔNG tồn tại: ['ghiLog']"
            # trong khi hàm CÓ thật. Đây là dương tính giả thứ hai cùng họ với vụ grep
            # trúng comment ở G11b: phép kiểm tự nó viết sai, rồi buộc tội mã đúng.
            # BẢN 2 (05/10, sau khi bản 1 báo oan `cham`): bản 1 dùng `(?:^|,)\s*(\w+)\s*[(:,{]`
            # — regex TIÊU THỤ dấu `,` phân cách, mà findall lại không chồng lấn, nên trong
            # `mo, cham, DS:` thì dấu `,` sau `mo` bị ăn mất và `cham` không còn dấu đứng
            # trước để khớp → cổng vu oan cho hàm CÓ thật. Sửa bằng cách để dấu phân cách
            # nằm trong LOOKAHEAD (không tiêu thụ), nhờ đó mọi khoá đều còn dấu trước nó.
            # Vẫn giữ ràng buộc "khoá phải đứng đầu dòng hoặc sau `,`/`{`" nên không nuốt
            # tên hàm nằm trong biểu thức (vd `keys` trong `Object.keys(BANG)`).
            xuat = set(re.findall(r'(?:^|[,{])\s*(\w+)\s*(?=[(:,{])', m_api.group(1), re.M))
        goi = set(re.findall(r"M3\(\)\.(\w+)", app_js))
        thieu_ham = sorted(h for h in goi if h not in xuat)
        self.them("G11f", "mọi hàm MX_MUC3.* mà app.js gọi đều có thật trong muc3.js",
                  not thieu_ham,
                  f"app.js gọi {sorted(goi)} · muc3.js xuất {sorted(xuat)} · khớp hết"
                  if not thieu_ham else f"app.js gọi hàm KHÔNG tồn tại: {thieu_ham}")

    def tong_ket(self):
        print("\n" + "=" * 72)
        dat = sum(1 for k in self.kq if k["dat"])
        loi = [k for k in self.kq if not k["dat"]]
        print(f"KẾT QUẢ: {dat}/{len(self.kq)} tiêu chí đạt")
        if loi:
            print("CÒN LỖI:")
            for k in loi:
                print(f"  ✗ {k['ma']} {k['ten']} — {k['chi_tiet'][:150]}")
        byG = {}
        for k in self.kq:
            g = k["ma"].rstrip("abcdefgh")
            byG.setdefault(g, [0, 0])
            byG[g][0] += k["dat"]
            byG[g][1] += 1
        print("Theo nhóm:", " · ".join(f"{g}:{v[0]}/{v[1]}" for g, v in sorted(byG.items())))
        print("=" * 72)

        # ---- GHI TỆP BẰNG CHỨNG — CHỈ KHI CHẠY ĐẦY ĐỦ ----
        # BUG ĐÃ SỬA (05/10), loại im lặng và nguy hiểm: bản cũ ghi đè judge_result.json
        # ở MỌI lần chạy, kể cả `nghiem_thu.py G11` (chạy đúng MỘT nhóm). Hậu quả thật:
        # sau khi chạy lọc 1 nhóm, tệp bằng chứng chỉ còn 5 mục, và công cụ cập nhật
        # Google Sheet đọc tệp đó rồi định ghi "Tiêu chí đạt = 5/5" trong khi cổng thật
        # là 52/52. Không có thông báo lỗi nào — tệp vẫn đúng định dạng, chỉ sai nội
        # dung. Đây đúng lớp lỗi "số đúng định dạng nhưng của bản khác" phải chặn ở gốc.
        # LUẬT: lần chạy LỌC không được phép ghi tệp bằng chứng; mọi tệp bằng chứng phải
        # kèm sidecar meta để bên đọc TỪ CHỐI ĐƯỢC nếu nó là bản phần.
        BC = os.path.join(ROOT, "out", "judge_result.json")
        META = os.path.join(ROOT, "out", "judge_result.meta.json")
        os.makedirs(os.path.dirname(BC), exist_ok=True)
        if self.day_du:
            json.dump(self.kq, open(BC, "w"), ensure_ascii=False, indent=1)
            commit = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"],
                                    capture_output=True, text=True).stdout.strip()[:12]
            json.dump({
                "day_du": True,
                "nhom_da_chay": self.nhom_da_chay,
                "so_tieu_chi": len(self.kq),
                "so_dat": dat,
                "commit": commit,
                "luc": datetime.datetime.now().isoformat(timespec="seconds"),
            }, open(META, "w"), ensure_ascii=False, indent=1)
            print(f"Đã ghi bằng chứng: judge_result.json ({len(self.kq)} tiêu chí) "
                  f"+ judge_result.meta.json (commit {commit})")
        else:
            print(f"KHÔNG ghi judge_result.json — lần chạy này LỌC nhóm "
                  f"{self.nhom_da_chay}, không phải chạy đầy đủ.")
            print("  Lý do: tệp bằng chứng phần sẽ làm mọi báo cáo đọc nó bị sai âm thầm.")
            print("  Muốn cập nhật bằng chứng: chạy `python3 tools/nghiem_thu.py` không đối số.")
        return 0 if not loi else 1


def main():
    j = Judge()
    chi = [a.upper() for a in sys.argv[1:]]
    NHOM = ["G1", "G2", "G3", "G4", "G6", "G7", "G8", "G9", "G10", "G11"]
    j.nhom_da_chay = [g for g in NHOM if not chi or g in chi]
    # Chỉ coi là chạy ĐẦY ĐỦ khi không lọc nhóm nào. Lần chạy lọc (vd `nghiem_thu.py G11`)
    # KHÔNG được ghi tệp bằng chứng — xem giải thích ở tong_ket.
    j.day_du = not chi and j.nhom_da_chay == NHOM
    for g in NHOM:
        if not chi or g in chi:
            getattr(j, g.lower())()
    return j.tong_ket()


if __name__ == "__main__":
    sys.exit(main())
