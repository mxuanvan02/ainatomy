#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Đổi tên sản phẩm MỔ XẺ AI -> SOI AI trong repo soi-ai (46 chỗ).

Lý do dùng script thay vì patch từng chỗ: tên cũ xuất hiện ở cả comment đầu file,
chuỗi hiển thị cho học sinh, README và đường dẫn thư mục — đổi lẻ dễ sót.
Script này báo cáo TỪNG chỗ đã đổi để đối chiếu, và KHÔNG đụng vendor/three
(thư viện bên thứ ba) để giữ nguyên giấy phép gốc.

Các phép thay:
  "MỔ XẺ AI"  -> "SOI AI"          (tên sản phẩm, cả trong chuỗi hiển thị)
  "MỔ XẺ"     -> "SOI"             (logo tách chữ: 🔬 MỔ XẺ <span>AI</span>)
  "moxe-ai"   -> "soi-ai"          (đường dẫn thư mục trong README)
  "moxeai"    -> "soiai"           (phòng hờ)
"""
import re, sys, pathlib

ROOT = pathlib.Path("/home/hitokiri/ieeai2026/soi-ai")
SKIP_DIRS = {"vendor", ".git", "node_modules"}
EXT = {".js", ".html", ".css", ".md", ".json", ".txt"}

RULES = [
    ("MỔ XẺ AI", "SOI AI"),
    ("Mổ Xẻ AI", "Soi AI"),
    ("MỔ XẺ", "SOI"),
    ("moxe-ai", "soi-ai"),
    ("moxeai", "soiai"),
    ("MoXeAI", "SoiAI"),
]


def main():
    tong = 0
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXT:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        try:
            src = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            print(f"[bỏ qua] {p.relative_to(ROOT)}: {e}")
            continue

        out, hits = src, []
        for old, new in RULES:
            c = out.count(old)
            if c:
                out = out.replace(old, new)
                hits.append(f"{old}->{new} ×{c}")
        if out != src:
            p.write_text(out, encoding="utf-8")
            n = sum(int(re.search(r'×(\d+)$', h).group(1)) for h in hits)
            tong += n
            print(f"[ĐỔI {n:2d}] {str(p.relative_to(ROOT)):34s} {'; '.join(hits)}")

    print(f"\nTổng số chỗ đã đổi: {tong}")

    # ---- verify: không còn tên cũ ở đâu ngoài vendor ----
    con = []
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXT:
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        for old, _ in RULES:
            if old in t:
                con.append((str(p.relative_to(ROOT)), old))
    if con:
        print("\n❌ VẪN CÒN TÊN CŨ:")
        for c in con:
            print("   ", c)
        return 1
    print("✅ VERIFY: không còn 'MỔ XẺ'/'moxe-ai' trong mã nguồn (vendor giữ nguyên)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
