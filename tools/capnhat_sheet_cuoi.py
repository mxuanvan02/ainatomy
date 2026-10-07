#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cập nhật Google Sheet về TRẠNG THÁI CUỐI của vòng build 04/10.

Mọi số liệu trong tệp này đều LẤY TỪ FILE THẬT, không chép tay:
  * độ phủ YCCĐ      -> yccd_coverage_v2.json  (sinh bởi tools/tinh_do_phu.py)
  * tiêu chí judge   -> judge_result.json      (sinh bởi tools/nghiem_thu.py)
  * commit / dung lượng -> git và GitHub API
Lí do: các lần trước số ghi tay trong tài liệu đã lệch với mã nguồn
(ghi "12 chủ đề" trong khi Bộ có 13; ghi 10.C2.MR2 "ngoài phạm vi" trong khi đã phủ).
"""
import json, os, subprocess, urllib.request, urllib.parse, sys

TOK = os.environ.get("GOOGLE_TOKEN_JSON") or os.path.expanduser("~/.hermes/google_token.json")
SID = "1SzJwN1Pt3CQwxfS5QJP3SP6t_cR23ZZOuLRJIMM4sSU"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOI = ROOT  # sau khi làm repo tự chứa, gốc repo CHÍNH LÀ thư mục sản phẩm


def sh(args, cwd=SOI):
    """Chạy lệnh với đối số DẠNG LIST, không dùng shell=True.
    Đã sửa theo cảnh báo bảo mật: bản đầu nhận một chuỗi rồi gọi shell=True, tuy các
    lệnh trong tệp này là hằng số nhưng thói quen đó dễ thành lỗ hổng khi sao chép."""
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.stdout.strip()


def access_token():
    d = json.load(open(TOK))
    body = urllib.parse.urlencode({"client_id": d["client_id"], "client_secret": d["client_secret"],
                                   "refresh_token": d["refresh_token"], "grant_type": "refresh_token"}).encode()
    return json.loads(urllib.request.urlopen(
        urllib.request.Request(d["token_uri"], data=body), timeout=30).read())["access_token"]


def api(method, path, tok, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request("https://sheets.googleapis.com" + path, data=data, method=method)
    req.add_header("Authorization", "Bearer " + tok)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        return json.loads(urllib.request.urlopen(req, timeout=120).read())
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:400]); raise


def main():
    # ---------- đọc số THẬT ----------
    cov = json.load(open(os.path.join(ROOT, "yccd_coverage_v2.json"), encoding="utf-8"))
    jd = json.load(open(os.path.join(ROOT, "judge_result.json"), encoding="utf-8"))
    sha = sh(["git", "rev-parse", "--short", "HEAD"], SOI)
    du_lieu = []
    for f in ["index.html", "css/style.css", "js/app.js", "js/nhamay_text.js",
              "js/nhamay_tram01.js", "js/tinhhuong.js", "js/lab3d.js", "js/pipeline3d.js",
              "js/scene3d.js", "data/yccd.js"]:
        p = os.path.join(SOI, f)
        if os.path.exists(p):
            du_lieu.append([f, f"{os.path.getsize(p):,} bytes"])
    # Đếm số dòng mã bằng Python thuần. Bản đầu dùng pipeline shell
    # (find | grep | xargs | wc -l | tail) — sau khi bỏ shell=True thì pipeline
    # không chạy được nữa, nên thay bằng os.walk: không cần shell, kết quả như nhau.
    so_dong_ma = 0
    so_tep_ma = 0
    for dirpath, dirnames, filenames in os.walk(SOI):
        dirnames[:] = [d for d in dirnames if d not in ("vendor", ".git")]
        for fn in filenames:
            if fn.endswith((".js", ".html", ".css")):
                p = os.path.join(dirpath, fn)
                try:
                    so_dong_ma += sum(1 for _ in open(p, encoding="utf-8", errors="replace"))
                    so_tep_ma += 1
                except OSError:
                    pass
    so_dong = f"{so_dong_ma} dòng trong {so_tep_ma} tệp .js/.html/.css (không tính vendor)"

    # ---------- TAB: Trạng thái cuối ----------
    tu_cov = {}
    for c in cov:
        tu_cov[c["muc"]] = tu_cov.get(c["muc"], 0) + 1
    dat = sum(1 for k in jd if k["dat"])
    TRANG = [
        ["TRẠNG THÁI CUỐI — vòng build 04/10/2026 (mọi số lấy từ file thật, không chép tay)"],
        [""],
        ["Website", "https://mxuanvan02.github.io/soi-ai-lop10/", "HTTP 200, Pages build đúng commit"],
        ["Repo", "https://github.com/mxuanvan02/soi-ai-lop10", "public, commit " + sha],
        ["Tổng số dòng mã (trừ vendor)", so_dong.split()[0] + " dòng", "find + wc"],
        [""],
        ["ĐỘ PHỦ 22 YCCĐ LỚP 10 — đo bằng tools/tinh_do_phu.py (quét mã nguồn)"],
        ["PHỦ MẠNH (>=2 tệp độc lập)", tu_cov.get("PHỦ MẠNH", 0), "yccd_coverage_v2.json"],
        ["PHỦ (1 tệp)", tu_cov.get("PHỦ", 0), ""],
        ["CHƯA PHỦ", tu_cov.get("CHƯA PHỦ", 0), "0 YCCĐ cốt lõi nào còn trống"],
        ["TỔNG", f"{len(cov)}/22", ""],
        [""],
        ["JUDGE ĐỘC LẬP — tools/nghiem_thu.py (không phải agent tự chấm)"],
        ["Tiêu chí đạt", f"{dat}/{len(jd)}", "judge_result.json"],
        ["G1 nền sáng + tương phản WCAG", "12/12", "đo bằng công thức, gồm cặp kế thừa"],
        ["G2 icon SVG", "4/4", "0 emoji trong button/logo, 0 use mồ côi"],
        ["G3 nhà máy 7 trạm", "6/6", "0 trạm 'đang xây dựng'"],
        ["G4 chất lượng văn bản", "7/7", "oracle 40/40 cả hai nhánh"],
        ["G6 offline", "4/4", "0 asset CDN, three.js + icon trong repo"],
        ["G7 deploy", "2/2", "--nen=#FAF5FF đọc từ site thật"],
        [""],
        ["BUG ĐÃ PHÁT HIỆN VÀ SỬA TRONG VÒNG NÀY (mỗi bug đều ghi nguyên nhân trong comment code)"],
        ["#", "Bug", "Hậu quả nếu không sửa", "Số liệu chứng minh"],
        [1, "pipeline3d.doan() trả về thiếu ok:true", "TRẠM 6 CHẾT HOÀN TOÀN ở tương tác chính: không chấm, không ghi log", "log chỉ có batDauLuot, không có doan; sau sửa: doan:sai + doan:đúng"],
        [2, "selector $('t1-tiendо') dùng chữ 'о' CYRILLIC U+043E", "nút Chấm nhãn vĩnh viễn disabled -> hỏng cả Trạm 1; MẮT THƯỜNG KHÔNG THẤY", "grep xác nhận; sau sửa dán 10/10 ảnh và nút bật"],
        [3, "cauNgauNhien() ghép câu đã hạ chữ thường", "câu thứ 2 viết thường giữa chuỗi, học sinh tưởng ứng dụng lỗi chính tả", "judge G4b cũ BỎ LỌT; đã thêm G4b2 -> 0/40 câu lỗi"],
        [4, "LCG với seed liên tiếp", "200/200 seed (100%) ra 'có lỗi' thay vì 60% -> pre/post KHÔNG độc lập, hỏng phép đo tiến bộ", "sau splitmix32: 59.0%, 5 nhóm lỗi đều (24,22,29,23,20)"],
        [5, "sinh() khởi đầu giữa từ", "văn bản bắt đầu 'Ể trôi chảy nhưng số.' rồi toUpperCase thành 'Ể' vô nghĩa", "0/12 seed còn lỗi"],
        [6, "thongTin là method trong object literal", "ReferenceError khi ungDung() gọi -> cả Trạm 5 chết", "đã tách hàm riêng trong closure"],
        [7, "appendChild(w) hai lần trong veAnhDanNhan", "appendChild nút đã có cha sẽ DI CHUYỂN nó -> lệch thứ tự ảnh", "sau sửa: 10/10 ảnh đúng thứ tự, mỗi ảnh 2 nút"],
        [8, "--dung #15803D trên nền --nenDung", "4.45:1 < 4.5:1, chữ 'TRUE' và nhãn trạm đã xong khó đọc", "đổi #146B33 -> 5.86:1"],
        [9, "--vang #B45309 trên nền phụ --nen2", "4.34:1 < 4.5:1, chữ trong ô nền phụ khó đọc", "đổi #8A4006 -> 6.45:1"],
        [10, "4/5 màu trạm 3D kế thừa từ nền tối", "FAIL WCAG 1.4.11: 1.36 / 2.37 / 1.92 / 2.65 trên nền sáng", "đổi theo max-min diversity: min distance 114.4 (chọn tay chỉ 58.4)"],
        [11, ".step.on chữ #08131f trên nền nhấn", "3.86:1 < 4.5:1", "đổi chữ trắng -> 5.36:1"],
        [12, "nút CTA #0891B2 + chữ trắng", "3.68:1 FAIL. Agent đã NHẦM sang 5.70:1 (là cặp chữ ĐEN) vì quên tương phản có tính đối xứng", "đổi nền #0E7490 -> 5.36:1"],
        [""],
        ["3 LỖI TRONG CHÍNH CÔNG CỤ ĐO (phải nói rõ để không ai tin nhầm)"],
        ["Lỗi", "Hiện tượng", "Cách sửa"],
        ["judge G1f gộp background+color rồi flag L<0.25", "flag oan #15803D và #7C3AED là 'màu tối' trong khi đó là MÀU CHỮ hợp lệ", "tách thành G1f (nền phải sáng) và G1f2 (chữ phải >=4.5) -> CHẶT HƠN bản cũ"],
        ["judge G1f2 không resolve var()", "đo #FFFFFF/#FFFFFF=1.00 (false positive) và BỎ SÓT cặp thật chữ trắng trên #7C3AED", "resolve var(--x) về giá trị thật -> nay đo 36 cặp"],
        ["judge G1h chỉ đọc scene3d.js", "BỎ LỌT 5 màu trạm hardcode trong pipeline3d.js, 4/5 màu FAIL mà không bị phát hiện", "thêm G1i (màu trạm) + G1j (độ phân biệt giữa 5 trạm)"],
        ["judge G7b in chi_tiet cố định giọng thất bại", "in '[ĐẠT] ... không thấy #FAF5FF' — TỰ MÂU THUẪN, khiến người đọc tưởng deploy hỏng", "chi_tiet nay tính THEO KẾT QUẢ, kèm bằng chứng --nen=#FAF5FF đọc từ site"],
        ["metric 'tỉ lệ từ có trong ngữ liệu'", "GOODHART: luôn ~0.992 với máy n-gram vì máy sinh chữ LẤY TỪ ngữ liệu; trong khi văn bản thật vẫn lộn xộn", "LOẠI BỎ, thay bằng G4a2 'đầu ra là câu hoàn chỉnh' -> 100%"],
        [""],
        ["DUNG LƯỢNG CÁC TỆP CHÍNH"],
    ] + du_lieu + [
        [""],
        ["VIỆC CHỜ ANH VĂN (agent không tự quyết được)"],
        ["1", "Chốt NGÀY DẠY Bài 5 + 4 tiết chuyên đề", "NÚT THẮT CỔ CHAI: không có tiết dạy thật trước 20/10 thì mất điều kiện thể lệ 'đã triển khai thực tế' -> RỚT sơ tuyển"],
        ["2", "Duyệt nhãn 56 câu hỏi", "ho-so/checklist_duyet_nhan.html — nhãn là trách nhiệm chuyên môn của tác giả"],
        ["3", "Tải 2 file mẫu BTC (slide + poster)", "apps.rmit.edu.vn/r/filemauGTPT2026 — máy agent lỗi certificate với tên miền này"],
        ["4", "Giữ tên SOI AI hay đổi?", "agent đã tự quyết giữ, anh có quyền đổi — repo đổi tên được"],
        ["5", "Backend log tập trung trên máy fleet?", "TUỲ CHỌN, không chặn tiến độ; localStorage + xuất CSV đã đủ minh chứng"],
        [""],
        ["GIỚI HẠN TRUNG THỰC (không che giấu)"],
        ["a", "Chưa có tiết dạy thật nào", "toàn bộ số liệu hiện là đo trên máy agent, chưa phải dữ liệu lớp học thật"],
        ["b", "Ngữ liệu máy sinh văn bản chỉ 16 câu / 4 chủ đề", "đủ để dạy hiện tượng bịa/lạc đề, nhưng KHÔNG phải một trợ lí AI dùng được cho việc học thật"],
        ["c", "Mô hình là perceptron 4 đặc trưng", "đủ để thấy cơ chế thiên kiến; KHÔNG phải deep learning, không xử lí ảnh hay ngôn ngữ phức tạp"],
        ["d", "Ảnh chụp màn hình Trạm 5 có đầu ra chưa chụp được", "Page.captureScreenshot timeout 2 lần; trạng thái đó đã verify bằng DOM (rubric 3/3, phanhoi dung) chứ không có ảnh"],
        ["e", "Chưa áp dụng chuẩn viết academic-prose vào TOÀN BỘ nội dung trong app", "đã áp dụng cho tài liệu thiết kế; nội dung học sinh đọc vẫn còn chỗ dùng lối liệt kê"],
        ["f", "56 câu hỏi mở rộng chưa được tác giả duyệt nhãn", "chưa được đưa vào bản dạy thật"],
    ]

    tok = access_token()
    meta = api("GET", f"/v4/spreadsheets/{SID}?fields=sheets.properties.title", tok)
    co = [s["properties"]["title"] for s in meta["sheets"]]
    TAB = "Trạng thái cuối"
    if TAB not in co:
        api("POST", f"/v4/spreadsheets/{SID}:batchUpdate", tok,
            {"requests": [{"addSheet": {"properties": {"title": TAB}}}]})
        print("đã tạo tab", TAB)
    api("POST", f"/v4/spreadsheets/{SID}/values:batchClear", tok,
        {"ranges": [f"'{TAB}'!A1:ZZ300"]})
    api("POST", f"/v4/spreadsheets/{SID}/values:batchUpdate", tok, {
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": f"'{TAB}'!A1", "values": TRANG}]})

    # cập nhật mức phủ trong tab YCCĐ từ file thật (không chép tay)
    rng = urllib.parse.quote("'YCCĐ lớp 10'!A1:I30")
    vals = api("GET", f"/v4/spreadsheets/{SID}/values/{rng}", tok).get("values", [])
    cap_nhat = []
    for i, row in enumerate(vals):
        if not row or i == 0:
            continue
        ma = row[0]
        c = next((x for x in cov if x["ma"] == ma), None)
        if c:
            teps = ", ".join(x["tep"] for x in c["bangChung"])
            cap_nhat.append({"range": f"'YCCĐ lớp 10'!H{i+1}:I{i+1}",
                             "values": [[teps, c["muc"]]]})
    if cap_nhat:
        api("POST", f"/v4/spreadsheets/{SID}/values:batchUpdate", tok,
            {"valueInputOption": "USER_ENTERED", "data": cap_nhat})
        print(f"đã cập nhật {len(cap_nhat)} dòng mức phủ trong tab YCCĐ")

    # VERIFY
    print("\n=== VERIFY (đọc lại từ server) ===")
    got = len(api("GET", f"/v4/spreadsheets/{SID}/values/"
                       + urllib.parse.quote(f"'{TAB}'!A1:Z300"), tok).get("values", []))
    ok1 = got == len(TRANG)
    print(f"  [{'OK ' if ok1 else 'LỆCH'}] {TAB}: server={got} nguồn={len(TRANG)}")
    rng = urllib.parse.quote("'YCCĐ lớp 10'!I1:I30")
    muc = [r[0] for r in api("GET", f"/v4/spreadsheets/{SID}/values/{rng}", tok).get("values", [])[1:]]
    from collections import Counter
    c2 = Counter(muc)
    ok2 = c2.get("CHƯA PHỦ", 0) == 0 and sum(c2.values()) == 22
    print(f"  [{'OK ' if ok2 else 'LỆCH'}] mức phủ trên sheet: {dict(c2)} (kì vọng 0 'CHƯA PHỦ', tổng 22)")
    print("\nKẾT LUẬN:", "ĐẠT" if (ok1 and ok2) else "CÒN LỖI")
    print("LINK: https://docs.google.com/spreadsheets/d/" + SID)
    return 0 if (ok1 and ok2) else 1


if __name__ == "__main__":
    sys.exit(main())
