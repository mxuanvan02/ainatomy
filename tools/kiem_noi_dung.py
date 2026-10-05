#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""KIỂM TRA NỘI DUNG HỌC SINH PHẢI ĐỌC — các lỗi mà judge tĩnh không bắt được.

VÌ SAO CÓ TỆP NÀY
  Vòng build 04/10 phát hiện ra ba lớp lỗi đều ĐÃ LỌT QUA các phép kiểm trước đó:

  1. KÝ TỰ ĐỒNG TỰ (homoglyph). Chuỗi "t1-tiend" + U+043E trông y hệt "t1-tiendo"
     nhưng chữ o là CYRILLIC. querySelector trả null, hàm return sớm, nút "Chấm nhãn"
     vĩnh viễn disabled — hỏng cả Trạm 1 mà KHÔNG báo lỗi nào. Mắt thường không phân
     biệt nổi, nên phải quét theo mã Unicode. Lỗi này lặp lại lần thứ hai ở
     js/kichban.js nên nay thành phép kiểm bắt buộc.

  2. EMOJI LÀM BIỂU TƯỢNG. MASTER.md cấm. Emoji render khác nhau giữa Windows/macOS/
     Android và mất nét khi phóng to trên máy chiếu lớp học.

  3. COMMENT TRỎ TỚI TỆP KHÔNG TỒN TẠI. Đã xảy ra: ghi chú "đo bằng tools/
     tinh_do_phu.py" và "có phép kiểm trong tools/kiem_noi_dung.py" được viết TRƯỚC
     khi các tệp đó tồn tại. Ghi chú kiểu này nguy hiểm hơn không có ghi chú, vì nó
     tạo bằng chứng giả cho người đọc sau.

CÁCH CHẠY
  python3 tools/kiem_noi_dung.py
  exit 0 = sạch, exit 1 = còn lỗi (dùng làm cổng trong CI/judge).

NGƯỠNG: cả ba phép kiểm đều là 0 lỗi. Không hạ ngưỡng để pass.
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")

# Ký tự trông giống chữ Latin nhưng không phải. Quét theo khoảng Unicode, không gõ tay
# từng chữ — gõ tay chính là cách ký tự lạ lọt vào tệp ngay từ đầu.
KY_TU_LA = [
    ("Cyrillic", 0x0400, 0x04FF),
    ("Greek", 0x0370, 0x03FF),
    ("Fullwidth Latin", 0xFF21, 0xFF3A),
    ("Fullwidth Latin", 0xFF41, 0xFF5A),
]

# NGOẠI LỆ HỢP LỆ — thêm sau khi K1 báo oan (04/10):
#   js/lab3d.js:71 dùng 'Σ' (U+03A3) trong COMMENT để viết công thức toán
#   "Σ wi*(...)". Đây là ký hiệu tổng, KHÔNG phải chữ Latin trá hình, và nằm trong
#   chú thích chứ không phải selector/định danh nên không thể gây lỗi runtime.
#   Nguyên tắc phân biệt: chữ Hy Lạp "giống Latin" (Α Β Ε Ζ Η Ι Κ Μ Ν Ο Ρ Τ Υ Χ) mới
#   nguy hiểm; ký hiệu toán (Σ Δ Ω π θ λ μ ...) thì hợp lệ. Liệt kê tường minh nhóm
#   được phép thay vì chặn cả khoảng Greek.
TOAN_HOP_LE = set("ΣΔΩΘΛΜΦΨΓΠσδωθλμφψγπξε∂∞≈≤≥≠±×÷→←∑∏√∫")

# Khoảng emoji + ký tự hình ảnh
EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\U00002B00-\U00002BFF\U0000FE0F]"
)

DUONG_DAN_RE = re.compile(r"(?:tools|js|css|data|vendor|design-system)/[\w./-]+\.(?:py|js|css|html|svg|json|md)")


def cac_tep():
    for goc, dirs, fs in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ("vendor", ".git", "shot")]
        for f in fs:
            if f.endswith((".js", ".html", ".css")):
                yield os.path.join(goc, f)


def doc(p):
    return io.open(p, encoding="utf-8", errors="replace").read()


def k1_ky_tu_la():
    """K1 — ký tự đồng dạng (homoglyph) trong MÃ NGUỒN, kể cả trong comment."""
    loi = []
    for p in cac_tep():
        s = doc(p)
        for i, ch in enumerate(s):
            o = ord(ch)
            if ch in TOAN_HOP_LE:          # ký hiệu toán: hợp lệ, bỏ qua (đã ghi chú ở trên)
                continue
            for ten, a, b in KY_TU_LA:
                if a <= o <= b:
                    dong = s[:i].count("\n") + 1
                    loi.append(f"{os.path.relpath(p, ROOT)}:{dong} — {ten} U+{o:04X} {ch!r}")
    return ("K1 ký tự đồng dạng (homoglyph)", loi,
            "Mắt thường không thấy. Đã 2 lần làm hỏng selector -> hàm return sớm, "
            "không báo lỗi. Ngoại lệ: ký hiệu toán hợp lệ.")


def k2_emoji():
    """K2 — emoji trong nội dung hiển thị (cấm làm biểu tượng)."""
    loi = []
    for p in cac_tep():
        s = doc(p)
        # bỏ chuỗi cấp phép của Lucide ("@license") vì không phải emoji
        for m in EMOJI_RE.finditer(s):
            dong = s[:m.start()].count("\n") + 1
            ngu = s[max(0, m.start() - 60):m.start() + 20].replace("\n", " ")
            loi.append(f"{os.path.relpath(p, ROOT)}:{dong} — U+{ord(m.group(0)):04X} trong: …{ngu[-70:]}")
    return ("K2 emoji làm biểu tượng", loi,
            "MASTER.md cấm; emoji render khác nhau giữa các hệ và mờ khi chiếu.")


def k3_duong_dan_mo():
    """K3 — comment/tài liệu trỏ tới tệp không tồn tại."""
    loi = []
    for p in cac_tep():
        s = doc(p)
        for m in DUONG_DAN_RE.finditer(s):
            rel = m.group(0)
            # thử cả trong repo sản phẩm lẫn thư mục tools của dự án
            ok = (os.path.exists(os.path.join(ROOT, rel))
                  or os.path.exists(os.path.join(ROOT, "data-source", rel))
                  or os.path.exists(os.path.join(TOOLS, os.path.basename(rel))))
            if not ok:
                dong = s[:m.start()].count("\n") + 1
                loi.append(f"{os.path.relpath(p, ROOT)}:{dong} — trỏ tới {rel} (KHÔNG tồn tại)")
    return ("K3 đường dẫn trong comment không tồn tại", loi,
            "Ghi chú trỏ tới thứ không có tạo ra bằng chứng giả cho người đọc sau.")


def main():
    phep = [k1_ky_tu_la(), k2_emoji(), k3_duong_dan_mo()]
    print("=" * 92)
    print("KIỂM TRA NỘI DUNG — 3 lớp lỗi đã từng lọt qua judge tĩnh")
    print("=" * 92)
    tong = 0
    for ten, loi, ly_do in phep:
        n = len(loi)
        tong += n
        print(f"\n{'✅' if n == 0 else '❌'} {ten}: {n} lỗi")
        print(f"   vì sao phải kiểm: {ly_do}")
        for x in loi[:12]:
            print(f"     · {x}")
        if n > 12:
            print(f"     … và {n - 12} lỗi nữa")
    print("\n" + "=" * 92)
    print(f"TỔNG: {tong} lỗi —", "SẠCH" if tong == 0 else "CHƯA ĐẠT")
    return 0 if tong == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
