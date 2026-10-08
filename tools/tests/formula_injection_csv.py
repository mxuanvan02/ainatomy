#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""TEST FORMULA INJECTION cho đường xuất CSV của app (js/engine.js xuatCSV).

VÌ SAO CÓ TỆP NÀY. `ma_hs`/`ma_lop` là văn bản tự do học sinh gõ (app.js dangNhap chỉ
trim + uppercase). Bản engine.js trước 08/10 chỉ thoát `" , \n` khi serialize CSV, nên
HS gõ `=SUM(A1:A9)` hay `+1+1` làm mã của mình thì chuỗi đó đi TRẦN vào ô CSV, và
Excel/LibreOffice THỰC THI ô bắt đầu bằng = + - @ khi giáo viên mở tệp. Lỗ này đã được
ĐO THẬT bằng app sống qua browser trước khi vá (payload vào nguyên văn cột 1-2), không
phát hiện bằng suy luận. Bản vá thêm prefix `'` (OWASP CSV injection) — chỉ khi ô không
phải số hợp lệ, để `-1` ở cột điểm không bị phá.

CÁCH THỬ — bốc serializer THẬT từ js/engine.js, chạy bằng node. Không chép logic vào
đây rồi thử bản chép: bản sao thì luôn khớp, đúng lớp lỗi "ĐẠT GIẢ" mà repo này đã trả
giá (G11b, G14a). Nếu ai đó sửa serializer cho lỏng ra, phép thử này kêu.

MỤC D — ĐỐI CHỨNG ÂM: chạy chính bộ kiểm này trên serializer BẢN CŨ (trích từ git),
nó PHẢI fail. Một phép kiểm chưa từng FAIL thì chưa chứng minh được nó CÓ THỂ fail
(Luật C/5v, skill agentic-efficiency-loop).

CÁCH CHẠY:  python3 tools/tests/formula_injection_csv.py    (cần node; thoát 2 nếu thiếu)
"""
import io
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENGINE = os.path.join(ROOT, "js", "engine.js")

# Payload: 4 ký tự mở đầu mà Excel/LibreOffice coi là formula (OWASP), + 2 đối chứng.
PAYLOADS = [
    ("formula =",      "=SUM(A1:A9)"),
    ("formula +",      "+1+1"),
    ("formula @",      "@SUM(A1:A2)"),
    ("HYPERLINK",      '=HYPERLINK("http://evil.example","bam")'),
    ("số âm (PHẢI lọt nguyên — đây là dữ liệu thật)", "-1"),
    ("mã sạch (PHẢI lọt nguyên)", "A001"),
]

def boc_serializer(js_src):
    """Bốc NGUYÊN VĂN khối map(...) serialize ô từ xuatCSV của engine.js.

    Khoá vào chữ ký `return rows.map(r => r.map(x => {` — nếu cấu trúc đổi thì
    hàm này KÊU thay vì âm thầm thử một khúc khác.
    """
    m = re.search(r"return rows\.map\(r => r\.map\(x => \{.*?\}\)\.join\(\",\"\)\)\.join\(\"\\n\"\);",
                  js_src, re.S)
    if not m:
        raise SystemExit("!!! không định vị được serializer `return rows.map(...)` trong "
                         "js/engine.js — xuatCSV đã đổi cấu trúc? Sửa hàm boc_serializer.")
    return m.group(0)

def chay_node(serializer, rows):
    """Chạy serializer thật bằng node với `rows` cho trước, trả về chuỗi CSV."""
    script = ("function xuat(rows){\n  " + serializer + "\n}\n"
              + "console.log(xuat(" + json.dumps(rows) + "));")
    tmp = tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8")
    tmp.write(script)
    tmp.close()
    r = subprocess.run(["node", tmp.name], capture_output=True, text=True, timeout=60)
    os.unlink(tmp.name)
    if r.returncode != 0:
        raise SystemExit(f"!!! chạy serializer bằng node thất bại: {r.stderr.strip()[:300]}")
    return r.stdout.rstrip("\n")

def o_con_song(o):
    """Ô CSV còn là formula sống không: bắt đầu bằng = + - @ sau khi bóc nháy kép."""
    return bool(re.match(r'^"?[=+\-@]', o)) and not o.startswith("'\"") and not o.startswith("''")

def kiem(serializer, ten_ban):
    """Chạy đủ ca trên một bản serializer, trả về (danh sách lỗi, danh sách dòng in)."""
    loi, log = [], []
    for ten, payload in PAYLOADS:
        chuoi_csv = chay_node(serializer, [[payload, "X"]])
        o = chuoi_csv.split(",")[0]
        la_so = payload != "" and _la_so(payload)
        if la_so:
            # ĐỐI CHỨNG DƯƠNG TÍNH: số hợp lệ (kể cả âm) PHẢI giữ nguyên — prefix nó
            # là phá dữ liệu thật của giáo viên.
            tot = (o == payload)
            if not tot:
                loi.append(f"{ten}: ô bị đổi thành {o!r} (phải nguyên {payload!r})")
            log.append(f"  {'OK  ' if tot else '<<< HỞ'} {ten:46s} -> {o!r}")
        else:
            tot = not o_con_song(o)
            if not tot:
                loi.append(f"{ten}: payload đi TRẦN vào ô {o!r} — Excel sẽ thực thi")
            log.append(f"  {'OK  ' if tot else '<<< HỞ'} {ten:46s} -> {o!r}")
    return loi, log

def _la_so(s):
    try:
        f = float(s)
        return f == f and abs(f) != float("inf")
    except ValueError:
        return False

def main():
    if subprocess.run(["node", "--version"], capture_output=True).returncode != 0:
        print("!!! không có `node` — KHÔNG thử được serializer thật. Thoát 2 chứ không "
              "trả 0: phép kiểm không chạy được mà vẫn báo sạch là phép kiểm vô hiệu (Luật 5d).")
        return 2

    js_src = io.open(ENGINE, encoding="utf-8").read()
    serializer = boc_serializer(js_src)
    print("=" * 92)
    print("TEST FORMULA INJECTION — chạy serializer THẬT bốc từ js/engine.js xuatCSV")
    print("=" * 92)

    # --- A. bản hiện hành PHẢI sạch ---
    loi, log = kiem(serializer, "hiện hành")
    print("\n--- A. bản hiện hành ---")
    print("\n".join(log))

    # --- B. ĐỐI CHỨNG ÂM: bản cũ (không prefix formula) PHẢI bị bắt ---
    # Dựng lại serializer bản cũ từ chính bản hiện hành: xoá dòng prefix `const t = …`
    # và đổi tham chiếu `t` về `s`. Nếu dòng đó không tồn tại thì bản vá đã bị gỡ và
    # mục A cũng đã fail. Dùng lambda thay chuỗi trong re.sub: chuỗi thay thế chứa
    # `\n` của regex JS mà re.sub sẽ diễn giải thành newline thật nếu truyền thẳng
    # (lỗi đã gặp lần chạy đầu — JS nhận regex gãy dòng, SyntaxError).
    REPL = ('\n      return /[",\\n]/.test(s) ? \'"\' + s.replace(/"/g,\'""\') + \'"\' : s;')
    ban_cu = re.sub(r"\s*const t = .*?;\n\s*return /\[\",\\n\]/\.test\(t\)[^\n]*",
                    lambda m: REPL, serializer, flags=re.S)
    print("\n--- B. đối chứng âm: bộ kiểm này CÓ THỂ fail không? (serializer bản cũ) ---")
    if ban_cu == serializer:
        print("  !!! không dựng được bản cũ từ bản hiện hành — dòng prefix `const t =` "
              "không còn? Bộ kiểm mất đối chứng.")
        loi.append("đối chứng âm: không dựng được serializer bản cũ")
    else:
        loi_cu, log_cu = kiem(ban_cu, "cũ")
        bat = sum(1 for l in loi_cu if l)
        print(f"  {'OK  ' if bat >= 3 else '<<<'} bản cũ bị bắt {bat} ca (phải ≥3: =, +, @) — "
              "bộ kiểm CÓ RĂNG")
        for l in log_cu:
            if "<<<" in l:
                print("    bắt được:" + l[2:])
        if bat < 3:
            loi.append(f"đối chứng âm: bản cũ chỉ bị bắt {bat} ca, bộ kiểm chưa đủ răng")

    print("\n" + "=" * 92)
    if loi:
        print(f"LỖI — {len(loi)} vấn đề:")
        for l in loi:
            print("  !", l)
        return 1
    print("OK — serializer thật của engine.js chặn formula injection, GIỮ NGUYÊN số hợp lệ,")
    print("     và bộ kiểm này đã được chứng minh là kêu được trên bản cũ.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
