#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho G17d / G17e / G17f — ba tiêu chí mới thêm 07/10.

SÁU CA, gồm HAI negative control (Luật C trong skill agentic-efficiency-loop: thiếu ca "đầu vào
hợp lệ trông giống lỗi thì cổng phải IM" thì không phân biệt được cổng có răng với cổng bắt oan).

  ca 5  — tài liệu hứa cờ `--xlsx` mà gop_csv.py không có      -> G17d PHẢI BẮT
  ca 6  — tài liệu thêm lệnh NGOÀI (`tar -xzvf`, `sha256sum -c`) -> G17d PHẢI IM (negative control)
  ca 7  — tài liệu đổi THỨ TỰ hai cột                          -> G17e PHẢI BẮT (so có thứ tự)
  ca 8  — tài liệu đổi TÊN một cột                             -> G17e PHẢI BẮT
  ca 9  — tài liệu sửa chữ "Mười cột" thành "Chín cột"         -> G17f BẮT mà G17e VẪN ĐẠT
          (ca này chứng minh G17f KHÔNG THỪA: nếu nó chỉ lặp lại G17e thì G17e đã bắt rồi)
  ca 10 — gop_csv.py ghi THÊM một cột vào baocao_ca_nhan.csv   -> G17e VÀ G17f cùng BẮT

Mọi ca đều khôi phục tệp và xác nhận hash về đúng bản gốc trước khi sang ca sau.
"""
import hashlib
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CONG = os.path.join(REPO, "tools", "nghiem_thu.py")
DOC = os.path.join(REPO, "huong-dan-danh-gia.md")
GOP = os.path.join(REPO, "tools", "gop_csv.py")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong(nhom="G17"):
    r = subprocess.run([sys.executable, CONG, nhom], cwd=REPO,
                       capture_output=True, text=True, timeout=400)
    return r.returncode, r.stdout + r.stderr


def ket(out, ma):
    """Kết quả của ĐÚNG tiêu chí `ma`."""
    for ln in out.splitlines():
        if f" {ma} " in ln:
            return "ĐẠT" if "[ĐẠT ]" in ln else ("LỖI" if "[LỖI]" in ln else "?")
    return "KHONG_THAY"


def thay(p, cu, moi, n=1):
    """Thay chuỗi, báo rõ nếu không tìm thấy chỗ thay (tránh ca phá âm thầm không làm gì)."""
    s = open(p, encoding="utf-8").read()
    if cu not in s:
        return None
    open(p, "w", encoding="utf-8").write(s.replace(cu, moi, n))
    return s


def khoi_phuc(p, s):
    open(p, "w", encoding="utf-8").write(s)


GOC = {DOC: sha(DOC), GOP: sha(GOP)}
ket_luan = []
DOC_STR = open(DOC, encoding="utf-8").read()
GOP_STR = open(GOP, encoding="utf-8").read()


def bao_cao(ten, bat, ghi_chu=""):
    print(f"  ->  {'BẮT ĐƯỢC' if bat else 'KHÔNG NHƯ KỲ VỌNG'}" + (f"  {ghi_chu}" if ghi_chu else ""))
    ket_luan.append((ten, bat))


# ============================== CA 5 ==============================
print("=" * 88)
print("CA 5 — tài liệu hứa cờ `--xlsx` mà gop_csv.py không có")
cu = "`python3 tools/gop_csv.py <thư_mục> -o <báo_cáo>`"
moi = "`python3 tools/gop_csv.py <thư_mục> -o <báo_cáo> --xlsx`"
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("5 cờ CLI ma", None))
else:
    try:
        rc, out = chay_cong()
        g = ket(out, "G17d")
        print(f"  rc={rc}  G17d={g}")
        if g != "LỖI":
            for ln in out.splitlines():
                if "G17d" in ln:
                    print("   |", ln.strip()[:200])
        bao_cao("5 tài liệu hứa cờ CLI ma (G17d phải bắt)", rc != 0 and g == "LỖI")
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

# ============================== CA 6 (negative control) ==============================
print("=" * 88)
print("CA 6 — NEGATIVE CONTROL: thêm lệnh NGOÀI repo với cờ lạ (`tar -xzvf`, `sha256sum -c`)")
them = ("\nLưu trữ: `tar -xzvf hoso.tar.gz`, kiểm mã: `sha256sum -c SHA256SUMS.txt`, "
        "và `grep -rn x js/`.\n")
s = DOC_STR
open(DOC, "w", encoding="utf-8").write(s + them)
try:
    rc, out = chay_cong()
    gd, gb = ket(out, "G17d"), ket(out, "G17b")
    m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
    im = (gd == "ĐẠT" and gb == "ĐẠT")
    print(f"  rc={rc}  G17d={gd}  G17b={gb}  {m.group(0) if m else ''}")
    if not im:
        for ln in out.splitlines():
            if "G17b" in ln or "G17d" in ln:
                print("   |", ln.strip()[:230])
    bao_cao("6 cờ của lệnh NGOÀI repo (G17d phải IM)", im)
finally:
    khoi_phuc(DOC, DOC_STR)
    print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

# ============================== CA 7 ==============================
print("=" * 88)
print("CA 7 — tài liệu đổi THỨ TỰ: ma_hs, ma_lop -> ma_lop, ma_hs")
cu = "ma_hs, ma_lop, so_cau_dau_truong"
moi = "ma_lop, ma_hs, so_cau_dau_truong"
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("7 lệch thứ tự cột", None))
else:
    try:
        rc, out = chay_cong()
        g = ket(out, "G17e")
        print(f"  rc={rc}  G17e={g}")
        for ln in out.splitlines():
            if "G17e" in ln and "LỆCH" in ln:
                print("   bằng chứng:", ln.strip()[-150:])
        bao_cao("7 tài liệu lệch THỨ TỰ cột (G17e phải bắt)", rc != 0 and g == "LỖI")
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

# ============================== CA 8 ==============================
print("=" * 88)
print("CA 8 — tài liệu đổi TÊN cột: ti_le_dung -> ty_le_dung")
cu = "ti_le_dung, so_nhiem_vu_lab"
moi = "ty_le_dung, so_nhiem_vu_lab"
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("8 sai tên cột", None))
else:
    try:
        rc, out = chay_cong()
        g = ket(out, "G17e")
        print(f"  rc={rc}  G17e={g}")
        for ln in out.splitlines():
            if "G17e" in ln and ("thừa" in ln or "KHÔNG ghi" in ln):
                print("   bằng chứng:", ln.strip()[-170:])
        bao_cao("8 tài liệu sai TÊN cột (G17e phải bắt)", rc != 0 and g == "LỖI")
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

# ============================== CA 9 ==============================
print("=" * 88)
print('CA 9 — tài liệu sửa chữ "Mười cột" thành "Chín cột" (danh sách cột GIỮ NGUYÊN)')
print("       kỳ vọng: G17f LỖI nhưng G17e VẪN ĐẠT -> chứng minh G17f không thừa")
cu = "Mười cột của `baocao_ca_nhan.csv`"
moi = "Chín cột của `baocao_ca_nhan.csv`"
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("9 số đếm trong câu dẫn", None))
else:
    try:
        rc, out = chay_cong()
        gf, ge = ket(out, "G17f"), ket(out, "G17e")
        print(f"  rc={rc}  G17f={gf}  G17e={ge}")
        for ln in out.splitlines():
            if "G17f" in ln and "mâu thuẫn" in ln:
                print("   bằng chứng:", ln.strip()[-170:])
        bat = (gf == "LỖI" and ge == "ĐẠT")
        bao_cao("9 số đếm sai mà danh sách vẫn đúng (G17f bắt, G17e không bắt -> không thừa)", bat)
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

# ============================== CA 10 ==============================
print("=" * 88)
print("CA 10 — gop_csv.py ghi THÊM cột `ghi_chu_gv` vào baocao_ca_nhan.csv, tài liệu không biết")
cu = ('"ti_le_du_doan_khop","du_doan_bo_qua"])')
moi = ('"ti_le_du_doan_khop","du_doan_bo_qua","ghi_chu_gv"])')
s = thay(GOP, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("10 mã thêm cột tài liệu không nhắc", None))
else:
    try:
        rc, out = chay_cong()
        ge, gf = ket(out, "G17e"), ket(out, "G17f")
        print(f"  rc={rc}  G17e={ge}  G17f={gf}")
        for ln in out.splitlines():
            if ("G17e" in ln and "KHÔNG liệt kê" in ln) or ("G17f" in ln and "mâu thuẫn" in ln):
                print("   bằng chứng:", ln.strip()[-160:])
        bat = (ge == "LỖI" and gf == "LỖI")
        bao_cao("10 mã thêm cột tài liệu không nhắc (G17e VÀ G17f cùng bắt)", bat)
    finally:
        khoi_phuc(GOP, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(GOP) == GOC[GOP] else "!!! LỆCH")

# ============================== TỔNG KẾT ==============================
print("=" * 88)
so = sum(1 for _, b in ket_luan if b is True)
tong = sum(1 for _, b in ket_luan if b is not None)
print(f"KẾT LUẬN: {so}/{tong} ca đúng như kỳ vọng")
for ten, b in ket_luan:
    if b is None:
        print(f"  {ten}: BỎ QUA (không dựng được ca)")
    else:
        print(f"  {ten}: {'ĐÚNG' if b else 'SAI KỲ VỌNG'}")

rc, out = chay_cong()
m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
print("=" * 88)
print(f"XÁC NHẬN SAU CÙNG: rc={rc}  {m.group(0) if m else 'không đọc được tổng'}  (phải về ĐẠT: hai số bằng nhau)")
for p, h in GOC.items():
    if sha(p) != h:
        print("  !!!", p, "CHƯA khôi phục đúng")
sys.exit(0 if (so == tong and rc == 0) else 1)
