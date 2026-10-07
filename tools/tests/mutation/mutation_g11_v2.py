#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST v2 cho cổng G11 — chứng minh bản MỞ RỘNG có răng.

VÌ SAO CÓ v2 (không phải chạy lại v1):
  v1 chỉ chứng minh G11 có răng với 2 tệp js/bt13.js và js/bt09.js. Reviewer độc lập
  chỉ ra tiếp: lớp lỗi icon mồ côi đã TỪNG xảy ra ở js/duDoan.js — tệp KHÔNG nằm trong
  2 tệp đó. Nên phép kiểm quan trọng nhất ở đây là CA 1: phá icon trong MỘT TỆP KHÁC
  (js/duDoan.js). Nếu cổng vẫn ĐẠT thì bản mở rộng là hình thức, không phải phép kiểm.
  Thêm CA 5 cho G11e (host id) — thiếu sót #2 reviewer nêu, trước đây không ai kiểm.

BẪY ĐÃ SỬA (giữ nguyên từ v1, ghi lại vì đã suýt tự phá công mình): KHÔNG khôi phục
bằng `git checkout --`. Bản vá của lượt này CHƯA COMMIT, nên `git checkout` trả tệp về
bản đã commit — tức XOÁ LUÔN công sửa vừa làm, và bài test báo "cổng mù" trong khi
chính nó gây ra. Khôi phục bằng bản sao BYTES lưu trong /tmp trước khi phá.

GHI CHÚ AN TOÀN: trong tệp này có chuỗi `fb.innerHTML = "<i>" + text + "</i>"`. Đó là
CHUỖI PHÁ CỐ Ý của mutation test — nó KHÔNG BAO GIỜ được ghi vào sản phẩm, chỉ được
chèn tạm để chứng minh cổng G11c bắt được lỗi rồi bị khôi phục ngay trong khối finally.
Mã sản phẩm thật (js/bt09.js) không có dòng đó, và cổng G11c cùng cổng kiem_noi_dung.py
đều kiểm điều này trên cây nguồn.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

APP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TU = ["js/bt13.js", "js/bt09.js", "js/duDoan.js", "index.html"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay(ma="G11"):
    r = subprocess.run([sys.executable, "tools/nghiem_thu.py", ma],
                       cwd=APP, capture_output=True, text=True, timeout=300)
    return r.returncode, r.stdout


def main():
    bak = tempfile.mkdtemp(prefix="g11v2-bak-")
    goc = {}
    for f in TU:
        p = os.path.join(APP, f)
        goc[f] = sha(p)
        shutil.copy(p, os.path.join(bak, f.replace("/", "__")))
    print("=" * 90)
    print("MUTATION TEST v2 CỔNG G11 — chứng minh bản MỞ RỘNG có răng")
    print(f"bản gốc: {bak} ({len(TU)} tệp)")
    print("=" * 90)
    ket = []

    def phuc(f):
        shutil.copy(os.path.join(bak, f.replace("/", "__")), os.path.join(APP, f))
        return sha(os.path.join(APP, f)) == goc[f]

    def ca(so, ten, tep, sua, ma_ky_vong, mo_ta_phuc):
        """Phá `tep` bằng hàm `sua`, yêu cầu cổng báo LỖI ở `ma_ky_vong`."""
        f = tep
        try:
            p = os.path.join(APP, f)
            s = open(p, encoding="utf-8").read()
            s2 = sua(s)
            assert s2 != s, f"không phá được {f} ({ten})"
            open(p, "w", encoding="utf-8").write(s2)
            rc, out = chay()
            bat = (ma_ky_vong in out and "[LỖI]" in out)
            print(f"[CA {so}] {ten:32s}: rc={rc}  "
                  f"{'CỔNG BẮT ĐƯỢC (' + ma_ky_vong + ' LỖI)' if bat else 'CỔNG MÙ — KHÔNG BẮT'}")
            ket.append((ten, bat))
        finally:
            k = phuc(f)
        print(f"        {mo_ta_phuc} {f}: hash {'KHỚP gốc' if k else 'LỆCH!'}")
        return k

    # ---------- CA 0: nguyên trạng phải ĐẠT 5/5 ----------
    rc, out = chay()
    # BẢN VÁ (06/10): neo cũ đòi chuỗi "5/5 tiêu chí đạt" — viết từ lúc bộ tiêu chí còn 5
    # dòng. Nay dòng tổng kết là "53/53 tiêu chí đạt", nên nhánh này LUÔN báo
    # "KHÔNG ĐẠT — bất thường" dù cổng xanh hoàn toàn (rc=0). Một bài test tự báo hỏng sai
    # sẽ bị người đọc bỏ qua, và từ đó nó không còn canh được gì — đúng lớp lỗi mà chính
    # bài test này sinh ra để chống. Đọc đúng thứ cần đọc: rc=0 VÀ không có dòng CÒN LỖI.
    ok0 = rc == 0 and "tiêu chí đạt" in out and "CÒN LỖI" not in out
    print(f"\n[CA 0] nguyên trạng                    : rc={rc}  "
          f"{'ĐẠT 5/5' if ok0 else 'KHÔNG ĐẠT — bất thường'}")
    ket.append(("nguyên trạng ĐẠT 5/5", ok0))

    # ---------- CA 1: QUAN TRỌNG NHẤT — phá icon ở tệp KHÁC (duDoan.js) ----------
    # Tìm một lời gọi svgIco thật trong duDoan.js rồi đổi sang tên không tồn tại.
    dd = open(os.path.join(APP, "js/duDoan.js"), encoding="utf-8").read()
    dd_song = re.sub(r"/\*.*?\*/", " ", dd, flags=re.S)
    dd_song = re.sub(r"(?m)//[^\n]*", " ", dd_song)
    m = re.search(r'svgIco\(\s*"([\w-]+)"\s*\)', dd_song)
    assert m, "js/duDoan.js không còn lời gọi svgIco nào — cập nhật bài test"
    icon_goc = m.group(1)
    ca(1, f"phá icon ở js/duDoan.js ({icon_goc})", "js/duDoan.js",
       lambda s: s.replace(f'svgIco("{icon_goc}")',
                           'svgIco("icon-khong-ton-tai-xyz")', 1),
       "G11b", "khôi phục")

    # ---------- CA 2: phá số comment ở bt13 ----------
    ca(2, "sửa số comment bt13 -> 99", "js/bt13.js",
       lambda s: s.replace("tệp này có **9 chỗ**", "tệp này có **99 chỗ**", 1),
       "G11d", "khôi phục")

    # ---------- CA 3: cho chữ học sinh vào innerHTML ở bt09 ----------
    # ANCHOR ĐÃ SỬA: bản đầu dùng chuỗi `((dungNhom && duBa) ? "dung" : "sai")` —
    # KHÔNG tồn tại trong mã thật. Bài test ném AssertionError và em suýt kết luận sai
    # là "cổng mù". Mã thật (dòng 307) là `fb.className = "phanhoi " + (kq.dat ? ...)`.
    # Biến chứa chữ học sinh gõ (đo bằng search_files): `text` = taCau.value.trim().
    # LUẬT: neo bài test phải lấy bằng cách ĐỌC mã thật, không viết từ trí nhớ.
    ca(3, "chữ HS đi vào innerHTML (bt09)", "js/bt09.js",
       lambda s: s.replace(
           '      fb.className = "phanhoi " + (kq.dat ? "dung" : "sai");',
           '      fb.innerHTML = "<i>" + text + "</i>";\n'
           '      fb.className = "phanhoi " + (kq.dat ? "dung" : "sai");', 1),
       "G11c", "khôi phục")

    # ---------- CA 4: bỏ thẻ script bt09 ----------
    ca(4, "bỏ thẻ script bt09.js", "index.html",
       lambda s: s.replace('<script src="js/bt09.js"></script>', "", 1),
       "G11a", "khôi phục")

    # ---------- CA 5: đổi tên host id kt-bt13 (G11e) ----------
    ca(5, 'đổi host id kt-bt13 -> kt-bt13-X', "index.html",
       lambda s: s.replace('id="kt-bt13"', 'id="kt-bt13-X"', 1),
       "G11e", "khôi phục")

    # ---------- kết ----------
    rc, out = chay()
    sach = "tiêu chí đạt" in out and "CÒN LỖI" not in out
    print(f"\n[CUỐI] sau mọi lần khôi phục      : rc={rc}  "
          f"{'ĐẠT 5/5 (cây về nguyên trạng)' if sach else 'KHÔNG ĐẠT — CÂY CHƯA SẠCH!'}")
    for x in TU:
        print(f"        hash {x:16s}: "
              f"{'KHỚP gốc' if sha(os.path.join(APP, x)) == goc[x] else 'LỆCH!'}")
    gs = subprocess.run(["git", "-C", APP, "status", "--porcelain"],
                        capture_output=True, text=True).stdout
    n = len(gs.strip().splitlines()) if gs.strip() else 0
    print(f"        git status: {n} tệp thay đổi (kỳ vọng 4: 3 tệp vá + SHA256SUMS)")

    print("\n" + "=" * 90)
    for ten, ok in ket:
        print(f"  {'ĐẠT' if ok else 'HỎNG'}  {ten}")
    tong = sum(1 for _, ok in ket[1:] if ok)
    print(f"\n  CỔNG CÓ RĂNG: bắt {tong}/5 ca phá · nguyên trạng ĐẠT: {ket[0][1]}")
    print("=" * 90)
    shutil.rmtree(bak, ignore_errors=True)
    return 0 if (tong == 5 and ok0 and sach) else 1


if __name__ == "__main__":
    sys.exit(main())
