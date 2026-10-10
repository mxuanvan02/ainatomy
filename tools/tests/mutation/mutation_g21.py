#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST CỔNG G21 — sáu ca tính điểm (năm ca phá + một ca đối chứng âm).

VÌ SAO CÓ TỆP NÀY. G21 thêm ngày 09/10 sau một lượt rà soát khoa học tìm ra ba khoản nợ
của trạm đấu trường. Một cổng mới ĐẠT ngay lần chạy đầu CHƯA chứng minh nó thấy được gì:
repo này đã có tiền lệ cổng in ĐẠT trong khi mù (G14c một chiều là code chết, G10f chiều c
bị một câu tham chiếu làm rỗng). Nên mỗi chiều của G21 phải có một ca phá làm nó KÊU.

NĂM CA PHÁ — mỗi ca là một cách KHÁC NHAU để lỗi tái diễn mà cổng vẫn im nếu nó mù:

  CA 1 — engine.js ngừng đọc lựa chọn của học sinh (`const cc = traLoi.claimChon` -> `-1`)
         -> G21a PHẢI kêu. Đây chính là Finding 1 nguyên trạng: thao tác bấm claim được
         ghi, được tô sáng, nhưng không tới được điểm. Ca nguy hiểm nhất vì grep
         "claimChon" vẫn thấy chuỗi đó trong tệp — chỉ có gọi hàm thật mới lộ.
  CA 2 — mất cột `claim_dung` khỏi header CSV của engine.js -> G21a PHẢI kêu.
         (Việc ba bản khai cột phải khớp nhau là nhiệm vụ của G16, đã có mutation_g16.py;
         ca này chỉ kiểm chiều mà G21a tự cam kết: cột có thật trong header.)
  CA 3 — khoản nợ vị trí PHÌNH: kéo claimLoi của 2 câu LLM từ 2 về 1 -> G21b PHẢI kêu.
         Tính trước lúc viết ca này: 20/39 = 51,3% -> 22/39 = 56,4%, ngưỡng 53,3%.
  CA 4 — thêm một lời giải khoá vị trí ("Câu 2 ...") -> G21b PHẢI kêu.
         Ca này bắt chiều THỨ HAI của G21b mà ca 3 không đụng tới: 14 -> 15, mốc là 14.
  CA 5 — cue chữ-số mạnh thêm: đổi "12 kí tự" thành "mười hai kí tự" trong câu ĐÚNG duy
         nhất có chữ số -> G21c PHẢI kêu. Tính trước: chênh 42,3 -> 47,2 điểm %, ngưỡng 44,4.
  CA 6 — ĐỐI CHỨNG ÂM: repo nguyên trạng -> G21a/b/c đều IM (ĐẠT).

HAI CA PHÁ CÙNG CHIỀU (3 và 4) là cố ý. G21b đo hai đại lượng; một cổng gộp chúng thành
một phép "hoặc" sẽ ĐẠT khi chỉ một chiều hỏng. Tách hai ca thì chiều nào mù cũng lộ.

CÁCH PHÁ: sửa tệp có thật rồi khôi phục, xác nhận hash về đúng bản gốc trong finally —
một ca chết giữa đường mà để lại data/cauhoi_moRong.js hỏng thì app hỏng thật.
SỬA THEO KHỐI, không replace toàn tệp: chuỗi `"claimLoi": 2` xuất hiện 11 lần trong
cauhoi_moRong.js, replace toàn tệp sẽ đổi nhãn của 11 câu thay vì 1 và ca phá đo sai thứ.

CÁCH CHẠY:  python3 tools/tests/mutation/mutation_g21.py
"""
import hashlib
import os
import re
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CONG = os.path.join(REPO, "tools", "nghiem_thu.py")
ENGINE = os.path.join(REPO, "js", "engine.js")
CAUHOI = os.path.join(REPO, "data", "cauhoi.js")
MORONG = os.path.join(REPO, "data", "cauhoi_moRong.js")

# Chuỗi cần phá. ĐỌC TỪ TỆP THẬT lúc chạy và KIỂM DUY NHẤT trước khi phá — sai một ký tự
# là ca phá thành không-làm-gì rồi báo "cổng im đúng", tức tự chứng minh điều ngược lại.
CA1_CU = "const cc = traLoi.claimChon;"
CA1_MOI = "const cc = -1;"
CA2_CU = '"phai_lap","claim_dung"]];'
CA2_MOI = '"phai_lap"]];'
CA3_IDS = ("g1-01", "g1-03")          # 2 câu LLM đang có claimLoi = 2
CA3_CU, CA3_MOI = '"claimLoi": 2', '"claimLoi": 1'
CA4_CU = "đúng tinh thần Khung 2422."  # trong giaiThich của slb-03 (câu KHÔNG tham chiếu vị trí)
CA4_MOI = "Câu 2 vi phạm đúng tinh thần Khung 2422."
CA5_CU = "gồm ít nhất 12 kí tự"        # chữ số duy nhất trong claims của g2-14 (câu đúng có số)
CA5_MOI = "gồm ít nhất mười hai kí tự"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong(nhom="G21"):
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
            return ln.strip()[:230]
    return ""


def ranh_gioi_khoi(s, id_item):
    """(đầu, cuối) của khối item chứa id này. Hai tệp data khai id KHÁC kiểu nhau
    (cauhoi.js là object literal `id: "x"`, cauhoi_moRong.js là JSON `"id": "x"`),
    nên phải thử cả hai — chỉ thử một kiểu thì hàm im lặng trả None và ca phá bị bỏ qua."""
    for mau in ('"id": "%s"' % id_item, 'id: "%s"' % id_item):
        i = s.find(mau)
        if i >= 0:
            j = s.find('"id": "', i + len(mau))
            k = s.find('id: "', i + len(mau))
            nxt = min([x for x in (j, k) if x > 0] or [len(s)])
            return i, nxt
    return None


def sua_toan_tep(p, cu, moi):
    s = open(p, encoding="utf-8").read()
    if s.count(cu) != 1:
        return None
    return s.replace(cu, moi, 1)


def sua_trong_khoi_text(s, id_item, cu, moi):
    """Sửa MỘT chuỗi bên trong khối item chứa `id_item`, trả chuỗi mới (hoặc None).

    Phải theo khối vì hai tệp data có những chuỗi LẶP nhiều lần: `"claimLoi": 2` xuất hiện
    11 lần trong cauhoi_moRong.js, replace toàn tệp sẽ đổi nhãn của 11 câu thay vì 1 — ca phá
    khi đó đo một thứ khác với thứ nó khai, và có thể vừa phá vừa tự huỷ ngưỡng.
    Nhận CHUỖI chứ không nhận đường dẫn để ca 3 sửa hai khối liên tiếp trên cùng một bản.
    Trả None (thay vì nổ) khi khối không tìm thấy hoặc chuỗi không duy nhất trong khối, để
    ca phá bị BỎ QUA có ghi chú thay vì sửa nhầm chỗ rồi báo cổng im.
    """
    r = ranh_gioi_khoi(s, id_item)
    if r is None:
        return None
    dau, cuoi = r
    khoi = s[dau:cuoi]
    if khoi.count(cu) != 1:
        return None
    return s[:dau] + khoi.replace(cu, moi, 1) + s[cuoi:]


def ghi_file(p, s):
    open(p, "w", encoding="utf-8").write(s)


GOC = {p: sha(p) for p in (ENGINE, CAUHOI, MORONG)}
ket_luan = []


def ghi(ten, dat, dc=False):
    """`dc=True` = ĐỐI CHỨNG ÂM (kỳ vọng cổng IM). Hai số phải tách trong dòng KẾT LUẬN
    để dem_ca.py đếm được và để không khai quá (luật ghi trong dem_ca.py)."""
    ket_luan.append((ten, dat, dc))
    return dat


def khoi_phuc(danh_sach):
    for p, s in danh_sach:
        ghi_file(p, s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(p) == GOC[p] else "!!! LỆCH — SỬA TAY NGAY")


def kiem_anchor():
    """Xác nhận mọi chuỗi cần phá có thật và DUY NHẤT (trong tệp hoặc trong khối item).
    Thiếu bước này thì ca phá âm thầm thành không-làm-gì và script báo cổng có răng."""
    loi = []
    eng = open(ENGINE, encoding="utf-8").read()
    cq = open(CAUHOI, encoding="utf-8").read()
    mr = open(MORONG, encoding="utf-8").read()
    for ten, s, chuoi in (("engine.js", eng, CA1_CU), ("engine.js", eng, CA2_CU),
                          ("cauhoi.js", cq, CA4_CU), ("cauhoi_moRong.js", mr, CA5_CU)):
        if s.count(chuoi) != 1:
            loi.append(f"{ten}: {chuoi[:40]!r} xuất hiện {s.count(chuoi)} lần (cần đúng 1)")
    for id_item in CA3_IDS:
        r = ranh_gioi_khoi(mr, id_item)
        if r is None:
            loi.append(f"cauhoi_moRong.js: không thấy khối item {id_item}")
        elif mr[r[0]:r[1]].count(CA3_CU) != 1:
            loi.append(f"cauhoi_moRong.js/{id_item}: {CA3_CU!r} xuất hiện "
                       f"{mr[r[0]:r[1]].count(CA3_CU)} lần trong khối (cần đúng 1)")
    return loi


def main():
    loi = kiem_anchor()
    if loi:
        print("!!! không phá được, anchor đã đổi:")
        for l in loi:
            print("   ", l)
        print("    Mã đã đổi cấu trúc — cập nhật hằng ở đầu script này, đừng đoán chuỗi mới.")
        return 2

    # ============================== CA 0 — baseline ==============================
    print("=" * 100)
    print("CA 0 — baseline: repo nguyên trạng, G21a/b/c phải ĐẠT cả ba")
    rc, out = chay_cong()
    a, b, c = ket(out, "G21a"), ket(out, "G21b"), ket(out, "G21c")
    print(f"  rc={rc}  G21a={a}  G21b={b}  G21c={c}")
    if not (a == b == c == "ĐẠT"):
        print("  !!! baseline đã đỏ — mọi ca bên dưới vô nghĩa. Sửa cổng/mã trước.")
        return 1

    # ============================== CA 1 — phá G21a ==============================
    print("=" * 100)
    print("CA 1 — engine.js ngừng đọc claimChon của học sinh  -> G21a PHẢI kêu")
    print("       đây là Finding 1 nguyên trạng; grep vẫn thấy chuỗi claimChon nên chỉ")
    print("       gọi hàm thật mới lộ")
    goc = open(ENGINE, encoding="utf-8").read()
    moi = sua_toan_tep(ENGINE, CA1_CU, CA1_MOI)
    if moi is None:
        ghi("1 engine ngừng đọc claimChon -> G21a bắt", None)
    else:
        try:
            ghi_file(ENGINE, moi)
            rc, out = chay_cong()
            a = ket(out, "G21a")
            print(f"  rc={rc}  G21a={a}")
            if a == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G21a"))
            ghi("1 engine ngừng đọc claimChon -> G21a bắt", a == "LỖI")
        finally:
            khoi_phuc([(ENGINE, goc)])

    # ============================== CA 2 — phá G21a ==============================
    print("=" * 100)
    print("CA 2 — mất cột claim_dung khỏi header CSV  -> G21a PHẢI kêu")
    goc = open(ENGINE, encoding="utf-8").read()
    moi = sua_toan_tep(ENGINE, CA2_CU, CA2_MOI)
    if moi is None:
        ghi("2 mất cột claim_dung trong header -> G21a bắt", None)
    else:
        try:
            ghi_file(ENGINE, moi)
            rc, out = chay_cong()
            a = ket(out, "G21a")
            print(f"  rc={rc}  G21a={a}")
            if a == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G21a"))
            ghi("2 mất cột claim_dung trong header -> G21a bắt", a == "LỖI")
        finally:
            khoi_phuc([(ENGINE, goc)])

    # ============================== CA 3 — phá G21b (chiều vị trí) ==============
    print("=" * 100)
    print("CA 3 — kéo claimLoi của 2 câu LLM về vị trí giữa  -> G21b PHẢI kêu")
    print("       tính trước: 20/39 = 51,3% -> 22/39 = 56,4%, ngưỡng 53,3%")
    goc = open(MORONG, encoding="utf-8").read()
    moi = goc
    for id_item in CA3_IDS:
        tmp = sua_trong_khoi_text(moi, id_item, CA3_CU, CA3_MOI)
        if tmp is None:
            print(f"  !!! không sửa được khối {id_item}")
            moi = None
            break
        moi = tmp
    if moi is None:
        ghi("3 nợ vị trí phình -> G21b bắt", None)
    else:
        try:
            ghi_file(MORONG, moi)
            rc, out = chay_cong()
            b = ket(out, "G21b")
            print(f"  rc={rc}  G21b={b}")
            if b == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G21b"))
            ghi("3 nợ vị trí phình -> G21b bắt", b == "LỖI")
        finally:
            khoi_phuc([(MORONG, goc)])

    # ============================== CA 4 — phá G21b (chiều lời giải) =============
    print("=" * 100)
    print("CA 4 — thêm một lời giải khoá vị trí ('Câu 2 ...')  -> G21b PHẢI kêu")
    print("       chiều THỨ HAI của G21b: 14 -> 15 lời giải, mốc là 14. Ca 3 không đụng chiều này")
    goc = open(CAUHOI, encoding="utf-8").read()
    moi = sua_toan_tep(CAUHOI, CA4_CU, CA4_MOI)
    if moi is None:
        ghi("4 thêm lời giải khoá vị trí -> G21b bắt", None)
    else:
        try:
            ghi_file(CAUHOI, moi)
            rc, out = chay_cong()
            b = ket(out, "G21b")
            print(f"  rc={rc}  G21b={b}")
            if b == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G21b"))
            ghi("4 thêm lời giải khoá vị trí -> G21b bắt", b == "LỖI")
        finally:
            khoi_phuc([(CAUHOI, goc)])

    # ============================== CA 5 — phá G21c ==============================
    print("=" * 100)
    print("CA 5 — bỏ chữ số khỏi câu ĐÚNG duy nhất có số  -> G21c PHẢI kêu")
    print("       tính trước: chênh 42,3 -> 47,2 điểm %, ngưỡng 44,4")
    goc = open(MORONG, encoding="utf-8").read()
    moi = sua_trong_khoi_text(goc, "g2-14", CA5_CU, CA5_MOI)
    if moi is None:
        ghi("5 cue chữ-số mạnh thêm -> G21c bắt", None)
    else:
        try:
            ghi_file(MORONG, moi)
            rc, out = chay_cong()
            c = ket(out, "G21c")
            print(f"  rc={rc}  G21c={c}")
            if c == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G21c"))
            ghi("5 cue chữ-số mạnh thêm -> G21c bắt", c == "LỖI")
        finally:
            khoi_phuc([(MORONG, goc)])

    # ============================== CA 6 — đối chứng âm ==========================
    print("=" * 100)
    print("CA 6 — ĐỐI CHỨNG ÂM: repo nguyên trạng thì G21a/b/c PHẢI IM (ĐẠT)")
    rc, out = chay_cong()
    a, b, c = ket(out, "G21a"), ket(out, "G21b"), ket(out, "G21c")
    print(f"  rc={rc}  G21a={a}  G21b={b}  G21c={c}")
    ghi("6 repo nguyên trạng -> G21 im cả ba (đối chứng âm)", a == b == c == "ĐẠT", dc=True)

    # ============================== TỔNG KẾT ====================================
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
