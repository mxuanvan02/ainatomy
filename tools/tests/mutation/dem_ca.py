#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đếm ca kiểm thử từ log của 12 script mutation — con số trong hồ sơ phải tái lập được.

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
    # chạy hết 12 script rồi đếm (làm một lệnh, không tự chạy hộ)
    cd soi-ai
    for b in tools/tests/mutation/*.py; do python3 "$b" > "/tmp/mut/$(basename $b .py).log" 2>&1; done
    python3 tools/tests/mutation/dem_ca.py /tmp/mut

Tệp này KHÔNG tự chạy script nào: nó chỉ đọc log. Chạy hộ thì nó lại thành một công cụ sửa tệp
repo mà người gọi không biết, và mỗi script mutation cần cây sạch trước khi bắt đầu.
"""
import io
import os
import re
import sys

# Khuôn A: bắt buộc có cả nhóm tách hai loại. Đây là khuôn CHUẨN.
KA = re.compile(r"KẾT LUẬN: (\d+)/(\d+) ca đúng như kỳ vọng "
                r"\((\d+) ca PHÁ bị cổng bắt \+ (\d+) ca ĐỐI CHỨNG ÂM")
# Khuôn B: chỉ dùng cho script mà MỌI ca đều là ca phá. Cố ý hẹp.
KB = re.compile(r"KẾT LUẬN: (\d+)/(\d+) ca phá [^\n]*")


def main():
    if len(sys.argv) < 2:
        print("dùng: python3 dem_ca.py <thư_mục chứa log các script mutation>")
        return 2
    thu_muc = sys.argv[1]
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
    return 0 if (not khong_khop and not khong_dat) else 1


if __name__ == "__main__":
    sys.exit(main())
