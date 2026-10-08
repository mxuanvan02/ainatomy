#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""TEST XSS cho duyet_nhan.html — chạy esc() THẬT của trang đã sinh, bằng node.

VÌ SAO CÓ TỆP NÀY. `duyet_nhan.html` dựng DOM bằng innerHTML và nội dung đưa vào có hai nguồn
KHÔNG tin cậy được:
  (1) câu hỏi do LLM sinh ra (claims, giaiThich, boiCanh) trong data/cauhoi_moRong.js;
  (2) ghi chú do chính người duyệt gõ vào ô textarea.
Nên "đã thoát HTML" không được là một lời khẳng định trong comment — nó phải là một phép thử
chạy được. Luật C/5v (skill agentic-efficiency-loop): một phép kiểm chưa từng FAIL thì chưa được
chứng minh là nó CÓ THỂ fail.

CÁCH THỬ, và vì sao cách này: KHÔNG chép hàm esc() vào đây rồi thử bản chép. Chép ra là thử một bản
sao, và bản sao thì luôn khớp — đúng lớp lỗi "ĐẠT GIẢ" mà repo này đã trả giá (G11b, G14a, Luật 5l).
Thay vào đó: BỐC hàm esc() RA TỪ CHÍNH TỆP duyet_nhan.html đã sinh, rồi chạy nó bằng node. Nếu ai đó
sửa esc() trong trang cho lỏng ra, phép thử này kêu — nó đo artifact thật, không đo ý định.

NĂM VECTOR, mỗi cái bắt một kiểu thoát khác nhau:
  V1  thoát khỏi CHUỖI trong thuộc tính nháy kép:  "><img src=x onerror=alert(1)>
  V2  thoát khỏi thuộc tính nháy đơn:              ' onload='alert(1)
  V3  BREAKOUT KHỎI KHỐI <script>:                </script><img src=x onerror=alert(1)>
  V4  thẻ thẳng:                                  <script>alert(1)</script>
  V5  entity lồng (kiểm thoát dấu &):             &lt;script&gt;alert(1)&lt;/script&gt;

TIÊU CHÍ "HỞ" — và bản đầu của tệp này đã làm SAI, đáng ghi lại:
Bản đầu tìm "thẻ sống" bằng mẫu `<\s*(script|img|…)` và tìm "handler" bằng mẫu `\bon\w+\s*=`.
Chạy ra báo HỞ cả V1, V2, V3 — trong khi esc() hoàn toàn đúng: V1 trả về
`&quot;&gt;&lt;img src=x onerror=alert(1)&gt;`, KHÔNG có thẻ nào sống vì dấu `<` đã thành `&lt;`.
Mẫu `\bon\w+\s*=` vẫn khớp chữ `onerror=` đang là TEXT TRƠ. Một handler chỉ nguy hiểm khi nó nằm
TRONG một thẻ thật, tức phải có dấu `<` THÔ đứng trước; tìm chữ "onerror" mà không tìm thẻ sống là
kiểm sai đối tượng.
Đây là lần thứ năm trong dự án một phép kiểm do chính tôi viết báo oan (G17b, G17d, mục [14],
verify_so_ngan_hang.py) và là lần thứ hai TRONG CÙNG MỘT NGÀY với cùng một gốc: suy kết luận từ
CHỮ trong kết quả thay vì từ CẤU TRÚC thật.

Tiêu chí đúng: sau khi thoát, đầu ra KHÔNG được còn bất kỳ ký tự THÔ nào trong `< > " '`, và mọi
dấu `&` còn lại phải mở đầu một entity hợp lệ. Đó là điều kiện cần và đủ để không breakout được
khỏi chuỗi, khỏi thuộc tính, và khỏi thẻ.

MỤC D là ĐỐI CHỨNG CHO CHÍNH PHÉP THỬ NÀY: chạy đúng bộ kiểm trên ba hàm esc() CỐ Ý HỎNG và đòi nó
phải kêu. Thiếu mục này thì "esc() an toàn" và "bộ kiểm đang mù" trông giống hệt nhau — cả hai đều
cho ra màn hình xanh.

CÁCH CHẠY:  python3 tools/tests/xss_duyet_nhan.py       (cần node; thoát 2 nếu thiếu)
"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRANG = os.path.join(ROOT, "duyet_nhan.html")

PAYLOADS = [
    ("V1 thuộc tính nháy kép", '"><img src=x onerror=alert(1)>'),
    ("V2 thuộc tính nháy đơn", "' onload='alert(1)"),
    ("V3 breakout </script>", "</script><img src=x onerror=alert(1)>"),
    ("V4 thẻ thẳng", "<script>alert(1)</script>"),
    ("V5 entity lồng", "&lt;script&gt;alert(1)&lt;/script&gt;"),
]

# Entity mà esc() được phép sinh ra. Mọi dấu `&` trong đầu ra phải mở đầu một trong các dạng này.
ENTITY_HOP_LE = re.compile(r"&(?:amp|lt|gt|quot|#39);")

# Bốn ký tự thô mà nếu còn sót thì breakout được. Không có `&` ở đây: một dấu `&` đơn lẻ không
# nguy hiểm (trình duyệt in nó ra nguyên văn), nhưng nó phải là entity hợp lệ nếu esc() muốn đúng.
KY_TU_NGUY_HIEM = ('<', '>', '"', "'")


def esc_hong(out):
    """Trả về danh sách lý do đầu ra của esc() còn HỞ; rỗng nghĩa là an toàn."""
    loi = []
    for c in KY_TU_NGUY_HIEM:
        if c in out:
            loi.append(f"còn ký tự thô {c!r}")
    for m in re.finditer(r"&", out):
        if not ENTITY_HOP_LE.match(out, m.start()):
            loi.append(f"dấu & ở vị trí {m.start()} không mở đầu entity hợp lệ")
            break
    return loi


def boc_ham_esc(html):
    """Bốc NGUYÊN VĂN hàm esc() từ tệp đã sinh — không chép bản sao."""
    m = re.search(r"const esc = .*?;\n", html, re.S)
    if not m:
        raise SystemExit("!!! không tìm thấy `const esc = …` trong duyet_nhan.html — trang đã đổi cấu trúc?")
    return m.group(0).strip()


def chay_esc(nguon_esc):
    """Chạy một hàm esc() (nguồn JS) trên mọi payload bằng node. Trả list chuỗi đã thoát."""
    script = (nguon_esc + "\nconst PAYLOADS = "
              + json.dumps([p for _, p in PAYLOADS])
              + ";\nconsole.log(JSON.stringify(PAYLOADS.map(p => esc(p))));\n")
    tmp = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
    tmp.write(script)
    tmp.close()
    try:
        r = subprocess.run(["node", tmp.name], capture_output=True, text=True, timeout=60)
    finally:
        os.unlink(tmp.name)
    if r.returncode != 0:
        raise SystemExit("!!! chạy esc() bằng node thất bại: " + r.stderr.strip()[:300])
    return json.loads(r.stdout.strip())


def main():
    if not os.path.isfile(TRANG):
        print(f"!!! chưa có {TRANG}")
        print("    Sinh trước bằng: python3 tools/sinh_trang_duyet_nhan.py --ghi")
        return 2

    if subprocess.run(["node", "--version"], capture_output=True).returncode != 0:
        print("!!! không có `node` — KHÔNG thử được hàm esc() thật của trang.")
        print("    Thoát mã 2 chứ không trả 0: một phép kiểm không chạy được mà vẫn báo sạch")
        print("    là phép kiểm bị vô hiệu (Luật 5d).")
        return 2

    html = io.open(TRANG, encoding="utf-8").read()
    esc_src = boc_ham_esc(html)
    print("=" * 96)
    print("TEST XSS — chạy esc() THẬT bốc từ duyet_nhan.html")
    print("=" * 96)
    print("  hàm esc() trong tệp đang thử:")
    for ln in esc_src.split("\n"):
        print("    | " + ln[:112])

    loi = []
    ket_qua = chay_esc(esc_src)

    # ------------------------------------------------------- A. esc() thật trên 5 vector
    print("\n--- A. esc() thật có chặn được breakout không (5 vector) ---")
    for (ten, payload), out in zip(PAYLOADS, ket_qua):
        ho = esc_hong(out)
        tot = not ho
        if not tot:
            loi.append(f"{ten}: esc() trả về {out[:90]!r} — {'; '.join(ho)}")
        print(f"  {'OK  ' if tot else '<<< HỞ'} {ten:26s} -> {out[:80]}")
        if not tot:
            print(f"        lý do: {'; '.join(ho)}")

    # ------------------------------------------- B. breakout khỏi <script> khi NHÚNG JSON
    # Đây là phép thử cho chính tệp đã sinh, không phải cho esc(): khối `const ITEMS = [...]` nằm
    # TRONG <script>, nên một dấu `<` thô ở đó có thể đóng sớm khối script. esc() không cứu được
    # chỗ này vì nó chỉ chạy khi dựng DOM, còn trình duyệt parse HTML trước đó.
    print("\n--- B. dữ liệu nhúng trong <script> có dấu `<` thô không (breakout) ---")
    m = re.search(r"const ITEMS = (\[.*?\]);\nconst NHAN_LOAI_LOI", html, re.S)
    if not m:
        loi.append("không định vị được khối `const ITEMS = …` để kiểm breakout")
        print("  !!! không định vị được khối ITEMS")
    else:
        khoi = m.group(1)
        parsed = None          # gán TRƯỚC try: nếu không thì nhánh except để biến chưa tồn tại
        try:
            parsed = json.loads(khoi)
            json_ok = True
        except json.JSONDecodeError as e:
            json_ok = False
            loi.append(f"khối ITEMS không parse được thành JSON: {e}")
        dau_nho = khoi.count("<")
        tot = json_ok and dau_nho == 0
        if not tot:
            loi.append(f"khối ITEMS chứa {dau_nho} dấu `<` thô — </script> trong dữ liệu sẽ breakout")
        so_item = len(parsed) if parsed is not None else "?"
        print(f"  {'OK  ' if tot else '<<< HỞ'} khối ITEMS: {so_item} item · dấu `<` thô = {dau_nho} (phải 0)")

    # ------------------------------------------------- C. payload THẬT có trong dữ liệu không
    print("\n--- C. dữ liệu thật đang nhúng có payload nào không (đối chứng) ---")
    if m:
        hits = [ten for ten, p in PAYLOADS if p in m.group(1)]
        print(f"  {'OK  ' if not hits else '<<<'} payload xuất hiện trong dữ liệu thật: {hits or 'không có'}")
        if hits:
            loi.append(f"dữ liệu thật chứa payload: {hits}")

    # --------------------------------- D. ĐỐI CHỨNG CHO CHÍNH PHÉP THỬ NÀY (Luật C + Luật 5v)
    # Mục A/B/C vừa báo "an toàn". Nhưng nếu esc_hong() hỏng thì nó báo an toàn cho MỌI hàm esc,
    # kể cả hàm không thoát gì — và đó là ĐẠT GIẢ, loại lỗi nguy hiểm nhất vì không ai đi kiểm lại.
    # Nên chạy đúng bộ kiểm đó trên ba hàm esc() CỐ Ý HỎNG và ĐÒI NÓ PHẢI KÊU.
    # Đây cũng là cách chứng minh mục A có ý nghĩa: cùng một bộ kiểm, đầu vào hỏng thì kêu.
    print("\n--- D. ĐỐI CHỨNG: bộ kiểm này CÓ THỂ fail không? (3 hàm esc() cố ý hỏng) ---")
    ESC_HONG = [
        ("không thoát gì",
         'const esc = s => String(s == null ? "" : s);'),
        ("chỉ thoát < >",
         'const esc = s => String(s).replace(/[<>]/g, c => (c === "<" ? "&lt;" : "&gt;"));'),
        ("thiếu nháy đơn",
         'const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",'
         '">":"&gt;",\'"\':"&quot;"}[c]));'),
    ]
    for ten, nguon in ESC_HONG:
        try:
            kq = chay_esc(nguon)
        except SystemExit as e:
            loi.append(f"đối chứng {ten}: không chạy được — {e}")
            print(f"  !!! {ten}: không chạy được")
            continue
        so_hong = sum(1 for o in kq if esc_hong(o))
        tot = so_hong > 0
        if not tot:
            loi.append(f"đối chứng {ten}: bộ kiểm KHÔNG kêu — esc_hong() đang MÙ, kết quả mục A vô nghĩa")
        print(f"  {'OK  ' if tot else '<<< MÙ'} esc() {ten:18s} -> {so_hong}/{len(kq)} vector bị bắt (phải >0)")

    print("\n" + "=" * 96)
    if loi:
        print(f"LỖI — {len(loi)} vấn đề:")
        for l in loi:
            print("  !", l)
        return 1
    print("OK — esc() thật của trang chặn cả 5 vector, khối dữ liệu nhúng không cho breakout,")
    print("     và bộ kiểm này ĐÃ được chứng minh là kêu được trên 3 hàm esc() cố ý hỏng.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
