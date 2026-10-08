#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Đổi TÊN THƯƠNG HIỆU sản phẩm: "HỌC AI" -> "AInatomy" (08/10/2026, v1.2.0).

LÝ DO ĐỔI. Chủ sản phẩm phán: "HỌC AI" nghe thô, cần tên tiếng Anh có chơi chữ.
"AInatomy" = AI + Anatomy (giải phẫu) — đúng việc sản phẩm làm: mổ xẻ hệ AI ra
từng trạm để xem bên trong, trực quan hoá bằng 3D. Không giới hạn cấp học.

ĐỔI KÈM PHỤ ĐỀ (quyết định có ý thức, kèm sửa cổng G10b/G10f):
  "Phòng thực hành Trí tuệ nhân tạo cấp THPT" -> "Phòng thực hành Trí tuệ nhân tạo".
  Ranh giới dữ liệu KHÔNG đổi: bản đồ YCCĐ nhúng trong app vẫn là LỚP 10 (22 yêu
  cầu, verify 22/22). README giữ nguyên câu khai "Phạm vi dữ liệu đã kiểm chứng".
  Cổng G10f được NỚI thêm chiều mới: phụ đề cũ "…cấp THPT" phải HẾT ở 3 tệp
  thương hiệu — để lần đổi này cũng bị khoá, không ai thêm lại vô ý.

ĐÂY LÀ VIỆC NHIỀU BẢN SAO — làm theo Luật G (skill agentic-efficiency-loop), kế
thừa nguyên khuôn doi_ten_hoc_ai.py: thay THẾ TỪNG DÒNG có phân loại, KHÔNG
replace toàn cục, vì các nhóm sau BẮT BUỘC giữ nguyên:
1. BẢN GHI LỊCH SỬ đổi tên: README §8 (dòng v1.1.0 "SOI AI -> HỌC AI"), docstring
   + hằng của chính tools/doi_ten_hoc_ai.py, tools/doi_ten_soi_ai.py,
   tools/doi_dinh_danh_cap_thpt.py. Viết lại lịch sử là làm bản ghi nói dối.
2. TÊN GOOGLE SHEET quản lý dự án trong tools/tao_sheet_thietke.py: sheet THẬT
   trên Google đang mang tên "HỌC AI — Thiết kế tổng quan & Quản lý dự án v2";
   các tool đồng bộ sheet (dong_bo_sheet2.py, dien_sheet_bai_toan.py…) tìm sheet
   THEO TÊN. Đổi chuỗi trong script mà không đổi sheet thật là tạo lệch; đổi
   sheet thật là việc khác, có chủ đích riêng, không nằm trong lần đổi tên này.
3. KHOÁ DỮ LIỆU / TÊN HẰNG NỘI BỘ: soiai_dulieu_v1 (localStorage — đổi là XOÁ
   sạch dữ liệu học sinh, KHÔNG đảo ngược), __SOIAI_PHIEN, logo-soi, kb-logo-soi
   (tên class CSS).
4. duyet_nhan.html là TỆP SINH TỰ ĐỘNG từ tools/sinh_trang_duyet_nhan.py — không
   sửa tay; sửa hằng __TEN__ trong script sinh rồi sinh lại.

BẪY LOGO TÁCH CHỮ (đã trả giá ở lần đổi trước, xem TEN_MOI_LOGO):
index.html viết `HỌC <span>AI</span>` (span tô màu). Thay thô chuỗi liền sẽ cho
ra logo hiển thị sai. Logo mới: `AI<span>natomy</span>` — chữ "AI" đứng trước giữ
màu chữ thường, "natomy" mang màu nhấn, đọc vẫn ra "AInatomy".

CÁCH CHẠY (từ gốc repo):
    python3 tools/doi_ten_ainatomy.py           # chỉ đếm + phân loại, chưa ghi
    python3 tools/doi_ten_ainatomy.py --ghi     # ghi thật + verify hai chiều
"""
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEN_CU = "HỌC AI"
TEN_MOI = "AInatomy"
PHU_DE_CU = "Phòng thực hành Trí tuệ nhân tạo cấp THPT"
PHU_DE_MOI = "Phòng thực hành Trí tuệ nhân tạo"

EXT = (".js", ".html", ".css", ".md", ".json", ".txt", ".py")

# Tệp KHÔNG BAO GIỜ đổi — lý do từng tệp ở docstring đầu.
GIU_THEO_TEP = re.compile(
    r"^review\d*/|^\.hermes/|^moxe-ai/|^out/|/vendor/|^vendor/"
    r"|so_lieu_ho_so\.json$|^SHA256SUMS"
    r"|^tools/doi_ten_soi_ai\.py$|^tools/doi_dinh_danh_cap_thpt\.py$"
    r"|^tools/doi_ten_hoc_ai\.py$|^tools/doi_ten_ainatomy\.py$"
    # Test mutation của cổng G10f: hằng TEN_MOI trong đó là ĐẠN BẮN VÀO CỔNG, phải
    # sửa cùng nhịp với chính cổng G10f một cách có ý thức, không để script thay mù.
    r"|^tools/tests/mutation/mutation_g10f\.py$"
    # Sheet quản lý dự án THẬT trên Google đang mang tên cũ; các tool đồng bộ tìm
    # sheet theo tên. Đổi chuỗi trong script sinh mà không đổi sheet là tạo lệch.
    r"|^tools/tao_sheet_thietke\.py$"
    # Tệp sinh tự động — sửa script sinh rồi sinh lại, không sửa tay đầu ra.
    r"|^duyet_nhan\.html$")

# Khoá dữ liệu / tên hằng nội bộ: đổi là mất dữ liệu hoặc hỏng CSS.
GIU_KHOA = re.compile(r"soiai_|__SOIAI_|SOIAI_|SOI_AI_SITE|logo-soi|kb-logo-soi")

# Ngữ cảnh phải GIỮ nguyên văn dù nằm trong tệp được đổi: BẢN GHI LỊCH SỬ.
GIU_NGU_CANH = [
    (re.compile(r'SOI AI -> \*\*HỌC AI\*\*|đổi tên thương hiệu thành \*\*HỌC AI\*\*'),
     "README §8 bản ghi lịch sử lần đổi v1.1.0"),
    (re.compile(r"Phụ đề KHÔNG đổi"),
     "README §8 bản ghi lịch sử v1.1.0 — phụ đề ĐÃ đổi ở v1.2.0, viết mục mới thay vì sửa sử"),
    (re.compile(r'"Soi AI để hiểu AI"|khau = "Soi AI để hiểu AI"'),
     "cổng G10c — chuỗi trong DANH SÁCH CẤM"),
    (re.compile(r"MỔ XẺ AI"), "ghi chú LỊCH SỬ tên đời đầu"),
    (re.compile(r"chuỗi cấm biến thành \"Học AI để hiểu AI\""),
     "README — ví dụ lịch sử trong ghi chú cổng G10c"),
]

# Logo tách chữ: `HỌC <span>AI</span>` -> `AI<span>natomy</span>`.
# Phải chạy TRƯỚC phép thay chuỗi liền, và chữ thay cho dạng tách KHÁC chữ thay cho
# dạng liền — đúng cái bẫy đã đo được ở lần đổi SOI AI -> HỌC AI (logo thành
# "HỌC AI AI"). Verify chiều 4 của script này khoá kết quả.
RE_LOGO = re.compile(r"HỌC(\s*<span[^>]*>\s*)AI")

# Dòng h2 trang chủ chẻ phụ đề bằng span:
#   `Phòng thực hành <span class="logo-soi">Trí tuệ nhân tạo</span> cấp THPT`
# Thay chuỗi liền không bắt được " cấp THPT" nằm NGOÀI span. Phải có phép riêng,
# nếu không giao diện còn chữ "cấp THPT" mồ côi sau khi đổi phụ đề.
RE_H2 = re.compile(r'(<span class="logo-soi">Trí tuệ nhân tạo</span>) cấp THPT')

# Số chỗ kiểm kê bằng grep ngày 08/10 (xem commit). CHỐT CHẶN: dry-run ra số khác
# thì DỪNG — hoặc mã đã đổi, hoặc có chỗ mới phát sinh, cả hai đều phải nhìn.
# Phân loại: dry-run đầu 54 − 2 loại có chủ đích (README:242 bản ghi lịch sử;
# mutation_g10f.py đạn của cổng) = 52. CỘNG 2: bản --ghi đầu tiên bỏ qua hai dòng
# chứa class logo-soi/kb-logo-soi vì GIU_KHOA khoá cả dòng (index.html:63 h2 trang
# chủ và kichban.js:309 phụ đề kịch bản) — nay doi_dong không bỏ qua theo dòng nữa,
# cả hai được đổi đúng như RE_H2/phụ đề liền đã thiết kế. Tổng 54.
SO_CHO_KY_VONG = 54


def files():
    r = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, timeout=120)
    return [f for f in r.stdout.split("\n") if f and f.endswith(EXT)]


def doi_dong(ln):
    """Trả (dòng_mới, số_lần_đổi). Giữ nguyên nếu dòng thuộc nhóm lịch sử.

    GIU_KHOA KHÔNG còn là lý do bỏ qua CẢ DÒNG (lỗi đã đo: kichban.js:309 chứa cả
    khoá class `kb-logo-soi` lẫn phụ đề cần đổi, bỏ qua cả dòng làm phụ đề sót).
    Các phép thay bên dưới là thay chuỗi con "HỌC AI"/phụ đề — không chuỗi nào chứa
    hay chồng lấn token được bảo vệ (soiai_, __SOIAI_, logo-soi…), nên token an toàn
    mà không cần khoá dòng. Verify chiều 2 đếm lại soiai_dulieu_v1 để chốt.
    """
    for rx, _ in GIU_NGU_CANH:
        if rx.search(ln):
            return ln, 0
    n = 0
    moi = ln
    # 1) logo tách chữ trước (kẻo chuỗi liền ăn mất). Khoảng trắng trong group phải
    #    bị LOẠI: bản đầu giữ nguyên `\s*` nên logo ra `AI <span>natomy</span>` —
    #    HTML render khoảng trắng đó thành "AI natomy", sai thương hiệu.
    moi, k = RE_LOGO.subn(lambda m: "AI" + re.sub(r"\s+", "", m.group(1)) + "natomy", moi)
    n += k
    # 2) h2 phụ đề tách span
    moi, k = RE_H2.subn(r"\1", moi)
    n += k
    # 3) phụ đề liền
    k = moi.count(PHU_DE_CU)
    moi = moi.replace(PHU_DE_CU, PHU_DE_MOI)
    n += k
    # 4) tên thương hiệu liền
    k = moi.count(TEN_CU)
    moi = moi.replace(TEN_CU, TEN_MOI)
    n += k
    return moi, n


def quet(ghi):
    tong = 0
    for f in files():
        p = os.path.join(ROOT, f)
        if not os.path.isfile(p) or GIU_THEO_TEP.search(f):
            continue
        try:
            lines = io.open(p, encoding="utf-8").read().split("\n")
        except (OSError, UnicodeDecodeError):
            continue
        moi_lines, doi_file = [], 0
        for ln in lines:
            m, k = doi_dong(ln)
            moi_lines.append(m)
            doi_file += k
        if doi_file:
            tong += doi_file
            print(f"  [{f}]  {doi_file} chỗ")
            if ghi:
                io.open(p, "w", encoding="utf-8").write("\n".join(moi_lines))
    return tong


def verify():
    """Verify HAI CHIỀU sau khi ghi — tên mới có mặt + thứ phải giữ còn nguyên."""
    print("\n--- VERIFY SAU KHI GHI (hai chiều) ---")
    ok = True

    def doc(f):
        try:
            return io.open(os.path.join(ROOT, f), encoding="utf-8").read()
        except OSError:
            return ""

    # CHIỀU 1: không còn chỗ nào ĐỔI ĐƯỢC nữa (quét lại bằng chính doi_dong).
    con_doi = 0
    for f in files():
        p = os.path.join(ROOT, f)
        if not os.path.isfile(p) or GIU_THEO_TEP.search(f):
            continue
        for ln in doc(f).split("\n"):
            _, k = doi_dong(ln)
            con_doi += k
    tot = (con_doi == 0)
    ok &= tot
    print(f"  {'OK  ' if tot else '<<<'} tên/phụ đề cũ còn đổi được ở {con_doi} chỗ (phải 0)")

    # CHIỀU 2: thứ BẮT BUỘC giữ phải còn nguyên văn.
    giu = [
        ("js/engine.js", "soiai_dulieu_v1", 1, "khoá localStorage (không mất dữ liệu HS)"),
        ("README.md", "MỔ XẺ AI", 1, "lịch sử đổi tên đời đầu (baseline HEAD đếm lại = 1, "
                                      "kỳ vọng 2 chép từ verify của lần đổi v1.1.0 đã cũ)"),
        ("README.md", "SOI AI -> **HỌC AI**", 1, "bản ghi lịch sử v1.1.0"),
        ("tools/tao_sheet_thietke.py", "HỌC AI", 3, "tên sheet thật trên Google chưa đổi"),
        ("tools/nghiem_thu.py", '"Soi AI để hiểu AI"', 3, "cổng G10c còn cấm khẩu hiệu cũ"),
    ]
    for f, chuoi, ky_vong, mo_ta in giu:
        n = doc(f).count(chuoi)
        tot = (n == ky_vong)
        ok &= tot
        print(f"  {'OK  ' if tot else '<<<'} {f}: {chuoi!r} còn {n} lần (kỳ vọng {ky_vong}) — {mo_ta}")

    # CHIỀU 3: tên mới PHẢI có mặt ở nơi học sinh/giám khảo nhìn thấy.
    for f, chuoi in [("index.html", TEN_MOI), ("data/meta.js", f'ten: "{TEN_MOI}"'),
                     ("js/kichban.js", TEN_MOI)]:
        n = doc(f).count(chuoi)
        tot = (n > 0)
        ok &= tot
        print(f"  {'OK  ' if tot else '<<<'} {f}: {chuoi!r} xuất hiện {n} lần (phải >0)")

    # CHIỀU 4: logo tách chữ phải ra `AI<span>natomy</span>`, không được lặp chữ.
    idx = doc("index.html")
    logo_dung = bool(re.search(r'class="logo-txt">\s*AI<span[^>]*>natomy</span>', idx))
    logo_sai = bool(re.search(r"AInatomy\s*<span[^>]*>", idx))
    tot = logo_dung and not logo_sai
    ok &= tot
    print(f"  {'OK  ' if tot else '<<<'} index.html logo: 'AI<span>natomy</span>'={logo_dung}"
          f" · dạng lặp={logo_sai} (phải False)")

    # CHIỀU 5: phụ đề cũ "…cấp THPT" phải HẾT ở 3 tệp thương hiệu (G10b mới sẽ khoá).
    for f in ("index.html", "data/meta.js", "js/kichban.js"):
        n = doc(f).count("Trí tuệ nhân tạo cấp THPT")
        tot = (n == 0)
        ok &= tot
        print(f"  {'OK  ' if tot else '<<<'} {f}: phụ đề '…cấp THPT' còn {n} (phải 0)")
    return ok


def main():
    ghi = "--ghi" in sys.argv
    print(f"ĐỔI TÊN THƯƠNG HIỆU: {TEN_CU} -> {TEN_MOI}")
    print(f"ĐỔI PHỤ ĐỀ: {PHU_DE_CU!r} -> {PHU_DE_MOI!r}")
    print(f"CHẾ ĐỘ: {'GHI THẬT' if ghi else 'CHỈ KIỂM (thêm --ghi để ghi)'}")
    print(f"ROOT (suy từ __file__): {ROOT}\n" + "=" * 92)

    # HAI LƯỢT, thứ tự bắt buộc (bài học ghi trong doi_ten_hoc_ai.py): lượt 1 CHỈ
    # ĐẾM; khớp kỳ vọng mới sang lượt 2 ghi. Ghi xong mới kêu là thông báo nói dối.
    tong = quet(False)
    print("=" * 92)
    print(f"LƯỢT 1 (chỉ đếm): {tong} chỗ sẽ đổi (kỳ vọng {SO_CHO_KY_VONG})")
    if tong != SO_CHO_KY_VONG:
        print(f"\nDỪNG — lệch {tong - SO_CHO_KY_VONG:+d} chỗ so với kiểm kê. Mã đã đổi hoặc có")
        print("chỗ mới phát sinh: đọc lại phân loại GIU_* trước khi cập nhật kỳ vọng.")
        return 1
    if not ghi:
        print("(Chế độ CHỈ KIỂM — chưa ghi gì.)")
        return 0

    quet(True)
    ok = verify()
    print("\n" + "=" * 92)
    print("KẾT LUẬN:", "✅ ĐÃ GHI VÀ VERIFY HAI CHIỀU" if ok else "❌ VERIFY FAIL — xem <<< ở trên")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
