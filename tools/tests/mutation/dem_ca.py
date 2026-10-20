#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đếm ca kiểm thử từ log của các script mutation — con số trong hồ sơ phải tái lập được.

TỆP NÀY CỐ Ý KHÔNG KHAI SỐ SCRIPT. Bản cũ viết "log của 12 script mutation" và con số đó
đã sai ngay trong repo (thực tế 14 trước khi thêm mutation_g21.py): mỗi lần thêm một cổng
mới là docstring lại thành một lời khai cứng lỗi thời — đúng loại "lời hứa gãy" mà cổng
G17 sinh ra để chặn. Số script là thứ tệp này TỰ ĐẾM được từ thư mục log, nên không lý do
gì khai cứng nó ở đây.

VÌ SAO CÓ TỆP NÀY. Trong một phiên, tôi đếm tay số ca và ra BA con số khác nhau trên cùng một bộ
log: 29 (regex bỏ sót dòng thụt lề), 40 (bỏ sót 5 ca ở 5 script), rồi 42 (hai script không in
dòng KẾT LUẬN theo mẫu nên bị tính thành 0, trong khi số đúng là 48). Không lần nào con số sai
tự báo là sai — cả ba lần đều in ra trông hợp lệ. Con số đi thẳng vào hồ sơ nộp giám khảo.

Nên việc đếm phải là MỘT CHƯƠNG TRÌNH đọc dòng `KẾT LUẬN` mà chính mỗi script tự khai, chứ không
phải phép đếm viết lại mỗi lần. Sau khi chuẩn hoá 08/10, cả 12 script khai theo hai khuôn:

  Khuôn A — tự tách hai loại ca (script có ca đối chứng âm):
      KẾT LUẬN: <so>/<tong> ca đúng như kỳ vọng (<X> ca PHÁ bị cổng bắt + <Y> ca ĐỐI CHỨNG ÂM cổng im đúng)
  Khuôn B — mọi ca đều là ca phá (script không có ca đối chứng âm):
      KẾT LUẬN: <so>/<tong> ca phá đều bị G<k> bắt

HAI SỐ PHẢI LUÔN TÁCH. Ca đối chứng âm không phải "cổng bắt được" mà là "cổng không bắt oan";
gộp lại thành một số là khai quá, và chính 5 script trong repo này từng gộp như vậy.

CÁCH DÙNG
    # chạy hết bộ script rồi đếm (làm một lệnh, không tự chạy hộ)
    cd soi-ai
    for b in tools/tests/mutation/*.py; do python3 "$b" > "/tmp/mut/$(basename $b .py).log" 2>&1; done
    python3 tools/tests/mutation/dem_ca.py /tmp/mut
    # thêm --json= để nơi khác ĐỌC số này thay vì chép tay:
    python3 tools/tests/mutation/dem_ca.py /tmp/mut --json=out/mutation_dem.json

Tệp này KHÔNG tự chạy script nào: nó chỉ đọc log. Chạy hộ thì nó lại thành một công cụ sửa tệp
repo mà người gọi không biết, và mỗi script mutation cần cây sạch trước khi bắt đầu.

VÌ SAO CÓ --json (thêm 20/10). Con số này được chép TAY vào `tools/sinh_noi_dung_ho_so.py`
(hằng MUTATION) rồi in lên slide nộp giám khảo, và nó đã cũ âm thầm hai lần: 50 ca -> 63 ca ->
69 ca, mỗi lần thêm một script mutation. Cổng [14] của repo hồ sơ KHÔNG bắt được, vì kiểm nó đòi
chạy lại cả bộ mutation (vài phút, mỗi script sửa tệp repo rồi khôi phục) trong khi [14] là phép
kiểm nhanh. Một con số không có đường nào tự cập nhật thì sớm muộn cũng sai, nên nay tệp này XUẤT
số đo ra JSON kèm commit + cờ `day_du`, và nơi đọc (sinh_noi_dung_ho_so.py) FAIL-CLOSED: thiếu
tệp, phép đếm không đáng tin, hay commit của phép đếm khác commit mà bằng chứng cổng được sinh ra
thì in `<<THIẾU>>` và từ chối ghi slide.
"""
import io
import json
import os
import re
import subprocess
import sys
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def head_repo():
    """Commit ngắn của repo con lúc ĐẾM — để nơi đọc số này biết phép đếm thuộc bản mã nào.

    Vì sao cần: con số mutation đi thẳng vào slide nộp giám khảo. Một phép đếm chạy trên cây cũ
    rồi được chép vào tài liệu mô tả cây mới là đúng loại lỗi mà repo này đã mắc với nhãn commit
    `f383ee7` (số 10.865 không đo được ở cây đó). Ghi commit kèm số thì nơi đọc so được.
    Trả None khi không đọc được git — người gọi phải coi đó là THIẾU, không phải là "không quan trọng".
    """
    try:
        r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=REPO,
                           capture_output=True, text=True, timeout=60)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None

# Khuôn A: bắt buộc có cả nhóm tách hai loại. Đây là khuôn CHUẨN.
KA = re.compile(r"KẾT LUẬN: (\d+)/(\d+) ca đúng như kỳ vọng "
                r"\((\d+) ca PHÁ bị cổng bắt \+ (\d+) ca ĐỐI CHỨNG ÂM")
# Khuôn B: chỉ dùng cho script mà MỌI ca đều là ca phá. Cố ý hẹp.
KB = re.compile(r"KẾT LUẬN: (\d+)/(\d+) ca phá [^\n]*")


def main():
    argv = sys.argv[1:]
    duong_json = None
    thu_muc = None
    for a in argv:
        if a.startswith("--json="):
            duong_json = a.split("=", 1)[1]
        elif a == "--json":
            print("!!! --json cần dạng --json=<đường_dẫn>, không đoán tên tệp")
            return 2
        elif thu_muc is None:
            thu_muc = a
    if not thu_muc:
        print("dùng: python3 dem_ca.py <thư_mục chứa log các script mutation> [--json=<tệp.json>]")
        return 2
    if not os.path.isdir(thu_muc):
        print(f"!!! không thấy thư mục: {thu_muc}")
        return 2

    logs = sorted(f for f in os.listdir(thu_muc) if f.endswith(".log"))
    if not logs:
        # Thư mục rỗng cũng là dạng "đo hỏng cho ra số trông hợp lệ": in 0 ca mà không báo gì.
        print(f"!!! không có tệp .log nào trong {thu_muc} — CHƯA CHẠY, không phải 'không có ca'.")
        return 2

    print(f"{'SCRIPT':26s} {'CA':>4s} {'PHÁ':>4s} {'ĐỐI CHỨNG ÂM':>13s}  KHUÔN")
    print("-" * 74)
    tong = pha = dc = 0
    khong_khop, khong_dat = [], []
    for f in logs:
        s = io.open(os.path.join(thu_muc, f), encoding="utf-8").read()
        a = KA.search(s)
        if a:
            so, t, p, d = (int(x) for x in a.groups())
            khuon = "A"
        else:
            b = KB.search(s)
            if not b:
                khong_khop.append(f[:-4])
                print(f"{f[:-4]:26s} {'?':>4s} {'?':>4s} {'?':>13s}  KHÔNG KHỚP KHUÔN NÀO")
                continue
            so, t = int(b.group(1)), int(b.group(2))
            p, d = t, 0        # khuôn B: mọi ca đều là ca phá, không có ca đối chứng âm
            khuon = "B"
        if so != t:
            khong_dat.append(f"{f[:-4]} ({so}/{t})")
        print(f"{f[:-4]:26s} {t:>4d} {p:>4d} {d:>13d}  {khuon}")
        tong += t
        pha += p
        dc += d

    print("-" * 74)
    print(f"TỔNG: {tong} ca = {pha} ca PHÁ bị cổng bắt + {dc} ca ĐỐI CHỨNG ÂM (cổng im đúng)")
    print(f"script đọc được: {len(logs) - len(khong_khop)}/{len(logs)}")
    if khong_khop:
        print(f"  !!! KHÔNG KHỚP KHUÔN (số của chúng KHÔNG được tính vào tổng trên): {khong_khop}")
    if khong_dat:
        print(f"  !!! CÓ CA KHÔNG ĐẠT: {khong_dat}")

    # Mã thoát phản ánh ĐỘ TIN CẬY CỦA PHÉP ĐẾM, không phải "có lỗi trong sản phẩm".
    # Người đọc phải phân biệt được "đếm xong, sạch" với "đếm thiếu một phần".
    day_du = not khong_khop and not khong_dat

    if duong_json:
        p = duong_json if os.path.isabs(duong_json) else os.path.join(REPO, duong_json)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        commit = head_repo()
        payload = {
            "tong": tong, "pha": pha, "doi_chung_am": dc,
            "so_script": len(logs), "so_script_doc_duoc": len(logs) - len(khong_khop),
            "khong_khop": khong_khop, "khong_dat": khong_dat,
            "day_du": day_du,          # False = số ở trên KHÔNG đáng tin, đừng chép đi đâu cả
            "commit": commit,           # None = không xác định được bản mã đã đếm
            "luc": datetime.now().isoformat(timespec="seconds"),
            "thu_muc_log": os.path.abspath(thu_muc),
        }
        io.open(p, "w", encoding="utf-8").write(
            json.dumps(payload, ensure_ascii=False, indent=1) + "\n")
        print(f"✓ đã ghi số đo -> {p} (day_du={day_du} · commit={commit})")
        if commit is None:
            print("  !!! không đọc được commit của repo — nơi đọc số này sẽ coi là THIẾU, không đoán")

    return 0 if day_du else 1


if __name__ == "__main__":
    sys.exit(main())
