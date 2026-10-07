#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Đổi ĐỊNH DANH sản phẩm: "…Trí tuệ nhân tạo lớp 10" -> "…Trí tuệ nhân tạo cấp THPT".

LÝ DO. Sản phẩm không còn là chuyện của riêng lớp 10: app cho nhập mã lớp tự do
(`index.html:83-84`, `js/app.js:188-190`), và Khung 2422/QĐ-BGDĐT có phụ lục yêu cầu cần đạt
cho CẢ BA lớp — đã định vị bằng số trong data-source/2422_PL_khung.txt:
    LỚP 10 @103295 · LỚP 11 @108657 · LỚP 12 @114841
Giữ chữ "lớp 10" trong định danh là tự thu hẹp sản phẩm so với những gì nó làm được.

BA RANH GIỚI MÀ SCRIPT NÀY CỐ Ý KHÔNG VƯỢT QUA. Đây là phần quan trọng nhất của tệp:

1. KHÔNG đổi "lớp 10" ở những chỗ nó là DỮ LIỆU/SỰ THẬT về phạm vi đã kiểm chứng.
   `data/yccd.js` chứa 22 yêu cầu cần đạt CỦA LỚP 10, trích nguyên văn và đã verify 22/22.
   `index.html:679-680` khai đúng điều đó. Sửa những chỗ ấy thành "cấp THPT" là làm hồ sơ
   KHAI RỘNG HƠN DỮ LIỆU THẬT — đúng lớp lỗi mà cổng G10b/G14 sinh ra để chặn.
   Vì vậy script này thay THẾ TỪNG CẶP CHUỖI CỤ THỂ kèm số lần kỳ vọng, không dùng
   replace("lớp 10", ...) toàn cục.

2. KHÔNG đổi "lớp 10" nằm TRONG NỘI DUNG CÂU HỎI. `js/nhamay_text.js:418` có
   `tuKhoa:[…, "lớp 10", …]` — đó là từ khoá của một bài đọc dùng để chấm, đổi là HỎNG ĐÁP ÁN.
   Tổng cộng 10 chỗ "lớp 10" nằm trong data/cauhoi*.js, data/kienthuc.js, js/nhamay_text.js.

3. KHÔNG đổi "SOI". Chữ này xuất hiện 73 lần nhưng 11 lần là ĐỘNG TỪ tiếng Việt mô tả đúng
   cơ chế sản phẩm, không phải tên: `index.html:380` "PHÒNG 3D — SOI MÔ HÌNH",
   `js/app.js:1008` "dấu hiệu đầu tiên để SOI ra chỗ hỏng", `js/muc3.js:263` "soi ĐÚNG sáu
   tiêu chí". Thay thế thô sẽ phá văn xuôi. Tên sản phẩm giữ nguyên "SOI AI".

CŨNG KHÔNG ĐỔI TÊN REPO. `soi-ai-lop10` nằm ở 12 chỗ, gồm link công khai trong hồ sơ dự thi
(ho-so/video_brief.md:172, review9/de_bai_phan_bien.md:12). Bằng chứng đo được ngày 07/10:
    https://mxuanvan02.github.io/soi-ai-lop10/  -> HTTP 200
    https://mxuanvan02.github.io/soi-ai/        -> HTTP 404
Tức lần đổi tên trước (moxe-ai -> soi-ai -> soi-ai-lop10) ĐÃ làm chết link cũ thật, và
tools/quet_so_cu.py:16 của chính dự án đã ghi "Link chết trong hồ sơ nguy hiểm hơn link sai".
Hạn nộp hồ sơ là 25/10/2026. Đổi tên repo trước mốc đó là đánh đổi một rủi ro đã có tiền lệ
lấy một lợi ích thuần thẩm mỹ. Việc đổi repo nên làm SAU 25/10, và khi làm thì phải giữ bản
github.io tên cũ sống song song một thời gian.

CÁCH CHẠY:  python3 tools/doi_dinh_danh_cap_thpt.py            (chỉ kiểm, chưa ghi)
            python3 tools/doi_dinh_danh_cap_thpt.py --ghi      (ghi thật)
Script báo cáo TỪNG chỗ đã đổi và đối chiếu với số lần kỳ vọng; lệch là dừng và báo, không ghi.
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CU = "Phòng thực hành Trí tuệ nhân tạo lớp 10"
MOI = "Phòng thực hành Trí tuệ nhân tạo cấp THPT"

# (tệp, chuỗi cũ, chuỗi mới, số lần kỳ vọng). Số lần kỳ vọng là CHỐT CHẶN: nếu thực tế khác
# thì có nghĩa tệp đã đổi từ trước, hoặc có chỗ mới phát sinh mà người viết script chưa biết —
# cả hai đều phải dừng lại mà nhìn, không được ghi đè im lặng.
THAY = [
    # --- Định danh: cùng một chuỗi ở 5 tệp (7 chỗ) ---
    ("index.html", CU, MOI, 4),                      # dòng 6 title, 48 tagline, 662, 697 chân trang
    ("data/meta.js", CU, MOI, 1),                    # dòng 7: dinhDanh
    ("js/kichban.js", CU, MOI, 1),                   # dòng 309: kb-logo-soi (logo trong kịch bản)
    ("tools/nghiem_thu.py", CU, MOI, 1),             # dòng 832: hằng TEN của cổng G10b

    # --- Ba chỗ viết khác kiểu, phải thay riêng ---
    ("index.html",
     '<h2>Phòng thực hành <span class="logo-soi">Trí tuệ nhân tạo</span> lớp 10</h2>',
     '<h2>Phòng thực hành <span class="logo-soi">Trí tuệ nhân tạo</span> cấp THPT</h2>', 1),
    ("index.html",
     "phần mềm dạy và kiểm định năng lực AI cho học sinh lớp 10, bám Khung 2422/QĐ-BGDĐT",
     "phần mềm dạy và kiểm định năng lực AI cho học sinh trung học phổ thông, "
     "bám Khung 2422/QĐ-BGDĐT", 1),
    ("README.md",
     "# SOI AI · Lớp 10 — Hướng dẫn giáo viên (v1.0.0)",
     "# SOI AI — Hướng dẫn giáo viên cấp THPT (v1.0.0)", 1),
    ("huong-dan-danh-gia.md",
     "dạy chuyên đề AI lớp 10 bằng SOI AI",
     "dạy chuyên đề AI bằng SOI AI", 1),
]

# Câu khai PHẠM VI, chèn vào README ngay sau đoạn giới thiệu. Bắt buộc có: đổi định danh thành
# "cấp THPT" mà không nói rõ dữ liệu đã kiểm chứng mới phủ lớp 10 thì hồ sơ thành khai quá.
NEO_README = "Học sinh **bắt lỗi AI** thay vì hỏi AI; hệ thống **tự chấm** vì lỗi do chính hệ cài sẵn.\n"
PHAM_VI = (
    "\n**Phạm vi dữ liệu đã kiểm chứng.** Định danh là cấp trung học phổ thông vì app không khoá "
    "lớp (mã lớp nhập tự do) và Khung 2422/QĐ-BGDĐT có phụ lục yêu cầu cần đạt cho cả lớp 10, 11, "
    "12. Nhưng bản đồ yêu cầu cần đạt đang nhúng trong app là của **lớp 10** — 22 yêu cầu, trích "
    "nguyên văn, đã kiểm chứng tự động 22/22 với văn bản Bộ bằng `tools/verify_yccd.py`. Nói rõ "
    "ranh giới này để hồ sơ không khai rộng hơn dữ liệu thật; mở rộng sang lớp 11 và 12 là việc "
    "trích thêm phụ lục, không phải việc đổi chữ.\n"
)


def main():
    ghi = "--ghi" in sys.argv
    print(f"CHẾ ĐỘ: {'GHI THẬT' if ghi else 'CHỈ KIỂM (thêm --ghi để ghi)'}\n")
    print("=" * 92)

    loi, tong = [], 0
    for tep, cu, moi, ky_vong in THAY:
        p = os.path.join(ROOT, tep)
        if not os.path.isfile(p):
            loi.append(f"{tep}: KHÔNG TỒN TẠI")
            continue
        s = io.open(p, encoding="utf-8").read()
        n = s.count(cu)
        if n != ky_vong:
            loi.append(f"{tep}: gặp {n} lần, kỳ vọng {ky_vong} lần — chuỗi: {cu[:58]!r}")
            continue
        tong += n
        print(f"  [×{n}] {tep:26s} {cu[:44]!r}")
        print(f"        {'':26s} -> {moi[:44]!r}")
        if ghi:
            io.open(p, "w", encoding="utf-8").write(s.replace(cu, moi))

    # Chèn câu khai phạm vi vào README (chỉ khi chưa có).
    p_readme = os.path.join(ROOT, "README.md")
    s_readme = io.open(p_readme, encoding="utf-8").read()
    if "Phạm vi dữ liệu đã kiểm chứng" in s_readme:
        print("  [bỏ qua] README đã có câu khai phạm vi")
    elif NEO_README not in s_readme:
        loi.append("README.md: không tìm thấy dòng neo để chèn câu khai phạm vi")
    else:
        print(f"  [+1 ] {'README.md':26s} chèn đoạn khai PHẠM VI DỮ LIỆU ĐÃ KIỂM CHỨNG")
        tong += 1
        if ghi:
            io.open(p_readme, "w", encoding="utf-8").write(
                s_readme.replace(NEO_README, NEO_README + PHAM_VI, 1))

    print("=" * 92)
    if loi:
        print(f"DỪNG — {len(loi)} chỗ LỆCH kỳ vọng, KHÔNG ghi gì cả:")
        for l in loi:
            print("  !", l)
        print("\nLệch nghĩa là tệp đã đổi từ trước hoặc có chỗ mới phát sinh. Xem lại rồi mới chạy.")
        return 1
    print(f"TỔNG: {tong} chỗ sẽ đổi" if not ghi else f"TỔNG: {tong} chỗ ĐÃ đổi")

    if ghi:
        # Verify: định danh cũ phải hết hẳn ở 4 tệp thương hiệu, nhưng PHẢI CÒN ở những tệp
        # khai sự thật về phạm vi YCCĐ lớp 10. Kiểm cả hai chiều, vì chỉ kiểm "hết chưa" thì
        # một cú replace toàn cục phá data/yccd.js cũng vẫn báo thành công.
        print("\n--- VERIFY SAU KHI GHI ---")
        phai_het = ["index.html", "data/meta.js", "js/kichban.js", "README.md"]
        phai_con = ["data/yccd.js", "js/nhamay_text.js", "data/kienthuc.js"]
        for f in phai_het:
            s = io.open(os.path.join(ROOT, f), encoding="utf-8").read()
            n = s.count(CU)
            print(f"  {f:26s} định danh cũ còn {n} lần  {'OK' if n == 0 else '<<< CHƯA HẾT'}")
        for f in phai_con:
            s = io.open(os.path.join(ROOT, f), encoding="utf-8").read()
            n = s.lower().count("lớp 10")
            print(f"  {f:26s} 'lớp 10' (dữ liệu thật) còn {n} lần  "
                  f"{'OK — không bị đổi nhầm' if n > 0 else '<<< BỊ ĐỔI NHẦM, DỮ LIỆU HỎNG'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
