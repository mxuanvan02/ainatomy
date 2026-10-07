#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho cổng G13 (toàn vẹn manifest SHA256SUMS).

VÌ SAO PHẢI CHẠY: G13a đã tự chứng minh có răng — khi manifest còn 72 tệp mà git theo dõi
89, nó in LỖI và kể đích danh tools/nghiem_thu.py cùng PDF văn bản Bộ. Nhưng G13b và G13c
chưa từng FAIL, và một cổng chưa từng fail thì chưa được chứng minh là CÓ THỂ fail (đúng
lớp lỗi G11c đã mắc: in ĐẠT trong khi nhánh dò có một nhánh chết).

Ba ca:
  1 (G13b): sửa MỘT tệp sản phẩm mà không sinh lại manifest -> hash lệch -> cổng phải kêu.
            Đây là ca thực tế nhất: chính là cách một bản vá mã làm manifest cũ đi.
  2 (G13c): thêm một dòng "mồ côi" vào manifest (tệp git không theo dõi) -> cổng phải kêu.
  3 (G13a): xoá một tệp khỏi manifest (giả lập tệp mới bị bỏ sót) -> cổng phải kêu.

Mỗi ca: sửa -> chạy cổng -> đòi rc != 0 VÀ đúng mã cổng đó kêu -> khôi phục -> đòi hash
khớp bản gốc. Khôi phục bằng BẢN SAO BYTES trong /tmp, tuyệt đối không dùng `git checkout`
(cây đang có thay đổi chưa commit; git checkout sẽ trả về bản đã commit và XOÁ MẤT công sửa).
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GATE = ["python3", "tools/nghiem_thu.py"]
TOUCH = ["js/muc3.js", "SHA256SUMS.txt"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong():
    r = subprocess.run(GATE, cwd=ROOT, capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr
    m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
    return r.returncode, (m.group(0) if m else "?"), out


def ca(so, ten, f, sua, ma_cong):
    p = os.path.join(ROOT, f)
    goc = open(p, encoding="utf-8").read()
    h0 = sha(p)
    try:
        moi = sua(goc)
        assert moi != goc, f"không phá được {f} ({ten}) — NEO SAI, đọc mã thật trước đã"
        open(p, "w", encoding="utf-8").write(moi)
        rc, ket, out = chay_cong()
        keu = f"[LỖI] {ma_cong}" in out
        tt = ("BẮT ĐƯỢC" if (rc != 0 and keu) else
              ("IM (KHÔNG RĂNG)" if rc == 0 else "KÊU NHƯNG SAI MÃ"))
        print(f"  [{so}] {ten:44s}: rc={rc}  {tt}")
        if tt != "BẮT ĐƯỢC":
            trich = [l for l in out.splitlines()
                     if "KẾT QUẢ" in l or "[LỖI]" in l or ma_cong in l]
            print(f"       !!! kỳ vọng {ma_cong} kêu. Trích:")
            for l in trich[:5]:
                print("       | " + l.strip()[:160])
        return tt == "BẮT ĐƯỢC"
    finally:
        open(p, "w", encoding="utf-8").write(goc)
        khop = sha(p) == h0
        print(f"       khôi phục {f}: hash {'KHỚP gốc' if khop else 'LỆCH !!!'}")
        if not khop:
            print("       !!! DỪNG: tệp không về nguyên trạng.")
            sys.exit(9)


def main():
    print("=" * 96)
    print("MUTATION TEST CỔNG G13 — toàn vẹn manifest SHA256SUMS")
    print("=" * 96)
    tmp = tempfile.mkdtemp(prefix="g13mut-")
    for f in TOUCH:
        shutil.copy2(os.path.join(ROOT, f), os.path.join(tmp, f.replace("/", "_")))
        print(f"  backup {f} sha={sha(os.path.join(ROOT, f))[:12]}")

    print("\n[CA 0] nguyên trạng — cổng phải ĐẠT")
    rc, ket, _ = chay_cong()
    print(f"       rc={rc}  {ket}")
    if rc != 0:
        print("       !!! nguyên trạng đã đỏ: sửa trước khi mutation test.")
        return 1

    kq = []
    print()
    # CA 1 — G13b: sửa mã mà KHÔNG sinh lại manifest (tình huống thực tế nhất)
    kq.append(ca(1, "sửa js/muc3.js, để manifest cũ (G13b)", "js/muc3.js",
                 lambda s: s.replace("window.MX_MUC3 = {", "window.MX_MUC3 = {  "),
                 "G13b"))

    # CA 2 — G13c: thêm dòng mồ côi vào manifest (tệp git không theo dõi)
    def them_mo_coi(s):
        fake = "0" * 64
        return s.rstrip("\n") + f"\n{fake}  js/tep_khong_thuoc_repo.js\n"
    kq.append(ca(2, "thêm dòng mồ côi vào manifest (G13c)", "SHA256SUMS.txt",
                 them_mo_coi, "G13c"))

    # CA 3 — G13a: xoá một tệp khỏi manifest (giả lập tệp mới bị bỏ sót)
    def xoa_mot_tep(s):
        dong = s.rstrip("\n").split("\n")
        # xoá dòng chứa tools/nghiem_thu.py — đúng ca đã xảy ra thật
        moi = [d for d in dong if "tools/nghiem_thu.py" not in d]
        assert len(moi) == len(dong) - 1, "neo sai: không thấy dòng tools/nghiem_thu.py"
        return "\n".join(moi) + "\n"
    kq.append(ca(3, "xoá tools/nghiem_thu.py khỏi manifest (G13a)", "SHA256SUMS.txt",
                 xoa_mot_tep, "G13a"))

    print("\n" + "=" * 96)
    print(f"KẾT LUẬN: {sum(kq)}/{len(kq)} ca phá đều bị G13 bắt")
    for i, o in enumerate(kq, 1):
        print(f"  ca {i}: {'BẮT ĐƯỢC' if o else 'CỔNG IM — G13 không có răng cho ca đó'}")
    print("=" * 96)
    rc, ket, _ = chay_cong()
    print(f"XÁC NHẬN SAU CÙNG: rc={rc}  {ket}   (phải về ĐẠT)")
    shutil.rmtree(tmp)
    return 0 if (all(kq) and rc == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
