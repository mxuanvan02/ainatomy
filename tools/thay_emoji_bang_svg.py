#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Thay emoji bằng SVG sprite (Lucide) trong index.html — G2 của tools/nghiem_thu.py.

VÌ SAO: MASTER.md (skill ui-ux-pro-max) xếp "emoji làm biểu tượng" vào nhóm cần tránh,
yêu cầu dùng một bộ SVG nhất quán. Lucide có giấy phép ISC và đã được tải về
vendor/lucide/ (34 icon, 144 KB) nên app vẫn chạy offline từ USB.

QUY TẮC (để judge kiểm được, không mơ hồ):
  Emoji đóng vai trò BIỂU TƯỢNG trên phần tử cấu trúc/tương tác -> thay bằng SVG:
    nút (.btn, .chip), logo, tiêu đề h2/h3, và câu dẫn đầu đoạn (.nho chu2 có emoji mở đầu).
  Emoji nằm GIỮA câu như biểu cảm thân thiện với học sinh -> GIỮ LẠI.

Sprite được nội tuyến ngay sau <body> (không phải tệp riêng) vì giao thức file://
chặn truy vấn tài nguyên cục bộ ở một số trình duyệt do chính sách CORS.
"""
import os, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICON_DIR = ROOT / "vendor" / "lucide"
IDX = ROOT / "index.html"

# emoji (kèm variation selector nếu có) -> tên icon Lucide
MAP = {
    "🔍": "search", "🏠": "house", "🔒": "lock", "🏭": "factory", "🧪": "flask-conical",
    "🕵️": "search", "🕵": "search", "📊": "chart-column", "🔀": "git-branch",
    "📚": "book-open", "🧊": "box", "🖼️": "image", "🖼": "image", "💡": "lightbulb",
    "⚖": "scale", "📋": "clipboard-list", "🏁": "flag", "🤖": "bot", "🎯": "gauge",
    "⚡": "zap", "❓": "circle-help", "💥": "zap", "⚙️": "cpu", "⚙": "cpu",
    "✅": "check", "🚫": "x",
}
# icon cho từng nút theo id (ưu tiên hơn MAP vì cùng emoji có thể cần icon khác nhau)
THEO_ID = {
    "btn-nhamay": "factory", "btn-lab": "flask-conical", "btn-dautruong": "search",
    "btn-baocao": "chart-column", "btn-logic": "git-branch", "btn-kienthuc": "book-open",
    "btn-lab3d": "box", "btn-pipe3d": "git-branch", "btn-ve-home": "house",
    "btn-tao-dulieu": "database", "btn-huanluyen": "play", "btn-sosanh": "scale",
    "dt-btn-pre": "clipboard-list", "dt-btn-post": "flag", "dt-btn-luyen": "play",
    "lab3d-tao": "image", "lab3d-hoc": "play", "lab3d-danhgia": "gauge",
    "lab3d-nhe": "zap", "pipe3d-hong": "zap", "pipe3d-reset": "rotate-ccw",
    "nm-sinh": "cpu", "nm-xoa5": "rotate-ccw", "nm-can-cu": "check", "nm-bia": "x",
    "btn-gioithieu": "file-text",
}

EMOJI_RE = re.compile(
    r'[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF\uFE0F\u2B50\u2696\u2699\u26A0\u2139]'
)


def svg(name):
    return f'<svg class="ic" aria-hidden="true"><use href="#i-{name}"/></svg>'


def svg_to(name):
    return f'<svg class="ic to" aria-hidden="true"><use href="#i-{name}"/></svg>'


def dung_icon(ten):
    """Trả về tên icon, đảm bảo tệp SVG tồn tại."""
    if not (ICON_DIR / f"{ten}.svg").exists():
        raise SystemExit(f"❌ thiếu icon: {ten}.svg — tải thêm trước khi chạy script này")
    return ten


def build_sprite(needed):
    """Ghép sprite từ các tệp SVG đã tải, chỉ gồm icon thực sự dùng."""
    out = ['<!-- Sprite SVG Lucide (giấy phép ISC, xem vendor/lucide/LICENSE).',
           '     Nội tuyến trong HTML thay vì tệp riêng vì giao thức file:// bị CORS chặn',
           '     ở một số trình duyệt. Sinh tự động bằng tools/thay_emoji_bang_svg.py —',
           '     KHÔNG sửa tay; sửa bằng cách chạy lại script. -->',
           '<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">']
    for name in sorted(needed):
        raw = (ICON_DIR / f"{name}.svg").read_text(encoding="utf-8")
        # bỏ comment giấy phép và thẻ <svg ...> mở, lấy phần ruột
        raw = re.sub(r'<!--.*?-->', '', raw, flags=re.S)
        m = re.search(r'<svg[^>]*>(.*)</svg>', raw, re.S)
        if not m:
            raise SystemExit(f"❌ không đọc được ruột của {name}.svg")
        inner = re.sub(r'\s+', ' ', m.group(1)).strip()
        out.append(f'  <symbol id="i-{name}" viewBox="0 0 24 24">{inner}</symbol>')
    out.append('</svg>')
    return "\n".join(out)


def main():
    html = IDX.read_text(encoding="utf-8")
    orig = html
    dung = set()          # icon thực sự dùng
    thay = []             # log từng chỗ thay

    def ghi(noi, icon):
        thay.append(f"{noi} -> {icon}")

    # ---------- 1. nút .menu-o : chèn icon + bọc chữ vào <div> (CSS mới là flex) ----------
    def menuo(m):
        attrs, body = m.group(1), m.group(2)
        mid = re.search(r'id="([\w-]+)"', attrs)
        bid = mid.group(1) if mid else ""
        # icon: ưu tiên theo id, sau đó theo emoji đầu tiên trong body
        icon = None
        if bid in THEO_ID:
            icon = THEO_ID[bid]
        else:
            e = EMOJI_RE.search(body)
            if e and e.group(0) in MAP:
                icon = MAP[e.group(0)]
        icon = dung_icon(icon) if icon else "box"
        dung.add(icon)
        ghi(f"menu-o#{bid or '?'}", icon)
        # xoá emoji + variation selector ở đầu các thẻ con
        sach = EMOJI_RE.sub("", body)
        sach = re.sub(r'\s+', ' ', sach).strip()
        # tách <b>...</b> và <span class="chu2">...</span>
        mb = re.search(r'<b>(.*?)</b>', sach, re.S)
        ms = re.search(r'<span class="chu2">(.*?)</span>', sach, re.S)
        ten = mb.group(1).strip() if mb else sach
        mo = ms.group(1).strip() if ms else ""
        out = (f'<button class="btn menu-o"{attrs}>\n'
               f'        {svg_to(icon)}\n'
               f'        <div><b>{ten}</b>')
        if mo:
            out += f'\n        <span class="chu2">{mo}</span>'
        out += '</div>\n      </button>'
        return out

    html = re.sub(r'<button class="btn menu-o"([^>]*)>(.*?)</button>', menuo, html, flags=re.S)

    # ---------- 2. các nút khác: thay emoji dẫn đầu bằng icon ----------
    def nut(m):
        attrs, body = m.group(1), m.group(2)
        e = EMOJI_RE.search(body)
        if not e:
            return m.group(0)
        mid = re.search(r'id="([\w-]+)"', attrs)
        bid = mid.group(1) if mid else ""
        icon = THEO_ID.get(bid) or MAP.get(e.group(0))
        if not icon:
            return m.group(0)
        icon = dung_icon(icon)
        dung.add(icon)
        ghi(f"button#{bid or body.strip()[:24]}", icon)
        # xoá MỌI emoji + variation selector trong nút
        sach = EMOJI_RE.sub("", body)
        sach = re.sub(r'[ \t]{2,}', ' ', sach)
        # chèn icon ngay sau thẻ mở
        return f'<button{attrs}>{svg(icon)}{sach}</button>'

    html = re.sub(r'<button(?![^>]*class="btn menu-o")([^>]*)>(.*?)</button>', nut, html, flags=re.S)

    # ---------- 3. logo ----------
    def logo(m):
        inner = m.group(1)
        e = EMOJI_RE.search(inner)
        icon = "search"
        dung.add(icon)
        ghi("logo", icon)
        sach = EMOJI_RE.sub("", inner).strip()
        return f'<div class="logo">{svg_to(icon)}<span class="logo-txt">{sach}</span></div>'
    html = re.sub(r'<div class="logo">(.*?)</div>', logo, html, flags=re.S)

    # ---------- 4. tiêu đề h2/h3 dẫn đầu bằng emoji ----------
    def heading(m):
        tag, body = m.group(1), m.group(2)
        e = EMOJI_RE.search(body)
        if not e or e.start() > 3:      # chỉ xử lí emoji DẪN ĐẦU tiêu đề
            return m.group(0)
        icon = MAP.get(e.group(0))
        if not icon:
            return m.group(0)
        icon = dung_icon(icon)
        dung.add(icon)
        ghi(f"{tag}", icon)
        sach = EMOJI_RE.sub("", body).strip()
        return f'<{tag}>{svg_to(icon)} {sach}</{tag}>'
    html = re.sub(r'<(h2|h3)>(.*?)</\1>', heading, html, flags=re.S)

    # ---------- 5. câu dẫn đầu đoạn (.nho chu2) có emoji mở đầu ----------
    def doan(m):
        body = m.group(1)
        s = body.strip()
        e = EMOJI_RE.search(s)
        if not e or e.start() > 2:          # chỉ xử lí emoji DẪN ĐẦU câu
            return m.group(0)
        icon = MAP.get(e.group(0))
        if not icon:
            return m.group(0)
        icon = dung_icon(icon)
        dung.add(icon)
        ghi("p.nho.chu2", icon)
        sach = EMOJI_RE.sub("", s).strip()
        return f'<p class="nho chu2">{svg(icon)} {sach}</p>'
    html = re.sub(r'<p class="nho chu2">(.*?)</p>', doan, html, flags=re.S)

    # ---------- 6. nhãn dẫn đầu trong <div class="nho chu2"> ----------
    def nhan(m):
        body = m.group(1)
        e = EMOJI_RE.search(body)
        if not e or e.start() > 2:
            return m.group(0)
        icon = MAP.get(e.group(0))
        if not icon:
            return m.group(0)
        icon = dung_icon(icon)
        dung.add(icon)
        ghi("div.nho.chu2", icon)
        return f'<div class="nho chu2" style="margin-bottom:8px">{svg(icon)} {EMOJI_RE.sub("", body).strip()}</div>'
    html = re.sub(r'<div class="nho chu2" style="margin-bottom:8px">(.*?)</div>', nhan, html, flags=re.S)

    # ---------- 7. chèn sprite sau <body> ----------
    sprite = build_sprite(dung)
    html = re.sub(r'(<body>)', r'\1\n' + sprite.replace('\\', '\\\\'), html, count=1)

    IDX.write_text(html, encoding="utf-8")

    # ---------- VERIFY ----------
    print(f"đã thay {len(thay)} chỗ, dùng {len(dung)} icon khác nhau")
    for t in thay:
        print("   ", t)

    ids = set(re.findall(r'symbol id="(i-[\w-]+)"', html))
    uses = set(re.findall(r'<use[^>]*href="#(i-[\w-]+)"', html))
    mo_coi = sorted(uses - ids)
    print(f"\nsymbol: {len(ids)} | use: {len(uses)} | mồ côi: {mo_coi or 'không'}")

    # emoji còn lại trong <button> và .logo
    nut = re.findall(r"<button[^>]*>(.*?)</button>", html, re.S)
    con = []
    for b in nut:
        sach = re.sub(r"<svg.*?</svg>", "", b, flags=re.S)
        e = EMOJI_RE.findall(sach)
        if e:
            con.append("".join(e) + " " + re.sub(r"<[^>]+>", "", sach).strip()[:30])
    print(f"emoji còn trong <button>: {len(con)}" + (f" -> {con[:6]}" if con else ""))
    lg = re.findall(r'<div class="logo">(.*?)</div>', html, re.S)
    lg_e = [EMOJI_RE.findall(x) for x in lg]
    print(f"emoji còn trong .logo: {[x for x in lg_e if x] or 'không'}")

    emoji_con_lai = EMOJI_RE.findall(html)
    print(f"\ntổng emoji còn lại trong file (kể cả trong câu văn thân thiện): {len(emoji_con_lai)}")

    ok = (not mo_coi) and (not con) and (not any(lg_e)) and (html != orig)
    print("\nKẾT LUẬN:", "ĐẠT" if ok else "CHƯA ĐẠT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
