#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho cổng G16 (ba bản khai cột CSV phải khớp nhau).

VÌ SAO PHẢI CHẠY: G16 in ĐẠT 4/4 ngay lần chạy đầu. Nhưng một cổng chưa từng FAIL vì đúng thứ
nó canh thì chưa được chứng minh là CÓ THỂ fail. Dự án này đã trả giá cho niềm tin đó ba lần:
G11c in ĐẠT trong khi có nhánh chết · G14a in ĐẠT trong khi đang so dữ liệu rác · G14c có một
chiều là code chết vì tập được xây từ chính tập kia.

Bốn ca, mỗi ca phá đúng thứ một tiêu chí con tuyên bố đang canh:
  1 (G16b): xoá một cột khỏi dict trong doc_json() — tái tạo đúng lỗi thật vừa tìm được
            (7 cột mất, làm trống khối TIẾN TRÌNH PRE/POST). Đây là ca quan trọng nhất.
  2 (G16c): thêm một cột lạ vào doc_json() — cột đó sẽ bị DictWriter(extrasaction="ignore")
            vứt âm thầm khi ghi tệp gộp.
  3 (G16d): đổi tên một cột trong header xuatCSV (js/engine.js) cho lệch với HDR.
  4 (G16d): đổi THỨ TỰ hai cột trong header xuatCSV — tên vẫn đủ, chỉ khác thứ tự.
            Ca này kiểm xem cổng có thật sự so thứ tự (như tên tiêu chí tuyên bố) hay chỉ so
            tập hợp. Nếu cổng chỉ so tập hợp thì ca này sẽ IM và tôi phải sửa cổng hoặc sửa
            lời tuyên bố — không được để tên tiêu chí hứa nhiều hơn mã làm.

Bước chuẩn bị: sinh lại manifest TRƯỚC CA 0 và in rõ. Lý do: chính tools/nghiem_thu.py nằm
trong manifest, nên mỗi lần sửa cổng là G13b kêu và CA 0 đỏ vì lý do không phải lỗi sản phẩm.
Đã mất hai lần chạy vì đọc nhầm CA 0 đỏ thành "cổng hỏng".

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
TOUCH = ["tools/gop_csv.py", "js/engine.js", "SHA256SUMS.txt"]


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
        print(f"  [{so}] {ten:48s}: rc={rc}  {tt}")
        if tt != "BẮT ĐƯỢC":
            for l in out.splitlines():
                if "KẾT QUẢ" in l or "[LỖI]" in l or "G16" in l:
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
    print("MUTATION TEST CỔNG G16 — ba bản khai cột CSV phải khớp nhau")
    print("=" * 96)
    sinh_manifest()
    tmp = tempfile.mkdtemp(prefix="g16mut-")
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

    # ---- CA 1 (G16b): xoá cột che_do khỏi doc_json — tái tạo đúng lỗi thật ----
    def xoa_cot_doc_json(s):
        target = '                "che_do": sk.get("cheDo", ""),\n'
        assert target in s, "neo sai: không thấy dòng che_do trong doc_json"
        return s.replace(target, "", 1)

    # ---- CA 2 (G16c): thêm cột lạ vào doc_json ----
    def them_cot_la(s):
        target = '                "su_kien": sk.get("suKien", ""),'
        assert target in s, "neo sai: không thấy dòng su_kien trong doc_json"
        return s.replace(target, target + '\n                "cot_la_khong_co_trong_hdr": 1,', 1)

    # ---- CA 3 (G16d): đổi tên một cột trong header xuatCSV ----
    def doi_ten_cot_engine(s):
        m = re.search(r'const rows = \[\[(.*?)\]\];', s, re.S)
        assert m, "neo sai: không thấy header xuatCSV trong js/engine.js"
        return s[:m.start(1)] + m.group(1).replace('"su_kien"', '"su_kien_DOI_TEN"') + s[m.end(1):]

    # ---- CA 4 (G16d): đổi THỨ TỰ hai cột, giữ nguyên tập hợp ----
    def doi_thu_tu_cot(s):
        m = re.search(r'const rows = \[\[(.*?)\]\];', s, re.S)
        assert m, "neo sai: không thấy header xuatCSV trong js/engine.js"
        body = m.group(1)
        assert '"su_kien","phai_lap"' in body, "neo sai: không thấy cặp su_kien,phai_lap cạnh nhau"
        return s[:m.start(1)] + body.replace('"su_kien","phai_lap"', '"phai_lap","su_kien"') + s[m.end(1):]

    kq = []
    print()
    kq.append(ca(1, "doc_json: xoá cột che_do (lỗi thật)", "tools/gop_csv.py",
                 xoa_cot_doc_json, "G16b"))
    kq.append(ca(2, "doc_json: thêm cột lạ ngoài HDR", "tools/gop_csv.py",
                 them_cot_la, "G16c"))
    kq.append(ca(3, "engine.js: đổi tên cột su_kien", "js/engine.js",
                 doi_ten_cot_engine, "G16d"))
    kq.append(ca(4, "engine.js: đổi THỨ TỰ 2 cột (đủ tên)", "js/engine.js",
                 doi_thu_tu_cot, "G16d"))

    print("\n" + "=" * 96)
    print(f"KẾT LUẬN: {sum(kq)}/{len(kq)} ca phá đều bị G16 bắt")
    for i, o in enumerate(kq, 1):
        print(f"  ca {i}: {'BẮT ĐƯỢC' if o else 'CỔNG IM — G16 không có răng cho ca đó'}")
    print("=" * 96)
    rc, out = chay_cong()
    ket = [l for l in out.splitlines() if "KẾT QUẢ" in l]
    print(f"XÁC NHẬN SAU CÙNG: rc={rc}  {ket[0] if ket else '?'}   (phải về ĐẠT)")
    shutil.rmtree(tmp)
    return 0 if (all(kq) and rc == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
