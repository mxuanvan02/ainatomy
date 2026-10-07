#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho G17 (cổng đường dẫn tài liệu) — chứng minh nó CÓ RĂNG.

G17 vừa được thêm và in ĐẠT 3/3 ngay lần chạy đầu đúng nghĩa (sau khi sửa 14 dương tính giả).
Nhưng "ĐẠT" chưa nói gì: một cổng luôn ĐẠT cũng in ĐẠT. Ba ca phá dưới đây kiểm từng tiêu chí:
  ca 1 — README hứa một tệp không tồn tại  -> G17b phải LỖI
  ca 2 — đổi tên tệp đầu ra trong tài liệu -> G17c phải LỖI (chiều: doc hứa, mã không ghi)
  ca 3 — gop_csv.py ghi thêm tệp mà tài liệu không nhắc -> G17c phải LỖI (chiều ngược)
Ca 3 là ca quan trọng nhất: nó chứng minh G17c kiểm HAI CHIỀU thật, không phải một phép
`subset` luôn rỗng (Luật A trong skill agentic-efficiency-loop: cổng tuyên bố "khớp nhau" mà
chỉ kiểm một chiều thì chiều kia là code chết và cổng vẫn in ĐẠT).
Mọi ca đều khôi phục tệp và xác nhận hash về đúng bản gốc.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CONG = os.path.join(REPO, "tools", "nghiem_thu.py")
README = os.path.join(REPO, "README.md")
GOP = os.path.join(REPO, "tools", "gop_csv.py")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong(nhom="G17"):
    r = subprocess.run([sys.executable, CONG, nhom], cwd=REPO,
                       capture_output=True, text=True, timeout=400)
    return r.returncode, r.stdout + r.stderr


def loai_kq(out, ma):
    """Lấy dòng kết quả của đúng tiêu chí `ma` (vd G17b), không lấy dòng của tiêu chí khác."""
    for ln in out.splitlines():
        if f" {ma} " in ln:
            return "ĐẠT" if "[ĐẠT ]" in ln else ("LỖI" if "[LỖI]" in ln else "?")
    return "KHONG_THAY"


GOC = {p: sha(p) for p in (README, GOP)}
ket_luan = []

# ---------- CA 1: README hứa một tệp không tồn tại ----------
print("=" * 88)
print("CA 1 — README hứa tệp `tools/khong_co_that.py` (không tồn tại)")
s = open(README, encoding="utf-8").read()
them = "\nChạy thêm `tools/khong_co_that.py` để đối chiếu.\n"
open(README, "w", encoding="utf-8").write(s + them)
try:
    rc, out = chay_cong()
    g17b = loai_kq(out, "G17b")
    bat = (rc != 0 and g17b == "LỖI")
    print(f"  rc={rc}  G17b={g17b}  ->  {'BẮT ĐƯỢC' if bat else 'CỔNG IM (G17b không có răng)'}")
    if not bat:
        for ln in out.splitlines():
            if "G17b" in ln:
                print("   |", ln.strip()[:200])
    ket_luan.append(("1 README hứa tệp ma", bat))
finally:
    open(README, "w", encoding="utf-8").write(s)
    print("  khôi phục README.md:", "hash KHỚP gốc" if sha(README) == GOC[README] else "!!! LỆCH")

# ---------- CA 2: tài liệu hứa tệp đầu ra mà mã KHÔNG ghi ----------
print("=" * 88)
print("CA 2 — tài liệu hứa đầu ra `baocao_tuan.csv` mà gop_csv.py không ghi (chiều 1 của G17c)")
doc = open(os.path.join(REPO, "huong-dan-danh-gia.md"), encoding="utf-8").read()
GOC_DOC = sha(os.path.join(REPO, "huong-dan-danh-gia.md"))
doc2 = doc.replace("`nhatky_gop.csv`", "`baocao_tuan.csv`", 1)
if doc2 == doc:
    print("  !!! không tìm thấy chỗ thay; bỏ qua ca này")
    ket_luan.append(("2 doc hứa đầu ra ma", None))
else:
    open(os.path.join(REPO, "huong-dan-danh-gia.md"), "w", encoding="utf-8").write(doc2)
    try:
        rc, out = chay_cong()
        g17c = loai_kq(out, "G17c")
        bat = (rc != 0 and g17c == "LỖI")
        print(f"  rc={rc}  G17c={g17c}  ->  {'BẮT ĐƯỢC' if bat else 'CỔNG IM'}")
        if not bat:
            for ln in out.splitlines():
                if "G17c" in ln:
                    print("   |", ln.strip()[:220])
        ket_luan.append(("2 doc hứa đầu ra ma", bat))
    finally:
        p = os.path.join(REPO, "huong-dan-danh-gia.md")
        open(p, "w", encoding="utf-8").write(doc)
        print("  khôi phục huong-dan-danh-gia.md:",
              "hash KHỚP gốc" if sha(p) == GOC_DOC else "!!! LỆCH")

# ---------- CA 3: mã ghi thêm tệp đầu ra mà tài liệu không nhắc ----------
print("=" * 88)
print("CA 3 — gop_csv.py ghi thêm `baocao_bi_mat.csv`, tài liệu không nhắc (chiều 2 của G17c)")
g = open(GOP, encoding="utf-8").read()
mo = 'p1 = os.path.join(outdir, "nhatky_gop.csv")'
if mo not in g:
    print("  !!! không thấy dòng neo để chèn; bỏ qua ca này")
    ket_luan.append(("3 mã ghi đầu ra không ai nhắc", None))
else:
    g2 = g.replace(mo, mo + '\n    _p_bi_mat = os.path.join(outdir, "baocao_bi_mat.csv")', 1)
    open(GOP, "w", encoding="utf-8").write(g2)
    try:
        rc, out = chay_cong()
        g17c = loai_kq(out, "G17c")
        bat = (rc != 0 and g17c == "LỖI")
        print(f"  rc={rc}  G17c={g17c}  ->  {'BẮT ĐƯỢC' if bat else 'CỔNG IM'}")
        if not bat:
            for ln in out.splitlines():
                if "G17c" in ln:
                    print("   |", ln.strip()[:220])
        else:
            for ln in out.splitlines():
                if "G17c" in ln:
                    print("   bằng chứng:", ln.strip()[-170:])
        ket_luan.append(("3 mã ghi đầu ra không ai nhắc", bat))
    finally:
        open(GOP, "w", encoding="utf-8").write(g)
        print("  khôi phục gop_csv.py:", "hash KHỚP gốc" if sha(GOP) == GOC[GOP] else "!!! LỆCH")

# ---------- CA 4 (NEGATIVE CONTROL): tên CSV động của app KHÔNG được bị bắt oan ----------
print("=" * 88)
print("CA 4 — README nhắc `soiai_nhatky_10A1_1728.csv` (tên app tự tải về, không có trên đĩa)")
print("        kỳ vọng: G17 vẫn ĐẠT 3/3 — ca này chứng minh cổng KHÔNG kêu oan.")
s = open(README, encoding="utf-8").read()
them = ("\nVí dụ tệp app cho tải về: `soiai_nhatky_10A1_1728.csv`.\n")
open(README, "w", encoding="utf-8").write(s + them)
try:
    rc, out = chay_cong()
    g17b, g17c = loai_kq(out, "G17b"), loai_kq(out, "G17c")
    m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
    khong_oan = (rc == 0 and g17b == "ĐẠT" and g17c == "ĐẠT")
    print(f"  rc={rc}  G17b={g17b}  G17c={g17c}  {m.group(0) if m else ''}")
    print(f"  ->  {'KHÔNG BẮT OAN (đúng)' if khong_oan else 'BẮT OAN — phần miễn trừ tên động hỏng'}")
    if not khong_oan:
        for ln in out.splitlines():
            if "G17b" in ln or "G17c" in ln:
                print("   |", ln.strip()[:230])
    ket_luan.append(("4 tên CSV động của app (không được bắt oan)", khong_oan))
finally:
    open(README, "w", encoding="utf-8").write(s)
    print("  khôi phục README.md:", "hash KHỚP gốc" if sha(README) == GOC[README] else "!!! LỆCH")

# ---------- TỔNG KẾT ----------
print("=" * 88)
so = sum(1 for _, b in ket_luan if b is True)
tong = sum(1 for _, b in ket_luan if b is not None)
print(f"KẾT LUẬN: {so}/{tong} ca phá bị G17 bắt")
for ten, b in ket_luan:
    if b is None:
        print(f"  {ten}: BỎ QUA (không dựng được ca)")
    else:
        print(f"  {ten}: {'BẮT ĐƯỢC' if b else 'CỔNG IM'}")

# Xác nhận sau cùng: cây phải về ĐẠT và không còn dấu vết mutation.
rc, out = chay_cong()
m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
print("=" * 88)
print(f"XÁC NHẬN SAU CÙNG: rc={rc}  KẾT QUẢ: {m.group(0).split(': ')[1] if m else '?'}")
for p, h in GOC.items():
    if sha(p) != h:
        print("  !!!", p, "CHƯA khôi phục đúng")
sys.exit(0 if (so == tong and rc == 0) else 1)
