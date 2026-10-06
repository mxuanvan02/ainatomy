#!/usr/bin/env python3
"""Gộp nhật ký CSV/JSON của SOI AI từ nhiều máy phòng lab thành 1 báo cáo lớp.

TỆP NÀY TỪNG NẰM NGOÀI REPO (06/10 mới đưa vào): README.md §4 hướng dẫn giáo viên chạy
`python3 tools/gop_csv.py`, nhưng tệp thật nằm ở ieeai2026/tools/ — NGOÀI repo. Nghĩa là
một giáo viên clone repo về, làm đúng từng chữ trong README, và nhận `No such file or
directory` ở đúng khâu cuối cùng của tiết học (gộp dữ liệu cả lớp). Đây là chỗ gãy đúng
vào mắt xích "nhân rộng": sản phẩm tự chứa mà thiếu công cụ mà chính tài liệu của nó
hướng dẫn dùng. Nay tệp nằm trong repo, đã test end-to-end (2 máy giả lập -> 3 báo cáo).

Tên cũ "MỔ XẺ AI" đã được thay bằng SOI AI (tên chính thức trong hồ sơ dự thi).

Bối cảnh: app lưu log trong localStorage của TỪNG máy (phòng máy 20 máy = 20 log rời).
Giáo viên thu file bằng nút "Xuất CSV/JSON" trên mỗi máy vào 1 USB, rồi chạy script này.

Cách dùng:
    python3 gop_csv.py <thư_mục_chứa_các_file_xuất> [-o báo_cáo.xlsx] [--prefix mã_lớp]

Đầu ra:
    - nhatky_gop.csv      : toàn bộ sự kiện (đã khử trùng lặp theo máy+mã HS+timestamp)
    - baocao_lop.csv      : recall theo 5 loại lỗi + bản đồ 12 khối UNESCO (cả lớp)
    - baocao_ca_nhan.csv  : từng mã HS một dòng
"""
import argparse, csv, glob, json, os, re, sys
from collections import defaultdict

LOAI_LOI = {
    "so_lieu_bia": "Số liệu bịa đặt",
    "nguon_khong_ton_tai": "Nguồn/văn bản không tồn tại",
    "thien_kien": "Thiên kiến, định kiến",
    "suy_luan_sai": "Suy luận sai",
    "lo_du_lieu_ca_nhan": "Xui lộ dữ liệu cá nhân",
}
UNESCO = {
    "A1": "A1 Hiểu: AI phục vụ con người", "A2": "A2 Vận dụng: đánh giá AI theo nhu cầu",
    "A3": "A3 Sáng tạo: đề xuất giải pháp AI", "B1": "B1 Hiểu: vấn đề đạo đức AI",
    "B2": "B2 Vận dụng: xử lí tình huống đạo đức", "B3": "B3 Sáng tạo: nguyên tắc dùng AI",
    "C1": "C1 Hiểu: kĩ thuật và ứng dụng AI", "C2": "C2 Vận dụng: dùng công cụ AI",
    "C3": "C3 Sáng tạo: tạo sản phẩm với AI", "D1": "D1 Hiểu: quá trình huấn luyện AI",
    "D2": "D2 Vận dụng: huấn luyện/cải tiến mô hình", "D3": "D3 Sáng tạo: thiết kế hệ thống AI",
}
HDR = ["ma_hs","ma_lop","loai_su_kien","item_id","mach","unesco",
       "dap_an_dung","loai_loi_that","tra_loi","tra_loi_loai","diem","bat_oan","bo_sot",
       "che_do","phien_tong","phien_dung","phien_bat_oan","phien_bo_sot","thoi_gian_ISO"]

def doc_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows: return []
    head = rows[0]
    out = []
    for r in rows[1:]:
        d = dict(zip(head, r))
        out.append(d)
    return out

def doc_json(path):
    """JSON xuất từ app = {maHS: {maHS, maLop, suKien:[...]}}"""
    d = json.load(open(path, encoding="utf-8"))
    out = []
    for ma, hs in d.items():
        for sk in hs.get("suKien", []):
            kq = sk.get("kq") or {}
            out.append({
                "ma_hs": ma, "ma_lop": hs.get("maLop", ""),
                "loai_su_kien": sk.get("loai", ""),
                "item_id": kq.get("itemId") or (sk.get("nhiemVu") or {}).get("id", ""),
                "mach": kq.get("mach") or (sk.get("nhiemVu") or {}).get("mach", ""),
                "unesco": kq.get("unesco") or (sk.get("nhiemVu") or {}).get("unesco", ""),
                "dap_an_dung": kq.get("loaiThat") or kq.get("dapAn", ""),
                "tra_loi": kq.get("traLoiVerdict") or kq.get("chon", ""),
                "diem": "" if kq.get("diem") is None else kq.get("diem"),
                "bat_oan": 1 if kq.get("batOan") else 0,
                "bo_sot": 1 if kq.get("boSot") else 0,
                "thoi_gian_ISO": sk.get("t_iso", ""),
            })
    return out

def gop(thu_muc):
    rows, nguon = [], []
    for p in sorted(glob.glob(os.path.join(thu_muc, "*"))):
        if not os.path.isfile(p): continue
        low = p.lower()
        try:
            if low.endswith(".csv"): r = doc_csv(p)
            elif low.endswith(".json"): r = doc_json(p)
            else: continue
        except Exception as e:
            print(f"  ! bỏ qua {os.path.basename(p)}: {e}", file=sys.stderr); continue
        nguon.append((os.path.basename(p), len(r)))
        # đánh dấu máy nguồn để khử trùng
        for x in r: x["_src"] = os.path.basename(p)
        rows.extend(r)
    # khử trùng lặp (cùng máy, cùng HS, cùng item, cùng thời điểm)
    seen, uniq = set(), []
    for r in rows:
        k = (r.get("_src"), r.get("ma_hs"), r.get("item_id"), r.get("thoi_gian_ISO"))
        if k in seen and k != (r.get("_src"), r.get("ma_hs"), "", ""): continue
        seen.add(k); uniq.append(r)
    return uniq, nguon

def bao_cao(rows):
    # recall theo loại lỗi (toàn lớp)
    theo_loai = {k: {"dung":0, "co_loi":0, "bat_oan":0} for k in LOAI_LOI}
    unesco = {k: {"dung":0, "tong":0} for k in UNESCO}
    ca_nhan = defaultdict(lambda: {"tong":0, "dung":0, "lab":0, "lop":"", "pre":[], "post":[]})
    for r in rows:
        if r.get("loai_su_kien") == "dauTruong":
            u = r.get("unesco","")
            if u in unesco:
                unesco[u]["tong"] += 1
                if str(r.get("diem")) == "1": unesco[u]["dung"] += 1
            loai_that = r.get("dap_an_dung","")
            if loai_that == "co_loi":
                key = r.get("loai_loi_that") or None
                if key and key in theo_loai:
                    theo_loai[key]["co_loi"] += 1
                    if str(r.get("diem")) == "1": theo_loai[key]["dung"] += 1
            if str(r.get("bat_oan")) == "1":
                key = r.get("tra_loi_loai") or None
                if key and key in theo_loai: theo_loai[key]["bat_oan"] += 1
        if r.get("loai_su_kien") == "lab":
            ca_nhan[r.get("ma_hs","")]["lab"] += 1
        cn = ca_nhan[r.get("ma_hs","")]
        cn["lop"] = r.get("ma_lop","") or cn["lop"]
        if r.get("loai_su_kien") == "dauTruong":
            cn["tong"] += 1
            if str(r.get("diem")) == "1": cn["dung"] += 1
    # phiên pre/post: mỗi sự kiện loai_su_kien == "phien" là một phiên hoàn tất
    phien = {"pre": [], "post": []}
    for r in rows:
        if r.get("loai_su_kien") == "phien" and r.get("che_do") in phien:
            try:
                t = int(r.get("phien_tong") or 0); dg = int(r.get("phien_dung") or 0)
                if t: phien[r["che_do"]].append(dg / t)
            except ValueError:
                pass
    return theo_loai, unesco, ca_nhan, phien

def ghi(rows, theo_loai, unesco, ca_nhan, phien, outdir):
    p1 = os.path.join(outdir, "nhatky_gop.csv")
    with open(p1, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HDR, extrasaction="ignore"); w.writeheader()
        for r in rows: w.writerow(r)
    p2 = os.path.join(outdir, "baocao_lop.csv")
    with open(p2, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["== RECALL THEO LOẠI LỖI (cả lớp) =="])
        w.writerow(["loai_loi","ten","phat_hien_dung","tong_cau_co_loi","recall","bat_oan"])
        for k, v in theo_loai.items():
            rec = (v["dung"]/v["co_loi"]) if v["co_loi"] else ""
            w.writerow([k, LOAI_LOI[k], v["dung"], v["co_loi"],
                        f"{rec:.3f}" if rec != "" else "", v["bat_oan"]])
        w.writerow([])
        w.writerow(["== TIẾN TRÌNH PRE/POST (trung bình tỉ lệ đúng của các phiên) =="])
        w.writerow(["phien","so_phien","trung_binh_ti_le_dung"])
        for mode in ("pre", "post"):
            arr = phien.get(mode, [])
            avg = sum(arr) / len(arr) if arr else ""
            w.writerow([mode, len(arr), f"{avg:.3f}" if avg != "" else ""])
        w.writerow([])
        w.writerow(["== BẢN ĐỒ 12 KHỐI NĂNG LỰC UNESCO × QĐ 2422 =="])
        w.writerow(["khoi","ten","dung","tong","ti_le"])
        for k, v in unesco.items():
            t = (v["dung"]/v["tong"]) if v["tong"] else ""
            w.writerow([k, UNESCO[k], v["dung"], v["tong"], f"{t:.3f}" if t != "" else ""])
    p3 = os.path.join(outdir, "baocao_ca_nhan.csv")
    with open(p3, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ma_hs","ma_lop","so_cau_dau_truong","so_cau_dung","ti_le_dung","so_nhiem_vu_lab"])
        for ma, v in sorted(ca_nhan.items()):
            if not ma: continue
            t = (v["dung"]/v["tong"]) if v["tong"] else ""
            w.writerow([ma, v["lop"], v["tong"], v["dung"], f"{t:.3f}" if t != "" else "", v["lab"]])
    return p1, p2, p3

def main():
    ap = argparse.ArgumentParser(description="Gộp nhật ký MỔ XẺ AI từ nhiều máy phòng lab.")
    ap.add_argument("thu_muc", help="Thư mục chứa các file CSV/JSON xuất từ các máy")
    ap.add_argument("-o", "--outdir", default=".", help="Thư mục xuất báo cáo (mặc định: hiện tại)")
    args = ap.parse_args()
    if not os.path.isdir(args.thu_muc):
        print(f"LỖI: không thấy thư mục {args.thu_muc}", file=sys.stderr); sys.exit(1)
    rows, nguon = gop(args.thu_muc)
    print(f"Đã đọc {len(nguon)} file nguồn:")
    for n, c in nguon: print(f"  - {n}: {c} dòng")
    if not rows:
        print("KHÔNG có dữ liệu nào. Kiểm tra thư mục có file CSV/JSON xuất từ app không.", file=sys.stderr)
        sys.exit(1)
    theo_loai, unesco, ca_nhan, phien = bao_cao(rows)
    os.makedirs(args.outdir, exist_ok=True)
    p1, p2, p3 = ghi(rows, theo_loai, unesco, ca_nhan, phien, args.outdir)
    print(f"\n✅ {len(rows)} sự kiện từ {len(nguon)} máy, {len(ca_nhan)} mã HS.")
    print(f"   {p1}\n   {p2}\n   {p3}")

if __name__ == "__main__":
    main()
