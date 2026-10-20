#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST CỔNG G21d + G23 — sáu ca (năm ca phá + một ca đối chứng âm).

VÌ SAO CÓ TỆP NÀY. Ngày 20/10 thêm bốn phép kiểm mới: G21d (nợ cue "claim dài nhất" ở đấu
trường, đóng Finding F1) và G23a/b/c (chữ học sinh đọc phải khớp thuật toán chọn câu, đóng
Finding F3). Cả bốn đều ĐẠT ngay lần chạy đầu — và repo này đã có tiền lệ cổng in ĐẠT trong khi
mù (G14c một chiều là code chết; G10f chiều c bị một câu tham chiếu làm rỗng; G12c mù 12 ngày vì
mốc phần trăm thuộc một phạm vi câu đã không còn tồn tại). Tệ hơn: `ho-so/noi_dung_trinh_chieu_15_trang.md`
khai "63 ca ... tức mỗi cổng được chứng minh là CÓ bắt được lỗi" và số đó đi thẳng vào PDF nộp
giám khảo. Thêm cổng mà không thêm ca phá thì câu khai đó thành lời khai sai.

NĂM CA PHÁ — mỗi ca nhắm một cơ chế KHÁC NHAU của cổng mới:

  CA 1 — G21d PHÌNH: kéo claimLoi của g1-01 từ 2 về 0 (chính là index của claim dài nhất)
         -> 42/53 = 79,2% thành 43/53 = 81,1%, vượt mốc 79,2 + dung sai 1,0 = 80,2.
         Đây là Finding F1 nguyên trạng: nợ nội dung lớn thêm mà không ai đo.
  CA 2 — G21d ĐO MÙ: đẩy claimLoi của g1-07 ra ngoài phạm vi claims (0 -> 9 với 3 claims)
         -> nMu = 1, cổng phải FAIL-CLOSED "PHÉP ĐO MÙ" thay vì in tỉ lệ từ phép đo thiếu.
         Ca này quan trọng nhất về mặt thiết kế: nó chứng minh cổng thà đỏ còn hơn xanh trên
         một phép đo sai — đúng bài học G12c và bài học `bang_gia_tri_kien_tao_v3.py`.
  CA 3 — G21d ĐỔI PHẠM VI: đổi loai của slb-01 từ co_loi thành dung -> 53 câu có lỗi thành 52.
         Mốc 79,2% được ghi cho 52... đúng hơn là cho 53 câu, nên hai số không so sánh được và
         cổng phải kêu "PHẠM VI ĐÃ ĐỔI". Bắt chiều CHỐT PHẠM VI mà ca 1 không đụng tới: một
         cổng chỉ so phần trăm sẽ im lặng so mốc của tập này với phép đo của tập khác.
  CA 4 — G23b SAI SỐ HỌC: sửa câu chữ trong index.html thành "9 câu có lỗi ... + 4 câu đúng"
         -> 9 + 4 = 13 ≠ 12 và 9 ≠ 8 của mã. Đây chính xác là Finding F3 tái diễn
         ("2 câu cho mỗi loại lỗi" với 5 loại = 14 ≠ 12). Sửa CÙNG DÒNG, không thêm dòng, để
         soDongCode không đổi (bộ đếm chỉ đếm .js/.html/.css theo dòng).
  CA 5 — G23a MẤT NEO: viết lại `while(pick.length < 8){` thành `for(;pick.length < 8;){`
         (hành vi y hệt, chỉ khác kiểu viết) -> regex của G23a trật, cổng phải báo "PHÉP ĐO MÙ"
         và DỪNG, không được in tiếp G23b/G23c xanh trên một phép đo rỗng. Ca này chứng minh
         cổng fail-closed bắt được lỗi của CHÍNH NGƯỜI VIẾT CỔNG: bản đầu của G23 gọi
         `html_song("index.html")` (truyền đường dẫn thay vì nội dung) và G23a đã kêu đúng thiết
         kế. Chú ý ca phá KHÔNG được là "bỏ một khoảng trắng" — regex có `\s*` nên khoảng trắng
         không phải là neo, phá kiểu đó là ca không-làm-gì (xem ghi chú ở CA5_MOI).

  CA 6 — ĐỐI CHỨNG ÂM: repo nguyên trạng -> G21d và G23a/b/c đều IM (ĐẠT).

CÁCH PHÁ: sửa tệp có thật rồi khôi phục, xác nhận hash về đúng bản gốc trong finally — một ca
chết giữa đường mà để lại data/cauhoi_moRong.js hỏng thì app hỏng thật.
SỬA THEO KHỐI, không replace toàn tệp: `loai: "co_loi"` xuất hiện 15 lần trong data/cauhoi.js
và `"claimLoi": 0` xuất hiện 8 lần trong data/cauhoi_moRong.js (đo bằng lệnh, không đoán), nên
replace toàn tệp sẽ đổi nhãn của cả chục câu và ca phá đo một thứ khác với thứ nó khai.

CÁCH CHẠY:  cd soi-ai && python3 tools/tests/mutation/mutation_g21d_g23.py
"""
import hashlib
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CONG = os.path.join(REPO, "tools", "nghiem_thu.py")
MORONG = os.path.join(REPO, "data", "cauhoi_moRong.js")
CAUHOI = os.path.join(REPO, "data", "cauhoi.js")
APP = os.path.join(REPO, "js", "app.js")
INDEX = os.path.join(REPO, "index.html")

# ---- anchor: MỌI chuỗi dưới đây được ĐO bằng lệnh trước khi viết, không gõ từ trí nhớ ----
# CA1: g1-01 có claimLoi=2, claims=[205,186,182] ký tự -> index dài nhất là 0.
CA1_ID = "g1-01"
CA1_CU, CA1_MOI = '"claimLoi": 2', '"claimLoi": 0'
# CA2: g1-07 có claimLoi=0 và 3 claims -> đẩy ra 9 là ngoài phạm vi.
CA2_ID = "g1-07"
CA2_CU, CA2_MOI = '"claimLoi": 0', '"claimLoi": 9'
# CA3: slb-01 là câu co_loi nằm trong data/cauhoi.js (kiểu object literal, không có dấu nháy ở key)
CA3_ID = "slb-01"
CA3_CU, CA3_MOI = 'loai: "co_loi"', 'loai: "dung"'
# CA4: câu chữ học sinh đọc — 1 lần duy nhất trong index.html (đã đo)
CA4_CU = "Mỗi phiên 12 câu — 8 câu có lỗi (mỗi loại ít nhất 1 câu) + 4 câu đúng"
CA4_MOI = "Mỗi phiên 12 câu — 9 câu có lỗi (mỗi loại ít nhất 1 câu) + 4 câu đúng"
# CA5: viết lại vòng lặp THEO KIỂU KHÁC, hành vi không đổi.
# LỖI THẬT ĐÃ MẮC ở bản đầu: CA5_CU là "while(pick.length < 8)" và CA5_MOI bỏ đi một khoảng
# trắng. Regex của G23a là `while\s*\(\s*pick\.length\s*<\s*(\d+)\s*\)` — có \s* nên bỏ khoảng
# trắng vẫn khớp, cổng vẫn ĐẠT và ca phá hoá ra KHÔNG LÀM GÌ (script in "SAI KỲ VỌNG", tức tự
# chứng minh điều ngược lại với điều nó khai). Đây đúng là loại lỗi mà docstring của
# mutation_g21.py:54-60 ghi là đã từng mắc. Ca phá phải mô phỏng tình huống THẬT mà G23a sinh
# ra để bắt: ai đó viết lại hằng số theo kiểu khác (`for(;...;)`) khiến regex trật.
CA5_CU, CA5_MOI = "while(pick.length < 8){", "for(;pick.length < 8;){"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong(nhom):
    r = subprocess.run([sys.executable, CONG, nhom], cwd=REPO,
                       capture_output=True, text=True, timeout=400)
    return r.returncode, r.stdout + r.stderr


def ket(out, ma):
    for ln in out.splitlines():
        if f" {ma} " in ln:
            return "ĐẠT" if "[ĐẠT ]" in ln else ("LỖI" if "[LỖI]" in ln else "?")
    return "KHONG_THAY"


def bang_chung(out, ma):
    """Trả về NGUYÊN VĂN dòng lỗi, KHÔNG cắt.

    LỖI THẬT ĐÃ MẮC ở bản đầu: hàm này cắt 230 ký tự cho gọn khi in, nhưng CA3 lại dùng chính
    chuỗi đã cắt để assert `"PHẠM VI" in bc`. Cổng G21d in lý do phạm vi ở CUỐI một đoạn giải
    thích dài ~900 ký tự, nên assertion không bao giờ thấy chữ đó và báo "SAI KỲ VỌNG" trong
    khi cổng kêu đúng. Bài học: cắt chuỗi để ĐỌC thì được, cắt chuỗi để SO thì không — muốn so
    gì phải so trên nguyên văn. In ra vẫn cắt (hien()) để log không nổ.
    (Lỗi này chính mutation test mới phát hiện ở lượt chạy đầu của nó: 4/6 ca, trong đó CA3
    "SAI KỲ VỌNG" là do helper cắt chuỗi, còn CA5 là ca phá không-làm-gì.)
    """
    for ln in out.splitlines():
        if f"[LỖI] {ma} " in ln:
            return ln.strip()
    return ""


def hien(s, n=230):
    return s if len(s) <= n else s[:n] + " …(cắt để đọc)"


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


def sua_trong_khoi(p, id_item, cu, moi):
    """Sửa MỘT chuỗi bên trong khối item chứa `id_item`. Trả None (không nổ) khi khối không
    tìm thấy hoặc chuỗi không duy nhất trong khối, để ca phá bị BỎ QUA có ghi chú thay vì
    sửa nhầm chỗ rồi báo "cổng im đúng" — tức tự chứng minh điều ngược lại."""
    s = open(p, encoding="utf-8").read()
    r = ranh_gioi_khoi(s, id_item)
    if r is None:
        return None
    dau, cuoi = r
    khoi = s[dau:cuoi]
    if khoi.count(cu) != 1:
        return None
    open(p, "w", encoding="utf-8").write(s[:dau] + khoi.replace(cu, moi, 1) + s[cuoi:])
    return True


def sua_toan_tep(p, cu, moi):
    s = open(p, encoding="utf-8").read()
    if s.count(cu) != 1:
        return None
    open(p, "w", encoding="utf-8").write(s.replace(cu, moi, 1))
    return True


GOC = {p: sha(p) for p in (MORONG, CAUHOI, APP, INDEX)}
ket_luan = []


def ghi(ten, dat, dc=False):
    """`dc=True` = ĐỐI CHỨNG ÂM (kỳ vọng cổng IM). Hai số phải tách trong dòng KẾT LUẬN để
    dem_ca.py đếm được và để không khai quá (luật ghi trong dem_ca.py)."""
    ket_luan.append((ten, dat, dc))
    return dat


def khoi_phuc(danh_sach):
    for p, s in danh_sach:
        open(p, "w", encoding="utf-8").write(s)
        print("  khôi phục:", "hash KHỚP gốc" if sha(p) == GOC[p] else "!!! LỆCH — SỬA TAY NGAY")


def kiem_anchor():
    """Xác nhận mọi chuỗi cần phá có thật và DUY NHẤT. Thiếu bước này thì ca phá âm thầm thành
    không-làm-gì và script báo cổng có răng trong khi nó chưa bị thử."""
    loi = []
    mr = open(MORONG, encoding="utf-8").read()
    cq = open(CAUHOI, encoding="utf-8").read()
    ap = open(APP, encoding="utf-8").read()
    ix = open(INDEX, encoding="utf-8").read()
    for ten, s, id_item, chu in [("cauhoi_moRong", mr, CA1_ID, CA1_CU),
                                 ("cauhoi_moRong", mr, CA2_ID, CA2_CU),
                                 ("cauhoi", cq, CA3_ID, CA3_CU)]:
        r = ranh_gioi_khoi(s, id_item)
        if r is None:
            loi.append("%s: không thấy khối id %s" % (ten, id_item))
        elif s[r[0]:r[1]].count(chu) != 1:
            loi.append("%s: %r không duy nhất trong khối %s" % (ten, chu, id_item))
    if ap.count(CA5_CU) != 1:
        loi.append("app.js: %r xuất hiện %d lần (mong 1)" % (CA5_CU, ap.count(CA5_CU)))
    if ix.count(CA4_CU) != 1:
        loi.append("index.html: câu chữ xuất hiện %d lần (mong 1)" % ix.count(CA4_CU))
    return loi


def main():
    print("=" * 100)
    print("MUTATION TEST G21d + G23 — cổng thêm 20/10 (đóng Finding F1 và F3)")
    print("=" * 100)
    loi_anchor = kiem_anchor()
    if loi_anchor:
        print("ABORT — anchor không hợp lệ, KHÔNG phá gì cả:")
        for l in loi_anchor:
            print("  ✗", l)
        print("\nKẾT LUẬN: 0/0 ca (anchor hỏng)")
        return 2
    print("  ✓ anchor kiểm OK: 3 chuỗi theo khối duy nhất + 2 chuỗi toàn tệp duy nhất\n")

    # ============================== CA 1 — G21d phình ==============================
    print("=" * 100)
    print("CA 1 — nợ cue 'claim dài nhất' PHÌNH (42/53 -> 43/53 = 81,1%, mốc 79,2 + 1,0)")
    goc = open(MORONG, encoding="utf-8").read()
    try:
        if sua_trong_khoi(MORONG, CA1_ID, CA1_CU, CA1_MOI):
            rc, out = chay_cong("G21")
            d = ket(out, "G21d")
            print("  rc=%d  G21d=%s" % (rc, d))
            if d == "LỖI":
                print("  bằng chứng:", bang_chung(out, "G21d"))
            ghi("1 nợ claim-dài-nhất phình -> G21d bắt", d == "LỖI")
        else:
            ghi("1 nợ claim-dài-nhất phình -> G21d bắt", None)
            print("  BỎ QUA: không sửa được khối", CA1_ID)
    finally:
        khoi_phuc([(MORONG, goc)])

    # ============================== CA 2 — G21d đo mù ==============================
    print("=" * 100)
    print("CA 2 — G21d ĐO MÙ: claimLoi của g1-07 ra ngoài phạm vi claims -> FAIL-CLOSED")
    goc = open(MORONG, encoding="utf-8").read()
    try:
        if sua_trong_khoi(MORONG, CA2_ID, CA2_CU, CA2_MOI):
            rc, out = chay_cong("G21")
            d = ket(out, "G21d")
            print("  rc=%d  G21d=%s" % (rc, d))
            bc = bang_chung(out, "G21d")
            if bc:
                print("  bằng chứng:", hien(bc))
            # phải kêu ĐÚNG lý do "đo mù", không phải kêu vì phình — hai lý do đó khác nhau
            ghi("2 phép đo mù -> G21d FAIL-CLOSED đúng lý do",
                d == "LỖI" and "MÙ" in bc)
        else:
            ghi("2 phép đo mù -> G21d FAIL-CLOSED đúng lý do", None)
            print("  BỎ QUA: không sửa được khối", CA2_ID)
    finally:
        khoi_phuc([(MORONG, goc)])

    # ============================== CA 3 — G21d đổi phạm vi ==============================
    print("=" * 100)
    print("CA 3 — G21d ĐỔI PHẠM VI: 53 câu có lỗi thành 52 -> mốc % cũ vô nghĩa, phải kêu")
    goc = open(CAUHOI, encoding="utf-8").read()
    try:
        if sua_trong_khoi(CAUHOI, CA3_ID, CA3_CU, CA3_MOI):
            rc, out = chay_cong("G21")
            d = ket(out, "G21d")
            bc = bang_chung(out, "G21d")
            print("  rc=%d  G21d=%s" % (rc, d))
            if bc:
                print("  bằng chứng:", hien(bc))
            ghi("3 phạm vi đổi -> G21d bắt đúng lý do PHẠM VI",
                d == "LỖI" and "PHẠM VI" in bc)
        else:
            ghi("3 phạm vi đổi -> G21d bắt đúng lý do PHẠM VI", None)
            print("  BỎ QUA: không sửa được khối", CA3_ID)
    finally:
        khoi_phuc([(CAUHOI, goc)])

    # ============================== CA 4 — G23b sai số học ==============================
    print("=" * 100)
    print("CA 4 — G23b SAI SỐ HỌC: chữ thành '9 câu có lỗi + 4 câu đúng' (9+4=13 ≠ 12)")
    goc = open(INDEX, encoding="utf-8").read()
    try:
        if sua_toan_tep(INDEX, CA4_CU, CA4_MOI):
            rc, out = chay_cong("G23")
            b = ket(out, "G23b")
            print("  rc=%d  G23b=%s" % (rc, b))
            bc = bang_chung(out, "G23b")
            if bc:
                print("  bằng chứng:", hien(bc))
            # G23a phải VẪN ĐẠT: regex câu chữ có nhóm (\\d+) nên vẫn parse được "9 câu có lỗi".
            # Nếu G23a cũng đỏ thì phép đo mù che mất lỗi số học — hai cổng này phải tách vai.
            ghi("4 chữ sai số học -> G23b bắt (G23a vẫn đạt)",
                b == "LỖI" and ket(out, "G23a") == "ĐẠT")
        else:
            ghi("4 chữ sai số học -> G23b bắt (G23a vẫn đạt)", None)
            print("  BỎ QUA: anchor index.html không duy nhất")
    finally:
        khoi_phuc([(INDEX, goc)])

    # ============================== CA 5 — G23a mất neo ==============================
    print("=" * 100)
    print("CA 5 — G23a MẤT NEO: bỏ khoảng trắng trong `while(pick.length < 8)` -> regex trật")
    goc = open(APP, encoding="utf-8").read()
    try:
        if sua_toan_tep(APP, CA5_CU, CA5_MOI):
            rc, out = chay_cong("G23")
            a = ket(out, "G23a")
            bc = bang_chung(out, "G23a")
            print("  rc=%d  G23a=%s" % (rc, a))
            if bc:
                print("  bằng chứng:", hien(bc))
            # G23a phải KÊU và DỪNG: khi phép đo mù thì không được in tiếp G23b/G23c xanh.
            ghi("5 regex trật -> G23a kêu và dừng, không in tiếp b/c",
                a == "LỖI" and ket(out, "G23b") == "KHONG_THAY")
        else:
            ghi("5 regex trật -> G23a kêu và dừng, không in tiếp b/c", None)
            print("  BỎ QUA: anchor app.js không duy nhất")
    finally:
        khoi_phuc([(APP, goc)])

    # ============================== CA 6 — đối chứng âm ==============================
    print("=" * 100)
    print("CA 6 — ĐỐI CHỨNG ÂM: repo nguyên trạng thì G21d và G23a/b/c PHẢI IM (ĐẠT)")
    rc, out = chay_cong("G21")
    d = ket(out, "G21d")
    rc3, out3 = chay_cong("G23")
    a, b, c = ket(out3, "G23a"), ket(out3, "G23b"), ket(out3, "G23c")
    print("  G21d=%s  G23a=%s G23b=%s G23c=%s" % (d, a, b, c))
    ghi("6 repo nguyên trạng -> bốn phép kiểm im (đối chứng âm)",
        d == a == b == c == "ĐẠT", dc=True)

    # ============================== TỔNG KẾT ====================================
    print("=" * 100)
    con_sot = any(sha(p) != h for p, h in GOC.items())
    print("[XÁC NHẬN] tệp nào chưa khôi phục đúng:", con_sot, "(phải False)")
    rc2, _ = chay_cong("G21")
    rc4, _ = chay_cong("G23")
    ran = [(t, o, dc) for t, o, dc in ket_luan if o is not None]
    so = sum(1 for _, o, _ in ran if o)
    so_pha = sum(1 for _, o, dc in ran if o and not dc)
    so_dc = sum(1 for _, o, dc in ran if o and dc)
    # Khuôn A của dem_ca.py — hai số PHẢI tách, gộp lại là khai quá.
    print("\nKẾT LUẬN: %d/%d ca đúng như kỳ vọng (%d ca PHÁ bị cổng bắt"
          " + %d ca ĐỐI CHỨNG ÂM cổng im đúng)" % (so, len(ran), so_pha, so_dc))
    for ten, o, dc in ket_luan:
        if o is None:
            print("  %s: BỎ QUA" % ten)
            continue
        nhan = ("KHÔNG BẮT OAN (đúng)" if o else "BẮT OAN — cổng hỏng") if dc \
            else ("ĐÚNG" if o else "SAI KỲ VỌNG")
        print("  %s: %s" % (ten, nhan))
    print("=" * 100)
    return 0 if (so == len(ran) and not con_sot and rc2 == 0 and rc4 == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
