#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Đổi TÊN THƯƠNG HIỆU sản phẩm: "SOI AI" -> "HỌC AI" (08/10/2026).

LÝ DO ĐỔI. Chủ sản phẩm (giáo viên Tin học THPT) phán: hệ thống này là để HỌC VỀ AI, không chỉ
"soi AI". "Soi" chỉ còn là phương pháp của MỘT tầng (Đấu trường bắt lỗi); sản phẩm thật gồm 5 phân
hệ — Xưởng huấn luyện, Đấu trường, Nhà máy AI 7 trạm, Lôgic & AI, Bản đồ năng lực. Tên "SOI AI"
hẹp hơn nội dung thật. Tên mới "HỌC AI" nói thẳng mục đích. Phụ đề GIỮ NGUYÊN: "Phòng thực hành
Trí tuệ nhân tạo cấp THPT" (cổng G10b khoá phụ đề này ở 3 nơi, không khoá tên thương hiệu).

ĐÂY LÀ VIỆC NHIỀU BẢN SAO — làm theo Luật G (skill agentic-efficiency-loop). Đã kiểm kê bằng
grep toàn repo trước khi viết script này: 56 chỗ ĐỔI, 11 chỗ GIỮ. Script thay THẾ TỪNG DÒNG có
phân loại, KHÔNG replace("SOI AI", ...) toàn cục — vì ba nhóm sau đây BẮT BUỘC giữ nguyên:

1. KHOÁ DỮ LIỆU / TÊN TỆP CSV: `soiai_dulieu_v1` (localStorage), `soiai_nhatky_*.csv`,
   `__SOIAI_PHIEN`. Đổi khoá localStorage = XOÁ SẠCH dữ liệu học sinh đang lưu trong trình duyệt.
   KHÔNG đảo ngược. Giữ nguyên.
2. ĐỘNG TỪ "soi" tiếng Việt mô tả đúng cơ chế: "soi mô hình", "soi ra chỗ hỏng", "đáng soi"
   (25 lần). Đây là văn xuôi nội dung, không phải tên. Thay thô là phá bài học.
3. ĐƯỜNG DẪN / TÊN REPO / URL: `soi-ai`, `soi-ai-lop10` (172 lần). GitHub Pages KHÔNG redirect;
   link cũ đã nằm trong hồ sơ nộp (tiền lệ: github.io/soi-ai/ -> 404). GIỮ tới sau hạn nộp 25/10.

MỘT CÁI BẪY NỮA, nguy hiểm vì nó im lặng: cổng G10c có DANH SÁCH TỪ CẤM chứa đúng chuỗi
"Soi AI để hiểu AI" (khẩu hiệu tiếp thị cũ). Nếu replace chạm vào danh sách đó thì chuỗi cấm biến
thành "Học AI để hiểu AI" và CỔNG THÔI CẤM khẩu hiệu cũ mà vẫn in ĐẠT — vô hiệu hoá một tiêu chí
mà không ai biết. Nên mọi chỗ khớp ngữ cảnh "danh sách cấm G10c" đều GIỮ NGUYÊN VĂN.

GHI CHÚ LỊCH SỬ cũng giữ: README §8 ("đổi tên thành SOI AI"), tools/doi_ten_soi_ai.py (bản ghi
lần đổi trước), tools/gop_csv.py:11. Viết đè là làm sai lịch sử quyết định.

CÁCH CHẠY:
    python3 tools/doi_ten_hoc_ai.py            # chỉ kiểm, in từng chỗ sẽ đổi, chưa ghi
    python3 tools/doi_ten_hoc_ai.py --ghi      # ghi thật, kèm verify hai chiều
Chốt chặn: tổng số chỗ đổi phải ĐÚNG bằng số kiểm kê; lệch là DỪNG và không ghi gì.
"""
import io
import os
import re
import subprocess
import sys

# Gốc repo suy từ vị trí tệp (G18a/G18b canh điều này): <repo>/tools/x.py -> hai lần dirname.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEN_CU_HOA = "SOI AI"
TEN_MOI_HOA = "HỌC AI"
TEN_CU_Hoa = "Soi AI"
TEN_MOI_Hoa = "Học AI"

# Số chỗ kiểm kê được ngày 08/10. Đây là CHỐT CHẶN: nếu một lần chạy sau cho ra số khác thì
# hoặc mã đã đổi, hoặc có chỗ mới phát sinh — cả hai đều phải dừng lại nhìn, không ghi đè im
# lặng (đúng nguyên tắc của doi_dinh_danh_cap_thpt.py).
#
# CON SỐ NÀY ĐÃ SỬA MỘT LẦN, và lý do đáng ghi hơn chính con số. Kiểm kê đầu ra 56 và dry-run
# cũng ra 56 → chốt chặn "khớp", trông như đã kiểm xong. Nhưng đọc ngữ cảnh 4 tệp đáng ngờ thì
# 8 chỗ trong số đó là BẢN GHI LỊCH SỬ (bảng RULES của lần đổi định danh trước, hai dòng quyết
# định trong sheet quản lý dự án), không phải thương hiệu. Tức CHỐT CHẶN THEO SỐ LƯỢNG KHÔNG KIỂM
# PHÂN LOẠI — nó xác nhận "đếm đủ" chứ không xác nhận "đếm đúng thứ". 56 - 8 = 48.
SO_CHO_KY_VONG = 48

EXT = (".js", ".html", ".css", ".md", ".json", ".txt", ".py")

# Tệp KHÔNG BAO GIỜ đổi: bản ghi lịch sử, đầu ra sinh tự động, thư viện bên thứ ba,
# và CHÍNH TỆP NÀY.
#
# CHÍNH TỆP NÀY — và đây là lần thứ năm trong dự án một công cụ suýt phá chính nó. Script này
# nằm trong tools/ nên nó nằm trong danh sách quét của chính nó, mà docstring + hai hằng
# TEN_CU_HOA/TEN_CU_Hoa của nó chứa đúng chuỗi cần thay. Lần chạy ĐẦU không sao (git ls-files
# chưa thấy tệp chưa commit), nhưng ngay sau khi commit thì lần chạy kế tiếp sẽ viết
# `TEN_CU_HOA = "HỌC AI"` — tức biến script thành vô nghĩa và xoá mất bản ghi của lần đổi tên.
# Cùng họ với cổng G18b phải ghép chuỗi dò lúc chạy ("iee" + "ai2026") để không tự bắt mình.
GIU_THEO_TEP = re.compile(
    r"^review\d*/|^\.hermes/|^moxe-ai/|^out/|/vendor/|^vendor/"
    r"|so_lieu_ho_so\.json$|^SHA256SUMS"
    # HAI SCRIPT ĐỔI TÊN/ĐỊNH DANH CŨ — bản thân chúng là BẢN GHI của lần đổi trước.
    # `doi_dinh_danh_cap_thpt.py` có bảng RULES là các cặp chuỗi cũ→mới ĐÃ THI HÀNH (vd
    # "# SOI AI · Lớp 10 — …" → "# SOI AI — …"), và docstring của nó ghi lại ranh giới
    # "Tên sản phẩm giữ nguyên SOI AI" — đúng với thời điểm nó được viết. Sửa hai thứ đó thì
    # bản ghi thành sai và script không tái chạy/đối chiếu được. Cùng lý do đã loại
    # `doi_ten_soi_ai.py` (bản ghi lần MỔ XẺ AI → SOI AI) ngay từ đầu.
    # Phát hiện nhờ ĐỌC NGỮ CẢNH 4 tệp đáng ngờ sau khi dry-run đã báo "56 = 56 khớp kỳ vọng":
    # chốt chặn theo SỐ LƯỢNG cho cảm giác an toàn sai, vì nó không kiểm phân loại.
    r"|^tools/doi_ten_soi_ai\.py$|^tools/doi_dinh_danh_cap_thpt\.py$"
    r"|^tools/doi_ten_hoc_ai\.py$")

# Khoá dữ liệu / tên hằng nội bộ: đổi là mất dữ liệu hoặc hỏng CSS.
GIU_KHOA = re.compile(r"soiai_|__SOIAI_|SOIAI_|SOI_AI_SITE|logo-soi|kb-logo-soi")

# Ngữ cảnh phải GIỮ nguyên văn dù nằm trong tệp được đổi.
GIU_NGU_CANH = [
    (re.compile(r'"Soi AI để hiểu AI"|khau = "Soi AI để hiểu AI"'),
     "cổng G10c — chuỗi trong DANH SÁCH CẤM"),
    (re.compile(r'thành "SOI AI"|thành SOI AI|đổi tên thành SOI AI'),
     "ghi chú LỊCH SỬ đổi tên"),
    (re.compile(r"MỔ XẺ AI"), "ghi chú LỊCH SỬ tên đời đầu"),
    # DÒNG QUYẾT ĐỊNH trong hai script sinh Google Sheet quản lý dự án. Đây là bản ghi của một
    # câu hỏi ĐÃ ĐƯỢC ĐẶT RA và lý do chọn đáp án khi đó ("Giữ SOI AI: thuần Việt 1 âm tiết,
    # đúng cơ chế 'soi lỗi'"). Viết lại thành "HỌC AI — giữ hay đổi?" sẽ làm bản ghi nói dối về
    # chính quyết định đó: người đọc sau tưởng câu hỏi là về HỌC AI. Quyết định nay đã bị chủ
    # sản phẩm đảo ngược (08/10) — cách đúng là GIỮ bản ghi cũ và ghi nhận quyết định mới ở nơi
    # khác (commit message + README §8), đúng nguyên tắc "thêm phụ lục, không viết đè".
    (re.compile(r"[Gg]iữ (tên )?SOI AI|Tên sản phẩm 'SOI AI'|giữ hay đổi"),
     "DÒNG QUYẾT ĐỊNH trong sheet quản lý dự án (bản ghi lịch sử)"),
]

# Ba phép thay, theo thứ tự: logo tách chữ trước (kẻo "SOI <span>AI" lọt lưới), rồi in hoa, rồi
# hoa đầu câu. LOGO TÁCH CHỮ là bẫy đã ghi trong script đổi tên lần trước.
RE_LOGO = re.compile(r"SOI(\s*<span[^>]*>\s*)AI")

# Chữ thay cho logo TÁCH CHỮ, và nó KHÁC chữ thay cho chuỗi liền — đây là lỗi đã đo được trước
# khi ghi. index.html:47 viết `SOI <span>AI</span>` (chữ AI được tô màu bằng span riêng). Bản đầu
# của script thay bằng `HỌC AI` + span + `AI`, cho ra `HỌC AI <span>AI</span>` — tức giao diện hiển
# thị "HỌC AI AI". Không cổng nào bắt được lỗi này: G10b chỉ khoá PHỤ ĐỀ, G2d chỉ đếm emoji trong
# .logo, và chuỗi vẫn parse hợp lệ. Nó chỉ lộ khi chạy đúng phép thay trên dòng thật rồi in ra.
# Luật: chỗ nào văn bản bị CHẺ bằng thẻ thì chữ thay cũng phải chẻ tương ứng, không ghép nguyên tên.
TEN_MOI_LOGO = "HỌC"


def files():
    r = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, timeout=120)
    return [f for f in r.stdout.split("\n") if f and f.endswith(EXT)]


def doi_dong(ln):
    """Trả (dòng_mới, số_lần_đổi). Giữ nguyên nếu dòng thuộc nhóm khoá hoặc ngữ cảnh cấm."""
    if GIU_KHOA.search(ln):
        return ln, 0
    for rx, _ in GIU_NGU_CANH:
        if rx.search(ln):
            return ln, 0
    n = 0
    moi = ln
    moi, k = RE_LOGO.subn(TEN_MOI_LOGO + r"\1" + "AI", moi)
    n += k
    k = moi.count(TEN_CU_HOA)
    moi = moi.replace(TEN_CU_HOA, TEN_MOI_HOA)
    n += k
    k = moi.count(TEN_CU_Hoa)
    moi = moi.replace(TEN_CU_Hoa, TEN_MOI_Hoa)
    n += k
    return moi, n


def quet(ghi):
    """Quét toàn repo. Ở chế độ --ghi thì ghi; luôn trả tổng số chỗ đổi."""
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
    """Verify HAI CHIỀU sau khi ghi — cả 'tên mới có mặt' lẫn 'thứ phải giữ còn nguyên'."""
    print("\n--- VERIFY SAU KHI GHI (hai chiều) ---")
    ok = True

    def doc(f):
        try:
            return io.open(os.path.join(ROOT, f), encoding="utf-8").read()
        except OSError:
            return ""

    # CHIỀU 1: tên thương hiệu cũ phải HẾT trong các tệp hiển thị chính (không tính nhóm GIỮ).
    # Đếm bằng chính logic doi_dong: nếu còn chỗ đổi được nghĩa là chưa sạch.
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
    print(f"  {'OK  ' if tot else '<<<'} tên cũ còn đổi được ở {con_doi} chỗ (phải 0)")

    # CHIỀU 2: những thứ BẮT BUỘC giữ phải còn nguyên văn.
    giu = [
        ("tools/nghiem_thu.py", '"Soi AI để hiểu AI"', 3, "cổng G10c còn cấm khẩu hiệu cũ"),
        ("tools/tao_sheet_thietke.py", "Soi AI để hiểu AI", 1, "sheet ghi khẩu hiệu cũ"),
        ("js/engine.js", "soiai_dulieu_v1", 1, "khoá localStorage còn nguyên (không mất dữ liệu HS)"),
        ("README.md", "MỔ XẺ AI", 2, "lịch sử đổi tên đời đầu còn nguyên"),
    ]
    for f, chuoi, ky_vong, mo_ta in giu:
        n = doc(f).count(chuoi)
        tot = (n == ky_vong)
        ok &= tot
        print(f"  {'OK  ' if tot else '<<<'} {f}: {chuoi!r} còn {n} lần (kỳ vọng {ky_vong}) — {mo_ta}")

    # CHIỀU 3: tên mới PHẢI có mặt ở nơi học sinh/giám khảo nhìn thấy.
    for f, chuoi in [("index.html", TEN_MOI_HOA), ("data/meta.js", TEN_MOI_HOA)]:
        n = doc(f).count(chuoi)
        tot = (n > 0)
        ok &= tot
        print(f"  {'OK  ' if tot else '<<<'} {f}: tên mới {chuoi!r} xuất hiện {n} lần (phải >0)")

    # CHIỀU 4: LOGO TÁCH CHỮ phải ra "HỌC <span>AI</span>", KHÔNG được thành "HỌC AI <span>AI".
    # Đây là phép kiểm cho đúng cái lỗi đã đo được khi viết script (xem chú thích ở TEN_MOI_LOGO).
    # Nó cũng là thứ không cổng nào trong bộ 80 tiêu chí canh, nên phải nằm ở đây.
    idx = doc("index.html")
    logo_dung = 'class="logo-txt">HỌC <span>AI</span>' in idx
    logo_sai = bool(re.search(r"HỌC AI\s*<span[^>]*>\s*AI", idx))
    tot = logo_dung and not logo_sai
    ok &= tot
    print(f"  {'OK  ' if tot else '<<<'} index.html logo: 'HỌC <span>AI</span>' có mặt={logo_dung}"
          f" · dạng lặp 'HỌC AI AI'={logo_sai} (phải False)")
    return ok


def main():
    ghi = "--ghi" in sys.argv
    print(f"ĐỔI TÊN THƯƠNG HIỆU: {TEN_CU_HOA} -> {TEN_MOI_HOA}")
    print(f"CHẾ ĐỘ: {'GHI THẬT' if ghi else 'CHỈ KIỂM (thêm --ghi để ghi)'}")
    print(f"ROOT (suy từ __file__): {ROOT}\n" + "=" * 92)

    # HAI LƯỢT, và thứ tự này là bắt buộc. Bản đầu của hàm này gọi `quet(ghi)` MỘT lần rồi mới
    # so tổng với số kỳ vọng — nghĩa là ở chế độ --ghi nó GHI XONG MỚI KÊU. Hồ sơ/mã nguồn bị sửa
    # nửa vời trong khi màn hình in "DỪNG — KHÔNG ghi gì": thông báo nói dối về chính việc nó vừa
    # làm. Đó đúng là lỗi đã sửa ở tools/dong_bo_so_lieu_ho_so.py, tái sinh ở đây.
    # Lượt 1 CHỈ ĐẾM. Chỉ khi tổng khớp kỳ vọng mới sang lượt 2 để ghi.
    tong = quet(False)
    print("=" * 92)
    print(f"LƯỢT 1 (chỉ đếm): {tong} chỗ sẽ đổi (kỳ vọng {SO_CHO_KY_VONG})")

    if tong != SO_CHO_KY_VONG:
        print(f"\nDỪNG — tổng {tong} KHÁC kỳ vọng {SO_CHO_KY_VONG}. CHƯA GHI GÌ CẢ.")
        print("Mã đã đổi từ trước, hoặc có chỗ mới phát sinh mà kiểm kê chưa biết. Xem lại từng")
        print("dòng trên rồi mới chạy; đừng sửa số kỳ vọng cho khớp nếu chưa đọc ngữ cảnh.")
        return 1

    if not ghi:
        print("\n(Chưa ghi gì. Chạy lại với --ghi để ghi thật.)")
        return 0

    print("\nLƯỢT 2 (ghi thật):")
    da_ghi = quet(True)
    print("=" * 92)
    print(f"ĐÃ GHI {da_ghi} chỗ (phải bằng lượt 1: {tong})")
    if da_ghi != tong:
        print("!!! HAI LƯỢT LỆCH NHAU — cây đang ở trạng thái nửa vời. Kiểm tra `git diff` ngay.")
        return 1

    return 0 if verify() else 1


if __name__ == "__main__":
    sys.exit(main())
