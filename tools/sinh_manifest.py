#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Sinh lại SHA256SUMS.txt của repo soi-ai từ chính các tệp trên đĩa.

VÌ SAO PHẢI LÀ CHƯƠNG TRÌNH, KHÔNG ĐƯỢC GÕ TAY (luật 5f của skill agentic-efficiency-loop):
  Dự án này đã BỊA hash SHA256 hai lần liên tiếp — lần 1 gõ chuỗi hex không có thật, lần 2
  "sửa" bằng cách chép lại chính chuỗi bịa đó. Một manifest hash bịa là bằng chứng giả: nó
  đúng định dạng, đọc như thật, và cả hồ sơ dựa trên nó. Nên: sinh bằng hashlib, ghi ra tệp,
  rồi verify bằng `sha256sum -c` (đọc kết quả từ file, không qua pipe).

DANH SÁCH TỆP lấy từ `git ls-files` — tức CHÍNH git quyết định tệp nào thuộc sản phẩm.

  LỖI ĐÃ SỬA (06/10), và đây là lỗi nặng nhất tìm được trong đợt phản biện này:
  bản đầu lấy danh sách từ `set(manifest_cũ) | set(THEM_MOI_gõ_tay)`. Hệ quả là một tệp
  chỉ được vào manifest nếu nó ĐÃ ở trong manifest, hoặc có ai nhớ gõ tên nó vào THEM_MOI.
  Tệp mới không nằm trong cả hai thì RƠI ÂM THẦM — không lỗi, không cảnh báo, script vẫn
  in "ĐÃ GHI ... (72 dòng)" và `sha256sum -c` vẫn trả 72/72 OK. Đo thật lúc phát hiện:
  git theo dõi 90 tệp, manifest chỉ có 72 — thiếu 18 tệp, trong đó có:
    · tools/nghiem_thu.py  — CHÍNH CÁI CỔNG sinh ra mọi con số "56/56 ĐẠT". Sửa cổng để nó
      luôn in ĐẠT thì manifest KHÔNG phát hiện. Đây là lỗ hổng tự tham chiếu: bằng chứng
      toàn vẹn không phủ công cụ sinh ra bằng chứng.
    · tools/kiem_noi_dung.py, tinh_do_phu.py, gop_csv.py, sinh_manifest.py — mọi công cụ đo.
    · data-source/2422_PL_khung.pdf — VĂN BẢN BỘ có chữ ký Thứ trưởng, căn cứ pháp lý của
      cả sản phẩm và là thứ giám khảo sẽ đối chiếu.
  README.md dòng 108 khai manifest là "bằng chứng mốc thời gian & toàn vẹn" — lời khai đó
  sai với phạm vi thực tế của nó. Đã kiểm: KHÔNG có gate hay ghi chú nào nói việc bỏ sót
  tools/ là cố ý (grep "SHA256SUMS" trong nghiem_thu.py ra rỗng), nên đây là rơi âm thầm
  chứ không phải thiết kế.
  Nay lấy danh sách từ git, và KHÔNG CẦN danh sách gõ tay nào nữa — tệp mới tự động vào.

  Loại trừ duy nhất: chính SHA256SUMS.txt (không thể hash chính nó một cách có nghĩa).

Mặc định CHỈ KIỂM: in ra tệp nào lệch hash, KHÔNG ghi. Muốn ghi thật phải thêm --ghi.
"""
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "."
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "soi-ai"))
# Đường dẫn gốc suy từ vị trí tệp này (luật 5m): script nằm ở ieeai2026/tools/, repo ở
# ieeai2026/soi-ai/ — nên đừng ghi cứng /home/<user>/... vì bản clone sẽ chấm nhầm máy.
MANIFEST = os.path.join(ROOT, "SHA256SUMS.txt")
LOAI_TRU = {"SHA256SUMS.txt"}


def danh_sach_tep():
    """Danh sách tệp THUỘC SẢN PHẨM, lấy từ git — nguồn có thẩm quyền duy nhất.

    Trả None nếu không phải repo git, để người gọi biết mà dừng thay vì âm thầm sinh một
    manifest thiếu (đúng lớp lỗi vừa sửa ở trên).
    """
    try:
        r = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                           text=True, timeout=120)
    except (OSError, subprocess.SubprocessError):
        return None
    if r.returncode != 0:
        return None
    ds = [d for d in r.stdout.split("\n") if d and d not in LOAI_TRU]
    return sorted(ds) or None


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

    ds = danh_sach_tep()
    if not ds:
        print("!!! không đọc được danh sách tệp từ `git ls-files`.")
        print("    KHÔNG suy ra từ manifest cũ: làm vậy là tái sinh đúng lỗi đã sửa —")
        print("    tệp mới sẽ rơi âm thầm và manifest vẫn in ra trông đầy đủ.")
        print(f"    Chạy trong repo git (ROOT = {ROOT}) hoặc tự thêm tệp vào LOAI_TRU/danh sách.")
        return 1

    print("=" * 96)
    print(f"SINH LẠI MANIFEST · git theo dõi {len(ds)} tệp (đã trừ {sorted(LOAI_TRU)})")
    print("=" * 96)
    print(f"ROOT (suy từ vị trí script, không ghi cứng): {ROOT}")

    # Tệp có trong manifest CŨ nhưng git không theo dõi nữa: báo rõ, không âm thầm xoá.
    # Đây có thể là (a) tệp vừa bị git rm — xoá khỏi manifest là đúng, hoặc
    # (b) tệp bị .gitignore sót — xoá khỏi manifest là MẤT BẰNG CHỨNG. Người chạy phải quyết.
    mo_cui = sorted(set(cu) - set(ds) - LOAI_TRU)
    if mo_cui:
        print(f"\n  TRONG MANIFEST CŨ NHƯNG GIT KHÔNG THEO DÕI ({len(mo_cui)} tệp): {mo_cui}")
        print("  -> chúng sẽ bị GỠ khỏi manifest. Nếu đây là tệp sản phẩm thật thì phải")
        print("     `git add` nó TRƯỚC — gỡ khỏi manifest là mất bằng chứng toàn vẹn.")
        if not ghi:
            print("     (chế độ chỉ-kiểm: chưa gỡ gì)")

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
