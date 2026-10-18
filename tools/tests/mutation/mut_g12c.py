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
import ast
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
CONG = os.path.join(ROOT, "tools", "nghiem_thu.py")

# ĐỌC MỐC TỪ MÃ CỔNG LÚC CHẠY, KHÔNG CHÉP SỐ VÀO ĐÂY.
# LỖI THẬT ĐÃ MẮC (phát hiện 18/10): bản cũ chép cứng `MOC = 82.9` vào script trong khi cổng giữ
# MOC_NO riêng của nó. Hai bản của cùng một hằng số thì kiểu gì cũng trôi: cổng đổi mốc, script
# không đổi, và ca phá tự thuyết phục mình bằng một ngưỡng không còn tồn tại ở đâu cả. Nay parse
# MOC_NO / MOC_SO_CAU / DUNGSAI thẳng từ tools/nghiem_thu.py — một nguồn duy nhất, hết khả năng lệch.
_ma_cong = io.open(CONG, encoding="utf-8").read()


_cay_cong = ast.parse(_ma_cong)


def _node_cua(ten):
    """Node giá trị của phép gán `ten = ...` trong mã cổng."""
    for node in ast.walk(_cay_cong):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == ten:
                    return node.value
    raise SystemExit("KHÔNG tìm thấy `%s` trong %s — cổng đã đổi tên biến. Dừng, không đoán."
                     % (ten, CONG))


def _so_cong(ten, kieu=float):
    return kieu(ast.literal_eval(_node_cua(ten)))


def _re_cong(ten):
    """Compile lại ĐÚNG pattern mà cổng dùng cho biến regex `ten`.

    VÌ SAO LẤY TỪ CỔNG CHỨ KHÔNG CHÉP TAY. Cả hai lần ca phá này cho kết luận SAI đều vì script
    giữ một bản sao đã trôi của thứ mà cổng sở hữu:
      · Lần 1 (18/10): script chép cứng `MOC = 82.9` trong khi cổng giữ MOC_NO riêng; cổng đổi mốc
        thì script không đổi, nên ca phá tự thuyết phục mình bằng một ngưỡng không còn tồn tại.
      · Lần 2 (cùng ngày, ngay trong lúc vá lần 1): chép `re_item` của cổng BẰNG MẮT và làm rớt
        đúng MỘT dấu nháy đóng — cổng có `..."(?:[^"\\\\]|\\\\.)*"(?:...`, bản chép thành
        `..."(?:[^"\\\\]|\\\\.)*(?:...`. Group 2 vì thế bắt được chuỗi KHÔNG kèm cặp nháy,
        RE_DOAN.findall trả rỗng, _dai() trả None cho cả 16 phương án của js/lab.js và script ABORT
        "ĐO MÙ" — trong khi cổng đo bình thường 38 câu.
    Chẩn lần 2 chỉ ra được nhờ in repr() từng ký tự của cả hai bản; đọc bằng MẮT trên màn hình thì
    hai chuỗi trông giống hệt nhau. Bài học: đừng chép pattern giữa hai tệp; nếu buộc phải có bản
    thứ hai thì lấy nó từ nguồn bằng máy.
    Python gộp các chuỗi kề nhau (`r'a' r'b`) thành MỘT Constant lúc parse, nên literal_eval trên
    args[0] lấy được pattern đầy đủ kể cả khi cổng viết nó trên nhiều dòng.

    PHẢI LẤY CẢ CỜ, KHÔNG CHỈ PATTERN — lỗi thứ ba, cùng một bài học, mắc ngay trong lúc vá hai lỗi
    trên. Bản đầu của hàm này chỉ `re.compile(literal_eval(args[0]))`, tức bỏ rơi tham số thứ hai.
    Mà cổng viết `re_block = re.compile(r"luaChon\\s*:\\s*\\[(.*?)\\]", re.S)`: cờ nằm Ở NGOÀI pattern.
    Mất re.S thì `.` không khớp newline, còn mọi khối `luaChon: [...]` đều trải nhiều dòng nên
    finditer trả RỖNG — script đếm 0/0 câu trong khi cổng đếm 29/38. Đáng chú ý là phép kiểm
    "pattern giống hệt cổng" vẫn PASS, vì nó chỉ so pattern: một phép so đúng thứ mình chép và
    sót đúng thứ mình không chép thì không thể bắt được lỗi này. Bài học: khi nhân bản một lời gọi,
    nhân bản TOÀN BỘ đối số của nó, và kiểm bằng HÀNH VI (đếm ra bao nhiêu câu) chứ không chỉ bằng
    việc so từng phần đã lấy.
    """
    call = _node_cua(ten)
    if not (isinstance(call, ast.Call) and call.args):
        raise SystemExit("`%s` trong cổng không phải re.compile(pattern) — dừng, không đoán." % ten)
    co = 0
    for a in call.args[1:]:
        # `re.S` parse thành Attribute(value=Name('re'), attr='S'); có nơi viết `S` trần sau
        # `from re import S`. Cả hai đều quy về getattr trên module re. Constant(int) thì lấy thẳng.
        if isinstance(a, ast.Attribute) and isinstance(a.value, ast.Name) and a.value.id == "re":
            co |= getattr(re, a.attr)
        elif isinstance(a, ast.Name):
            co |= getattr(re, a.id)
        elif isinstance(a, ast.Constant) and isinstance(a.value, int):
            co |= a.value
        else:
            raise SystemExit("cờ của %s trong cổng không đọc được bằng máy (node %s) — dừng, "
                             "không đoán; đoán cờ là cách sinh ra lỗi 0/0 câu vừa rồi."
                             % (ten, type(a).__name__))
    return re.compile(ast.literal_eval(call.args[0]), co)


MOC = _so_cong("MOC_NO")
MOC_SO_CAU = _so_cong("MOC_SO_CAU", int)
DUNGSAI = _so_cong("DUNGSAI")

RE_BLOCK = _re_cong("re_block")
RE_ITEM = _re_cong("re_item")
RE_DOAN = _re_cong("re_doan")
RE_DAP = _re_cong("re_dap")


def _dai(bieu_thuc):
    """Độ dài ký tự THẬT của một phương án, kể cả khi text viết bằng chuỗi nối.

    Nhân bản do_dai_text() của cổng: tách theo dấu nháy rồi literal_eval TỪNG ĐOẠN. KHÔNG xoá dấu
    cộng bằng regex — sẽ xoá nhầm dấu cộng nằm TRONG nội dung chuỗi ("5 cộng 3" thành "5  3"), tức
    tạo một phép đo mù mới và lần này nó im lặng. Trả None khi không đo được; người gọi PHẢI coi
    None là "đo mù" chứ không phải "dài 0".
    """
    if not bieu_thuc or not bieu_thuc.strip():
        return None
    doan = RE_DOAN.findall(bieu_thuc)
    if not doan:
        return None
    try:
        return sum(len(ast.literal_eval('"' + d + '"')) for d in doan)
    except (ValueError, SyntaxError):
        return None


# PHẠM VI = ĐÚNG PHẠM VI CỦA CỔNG: mọi .js trong js/ và data/ có chứa luaChon.
# Bản cũ hardcode 5 tệp nên bỏ sót js/app.js, js/kienthuc.js, js/logic.js, js/vaitro_connguoi.js,
# data/kienthuc.js -> đếm 35 câu trong khi cổng đếm 38. Hai phép đo trên hai tập câu khác nhau thì
# KHÔNG SO SÁNH ĐƯỢC, và script đã kết luận sai về một cổng hoàn toàn lành mạnh (báo "IM, KHÔNG
# RĂNG" trong lúc cổng đúng). Danh sách nay suy ra bằng cách quét y như cổng, không liệt kê tay:
# liệt kê tay là thứ đã gây ra lỗi này ngay từ đầu.
NGUON = tuple(
    "%s/%s" % (d, f)
    for d in ("js", "data")
    for f in sorted(os.listdir(os.path.join(ROOT, d)))
    if f.endswith(".js")
    and "luaChon" in io.open(os.path.join(ROOT, d, f), encoding="utf-8", errors="replace").read()
)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def do_no():
    """Đo tỉ lệ 'đáp án là phương án dài nhất' bằng ĐÚNG phép của cổng G12c.

    ĐÚNG phép nghĩa là cả HAI thứ phải khớp cổng: tập câu (NGUON) và cách tính độ dài (_dai).
    Bản cũ dùng len(x[1]) — đếm thô ký tự TRONG MÃ NGUỒN, kể cả dấu nháy, dấu cộng và khoảng trắng
    của phép nối. Với phương án viết "đoạn 1 " + "đoạn 2" thì số đó lớn hơn độ dài thật mà học sinh
    nhìn thấy, nên script và cổng xếp hạng phương án dài nhất KHÁC NHAU trên cùng một câu.
    """
    tong = no = 0
    for rel in NGUON:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            continue
        s = io.open(p, encoding="utf-8").read()
        if "luaChon" not in s:
            continue
        for m in RE_BLOCK.finditer(s):
            items = [(k, d) for k, d in
                     ((kk, _dai(tt)) for kk, tt in RE_ITEM.findall(m.group(1)))]
            if any(d is None for _, d in items):
                # KHÔNG coi None là "dài 0": đó là đo mù, và cổng gặp trường hợp này thì báo LỖI
                # chứ không in tỉ lệ. Chạy ca phá lúc đó chỉ cho kết luận về một phép đo hỏng.
                raise SystemExit("ĐO MÙ ở %s: có phương án không đo được độ dài text — dừng." % rel)
            if len(items) < 2:
                continue
            dm = RE_DAP.search(s[m.end():m.end() + 900])
            if not dm:
                continue
            dap = dm.group(1)
            if dap not in [k for k, _ in items]:
                continue
            # items là (str, int) sau khi đã chặn None, nên key=int hợp lệ với max().
            dai = max(items, key=lambda x: x[1])[0]
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
    print(f"        mốc đọc từ mã cổng: MOC_NO={MOC} · MOC_SO_CAU={MOC_SO_CAU} · DUNGSAI={DUNGSAI}")
    print(f"        phạm vi quét: {len(NGUON)} tệp js/data có luaChon")
    print(f"        hash {TEP} = {h0[:16]}")

    # CHỐT PHẠM VI TRƯỚC KHI PHÁ. Lỗi ngày 18/10 nằm đúng ở đây: script đếm 35 câu, cổng đếm 38,
    # và script vẫn chạy tiếp để rồi phán "cổng IM, KHÔNG RĂNG" về một cổng hoàn toàn lành mạnh.
    # Hai phép đo trên hai tập câu khác nhau thì không so sánh được — phải dừng và nói rõ, không
    # được in ra một kết luận trông như đã kiểm chứng.
    if tong0 != MOC_SO_CAU:
        print(f"\n!!! PHẠM VI LỆCH: script đếm {tong0} câu, cổng chốt mốc cho {MOC_SO_CAU} câu.")
        print("    Không kết luận gì về răng của cổng từ hai phép đo lệch phạm vi. Dừng.")
        return 4

    # --- tìm câu mà đáp án KHÔNG phải phương án dài nhất ---
    # Dùng finditer (không findall) vì cần VỊ TRÍ của biểu thức text trong tệp để nối dài đúng chỗ.
    s = io.open(P, encoding="utf-8").read()
    muc_tieu = None
    for m in RE_BLOCK.finditer(s):
        items = []
        for mi in RE_ITEM.finditer(m.group(1)):
            d = _dai(mi.group(2))
            if d is None:
                raise SystemExit("ĐO MÙ khi tìm neo trong %s — dừng." % TEP)
            items.append((mi.group(1), d, mi.group(2)))
        if len(items) < 2:
            continue
        dm = RE_DAP.search(s[m.end():m.end() + 900])
        if not dm:
            continue
        dap = dm.group(1)
        if dap not in [k for k, _, _ in items]:
            continue
        # `items` ở đây là (id, độ_dài:int, biểu_thức:str) và độ_dài đã bị chặn None ở trên,
        # nên cặp đưa vào max là (str, int) — tách khỏi bộ ba để kiểu rõ ràng với checker.
        dai, ldai = max(((k, d) for k, d, _ in items), key=lambda x: x[1])
        if dai != dap:
            _, ldap, bieu_thuc = [x for x in items if x[0] == dap][0]
            muc_tieu = (dap, dai, bieu_thuc, ldap, ldai)
            break
    if not muc_tieu:
        print("\n!!! KHÔNG tìm được câu nào có đáp án không-phải-dài-nhất.")
        print("    Nghĩa là nợ đã 100% — không còn neo để phá. Dừng, không đoán.")
        return 2
    dap, dai, text_dap, ldap, ldai = muc_tieu
    print(f"\n[NEO] câu có dapAn='{dap}' (dài {ldap}) nhưng phương án dài nhất là '{dai}' (dài {ldai})")
    print(f"      text của '{dap}': {text_dap[:70]}...")

    # --- nối dài phương án đúng để LẬT câu này thành "nợ" ---
    # NỐI THÊM MỘT ĐOẠN CHUỖI VÀO CUỐI BIỂU THỨC, không chèn khoảng trắng trước dấu nháy kết.
    # Bản cũ dựng neo `'text:"' + text_dap + '"'`: chỉ đúng khi text là MỘT chuỗi nguyên khối.
    # Nay RE_ITEM bắt cả chuỗi nối ("a" + "b") nên neo cũ khớp 0 lần trong tệp, `s.count(neo) != 1`
    # và script dừng ở bước kiểm duy nhất — tức ca phá chết ngay, không đo được gì. Nối thêm một
    # đoạn `+ "..."` thì đúng với cả hai cách viết, và _dai() cộng đúng `them` ký tự vì nó
    # literal_eval từng đoạn rồi tổng lại.
    if s.count(text_dap) != 1:
        print(f"\n!!! biểu thức text xuất hiện {s.count(text_dap)} lần (cần đúng 1). Dừng — không phá mù.")
        return 2
    # cần nối thêm bao nhiêu để vượt phương án dài nhất + biên an toàn
    them = (ldai - ldap) + 120
    moi = s.replace(text_dap, text_dap + ' + "' + " " * them + '"', 1)
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
    # Tự khai cùng khuôn với 10 script kia, để con số ĐẾM ĐƯỢC BẰNG MÁY. Trước 08/10 script
    # này chỉ in "-> BẮT ĐƯỢC" nên bộ đếm tự động tính nó thành 0 ca.
    #
    # KHAI THEO ĐÚNG BA ĐIỀU KIỆN của mã thoát, không chỉ điều kiện đầu. Bản vá đầu tiên của
    # dòng này chỉ tính `bat`, nên nó in "1/1 ca đúng như kỳ vọng" trong khi script trả rc=1 —
    # tự khai ngược với chính mã thoát của nó. Lỗi đó lộ ra chỉ vì tôi đọc cả log thay vì tin
    # dòng tóm tắt. Nay `dat` = đúng cả ba: bắt được · khôi phục khớp hash · cổng về ĐẠT.
    dat = bat and khop and rc2 == 0
    ly_do = []
    if not bat:
        ly_do.append("cổng KHÔNG bắt")
    if not khop:
        ly_do.append("khôi phục LỆCH hash")
    if rc2 != 0:
        ly_do.append(f"cổng KHÔNG về ĐẠT (rc={rc2}, {ket2})")
    print(f"KẾT LUẬN: {1 if dat else 0}/1 ca đúng như kỳ vọng (1 ca PHÁ bị cổng bắt"
          f" + 0 ca ĐỐI CHỨNG ÂM cổng im đúng)"
          + ("" if dat else " — KHÔNG ĐẠT vì: " + "; ".join(ly_do)))
    shutil.rmtree(tmp)
    return 0 if (bat and khop and rc2 == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
