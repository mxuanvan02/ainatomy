#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho html_song() — chứng minh cổng không ĐẠT GIẢ vì chữ trong chú thích HTML.

VẤN ĐỀ ĐÃ XẢY RA THẬT (07/10). Tôi thêm một chú thích dài vào index.html để giải thích vì sao
xoá phần tử chết #btn-dangnhap; trong chú thích có nhắc `js/app.js`. Ngay lập tức:
· Cổng G8d đo thứ tự nạp script bằng `idx.find("js/app.js")` bắt đúng chữ trong chú thích ở vị
  trí 7811, trong khi thẻ <script src="js/app.js"> thật nằm ở 44048 → cổng BÁO OAN rằng app.js
  nạp trước kichban.js. Sản phẩm không hỏng, phép kiểm hỏng.
· Tệ hơn, tôi phát hiện cùng lớp lỗi đó ở CHIỀU NGƯỢC LẠI và nó nguy hiểm hơn: G11e và G15b
  kiểm sự tồn tại của thẻ bằng `f'id="{i}"' not in idx` trên tệp THÔ. Chỉ cần một chú thích nào
  đó chép ra chuỗi `id="kt-bt13"` là cổng ĐẠT dù THẺ THẬT ĐÃ BỊ XOÁ. Báo oan thì có người đi
  cãi; ĐẠT GIẢ thì không ai kiểm tra lại, và lỗ hổng nằm im tới lúc học sinh bấm nút không thấy
  gì.

ĐÃ SỬA: thêm html_song() (lột `<!-- ... -->`) và chuyển 7 phép kiểm sang dùng nó —
G2a, G3e, G6a, G8c, G8d, G8e, G10b, G10d, G11a/G11e, G15b.

TEST NÀY CHỨNG MINH HAI CHIỀU, vì sửa một chiều thì dễ làm hỏng chiều kia:
  A. KHÔNG MÙ HƠN: thẻ thật còn nguyên thì cổng phải ĐẠT (CA 0 — nguyên trạng 69/69).
  B. CÓ RĂNG HƠN: thẻ thật bị xoá nhưng chú thích vẫn chứa chuỗi id đó thì cổng phải KÊU.
     Đây là ca quyết định: nếu cổng vẫn ĐẠT thì html_song() vô tác dụng.
  C. So sánh trực tiếp hai phép đo trên CÙNG một tệp đã phá, để chỉ ra bản thô cho kết quả
     SAI còn bản lột cho kết quả ĐÚNG — bằng chứng giải thích vì sao bản sửa là cần thiết.

Bước chuẩn bị: sinh lại manifest TRƯỚC CA 0 và in rõ. Lý do: chính tools/nghiem_thu.py nằm
trong manifest, nên mỗi lần sửa cổng là G13b kêu và CA 0 đỏ vì lý do không phải lỗi sản phẩm.
Đã mất hai lần chạy vì đọc nhầm CA 0 đỏ thành "cổng hỏng" (Luật B, skill agentic-efficiency-loop).

Khôi phục bằng bản sao BYTES trong /tmp, không dùng `git checkout`: cây đang có thay đổi chưa
commit, git checkout sẽ trả về bản đã commit và XOÁ MẤT công sửa.
"""
import glob
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GATE = ["python3", "tools/nghiem_thu.py"]
IDX = "index.html"
TOUCH = [IDX, "SHA256SUMS.txt"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sinh_manifest():
    r = subprocess.run([sys.executable, "tools/sinh_manifest.py", "--ghi"],
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    dong = [l.strip() for l in r.stdout.splitlines() if "ĐÃ GHI" in l]
    print(f"  [chuẩn bị] sinh lại manifest (rc={r.returncode}): "
          + (dong[-1] if dong else r.stdout.strip()[:80]))
    for f in glob.glob(os.path.join(ROOT, "SHA256SUMS.txt.bak-*")):
        os.replace(f, os.path.join(tempfile.gettempdir(), os.path.basename(f)))


def chay_cong():
    r = subprocess.run(GATE, cwd=ROOT, capture_output=True, text=True, timeout=900)
    return r.returncode, r.stdout + r.stderr


def ca(so, ten, sua, ma_cong):
    p = os.path.join(ROOT, IDX)
    goc = open(p, encoding="utf-8").read()
    h0 = sha(p)
    try:
        moi = sua(goc)
        assert moi != goc, f"không phá được {IDX} ({ten}) — NEO SAI, đọc tệp thật trước đã"
        open(p, "w", encoding="utf-8").write(moi)

        # (C) so sánh hai phép đo trên CÙNG tệp đã phá
        tho = moi
        lot = re.sub(r"<!--.*?-->", " ", moi, flags=re.S)
        print(f"  [{so}] {ten}")
        for chuoi in ma_cong["chuoi_kiem"]:
            in_tho = chuoi in tho
            in_lot = chuoi in lot
            print(f"       chuỗi {chuoi!r}: bản THÔ={'CÓ' if in_tho else 'không'} · "
                  f"bản LỘT={'CÓ' if in_lot else 'không'}"
                  + ("   <- bản thô cho kết quả SAI (đạt giả)" if (in_tho and not in_lot) else ""))

        rc, out = chay_cong()
        keu = f"[LỖI] {ma_cong['ma']}" in out
        tt = ("BẮT ĐƯỢC" if keu else
              ("KÊU NHƯNG SAI MÃ" if rc != 0 else "IM (KHÔNG RĂNG)"))
        print(f"       cổng {ma_cong['ma']}: rc={rc}  {tt}")
        if tt != "BẮT ĐƯỢC":
            for l in out.splitlines():
                if "KẾT QUẢ" in l or "[LỖI]" in l or ma_cong["ma"] in l:
                    print("       | " + l.strip()[:165])
        return tt == "BẮT ĐƯỢC"
    finally:
        open(p, "w", encoding="utf-8").write(goc)
        khop = sha(p) == h0
        print(f"       khôi phục {IDX}: hash {'KHỚP gốc' if khop else 'LỆCH !!!'}")
        if not khop:
            print("       !!! DỪNG: tệp không về nguyên trạng.")
            sys.exit(9)


def main():
    print("=" * 96)
    print("MUTATION TEST html_song() — cổng không được ĐẠT GIẢ vì chữ trong chú thích")
    print("=" * 96)
    sinh_manifest()
    tmp = tempfile.mkdtemp(prefix="htmlsong-")
    for f in TOUCH:
        shutil.copy2(os.path.join(ROOT, f), os.path.join(tmp, f.replace("/", "_")))
        print(f"  backup {f} sha={sha(os.path.join(ROOT, f))[:12]}")

    print("\n[CA 0] nguyên trạng — cổng phải ĐẠT (chứng minh html_song không làm cổng MÙ)")
    rc, out = chay_cong()
    ket = [l for l in out.splitlines() if "KẾT QUẢ" in l]
    print(f"       rc={rc}  {ket[0] if ket else '?'}")
    if rc != 0:
        print("       !!! nguyên trạng đã đỏ: sửa trước khi mutation test.")
        for l in out.splitlines():
            if "[LỖI]" in l:
                print("       | " + l.strip()[:160])
        return 1

    kq = []
    print()

    # ---- CA 1: xoá thẻ THẬT id="kt-bt13" nhưng để lại một CHÚ THÍCH chứa đúng chuỗi đó ----
    # Nếu cổng đọc tệp thô thì chú thích đủ làm nó ĐẠT (đạt giả). Đọc bản lột thì phải KÊU.
    def xoa_the_giu_comment(s):
        assert 'id="kt-bt13"' in s, "neo sai: index.html không còn id=\"kt-bt13\""
        m = re.search(r'<div[^>]*id="kt-bt13"[^>]*>\s*</div>', s)
        assert m, "neo sai: không thấy thẻ <div ... id=\"kt-bt13\" ...></div>"
        moi = ('<!-- MỒI ĐẠT GIẢ: thẻ thật đã bị xoá bên dưới, nhưng chú thích này vẫn chép\n'
               '     nguyên văn chuỗi id="kt-bt13" để thử xem cổng có bị lừa không. -->\n')
        return s[:m.start()] + moi + s[m.end():]
    kq.append(ca(1, "xoá thẻ THẬT id=\"kt-bt13\", để chú thích chứa id đó (G11e)",
                 xoa_the_giu_comment,
                 {"ma": "G11e", "chuoi_kiem": ['id="kt-bt13"']}))

    # ---- CA 2: xoá thẻ THẬT id="nm-tram1" nhưng để chú thích chứa id đó ----
    # Cùng lớp lỗi, cổng khác (G15b). Chính tôi đã viết chú thích dài trong index.html nhắc tới
    # các id nm-tram*, nên đây là ca có thật trong repo chứ không phải giả định.
    def xoa_tram_giu_comment(s):
        assert 'id="nm-tram1"' in s, "neo sai: index.html không còn id=\"nm-tram1\""
        m = re.search(r'<div class="card" id="nm-tram1"[^>]*>', s)
        assert m, "neo sai: không thấy thẻ <div class=\"card\" id=\"nm-tram1\">"
        # chỉ đổi id của thẻ mở (giữ phần còn lại để tệp vẫn parse được), và chèn chú thích mồi
        moi = ('<!-- MỒI ĐẠT GIẢ cho G15b: id="nm-tram1" vẫn xuất hiện ở đây -->\n'
               '<div class="card" id="nm-tram1-DA-BI-DOI-TEN" style="display:none">')
        return s[:m.start()] + moi + s[m.end():]
    kq.append(ca(2, "xoá thẻ THẬT id=\"nm-tram1\", để chú thích chứa id đó (G15b)",
                 xoa_tram_giu_comment,
                 {"ma": "G15b", "chuoi_kiem": ['id="nm-tram1"']}))

    # ---- CA 3: biến thẻ nạp nhamay_tram01.js THÀNH chú thích ----
    # Thẻ không còn là mã nữa, nhưng chuỗi src="..." vẫn nằm trong tệp. G3e phải kêu.
    def comment_hoa_the_nap(s):
        target = '<script src="js/nhamay_tram01.js"></script>'
        assert target in s, f"neo sai: không thấy {target}"
        return s.replace(target, "<!-- " + target + " -->", 1)
    kq.append(ca(3, "biến thẻ nạp nhamay_tram01.js thành chú thích (G3e)",
                 comment_hoa_the_nap,
                 {"ma": "G3e", "chuoi_kiem": ['src="js/nhamay_tram01.js"']}))

    print("\n" + "=" * 96)
    print(f"KẾT LUẬN: {sum(kq)}/{len(kq)} ca phá đều bị bắt — html_song() có tác dụng thật")
    for i, o in enumerate(kq, 1):
        print(f"  ca {i}: {'BẮT ĐƯỢC' if o else 'CỔNG VẪN ĐẠT GIẢ — html_song() chưa diệt được lỗi'}")
    print("=" * 96)
    rc, out = chay_cong()
    ket = [l for l in out.splitlines() if "KẾT QUẢ" in l]
    print(f"XÁC NHẬN SAU CÙNG: rc={rc}  {ket[0] if ket else '?'}   (phải về ĐẠT)")
    shutil.rmtree(tmp)
    return 0 if (all(kq) and rc == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
