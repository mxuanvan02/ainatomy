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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YCCD = os.path.join(ROOT, "data-source", "yccd_lop10_sach.json")
OUT = os.path.join(ROOT, "out", "yccd_coverage_v2.json")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

# BẰNG CHỨNG: mã YCCĐ -> [(tệp, mô tả, tên hàm/hằng phải có thật trong tệp)]
# Phần tử thứ ba để trống ("") nghĩa là chỉ cần MÃ YCCĐ xuất hiện trong tệp.
BC = {
 # 10.A1.1 "Thực hành xác định được vai trò của con người trong sử dụng, vận hành, tùy chỉnh
 # một hệ thống AI cụ thể" — XOÁ HAI BẰNG CHỨNG CŨ ngày 11/10, và đây là mã duy nhất rơi về
 # CHƯA PHỦ. Lý do (reviewer A và reviewer D độc lập cùng kết luận, em verify lại bằng lệnh):
 #   · chuỗi "10.A1.1" KHÔNG xuất hiện trong bất kỳ tệp js/ hay data/ nào ngoại trừ
 #     data/yccd.js:48 — mà đó là BẢNG TRA nguyên văn 22 mã, dùng nó làm bằng chứng thì mã nào
 #     cũng thành PHỦ (tautology).
 #   · hai tệp cũ viện dẫn đều TỰ KHAI MÃ KHÁC: trạm `connguoi` trong pipeline3d.js:60 khai
 #     yccd:"10.A1.2", và câu t0-5 trong nhamay_tram01.js:87 khai 10.D2.1. Tức bằng chứng đang
 #     chứng minh hai yêu cầu khác, không phải 10.A1.1.
 #   · hai "hàm" viện dẫn là tên chung, không đặc trưng: TRAM xuất hiện 13 lần trong
 #     pipeline3d.js, CAU_HOI_T0 4 lần trong nhamay_tram01.js.
 # Nội dung dạy về vai trò con người THÌ CÓ (trạm CON NGƯỜI KIỂM thật sự dạy việc đó), nhưng
 # nó được khai cho 10.A1.2. Muốn phủ 10.A1.1 thì phải THÊM hoạt động cho học sinh THỰC HÀNH
 # xác định vai trò con người (động từ là "Thực hành xác định được", không phải "kể được") —
 # việc đó là nội dung mới, không phải sửa khai báo. tools/tao_sheet_thietke.py:159 đã tự khai
 # mã này "CHƯA PHỦ" từ trước; nay hai bảng mới khớp nhau.
 # 10.A1.1 — ĐÃ CÓ HOẠT ĐỘNG RIÊNG ngày 11/10, sau khi bốn giám khảo độc lập xác nhận mã này
 # là mã duy nhất rơi về CHƯA PHỦ. Hai ô bằng chứng cũ (pipeline3d.js với token TRAM, và
 # nhamay_tram01.js với CAU_HOI_T0) đã bị XOÁ vì chuỗi "10.A1.1" không tồn tại trong hai tệp
 # đó — chúng tự khai mã khác (trạm connguoi khai 10.A1.2, câu t0-5 khai 10.D2.1).
 # Nay trỏ vào tệp THẬT SỰ chứa mã và chứa hoạt động: js/vaitro_connguoi.js (ba câu hỏi, mỗi
 # câu một vế của động từ: SỬ DỤNG / VẬN HÀNH / TÙY CHỈNH, oracle tất định) và js/app.js
 # (hàm pipe3dVaiTro() dựng ba câu ở trạm ống dẫn, chấm rồi log kèm mã ở cấp sự kiện).
 # Cả hai tệp đều chứa chuỗi "10.A1.1" nên đây là bằng chứng LOẠI MẠNH, không phải chỉ khớp tên
 # hàm. LƯU Ý khi đọc mức phủ: hoạt động này ở mức NHẬN DIỆN, nên trục THAO TÁC
 # (tools/tests/bang_gia_tri_kien_tao_v3.py) xếp 10.A1.1 là PHỦ MỘT PHẦN, không phải PHỦ THẬT.
 "10.A1.1": [("js/vaitro_connguoi.js", "3 câu xác định vai trò con người: sử dụng, vận hành, tùy chỉnh", "MX_VAI_TRO"),
             ("js/app.js", "pipe3dVaiTro() dựng 3 câu ở trạm ống dẫn, chấm tất định, log kèm mã", "pipe3dVaiTro")],
 "10.A1.2": [("js/pipeline3d.js", "Trạm CON NGƯỜI KIỂM, đoán trạm hỏng", "TRAM")],
 "10.A2.1": [("js/tinhhuong.js", "4 tình huống rủi ro: X-quang khoa nhi, camera khuôn mặt", "NHOM_RUI_RO")],
 "10.A2.MR1": [("js/tinhhuong.js", "Tình huống dự án sáng tạo + biện pháp hạn chế rủi ro", "NHOM_RUI_RO")],
 "10.A3.1": [("data/kienthuc.js", "4 luật VN đã kiểm chứng số hiệu", "kt-01")],
 "10.B2.1": [("js/tinhhuong.js", "4 tình huống vi phạm nội quy/pháp luật", "NHOM_VI_PHAM"),
             ("js/bt09.js", "BT-09 Mức 3: học sinh tự cài một lỗi cho bạn bắt", "kiemCau")],
 # 10.B2.MR1 — TRỎ LẠI ĐÚNG TỆP ngày 11/10. Hai ô cũ (data/cauhoi.js, js/nhamay_text.js) mô tả
 # đúng hoạt động nhưng cả hai KHÔNG chứa chuỗi mã, nên chỉ là bằng chứng yếu. Nay thêm hai tệp
 # THẬT SỰ khai mã: trạm `daura` (pipeline3d.js:55, yccd:"10.B2.MR1") và NM_TRAM[5]
 # (app.js:1202) — giao diện còn in mã ra cho học sinh xem ở app.js:1561. Hai ô yếu cũ vẫn giữ
 # vì chúng là bằng chứng HÀNH VI (đấu trường soi lỗi, trạm 5 phán quyết căn cứ/bịa); cột
 # LOẠI BC trong bảng in sẽ cho thấy ô nào mạnh ô nào yếu.
 "10.B2.MR1": [("js/pipeline3d.js", "Trạm ĐẦU RA: dấu hiệu nội dung AI tạo sinh, bịa số liệu/nguồn", "daura"),
               ("js/app.js", "NM_TRAM[5] ỨNG DỤNG khai 10.B2.MR1, giao diện in mã cho HS xem", "NM_TRAM"),
               ("data/cauhoi.js", "Ngân hàng đấu trường, 5 nhóm lỗi cài sẵn", "MX_BANK"),
               ("js/nhamay_text.js", "Trạm 5: phán đoán câu trả lời có căn cứ hay bịa", "chamUngDung")],
 "10.B3.1": [("js/lab.js", "Thiên kiến ngày/đêm từ dữ liệu lệch 92%", "taoDuLieu"),
             ("js/lab3d.js", "Phòng 3D: mặt phẳng quyết định và cụm ngày/đêm", "matPhangTuTrongSo")],
 "10.C2.1": [("js/nhamay_tram01.js", "Câu hỏi t0-3: ưu tiên vấn đề Việt Nam", "CAU_HOI_T0"),
             ("js/nhamay_text.js", "4 chủ đề VN: nông nghiệp, y tế, giáo dục, môi trường", "CHU_DE")],
 # 10.C2.2 và 10.C2.3 — LỖI THẬT ĐÃ SỬA (05/10). Ô bằng chứng cũ trỏ tới "kt-02" và
 # "kt-06", nhưng chính hai item quiz đó TỰ KHAI yccd khác: kt-02 -> 10.A3.1, kt-06 ->
 # 10.C3.2. Phép kiểm cũ chỉ hỏi "item có tồn tại trong tệp không" nên hai bằng chứng
 # trỏ sai chỗ này VẪN ĐẠT và bảng độ phủ vẫn in PHỦ MẠNH. Nay trỏ đúng item (kt-03 cho
 # 10.C2.2) và trỏ đúng nội dung mới viết cho 10.C2.3 (hằng hoTroHocTap + js/bt13.js).
 "10.C2.2": [("data/kienthuc.js", "Ứng dụng AI theo 6 nhóm tính năng, có mã máy đọc", "kt-03")],
 "10.C2.3": [("data/kienthuc.js", "6 tình huống AI hỗ trợ quá trình học tập (hằng hoTroHocTap)", "hoTroHocTap"),
             ("js/bt13.js", "BT-13: xếp nhóm tính năng + nêu rõ đầu vào/đầu ra", "veTinhHuong")],
 "10.C2.MR1": [("js/tinhhuong.js", "2 tình huống xác định yêu cầu khi ứng dụng AI", "NHOM_YEU_CAU")],
 "10.C2.MR2": [("js/nhamay_text.js", "Học sinh DÙNG hệ AI thật trong trình duyệt, 0 MB, offline", "ungDung")],
 # 10.C3.1 — THÊM ô thứ hai ngày 11/10 (trước đó bảng chỉ khai một ô, tức khai THẤP hơn sự thật).
 # data/kienthuc.js chứa chuỗi "10.C3.1" ba lần, trong đó quiz kt-05 hỏi đúng động từ của YCCĐ:
 # nguyên văn YCCĐ là "Mô tả được các yêu cầu để đưa ra prompt phù hợp với mục tiêu cụ thể",
 # còn kt-05 hỏi "Prompt nào dưới đây đáp ứng ĐẦY ĐỦ nhất các yêu cầu về mục tiêu, bối cảnh,
 # định dạng và ràng buộc?" — đúng bốn loại yêu cầu đó, có oracle tất định (đáp án c).
 # js/nhamay_text.js:432 cũng chứa chuỗi mã trong tiêu đề khối chấm rubric prompt.
 # Cả hai tệp đều chứa chuỗi "10.C3.1" nên mã này là bằng chứng LOẠI MẠNH.
 # LƯU Ý mức thao tác: kt-05 là trắc nghiệm chọn 1 trong 4 = NHẬN DIỆN, nên trục THAO TÁC xếp
 # 10.C3.1 là PHỦ MỘT PHẦN, không phải PHỦ THẬT. Thao tác tự xuất thật cho mã này là học sinh
 # TỰ GÕ prompt ở trạm Nhà máy chữ (js/nhamay_text.js), được chấm bằng rubric 3 tiêu chí.
 "10.C3.1": [("js/nhamay_text.js", "Rubric 3 tiêu chí chấm prompt", "RUBRIC_PROMPT"),
             ("data/kienthuc.js", "quiz kt-05: chọn prompt đủ 4 yêu cầu, oracle tất định", "kt-05")],
 "10.C3.2": [("js/nhamay_text.js", "Thực hành đặt prompt + máy sinh trả lời", "ungDung"),
             ("data/kienthuc.js", "3 bài thực hành prompt tự chấm theo rubric", "p-02")],
 "10.C3.3": [("data/kienthuc.js", "Bảng so sánh AI tạo sinh với phân loại/dự đoán", "kt-04")],
 "10.C3.MR1": [("js/tinhhuong.js", "2 tình huống công nghệ thiết kế và tạo AI", "NHOM_YEU_CAU")],
 "10.C4.1": [("js/lab.js", "Perceptron học thật + kiểm tra tách ngày/đêm", "kiemTra"),
             ("js/lab3d.js", "Kéo tỉ lệ ảnh ngày và xem hậu quả trong không gian 3D", "doiTiLeNgay"),
             ("js/nhamay_tram01.js", "Trạm 1: dán nhãn sai làm mất 40% độ chính xác (đo thật)", "chamT1")],
 "10.C4.MR1": [("js/nhamay_tram01.js", "Trạm 0: ba dạng dữ liệu và bốn đặc trưng máy đọc", "veAnhVaDacTrung")],
 "10.D1.1": [("js/pipeline3d.js", "5 trạm và mối liên hệ mục tiêu - thành phần", "TRAM")],
 "10.D2.1": [("js/pipeline3d.js", "5 thành phần: dữ liệu, mô hình, thuật toán, đầu ra, phản hồi", "TRAM"),
             ("js/nhamay_tram01.js", "Câu hỏi t0-5 về vị trí khâu nhập liệu trong hệ thống", "CAU_HOI_T0")],
 # 10.D2.2 — TRỎ LẠI ĐÚNG TỆP ngày 11/10, cùng lý do với 10.B2.MR1. Chuỗi mã thật nằm ở
 # js/app.js:960 (câu GIẢI THÍCH in cho học sinh: "Đây chính là ý nghĩa của việc khắc phục
 # (YCCĐ 10.D2.2). Sửa ở gốc là sửa dữ liệu"), js/app.js:1199 (NM_TRAM[4] KIỂM ĐỊNH) và
 # js/lab3d.js:5 (header khai YCCĐ phủ). Ba ô cũ giữ lại làm bằng chứng hành vi.
 "10.D2.2": [("js/app.js", "NM_TRAM[4] KIỂM ĐỊNH + câu giải thích in cho HS về ý nghĩa khắc phục", "NM_TRAM"),
             ("js/lab3d.js", "header khai YCCĐ phủ + cảnh đánh giá trên bộ dữ liệu mới", "danhGia"),
             ("js/lab.js", "Đánh giá trên bộ mới: 100% ban ngày so với 59% ban đêm", "kiemTra"),
             ("js/logic.js", "Bảng nhầm lẫn: bỏ sót và bắt oan", "bangNhamLan"),
             ("js/pipeline3d.js", "Hậu quả khi từng trạm hỏng", "TRAM")],
}


def yccd_item_tu_khai(noi_dung, item_id):
    """Trả về mã YCCĐ mà CHÍNH item quiz đó khai, hoặc None nếu không tìm thấy.

    Vì sao cần: mỗi item trong data/kienthuc.js đã tự ghi `yccd:"..."` — đó là lời khai
    của chính dữ liệu. Nếu ô bằng chứng trỏ tới item đó để chứng minh một mã KHÁC thì
    bằng chứng đang chống lại lời khai của chính nó, và bảng độ phủ sẽ sai một cách rất
    khó thấy: phép kiểm cũ chỉ hỏi "item có tồn tại không", mà nó thì có tồn tại thật.
    """
    m = re.search(r'id:\s*"' + re.escape(item_id) + r'"', noi_dung)
    if not m:
        return None
    # yccd nằm ngay sau id trong cùng một object; cắt một cửa sổ đủ rộng nhưng không
    # tràn sang item kế tiếp (item kế tiếp cách xa hơn thế rất nhiều).
    y = re.search(r'yccd:\s*"([^"]+)"', noi_dung[m.end():m.end() + 400])
    return y.group(1) if y else None


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
            # LỚP KIỂM THỨ BA (thêm 05/10): nếu ô bằng chứng trỏ tới một item quiz
            # (kt-NN) thì chính item đó phải tự khai ĐÚNG mã YCCĐ đang được chứng minh.
            # Không có lớp này thì một bằng chứng trỏ sai chỗ vẫn ĐẠT, vì hai phép kiểm
            # cũ chỉ hỏi tệp có tồn tại và tên có tồn tại. Đã xảy ra thật: 10.C2.2 trỏ
            # "kt-02" trong khi kt-02 tự khai 10.A3.1, và 10.C2.3 trỏ "kt-06" mà kt-06
            # tự khai 10.C3.2 — bảng vẫn in PHỦ MẠNH cho cả hai.
            if ham and re.fullmatch(r"kt-\d+", ham):
                tu_khai = yccd_item_tu_khai(noi_dung, ham)
                if tu_khai and tu_khai != ma:
                    loi_bc.append(f"{ma}: bằng chứng TỰ MÂU THUẪN — {tep} item '{ham}' "
                                  f"tự khai yccd='{tu_khai}', không phải {ma}")
                    continue
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
        # MỨC PHỦ chỉ tính BẰNG CHỨNG MẠNH (tệp CÓ chứa chuỗi mã YCCĐ). Đây là khuyến nghị gốc
        # của reviewer D (review13/reviewer_D_machCD_phu.md): "sửa dòng 143 thành bắt buộc co_ma".
        # Trước đây một mã chỉ cần khớp TÊN HÀM ở ≥2 tệp là được in "PHỦ MẠNH" dù chuỗi mã không
        # nằm trong tệp nào — đúng trường hợp 10.A1.1, 10.B2.MR1, 10.D2.2 mà cả reviewer A và D
        # độc lập phát hiện. Nay PHỦ đòi ≥1 tệp chứa chuỗi mã, PHỦ MẠNH đòi ≥2.
        #
        # KHÔNG dùng guard "tệp chứa mã khác = trỏ nhầm chỗ": guard đó (đã thử và đã bỏ) báo oan
        # cho bằng chứng HÀNH VI hợp lệ — ví dụ js/nhamay_text.js dạy đúng nội dung 10.B2.MR1 và
        # 10.C2.1 nhưng chỉ chứa chuỗi 10.C2.MR2/10.C3.1 trong comment, nên guard kết luận nhầm là
        # trỏ sai. Một cổng kêu oan đều đặn sẽ bị người đọc bỏ qua luôn cả phần đúng của nó.
        # Bằng chứng yếu (chỉ khớp tên hàm) vẫn được GHI LẠI trong `bangChung` và đếm ở
        # `soTepBangChung` để minh bạch, nhưng KHÔNG nâng mức phủ.
        so_tep_manh = len({x["tep"] for x in xac_nhan if x["maYCCDTrongTep"] is True})
        muc = "CHƯA PHỦ" if so_tep_manh == 0 else ("PHỦ MẠNH" if so_tep_manh >= 2 else "PHỦ")

        # TÁCH HAI LOẠI BẰNG CHỨNG — thêm 11/10. ĐÂY LÀ CHỖ CON SỐ "22/22" BỊ HIỂU SAI.
        #
        # `muc` ở trên KHÔNG đổi: docstring của tệp này đã khai từ trước rằng bằng chứng yếu
        # (chỉ khớp tên hàm) vẫn được tính, và nhãn của nó là "có bằng chứng TRONG MÃ" — đúng
        # như nó đo. Lỗi thật nằm ở chỗ khác: hồ sơ và slide in chữ "22/22 yêu cầu cần đạt có
        # bằng chứng", và người đọc (giám khảo, giáo viên) hiểu thành "22/22 yêu cầu ĐÃ ĐẠT".
        # Hai câu đó khác nhau một trời một vực.
        #
        # Đo được ngày 11/10: 3 mã được tính là phủ mà chuỗi mã YCCĐ KHÔNG xuất hiện trong tệp
        # được viện dẫn — chỉ khớp tên hàm/hằng:
        #   10.A1.1    -> js/pipeline3d.js (token "TRAM"), js/nhamay_tram01.js ("CAU_HOI_T0")
        #   10.B2.MR1  -> data/cauhoi.js ("MX_BANK"), js/nhamay_text.js ("chamUngDung")
        #   10.D2.2    -> js/lab.js ("kiemTra"), js/logic.js ("bangNhamLan"), js/pipeline3d.js
        # Với 10.A1.1 thì nội dung trạm "connguoi" trong pipeline3d.js ĐÚNG là có dạy vai trò
        # con người, nhưng tệp đó không hề chứa chuỗi "10.A1.1" — nên ánh xạ là suy diễn của
        # người viết BC, không phải thứ kiểm chứng được bằng máy. Vẫn có giá trị, nhưng là
        # bằng chứng YẾU và phải được in ra là yếu, không được cộng ngang với bằng chứng mạnh.
        #
        # Cách xử lý: KHÔNG hạ `muc` (làm vậy sẽ phá check_sheet_drift.py:104 và
        # sinh_noi_dung_ho_so.py:102 đang đọc đúng nhãn cũ), mà THÊM hai trường mới để ai đọc
        # JSON cũng thấy ngay bằng chứng của mã này thuộc loại nào:
        #   soTepBangChungManh — chỉ đếm tệp CÓ chứa chuỗi mã YCCĐ
        #   bangChungManh      — True/False, tiện lọc
        ket.append({"ma": ma, "chuDe": ma_nguon[ma].get("chuDe", ma.split('.')[1]),
                    "mach": ma[3], "loai": ma_nguon[ma].get("loai", ""),
                    "muc": muc, "soTepBangChung": so_tep,
                    "soTepBangChungManh": so_tep_manh,
                    "bangChungManh": so_tep_manh > 0,
                    "bangChung": xac_nhan,
                    "text": ma_nguon[ma]["text"]})

    # ---------- in bảng ----------
    # Cột LOẠI BẰNG CHỨNG — thêm 11/10. 'MÃ' = chuỗi mã YCCĐ có thật trong tệp (kiểm bằng máy
    # được). 'HÀM' = chỉ khớp tên hàm/hằng, tức ánh xạ là suy diễn của người viết bảng BC.
    # Không có cột này thì người đọc chỉ thấy chữ 'PHỦ MẠNH' và hiểu là yêu cầu đã đạt.
    print(f"{'MÃ YCCĐ':13s}{'MỨC':11s}{'LOẠI BC':9s}{'BẰNG CHỨNG TRONG MÃ'}")
    print("-" * 108)
    for k in ket:
        tep = ", ".join(x["tep"] for x in k["bangChung"]) or "—"
        loai = "MÃ" if k["bangChungManh"] else ("HÀM" if k["soTepBangChung"] else "—")
        print(f"{k['ma']:13s}{k['muc']:11s}{loai:9s}{tep}")

    from collections import Counter
    c = Counter(k["muc"] for k in ket)
    print("-" * 108)
    # Dòng này từng in "TỔNG: 22/22" bằng sum(c.values())/len(ma_nguon) — tức "tổng số mã đã
    # xét", nhưng đọc lên y hệt "22/22 đã phủ". Khi 10.A1.1 rơi về CHƯA PHỦ (11/10, sau phản
    # biện của reviewer A và D) thì dòng đó vẫn in 22/22 trong khi thực chất là 21/22: một con
    # số tự mâu thuẫn với ngay dòng bên dưới nó ("chưa phủ: ['10.A1.1']"). Đây chính là loại số
    # chảy vào hồ sơ nộp, nên phải in ra thứ KHÔNG THỂ đọc nhầm: tách số CÓ bằng chứng khỏi
    # tổng số mã, và in kèm danh sách mã chưa phủ ngay trên cùng một dòng.
    n_phu = c.get("PHỦ MẠNH", 0) + c.get("PHỦ", 0)
    n_chua = c.get("CHƯA PHỦ", 0)
    chua = [k["ma"] for k in ket if k["muc"] == "CHƯA PHỦ"]
    print(f"PHỦ MẠNH: {c.get('PHỦ MẠNH',0)}  ·  PHỦ: {c.get('PHỦ',0)}  ·  "
          f"CHƯA PHỦ: {n_chua}" + (f" ({', '.join(chua)})" if chua else "")
          + f"\nCÓ BẰNG CHỨNG TRONG MÃ: {n_phu}/{len(ma_nguon)}"
          + (f" — KHÔNG PHẢI {len(ma_nguon)}/{len(ma_nguon)}" if n_chua else "")
          + "  (đọc là 'có vết trong mã nguồn', không phải 'học sinh đã đạt')")
    manh = [k["ma"] for k in ket if k["bangChungManh"]]
    yeu = [k["ma"] for k in ket if not k["bangChungManh"] and k["soTepBangChung"]]
    print(f"\ntrong đó: {len(manh)}/22 mã có bằng chứng LOẠI MẠNH (chuỗi mã YCCĐ xuất hiện trong tệp), "
          f"{len(yeu)}/22 chỉ có bằng chứng LOẠI YẾU (khớp tên hàm/hằng).")
    if yeu:
        print("  mã chỉ có bằng chứng yếu: " + ", ".join(yeu))
    # Câu này là lý do tồn tại của cả khối: chữ 'PHỦ' ở đây nghĩa là 'có vết trong mã nguồn',
    # KHÔNG nghĩa là 'học sinh đã đạt yêu cầu'. Ai chép con số 22/22 vào hồ sơ mà không kèm
    # câu này thì đang để người đọc hiểu sai. Chiều đo thật về thao tác học sinh nằm ở
    # tools/tests/bang_gia_tri_kien_tao.py (PHỦ THẬT / PHỦ MỘT PHẦN / CHƯA PHỦ).
    print("\nLƯU Ý CÁCH ĐỌC: 'PHỦ' ở đây = CÓ BẰNG CHỨNG TRONG MÃ NGUỒN, không phải "
          "'học sinh đã đạt yêu cầu'.")
    print("  Độ phủ đo từ THAO TÁC học sinh (có chấm + ghi nhật ký) nằm ở tệp khác:")
    print("  python3 tools/tests/bang_gia_tri_kien_tao.py")
    con = [k["ma"] for k in ket if k["muc"] == "CHƯA PHỦ"]
    print("\nchưa phủ:", con or "KHÔNG CÒN")

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
