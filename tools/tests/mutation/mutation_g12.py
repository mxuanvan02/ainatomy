#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho cổng G12 (chống mẹo làm bài không cần đọc).

VÌ SAO PHẢI CHẠY: G12 vừa được thêm và in ĐẠT cả ba phép. Nhưng một cổng chưa từng FAIL
thì chưa được chứng minh là nó CÓ THỂ fail — nó có thể đang đọc nhầm chỗ, như G11c đã từng
(in "0 chỗ chèn biến .value" trong khi có một nhánh chết và bỏ lọt 5/5 dạng nguy hiểm).
Cách duy nhất: PHÁ đúng thứ cổng khai là đang canh, rồi xem cổng có kêu không.

Ba ca, mỗi ca phá một lớp mà G12 khai là đang canh:
  ca 1 (G12a): bỏ lời gọi xaoLuaChon ở một tệp vẽ phương án -> mẹo "luôn bấm B" sống lại.
  ca 2 (G12b): đổi chữ cái hiển thị về nhãn cố định `l.id.toUpperCase()` -> xáo vị trí
               thành vô nghĩa vì đáp án vẫn luôn hiện chữ B.
  ca 3 (G12c): làm khoản nợ nội dung PHÌNH ra (nối dài phương án đúng) -> cổng phải kêu
               vì tỉ lệ vượt mốc 82,9%.

Mỗi ca: sửa -> chạy cổng -> đòi rc != 0 VÀ đúng mã cổng đó kêu -> khôi phục -> đòi hash
khớp bản gốc. Không khôi phục được thì DỪNG NGAY, không chạy ca tiếp.

KHÔI PHỤC BẰNG BẢN SAO BYTES, KHÔNG dùng `git checkout`: cây đang có thay đổi chưa commit,
`git checkout --` sẽ trả về bản đã commit và XOÁ MẤT công sửa (đã từng tự phá như vậy).
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
TOUCH = ["js/tinhhuong.js", "js/app.js"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong():
    r = subprocess.run(GATE, cwd=ROOT, capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr
    m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
    return r.returncode, (m.group(0) if m else "KHONG DOC DUOC"), out


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
        print(f"  [{so}] {ten:46s}: rc={rc}  {tt}")
        if tt != "BẮT ĐƯỢC":
            trich = [l for l in out.splitlines() if "KẾT QUẢ" in l or "[LỖI]" in l or ma_cong in l]
            print("       !!! kỳ vọng " + ma_cong + " kêu. Trích:")
            for l in trich[:6]:
                print("       | " + l.strip()[:150])
        return tt == "BẮT ĐƯỢC"
    finally:
        open(p, "w", encoding="utf-8").write(goc)
        khop = (sha(p) == h0)
        print(f"       khôi phục {f}: hash {'KHỚP gốc' if khop else 'LỆCH !!!'}")
        if not khop:
            print("       !!! DỪNG: tệp không về nguyên trạng.")
            sys.exit(9)


def main():
    print("=" * 100)
    print("MUTATION TEST CỔNG G12 — hai ca phá đúng thứ cổng khai là đang canh (G12a, G12b)")
    print("  (G12c có ca riêng ở mut_g12c.py — xem ghi chú trong main() vì sao tách ra)")
    print("=" * 100)
    tmp = tempfile.mkdtemp(prefix="g12mut-")
    for f in TOUCH:
        shutil.copy2(os.path.join(ROOT, f), os.path.join(tmp, f.replace("/", "_")))
        print(f"  backup {f} sha={sha(os.path.join(ROOT, f))[:12]}")

    print("\n[CA 0] nguyên trạng — cổng phải ĐẠT: hai số bằng nhau")
    rc, ket, _ = chay_cong()
    print(f"       rc={rc}  {ket}")
    if rc != 0:
        print("       !!! nguyên trạng đã đỏ: sửa trước khi mutation test.")
        return 1

    kq = []
    print()
    # CA 1 — G12a: bỏ xáo vị trí ở tinhhuong.js (nơi mẹo đạt 92%)
    kq.append(ca(1, "tinhhuong.js bỏ xaoLuaChon (G12a)", "js/tinhhuong.js",
                 lambda s: s.replace(
                     "const ds = window.MX_ENGINE.xaoLuaChon(q.luaChon, q.id);",
                     "const ds = q.luaChon;").replace(
                     "const viTriDapAn = ds.findIndex(x => x.id === q.dapAn);",
                     "const viTriDapAn = ds.findIndex(x => x.id === q.dapAn);"),
                 "G12a"))

    # CA 2 — G12b: chữ cái hiển thị quay về nhãn cố định
    kq.append(ca(2, "tinhhuong.js in chữ cái theo l.id (G12b)", "js/tinhhuong.js",
                 lambda s: s.replace(
                     'nut.textContent = window.MX_ENGINE.chuCai(i) + ". " + l.text;',
                     'nut.textContent = l.id.toUpperCase() + ". " + l.text;'),
                 "G12b"))

    # CA 3 (G12c) ĐÃ ĐƯỢC TÁCH SANG mut_g12c.py — và đây là một lỗi NEO thật, đáng ghi lại.
    #
    # Bản đầu của ca 3 nằm ở đây, với NEO `\{id:"b", text:"([^"]{40,})"\}` và comment khẳng định
    # "ở tinhhuong.js câu đầu, phương án đúng có id b". Khẳng định đó SAI. Đo lại bằng đúng phép
    # của cổng G12c thì câu được chọn có dapAn='d' (dài 63 ký tự) trong khi phương án dài nhất
    # là 'b' (dài 98) — tức 'b' là phương án NHIỄU. Nối dài 'b' thêm 600 ký tự không làm "đáp án
    # là phương án dài nhất" tăng, mà làm GIẢM ở câu đó. Cổng vẫn đỏ (rc=1) nhưng đỏ vì tiêu chí
    # khác, nên hàm ca() báo "KÊU NHƯNG SAI MÃ" và kết luận in ra "2/3 ... CỔNG IM".
    #
    # Đọc dòng kết luận đó dễ hiểu nhầm thành "G12c không có răng". Không phải. G12c có răng —
    # mut_g12c.py chứng minh bằng cách chọn đúng câu mà đáp án KHÔNG phải phương án dài nhất
    # rồi nối dài ĐÁP ÁN, đo nợ trước/sau (82.9% -> 85.7%, vượt mốc 83.9%), và cổng kêu đúng mã
    # `[LỖI] G12c`. Bài học: một ca mutation mà NEO phá sai thứ sẽ sinh ra hai lỗi cùng lúc —
    # cổng bị nghi oan, và người đọc tin vào kết luận sai. G12c đo một TỈ LỆ trên TOÀN NGÂN HÀNG,
    # nên ca phá nó phải chọn mẫu có chủ đích, không được neo vào "câu đầu tiên".
    #
    # Script này vì thế chỉ còn hai ca, đúng hai thứ mà G12a/G12b khai là đang canh: cơ chế xáo
    # vị trí và nhãn chữ cái hiển thị.

    print("\n" + "=" * 100)
    print(f"KẾT LUẬN: {sum(kq)}/{len(kq)} ca phá đều bị G12 bắt")
    for i, o in enumerate(kq, 1):
        print(f"  ca {i}: {'BẮT ĐƯỢC' if o else 'CỔNG IM — G12 không có răng cho ca đó'}")
    print("=" * 100)
    rc, ket, _ = chay_cong()
    print(f"XÁC NHẬN SAU CÙNG: rc={rc}  {ket}   (phải về ĐẠT: hai số bằng nhau)")
    shutil.rmtree(tmp)
    return 0 if (all(kq) and rc == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
