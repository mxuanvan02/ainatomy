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
import datetime, hashlib, json, os, re, subprocess, sys, urllib.request, urllib.parse

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


def html_song(idx):
    """Bỏ chú thích `<!-- ... -->` khỏi HTML để chỉ còn MÃ SỐNG.

    Cùng một bài học với than_ma_song(), nhưng cho HTML — và phải trả giá hai lần mới học được.

    LẦN MỘT (báo OAN): cổng G8d đo thứ tự nạp script bằng `idx.find("js/app.js")`. Tôi viết một
    chú thích HTML có nhắc tới đường dẫn đó; find() bắt đúng chữ trong chú thích ở vị trí 7811
    trong khi thẻ <script> thật nằm ở 44048, nên cổng kết luận sai rằng app.js nạp trước
    kichban.js. Sản phẩm không hỏng, phép kiểm hỏng.

    LẦN HAI (nghiêm trọng hơn — ĐẠT GIẢ): các cổng kiểm "có tồn tại không" bằng
    `f'id="{i}"' not in idx`. Chỉ cần một chú thích nào đó viết ra chuỗi `id="kt-bt13"` là cổng
    ĐẠT dù THẺ THẬT ĐÃ BỊ XOÁ. Báo oan thì còn có người đi cãi; đạt giả thì không ai kiểm lại,
    và lỗ hổng nằm im cho tới lúc học sinh bấm nút không thấy gì.

    Nên mọi phép kiểm sự tồn tại của MÃ trong HTML phải chạy trên bản đã lột chú thích.
    """
    return re.sub(r"<!--.*?-->", " ", idx, flags=re.S)


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
        # html_song(): kiểm "có tồn tại không" phải chạy trên MÃ SỐNG. Một dòng chú thích chứa
        # `symbol id="i-xxx"` hay `<use href="#i-xxx">` sẽ làm cổng ĐẠT khi thẻ thật đã bị xoá.
        idx = html_song(doc("index.html"))
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
            # html_song(): đây là kiểm THẺ NẠP MODULE, tức kiểm mã, nên phải chạy trên bản đã
            # lột chú thích. Nếu không thì một dòng chú thích viết `src="js/nhamay_tram01.js"`
            # (ví dụ để giải thích) đủ làm cổng ĐẠT dù thẻ thật đã bị xoá — và module biến mất
            # thì Trạm 0/1 chết im lặng, không exception nào.
            nap = 'src="js/nhamay_tram01.js"' in html_song(doc("index.html"))
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
        # html_song(): chiều ngược lại của đạt giả — một chú thích ghi ví dụ URL CDN
        # (`<!-- không nạp từ https://fonts.googleapis.com -->`) sẽ làm cổng BÁO OAN là có CDN.
        idx = html_song(doc("index.html"))
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
        # `idx` giữ nguyên BẢN THÔ: một số phép kiểm cần đúng văn bản đầy đủ.
        # `idx_song` = index.html ĐÃ LỘT CHÚ THÍCH. Mọi phép kiểm "có tồn tại không" trên tệp
        # HTML phải chạy trên biến này, KHÔNG chạy trên `idx`.
        # (Bản vá đầu tiên đã XOÁ luôn dòng `idx = doc(...)` khi thêm `idx_song`, làm idx thành
        # undefined ở năm chỗ phía dưới — cổng chết bằng NameError. Khi thêm một biến "đã làm
        # sạch" thì phải giữ biến gốc, không thay thế nó.)
        idx = doc("index.html")
        # VÌ SAO: HTML có <!-- chú thích -->, và các chuỗi kiểm tra ở đây đều là mã nguồn
        # (id="...", <script src="...">) — thứ hoàn toàn có thể xuất hiện trong chú thích để
        # giải thích. Kiểm trên tệp thô thì một dòng chú thích cũng làm cổng ĐẠT khi thẻ thật
        # đã bị xoá: đó là ĐẠT GIẢ, và nó nguy hiểm hơn báo oan vì không ai đi kiểm tra lại.
        # G8d vừa bị chính lỗi này ở chiều ngược lại (find() bắt chữ trong chú thích rồi báo
        # sai thứ tự nạp script). Cùng một gốc: đọc tệp thô thay vì đọc mã sống.
        idx_song = html_song(idx)

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
        # `idx_hien` từng là một phép re.sub riêng y hệt html_song(), tạo ra BIẾN THỨ HAI cùng
        # nghĩa ngay trong hàm đã có `idx_song` (dòng trên). Hai bản sao của một phép làm sạch
        # thì sớm muộn cũng lệch nhau và không ai biết bản nào đang được dùng. Nay dùng chung.
        idx_hien = idx_song
        kb_hien = re.sub(r"/\*.*?\*/", " ", kb, flags=re.S)
        kb_hien = re.sub(r"//[^\n]*", " ", kb_hien)
        cung = re.findall(r"\b(\d{2,3})\s*(?:giây|s\b)", idx_hien + "\n" + kb_hien)
        self.them("G8c", "thời lượng hiển thị lấy từ dữ liệu, không gõ tay",
                  not cung,
                  "đạt — không thấy số giây cứng trong nội dung hiển thị" if not cung else
                  f"thấy số giây gõ tay: {sorted(set(cung))} — phải để TONG_MS tự cộng từ dur")

        # G8d — thứ tự nạp script.
        #
        # SỬA 07/10 — DƯƠNG TÍNH GIẢ, và chính tôi vừa gây ra nó. Bản cũ dùng
        # `idx.find("js/app.js")`, tức tìm lần xuất hiện ĐẦU TIÊN của chuỗi đó ở BẤT KỲ đâu
        # trong tệp. Tôi thêm một chú thích HTML giải thích phần tử chết #btn-dangnhap, và trong
        # chú thích có viết "được gắn ở js/app.js" — find() bắt đúng chữ đó ở vị trí 7811, trong
        # khi thẻ <script src="js/app.js"> THẬT nằm ở 44048 (kichban.js ở 43795, tức vẫn nạp
        # trước đúng như thiết kế). Cổng in "kichban @43795, app @7811" rồi kết luận sai rằng
        # app.js nạp trước. SẢN PHẨM KHÔNG HỎNG; PHÉP KIỂM HỎNG.
        #
        # Đây CHÍNH XÁC là lớp lỗi mà G11b đã ghi lại trong dự án: "phép grep thô trên tệp còn
        # comment sẽ khớp cả CHỮ TRONG GHI CHÚ ... đó là dương tính giả toàn tập: nó khiến người
        # đọc đi sửa thứ không hỏng, và tệ nhất là làm mất lòng tin vào các cảnh báo thật".
        # G11a cũng đã dùng cách đúng — re.finditer trên thẻ <script src="...">. G8d là chỗ sót
        # lại cuối cùng còn dùng find() thô.
        #
        # VÌ SAO SỬA CỔNG CHỨ KHÔNG SỬA CHÚ THÍCH: nếu tôi chỉ đổi chữ trong chú thích thì cổng
        # vẫn mù — lần sau bất kỳ ai (kể cả tôi) viết một dòng chú thích nhắc tới đường dẫn tệp
        # là cổng lại báo oan. Sửa chỗ đo thì lỗi không tái diễn được. Và chính dòng chú thích
        # đang nằm trong index.html lúc này trở thành phép thử thường trực cho bản sửa: nó có chữ
        # "js/app.js" ở vị trí 7811, nên nếu G8d còn đọc chữ trong comment thì nó sẽ FAIL ngay.
        # Đọc trên idx_song, KHÔNG đọc idx thô. Regex này đòi cả thẻ `<script src="...">` nên
        # hiện tại chưa bị chú thích đánh lừa, nhưng đó là ăn may chứ không phải an toàn: chỉ cần
        # một chú thích nào đó chép nguyên văn thẻ script (rất dễ xảy ra khi viết tài liệu hướng
        # dẫn ngay trong HTML) là cổng đo sai thứ tự nạp. Đã xảy ra một lần với bản find() thô.
        vi_tri = {m.group(1): m.start()
                  for m in re.finditer(r'<script\s+src="([^"]+)"', idx_song)}
        a, b = vi_tri.get("js/kichban.js", -1), vi_tri.get("js/app.js", -1)
        self.them("G8d", "kichban.js nạp trước app.js",
                  a > -1 and b > -1 and a < b,
                  f"kichban @{a}, app @{b} (đọc từ thẻ <script src>, không đọc chữ trong chú thích)"
                  if (a > -1 and b > -1)
                  else f"thiếu một trong hai THẺ SCRIPT thật: kichban={a}, app={b}")

        # G8e — section và nút phải có thật, nếu không thì kịch bản không mở được.
        # Kiểm trên idx_song (đã lột chú thích): một dòng chú thích nhắc tới `id="kb-host"`
        # không được phép làm cổng ĐẠT khi thẻ thật đã bị xoá — đó là đạt giả.
        self.them("G8e", "có section #v-kichban + #kb-host + nút #btn-kichban",
                  all(x in idx_song for x in ('id="v-kichban"', 'id="kb-host"', 'id="btn-kichban"')),
                  "đạt" if all(x in idx_song for x in ('id="v-kichban"', 'id="kb-host"', 'id="btn-kichban"'))
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
        # html_song(): tên này phải là chữ HIỂN THỊ thật, không phải chữ nằm trong chú thích.
        du = (TEN in html_song(idx)) and (TEN in meta)
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

        # G10d so CHỮ HIỂN THỊ ở chân trang với data/meta.js, nên phải đọc idx_txt (đã lột cả
        # chú thích lẫn thẻ) chứ không phải idx thô. Đọc thô thì một chú thích nhắc
        # "Phiên bản 1.0.0" sẽ được coi là chữ chân trang — và nếu chân trang thật đã đổi phiên
        # bản mà quên sửa meta.js thì cổng vẫn ĐẠT, tức bỏ lọt đúng lỗi nó sinh ra để bắt.
        m_footer = re.search(r"Phiên bản\s+([\d.]+)", idx_txt)
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
        # html_song(): G11a so thứ tự nạp script và G11e kiểm host id có thật. Cả hai đều là
        # kiểm MÃ, nên phải chạy trên bản đã lột chú thích — nếu không thì một chú thích chứa
        # `<script src="js/app.js">` hay `id="kt-bt13"` đủ để cổng ĐẠT giả.
        # Lưu ý: html_song thay mỗi chú thích bằng MỘT khoảng trắng nên offset tuyệt đối sẽ khác
        # tệp thô, nhưng THỨ TỰ TƯƠNG ĐỐI giữa các thẻ thì giữ nguyên — và G11a/G8d chỉ so
        # thứ tự, không so offset với bên ngoài.
        idx = html_song(doc("index.html"))
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

    def g12(self):
        """G12 — CHỐNG MẸO LÀM BÀI MÀ KHÔNG CẦN ĐỌC (thêm 06/10).

        VÌ SAO CÓ CỔNG NÀY. Phản biện độc lập vòng 9 cáo buộc: học sinh không đọc câu hỏi
        vẫn đạt điểm cao. Đo lại trên chính dữ liệu của repo thì cáo buộc ĐÚNG:
            js/tinhhuong.js  đáp án là "b" ở 11/12 câu, và "b" cũng là phương án DÀI NHẤT
                             ở 11/12 câu  -> mẹo "luôn bấm B" đạt 92%
            js/lab.js        đáp án "b" ở 4/4 câu, dài nhất 4/4 -> mẹo đó đạt 100%
        Điều này phá đúng tuyên bố cốt lõi của sản phẩm ("tự chấm khách quan bằng oracle"):
        con số thu về không còn đo năng lực, nên pre/post và recall đều vô nghĩa nếu học
        sinh phát hiện ra mẹo. Một hệ tự chấm mà bị mẹo hoá thì tệ hơn không tự chấm, vì
        nó tạo cảm giác đã đo được.

        HAI LỚP LỖI, HAI CÁCH CHỮA KHÁC NHAU — cổng này tách bạch để không ai tưởng
        sửa một cái là xong cả hai:
          LỚP 1 (VỊ TRÍ cố định) chữa được bằng MÃ: xáo thứ tự phương án trước khi vẽ
            (MX_ENGINE.xaoLuaChon) và sinh chữ cái hiển thị theo VỊ TRÍ sau khi xáo
            (MX_ENGINE.chuCai). Đã đo sau khi sửa: mẹo "luôn bấm một vị trí" từ 92% xuống
            26,0%, và kiểm định khi-bình-phương trên 3.600 mẫu cho χ²=5,47 < 7,81 (ngưỡng
            5%, 3 bậc tự do) — tức phân bố vị trí đáp án đều, không lệch chỗ nào.
          LỚP 2 (phương án ĐÚNG dài hơn phương án nhiễu) KHÔNG chữa được bằng mã. Không
            phép xáo trộn nào thay đổi được độ dài tương đối. Muốn diệt phải VIẾT LẠI
            phương án nhiễu cho cân độ dài — việc của tác giả, cần thời gian, và phải làm
            trước khi dạy thật. Vì vậy cổng KHÔNG che nó đi: nó đo, in ra tỉ lệ thật, và
            liệt kê từng item mắc nợ để thành danh sách việc làm.

        G12a  mọi chỗ vẽ phương án đều phải xáo vị trí (bắt hồi quy: ai thêm chỗ vẽ mới mà
              quên xáo thì mẹo "luôn bấm B" sống lại ngay).
        G12b  chữ cái hiển thị không được lấy từ nhãn cố định trong dữ liệu.
        G12c  ĐO KHOẢN NỢ NỘI DUNG: tỉ lệ câu có đáp án là phương án dài nhất. KHÔNG đặt
              ngưỡng pass/fail — đặt ngưỡng thì người ta sẽ sửa số đo cho qua, hoặc bỏ câu
              khó ra khỏi ngân hàng. In ra để nhìn thấy, và FAIL chỉ khi tỉ lệ TĂNG so với
              mốc đã ghi (khoản nợ phình ra mà không ai để ý).
        """
        print("\n=== G12 CHỐNG MẸO LÀM BÀI KHÔNG CẦN ĐỌC ===")
        # ---- G12a: mọi chỗ vẽ phương án đều phải đi qua xaoLuaChon ----
        # Đo bằng cách đếm: tệp nào có `.forEach` trên một mảng luaChon THÌ tệp đó phải có
        # lời gọi xaoLuaChon. Bản cũ của app vẽ thẳng `nv.luaChon.forEach(...)` — đó chính
        # là chỗ mẹo hoạt động. Nếu ai viết thêm một chỗ vẽ mới theo kiểu cũ, cổng kêu.
        tep_ve = []
        quen_xao = []
        for f in sorted(os.listdir(os.path.join(ROOT, "js"))):
            if not f.endswith(".js"):
                continue
            song = than_ma_song(doc("js/" + f))
            if "luaChon" not in song:
                continue
            # chỗ VẼ: duyệt mảng luaChon bằng forEach/map rồi tạo button
            ve = re.findall(r"(\w+)\.forEach\(", song)
            co_cho_ve = False
            for m in re.finditer(r"(\w+)\.forEach\(", song):
                bien = m.group(1)
                # biến đó có phải mảng phương án (gốc hoặc đã xáo) không
                sau = song[m.end():m.end() + 700]
                if re.search(r"createElement\(\s*[\"']button", sau) and \
                   re.search(r"\b" + re.escape(bien) + r"\b\s*=\s*"
                             r"(?:\w+\.)?xaoLuaChon\(", song):
                    co_cho_ve = True
                elif bien in ("ds",) and re.search(
                        r"createElement\(\s*[\"']button", sau):
                    co_cho_ve = True
            if not co_cho_ve:
                continue
            tep_ve.append("js/" + f)
            if "xaoLuaChon" not in song:
                quen_xao.append("js/" + f)
        self.them("G12a", "mọi chỗ vẽ phương án đều xáo vị trí (chống mẹo 'luôn bấm B')",
                  tep_ve and not quen_xao,
                  f"{len(tep_ve)} tệp vẽ phương án ({', '.join(tep_ve)}) đều gọi xaoLuaChon"
                  if tep_ve and not quen_xao
                  else ("KHÔNG tìm thấy chỗ vẽ phương án nào — phép đo HỎNG, đừng tin dòng này"
                        if not tep_ve else f"quên xáo vị trí: {quen_xao}"))

        # ---- G12b: chữ cái hiển thị không lấy từ nhãn cố định ----
        # `l.id.toUpperCase()` in ra chữ cái DÍNH với dữ liệu: xáo vị trí xong đáp án vẫn
        # luôn hiện chữ B, nên học sinh vẫn "luôn bấm B" được. Phải in theo VỊ TRÍ.
        in_nhan_co_dinh = []
        for f in sorted(os.listdir(os.path.join(ROOT, "js"))):
            if not f.endswith(".js"):
                continue
            song = than_ma_song(doc("js/" + f))
            for m in re.finditer(r"(\w+)\.id\.toUpperCase\(\)", song):
                dong = song[:m.start()].count("\n") + 1
                in_nhan_co_dinh.append(f"js/{f}:{dong}")
            # dòng "Phương án đúng: " in ra nhãn cố định cũng lộ đáp án sai chỗ
            for m in re.finditer(r"Phương án đúng[^\n]{0,80}\.dapAn\.toUpperCase\(\)", song):
                dong = song[:m.start()].count("\n") + 1
                in_nhan_co_dinh.append(f"js/{f}:{dong} (dòng 'Phương án đúng')")
        self.them("G12b", "chữ cái phương án sinh theo VỊ TRÍ, không theo nhãn cố định",
                  not in_nhan_co_dinh,
                  "không còn chỗ nào in `.id.toUpperCase()` hay `dapAn.toUpperCase()`"
                  if not in_nhan_co_dinh else "vẫn in nhãn cố định: " + ", ".join(in_nhan_co_dinh))

        # ---- G12c: đo khoản nợ nội dung, so với mốc đã ghi ----
        MOC_NO = 82.9          # % đo được ngày 06/10, trước khi viết lại phương án nhiễu
        DUNGSAI = 1.0          # điểm phần trăm: lệch dưới mức này coi như nhiễu đo
        re_block = re.compile(r"luaChon\s*:\s*\[(.*?)\]", re.S)
        re_item = re.compile(r'\{\s*id\s*:\s*"([a-e])"\s*,\s*text\s*:\s*"((?:[^"\\]|\\.)*)"')
        re_dap = re.compile(r'dapAn\s*:\s*"([a-e])"')
        tong, no, muc = 0, 0, {}
        nguon = ("js", "data")
        for thu_muc in nguon:
            for f in sorted(os.listdir(os.path.join(ROOT, thu_muc))):
                if not f.endswith(".js"):
                    continue
                rel = f"{thu_muc}/{f}"
                s = doc(rel)
                if "luaChon" not in s:
                    continue
                n = d = 0
                for m in re_block.finditer(s):
                    items = re_item.findall(m.group(1))
                    if len(items) < 2:
                        continue
                    dm = re_dap.search(s[m.end():m.end() + 900])
                    if not dm:
                        truoc = s[max(0, m.start() - 1500):m.start()]
                        c = list(re_dap.finditer(truoc))
                        dm = c[-1] if c else None
                    if not dm:
                        continue
                    dap = dm.group(1)
                    if dap not in [k for k, _ in items]:
                        continue
                    dai = max(items, key=lambda x: len(x[1]))[0]
                    n += 1
                    if dai == dap:
                        d += 1
                if n:
                    muc[rel] = (d, n)
                    tong += n
                    no += d
        ti_le = (100.0 * no / tong) if tong else None
        self.them("G12c", f"khoản nợ nội dung không phình (mốc {MOC_NO}%, đo {ti_le:.1f}%)"
                  if ti_le is not None else "khoản nợ nội dung (không đo được)",
                  ti_le is not None and ti_le <= MOC_NO + DUNGSAI,
                  (f"{no}/{tong} câu có đáp án LÀ phương án dài nhất = {ti_le:.1f}% "
                   f"(mẹo 'chọn câu dài nhất' đạt từng ấy; ngẫu nhiên ~25%). "
                   f"Chi tiết: " + ", ".join(f"{k} {v[0]}/{v[1]}" for k, v in sorted(muc.items()))
                   + " — ĐÂY LÀ NỢ NỘI DUNG, xáo vị trí không sửa được, phải viết lại phương án nhiễu")
                  if ti_le is not None else
                  "không tìm thấy câu hỏi nào có luaChon+dapAn — phép đo HỎNG, đừng tin dòng này")

    def g13(self):
        """G13 — MANIFEST PHẢI PHỦ ĐỦ MỌI TỆP THUỘC SẢN PHẨM (thêm 06/10).

        VÌ SAO CÓ CỔNG NÀY. SHA256SUMS.txt được README khai là "bằng chứng mốc thời gian &
        toàn vẹn", và hồ sơ dự thi dựa vào nó để chứng minh "sản phẩm gốc". Nhưng đo thật
        lúc phát hiện: git theo dõi 90 tệp mà manifest chỉ có 72 — thiếu 18 tệp, trong đó có
            · tools/nghiem_thu.py  — CHÍNH CÁI CỔNG sinh ra mọi con số "56/56 ĐẠT"
            · tools/kiem_noi_dung.py, tinh_do_phu.py, gop_csv.py, sinh_manifest.py
            · data-source/2422_PL_khung.pdf — văn bản Bộ có chữ ký, căn cứ pháp lý của sản phẩm
        Đây là LỖ HỔNG TỰ THAM CHIẾU: bằng chứng toàn vẹn không phủ công cụ sinh ra bằng
        chứng. Sửa cổng để nó luôn in ĐẠT thì manifest không phát hiện. Và `sha256sum -c`
        vẫn trả "72/72 OK" — đúng định dạng, đọc như thật, không ai nghi ngờ.

        Nguyên nhân gốc nằm ở tools/sinh_manifest.py: danh sách tệp lấy từ
        `set(manifest_cũ) | set(danh_sách_gõ_tay)`, nên tệp mới chỉ được vào manifest nếu
        nó ĐÃ ở trong đó hoặc có ai nhớ gõ tên. Đã sửa sang `git ls-files`. Cổng này giữ
        cho lỗi đó không quay lại.

        G13a  mọi tệp git theo dõi phải có trong manifest (trừ chính manifest).
        G13b  hash trong manifest phải KHỚP tệp trên đĩa — bắt manifest cũ sau khi sửa mã.
        G13c  manifest không được chứa tệp mà git không theo dõi (bằng chứng mồ côi).
        """
        print("\n=== G13 TOÀN VẸN MANIFEST SHA256SUMS ===")
        man = os.path.join(ROOT, "SHA256SUMS.txt")
        if not os.path.isfile(man):
            self.them("G13a", "manifest phủ đủ mọi tệp sản phẩm", False,
                      "KHÔNG có SHA256SUMS.txt — không có bằng chứng toàn vẹn nào để kiểm")
            return

        khai = {}
        for dong in open(man, encoding="utf-8"):
            m = re.match(r"^([0-9a-f]{64})\s+(.+?)\s*$", dong)
            if m:
                khai[m.group(2)] = m.group(1)

        # Danh sách tệp thuộc sản phẩm: hỏi git, không gõ tay.
        try:
            r = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                               text=True, timeout=120)
            tracked = [f for f in r.stdout.split("\n") if f] if r.returncode == 0 else None
        except (OSError, subprocess.SubprocessError):
            tracked = None
        if not tracked:
            self.them("G13a", "manifest phủ đủ mọi tệp sản phẩm", False,
                      "không đọc được `git ls-files` — KHÔNG đoán danh sách thay thế, "
                      "vì đoán là tái sinh đúng lỗi manifest thiếu tệp")
            return

        tracked = [f for f in tracked if f != "SHA256SUMS.txt"]

        thieu = sorted(f for f in tracked if f not in khai)
        # Cổng phải phủ CHÍNH NÓ: nêu đích danh nếu thiếu công cụ đo.
        thieu_cong_cu = [f for f in thieu
                         if f.startswith("tools/") or f.startswith("data-source/")]
        self.them("G13a", f"manifest phủ đủ {len(tracked)} tệp git theo dõi (kể cả cổng + văn bản Bộ)",
                  not thieu,
                  f"đủ {len(tracked)}/{len(tracked)} tệp" if not thieu
                  else f"THIẾU {len(thieu)} tệp"
                       + (f" — trong đó có CÔNG CỤ ĐO/NGUỒN PHÁP LÝ: {thieu_cong_cu}"
                          if thieu_cong_cu else "")
                       + f": {thieu[:8]}{'…' if len(thieu) > 8 else ''}"
                       + " · chạy `python3 tools/sinh_manifest.py --ghi`")

        # G13b — hash phải khớp. Tệp không còn trên đĩa thì báo riêng, không tính là khớp.
        lech, mat = [], []
        for f, h in sorted(khai.items()):
            p = os.path.join(ROOT, f)
            if not os.path.isfile(p):
                mat.append(f)
                continue
            hh = hashlib.sha256()
            with open(p, "rb") as fp:
                for khoi in iter(lambda: fp.read(1 << 20), b""):
                    hh.update(khoi)
            if hh.hexdigest() != h:
                lech.append(f)
        self.them("G13b", "hash trong manifest KHỚP tệp trên đĩa (manifest không cũ)",
                  not lech and not mat,
                  f"{len(khai) - len(lech) - len(mat)}/{len(khai)} tệp khớp hash"
                  if not lech and not mat
                  else ("mất trên đĩa: " + ", ".join(mat[:6]) + " · " if mat else "")
                       + (f"hash LỆCH {len(lech)} tệp: {', '.join(lech[:6])}"
                          f"{'…' if len(lech) > 6 else ''}" if lech else "")
                       + " · mã đã đổi mà manifest chưa sinh lại: "
                         "`python3 tools/sinh_manifest.py --ghi`")

        mo_coi = sorted(set(khai) - set(tracked) - {"SHA256SUMS.txt"})
        self.them("G13c", "manifest không chứa tệp ngoài git (bằng chứng mồ côi)",
                  not mo_coi,
                  "mọi tệp trong manifest đều được git theo dõi" if not mo_coi
                  else f"{len(mo_coi)} tệp trong manifest mà git không theo dõi: "
                       f"{mo_coi[:8]} — hoặc `git add` nó, hoặc nó không thuộc sản phẩm")

    def g14(self):
        """G14 — NHÃN LOẠI LỖI PHẢI KHỚP NHAU Ở MỌI BẢN SAO (thêm 07/10).

        VÌ SAO CÓ CỔNG NÀY. Tên 5 loại lỗi AI được chép tay ở BA nơi khác nhau:
          data/meta.js         -> nguồn hiển thị trong app (bảng báo cáo, bảng nhầm lẫn)
          js/nhamay_text.js    -> nhãn dùng ở Trạm 5 (nhà máy sinh văn bản)
          tools/gop_csv.py     -> dict LOAI_LOI, in ra baocao_lop.csv khi gộp đa máy
        Ba bản sao chép tay thì SỚP MUỘN cũng lệch. Hậu quả rất khó thấy: học sinh nhìn tên
        lỗi này trong app, giáo viên mở tệp báo cáo gộp lại thấy tên khác, và không nối được
        hai bên — trong khi cả hai đều "đúng" theo tệp của mình. Đã xảy ra thật: nhãn này
        từng là "Xui lộ dữ liệu cá nhân" và được sửa thành "Xúi lộ dữ liệu cá nhân" (vì "xui"
        đọc lướt thành "xui xẻo", sai hẳn ý "xúi giục"). Sửa nhãn ở một chỗ mà quên hai chỗ
        còn lại là đúng loại lỗi cổng này phải chặn.

        CÁCH SO. Đọc khoá (so_lieu_bia, thien_kien, ...) làm trục, không so cả tệp: mỗi nơi
        khai nhãn theo cú pháp riêng (JS object vs dict Python), nên chỉ trích đúng cặp
        khoá -> nhãn rồi đối chiếu từng khoá một. Khoá có ở nơi này mà thiếu ở nơi khác
        cũng bị bắt, không chỉ bắt khi nhãn khác chữ.
        """
        import re as _re

        # tools/gop_csv.py: dict LOAI_LOI = { "<khoá>": "<nhãn>", ... } — đây là NGUỒN KHOÁ
        # chuẩn, vì nó phẳng (không lồng) nên trích không thể nhầm.
        py = doc("tools/gop_csv.py")
        m_dict = _re.search(r"^LOAI_LOI\s*=\s*\{(?P<body>.*?)^\}", py, _re.S | _re.M)
        gop = {}
        if m_dict:
            for k, v in _re.findall(r'"(\w+)"\s*:\s*"([^"]+)"', m_dict.group("body")):
                gop[k] = v

        def nhan_js(path, khoa):
            """Lấy nhãn của MỘT khoá trong tệp JS.

            CÁCH LÀM VÀ VÌ SAO: định vị chuỗi `<khoá>: {` rồi lấy `ten: "..."` ĐẦU TIÊN sau
            vị trí đó. Bản đầu của cổng này quét mọi khối `^\s{2,}(\w+): {` trong tệp — và
            sai, vì cả hai tệp JS đều có cấu trúc LỒNG: data/meta.js có `loaiLoi: {` chứa 5
            khoá con rồi tới `dauHieu: {`, còn js/nhamay_text.js có thêm 4 khối chủ đề Trạm 5
            (nongNghiep/yTe/giaoDuc/moiTruong). Kết quả lần chạy đầu: meta.js trích ra 6 nhãn
            trong đó có `unesco` và `loaiLoi` là RÁC, `so_lieu_bia` bị nuốt vào khối cha nên
            biến mất, và G14a vẫn in ĐẠT. Đó là ĐẠT GIẢ — cổng báo xanh trong khi nó đang so
            sai dữ liệu, tức tệ hơn là không có cổng.
            Tra theo khoá cụ thể thì không phụ thuộc độ lồng, và khoá lạ không thể lọt vào.
            """
            src = doc(path)
            m = _re.search(rf"(?<![\w]){_re.escape(khoa)}\s*:\s*\{{", src)
            if not m:
                return None
            t = _re.search(r'ten:\s*"([^"]+)"', src[m.end():])
            return t.group(1) if t else None

        # G14a — cổng có TRÍCH ĐƯỢC nhãn không. Đây là phép kiểm SỨC KHOẺ CỦA CHÍNH CỔNG,
        # không phải phép kiểm sản phẩm: nếu regex trật (đổi định dạng tệp, đổi tên trường)
        # thì hai phép dưới so sánh trên dữ liệu rỗng và sẽ in ĐẠT GIẢ.
        #
        # SỬA 07/10 SAU MUTATION TEST. Bản đầu viết `ok_a = not thieu_trich and
        # len(meta) == len(gop)` rồi `return` sớm — tức G14a FAIL ngay khi gop_csv.py có một
        # khoá mà meta.js không có. Nhưng đó CHÍNH XÁC là việc G14c phải bắt. Hệ quả: G14c
        # không bao giờ chạy được (mutation ca 3 chứng minh: phá đúng thứ G14c canh thì
        # G14a kêu trước rồi return, G14c im lặng vĩnh viễn). Một tiêu chí không thể fail
        # là nhánh chết — cùng lớp lỗi với G11c.
        # Nay G14a chỉ hỏi "có trích được gì không", còn thiếu/lệch/lạ giao cho G14b, G14c.
        def khoa_con_cap1(src, ten_khoi):
            """Liệt kê khoá CON CẤP 1 của khối `ten_khoi: { ... }`, bỏ qua khối lồng.

            VÌ SAO KHÔNG DÙNG `^\\s{4}(\\w+):\\{`: cách đó phụ thuộc số dấu cách thụt lề, và
            một lần chạy formatter là cổng mù. Cách này đếm depth bằng chính dấu ngoặc: một
            khoá được nhận khi tại vị trí của nó, số `{` trừ số `}` tính từ đầu khối bằng 0
            (tức đang ở cấp 1, chưa vào khối con nào). `dauHieu: {` bên trong mỗi loại lỗi
            có depth 1 nên bị loại — đó chính là lỗi của bản regex đầu tiên.

            Trả về None nếu không thấy khối (định dạng đã đổi) — để G14a báo cổng hỏng.
            """
            m = _re.search(rf"(?<![\w]){_re.escape(ten_khoi)}\s*:\s*\{{", src)
            if not m:
                return None
            # cắt đúng thân khối bằng đếm ngoặc, không đoán bằng indent
            i, depth = m.end(), 1
            while i < len(src) and depth > 0:
                if src[i] == "{":
                    depth += 1
                elif src[i] == "}":
                    depth -= 1
                i += 1
            than = src[m.end():i - 1]
            keys = []
            for mm in _re.finditer(r"(\w+)\s*:\s*\{", than):
                truoc = than[:mm.start()]
                if truoc.count("{") - truoc.count("}") == 0:
                    keys.append(mm.group(1))
            return keys

        meta_src = doc("data/meta.js")
        khoa_meta = khoa_con_cap1(meta_src, "loaiLoi") or []

        meta, nhamay, thieu_trich = {}, {}, []
        for khoa in sorted(gop):
            a = nhan_js("data/meta.js", khoa)
            b = nhan_js("js/nhamay_text.js", khoa)
            if a is None:
                thieu_trich.append(khoa)
            else:
                meta[khoa] = a
            if b is not None:
                nhamay[khoa] = b      # nhamay_text.js không bắt buộc đủ 5 loại

        # G14a = SỨC KHOẺ CỦA CHÍNH CỔNG. Chỉ hỏi "cơ chế trích có chạy không", KHÔNG hỏi
        # "hai bên có đủ 5 khoá không" — việc đó của G14c. Bản đầu gộp hai câu hỏi làm một
        # (`len(meta) == len(gop)`) nên G14a kêu trước rồi `return`, và G14c thành nhánh chết.
        # Cũng KHÔNG đòi `len(khoa_meta) >= 5`: nếu meta.js thật sự chỉ còn 4 loại lỗi thì
        # việc trích vẫn ĐÃ THÀNH CÔNG (tìm ra 4) — báo "cổng hỏng" lúc đó là báo sai, và
        # che mất thông tin thật là hai bên lệch nhau.
        ok_a = len(gop) >= 5 and len(meta) >= 1 and len(nhamay) >= 1 and len(khoa_meta) >= 1
        self.them("G14a", "cơ chế trích nhãn loại lỗi còn hoạt động ở cả ba bản sao", ok_a,
                  f"gop_csv.py {len(gop)} khoá · data/meta.js {len(khoa_meta)} khoá "
                  f"(trích được {len(meta)} nhãn) · nhamay_text.js {len(nhamay)} nhãn"
                  if ok_a
                  else f"chỉ trích được gop={len(gop)} meta={len(meta)} "
                       f"khoa_meta={len(khoa_meta)} nhamay={len(nhamay)} — cơ chế trích trong "
                       f"g14() đã trật (đổi định dạng tệp? đổi tên trường? đổi kiểu dấu nháy?), "
                       f"cổng không được tin, ĐỪNG đọc hai phép dưới là ĐẠT")
        if not ok_a:
            return

        # G14b — nhãn phải trùng chữ ở mọi nơi có cùng khoá.
        # Chỉ so những khoá CÓ ở cả hai bên; khoá thiếu được G14c xử, không cộng vào đây
        # (nếu không thì một lỗi bị đếm hai lần và thông báo lỗi chỉ chỗ sai).
        lech = []
        for khoa in sorted(meta):
            ten = meta[khoa]
            for ten_tep, bang in (("js/nhamay_text.js", nhamay), ("tools/gop_csv.py", gop)):
                if khoa not in bang:
                    # nhamay_text.js không bắt buộc đủ 5 loại (nó chỉ sinh văn bản theo
                    # loại có mẫu), nên thiếu ở đó là bình thường; thiếu trong gop_csv.py
                    # thì báo cáo gộp sẽ in rỗng — mới là lỗi, và do G14c bắt.
                    continue
                if bang[khoa] != ten:
                    lech.append(f"{khoa}: meta.js «{ten}» ≠ {ten_tep} «{bang[khoa]}»")
        self.them("G14b", "nhãn 5 loại lỗi trùng chữ ở meta.js / nhamay_text.js / gop_csv.py",
                  not lech,
                  f"{len(meta)} loại lỗi có nhãn khớp nhau ở mọi bản sao" if not lech
                  else ("; ".join(lech[:4])
                        + " — sửa cho khớp, hoặc nếu nhãn đổi có chủ đích thì đổi ở CẢ BA nơi"))

        # G14c — hai chiều của tập khoá. Chiều thứ nhất (khoá lạ trong gop_csv.py) là ca
        # mutation số 3; chiều thứ hai (meta.js có khoá mà gop_csv.py thiếu) cũng bắt luôn,
        # vì nó làm dòng báo cáo của loại lỗi đó in rỗng.
        # SO VỚI `khoa_meta` (liệt kê độc lập từ data/meta.js), KHÔNG so với `meta`.
        # `meta` chỉ được xây từ `for khoa in sorted(gop)` nên tập khoá của nó luôn là TẬP CON
        # của gop — viết `set(meta) - set(gop)` thì kết quả luôn rỗng, tức nhánh "thiếu" không
        # bao giờ chạy được. Đó là code chết nằm ngay dưới một tiêu chí có tên tuyên bố kiểm
        # CẢ HAI CHIỀU ("hai bên khai đúng cùng một tập"), nên cổng vẫn in ĐẠT và không ai
        # biết nửa còn lại chưa từng được thực thi. Chỉ phát hiện được khi thiết kế ca phá
        # cho đúng chiều đó TRƯỚC khi tin rằng cổng đã canh.
        thua = sorted(set(gop) - set(khoa_meta))     # gop_csv khai mà app không có loại lỗi đó
        thieu = sorted(set(khoa_meta) - set(gop))    # app có mà báo cáo gộp sẽ in rỗng
        ok_c = not thua and not thieu
        self.them("G14c", "hai bên khai đúng cùng một tập 5 loại lỗi",
                  ok_c,
                  f"cùng {len(gop)} khoá ở data/meta.js và tools/gop_csv.py" if ok_c
                  else (" · ".join(filter(None, [
                            f"thừa trong gop_csv.py (app không bao giờ ghi, dòng báo cáo luôn "
                            f"trống): {thua[:4]}" if thua else "",
                            f"thiếu trong gop_csv.py (loại lỗi này mất khỏi baocao_lop.csv): "
                            f"{thieu[:4]}" if thieu else ""]))))

        # G14d — BẢN SAO NHÃN THỨ TƯ: huong-dan-danh-gia.md (thêm 07/10).
        #
        # VÌ SAO: khi viết tài liệu hướng dẫn đánh giá, tôi đã CHÉP TAY năm tên loại lỗi vào đó
        # ("Số liệu bịa đặt · Nguồn/văn bản không tồn tại · ...") để giáo viên dùng đúng chữ mà
        # học sinh thấy trên màn hình. Thế là nhãn có bốn bản sao chứ không phải ba, và G14b/G14c
        # chỉ canh ba. Đổi tên ở data/meta.js (như đã đổi "Xui" -> "Xúi") thì tài liệu lệch âm
        # thầm: giáo viên viết nhận xét bằng một cái tên không còn xuất hiện trong app, và phụ
        # huynh/hội đồng đối chiếu sẽ không nối được.
        # Đúng lớp lỗi mà cả cổng G14 sinh ra để chặn, chỉ khác chỗ bản sao thứ tư nằm trong .md.
        #
        # Không đòi tài liệu phải liệt kê theo cấu trúc nào — chỉ đòi mỗi tên nhãn xuất hiện
        # NGUYÊN VĂN ở đâu đó trong tệp. Tài liệu là văn xuôi cho người đọc, không phải dữ liệu;
        # bắt nó theo khuôn thì sẽ sinh ra dương tính giả mỗi lần ai đó viết lại câu chữ.
        duong_doc = "huong-dan-danh-gia.md"
        p_doc = os.path.join(ROOT, duong_doc)
        if not os.path.isfile(p_doc):
            self.them("G14d", f"nhãn 5 loại lỗi khớp trong {duong_doc}", False,
                      f"không thấy {duong_doc} trong repo — README §2 dẫn giáo viên tới tệp đó "
                      f"để đọc số liệu, nên thiếu tệp là một lời hứa gãy (cùng lớp lỗi với "
                      f"gop_csv.py và ho-so/ từng bị hứa mà không có)")
        else:
            doc_md = doc(duong_doc)
            thieu_doc = [meta[k] for k in sorted(meta) if meta[k] not in doc_md]
            self.them("G14d", f"nhãn 5 loại lỗi khớp trong {duong_doc}", not thieu_doc,
                      f"cả {len(meta)} tên loại lỗi của data/meta.js đều xuất hiện nguyên văn "
                      f"trong tài liệu hướng dẫn đánh giá" if not thieu_doc
                      else f"{len(thieu_doc)} nhãn trong {duong_doc} LỆCH với data/meta.js: "
                           f"{thieu_doc} — giáo viên sẽ viết nhận xét bằng cái tên không còn "
                           f"hiện trên màn hình. Sửa tài liệu theo meta.js (hoặc ngược lại, "
                           f"nhưng phải sửa CẢ BỐN nơi: meta.js, nhamay_text.js, gop_csv.py, "
                           f"{duong_doc})")

    def g15(self):
        """G15 — MỌI TRẠM/VIEW ẨN BAN ĐẦU PHẢI CÓ LỆNH HIỆN LẠI (thêm 07/10).

        LỖI THẬT MÀ CỔNG NÀY SINH RA ĐỂ CHẶN. index.html khai ba trạm nhà máy với
        `style="display:none"`. nmMoTram() ẩn cả ba rồi gọi hàm khởi động của trạm được chọn;
        hàm đó PHẢI hiện lại trạm của mình. nmKhoiDongTram0() và nmKhoiDongTram1() có dòng
        `$("nm-tramN").style.display = ""` — còn nmKhoiDongTram5() KHÔNG CÓ, chỉ có dòng ẩn ở
        nhánh thiếu module. Kết quả: TRẠM 5 — ỨNG DỤNG vô hình vĩnh viễn kể từ commit f0936c8
        (04/10), tức từ chính commit tạo ra nó. Trạm đó phủ bốn YCCĐ (10.C2.MR2 · 10.C3.1 ·
        10.C3.2 · 10.B2.MR1) và chứa hai ô dự đoán BT-07/BT-08.

        VÌ SAO SUỐT BẤY LÂU KHÔNG AI BIẾT:
        · Không cổng nào kiểm tính HIỂN THỊ. G11e chỉ kiểm host id CÓ trong index.html — và id
          `nm-muc3-bt07` có thật, chỉ là tổ tiên của nó bị ẩn. Phép kiểm "có tồn tại không"
          không bao giờ bắt được lỗi "tồn tại mà không tới được".
        · tools/tinh_do_phu.py vẫn báo 22/22 PHỦ vì nó đếm YCCĐ xuất hiện trong MÃ, không kiểm
          mã đó học sinh có tới được không → BẰNG CHỨNG PHỦ GIẢ.
        · `.click()` bằng JS chạy được trên phần tử ẩn, nên mọi test tự động đều "đạt". Chỉ có
          người thật nhìn màn hình mới thấy trạm trống.

        CÁCH KIỂM (cố ý hẹp để không có dương tính giả): đọc DANH SÁCH ID BỊ ẨN từ chính mảng
        trong nmMoTram() — không gõ tay. Với mỗi id: (a) phải có trong index.html, (b) phải có
        lệnh hiện lại `$("id").style.display = ""` ở đâu đó trong js/app.js. Thêm trạm mới vào
        mảng đó thì cổng tự kiểm luôn, không cần sửa cổng.
        """
        app_js = than_ma_song(doc("js/app.js"))
        # html_song(): G15b kiểm `id="nm-tramN"` có thật trong index.html. Chính tôi đã viết một
        # chú thích dài trong index.html nhắc tới các id này khi giải thích phần tử chết
        # #btn-dangnhap — nếu kiểm trên tệp thô thì chú thích đó đủ làm G15b ĐẠT giả kể cả khi
        # thẻ trạm bị xoá. Đây là ca có thật trong repo, không phải giả định.
        idx = html_song(doc("index.html"))

        # Danh sách id mà nmMoTram() ẩn đi trước khi mở trạm. Nếu không trích được thì cổng
        # đang hỏng — phải báo LỖI, tuyệt đối không im lặng in ĐẠT (bài học từ G14a).
        m = re.search(r'\[\s*((?:"nm-tram\d+"\s*,?\s*)+)\]\s*\.forEach', app_js)
        if not m:
            self.them("G15a", "trích được danh sách trạm bị ẩn trong nmMoTram()", False,
                      "không tìm thấy mảng [\"nm-tram…\"].forEach trong js/app.js — cấu trúc đã "
                      "đổi, cổng G15 không còn canh được gì. Sửa regex trong g15().")
            return
        ids = re.findall(r'"([\w-]+)"', m.group(1))
        self.them("G15a", "trích được danh sách trạm bị ẩn trong nmMoTram()", bool(ids),
                  f"{len(ids)} trạm: {ids}" if ids else "mảng rỗng — cổng không canh gì")

        thieu_html, thieu_hien = [], []
        for i in ids:
            if f'id="{i}"' not in idx:
                thieu_html.append(i)
            # lệnh hiện lại: $("id").style.display = "" (hoặc 'block')
            if not re.search(rf'\$\("{re.escape(i)}"\)\s*\.\s*style\s*\.\s*display\s*=\s*(""|\'\'|"block")',
                             app_js):
                thieu_hien.append(i)

        self.them("G15b", "mọi trạm đều có id thật trong index.html", not thieu_html,
                  f"{len(ids)}/{len(ids)} id có trong index.html" if not thieu_html
                  else f"thiếu id trong index.html: {thieu_html}")

        self.them("G15c", "mọi trạm bị ẩn đều có lệnh HIỆN LẠI (không trạm nào vô hình)",
                  not thieu_hien,
                  f"cả {len(ids)} trạm đều có lệnh hiện lại — không trạm nào kẹt ở display:none"
                  if not thieu_hien
                  else f"{len(thieu_hien)} trạm BỊ ẨN VĨNH VIỄN (không có lệnh hiện lại): "
                       f"{thieu_hien} — học sinh bấm nút trạm đó sẽ thấy một khoảng TRỐNG; "
                       f"thêm `$(\"{thieu_hien[0]}\").style.display = \"\";` vào hàm khởi động "
                       f"của nó. Đây chính là lỗi đã làm Trạm 5 vô hình từ 04/10.")

    def g16(self):
        """G16 — BA BẢN KHAI CỘT CSV PHẢI KHỚP NHAU (thêm 07/10).

        LỖI THẬT MÀ CỔNG NÀY SINH RA ĐỂ CHẶN. Cùng một bộ nhật ký, giáo viên có HAI nút để tải
        về: "Xuất CSV" (js/engine.js xuatCSV) và "Xuất JSON" (engine.js xuatJSON, rồi
        tools/gop_csv.py doc_json đọc lại). Hai đường đó khai danh sách cột ở BA nơi khác nhau:
          1. `const rows = [[...]]` trong js/engine.js  — header của tệp CSV
          2. `HDR = [...]` trong tools/gop_csv.py        — header của tệp gộp (DictWriter)
          3. dict dựng BẰNG TAY trong `doc_json()`       — các cột có được khi đọc JSON
        Không có gì buộc ba nơi đó khớp nhau. Và chúng ĐÃ lệch: doc_json chỉ xuất 14/21 cột,
        mất `che_do`, `phien_tong`, `phien_dung` nên bao_cao() bỏ qua MỌI phiên pre/post đến từ
        tệp JSON — khối "TIẾN TRÌNH PRE/POST" trống trơn, mà hiệu pre/post chính là con số dùng
        làm bằng chứng tác động trong hồ sơ. Mất luôn `loai_loi_that` nên cả 5 loại lỗi ra
        recall = 0. Script vẫn in "✅ N sự kiện" và vẫn ghi đủ 3 tệp, không một dòng cảnh báo.
        Lỗi này có từ khi doc_json được viết, không phải do đợt vá nào gây ra.

        VÌ SAO KIỂM BẰNG CÁCH GỌI THẬT, KHÔNG BẰNG REGEX: bản đầu tôi định trích khoá của dict
        trong doc_json bằng regex. Nhưng dict đó dựng bằng biểu thức điều kiện (`"" if ... else
        ...`) và comment nằm XEN giữa các cặp khoá-giá trị, nên regex rất dễ đếm sai — và một
        phép kiểm đếm sai thì hoặc báo oan (bắt người ta sửa thứ không hỏng) hoặc báo ĐẠT giả.
        Cách này ghi một tệp JSON tối thiểu ra /tmp rồi GỌI doc_json() và đọc tập khoá của dict
        trả về: đó là sự thật runtime, không phải suy đoán từ văn bản.

        BẪY KHI SỬA CỔNG NÀY: trích cột từ engine.js phải dùng `[\\w]+`, KHÔNG dùng `[a-z_]+`.
        Tên cột `thoi_gian_ISO` có CHỮ HOA; bản đầu tôi dùng `[a-z_]+` nên cột đó bị bỏ rơi và
        cổng báo lệch 20/21 trong khi thật ra khớp 21/21 — một dương tính giả do chính phép đo.
        """
        import importlib.util

        # ---- (1) nạp gop_csv.py như một module để lấy HDR và gọi doc_json thật ----
        # PHẢI kiểm `spec is None`: spec_from_file_location trả None khi đường dẫn không tồn tại
        # hoặc không phải tệp Python nạp được. Bản đầu bỏ qua bước này và truyền thẳng vào
        # module_from_spec(spec) rồi gọi spec.loader — tức là nếu tools/gop_csv.py biến mất (đổi
        # tên, quên commit, checkout sai branch) thì cổng NỔ AttributeError thay vì in một tiêu
        # chí LỖI. Một cổng chết bằng traceback thì không ai đọc được nó muốn nói gì, và cả
        # nhóm G16 mất trắng thay vì chỉ báo đúng phép kiểm bị hỏng.
        duong_gop = os.path.join(ROOT, "tools", "gop_csv.py")
        mod, hdr = None, []
        try:
            spec = importlib.util.spec_from_file_location("gop_csv_g16", duong_gop)
            if spec is None or spec.loader is None:
                raise ImportError(f"không nạp được {duong_gop} như một module Python")
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            hdr = list(mod.HDR)
        except Exception as e:
            self.them("G16a", "nạp được tools/gop_csv.py để đọc HDR", False,
                      f"không nạp được: {type(e).__name__}: {e} — cổng G16 không kiểm được gì, "
                      f"ĐỪNG đọc các phép dưới là ĐẠT")
            return
        self.them("G16a", "nạp được tools/gop_csv.py để đọc HDR", bool(hdr),
                  f"HDR có {len(hdr)} cột" if hdr else "HDR rỗng — cổng không canh được gì")
        if not hdr:
            return

        # ---- (2) gọi doc_json THẬT trên một tệp JSON tối thiểu ----
        # Sự kiện mẫu cố ý mang đủ loại trường (kq của câu đấu trường + trường của phiên) để
        # mọi nhánh trong dict đều được đi qua. Thiếu một trường thì giá trị rỗng, nhưng TÊN
        # khoá vẫn phải có — đó chính là thứ đang được kiểm.
        mau = {"ZZ01": {"maHS": "ZZ01", "maLop": "10Z", "suKien": [
            {"loai": "phien", "cheDo": "post", "t": 1791296700011, "phaiLap": 0,
             "tong": 12, "dung": 9, "batOan": 1, "boSot": 2},
            {"loai": "dauTruong", "t": 1791296700020,
             "kq": {"itemId": "dt-1", "diem": 1, "loaiThat": "co_loi",
                    "loaiLoiThat": "thien_kien", "traLoiVerdict": "co_loi",
                    "traLoiLoai": "so_lieu_bia", "mach": "A1", "unesco": "A1"}},
            {"loai": "duDoan", "suKien": "doiChieu", "baiToan": "BT-03", "t": 1791296700001,
             "kq": {"duDoan": 70, "dapAn": 100, "diem": 0, "dung": False}},
        ]}}
        import tempfile
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(prefix="g16_", suffix=".json")
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(mau, f, ensure_ascii=False)
            dong = mod.doc_json(tmp)
            khoa_json = set(dong[0].keys()) if dong else set()
            loi_goi = None
        except Exception as e:
            khoa_json, loi_goi = set(), f"{type(e).__name__}: {e}"
        finally:
            if tmp and os.path.isfile(tmp):
                os.remove(tmp)

        if loi_goi:
            self.them("G16b", "doc_json() chạy được trên dữ liệu mẫu", False,
                      f"gọi doc_json() nổ: {loi_goi}")
            return
        thieu = [c for c in hdr if c not in khoa_json]
        thua = sorted(khoa_json - set(hdr))
        self.them("G16b", "doc_json() xuất ĐỦ mọi cột trong HDR (đường JSON không mất dữ liệu)",
                  not thieu,
                  f"doc_json xuất đủ {len(hdr)}/{len(hdr)} cột" if not thieu
                  else f"{len(thieu)} cột của HDR KHÔNG được doc_json xuất ra: {thieu} — với tệp "
                       f"JSON, các cột này rỗng nên báo cáo gộp mất dữ liệu ÂM THẦM (đã từng làm "
                       f"mất toàn bộ tiến trình pre/post và làm recall = 0). Thêm chúng vào dict "
                       f"trong doc_json().")
        self.them("G16c", "doc_json() không sinh cột lạ ngoài HDR (cột lạ sẽ bị DictWriter vứt)",
                  not thua,
                  "mọi cột doc_json sinh ra đều có trong HDR" if not thua
                  else f"{len(thua)} cột doc_json sinh ra mà HDR không có: {thua} — chúng sẽ bị "
                       f"DictWriter(extrasaction='ignore') VỨT âm thầm khi ghi tệp gộp, hoặc làm "
                       f"lệch thứ tự cột. Thêm vào HDR hoặc bỏ khỏi doc_json.")

        # ---- (3) header của xuatCSV trong js/engine.js phải khớp HDR tuyệt đối ----
        app_engine = than_ma_song(doc("js/engine.js"))
        m = re.search(r"const rows = \[\[(.*?)\]\];", app_engine, re.S)
        if not m:
            self.them("G16d", "trích được header của xuatCSV trong js/engine.js", False,
                      "không tìm thấy `const rows = [[...]]` trong js/engine.js — xuatCSV đã đổi "
                      "cấu trúc, cổng G16 không còn canh được đường CSV. Sửa regex trong g16().")
            return
        # [\w]+ chứ KHÔNG phải [a-z_]+ : tên cột thoi_gian_ISO có chữ hoa (xem docstring).
        cols = re.findall(r'"([\w]+)"', m.group(1))
        khop = cols == hdr
        self.them("G16d", "header xuatCSV (engine.js) KHỚP HDR (gop_csv.py) tuyệt đối, cả thứ tự",
                  khop,
                  f"cả hai khai {len(hdr)} cột, giống nhau từng cột và đúng thứ tự" if khop
                  else f"LỆCH: engine.js {len(cols)} cột vs HDR {len(hdr)} cột · "
                       f"chỉ engine.js có: {[c for c in cols if c not in hdr]} · "
                       f"chỉ HDR có: {[c for c in hdr if c not in cols]} · "
                       f"sai thứ tự thì tệp CSV của máy này và máy khác không gộp được theo tên cột")

    def g17(self):
        """G17 — MỌI ĐƯỜNG DẪN MÀ TÀI LIỆU HỨA PHẢI TỒN TẠI THẬT (thêm 07/10).

        LỖI THẬT, XẢY RA HAI LẦN, VÀ HAI LẦN ĐỀU DO REVIEWER ĐỘC LẬP PHÁT HIỆN CHỨ KHÔNG PHẢI
        DO CỔNG:
        · README §4 hướng dẫn giáo viên chạy `python3 tools/gop_csv.py`, nhưng tệp đó NẰM NGOÀI
          repo (ở thư mục cha). Giáo viên trường khác clone về, làm đúng từng chữ, và nhận
          "No such file or directory" ở đúng khâu cuối của tiết học. Gãy đúng mắt xích nhân rộng.
        · README §5 hứa "mẫu văn bản BGH trong `ho-so/`", nhưng repo không có thư mục ho-so/ và
          mẫu đó chưa từng được viết. Lời hứa xuất hiện ở HAI chỗ (README và proposal).
        Cả hai đều là: TÀI LIỆU HỨA MỘT ĐƯỜNG DẪN, ĐƯỜNG DẪN KHÔNG CÓ. Không cổng nào bắt được,
        vì mọi cổng khác đều đọc mã, không đọc lời hứa.

        VÌ SAO NGUY HIỂM: đây là thứ giáo viên và giám khảo làm theo ĐẦU TIÊN. Một lệnh fail thì
        mất lòng tin vào toàn bộ phần còn lại, dù phần đó đúng. Và nó chỉ lộ ra khi có người
        thật ở máy khác làm theo — tức là lộ ra đúng lúc tệ nhất.

        CÁCH KIỂM. Quét các đoạn trong dấu ` (backtick) của tài liệu, lấy token trông như đường
        dẫn (có phần mở rộng tệp, hoặc có dấu / và không chứa khoảng trắng), rồi kiểm tồn tại.
        Ba điểm phải nói rõ để không tạo dương tính giả:
        · Chấp nhận cả THƯ MỤC CHA: README §6 cố ý dẫn `ke-hoach-12-tiet.md` và ghi rõ "(thư mục
          cha)" — tệp đó nằm ngoài repo theo thiết kế, không phải lời hứa gãy.
        · Bỏ qua `out/`: đó là đầu ra do cổng sinh lúc chạy và đã nằm trong .gitignore, nên trên
          một bản clone sạch nó chưa tồn tại. Đòi nó tồn tại là đòi sai.
        · Chỉ nhận token CÓ phần mở rộng hoặc có dấu /, nên `python3`, `--ghi`, `<thư_mục>`
          (có dấu nhọn), `MX_MUC3.cham()` (có dấu ngoặc) đều không bị coi là đường dẫn.
        """
        import glob as _glob

        tai_lieu = ["README.md", "huong-dan-danh-gia.md"]
        tai_lieu += sorted(os.path.relpath(p, ROOT)
                           for p in _glob.glob(os.path.join(ROOT, "ho-so", "*.md")))
        # Đầu ra sinh lúc chạy, đã gitignore: trên bản clone sạch chưa có, đòi nó là đòi sai.
        BO_QUA = ("out/",)
        # Token trông như đường dẫn tệp. Cố ý hẹp: thà bỏ sót một cách viết lạ còn hơn bắt oan,
        # vì mỗi lần báo oan là một lần người đọc mất tin vào các cảnh báo thật (bài học G11b).
        RE_DDP = re.compile(
            r"^[\w.\-/]+/[\w.\-/]+$"                       # có dấu / : path/to/file.ext
            r"|^[\w\-]+\.(?:py|js|md|json|txt|html|css|csv|pdf|png|svg)$")  # hoặc tệp ở gốc

        cha = os.path.dirname(ROOT)

        # TÊN TỆP DO tools/gop_csv.py THẬT SỰ GHI RA — đọc từ mã, không gõ tay.
        # VÌ SAO BẮT BUỘC CÓ: bản đầu của cổng này coi MỌI đường dẫn trong tài liệu là thứ
        # phải tồn tại sẵn, và báo LỖI cho `nhatky_gop.csv`, `baocao_lop.csv`,
        # `baocao_ca_nhan.csv` — 14 dương tính giả trong lần chạy đầu. Ba tên đó là ĐẦU RA mà
        # lệnh gộp SINH RA; giáo viên không mở chúng trước khi chạy lệnh, họ chạy lệnh rồi mới
        # có tệp. Đòi chúng tồn tại sẵn là đòi sai, và một cổng báo oan thì tệ gần bằng cổng mù:
        # người đọc phải tự đi phân loại từng dòng, rồi dần dần bỏ qua cả cảnh báo thật
        # (đúng bài học G11b đã ghi trong dự án này).
        # NHƯNG không vì thế mà bỏ qua chúng. Đầu ra phải được kiểm theo CÁCH KHÁC và CHẶT HƠN:
        # xem G17c — tên tài liệu hứa phải do mã thật sự ghi, và ngược lại.
        py_gop = doc("tools/gop_csv.py")
        sinh_ra = set(re.findall(r'os\.path\.join\(outdir,\s*"([^"]+)"\)', py_gop))

        # TÊN TỆP APP TỰ CHO TẢI VỀ là TÊN ĐỘNG, không phải hằng số: js/app.js:711 ghép
        # `soiai_nhatky_${maLop||'lop'}_${Date.now()}.csv`. Nếu tài liệu viết một ví dụ tên tệp
        # như vậy thì không được coi là "hứa một tệp phải có sẵn trên đĩa". Lấy phần chữ cố định
        # đứng trước ${...} ngay trong mã JS — đọc từ mã chứ không gõ tay, để app đổi tên thì
        # cổng tự đổi theo (gõ tay là tạo bản sao thứ năm của một cái tên, đúng lỗi G14 canh).
        js_nguon = "\n".join(doc(p) for p in ("js/app.js", "js/engine.js")
                             if os.path.isfile(os.path.join(ROOT, p)))
        tien_to_app = set(re.findall(r"`([A-Za-z0-9_\-]+)\$\{[^`]*\.csv`", js_nguon))

        loi, da_kiem, tai_lieu_thieu = [], 0, []
        # MỌI tên .csv tài liệu nhắc, bất kể mã có ghi hay không. Xem chú thích ở chỗ thu thập.
        csv_doc_nhac = set()
        for f in tai_lieu:
            if not os.path.isfile(os.path.join(ROOT, f)):
                tai_lieu_thieu.append(f)
                continue
            for m in re.finditer(r"`([^`\n]+)`", doc(f)):
                for tok in re.split(r"\s+", m.group(1).strip()):
                    tok = tok.strip(".,;:")
                    # Bỏ qua: chuỗi rỗng, tuỳ chọn dòng lệnh (`--ghi`), placeholder có dấu nhọn
                    # (`<thư_mục>`), lời gọi hàm (`MX_MUC3.cham()`), và đầu ra đã gitignore (`out/`).
                    # `str.startswith` nhận được cả tuple nên một lời gọi là đủ cho BO_QUA.
                    if (not tok or tok.startswith("-") or tok.startswith("<")
                            or tok.startswith("(") or tok.startswith(BO_QUA)):
                        continue
                    if not RE_DDP.match(tok):
                        continue
                    ten_tron = tok.rsplit("/", 1)[-1]
                    # Thu MỌI tên .csv, kể cả tên mã KHÔNG ghi. Đây chính là chỗ bản cũ làm
                    # chết chiều 1 của G17c: bản cũ chỉ thêm token khi nó ĐÃ nằm trong sinh_ra,
                    # nên tập thu được luôn là tập con của sinh_ra, và phép
                    # `dau_ra_doc_nhac - sinh_ra` không thể khác rỗng — một nhánh kiểm tra không
                    # bao giờ có khả năng fail, tức code chết (Luật A, skill agentic-efficiency-loop).
                    # Tôi còn viết chú thích biện minh cho nó ("luôn rỗng nhưng vẫn giữ"), là cách
                    # tệ nhất: nó làm nhánh chết trông như đã được cân nhắc.
                    if ten_tron.endswith(".csv"):
                        csv_doc_nhac.add(ten_tron)
                    # Đầu ra của lệnh gộp, hoặc tên app tự cho tải về, thì không đòi tồn tại sẵn
                    # trên đĩa; G17c kiểm chúng theo cách khác và chặt hơn.
                    if ten_tron in sinh_ra or any(ten_tron.startswith(p) for p in tien_to_app):
                        continue
                    da_kiem += 1
                    if (not os.path.exists(os.path.join(ROOT, tok))
                            and not os.path.exists(os.path.join(cha, tok))):
                        loi.append(f"{f} -> `{tok}`")

        self.them("G17a", "mọi tệp tài liệu được cổng này quét đều tồn tại",
                  not tai_lieu_thieu,
                  f"{len(tai_lieu) - len(tai_lieu_thieu)}/{len(tai_lieu)} tệp tài liệu có thật"
                  if not tai_lieu_thieu
                  else f"thiếu chính tệp tài liệu: {tai_lieu_thieu}")

        self.them("G17b", "mọi đường dẫn ĐẦU VÀO mà tài liệu hứa đều tồn tại thật",
                  not loi,
                  f"{da_kiem} đường dẫn đầu vào được nhắc trong tài liệu, tất cả đều có thật "
                  f"(repo hoặc thư mục cha)" if not loi
                  else f"{len(loi)} đường dẫn ĐƯỢC HỨA MÀ KHÔNG CÓ: {loi} — giáo viên làm theo sẽ "
                       f"gặp 'No such file or directory'. Hoặc đưa tệp vào repo (`git add`), hoặc "
                       f"sửa tài liệu cho hết hứa. Đây đúng là lỗi đã xảy ra với tools/gop_csv.py "
                       f"và với lời hứa 'mẫu trong ho-so/'.")

        # G17c — ĐẦU RA phải khớp hai chiều giữa tài liệu và mã.
        # Kiểm hai chiều vì mỗi chiều bắt một lỗi khác nhau, và theo Luật A (mục 6 skill
        # agentic-efficiency-loop) một cổng tuyên bố "khớp nhau" mà chỉ kiểm một chiều thì chiều
        # còn lại là code chết — cổng vẫn in ĐẠT và không ai biết.
        #   chiều 1: tài liệu hứa một tệp đầu ra mà mã KHÔNG ghi -> giáo viên chạy lệnh xong
        #           không thấy tệp đó, tưởng mình làm sai.
        #   chiều 2: mã ghi ra một tệp mà tài liệu KHÔNG nhắc -> giáo viên không biết tệp đó để
        #           làm gì, và baocao_ca_nhan.csv (thứ dùng để viết nhận xét) có thể bị bỏ qua.
        # CẢ HAI CHIỀU ĐỀU ĐÃ ĐƯỢC CA PHÁ KIỂM CHỨNG (mutation ca 2 và ca 3). Chiều 1 từng chết
        # trong bản đầu và chỉ lộ ra khi ca phá 2 được dựng; xem chú thích ở chỗ thu thập.
        # Tên app tự cho tải về (tien_to_app) được loại khỏi chiều 1 vì đó là tên động ghép lúc
        # chạy, không có tệp nào tên như vậy tồn tại sẵn để mà đòi.
        loi_hua = sorted(csv_doc_nhac - sinh_ra
                         - {t for t in csv_doc_nhac
                            if any(t.startswith(p) for p in tien_to_app)})
        thieu_doc = sorted(sinh_ra - csv_doc_nhac)
        self.them("G17c", "tên tệp đầu ra khớp hai chiều giữa tài liệu và tools/gop_csv.py",
                  not loi_hua and not thieu_doc,
                  f"{len(sinh_ra)} tệp đầu ra ({sorted(sinh_ra)}) đều được tài liệu nói tới "
                  f"(tài liệu nhắc {len(csv_doc_nhac)} tên .csv), và tài liệu không hứa tệp nào "
                  f"mà mã không ghi"
                  if not loi_hua and not thieu_doc
                  else ("; ".join(filter(None, [
                            f"tài liệu hứa nhưng tools/gop_csv.py KHÔNG ghi: {loi_hua} — giáo viên "
                            f"chạy lệnh xong sẽ không thấy tệp đó và tưởng mình làm sai"
                            if loi_hua else "",
                            f"tools/gop_csv.py ghi nhưng tài liệu KHÔNG nhắc: {thieu_doc} — "
                            f"giáo viên sẽ không biết tệp đó dùng để làm gì" if thieu_doc else ""]))))

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
    NHOM = ["G1", "G2", "G3", "G4", "G6", "G7", "G8", "G9", "G10", "G11", "G12", "G13",
            "G14", "G15", "G16", "G17"]
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
