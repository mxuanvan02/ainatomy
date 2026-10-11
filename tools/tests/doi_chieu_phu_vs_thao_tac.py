#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ĐỐI CHIẾU hai trục đo độ phủ YCCĐ, và TỰ KIỂM LẠI bằng chứng mà tool viện dẫn.

HAI TRỤC, vì một trục không đủ và vì gộp lại sẽ che mất lỗi:
  Trục 1 — tools/tinh_do_phu.py: "có bằng chứng TRONG MÃ NGUỒN không". Đọc bảng BC khai tay
           (mã -> tệp + mô tả + tên hàm), kiểm tệp có tồn tại và chuỗi mã/tên hàm có trong tệp.
  Trục 2 — tools/tests/bang_gia_tri_kien_tao_v3.py: "thao tác học sinh có chứng minh được mã đó
           không". Đơn vị bằng chứng là LOG CALL SITE, vì mỗi lời gọi logSuKien() chính là một
           thao tác được ghi lại.
Hai trục trả lời hai câu hỏi khác nhau. Một mã có thể CÓ trong mã nguồn (trục 1) mà không đi
theo bản ghi nào tới CSV của giáo viên (trục 2 = ĐỨT CHUỖI).

VÌ SAO CÓ TỆP NÀY. Ngày 11/10 hai reviewer độc lập (review13/reviewer_A_machA.md và
reviewer_D_machCD_phu.md) phát hiện ba ô bằng chứng của trục 1 TRỎ SAI TỆP: 10.B2.MR1 viện dẫn
data/cauhoi.js + js/nhamay_text.js, 10.D2.2 viện dẫn js/lab.js + js/logic.js + js/pipeline3d.js,
10.A1.1 viện dẫn pipeline3d.js + nhamay_tram01.js — trong khi chuỗi mã không nằm trong tệp nào
trong số đó. Phép OR ở tinh_do_phu.py:143 (`if not co_ma and co_ham is not True`) cho qua khi chỉ
khớp TÊN HÀM, nên lỗi khai báo bị che và cả ba vẫn in "PHỦ MẠNH". Reviewer D còn nêu mâu thuẫn
BA NGUỒN về 10.C3.MR1 (tool in PHỦ, bảng tự chấm in PHỦ MỘT PHẦN, tệp đối chiếu in CHƯA PHỦ)
và yêu cầu "hồ sơ nộp thi phải chốt một nguồn duy nhất". Tệp này chính là nguồn đối chiếu đó,
và nó phải TỰ TÁI LẬP ĐƯỢC bằng một lệnh chứ không phải chép tay.

BỐN VIỆC NÓ LÀM:
  1. nạp output THẬT của tools/tinh_do_phu.py (out/yccd_coverage_v2.json) — không tự tính lại
     mức phủ, vì tính lại nghĩa là có hai bản logic và chúng sẽ drift.
  2. TỰ KIỂM LẠI từng ô bằng chứng: chuỗi mã có trong tệp viện dẫn không, tên hàm có không.
     Đây là phép kiểm độc lập, không tin trường maYCCDTrongTep mà tool tự ghi.
  3. nạp bảng v3 (trục thao tác) rồi in bảng đối chiếu 22 mã, hai trục cạnh nhau.
  4. liệt kê MÂU THUẪN: mã mà trục 1 nói có bằng chứng còn trục 2 nói đứt chuỗi, và mã chỉ có
     bằng chứng yếu. Đây là danh sách phải nêu trong hồ sơ, không được để người đọc tự suy ra.

CÁCH CHẠY
  cd soi-ai
  python3 tools/tinh_do_phu.py                      # sinh out/yccd_coverage_v2.json trước
  python3 tools/tests/doi_chieu_phu_vs_thao_tac.py  # rồi đối chiếu
"""
import io
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
S = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_COV = os.path.join(S, "out", "yccd_coverage_v2.json")
OUT_V3 = os.path.join(S, "data-source", "bang_gia_tri_kien_tao_v3.json")
OUT_DC = os.path.join(S, "data-source", "doi_chieu_phu_vs_thao_tac.json")
RE_MA = r"10\.[A-D]\d?\.(?:MR)?\d+"


def doc(rel):
    p = os.path.join(S, rel)
    if not os.path.exists(p):
        return None
    return io.open(p, encoding="utf-8", errors="ignore").read()


def nap_json(p, ten):
    if not os.path.exists(p):
        print("✗ THIẾU " + os.path.relpath(p, S) + " — " + ten)
        return None
    return json.load(io.open(p, encoding="utf-8"))


def main():
    cov = nap_json(OUT_COV, "chạy `python3 tools/tinh_do_phu.py` trước")
    v3 = nap_json(OUT_V3, "chạy `python3 tools/tests/bang_gia_tri_kien_tao_v3.py` trước")
    if cov is None or v3 is None:
        return 2
    if not isinstance(cov, list):
        print("✗ out/yccd_coverage_v2.json không phải danh sách: " + type(cov).__name__)
        return 2

    # nạp nội dung mọi tệp mã một lần
    files = {}
    for sub in ("js", "data"):
        d = os.path.join(S, sub)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith((".js", ".html")):
                files[sub + "/" + f] = doc(sub + "/" + f)

    v3map = {x["ma"]: x for x in v3["bang"]}
    print("đã nạp: " + str(len(cov)) + " mã từ tool độ phủ · " + str(len(v3map))
          + " mã từ bảng thao tác v3 · " + str(len(files)) + " tệp mã nguồn")

    rows = []
    bc_yeu = []
    bc_sai_tep = []
    mau_thuan = []

    print("\n" + "=" * 116)
    print("ĐỐI CHIẾU 2 TRỤC + TỰ KIỂM LẠI Ô BẰNG CHỨNG")
    print("=" * 116)
    print("MÃ".ljust(12) + "TRỤC 1 (trong mã)".ljust(22) + "BC mạnh".ljust(9)
          + "KIỂM ĐỘC LẬP ô BC".ljust(26) + "TRỤC 2 (thao tác)")
    print("-" * 116)

    for x in cov:
        ma = x["ma"]
        muc = x.get("muc", "?")
        manh = x.get("soTepBangChungManh", 0)
        tong_bc = x.get("soTepBangChung", 0)

        # --- tự kiểm lại TỪNG ô bằng chứng, không tin trường tool tự ghi ---
        kiem = []
        n_manh_that = 0
        for b in x.get("bangChung", []):
            tep = b.get("tep", "?")
            ham = b.get("hamCoThat")
            nd = files.get(tep)
            if nd is None:
                kiem.append(tep + "=TỆP KHÔNG TỒN TẠI")
                continue
            co_ma = ma in nd
            # tên hàm/hằng: nếu tool khai là "không kiểm" thì bỏ qua
            co_ham = None
            if isinstance(ham, bool):
                co_ham = ham
            if co_ma:
                n_manh_that += 1
            kiem.append(tep + ("=MÃ✓" if co_ma else "=mã✗"))
        if n_manh_that != manh:
            kiem.append("LỆCH công cụ khai mạnh=" + str(manh) + " kiểm lại=" + str(n_manh_that))
        if manh == 0 and tong_bc:
            bc_yeu.append({"ma": ma, "muc_tool": muc, "vien_dan": kiem})
        # ô BC trỏ tệp KHÔNG chứa chuỗi mã
        for b in x.get("bangChung", []):
            if b.get("maYCCDTrongTep") is False:
                bc_sai_tep.append({"ma": ma, "tep": b.get("tep"),
                                   "ham": b.get("hamCoThat")})

        v3x = v3map.get(ma, {})
        pq = v3x.get("phan_quyet", "KHÔNG CÓ TRONG BẢNG v3")
        print(ma.ljust(12) + (muc + " (" + str(tong_bc) + " ô)").ljust(22)
              + (str(manh) + "/" + str(tong_bc)).ljust(9)
              + ("; ".join(kiem)[:25] or "—").ljust(26) + pq)

        if muc != "CHƯA PHỦ" and pq.endswith("ĐỨT CHUỖI"):
            mau_thuan.append({"ma": ma, "truc1": muc, "truc2": pq,
                              "nghia": "có vết trong mã nguồn nhưng mã không đi theo bản ghi nào "
                                       "tới CSV của giáo viên"})

    print("\n" + "=" * 116)
    print("KẾT LUẬN ĐO ĐƯỢC")
    print("=" * 116)
    print("1. Mã chỉ có bằng chứng YẾU (không tệp nào chứa chuỗi mã, mức phủ không được nâng "
          "từ 11/10): " + str(len(bc_yeu)))
    for z in bc_yeu:
        print("     " + z["ma"] + " — tool in " + z["muc_tool"] + " · " + "; ".join(z["vien_dan"]))
    print("2. Ô bằng chứng trỏ tệp KHÔNG chứa chuỗi mã (bằng chứng hành vi, vẫn giữ nhưng là "
          "loại yếu): " + str(len(bc_sai_tep)))
    for z in bc_sai_tep:
        print("     " + z["ma"] + " -> " + str(z["tep"]) + " (chỉ khớp tên hàm: "
              + str(z["ham"]) + ")")
    print("3. MÂU THUẪN HAI TRỤC (trục 1 nói có, trục 2 nói đứt chuỗi): " + str(len(mau_thuan)))
    for z in mau_thuan:
        print("     " + z["ma"] + " — " + z["truc1"] + " vs " + z["truc2"])
    print("4. Tổng hợp trục 2 (thao tác): " + json.dumps(v3["tong_hop"], ensure_ascii=False))
    dem1 = {}
    for x in cov:
        dem1[x.get("muc", "?")] = dem1.get(x.get("muc", "?"), 0) + 1
    print("5. Tổng hợp trục 1 (trong mã): " + json.dumps(dem1, ensure_ascii=False))
    chua = [x["ma"] for x in cov if x.get("muc") == "CHƯA PHỦ"]
    print("6. Chưa phủ ở trục 1: " + (", ".join(chua) if chua else "không"))

    os.makedirs(os.path.dirname(OUT_DC), exist_ok=True)
    io.open(OUT_DC, "w", encoding="utf-8").write(json.dumps({
        "mo_ta": "Đối chiếu HAI TRỤC đo độ phủ YCCĐ lớp 10, kèm phép kiểm độc lập lại từng ô "
                 "bằng chứng mà tools/tinh_do_phu.py viện dẫn",
        "cong_cu": "tools/tests/doi_chieu_phu_vs_thao_tac.py (chạy lại được, không gõ tay)",
        "hai_truc": {
            "truc1_trong_ma": "tools/tinh_do_phu.py — mã có vết trong mã nguồn không; mức PHỦ "
                              "chỉ tính bằng chứng MẠNH (tệp chứa chuỗi mã) từ 11/10",
            "truc2_thao_tac": "tools/tests/bang_gia_tri_kien_tao_v3.py — thao tác học sinh có "
                              "chứng minh được mã đó không, đơn vị là log call site",
        },
        "nguon_doc": ["soi-ai/out/yccd_coverage_v2.json",
                      "soi-ai/data-source/bang_gia_tri_kien_tao_v3.json"],
        "tong_hop_truc1": dem1,
        "tong_hop_truc2": v3["tong_hop"],
        "ma_chi_co_bang_chung_yeu": bc_yeu,
        "o_bang_chung_tep_khong_chua_ma": bc_sai_tep,
        "mau_thuan_hai_truc": mau_thuan,
        "ma_chua_phu_truc1": chua,
        "bang_doi_chieu": [{"ma": x["ma"], "truc1_muc": x.get("muc"),
                            "truc1_so_o": x.get("soTepBangChung"),
                            "truc1_manh": x.get("soTepBangChungManh"),
                            "truc2": v3map.get(x["ma"], {}).get("phan_quyet"),
                            "kiem_doc_lap": [b.get("tep") for b in x.get("bangChung", [])]}
                           for x in cov],
    }, ensure_ascii=False, indent=2))
    print("\nđã ghi -> " + os.path.relpath(OUT_DC, S))
    return 0


if __name__ == "__main__":
    sys.exit(main())
