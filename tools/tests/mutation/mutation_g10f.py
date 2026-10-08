#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho G10b (mở rộng) và G10f (mới) — bốn ca.

G10f canh một RANH GIỚI HỒ SƠ: định danh đã đổi thành "cấp THPT" nhưng dữ liệu yêu cầu cần
đạt mới chỉ có lớp 10. Ranh giới đó có ba mặt, và mỗi mặt cần một ca phá riêng:
  ca 1 — nhét định danh CŨ trở lại index.html          -> G10f bắt (chiều a: đổi tên nửa vời)
  ca 2 — replace "lớp 10" toàn cục trong data/yccd.js   -> G10f bắt (chiều b: MẤT DẤU phạm vi)
  ca 3 — xoá đoạn khai phạm vi trong README.md          -> G10f bắt (chiều c)
  ca 4 — NEGATIVE CONTROL: xoá định danh MỚI khỏi js/kichban.js
         -> G10b BẮT nhưng G10f phải IM. Ca này chứng minh hai cổng chia việc chứ không trùng:
            G10b hỏi "tên mới có đủ ở cả ba nơi không", G10f hỏi "tên cũ còn sót không và phạm
            vi dữ liệu có bị khai quá không". Nếu G10f cũng kêu ở ca 4 thì nó đang làm hộ việc
            của G10b, và ngược lại nếu G10b im ở ca 1 thì việc mở rộng sang nơi thứ ba là vô ích.
Ca 2 là ca quan trọng nhất: một cú `replace("lớp 10", "cấp THPT")` toàn cục làm cho chiều (a)
càng đẹp (tên cũ sạch bong) nên mọi cổng kiểu "kiểm tên mới đã thay hết chưa" đều ĐẠT, trong
khi hồ sơ vừa bị làm cho khai rộng hơn dữ liệu thật.

Mọi ca đều khôi phục tệp và xác nhận hash về đúng bản gốc.
"""
import hashlib
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CONG = os.path.join(REPO, "tools", "nghiem_thu.py")
IDX = os.path.join(REPO, "index.html")
YCCD = os.path.join(REPO, "data", "yccd.js")
README = os.path.join(REPO, "README.md")
KB = os.path.join(REPO, "js", "kichban.js")

TEN_CU = "Phòng thực hành Trí tuệ nhân tạo lớp 10"
TEN_MOI = "Phòng thực hành Trí tuệ nhân tạo cấp THPT"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay(nhom="G10"):
    r = subprocess.run([sys.executable, CONG, nhom], cwd=REPO,
                       capture_output=True, text=True, timeout=400)
    return r.returncode, r.stdout + r.stderr


def ket(out, ma):
    for ln in out.splitlines():
        if f" {ma} " in ln:
            return "ĐẠT" if "[ĐẠT ]" in ln else ("LỖI" if "[LỖI]" in ln else "?")
    return "KHONG_THAY"


def in_bang_chung(out, ma, n=1):
    k = 0
    for ln in out.splitlines():
        if f"[LỖI] {ma} " in ln:
            print("   bằng chứng:", ln.strip()[:250])
            k += 1
            if k >= n:
                break


GOC = {p: sha(p) for p in (IDX, YCCD, README, KB)}
ket_luan = []


def ghi(ten, dat, dc=False):
    """Ghi kết quả một ca. `dc=True` = ĐỐI CHỨNG ÂM, tức kỳ vọng cổng phải IM.

    Thêm 08/10 để dòng KẾT LUẬN đếm được bằng máy VÀ không khai quá. Trước đó script này chỉ in
    `KẾT LUẬN: 4/4 ca đúng như kỳ vọng`, không nói 4 ca đó gồm loại gì — đọc vào dễ tưởng cả 4
    đều là ca phá bị cổng bắt, trong khi ca 4 là ca ĐỐI CHỨNG ÂM (G10b phải bắt, G10f phải im).
    Phân loại bằng DỮ LIỆU (cờ này), không bằng chữ trong tên ca.
    """
    ket_luan.append((ten, dat, dc))
    return dat


def sua(p, cu, moi, n=1):
    """Thay chuỗi; trả None nếu không tìm thấy (để ca phá không âm thầm thành không-làm-gì)."""
    s = open(p, encoding="utf-8").read()
    if cu not in s:
        return None
    open(p, "w", encoding="utf-8").write(s.replace(cu, moi, n))
    return s


def tra(p, s):
    open(p, "w", encoding="utf-8").write(s)
    print("  khôi phục:", "hash KHỚP gốc" if sha(p) == GOC[p] else "!!! LỆCH")


# ============================== CA 1 ==============================
print("=" * 92)
print("CA 1 — nhét ĐỊNH DANH CŨ trở lại tagline index.html (đổi tên nửa vời)")
s = sua(IDX,
        f'<div class="tagline">{TEN_MOI}',
        f'<div class="tagline">{TEN_CU}')
if s is None:
    print("  !!! không tìm thấy chỗ thay")
    ghi("1 định danh cũ sót lại (G10f chiều a)", None)
else:
    try:
        rc, out = chay()
        gf = ket(out, "G10f")
        print(f"  rc={rc}  G10f={gf}")
        in_bang_chung(out, "G10f")
        ghi("1 định danh cũ sót lại (G10f chiều a)", gf == "LỖI")
    finally:
        tra(IDX, s)

# ============================== CA 2 ==============================
print("=" * 92)
print('CA 2 — replace "lớp 10" TOÀN CỤC trong data/yccd.js (mất dấu phạm vi dữ liệu)')
print("       kỳ vọng: G10f BẮT, trong khi tên cũ ở 3 tệp thương hiệu vẫn sạch")
s = open(YCCD, encoding="utf-8").read()
n_lan = s.count("lớp 10")
print(f"  data/yccd.js có {n_lan} lần 'lớp 10' — thay hết thành 'cấp THPT'")
if n_lan == 0:
    print("  !!! không có chỗ nào để thay")
    ghi("2 mất dấu phạm vi YCCĐ (G10f chiều b)", None)
else:
    open(YCCD, "w", encoding="utf-8").write(s.replace("lớp 10", "cấp THPT"))
    try:
        rc, out = chay()
        gf = ket(out, "G10f")
        print(f"  rc={rc}  G10f={gf}")
        in_bang_chung(out, "G10f")
        ghi("2 mất dấu phạm vi YCCĐ (G10f chiều b)", gf == "LỖI")
    finally:
        tra(YCCD, s)

# ============================== CA 3 ==============================
print("=" * 92)
print("CA 3 — xoá đoạn khai 'Phạm vi dữ liệu đã kiểm chứng' khỏi README.md")
s = open(README, encoding="utf-8").read()
i = s.find("\n**Phạm vi dữ liệu đã kiểm chứng.**")
if i < 0:
    print("  !!! không tìm thấy đoạn khai phạm vi")
    ghi("3 README mất câu khai phạm vi (G10f chiều c)", None)
else:
    j = s.find("\n\n", i + 10)
    moi = s[:i] + s[j:]
    open(README, "w", encoding="utf-8").write(moi)
    print(f"  đã xoá {j - i} ký tự của đoạn khai phạm vi")
    try:
        rc, out = chay()
        gf = ket(out, "G10f")
        print(f"  rc={rc}  G10f={gf}")
        in_bang_chung(out, "G10f")
        ghi("3 README mất câu khai phạm vi (G10f chiều c)", gf == "LỖI")
    finally:
        tra(README, s)

# ============================== CA 4 (negative control) ==============================
print("=" * 92)
print("CA 4 — NEGATIVE CONTROL: xoá định danh MỚI khỏi js/kichban.js (logo kịch bản)")
print("       kỳ vọng: G10b BẮT (thiếu ở nơi thứ ba) nhưng G10f phải IM")
s = sua(KB, TEN_MOI, "Phòng thực hành AI")
if s is None:
    print("  !!! không tìm thấy định danh mới trong js/kichban.js")
    ghi("4 G10b bắt nơi thứ ba, G10f im (negative control)", None, dc=True)
else:
    try:
        rc, out = chay()
        gb, gf = ket(out, "G10b"), ket(out, "G10f")
        print(f"  rc={rc}  G10b={gb}  G10f={gf}")
        in_bang_chung(out, "G10b")
        dung = (gb == "LỖI" and gf == "ĐẠT")
        print(f"  ->  {'ĐÚNG: G10b bắt, G10f im (hai cổng chia việc)' if dung else 'SAI phân công'}")
        ghi("4 G10b bắt nơi thứ ba, G10f im (negative control)", dung, dc=True)
    finally:
        tra(KB, s)

# ============================== TỔNG KẾT ==============================
print("=" * 92)
def _dc(t):
    return t[2] if len(t) > 2 else False


so = sum(1 for t in ket_luan if t[1] is True)
tong = sum(1 for t in ket_luan if t[1] is not None)
so_pha = sum(1 for t in ket_luan if t[1] is True and not _dc(t))
so_dc = sum(1 for t in ket_luan if t[1] is True and _dc(t))
# Khuôn chung với 11 script kia, để máy đếm được: hai số PHẢI tách (xem docstring của ghi()).
print(f"KẾT LUẬN: {so}/{tong} ca đúng như kỳ vọng ({so_pha} ca PHÁ bị cổng bắt"
      f" + {so_dc} ca ĐỐI CHỨNG ÂM cổng im đúng)")
for t in ket_luan:
    ten, b = t[0], t[1]
    if b is None:
        print(f"  {ten}: BỎ QUA")
    elif _dc(t):
        print(f"  {ten}: " + ("KHÔNG BẮT OAN (đúng)" if b else "BẮT OAN — luật miễn trừ hỏng"))
    else:
        print(f"  {ten}: " + ("ĐÚNG" if b else "SAI KỲ VỌNG"))

rc, out = chay()
m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
print("=" * 92)
print(f"XÁC NHẬN SAU CÙNG: rc={rc}  {m.group(0) if m else '?'}  (phải về ĐẠT: hai số bằng nhau)")
for p, h in GOC.items():
    if sha(p) != h:
        print("  !!!", os.path.basename(p), "CHƯA khôi phục đúng")
sys.exit(0 if (so == tong and rc == 0) else 1)
