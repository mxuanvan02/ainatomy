#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bộ kiểm TỔNG QUÁT: mọi mã YCCĐ lớp 10 xuất hiện trong repo phải nằm trong danh sách 22 mã
của Khung 2422. Không chỉ tìm '10.C5' — tìm MỌI mã không hợp lệ, ở CẢ HAI repo.

Vì sao không vá từng chỗ: lần sửa trước dùng heuristic 'rel bắt đầu bằng js/ hoặc tools/ thì
thuộc repo con' và SAI, vì cả hai repo đều có thư mục tools/ và đều giữ bản sao tài liệu thiết
kế. Kết quả: script báo OK 10/10 phép thay trong khi quét lại còn 21 chỗ. Đây là lần thứ tư
bẫy 'hai repo lồng nhau' xuất hiện trong dự án này, nên bộ kiểm phải đi theo ĐƯỜNG DẪN TUYỆT
ĐỐI tìm được bằng os.walk, không suy ra từ tiền tố tên tệp.
"""
import io
import os
import re
import sys

# Đường dẫn SUY RA từ vị trí chính tệp này, không ghi cứng. Tệp nằm ở <repo_con>/tools/tests/
# nên repo_con = lên 2 cấp, repo_cha = cha của repo_con. Ghi cứng '/home/<tác giả>/...' sẽ phá
# cổng G18a/G18b (sản phẩm phải tự chứa — giáo viên clone về máy khác vẫn chạy được). Chính
# bộ kiểm này, khi mới thêm vào để bắt mã YCCĐ sai, đã bị G18 bắt vì lỗi đường dẫn cứng: một
# cổng kêu oan thì người ta bỏ qua luôn phần đúng của nó, nên phải sạch từ đầu.
import os as _os_here
_DAY = _os_here.path.dirname(_os_here.path.abspath(__file__))
REPO_CON = _os_here.path.abspath(_os_here.path.join(_DAY, "..", ".."))
REPO_CHA = _os_here.path.dirname(REPO_CON)
KHUNG = _os_here.path.join(REPO_CHA, "research/src/2422_PL_khung.txt")

BO_QUA_THU_MUC = {".git", "node_modules", "_build", "__pycache__", "_backups", ".hermes"}
# Chỉ soi tệp có thể chảy ra sản phẩm hoặc hồ sơ nộp
DUOI = (".js", ".py", ".html", ".json", ".md", ".csv", ".txt")
# Không soi chính bộ kiểm này và các bản ghi rà soát cũ (chúng TRÍCH mã sai để giải thích)
BO_QUA_TEP = ("/tmp/", "probe_c5", "fix_c5", "kiem_ma_yccd")


RE_MA_DAY_DU = r"10\.[A-D]\d?\.(?:MR)?\d+"
CHU_DE_10 = {"A1", "A2", "A3", "B2", "B3", "C2", "C3", "C4", "D1", "D2"}


def ma_chuan():
    """22 mã YCCĐ lớp 10, trích từ vùng LỚP 10 của Khung 2422 (bản text của PDF có chữ ký)."""
    kf = re.sub(r"\s+", " ", io.open(KHUNG, encoding="utf-8", errors="ignore").read())
    i10 = kf.find("LỚP 10")
    i11 = kf.find("LỚP 11")
    vung = kf[i10:i11] if (i10 >= 0 and i11 > i10) else kf
    return set(re.findall(r"10\.[A-D]\d?\.(?:MR)?\d+", vung)), vung


def chu_de_lop10(vung):
    return set(re.findall(r"(?<![A-Z\d.])([A-D]\d)\.\s", vung))


def quen(t):
    for b in BO_QUA_TEP:
        if b in t:
            return True
    return False


def main():
    chuan, vung = ma_chuan()
    print("=== DANH SÁCH CHUẨN: " + str(len(chuan)) + " mã YCCĐ lớp 10 (từ Khung 2422) ===")
    print("  " + ", ".join(sorted(chuan)))
    print("  chủ đề lớp 10: " + str(sorted(chu_de_lop10(vung))))

    # mọi token dạng 10.<chữ> trong repo — kể cả mã KHÔNG đầy đủ như '10.C5'
    RE_TOKEN = "10\.[A-D]\d?(?:\.(?:MR)?\d+)?"
    loi = {}
    for base in (REPO_CON, REPO_CHA):
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in BO_QUA_THU_MUC]
            # khi đi từ repo cha thì BỎ QUA repo con (đã đi riêng) để không đếm trùng
            if base == REPO_CHA and os.path.abspath(root).startswith(REPO_CON + os.sep):
                dirs[:] = []
                continue
            if base == REPO_CHA and os.path.abspath(root) == REPO_CON:
                dirs[:] = []
                continue
            for f in files:
                if not f.endswith(DUOI):
                    continue
                p = os.path.join(root, f)
                if quen(p):
                    continue
                try:
                    s = io.open(p, encoding="utf-8", errors="ignore").read()
                except Exception:
                    continue
                for m in re.finditer(RE_TOKEN, s):
                    tok = m.group(0)
                    if tok in chuan:
                        continue
                    # Token KHÔNG phải mã YCCĐ đầy đủ (thiếu phần '.n') thì đó là THAM CHIẾU
                    # CHỦ ĐỀ, ví dụ 'làm rõ cải tiến hệ thống 10.D2'. Chủ đề D2 CÓ ở lớp 10
                    # (10.D2.1, 10.D2.2) nên tham chiếu đó hợp lệ. Bản đầu của bộ kiểm báo nó
                    # là mã sai — một cổng kêu oan thì người đọc sẽ bỏ qua luôn phần đúng của nó
                    # (đúng bài học repo đã ghi ở mục [12] và cổng G11b/G17b). Chỉ bắt chủ đề
                    # KHÔNG thuộc lớp 10, ví dụ 10.C5 (C5 là chủ đề lớp 11).
                    if not re.fullmatch(RE_MA_DAY_DU, tok):
                        chu_de = tok[3:]
                        if chu_de in CHU_DE_10:
                            continue
                    ln = s[:m.start()].count("\n") + 1
                    ctx = re.sub(r"\s+", " ", s[max(0, m.start() - 70):m.end() + 40])
                    loi.setdefault(tok, []).append((p, ln, ctx))

    print("\n=== MÃ KHÔNG HỢP LỆ (không nằm trong 22 mã của Khung) ===")
    if not loi:
        print("  KHÔNG CÓ ✓")
    for tok in sorted(loi):
        print("\n  " + repr(tok) + " — " + str(len(loi[tok])) + " chỗ:")
        for p, ln, ctx in loi[tok]:
            print("    " + p.replace(REPO_CHA + "/", "") + ":" + str(ln))
            print("      …" + ctx[:110] + "…")
    print("\nTỔNG số chỗ cần xử lý: " + str(sum(len(v) for v in loi.values())))
    return 1 if loi else 0


if __name__ == "__main__":
    sys.exit(main())
