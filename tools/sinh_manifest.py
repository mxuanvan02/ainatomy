#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Sinh lại SHA256SUMS.txt của repo soi-ai từ chính các tệp trên đĩa.

VÌ SAO PHẢI LÀ CHƯƠNG TRÌNH, KHÔNG ĐƯỢC GÕ TAY (luật 5f của skill agentic-efficiency-loop):
  Dự án này đã BỊA hash SHA256 hai lần liên tiếp — lần 1 gõ chuỗi hex không có thật, lần 2
  "sửa" bằng cách chép lại chính chuỗi bịa đó. Một manifest hash bịa là bằng chứng giả: nó
  đúng định dạng, đọc như thật, và cả hồ sơ dựa trên nó. Nên: sinh bằng hashlib, ghi ra tệp,
  rồi verify bằng `sha256sum -c` (đọc kết quả từ file, không qua pipe).

DANH SÁCH TỆP lấy từ CHÍNH manifest cũ (không tự bịa thêm/bớt), cộng js/muc3.js là tệp MỚI
  của đợt này. Giữ nguyên thứ tự sắp xếp theo đường dẫn như bản cũ để diff chỉ hiện đúng
  những dòng thật sự đổi.

Mặc định CHỈ KIỂM: in ra tệp nào lệch hash, KHÔNG ghi. Muốn ghi thật phải thêm --ghi.
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "."
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "soi-ai"))
# Đường dẫn gốc suy từ vị trí tệp này (luật 5m): script nằm ở ieeai2026/tools/, repo ở
# ieeai2026/soi-ai/ — nên đừng ghi cứng /home/<user>/... vì bản clone sẽ chấm nhầm máy.
MANIFEST = os.path.join(ROOT, "SHA256SUMS.txt")
THEM_MOI = ["js/muc3.js"]


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


def main():
    ghi = "--ghi" in sys.argv
    if not os.path.isfile(MANIFEST):
        print(f"!!! không thấy {MANIFEST}")
        return 1

    cu = {}
    for dong in open(MANIFEST, encoding="utf-8"):
        m = re.match(r"^([0-9a-f]{64})\s+(.+?)\s*$", dong)
        if m:
            cu[m.group(2)] = m.group(1)

    ds = sorted(set(cu) | set(THEM_MOI))
    print("=" * 96)
    print(f"SINH LẠI MANIFEST · {len(cu)} tệp trong bản cũ + {len(THEM_MOI)} tệp mới "
          f"-> {len(ds)} tệp")
    print("=" * 96)
    print(f"ROOT (suy từ vị trí script, không ghi cứng): {ROOT}")

    thieu, lech, moi, khop = [], [], [], []
    dong_moi = []
    for d in ds:
        p = os.path.join(ROOT, d)
        if not os.path.isfile(p):
            thieu.append(d)
            continue
        h = sha256(p)
        dong_moi.append(f"{h}  {d}")
        if d not in cu:
            moi.append(d)
        elif cu[d] != h:
            lech.append(d)
        else:
            khop.append(d)

    print(f"\n  khớp hash      : {len(khop)} tệp")
    print(f"  LỆCH hash      : {len(lech)} tệp {lech if lech else ''}")
    print(f"  TỆP MỚI        : {len(moi)} tệp {moi if moi else ''}")
    print(f"  THIẾU TRÊN ĐĨA : {len(thieu)} tệp {thieu if thieu else ''}")

    if thieu:
        print("\n!!! Có tệp trong manifest mà KHÔNG có trên đĩa. Không ghi gì cả —")
        print("    ghi bây giờ là XOÁ tệp đó khỏi manifest, tức mất dấu một tệp đã từng có.")
        print("    Quyết định thủ công: tệp bị xoá thật, hay manifest sai?")
        return 1

    if not ghi:
        print("\n(CHẾ ĐỘ CHỈ-KIỂM — chưa ghi gì. Chạy lại với --ghi để ghi thật.)")
        return 0

    # Ghi: sao lưu bản cũ TRƯỚC, rồi ghi qua tệp tạm và os.replace để không để lại
    # manifest nửa vời nếu tiến trình chết giữa chừng.
    import shutil
    import time
    bak = f"{MANIFEST}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
    shutil.copy2(MANIFEST, bak)
    tam = MANIFEST + ".tmp"
    with open(tam, "w", encoding="utf-8") as f:
        f.write("\n".join(dong_moi) + "\n")
    os.replace(tam, MANIFEST)
    print(f"\nĐÃ GHI {MANIFEST}  ({len(dong_moi)} dòng)")
    print(f"  sao lưu bản cũ: {bak}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
