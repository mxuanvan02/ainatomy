#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho G17d / G17e / G17f — ba tiêu chí mới thêm 07/10.

MƯỜI HAI CA, gồm BỐN negative control (Luật C trong skill agentic-efficiency-loop: thiếu ca "đầu vào
hợp lệ trông giống lỗi thì cổng phải IM" thì không phân biệt được cổng có răng với cổng bắt oan).

SỐ CA TRONG DOCSTRING NÀY ĐÃ SAI MỘT LẦN và đáng ghi lại: bản trước khai "MƯỜI CA, gồm BỐN
negative control" trong khi thật chỉ có BA (ca 6, 12, 14) — tức tài liệu mô tả chính tệp này
cũng khai quá, đúng lớp lỗi mà bộ mutation test sinh ra để săn. Đếm bằng `grep -c "dc=True"` rồi
đọc từng dòng mới ra số đúng. Nay thêm ca 15 (đối chứng âm) nên BỐN là đúng, và tổng là MƯỜI HAI.

  ca 5  — tài liệu hứa cờ `--xlsx` mà gop_csv.py không có      -> G17d PHẢI BẮT
  ca 6  — tài liệu thêm lệnh NGOÀI (`tar -xzvf`, `sha256sum -c`) -> G17d PHẢI IM (negative control)
  ca 7  — tài liệu đổi THỨ TỰ hai cột                          -> G17e PHẢI BẮT (so có thứ tự)
  ca 8  — tài liệu đổi TÊN một cột                             -> G17e PHẢI BẮT
  ca 9  — tài liệu sửa chữ "Mười cột" thành "Chín cột"         -> G17f BẮT mà G17e VẪN ĐẠT
          (ca này chứng minh G17f KHÔNG THỪA: nếu nó chỉ lặp lại G17e thì G17e đã bắt rồi)
  ca 10 — gop_csv.py ghi THÊM một cột vào baocao_ca_nhan.csv   -> G17e VÀ G17f cùng BẮT

BỐN CA THÊM 08/10, sau khi vá hai dương tính giả của chính cổng này. Mỗi bản vá được cắm ĐÚNG
HAI CA: một ca phá (cổng phải kêu) và một ca đối chứng âm (cổng phải im). Thiếu ca thứ hai thì
không phân biệt được bản vá với việc vừa làm cổng mù hẳn — mà "làm cổng mù" lại luôn cho ra
màn hình xanh, nên nó là kiểu hỏng dễ bị bỏ qua nhất.

  ca 11 — tài liệu nhắc đường dẫn `../` KHÔNG tồn tại            -> G17b PHẢI BẮT
  ca 12 — tài liệu nhắc đường dẫn `../` CÓ tồn tại (đối chứng âm) -> G17b PHẢI IM
          Cặp này kiểm bản vá `strip(".,;:")` -> `rstrip(".,;:")`. Bản cũ ăn mất hai dấu chấm ở
          ĐẦU token, biến `../tools/x.py` thành `/tools/x.py` (đường dẫn tuyệt đối), nên nó tố
          oan mọi đường dẫn `../` — kể cả đường dẫn đúng. Ca 12 là chính ca đã bị tố oan.
  ca 13 — tài liệu hứa cờ `--khong-co-co-nay` của sinh_manifest -> G17d PHẢI BẮT
  ca 14 — tài liệu hứa cờ `--ghi` của sinh_manifest (đối chứng âm) -> G17d PHẢI IM
          Cặp này kiểm bản vá đọc cờ theo HAI kiểu khai. `sinh_manifest.py` đọc cờ bằng
          `ghi = "--ghi" in sys.argv` chứ không dùng argparse, nên bản cổng cũ tố oan nó là
          "không có cờ --ghi". Ca 14 là chính ca đã bị tố oan; ca 13 chứng minh bản vá KHÔNG
          mở toang cổng (nếu quét cả tệp thay vì chỉ dòng có `sys.argv` thì ca 13 sẽ lọt).

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


def bao_cao(ten, bat, ghi_chu="", dc=False):
    """Ghi kết quả một ca. `dc=True` = ĐỐI CHỨNG ÂM: kỳ vọng cổng IM.

    Sửa 08/10 cùng lúc với mutation_g17.py, cùng một lỗi nhãn: in "BẮT ĐƯỢC" cho một ca mà đúng
    nghĩa là "cổng phải im" làm dòng kết quả tự nói sai về chính nó, và người đọc sau sẽ đếm nó
    thành ca phá. Ca 6, 12, 14 dùng `dc=True`.
    """
    if bat is None:
        nhan = "BỎ QUA"
    elif dc:
        nhan = "KHÔNG BẮT OAN (đúng)" if bat else "BẮT OAN — luật miễn trừ hỏng"
    else:
        nhan = "BẮT ĐƯỢC" if bat else "KHÔNG NHƯ KỲ VỌNG"
    print(f"  ->  {nhan}" + (f"  {ghi_chu}" if ghi_chu else ""))
    ket_luan.append((ten, bat, dc))


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
    bao_cao("6 cờ của lệnh NGOÀI repo (G17d phải IM)", im, dc=True)
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

# ============================== CA 11 + CA 12 ==============================
# Cặp ca cho bản vá `strip(".,;:")` -> `rstrip(".,;:")` của G17b.
print("=" * 88)
print("CA 11 — tài liệu nhắc đường dẫn `../` KHÔNG tồn tại")
print("        kỳ vọng: G17b LỖI")
cu = "  nói rõ điều đó."
moi = ("  nói rõ điều đó.\n\n  Tham chiếu cần kiểm: `../tools/khong-co-tap-tin-nay.py`.")
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("11 đường dẫn ../ không tồn tại", None))
else:
    try:
        rc, out = chay_cong()
        gb = ket(out, "G17b")
        print(f"  rc={rc}  G17b={gb}")
        for ln in out.splitlines():
            if "G17b" in ln and "[LỖI]" in ln:
                print("   bằng chứng:", ln.strip()[-150:])
        bao_cao("11 đường dẫn ../ KHÔNG tồn tại (G17b phải bắt)", gb == "LỖI")
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

print("=" * 88)
print("CA 12 — NEGATIVE CONTROL: tài liệu nhắc đường dẫn `../` CÓ tồn tại thật")
print("        kỳ vọng: G17b IM  (đây là chính ca bị bản cũ tố oan)")
cu = "  nói rõ điều đó."
moi = ("  nói rõ điều đó.\n\n  Tham chiếu cần kiểm: `../tools/tao_sheet_thietke.py`.")
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("12 đối chứng âm: đường dẫn ../ có thật", None))
else:
    try:
        rc, out = chay_cong()
        gb = ket(out, "G17b")
        print(f"  rc={rc}  G17b={gb}")
        for ln in out.splitlines():
            if "G17b" in ln and "[LỖI]" in ln and "khong" not in ln.lower():
                print("   TỐ OAN:", ln.strip()[-150:])
        bao_cao("12 đối chứng âm: đường dẫn ../ CÓ thật (G17b phải im)", gb == "ĐẠT", dc=True)
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

# ============================== CA 13 + CA 14 ==============================
# Cặp ca cho bản vá đọc cờ CLI theo HAI kiểu khai (argparse và sys.argv) của G17d.
print("=" * 88)
print("CA 13 — tài liệu hứa cờ `--khong-co-co-nay` cho sinh_manifest.py")
print("        kỳ vọng: G17d LỖI  (chứng minh bản vá KHÔNG mở toang cổng)")
cu = "  nói rõ điều đó."
moi = ("  nói rõ điều đó.\n\n  Lệnh cần kiểm: `python3 tools/sinh_manifest.py --khong-co-co-nay`.")
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("13 cờ bịa của sinh_manifest", None))
else:
    try:
        rc, out = chay_cong()
        gd = ket(out, "G17d")
        print(f"  rc={rc}  G17d={gd}")
        for ln in out.splitlines():
            if "G17d" in ln and "[LỖI]" in ln:
                print("   bằng chứng:", ln.strip()[-160:])
        bao_cao("13 cờ bịa `--khong-co-co-nay` (G17d phải bắt)", gd == "LỖI")
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

print("=" * 88)
print("CA 14 — NEGATIVE CONTROL: tài liệu hứa cờ `--ghi` mà sinh_manifest THẬT SỰ có")
print("        (tool đọc cờ bằng `ghi = \"--ghi\" in sys.argv`, KHÔNG dùng argparse)")
print("        kỳ vọng: G17d IM  (đây là chính ca bị bản cũ tố oan)")
cu = "  nói rõ điều đó."
moi = ("  nói rõ điều đó.\n\n  Lệnh cần kiểm: `python3 tools/sinh_manifest.py --ghi`.")
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("14 đối chứng âm: cờ --ghi của sinh_manifest", None))
else:
    try:
        rc, out = chay_cong()
        gd = ket(out, "G17d")
        print(f"  rc={rc}  G17d={gd}")
        for ln in out.splitlines():
            if "G17d" in ln and "[LỖI]" in ln:
                print("   TỐ OAN:", ln.strip()[-160:])
        bao_cao("14 đối chứng âm: cờ `--ghi` CÓ thật (G17d phải im)", gd == "ĐẠT", dc=True)
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

# ============================== CA 15 + CA 16 ==============================
# Cặp ca cho phép loại trừ MẢNH URL vừa thêm vào G17b (08/10).
# Ca 15 là chính ca đã bị bắt oan: README §8 kể lại "github.io/soi-ai/ trả 404" — một tên miền
# trong văn xuôi, không phải đường dẫn tệp, nhưng RE_DDP nhận nó rồi os.path.exists trả False.
# Ca 16 chứng minh phép loại trừ KHÔNG làm cổng mù: đường dẫn tệp thật sự không tồn tại vẫn phải
# bị bắt. Thiếu ca 16 thì "hết bắt oan" và "cổng mù hẳn" trông giống hệt nhau — cả hai đều xanh.
print("=" * 88)
print("CA 15 — NEGATIVE CONTROL: tài liệu nhắc MẢNH URL không có scheme (`github.io/soi-ai/`)")
print("        kỳ vọng: G17b IM  (đây là chính ca bị bản cũ tố oan — nó là tên miền, không phải tệp)")
cu = "  nói rõ điều đó."
moi = ("  nói rõ điều đó.\n\n  Tiền lệ đã đo: `github.io/soi-ai/` trả 404 sau lần đổi tên repo.")
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("15 đối chứng âm: mảnh URL trong văn xuôi", None))
else:
    try:
        rc, out = chay_cong()
        gb = ket(out, "G17b")
        print(f"  rc={rc}  G17b={gb}")
        for ln in out.splitlines():
            if "G17b" in ln and "[LỖI]" in ln:
                print("   TỐ OAN:", ln.strip()[-160:])
        bao_cao("15 đối chứng âm: mảnh URL `github.io/soi-ai/` (G17b phải im)", gb == "ĐẠT", dc=True)
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

print("=" * 88)
print("CA 16 — tài liệu hứa đường dẫn TỆP không tồn tại (`tools/khong-co-tap-tin-nay.py`)")
print("        kỳ vọng: G17b LỖI  (chứng minh phép loại trừ URL KHÔNG làm cổng mù)")
cu = "  nói rõ điều đó."
moi = ("  nói rõ điều đó.\n\n  Chạy thêm `tools/khong-co-tap-tin-nay.py` để đối chiếu.")
s = thay(DOC, cu, moi)
if s is None:
    print("  !!! không tìm thấy chỗ thay; bỏ qua")
    ket_luan.append(("16 đường dẫn tệp ma sau khi thêm phép loại trừ URL", None))
else:
    try:
        rc, out = chay_cong()
        gb = ket(out, "G17b")
        print(f"  rc={rc}  G17b={gb}")
        for ln in out.splitlines():
            if "G17b" in ln and "[LỖI]" in ln:
                print("   bằng chứng:", ln.strip()[-160:])
        bao_cao("16 đường dẫn tệp ma vẫn bị bắt (phép loại trừ URL không làm mù cổng)", gb == "LỖI")
    finally:
        khoi_phuc(DOC, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(DOC) == GOC[DOC] else "!!! LỆCH")

# ============================== TỔNG KẾT ==============================
print("=" * 88)
# Đếm TÁCH HAI LOẠI, và chịu được cả tuple 2 phần tử: các nhánh "không dựng được ca" chỉ ghi
# (tên, None). Đọc cờ ở vị trí 2 nếu có, KHÔNG suy từ chữ trong tên ca.
def _dc(t):
    return t[2] if len(t) > 2 else False


so = sum(1 for t in ket_luan if t[1] is True)
tong = sum(1 for t in ket_luan if t[1] is not None)
so_pha = sum(1 for t in ket_luan if t[1] is True and not _dc(t))
so_dc = sum(1 for t in ket_luan if t[1] is True and _dc(t))
print(f"KẾT LUẬN: {so}/{tong} ca đúng như kỳ vọng ({so_pha} ca PHÁ bị cổng bắt"
      f" + {so_dc} ca ĐỐI CHỨNG ÂM cổng im đúng)")
for t in ket_luan:
    ten, b = t[0], t[1]
    if b is None:
        print(f"  {ten}: BỎ QUA (không dựng được ca)")
    elif _dc(t):
        print(f"  {ten}: {'KHÔNG BẮT OAN (đúng)' if b else 'BẮT OAN — luật miễn trừ hỏng'}")
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
