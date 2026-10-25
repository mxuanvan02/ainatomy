#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render poster A0 iEEAI 2026 từ HTML sang PDF bằng Chrome headless.

VÌ SAO LÀ HTML CHỨ KHÔNG PHẢI PPTX (lỗi thật đã gặp):
  - Bản PPTX đặt textbox tuyệt đối; khi font thay đổi, chữ tràn khỏi thanh tiêu đề
    và đè lên nhau. Cổng cũ chỉ kiểm "nằm trong trang" nên vẫn báo ĐẠT — gate không
    bắt được lỗi thật.
  - Bản LaTeX tikzposter dựng lại từ đầu nên sai bố cục mẫu BTC.
  - HTML/CSS để trình duyệt tự dàn layout, và đo được bounding box thật của từng
    phần tử để kiểm chồng lấn/cắt chữ một cách xác định.

Đường dẫn suy từ vị trí tệp này, không ghi cứng /home/<user>.

Cách dùng:
    python3 tools/render_poster.py            # render + kiểm
    python3 tools/render_poster.py --check    # chỉ kiểm PDF đã có
"""
import argparse
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTER_DIR = os.path.join(ROOT, "deliverables", "poster")
HTML = os.path.join(POSTER_DIR, "poster.html")
PDF = os.path.join(POSTER_DIR, "poster_A0.pdf")

# A0 dọc: 841 x 1189 mm = 2383.94 x 3370.39 pt. Dung sai 2pt.
A0_W_PT = 2383.94
A0_H_PT = 3370.39
TOL_PT = 2.0


def _find_chrome():
    for name in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        path = shutil.which(name)
        if path:
            return path
    return None


def render():
    chrome = _find_chrome()
    if not chrome:
        print("LỖI: không tìm thấy Chrome/Chromium để render.", file=sys.stderr)
        return 1
    if not os.path.isfile(HTML):
        print(f"LỖI: không thấy {HTML}", file=sys.stderr)
        return 1
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",
        "--no-margins",
        f"--print-to-pdf={PDF}",
        f"file://{HTML}",
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    if r.returncode != 0 or not os.path.isfile(PDF):
        print("LỖI render:", r.stderr[-800:], file=sys.stderr)
        return 1
    return 0


def check():
    """Kiểm xác định: đúng 1 trang, đúng khổ A0."""
    try:
        out = subprocess.run(
            ["pdfinfo", PDF], capture_output=True, text=True, timeout=60
        ).stdout
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"LỖI: không chạy được pdfinfo ({exc})", file=sys.stderr)
        return 1

    pages = None
    width = height = None
    for line in out.splitlines():
        if line.startswith("Pages:"):
            pages = int(line.split(":", 1)[1].strip())
        elif line.startswith("Page size:"):
            parts = line.split(":", 1)[1].split()
            width, height = float(parts[0]), float(parts[2])

    ok = True
    if pages != 1:
        print(f"✗ Số trang = {pages}, phải là 1")
        ok = False
    else:
        print("✓ 1 trang")
    if width is None or height is None:
        print("✗ Không đọc được khổ giấy")
        return 1
    if abs(width - A0_W_PT) > TOL_PT or abs(height - A0_H_PT) > TOL_PT:
        print(f"✗ Khổ {width:.1f}x{height:.1f}pt, phải là A0 {A0_W_PT}x{A0_H_PT}pt")
        ok = False
    else:
        print(f"✓ Khổ A0 ({width:.0f}x{height:.0f}pt)")
    size_mb = os.path.getsize(PDF) / (1024 * 1024)
    if size_mb > 100:
        print(f"✗ Dung lượng {size_mb:.1f}MB vượt 100MB")
        ok = False
    else:
        print(f"✓ Dung lượng {size_mb:.2f}MB (giới hạn 100MB)")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Render poster A0 iEEAI từ HTML")
    ap.add_argument("--check", action="store_true", help="chỉ kiểm PDF đã có")
    args = ap.parse_args()

    if not args.check:
        if render() != 0:
            return 1
        print(f"✓ Đã render {os.path.relpath(PDF, ROOT)}")
    if not os.path.isfile(PDF):
        print(f"LỖI: chưa có {os.path.relpath(PDF, ROOT)}", file=sys.stderr)
        return 1
    return check()


if __name__ == "__main__":
    sys.exit(main())
