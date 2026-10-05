#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh data/yccd.js cho app SOI AI từ nguồn ĐÃ VERIFY.

Nguồn vào:
  * ~/ieeai2026/yccd_lop10_sach.json  — 22 YCCĐ lớp 10, đã verify 22/22 bằng
    tools/verify_yccd.py (subsequence + ô đặc hiệu nhất + từ khoá + tập mã).
  * Tên 13 chủ đề: chép NGUYÊN VĂN từ Khung 2422 (đã đọc trực tiếp ở offset 36509
    của 2422_PL_khung.txt).

KHÔNG được sửa tay nội dung YCCĐ trong file sinh ra — sửa ở nguồn rồi sinh lại.
"""
import json, os, re, sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(_ROOT, "data-source", "yccd_lop10_sach.json")
OUT = os.path.join(_ROOT, "data", "yccd.js")

# 13 chủ đề — NGUYÊN VĂN Khung 2422 (phụ lục, mục danh mục chủ đề)
CHU_DE = {
    "A1": "Tính chủ động của con người",
    "A2": "AI vì sự tiến bộ của con người",
    "A3": "Công dân trong kỉ nguyên AI",
    "B1": "Các khía cạnh đạo đức của AI",
    "B2": "Sử dụng AI an toàn và có trách nhiệm",
    "B3": "Nguyên tắc đạo đức và trách nhiệm xã hội",
    "C1": "Đặc điểm chính của AI",
    "C2": "Ứng dụng AI trong học tập và cuộc sống",
    "C3": "Công nghệ AI",
    "C4": "Dữ liệu trong AI",
    "C5": "Kĩ thuật và thuật toán AI",
    "D1": "Nhận diện và hình thành giải pháp",
    "D2": "Cấu trúc và tương tác, cải tiến hệ thống",
}
MACH = {
    "A": "Tư duy lấy con người làm trung tâm",
    "B": "Đạo đức AI",
    "C": "Các kĩ thuật và ứng dụng AI",
    "D": "Thiết kế hệ thống AI",
}
# UNESCO AI CFS 2024 chỉ để ĐỐI CHIẾU (4 aspects × 3 levels), không phải trục chính
UNESCO = {
    "A1": "A1", "A2": "A2", "A3": "A3",
    "B1": "B1", "B2": "B2", "B3": "B3",
    "C1": "C1", "C2": "C2", "C3": "C3", "C4": "D1", "C5": "D2",
    "D1": "D1", "D2": "D2",
}


def main():
    yc = json.load(open(SRC))
    if len(yc) != 22:
        print(f"❌ nguồn có {len(yc)} YCCĐ, kì vọng 22", file=sys.stderr); return 1
    bad = [r["ma"] for r in yc if not r.get("verify", {}).get("dat")]
    if bad:
        print(f"❌ nguồn có YCCĐ chưa đạt verify: {bad}", file=sys.stderr); return 1

    # gom theo chủ đề
    theo_cd = {}
    for r in yc:
        theo_cd.setdefault(r["chuDe"], []).append(r)

    lines = [
        "/* SOI AI — dữ liệu 13 chủ đề + 22 yêu cầu cần đạt (YCCĐ) của LỚP 10.",
        " * NGUỒN: Khung nội dung giáo dục Trí tuệ nhân tạo cho học sinh phổ thông,",
        " *        ban hành kèm QĐ 2422/QĐ-BGDĐT ngày 18/8/2026 (phụ lục, lớp 10).",
        " * Nội dung YCCĐ là NGUYÊN VĂN, đã verify tự động bằng tools/verify_yccd.py",
        " * (22/22 đạt: subsequence đầy đủ + ô đặc hiệu nhất + từ khoá + tập mã).",
        " * KHÔNG sửa tay file này — sửa nguồn rồi sinh lại bằng tools/gen_yccd_js.py.",
        " *",
        " * Trục năng lực CHÍNH của app là 13 chủ đề của Bộ (mã [lớp].[chủ đề].[thứ tự]).",
        " * UNESCO AI CFS 2024 chỉ là cột ĐỐI CHIẾU phụ.",
        " */",
        "window.MX_YCCD = {",
        '  nguon: "QĐ 2422/QĐ-BGDĐT (18/8/2026) — Khung nội dung giáo dục AI cho HS phổ thông, lớp 10",',
        '  lop: 10,',
        '  daVerify: "22/22 YCCĐ — tools/verify_yccd.py",',
        "",
        "  /* 4 mạch nội dung (nguyên văn) */",
        "  mach: " + json.dumps(MACH, ensure_ascii=False, indent=4).replace("\n", "\n  ") + ",",
        "",
        "  /* 13 chủ đề thành phần (nguyên văn). Lớp 10 có YCCĐ ở 10/13 chủ đề:",
        "     B1, C1, C5 không có YCCĐ lớp 10 trong Khung. */",
        "  chuDe: " + json.dumps(CHU_DE, ensure_ascii=False, indent=4).replace("\n", "\n  ") + ",",
        "",
        "  /* Đối chiếu UNESCO AI Competency Framework for Students (2024) — PHỤ */",
        "  unescoDoiChieu: " + json.dumps(UNESCO, ensure_ascii=False) + ",",
        "",
        "  /* 22 YCCĐ lớp 10 — nguyên văn */",
        "  danhSach: [",
    ]
    for r in yc:
        lines.append("    {")
        lines.append(f'      ma: "{r["ma"]}",')
        lines.append(f'      chuDe: "{r["chuDe"]}",')
        lines.append(f'      mach: "{r["chuDe"][0]}",')
        lines.append(f'      loai: "{r["loai"]}",')
        txt = r["text"].replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'      text: "{txt}",')
        v = r["verify"]
        lines.append(f'      verify: {{ subseq: "{v["subseq"]}", tuKhoa: "{v["tuKhoa"]}" }},')
        lines.append("    },")
    lines += [
        "  ],",
        "",
        "  /* Chủ đề KHÔNG có YCCĐ lớp 10 — app vẫn hiện để HS thấy toàn cảnh 13 chủ đề */",
        '  khongCoLop10: ["B1", "C1", "C5"],',
        "",
        "  /* Tra cứu nhanh theo mã */",
        "  lay(ma){ return this.danhSach.find(x => x.ma === ma) || null; },",
        "  theoChuDe(cd){ return this.danhSach.filter(x => x.chuDe === cd); },",
        "  tenChuDe(cd){ return this.chuDe[cd] || cd; },",
        "};",
        "",
    ]
    open(OUT, "w").write("\n".join(lines))

    # self-check: file sinh ra phải parse được như JS object và đủ 22
    node = __import__("subprocess").run(
        ["node", "-e",
         "global.window={};require('" + OUT + "');"
         "const d=window.MX_YCCD;"
         "console.log(JSON.stringify({soYCCD:d.danhSach.length,soChuDe:Object.keys(d.chuDe).length,"
         "mach:Object.keys(d.mach).length,"
         "chuDeCoYCCD:new Set(d.danhSach.map(x=>x.chuDe)).size,"
         "maMau:d.danhSach[0].ma,txtMau:d.danhSach[0].text.slice(0,60),"
         "c41:d.lay('10.C4.1').text,d22:d.lay('10.D2.2').text.slice(0,50),"
         "bm:d.lay('10.B2.MR1').text.slice(0,50)}))"],
        capture_output=True, text=True)
    print("node self-check:", node.stdout.strip() or node.stderr[:400])
    if node.returncode != 0:
        print("❌ file sinh ra không parse được", file=sys.stderr); return 1

    j = json.loads(node.stdout.strip())
    ok = (j["soYCCD"] == 22 and j["soChuDe"] == 13 and j["mach"] == 4
          and j["chuDeCoYCCD"] == 10
          and j["c41"] == "Phân tích được sự ảnh hưởng của chất lượng dữ liệu đến chất lượng AI.")
    print("KIỂM TRA:", "ĐẠT" if ok else "❌ LỆCH", "|", json.dumps(j, ensure_ascii=False)[:300])
    print(f"Đã ghi → {OUT}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
