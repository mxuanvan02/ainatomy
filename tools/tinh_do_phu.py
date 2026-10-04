#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Tính ĐỘ PHỦ 22 yêu cầu cần đạt lớp 10 từ BẰNG CHỨNG TRONG CODE.

VÌ SAO CÓ TỆP NÀY
  Trước đây độ phủ được ghi tay trong tài liệu thiết kế và trong Google Sheet, nên có
  lần tài liệu ghi "12 chủ đề" trong khi văn bản của Bộ có 13, và có lần ghi 10.C2.MR2
  là "ngoài phạm vi" trong khi thực tế đã phủ được. Số ghi tay luôn có nguy cơ lệch
  với mã nguồn.

  Tệp này tính lại độ phủ bằng cách QUÉT MÃ NGUỒN: một yêu cầu cần đạt chỉ được tính
  là phủ khi có tên tệp thật và bằng chứng kiểm chứng được. Kết quả ghi ra
  yccd_coverage_v2.json để tài liệu và Sheet lấy số từ đó, không chép tay.

CÁCH CHẤM
  PHỦ MẠNH : có bằng chứng ở >= 2 tệp mã độc lập (hai con đường khác nhau cùng dạy
             một yêu cầu) — ví dụ thiên kiến dữ liệu vừa dạy ở xưởng 2D vừa ở phòng 3D.
  PHỦ      : có bằng chứng ở 1 tệp mã.
  CHƯA PHỦ : không có bằng chứng nào.

  Mỗi bằng chứng được KIỂM CHỨNG hai lớp:
    (1) tệp phải tồn tại trên đĩa;
    (2) bằng chứng phải là MÃ YCCĐ xuất hiện trong tệp (mạnh) hoặc tên hàm/hằng
        được liệt kê tường minh và có thật trong tệp (yếu hơn, vẫn phải tồn tại).
  Nếu khai báo một hàm không có trong tệp, phép kiểm báo LỖI CHỨ KHÔNG im lặng bỏ qua —
  đây là điểm khác biệt so với việc ghi tay.

CÁCH CHẠY
  python3 tools/tinh_do_phu.py            # in bảng + ghi JSON
  python3 tools/tinh_do_phu.py --strict   # thoát 1 nếu còn yêu cầu CHƯA PHỦ
"""
import json, os, re, sys

ROOT = "/home/hitokiri/ieeai2026/soi-ai"
YCCD = "/home/hitokiri/ieeai2026/yccd_lop10_sach.json"
OUT = "/home/hitokiri/ieeai2026/yccd_coverage_v2.json"

# BẰNG CHỨNG: mã YCCĐ -> [(tệp, mô tả, tên hàm/hằng phải có thật trong tệp)]
# Phần tử thứ ba để trống ("") nghĩa là chỉ cần MÃ YCCĐ xuất hiện trong tệp.
BC = {
 "10.A1.1": [("js/pipeline3d.js", "Trạm CON NGƯỜI KIỂM: vai trò + hậu quả khi hỏng", "TRAM"),
             ("js/nhamay_tram01.js", "Câu hỏi t0-5: khâu nhập liệu là việc của con người", "CAU_HOI_T0")],
 "10.A1.2": [("js/pipeline3d.js", "Trạm CON NGƯỜI KIỂM, đoán trạm hỏng", "TRAM")],
 "10.A2.1": [("js/tinhhuong.js", "4 tình huống rủi ro: X-quang khoa nhi, camera khuôn mặt", "NHOM_RUI_RO")],
 "10.A2.MR1": [("js/tinhhuong.js", "Tình huống dự án sáng tạo + biện pháp hạn chế rủi ro", "NHOM_RUI_RO")],
 "10.A3.1": [("data/kienthuc.js", "4 luật VN đã kiểm chứng số hiệu", "kt-01")],
 "10.B2.1": [("js/tinhhuong.js", "4 tình huống vi phạm nội quy/pháp luật", "NHOM_VI_PHAM")],
 "10.B2.MR1": [("data/cauhoi.js", "Ngân hàng đấu trường, 5 nhóm lỗi cài sẵn", "MX_BANK"),
               ("js/nhamay_text.js", "Trạm 5: phán đoán câu trả lời có căn cứ hay bịa", "chamUngDung")],
 "10.B3.1": [("js/lab.js", "Thiên kiến ngày/đêm từ dữ liệu lệch 92%", "taoDuLieu"),
             ("js/lab3d.js", "Phòng 3D: mặt phẳng quyết định và cụm ngày/đêm", "matPhangTuTrongSo")],
 "10.C2.1": [("js/nhamay_tram01.js", "Câu hỏi t0-3: ưu tiên vấn đề Việt Nam", "CAU_HOI_T0"),
             ("js/nhamay_text.js", "4 chủ đề VN: nông nghiệp, y tế, giáo dục, môi trường", "CHU_DE")],
 "10.C2.2": [("data/kienthuc.js", "Ứng dụng AI theo 6 nhóm tính năng", "kt-02")],
 "10.C2.3": [("data/kienthuc.js", "Trường hợp AI hỗ trợ học tập", "kt-06"),
             ("js/nhamay_text.js", "Chủ đề giáo dục + Trạm 5 dùng AI trong học tập", "giaoDuc")],
 "10.C2.MR1": [("js/tinhhuong.js", "2 tình huống xác định yêu cầu khi ứng dụng AI", "NHOM_YEU_CAU")],
 "10.C2.MR2": [("js/nhamay_text.js", "Học sinh DÙNG hệ AI thật trong trình duyệt, 0 MB, offline", "ungDung")],
 "10.C3.1": [("js/nhamay_text.js", "Rubric 3 tiêu chí chấm prompt", "RUBRIC_PROMPT")],
 "10.C3.2": [("js/nhamay_text.js", "Thực hành đặt prompt + máy sinh trả lời", "ungDung"),
             ("data/kienthuc.js", "3 bài thực hành prompt tự chấm theo rubric", "p-02")],
 "10.C3.3": [("data/kienthuc.js", "Bảng so sánh AI tạo sinh với phân loại/dự đoán", "kt-03")],
 "10.C3.MR1": [("js/tinhhuong.js", "2 tình huống công nghệ thiết kế và tạo AI", "NHOM_YEU_CAU")],
 "10.C4.1": [("js/lab.js", "Perceptron học thật + kiểm tra tách ngày/đêm", "kiemTra"),
             ("js/lab3d.js", "Kéo tỉ lệ ảnh ngày và xem hậu quả trong không gian 3D", "doiTiLeNgay"),
             ("js/nhamay_tram01.js", "Trạm 1: dán nhãn sai làm mất 40% độ chính xác (đo thật)", "chamT1")],
 "10.C4.MR1": [("js/nhamay_tram01.js", "Trạm 0: ba dạng dữ liệu và bốn đặc trưng máy đọc", "veAnhVaDacTrung")],
 "10.D1.1": [("js/pipeline3d.js", "5 trạm và mối liên hệ mục tiêu - thành phần", "TRAM")],
 "10.D2.1": [("js/pipeline3d.js", "5 thành phần: dữ liệu, mô hình, thuật toán, đầu ra, phản hồi", "TRAM"),
             ("js/nhamay_tram01.js", "Câu hỏi t0-5 về vị trí khâu nhập liệu trong hệ thống", "CAU_HOI_T0")],
 "10.D2.2": [("js/lab.js", "Đánh giá trên bộ mới: 100% ban ngày so với 59% ban đêm", "kiemTra"),
             ("js/logic.js", "Bảng nhầm lẫn: bỏ sót và bắt oan", "bangNhamLan"),
             ("js/pipeline3d.js", "Hậu quả khi từng trạm hỏng", "TRAM")],
}


def nap_ma():
    out = {}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "vendor")]
        for f in filenames:
            if f.endswith((".js", ".html")):
                p = os.path.join(dirpath, f)
                out[os.path.relpath(p, ROOT)] = open(p, encoding="utf-8").read()
    return out


def main():
    strict = "--strict" in sys.argv
    ma_nguon = {r["ma"]: r for r in json.load(open(YCCD, encoding="utf-8"))}
    files = nap_ma()
    print(f"đã nạp {len(files)} tệp mã nguồn từ {ROOT}")
    print(f"YCCĐ lớp 10 (nguồn đã kiểm chứng 22/22): {len(ma_nguon)}\n")

    loi_bc, ket = [], []
    for ma in sorted(ma_nguon, key=lambda m: (m[3], m[4],
                                              int(re.sub(r'\D', '', m.split('.')[-1]) or 0),
                                              'MR' in m)):
        xac_nhan = []
        for tep, mo_ta, ham in BC.get(ma, []):
            if tep not in files:
                loi_bc.append(f"{ma}: tệp KHÔNG TỒN TẠI {tep}")
                continue
            noi_dung = files[tep]
            co_ma = ma in noi_dung
            co_ham = (ham in noi_dung) if ham else None
            if not co_ma and co_ham is not True:
                loi_bc.append(f"{ma}: bằng chứng yếu — không có mã YCCĐ và không có "
                              f"'{ham}' trong {tep}")
                continue
            xac_nhan.append({"tep": tep, "moTa": mo_ta,
                             "maYCCDTrongTep": co_ma,
                             "hamCoThat": (co_ham if co_ham is not None else "không kiểm")})
        so_tep = len({x["tep"] for x in xac_nhan})
        muc = "CHƯA PHỦ" if so_tep == 0 else ("PHỦ MẠNH" if so_tep >= 2 else "PHỦ")
        ket.append({"ma": ma, "chuDe": ma_nguon[ma].get("chuDe", ma.split('.')[1]),
                    "mach": ma[3], "loai": ma_nguon[ma].get("loai", ""),
                    "muc": muc, "soTepBangChung": so_tep,
                    "bangChung": xac_nhan,
                    "text": ma_nguon[ma]["text"]})

    # ---------- in bảng ----------
    print(f"{'MÃ YCCĐ':13s}{'MỨC':11s}{'BẰNG CHỨNG TRONG MÃ'}")
    print("-" * 100)
    for k in ket:
        tep = ", ".join(x["tep"] for x in k["bangChung"]) or "—"
        print(f"{k['ma']:13s}{k['muc']:11s}{tep}")

    from collections import Counter
    c = Counter(k["muc"] for k in ket)
    print("-" * 100)
    print(f"PHỦ MẠNH: {c.get('PHỦ MẠNH',0)}  ·  PHỦ: {c.get('PHỦ',0)}  ·  "
          f"CHƯA PHỦ: {c.get('CHƯA PHỦ',0)}  ·  TỔNG: {sum(c.values())}/{len(ma_nguon)}")
    con = [k["ma"] for k in ket if k["muc"] == "CHƯA PHỦ"]
    print("chưa phủ:", con or "KHÔNG CÒN")

    # cốt lõi và mở rộng
    loi_core = [k["ma"] for k in ket if k["loai"] != "mở rộng" and k["muc"] == "CHƯA PHỦ"]
    print(f"\nYCCĐ CỐT LÕI chưa phủ ({len(loi_core)}):", loi_core or "KHÔNG CÒN")

    if loi_bc:
        print(f"\n❌ {len(loi_bc)} BẰNG CHỨNG KHÔNG HỢP LỆ (khai báo sai, không được bỏ qua):")
        for l in loi_bc:
            print("   ", l)
        return 1

    json.dump(ket, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\nđã ghi -> {OUT}")
    if strict and con:
        print(f">>> --strict: còn {len(con)} yêu cầu chưa phủ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
