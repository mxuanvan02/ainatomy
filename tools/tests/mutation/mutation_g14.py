#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST cho cổng G14 (nhãn 5 loại lỗi phải khớp ở cả ba bản sao).

VÌ SAO PHẢI CHẠY: G14 vừa in ĐẠT 3/3, nhưng lần ĐẠT đó chưa chứng minh nó có răng — lần chạy
đầu tiên nó FAIL là do regex trích sai (bắt cả `unesco`, `loaiLoi`, 4 chủ đề Trạm 5 làm "loại
lỗi"), tức fail vì LÝ DO KHÁC, không phải vì nhãn lệch. Một cổng chưa từng fail vì đúng thứ nó
canh thì có thể đang in ĐẠT vô điều kiện — đúng lớp lỗi G11c từng mắc.

Bốn ca, mỗi ca phá ĐÚNG thứ một tiêu chí con tuyên bố đang canh:
  1 (G14b): đổi nhãn ở tools/gop_csv.py cho LỆCH với data/meta.js -> cổng phải kêu.
            Đây là ca thực tế nhất: chính là cách một bản sửa nhãn quên một trong ba nơi.
  2 (G14b): đổi nhãn ở js/nhamay_text.js cho lệch -> cổng phải kêu (bản sao thứ hai).
  3 (G14c): thêm một khoá lạ vào LOAI_LOI của gop_csv.py -> cổng phải kêu.
  4 (G14a): xoá hẳn một khoá khỏi data/meta.js -> cổng phải kêu, và phải kêu ở G14a
            (cổng tự nhận nó không trích đủ dữ liệu) chứ không được im lặng báo ĐẠT.

LƯU Ý KHI ĐỌC KẾT QUẢ: phá gop_csv.py hoặc meta.js cũng làm hash manifest lệch, nên G13b sẽ
kêu theo. Vì vậy mỗi ca phải kiểm ĐÚNG MÃ cổng của nó có trong output, không được chỉ nhìn
mã thoát — nếu không thì ca nào cũng "pass" nhờ một cổng khác kêu oan.

Khôi phục bằng bản sao BYTES trong /tmp, tuyệt đối không dùng `git checkout`: cây đang có thay
đổi chưa commit, git checkout sẽ trả về bản đã commit và XOÁ MẤT công sửa.
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
TOUCH = ["data/meta.js", "js/nhamay_text.js", "tools/gop_csv.py", "SHA256SUMS.txt"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong():
    r = subprocess.run(GATE, cwd=ROOT, capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr
    m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
    return r.returncode, (m.group(0) if m else "?"), out


def ca(so, ten, tep, sua, ma_cong):
    p = os.path.join(ROOT, tep)
    goc = open(p, encoding="utf-8").read()
    h0 = sha(p)
    try:
        moi = sua(goc)
        assert moi != goc, f"không phá được {tep} ({ten}) — NEO SAI, đọc mã thật trước đã"
        open(p, "w", encoding="utf-8").write(moi)
        rc, ket, out = chay_cong()
        keu = f"[LỖI] {ma_cong}" in out
        # rc != 0 là cần nhưng CHƯA ĐỦ: phải đúng mã cổng này kêu (xem chú thích đầu tệp)
        tt = ("BẮT ĐƯỢC" if keu else
              ("KÊU NHƯNG SAI MÃ" if rc != 0 else "IM (KHÔNG RĂNG)"))
        print(f"  [{so}] {ten:46s}: rc={rc} {ket:26s} {tt}")
        if tt != "BẮT ĐƯỢC":
            trich = [l for l in out.splitlines()
                     if "KẾT QUẢ" in l or "[LỖI]" in l or ma_cong in l]
            print(f"       !!! kỳ vọng {ma_cong} kêu. Trích:")
            for l in trich[:6]:
                print("       | " + l.strip()[:170])
        return tt == "BẮT ĐƯỢC"
    finally:
        open(p, "w", encoding="utf-8").write(goc)
        khop = sha(p) == h0
        print(f"       khôi phục {tep}: hash {'KHỚP gốc' if khop else 'LỆCH !!!'}")
        if not khop:
            print("       !!! DỪNG: tệp không về nguyên trạng.")
            sys.exit(9)


def sinh_manifest():
    """Sinh lại SHA256SUMS.txt để CA 0 bắt đầu từ nền XANH.

    VÌ SAO BẮT BUỘC: cổng G13b kiểm hash trong manifest khớp tệp trên đĩa. Mà chính tệp cổng
    (tools/nghiem_thu.py) cũng nằm trong manifest, nên MỖI lần sửa cổng là manifest cũ đi và
    G13b kêu — kể cả khi sản phẩm hoàn toàn lành. Lần chạy đầu và lần thứ hai của script này
    đều chết ở CA 0 vì đúng lý do đó, và cả hai lần đều dễ bị đọc nhầm thành "cổng hỏng".
    Sinh lại ở đây để CA 0 chỉ đỏ khi CÓ LỖI THẬT. In rõ đã làm gì, không làm âm thầm:
    một bước chuẩn bị giấu kín là cách nhanh nhất để biến baseline xanh thành xanh giả.
    """
    r = subprocess.run([sys.executable, "tools/sinh_manifest.py", "--ghi"],
                       cwd=ROOT, capture_output=True, text=True, timeout=300)
    dong = [l.strip() for l in r.stdout.splitlines() if "ĐÃ GHI" in l or "dòng" in l]
    print(f"  [chuẩn bị] sinh lại manifest (rc={r.returncode}): "
          + (dong[-1] if dong else r.stdout.strip()[:90]))
    # dọn tệp .bak mà sinh_manifest để lại trong repo, tránh nhiễu git status
    for f in glob.glob(os.path.join(ROOT, "SHA256SUMS.txt.bak-*")):
        os.replace(f, os.path.join(tempfile.gettempdir(), os.path.basename(f)))


def main():
    print("=" * 96)
    print("MUTATION TEST CỔNG G14 — nhãn loại lỗi khớp ở 3 bản sao")
    print("=" * 96)
    sinh_manifest()
    tmp = tempfile.mkdtemp(prefix="g14mut-")
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
    # CA 1 — G14b: gop_csv.py lệch với meta.js
    kq.append(ca(1, "gop_csv.py: 'Xúi'->'Làm lộ' (lệch meta.js)", "tools/gop_csv.py",
                 lambda s: s.replace('"lo_du_lieu_ca_nhan": "Xúi lộ dữ liệu cá nhân"',
                                     '"lo_du_lieu_ca_nhan": "Làm lộ dữ liệu cá nhân"'),
                 "G14b"))

    # CA 2 — G14b: nhamay_text.js lệch (bản sao thứ hai)
    kq.append(ca(2, "nhamay_text.js: 'Xúi'->'Rò rỉ' (lệch meta.js)", "js/nhamay_text.js",
                 lambda s: s.replace('ten: "Xúi lộ dữ liệu cá nhân"',
                                     'ten: "Rò rỉ dữ liệu cá nhân"'),
                 "G14b"))

    # CA 3 — G14c: khoá lạ trong gop_csv.py mà app không có
    kq.append(ca(3, "gop_csv.py: thêm khoá lạ 'loai_khong_co'", "tools/gop_csv.py",
                 lambda s: s.replace('"suy_luan_sai": "Suy luận sai",',
                                     '"suy_luan_sai": "Suy luận sai",\n'
                                     '    "loai_khong_co_trong_app": "Nhãn bịa ra",'),
                 "G14c"))

    # CA 4 — G14c: xoá khoá khỏi meta.js -> hai bên lệch tập khoá.
    # ĐỔI KỲ VỌNG TỪ G14a SANG G14c (07/10): bản đầu của cổng gộp "trích được không" với
    # "hai bên có khớp không" vào G14a nên ca này kêu ở G14a. Sau khi tách trách nhiệm,
    # G14a chỉ còn là phép kiểm sức khoẻ của chính cổng (cơ chế trích có chạy không), còn
    # lệch tập khoá là việc G14c. Expectation cũ không sai về sản phẩm, nó chỉ trỏ nhầm cổng
    # — và nếu cứ để vậy thì ca này sẽ "fail" mãi, che mất việc G14c thật sự có răng.
    def xoa_khoá_meta(s):
        # đổi tên khoá để regex định vị không thấy (giữ nguyên cấu trúc tệp cho hợp lệ JS)
        moi = s.replace("    lo_du_lieu_ca_nhan: {\n      /* \"Xúi\"",
                        "    lo_du_lieu_ca_nhan_BI_XOA: {\n      /* \"Xúi\"")
        if moi == s:
            # neo dự phòng: đổi trực tiếp dòng khoá
            moi = re.sub(r"^(\s*)lo_du_lieu_ca_nhan:\s*\{",
                         r"\1lo_du_lieu_ca_nhan_BI_XOA: {", s, count=1, flags=re.M)
        return moi
    kq.append(ca(4, "meta.js: mất khoá lo_du_lieu_ca_nhan", "data/meta.js",
                 xoa_khoá_meta, "G14c"))

    # CA 5 — chiều CÒN LẠI của G14c: thêm một loại lỗi vào data/meta.js mà gop_csv.py không khai.
    # VÌ SAO CA NÀY BẮT BUỘC CÓ: cho tới trước ca này, nhánh `thieu = set(khoa_meta) - set(gop)`
    # của G14c CHƯA TỪNG ĐƯỢC THỰC THI lần nào. Lý do: `meta` chỉ được xây từ
    # `for khoa in sorted(gop)`, nên tập khoá của nó luôn là tập con của gop và hiệu đó luôn
    # rỗng. Cổng vẫn in ĐẠT, tiêu chí vẫn mang tên tuyên bố kiểm cả hai chiều — nhưng một
    # chiều là code chết. Chỉ khi thiết kế ca phá cho đúng chiều đó mới lộ ra.
    def them_loai_vao_meta(s):
        neu = ('    loai_moi_chua_co_trong_gop: {\n'
               '      ten: "Loại lỗi mới thêm để thử cổng",\n'
               '      moTa: "Ca mutation số 5.",\n'
               '      mau: "#123456",\n'
               '      dauHieu: { buocPhaiCo: [], moTaBatBuoc: "", khongNenCo: [], moTaKhongNen: "" }\n'
               '    },\n')
        m = re.search(r"^(\s{2})loaiLoi:\s*\{\n", s, re.M)
        assert m, "neo sai: không thấy khối loaiLoi: { trong data/meta.js"
        return s[:m.end()] + neu + s[m.end():]
    kq.append(ca(5, "meta.js: thêm loại lỗi mà gop_csv.py không khai", "data/meta.js",
                 them_loai_vao_meta, "G14c"))

    print("\n" + "=" * 96)
    print(f"KẾT LUẬN: {sum(kq)}/{len(kq)} ca phá đều bị G14 bắt")
    for i, o in enumerate(kq, 1):
        print(f"  ca {i}: {'BẮT ĐƯỢC' if o else 'CỔNG IM — G14 không có răng cho ca đó'}")
    print("=" * 96)
    rc, ket, _ = chay_cong()
    print(f"XÁC NHẬN SAU CÙNG: rc={rc}  {ket}   (phải về ĐẠT)")
    shutil.rmtree(tmp)
    return 0 if (all(kq) and rc == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
