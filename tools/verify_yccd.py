#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""YCCĐ lớp 10 — verify bản chép tay bằng SUBSEQUENCE + Ô ĐẶC HIỆU NHẤT (v7).

SÁU LẦN THẤT BẠI TRƯỚC (ghi lại để không lặp):
  v1   trích PDF không giữ layout -> 3 cột xen kẽ ("con động của con hệ thống AI người")
  v1.5 cắt cột cố định             -> lệch 1-2 kí tự làm mất chữ "10." của mã, ra 21/22
  v2   toạ độ theo từng TRANG      -> cắt giữa trang ("thực|hiện"); dính YCCĐ lớp 11
  v3   lọc tiêu đề theo TỪ         -> xoá mất "đề"/"cầu" TRONG nội dung thật
  v4   lọc theo dòng, 2 phương pháp-> chữ tràn trái cột ("ứng dụng" -> "ng dụng")
  v5   verify bằng CỤM 4 TỪ LIỀN MẠCH -> 17/22; 5 câu "thiếu từ khoá" là GIẢ:
       PDF chèn cột trái VÀO GIỮA từ ghép, vd ô 10.B2.1 =
         "...vi phạm quy định của nhà [có trách khi sử dụng ai] trường hoặc..."
       cụm "nhà trường" không liền mạch nên không tìm thấy — dù chữ có đủ.
  v6   verify bằng TẬP HỢP TỪ + từ khoá liền mạch -> 18/22; còn 4 lỗi GIẢ:
       (a) 3 từ khoá "nhà trường"/"hình ảnh"/"phản hồi" vẫn dùng khớp LIỀN MẠCH
           nên vẫn dính đúng bẫy v5 (recall từ đã = 1.000 cả 22 câu, tức chữ có đủ).
       (b) 10.A2.1 biên cách biệt 1.00 -> KHÔNG PHẢI gán sai mã, mà vì 10.A2.MR1
           là BẢN MỞ RỘNG của chính nó ("...đem lại" + "thông qua một dự án sáng
           tạo AI") nên hai ô trùng tập từ. Đây là cấu trúc thật của Khung.

PHÉP KIỂM ĐÚNG (v7) — khớp theo THỨ TỰ nhưng CHO PHÉP rác chèn giữa:
  1. SUBSEQUENCE ĐẦY ĐỦ: mọi từ của câu chép tay phải xuất hiện trong ô của mã đó
     theo ĐÚNG THỨ TỰ (không cần liền mạch). Bắt lỗi chép thiếu/sai/sai thứ tự,
     mà không bị cột chèn ngang đánh lừa.
  2. Ô ĐẶC HIỆU NHẤT (phá hoà đúng cách): trong TẤT CẢ ô mà câu khớp đầy đủ,
     ô được gán phải là ô NGẮN NHẤT (khớp đặc hiệu nhất). Với cặp lõi/mở rộng
     (A2.1 ⊂ A2.MR1) thì ô A2.1 ngắn hơn -> gán đúng, không cần ngưỡng biên.
     Bắt lỗi chép câu này sang mã kia mà không cần đoán ngưỡng.
  3. TỪ KHOÁ THEO THỨ TỰ: các từ của mỗi từ khoá phải có mặt trong ô theo đúng
     thứ tự (không liền mạch) -> chống chèn ngang, vẫn bắt lỗi chép nhầm câu.
  4. TẬP MÃ: đúng 22 mã, khớp tập mã PDF tìm thấy trong vùng LỚP 10.
Chỉ khi cả 22 câu đạt cả 4 phép mới ghi JSON. Không đạt thì KHÔNG ghi.
"""
import json, re, subprocess, sys

PDF = "/home/hitokiri/ieeai2026/research/src/2422_PL_khung.pdf"
OUT = "/home/hitokiri/ieeai2026/yccd_lop10_sach.json"
CODE_RE = re.compile(r'10\.[A-D]\d\.(?:MR)?\d+\.')

# Bản chép tay từ `pdftotext -layout 2422_PL_khung.pdf` trang 37-39, vùng LỚP 10.
# Cột "Yêu cầu cần đạt" ở bản -layout hiển thị đúng, người đọc được.
GT = {
 "10.A1.1": ("Thực hành xác định được vai trò của con người trong sử dụng, vận hành, tùy chỉnh một hệ thống AI cụ thể.",
             ["thực hành", "vai trò", "tùy chỉnh"]),
 "10.A1.2": ("Giải thích được tại sao việc con người kiểm soát AI là quan trọng, thông qua việc liên hệ đến các giá trị như an toàn, công bằng và quyền lợi con người.",
             ["giải thích", "kiểm soát", "công bằng", "quyền lợi"]),
 "10.A2.1": ("Nêu được một số rủi ro đối với con người, xã hội mà một sản phẩm AI có thể đem lại.",
             ["rủi ro", "xã hội", "đem lại"]),
 "10.A2.MR1": ("Nêu được một số biện pháp hạn chế các rủi ro đối với con người, xã hội mà một sản phẩm AI có thể đem lại thông qua một dự án sáng tạo AI.",
               ["biện pháp", "hạn chế", "sáng tạo"]),
 "10.A3.1": ("Kể tên được một vài quy định hoặc luật lệ (ở mức độ khái niệm, ví dụ: Luật An ninh mạng, Luật Dữ liệu, Luật Bảo vệ dữ liệu cá nhân) có chức năng bảo vệ người dùng trong không gian số.",
             ["luật lệ", "khái niệm", "bảo vệ", "không gian số"]),
 "10.B2.1": ("Nêu được ví dụ về hành vi sử dụng AI hoặc sự cố liên quan đến AI vi phạm quy định của nhà trường hoặc các văn bản pháp luật liên quan đến sử dụng công nghệ thông tin.",
             ["hành vi", "sự cố", "vi phạm", "nhà trường", "pháp luật"]),
 "10.B2.MR1": ("Nhận biết được một số dấu hiệu của nội dung do AI tạo sinh tạo ra; kiểm tra và nhận xét được mức độ minh bạch của việc khai báo sử dụng AI trong một sản phẩm.",
               ["dấu hiệu", "tạo sinh", "minh bạch", "khai báo"]),
 "10.B3.1": ("Trình bày được ví dụ minh họa một số vấn đề đạo đức có thể phát sinh trong quá trình thiết kế và vận hành AI (như thiên vị dữ liệu, vi phạm quyền riêng tư hoặc thiếu minh bạch).",
             ["đạo đức", "thiên vị", "riêng tư", "minh bạch"]),
 "10.C2.1": ("Xác định được các vấn đề thực tế có thể ứng dụng AI để thực hiện. Ưu tiên các vấn đề gần gũi, cần thiết trong bối cảnh Việt Nam, chẳng hạn: sản xuất nông nghiệp, các vấn đề liên quan đến các cộng đồng thiểu số, …",
             ["thực tế", "ưu tiên", "việt nam", "nông nghiệp", "thiểu số"]),
 "10.C2.2": ("Liệt kê được tên các ứng dụng AI theo các tính năng của hệ thống.",
             ["liệt kê", "tính năng"]),
 "10.C2.3": ("Nêu được ví dụ một số trường hợp sử dụng AI hỗ trợ quá trình học tập.",
             ["trường hợp", "hỗ trợ", "học tập"]),
 "10.C2.MR1": ("Xác định được các yêu cầu cần có đối với việc ứng dụng AI thực hiện nhiệm vụ cụ thể.",
               ["yêu cầu", "nhiệm vụ"]),
 "10.C2.MR2": ("Sử dụng được một số ứng dụng AI trong học tập.",
               ["sử dụng", "học tập"]),
 "10.C3.1": ("Mô tả được các yêu cầu để đưa ra prompt phù hợp với mục tiêu cụ thể.",
             ["mô tả", "prompt", "mục tiêu"]),
 "10.C3.2": ("Thực hành đặt prompt giải quyết một số vấn đề gần gũi trong cuộc sống, học tập một cách hiệu quả.",
             ["thực hành", "prompt", "gần gũi", "hiệu quả"]),
 "10.C3.3": ("Phân biệt được AI tạo sinh với các hệ thống AI phân loại, dự đoán qua ví dụ cụ thể.",
             ["phân biệt", "tạo sinh", "phân loại", "dự đoán"]),
 "10.C3.MR1": ("Trình bày được ví dụ mô tả một số công nghệ để thiết kế và tạo AI.",
               ["công nghệ", "thiết kế"]),
 "10.C4.1": ("Phân tích được sự ảnh hưởng của chất lượng dữ liệu đến chất lượng AI.",
             ["phân tích", "ảnh hưởng", "chất lượng", "dữ liệu"]),
 "10.C4.MR1": ("Phân tích được các dạng dữ liệu (hình ảnh, âm thanh, từ ngữ, …) được sử dụng để huấn luyện AI.",
               ["dạng", "hình ảnh", "âm thanh", "từ ngữ", "huấn luyện"]),
 "10.D1.1": ("Nêu được ví dụ cụ thể, xác định nhiệm vụ hoặc mục tiêu cụ thể mà một hệ thống AI cần thực hiện, nêu được mối liên hệ giữa mục tiêu đó với các thành phần chính của hệ thống.",
             ["nhiệm vụ", "mục tiêu", "liên hệ", "thành phần"]),
 "10.D2.1": ("Mô tả được các thành phần cơ bản của hệ thống AI (dữ liệu, mô hình, thuật toán, đầu ra, phản hồi) phù hợp với nhiệm vụ cụ thể.",
             ["thành phần", "cơ bản", "mô hình", "thuật toán", "phản hồi"]),
 "10.D2.2": ("Nêu được ví dụ về một số vấn đề phát sinh trong quá trình vận hành hoặc tối ưu hoá AI và trình bày được ý nghĩa của việc khắc phục các vấn đề đó.",
             ["phát sinh", "vận hành", "tối ưu hoá", "khắc phục"]),
}

TU_RE = re.compile(r"[a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễ"
                   r"ìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữ"
                   r"ỳýỵỷỹđ]+")


def n(s):
    return re.sub(r'\s+', ' ', (s or '').lower()).strip()


def tu(c):
    return [w for w in TU_RE.findall(n(c)) if len(w) > 1]


def subseq_match(nhay, kim):
    """kim có phải là subsequence (theo thứ tự, không cần liền mạch) của nhay không.
    Trả về (khớp_hết, số_từ_khớp, vị_trí_dừng)."""
    i, hit = 0, 0
    for w in nhay:
        if i < len(kim) and w == kim[i]:
            i += 1; hit += 1
    return i == len(kim), hit, i


def vung_lop10():
    txt = subprocess.run(["pdftotext", "-layout", PDF, "-"],
                         capture_output=True, text=True).stdout
    lines = txt.split("\n")
    i = next(k for k, l in enumerate(lines) if re.search(r'LỚP 10', l))
    j = next(k for k, l in enumerate(lines) if re.search(r'LỚP 11', l) and k > i)
    return "\n".join(lines[i + 1:j])


def cat_o(vung):
    found = [(m.group(0).rstrip('.'), m.start()) for m in CODE_RE.finditer(vung)]
    return {ma: vung[pos:(found[k + 1][1] if k + 1 < len(found) else len(vung))]
            for k, (ma, pos) in enumerate(found)}


def main():
    vung = vung_lop10()
    o = cat_o(vung)
    o_tu = {ma: tu(t) for ma, t in o.items()}
    print(f"vùng LỚP 10: {len(vung)} kí tự | PDF có {len(o)} ô mã | chép tay {len(GT)} câu")

    # PHÉP 4: tập mã
    if set(GT) != set(o):
        print("❌ tập mã lệch:", sorted(set(GT) ^ set(o)), file=sys.stderr)
        return 1
    if len(GT) != 22:
        print(f"❌ số câu != 22 (được {len(GT)})", file=sys.stderr)
        return 1

    loi, ket = [], []
    print(f"\n{'MÃ':12s} {'subseq':>13s} {'ô đặc hiệu nhất':>26s} {'từkhoá':>7s}  KẾT LUẬN")
    print("-" * 84)
    for ma in sorted(GT, key=lambda m: (m[3], m[4],
                                        int(re.sub(r'\D', '', m.split('.')[-1]) or 0),
                                        'MR' in m)):
        cau, kws = GT[ma]
        kim = tu(cau)

        # PHÉP 1: subsequence đầy đủ trong ô của chính mã này
        ok1, hit, _ = subseq_match(o_tu[ma], kim)

        # PHÉP 2: trong mọi ô khớp đầy đủ, ô được gán phải NGẮN NHẤT (đặc hiệu nhất)
        khop = [m2 for m2, t2 in o_tu.items() if subseq_match(t2, kim)[0]]
        ngan_nhat = min(khop, key=lambda m2: len(o[m2])) if khop else None
        ok2 = (ngan_nhat == ma)

        # PHÉP 3: từ khoá theo thứ tự (không cần liền mạch)
        kw_loi = [k for k in kws if not subseq_match(o_tu[ma], tu(k))[0]]

        ok = ok1 and ok2 and not kw_loi
        if not ok1:
            loi.append((ma, f"subsequence chỉ khớp {hit}/{len(kim)} từ theo thứ tự",
                        "chép thiếu/sai chữ hoặc sai thứ tự"))
        if not ok2:
            loi.append((ma, f"ô đặc hiệu nhất là {ngan_nhat} (các ô khớp: {khop})",
                        "GÁN SAI MÃ"))
        if kw_loi:
            loi.append((ma, "từ khoá không khớp theo thứ tự", ", ".join(kw_loi)))

        print(f"{ma:12s} {('✅ %d/%d'%(hit,len(kim))) if ok1 else ('❌ %d/%d'%(hit,len(kim))):>13s} "
              f"{('✅ '+ma) if ok2 else ('❌ '+str(ngan_nhat)):>26s} "
              f"{len(kws)-len(kw_loi)}/{len(kws):<5d}  {'✅ đạt' if ok else '❌ LỆCH'}")

        ket.append({"ma": ma, "text": cau, "chuDe": ma.split('.')[1],
                    "loai": "mở rộng" if "MR" in ma else "cốt lõi",
                    "verify": {"subseq": f"{hit}/{len(kim)}", "subseqDayDu": ok1,
                               "oDacHieuNhat": ok2, "cacOKhop": khop,
                               "tuKhoa": f"{len(kws)-len(kw_loi)}/{len(kws)}", "dat": ok},
                    "nguon": "QĐ 2422/QĐ-BGDĐT (18/8/2026), Phụ lục Khung nội dung GD AI, lớp 10"})

    print("-" * 84)
    dat = sum(1 for r in ket if r["verify"]["dat"])
    print(f"KẾT QUẢ: {dat}/{len(ket)} câu đạt cả 4 phép kiểm")
    if loi:
        print("LỖI:")
        for l in loi:
            print("   ", l)
        print("\n>>> CHƯA ĐẠT — không ghi file.", file=sys.stderr)
        return 1

    json.dump(ket, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(f">>> ĐẠT. Đã ghi {len(ket)} YCCĐ đã verify → {OUT}\n")
    for r in ket:
        print(f"{r['ma']:12s} [{r['loai']:8s}] {r['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
