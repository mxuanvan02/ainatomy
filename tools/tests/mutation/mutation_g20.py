#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST CỔNG G20 — bốn ca tính điểm (ba ca phá + một ca đối chứng âm).

VÌ SAO CÓ TỆP NÀY. G20 thêm ngày 09/10 để canh lời khai trong HỒ SƠ NỘP GIÁM KHẢO:
"56 câu sinh LLM đã merge vào app ở chế độ ghi rõ 'chờ duyệt'". Lời khai đó từng SAI
(mã merge vô điều kiện, grep "chờ duyệt|choDuyet|pending" ra 0) và một reviewer độc
lập bắt được. Sau khi sửa mã, cổng G20 phải có mutation test — một cổng mới ĐẠT ngay
lần chạy đầu chưa chứng minh nó thấy được gì; repo này đã có tiền lệ cổng in ĐẠT trong
khi mù (G14c một chiều là code chết, G10f chiều c bị một câu tham chiếu làm rỗng).

BỐN CA — mỗi ca phá MỘT trong ba chiều, vì ba chiều đó là ba cách KHÁC NHAU để nhãn
chết mà trông vẫn có. Một cổng chỉ kiểm "repo có chữ choDuyet" sẽ ĐẠT ở cả ba ca phá
bên dưới, đó là lý do phải tách ba chiều.

  CA 1 — xoá phần tử `dt-choDuyet` khỏi index.html      -> G20a PHẢI kêu
  CA 2 — xoá chuỗi cảnh báo trong app.js (giữ phần tử,
         giữ cờ, giữ lệnh tra phần tử)                    -> G20b PHẢI kêu
         Đây là ca nguy hiểm nhất: nhãn vẫn "có" trong mã, học sinh vẫn không thấy gì.
  CA 3 — bỏ `choDuyet: 1` lúc merge                      -> G20c PHẢI kêu
         Ca này cũng nguy hiểm ngang: mọi dòng mã hiển thị vẫn còn nguyên, chỉ điều
         kiện không bao giờ đúng nên nhãn không bao giờ hiện.
  CA 4 — ĐỐI CHỨNG ÂM: repo nguyên trạng                 -> G20a/b/c đều IM

CÁCH PHÁ: sửa tệp có thật rồi khôi phục bằng hash (khác mutation_g18/g19 là tạo tệp
thăm dò, vì G20 soi ĐÚNG HAI tệp cụ thể nên phải đụng vào chúng). Mỗi ca khôi phục
trong khối finally và xác nhận hash về đúng bản gốc — một ca chết giữa đường mà để lại
index.html bị hỏng thì app hỏng thật.

CÁCH CHẠY:  python3 tools/tests/mutation/mutation_g20.py
"""
import hashlib
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CONG = os.path.join(REPO, "tools", "nghiem_thu.py")
IDX = os.path.join(REPO, "index.html")
APP = os.path.join(REPO, "js", "app.js")

# Ba chuỗi cần phá. Đọc từ TỆP THẬT lúc chạy (không gõ lại từ trí nhớ) — sai một ký tự
# là ca phá thành không-làm-gì và cổng trông như có răng trong khi mù.
PHAN_TU = '<p id="dt-choDuyet" class="nho vang" style="display:none"></p>'
CANH_BAO = "CHƯA được tác giả xác nhận nhãn"
CO_MERGE = "choDuyet: 1"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong(nhom="G20"):
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
            return ln.strip()[:220]
    return ""


GOC = {p: sha(p) for p in (IDX, APP)}
ket_luan = []


def ghi(ten, dat, dc=False):
    """`dc=True` = ĐỐI CHỨNG ÂM (kỳ vọng cổng IM). Hai số phải tách trong dòng KẾT LUẬN
    để dem_ca.py đếm được và để không khai quá (luật ghi trong dem_ca.py)."""
    ket_luan.append((ten, dat, dc))
    return dat


def sua(p, cu, n=1):
    """Xoá n lần xuất hiện của `cu`. Trả bản gốc, hoặc None nếu chuỗi không có
    (để ca phá không âm thầm thành không-làm-gì rồi báo 'cổng im đúng')."""
    s = open(p, encoding="utf-8").read()
    if cu not in s:
        return None
    open(p, "w", encoding="utf-8").write(s.replace(cu, "", n))
    return s


def tra(p, s):
    open(p, "w", encoding="utf-8").write(s)
    print("  khôi phục:", "hash KHỚP gốc" if sha(p) == GOC[p] else "!!! LỆCH — SỬA TAY NGAY")


def main():
    for p, chuoi in ((IDX, PHAN_TU), (APP, CANH_BAO), (APP, CO_MERGE)):
        if chuoi not in open(p, encoding="utf-8").read():
            print(f"!!! không tìm thấy {chuoi[:40]!r} trong {os.path.relpath(p, REPO)}")
            print("    Mã đã đổi cấu trúc — cập nhật hằng ở đầu script này, đừng đoán chuỗi mới.")
            return 2

    # ============================== CA 0 — baseline ==============================
    print("=" * 100)
    print("CA 0 — baseline: repo nguyên trạng, G20a/b/c phải ĐẠT cả ba")
    rc, out = chay_cong()
    a, b, c = ket(out, "G20a"), ket(out, "G20b"), ket(out, "G20c")
    print(f"  rc={rc}  G20a={a}  G20b={b}  G20c={c}")
    if not (a == b == c == "ĐẠT"):
        print("  !!! baseline đã đỏ — mọi ca bên dưới vô nghĩa. Sửa cổng/mã trước.")
        return 1

    # ============================== CA 1 — phá G20a ==============================
    print("=" * 100)
    print("CA 1 — xoá phần tử dt-choDuyet khỏi index.html  -> G20a PHẢI kêu")
    s = sua(IDX, PHAN_TU)
    if s is None:
        ghi("1 mất phần tử trong index.html -> G20a bắt", None)
    else:
        try:
            rc, out = chay_cong()
            a = ket(out, "G20a")
            print(f"  rc={rc}  G20a={a}")
            if a == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G20a"))
            ghi("1 mất phần tử trong index.html -> G20a bắt", a == "LỖI")
        finally:
            tra(IDX, s)

    # ============================== CA 2 — phá G20b ==============================
    print("=" * 100)
    print("CA 2 — xoá CHUỖI CẢNH BÁO trong app.js (phần tử + cờ vẫn còn)  -> G20b PHẢI kêu")
    print("       đây là ca 'nhãn chết mà trông vẫn có': mã vẫn tra phần tử, vẫn gắn cờ")
    s = sua(APP, CANH_BAO)
    if s is None:
        ghi("2 mất chuỗi cảnh báo -> G20b bắt", None)
    else:
        try:
            rc, out = chay_cong()
            b = ket(out, "G20b")
            print(f"  rc={rc}  G20b={b}")
            if b == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G20b"))
            ghi("2 mất chuỗi cảnh báo -> G20b bắt", b == "LỖI")
        finally:
            tra(APP, s)

    # ============================== CA 3 — phá G20c ==============================
    print("=" * 100)
    print("CA 3 — bỏ `choDuyet: 1` lúc merge (mọi dòng hiển thị còn nguyên)  -> G20c PHẢI kêu")
    s = sua(APP, CO_MERGE)
    if s is None:
        ghi("3 mất cờ lúc merge -> G20c bắt", None)
    else:
        try:
            rc, out = chay_cong()
            c = ket(out, "G20c")
            print(f"  rc={rc}  G20c={c}")
            if c == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G20c"))
            ghi("3 mất cờ lúc merge -> G20c bắt", c == "LỖI")
        finally:
            tra(APP, s)

    # ============================== CA 4 — đối chứng âm ==============================
    print("=" * 100)
    print("CA 4 — ĐỐI CHỨNG ÂM: repo nguyên trạng thì G20a/b/c PHẢI IM (ĐẠT)")
    rc, out = chay_cong()
    a, b, c = ket(out, "G20a"), ket(out, "G20b"), ket(out, "G20c")
    print(f"  rc={rc}  G20a={a}  G20b={b}  G20c={c}")
    ghi("4 repo nguyên trạng -> G20 im cả ba (đối chứng âm)", a == b == c == "ĐẠT", dc=True)

    # ============================== TỔNG KẾT ==============================
    print("=" * 100)
    con_sot = any(sha(p) != h for p, h in GOC.items())
    print(f"[XÁC NHẬN] tệp nào chưa khôi phục đúng: {con_sot} (phải False)")
    rc2, _ = chay_cong()
    ran = [(t, o, d) for t, o, d in ket_luan if o is not None]
    so = sum(1 for _, o, _ in ran if o)
    so_pha = sum(1 for _, o, d in ran if o and not d)
    so_dc = sum(1 for _, o, d in ran if o and d)
    # Khuôn A của dem_ca.py — hai số PHẢI tách, gộp lại là khai quá.
    print(f"\nKẾT LUẬN: {so}/{len(ran)} ca đúng như kỳ vọng ({so_pha} ca PHÁ bị cổng bắt"
          f" + {so_dc} ca ĐỐI CHỨNG ÂM cổng im đúng)")
    for ten, o, dc in ket_luan:
        if o is None:
            print(f"  {ten}: BỎ QUA")
            continue
        nhan = ("KHÔNG BẮT OAN (đúng)" if o else "BẮT OAN — cổng hỏng") if dc \
            else ("ĐÚNG" if o else "SAI KỲ VỌNG")
        print(f"  {ten}: {nhan}")
    print("=" * 100)
    return 0 if (so == len(ran) and not con_sot and rc2 == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
