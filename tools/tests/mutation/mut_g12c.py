#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION CA 3 cho cổng G12c — chứng minh cổng có răng với KHOẢN NỢ NỘI DUNG.

VÌ SAO PHẢI CÓ TỆP RIÊNG: bản đầu viết trong heredoc và chết ngay lúc compile vì
`SyntaxError: f-string expression part cannot include a backslash` — nghĩa là KHÔNG DÒNG NÀO
CHẠY, tệp không bị sửa, và phép "đo lại tỉ lệ nợ" in ra đúng con số cũ. Kết luận rút ra từ
lần chạy đó (cổng im = cổng mù) là SAI HOÀN TOÀN: chưa phá gì thì dĩ nhiên cổng không kêu.
Một phép kiểm không chạy thì không có kết quả, và kết quả rỗng không phải kết quả tốt.

NEO ĐƯỢC CHỌN SAO (đọc từ mã thật, không đoán):
  js/tinhhuong.js dòng ~154 là câu DUY NHẤT trong tệp mà đáp án KHÔNG phải phương án dài
  nhất (dapAn="d" dài 63 ký tự, trong khi phương án "b" dài 98 ký tự). Nối dài phương án
  "d" sẽ LẬT câu đó từ "không nợ" thành "có nợ", đẩy tỉ lệ 29/35 -> 30/35 = 85,7%,
  vượt mốc 82,9% + dung sai 1,0 = 83,9% -> G12c phải kêu.
  Bản đầu của ca này nối dài một phương án ĐÃ là dài nhất, nên tỉ lệ không đổi: phép phá
  là no-op. Đó là lỗi neo, cùng họ với vụ neo `((dungNhom && duBa) ? ...)` không tồn tại.

Script tự kiểm: sau khi phá phải ĐO LẠI tỉ lệ và đòi nó THẬT SỰ tăng, rồi mới chạy cổng.
Nếu tỉ lệ không tăng thì dừng và báo "phép phá là no-op" — không chạy cổng để rồi kết luận sai.
"""
import hashlib
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TEP = "js/tinhhuong.js"
P = os.path.join(ROOT, TEP)
MOC = 82.9
DUNGSAI = 1.0

RE_BLOCK = re.compile(r"luaChon\s*:\s*\[(.*?)\]", re.S)
RE_ITEM = re.compile(r'\{\s*id\s*:\s*"([a-e])"\s*,\s*text\s*:\s*"((?:[^"\\]|\\.)*)"')
RE_DAP = re.compile(r'dapAn\s*:\s*"([a-e])"')

NGUON = ("js/tinhhuong.js", "js/lab.js", "js/nhamay_tram01.js",
         "data/bai5_logic.js", "data/kienthuc.js")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def do_no():
    """Đo tỉ lệ 'đáp án là phương án dài nhất' bằng ĐÚNG phép của cổng G12c."""
    tong = no = 0
    for rel in NGUON:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        if "luaChon" not in s:
            continue
        for m in RE_BLOCK.finditer(s):
            items = RE_ITEM.findall(m.group(1))
            if len(items) < 2:
                continue
            dm = RE_DAP.search(s[m.end():m.end() + 900])
            if not dm:
                continue
            dap = dm.group(1)
            if dap not in [k for k, _ in items]:
                continue
            dai = max(items, key=lambda x: len(x[1]))[0]
            tong += 1
            if dai == dap:
                no += 1
    return no, tong, (100.0 * no / tong if tong else None)


def chay_cong():
    r = subprocess.run(["python3", "tools/nghiem_thu.py"], cwd=ROOT,
                       capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr
    m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
    dong = [l for l in out.splitlines() if "G12c" in l]
    return r.returncode, (m.group(0) if m else "?"), (dong[0].strip() if dong else "")


def main():
    print("=" * 96)
    print("MUTATION CA 3 — G12c (khoản nợ nội dung phình ra thì cổng phải kêu)")
    print("=" * 96)

    h0 = sha(P)
    tmp = tempfile.mkdtemp(prefix="g12c-")
    bak = os.path.join(tmp, "tinhhuong.js")
    shutil.copy2(P, bak)
    no0, tong0, t0 = do_no()
    print(f"\n[TRƯỚC] nợ = {no0}/{tong0} = {t0:.1f}%  · ngưỡng fail = {MOC + DUNGSAI:.1f}%")
    print(f"        hash {TEP} = {h0[:16]}")

    # --- tìm câu mà đáp án KHÔNG phải phương án dài nhất ---
    s = io.open(P, encoding="utf-8").read()
    muc_tieu = None
    for m in RE_BLOCK.finditer(s):
        items = RE_ITEM.findall(m.group(1))
        if len(items) < 2:
            continue
        dm = RE_DAP.search(s[m.end():m.end() + 900])
        if not dm:
            continue
        dap = dm.group(1)
        d = {k: v for k, v in items}
        if dap not in d:
            continue
        dai = max(items, key=lambda x: len(x[1]))[0]
        if dai != dap:
            muc_tieu = (dap, dai, d[dap], len(d[dap]), len(d[dai]))
            break
    if not muc_tieu:
        print("\n!!! KHÔNG tìm được câu nào có đáp án không-phải-dài-nhất.")
        print("    Nghĩa là nợ đã 100% — không còn neo để phá. Dừng, không đoán.")
        return 2
    dap, dai, text_dap, ldap, ldai = muc_tieu
    print(f"\n[NEO] câu có dapAn='{dap}' (dài {ldap}) nhưng phương án dài nhất là '{dai}' (dài {ldai})")
    print(f"      text của '{dap}': {text_dap[:70]}...")

    # --- nối dài phương án đúng để LẬT câu này thành "nợ" ---
    neo = 'text:"' + text_dap + '"'
    if s.count(neo) != 1:
        print(f"\n!!! neo xuất hiện {s.count(neo)} lần (cần đúng 1). Dừng — không phá mù.")
        return 2
    # cần nối thêm bao nhiêu để vượt phương án dài nhất + biên an toàn
    them = (ldai - ldap) + 120
    moi = s.replace(neo, 'text:"' + text_dap + " " * them + '"', 1)
    assert moi != s, "thay thế không đổi được nội dung"
    io.open(P, "w", encoding="utf-8").write(moi)

    no1, tong1, t1 = do_no()
    print(f"\n[SAU KHI PHÁ] nợ = {no1}/{tong1} = {t1:.1f}%  (đã nối dài thêm {them} ký tự)")
    if t1 is None or t1 <= t0:
        print("!!! tỉ lệ nợ KHÔNG tăng — phép phá là NO-OP, chạy cổng lúc này sẽ cho kết luận sai.")
        shutil.copy2(bak, P)
        print(f"    đã khôi phục; hash khớp: {sha(P) == h0}")
        return 3
    print(f"    {t1:.1f}% > ngưỡng {MOC + DUNGSAI:.1f}% -> G12c PHẢI kêu")

    rc, ket, dong = chay_cong()
    keu = "[LỖI] G12c" in dong
    bat = (rc != 0 and keu)
    print(f"\n[KẾT QUẢ CỔNG] rc={rc} · {ket}")
    print(f"    {dong[:200]}")
    print(f"    -> {'BẮT ĐƯỢC' if bat else 'IM (KHÔNG RĂNG)'}")

    # --- khôi phục và xác nhận ---
    shutil.copy2(bak, P)
    khop = sha(P) == h0
    print(f"\n[KHÔI PHỤC] hash {TEP} {'KHỚP gốc' if khop else 'LỆCH !!!'}")
    if not khop:
        print("    !!! DỪNG: tệp không về nguyên trạng. Bản sao ở " + bak)
        return 9
    rc2, ket2, _ = chay_cong()
    print(f"[XÁC NHẬN CUỐI] rc={rc2} · {ket2}   (phải về ĐẠT: hai số bằng nhau)")
    shutil.rmtree(tmp)
    return 0 if (bat and khop and rc2 == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
