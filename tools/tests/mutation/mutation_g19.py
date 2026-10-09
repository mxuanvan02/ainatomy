#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST CỔNG G19 — ba ca tính điểm (hai ca phá + một ca đối chứng âm),
kèm một bước baseline không tính điểm.

VÌ SAO CÓ TỆP NÀY. G19 thêm ngày 09/10 để canh lời khai "0 lượt gọi mạng khi chạy
(app offline hoàn toàn)" trong ho-so/video_brief.md — một câu sẽ được ĐỌC THÀNH LỜI
cho giám khảo mà trước đó KHÔNG tiêu chí nào canh. Nhưng cổng mới mà chưa có
mutation test thì chỉ là một lời khai khác: nó ĐẠT ngay lần chạy đầu chưa chứng minh
nó thấy được gì. Repo này đã có tiền lệ một cổng in ĐẠT trong khi mù (G14c một
chiều là code chết), nên G19 phải được chứng minh là CÓ RĂNG bằng ca phá.

CÁCH PHÁ: tạo một TỆP THĂM DÒ rồi xoá (theo khuôn mutation_g18.py, không sửa công
cụ thật), vì G19a quét MỌI tệp .js trong js/ nên một tệp mới đủ để nó nhìn thấy;
khôi phục bằng cách xoá tệp và kiểm chứng "tệp không còn tồn tại" — chắc hơn so
khớp hash. Riêng ca 3 phải đụng index.html nên dùng hash khôi phục.

CA 0 (baseline, KHÔNG tính điểm) — repo nguyên trạng thì G19a/b/c phải ĐẠT cả ba.
Nếu baseline đã đỏ thì mọi ca bên dưới vô nghĩa, script dừng ngay với mã 1: một bộ
mutation chạy trên nền cổng đang đỏ chỉ đo được tiếng ồn.

BA CA TÍNH ĐIỂM:
  CA 1 — tệp thăm dò js/ chứa `fetch(...)` trong MÃ SỐNG           -> G19a PHẢI kêu
  CA 2 — tệp thăm dò js/ chứa `fetch(...)` CHỈ TRONG COMMENT        -> G19a PHẢI IM
         (đối chứng âm: đây đúng là tình huống đã xảy ra thật khi viết G19 — chính em
          viết một comment giải thích có chứa chữ fetch("https://huggingface.co"...) và
          grep thô báo 1 lệnh gọi mạng ở đúng dòng comment đó. Nếu cổng dùng grep thô
          thì ca này ĐỎ, và cổng sẽ đỏ vĩnh viễn vì chính comment ghi lại bài học.)
  CA 3 — index.html trỏ src tới một tệp .js KHÔNG TỒN TẠI          -> G19b PHẢI kêu

CA 2 là ca quan trọng nhất: một cổng chỉ biết kêu mà không biết im thì sẽ bị tắt đi,
và tắt đi thì bằng không có cổng. G19c không có ca phá riêng — nó cùng luật đo với
G19a/G6a (quét src/href ra mạng trên mã sống) và đã được G6a chứng minh bằng mutation
trước đó; thêm một ca phá cho nó chỉ là lặp lại cùng một phép thử trên tệp khác.

CÁCH CHẠY:  python3 tools/tests/mutation/mutation_g19.py
"""
import hashlib
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CONG = os.path.join(REPO, "tools", "nghiem_thu.py")
IDX = os.path.join(REPO, "index.html")
THAM_DO = os.path.join(REPO, "js", "zz_tham_do_mutation_g19.js")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong(nhom="G19"):
    r = subprocess.run([sys.executable, CONG, nhom], cwd=REPO,
                       capture_output=True, text=True, timeout=400)
    return r.returncode, r.stdout + r.stderr


def ket(out, ma):
    for ln in out.splitlines():
        if f" {ma} " in ln:
            return "ĐẠT" if "[ĐẠT ]" in ln else ("LỖI" if "[LỖI]" in ln else "?")
    return "KHONG_THAY"


def bang_chung(out, ma):
    for ln in out.splitlines():
        if f"[LỖI] {ma} " in ln:
            return ln.strip()[:230]
    return ""


GOC_IDX = sha(IDX)
ket_luan = []


def ghi(ten, dat, dc=False):
    """`dc=True` = ĐỐI CHỨNG ÂM (kỳ vọng cổng IM). Hai số phải tách trong KẾT LUẬN."""
    ket_luan.append((ten, dat, dc))
    return dat


def main():
    if not os.path.exists(os.path.join(REPO, "js")):
        print("!!! không thấy thư mục js/ — chạy từ gốc repo")
        return 2

    # ============================== CA 0 — baseline ==============================
    print("=" * 100)
    print("CA 0 — baseline: repo nguyên trạng, G19 phải ĐẠT cả ba tiêu chí")
    rc, out = chay_cong()
    a, b, c = ket(out, "G19a"), ket(out, "G19b"), ket(out, "G19c")
    print(f"  rc={rc}  G19a={a}  G19b={b}  G19c={c}")
    if not (a == b == c == "ĐẠT"):
        print("  !!! baseline đã đỏ — sửa cổng trước khi tin bất kỳ ca nào bên dưới")
        return 1

    # ============================== CA 1 — phá G19a ==============================
    print("=" * 100)
    print("CA 1 — tệp thăm dò js/ gọi fetch() trong MÃ SỐNG  -> G19a PHẢI kêu")
    try:
        open(THAM_DO, "w", encoding="utf-8").write(
            "/* tệp thăm dò của mutation_g19 — sẽ bị xoá */\n"
            'async function guiDi(d){ const r = await fetch("https://vidu.example/x", {method:"HEAD"}); return r; }\n'
            "window.ZZ_THAM_DO = { guiDi };\n")
        rc, out = chay_cong()
        a = ket(out, "G19a")
        print(f"  rc={rc}  G19a={a}")
        if a == "LỖI":
            print("  bằng chứng:", bang_chung(out, "G19a"))
        ghi("1 fetch() trong mã sống -> G19a bắt", a == "LỖI")
    finally:
        if os.path.exists(THAM_DO):
            os.unlink(THAM_DO)
        print("  khôi phục:", "tệp thăm dò đã xoá" if not os.path.exists(THAM_DO) else "!!! CÒN SÓT")

    # ============================== CA 2 — đối chứng âm cho G19a ==============================
    print("=" * 100)
    print("CA 2 — tệp thăm dò js/ nhắc fetch() CHỈ TRONG COMMENT  -> G19a PHẢI IM")
    print("       (đây là tình huống có thật: comment ghi lại bài học chứa chữ fetch)")
    try:
        open(THAM_DO, "w", encoding="utf-8").write(
            "/* tệp thăm dò của mutation_g19 — sẽ bị xoá.\n"
            ' * Bài học: từng có fetch("https://huggingface.co") trong hàm chết doKhaNang().\n'
            " */\n"
            '// một dòng chú thích kiểu // cũng nhắc fetch( và navigator.gpu\n'
            "function tinhTong(a, b){ return a + b; }\n"
            "window.ZZ_THAM_DO = { tinhTong };\n")
        rc, out = chay_cong()
        a = ket(out, "G19a")
        print(f"  rc={rc}  G19a={a}")
        if a == "LỖI":
            print("  BẮT OAN, bằng chứng:", bang_chung(out, "G19a"))
        ghi("2 fetch() chỉ trong comment -> G19a im (đối chứng âm)", a == "ĐẠT", dc=True)
    finally:
        if os.path.exists(THAM_DO):
            os.unlink(THAM_DO)
        print("  khôi phục:", "tệp thăm dò đã xoá" if not os.path.exists(THAM_DO) else "!!! CÒN SÓT")

    # ============================== CA 3 — phá G19b ==============================
    print("=" * 100)
    print("CA 3 — index.html trỏ src tới tệp .js KHÔNG TỒN TẠI  -> G19b PHẢI kêu")
    s_idx = open(IDX, encoding="utf-8").read()
    MOI = '<script src="js/khong_ton_tai_mutation_g19.js"></script>'
    try:
        # chèn ngay trước </head> để chắc chắn nằm trong mã sống, không phải trong chú thích
        if "</head>" not in s_idx:
            print("  !!! không tìm thấy </head> để chèn — bỏ qua ca này")
            ghi("3 asset thiếu -> G19b bắt", None)
        else:
            open(IDX, "w", encoding="utf-8").write(s_idx.replace("</head>", MOI + "\n</head>", 1))
            rc, out = chay_cong()
            b = ket(out, "G19b")
            print(f"  rc={rc}  G19b={b}")
            if b == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G19b"))
            ghi("3 asset thiếu -> G19b bắt", b == "LỖI")
    finally:
        open(IDX, "w", encoding="utf-8").write(s_idx)
        print("  khôi phục:", "hash KHỚP gốc" if sha(IDX) == GOC_IDX else "!!! LỆCH — PHẢI SỬA TAY")

    # ============================== TỔNG KẾT ==============================
    print("=" * 100)
    con_sot = os.path.exists(THAM_DO) or sha(IDX) != GOC_IDX
    print(f"[XÁC NHẬN] còn dấu vết phá: {con_sot} (phải False)")
    rc2, ket2 = chay_cong()
    a2, b2, c2 = ket(ket2, "G19a"), ket(ket2, "G19b"), ket(ket2, "G19c")
    print(f"[XÁC NHẬN SAU CÙNG] rc={rc2}  G19a={a2} G19b={b2} G19c={c2}  (phải về ĐẠT cả ba)")

    # Khuôn chung với các script mutation khác để dem_ca.py đếm được bằng máy.
    # Hai số PHẢI tách: ca đối chứng âm không phải "cổng bắt được" mà là "cổng không
    # bắt oan" — gộp lại là khai quá (luật đã ghi trong dem_ca.py).
    ran = [(t, o, d) for t, o, d in ket_luan if o is not None]
    so = sum(1 for _, o, _ in ran if o)
    so_pha = sum(1 for _, o, d in ran if o and not d)
    so_dc = sum(1 for _, o, d in ran if o and d)
    print(f"\nKẾT LUẬN: {so}/{len(ran)} ca đúng như kỳ vọng ({so_pha} ca PHÁ bị cổng bắt"
          f" + {so_dc} ca ĐỐI CHỨNG ÂM cổng im đúng)")
    for ten, o, dc in ket_luan:
        if o is None:
            print(f"  {ten}: BỎ QUA")
            continue
        nhan = ("KHÔNG BẮT OAN (đúng)" if o else "BẮT OAN — luật lột comment hỏng") if dc \
            else ("ĐÚNG" if o else "SAI KỲ VỌNG")
        print(f"  {ten}: {nhan}")
    print("=" * 100)
    ok = (so == len(ran)) and not con_sot and rc2 == 0 and (a2 == b2 == c2 == "ĐẠT")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
