#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho cổng G15 (trạm ẩn ban đầu phải có lệnh hiện lại).

VÌ SAO PHẢI CHẠY: G15 vừa in ĐẠT 3/3 ngay lần chạy đầu. Nhưng một cổng chưa từng FAIL vì đúng
thứ nó canh thì chưa được chứng minh là CÓ THỂ fail — đó là bài học trả giá hai lần trong dự
án này (G11c in ĐẠT trong khi có nhánh chết; G14a in ĐẠT trong khi đang so sánh dữ liệu rác).

Ba ca:
  1 (G15c): xoá dòng `$("nm-tram5").style.display = "";` — tái tạo đúng lỗi thật đã làm Trạm 5
            vô hình từ commit f0936c8. Cổng phải kêu, và phải kêu ở G15c.
  2 (G15c): xoá dòng hiện lại của nm-tram0 — chứng minh cổng canh CẢ BA trạm chứ không chỉ
            trạm vừa sửa. Nếu chỉ bắt được ca 1 thì cổng thực chất là một phép kiểm ad-hoc.
  3 (G15b): đổi id trong index.html thành id khác -> cổng phải kêu ở G15b.

Bước chuẩn bị: sinh lại manifest TRƯỚC CA 0, và in rõ đã làm. Lý do: chính tools/nghiem_thu.py
nằm trong manifest, nên mỗi lần sửa cổng là G13b kêu và CA 0 đỏ vì lý do không phải lỗi sản
phẩm. Đã mất hai lần chạy vì đọc nhầm CA 0 đỏ thành "cổng hỏng" (Luật B trong skill
agentic-efficiency-loop).

Khôi phục bằng bản sao BYTES trong /tmp, không dùng `git checkout`: cây đang có thay đổi chưa
commit, git checkout sẽ trả về bản đã commit và XOÁ MẤT công sửa.
"""
import glob
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
GATE = ["python3", "tools/nghiem_thu.py"]
TOUCH = ["js/app.js", "index.html", "SHA256SUMS.txt"]


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
    out = r.stdout + r.stderr
    return r.returncode, out


def ca(so, ten, tep, sua, ma_cong):
    p = os.path.join(ROOT, tep)
    goc = open(p, encoding="utf-8").read()
    h0 = sha(p)
    try:
        moi = sua(goc)
        assert moi != goc, f"không phá được {tep} ({ten}) — NEO SAI, đọc mã thật trước đã"
        open(p, "w", encoding="utf-8").write(moi)
        rc, out = chay_cong()
        keu = f"[LỖI] {ma_cong}" in out
        tt = ("BẮT ĐƯỢC" if keu else
              ("KÊU NHƯNG SAI MÃ" if rc != 0 else "IM (KHÔNG RĂNG)"))
        print(f"  [{so}] {ten:44s}: rc={rc}  {tt}")
        if tt != "BẮT ĐƯỢC":
            for l in out.splitlines():
                if "KẾT QUẢ" in l or "[LỖI]" in l or "G15" in l:
                    print("       | " + l.strip()[:165])
        return tt == "BẮT ĐƯỢC"
    finally:
        open(p, "w", encoding="utf-8").write(goc)
        khop = sha(p) == h0
        print(f"       khôi phục {tep}: hash {'KHỚP gốc' if khop else 'LỆCH !!!'}")
        if not khop:
            print("       !!! DỪNG: tệp không về nguyên trạng.")
            sys.exit(9)


def main():
    print("=" * 96)
    print("MUTATION TEST CỔNG G15 — trạm ẩn phải có lệnh hiện lại")
    print("=" * 96)
    sinh_manifest()
    tmp = tempfile.mkdtemp(prefix="g15mut-")
    for f in TOUCH:
        shutil.copy2(os.path.join(ROOT, f), os.path.join(tmp, f.replace("/", "_")))
        print(f"  backup {f} sha={sha(os.path.join(ROOT, f))[:12]}")

    print("\n[CA 0] nguyên trạng — cổng phải ĐẠT")
    rc, out = chay_cong()
    ket = [l for l in out.splitlines() if "KẾT QUẢ" in l]
    print(f"       rc={rc}  {ket[0] if ket else '?'}")
    if rc != 0:
        print("       !!! nguyên trạng đã đỏ: sửa trước khi mutation test.")
        for l in out.splitlines():
            if "[LỖI]" in l:
                print("       | " + l.strip()[:160])
        return 1

    def xoa_hien_tram5(s):
        # xoá ĐÚNG dòng vừa được thêm để sửa lỗi Trạm 5 vô hình (tái tạo lỗi f0936c8)
        target = '    $("nm-tram5").style.display = "";\n'
        assert target in s, "neo sai: không thấy dòng hiện lại nm-tram5"
        return s.replace(target, "", 1)

    def xoa_hien_tram0(s):
        target = '    $("nm-tram0").style.display = "";\n'
        assert target in s, "neo sai: không thấy dòng hiện lại nm-tram0"
        return s.replace(target, "", 1)

    def doi_id_tram1(s):
        return s.replace('<div class="card" id="nm-tram1"',
                         '<div class="card" id="nm-tram1-DOI-TEN"', 1)

    kq = []
    print()
    kq.append(ca(1, "xoá lệnh hiện lại nm-tram5 (lỗi thật)", "js/app.js",
                 xoa_hien_tram5, "G15c"))
    kq.append(ca(2, "xoá lệnh hiện lại nm-tram0 (trạm khác)", "js/app.js",
                 xoa_hien_tram0, "G15c"))
    kq.append(ca(3, "đổi id nm-tram1 trong index.html", "index.html",
                 doi_id_tram1, "G15b"))

    print("\n" + "=" * 96)
    print(f"KẾT LUẬN: {sum(kq)}/{len(kq)} ca phá đều bị G15 bắt")
    for i, o in enumerate(kq, 1):
        print(f"  ca {i}: {'BẮT ĐƯỢC' if o else 'CỔNG IM — G15 không có răng cho ca đó'}")
    print("=" * 96)
    rc, out = chay_cong()
    ket = [l for l in out.splitlines() if "KẾT QUẢ" in l]
    print(f"XÁC NHẬN SAU CÙNG: rc={rc}  {ket[0] if ket else '?'}   (phải về ĐẠT)")
    shutil.rmtree(tmp)
    return 0 if (all(kq) and rc == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
