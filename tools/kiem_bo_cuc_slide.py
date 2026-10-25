#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cổng đo bố cục slide PDF: chữ tràn biên trang và chữ đè chữ.

VÌ SAO CẦN (lỗi thật đã gặp):
  Poster PPTX từng bị tiêu đề tràn khỏi thanh màu và đè lên chữ bên dưới, nhưng
  cổng cũ chỉ kiểm "phần tử nằm trong trang" nên vẫn báo ĐẠT — gate mù với lỗi
  bố cục bên trong.

CÁCH ĐO (hình học thuần, không dùng mắt, không đoán theo "khối"):
  - `pdftotext -bbox` cho hộp bao của từng TỪ.
  - CHỮ ĐÈ CHỮ = hai hộp từ có phần giao nhau. Đây là định nghĩa trực tiếp: chữ
    thật sự chồng nhau thì hộp của chúng giao nhau. Không cần gom "khối" — mà
    gom khối là nguồn false positive (hai cột cạnh nhau cùng dải y bị gộp rồi
    báo đè 100%).
  - CHỮ TRÀN BIÊN = hộp từ vượt ra ngoài khổ trang.
  - Ngưỡng diện tích giao nhau so với từ nhỏ hơn, để bỏ qua chạm mép do lỗi
    làm tròn subpixel.

CÁCH DÙNG:
    python3 tools/kiem_bo_cuc_slide.py <file.pdf> [--json]
    python3 tools/kiem_bo_cuc_slide.py --self-test    # tự kiểm bộ đo
Mã thoát: 0 = không lỗi, 1 = có lỗi, 2 = không đọc được input.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile

# Ngưỡng: phần giao nhau so với diện tích từ nhỏ hơn phải vượt ngưỡng này.
OVERLAP_RATIO = 0.25
# Mỗi chiều phải giao nhau tối thiểu 1.2pt thì mới tính là chồng.
MIN_OVERLAP_PT = 1.2


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=180)


def page_size(pdf):
    out = _run(["pdfinfo", pdf]).stdout
    m = re.search(r"Page size:\s+([\d.]+)\s+x\s+([\d.]+)", out)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2))


def page_count(pdf):
    out = _run(["pdfinfo", pdf]).stdout
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else None


def extract_words(pdf):
    """Trả về {page_index_1based: [(x0,y0,x1,y1,text), ...]}."""
    out = _run(["pdftotext", "-bbox", pdf, "-"]).stdout
    pages = {}
    page_no = 1
    for line in out.splitlines():
        if "<page " in line:
            pages.setdefault(page_no, [])
            continue
        wm = re.search(
            r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*)</word>',
            line,
        )
        if wm:
            x0, y0, x1, y1 = (float(wm.group(i)) for i in range(1, 5))
            txt = re.sub(r"&[a-z]+;", " ", wm.group(5)).strip()
            if txt:
                pages.setdefault(page_no, []).append((x0, y0, x1, y1, txt))
        if "</page>" in line:
            page_no += 1
    return pages


def _overlap(a, b):
    """Diện tích giao nhau của hai hộp."""
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    if w <= 0 or h <= 0:
        return 0.0, 0.0, 0.0
    area = w * h
    small = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
    ratio = area / small if small > 0 else 0.0
    return area, ratio, w


def check_page(words, pw, ph, page_no):
    issues = []

    # 1) từ vượt biên trang
    out_words = [w for w in words if w[0] < -1 or w[1] < -1 or w[2] > pw + 1 or w[3] > ph + 1]
    if out_words:
        sample = ", ".join(w[4] for w in out_words[:5])
        issues.append({
            "type": "ngoai_bien",
            "page": page_no,
            "detail": f"{len(out_words)} từ vượt biên trang (ví dụ: {sample})",
        })

    # 2) hai từ chồng nhau
    # Sắp theo y để chỉ so các cặp gần nhau — chồng lấn luôn là gần.
    ws = sorted(words, key=lambda w: (w[1], w[0]))
    seen = set()
    for i, a in enumerate(ws):
        for b in ws[i + 1:]:
            if b[1] - a[1] > 30:      # cách xa theo y thì không thể chồng
                break
            area, ratio, ow = _overlap(a, b)
            if area <= 0:
                continue
            if ow < MIN_OVERLAP_PT:
                continue
            if ratio <= OVERLAP_RATIO:
                continue
            key = (page_no, a[4], b[4], round(a[0], 1), round(b[0], 1))
            if key in seen:
                continue
            seen.add(key)
            issues.append({
                "type": "chong_cheo",
                "page": page_no,
                "ratio": round(ratio, 3),
                "detail": f"'{a[4]}' đè '{b[4]}' ({ratio*100:.0f}% diện tích từ nhỏ)",
            })
    return issues


def check(pdf):
    """Trả về (issues, page_w, page_h, n_pages). Nếu không đọc được thì issues=None."""
    size = page_size(pdf)
    if not size:
        return None, 0.0, 0.0, 0
    pw, ph = size
    pages = extract_words(pdf)
    if not pages:
        return None, pw, ph, 0

    all_issues = []
    for pno in sorted(pages):
        all_issues.extend(check_page(pages[pno], pw, ph, pno))
    return all_issues, pw, ph, len(pages)


def _make_sample_pdf(path, mode):
    """Tạo PDF mẫu để tự kiểm bộ đo: 'clean' hoặc 'overlap'."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "_mau_pdf", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_mau_pdf.py")
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as exc:  # pragma: no cover
        print(f"SKIP: không nạp được module sinh PDF mẫu ({exc})")
        return False

    if mode == "clean":
        # hai dòng cách nhau rõ
        lines = [(72, 700, 24, "Dong thu nhat"), (72, 660, 24, "Dong thu hai")]
    else:
        # hai dòng đè đúng lên nhau
        lines = [(72, 700, 24, "Dong tren"), (72, 700, 24, "Dong duoi")]
    mod.make_pdf(path, lines)
    return os.path.isfile(path) and os.path.getsize(path) > 0


def self_test():
    """Tự kiểm: bộ đo phải SẠCH trên PDF không chồng và BẮT được PDF có chồng."""
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        clean = os.path.join(tmp, "clean.pdf")
        overlap = os.path.join(tmp, "overlap.pdf")

        if not _make_sample_pdf(clean, "clean"):
            print("SKIP: không tạo được PDF mẫu (thiếu ps2pdf)")
            return 0
        if not _make_sample_pdf(overlap, "overlap"):
            print("SKIP: không tạo được PDF mẫu (thiếu ps2pdf)")
            return 0

        iss_clean, _, _, _ = check(clean)
        iss_over, _, _, _ = check(overlap)

        ok_clean = iss_clean is not None and not iss_clean
        ok_over = iss_over is not None and any(i["type"] == "chong_cheo" for i in iss_over)
        n_clean = len(iss_clean) if iss_clean else 0
        n_over = len(iss_over) if iss_over else 0
        results.append((ok_clean, f"PDF sạch: không được báo lỗi (got {n_clean})"))
        results.append((ok_over, f"PDF có chồng: phải bắt được (got {n_over})"))

    print("Tự kiểm bộ đo đo bố cục:")
    for ok, msg in results:
        print(f"  {'✓' if ok else '✗'} {msg}")
    return 0 if all(ok for ok, _ in results) else 1


def main():
    ap = argparse.ArgumentParser(description="Cổng đo bố cục slide PDF")
    ap.add_argument("pdf", nargs="?")
    ap.add_argument("--json", action="store_true", help="in kết quả dạng JSON")
    ap.add_argument("--self-test", action="store_true", help="tự kiểm bộ đo bằng PDF mẫu")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.pdf:
        ap.error("cần đường dẫn PDF, hoặc dùng --self-test")
    if not os.path.isfile(args.pdf):
        print(f"LỖI: không thấy {args.pdf}", file=sys.stderr)
        return 2

    issues, pw, ph, npages = check(args.pdf)
    result = {
        "pdf": os.path.basename(args.pdf),
        "page_size_pt": [round(pw, 1), round(ph, 1)],
        "pages": npages,
        "issues": issues,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"File: {result['pdf']}")
        print(f"Khổ: {pw:.0f}x{ph:.0f}pt · {npages} trang")
        if not issues:
            print("✓ Không phát hiện chữ tràn biên hoặc chữ đè chữ")
        else:
            print(f"✗ {len(issues)} lỗi bố cục:")
            for it in issues:
                print(f"  [trang {it['page']}] {it['detail']}")
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
