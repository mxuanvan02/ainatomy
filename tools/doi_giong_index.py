#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""ĐỔI GIỌNG VĂN v1.2.0: trung tính, không ngôi, học thuật (08/10/2026).

YÊU CẦU CỦA CHỦ SẢN PHẨM: bỏ xưng hô "em"/ngôi thứ hai, giọng văn trung tính
không có ngôi ("chỗ này làm gì thì ghi làm gì" — như các app học tập chuẩn),
tận dụng văn phong học thuật, HẠN CHẾ dấu gạch ngang "—" và dấu hai chấm ":"
trong câu chữ mới viết (không đụng câu cũ không liên quan).

PHẠM VI TỆP NÀY: index.html — toàn bộ chuỗi người dùng nhìn thấy có "em".
Các tệp js/ làm ở script doi_giong_js.py (cùng khuôn).

NGUYÊN TẮC (Luật G — không replace mù "\bem\b"):
  · "em" trong COMMENT kỹ thuật (ví dụ app.js:719 "một em bấm nhầm" nói về học
    sinh thật ở phòng lab) KHÔNG đổi — comment không phải câu chữ người dùng.
  · "trẻ em" là DANH TỪ, không phải đại từ — không đổi.
  · Mỗi phép thay là chuỗi nguyên văn + số lần kỳ vọng; lệch là DỪNG.
  · Câu mới ưu tiên bỏ luôn "—" và ":" khi viết lại được tự nhiên.

CHẠY:  python3 tools/doi_giong_index.py [--ghi]
"""
import io
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = os.path.join(ROOT, "index.html")

# (chuỗi cũ, chuỗi mới, số lần kỳ vọng). Chuỗi cũ chép NGUYÊN VĂN từ grep 08/10.
CAPS = [
    # ---- Trang chủ ----
    ("<p>Em <b>vận hành một hệ thống AI</b>, rồi tìm ra <b>chỗ nó sai</b>.</p>",
     "<p><b>Vận hành một hệ thống AI</b> và tìm ra <b>chỗ nó sai</b>.</p>", 1),
    ('<label for="in-maHS">Mã của em (thầy/cô phát — ví dụ A001)</label>',
     '<label for="in-maHS">Mã học sinh (giáo viên phát, ví dụ A001)</label>', 1),
    ("<b>ứng dụng (em dùng AI thật)</b>",
     "<b>ứng dụng (dùng AI thật)</b>", 1),
    ("<b>Tầng 3 — Bản đồ năng lực của em</b>",
     "<b>Tầng 3 — Bản đồ năng lực cá nhân</b>", 1),
    ("bảng chân lí — và bảng nhầm lẫn của chính em.",
     "bảng chân lí, kèm bảng nhầm lẫn của chính người học.", 1),
    ("dán bảng điểm lên mạng. Em chọn cách xử lí và xem giải thích kèm biện pháp hạn chế.",
     "dán bảng điểm lên mạng. Chọn cách xử lí và xem giải thích kèm biện pháp hạn chế.", 1),
    ("Hệ thống làm hỏng một trạm — em phải đoán ra trạm nào.",
     "Hệ thống làm hỏng một trạm, nhiệm vụ là đoán ra trạm nào.", 1),
    ("<h3>Em làm gì ở đây</h3>",
     "<h3>Các hoạt động chính</h3>", 1),
    # ---- Tầng 1 ----
    ("<h3>Bộ dữ liệu của em</h3>",
     "<h3>Bộ dữ liệu hiện có</h3>", 1),
    ("<h3>Nhiệm vụ: em hãy làm người kiểm định AI</h3>",
     "<h3>Nhiệm vụ kiểm định AI</h3>", 1),
    ("Nhiệm vụ của em: đọc kĩ, bấm vào câu em nghi là sai, rồi phán quyết.</p>",
     "Đọc kĩ, bấm vào câu nghi là sai, rồi phán quyết.</p>", 1),
    ("<h3>Phán quyết của em</h3>",
     "<h3>Phán quyết đã ghi</h3>", 1),
    ("</svg> Em tự cài một lỗi cho bạn bắt ",
     "</svg> Tự cài một lỗi cho bạn cùng lớp bắt ", 1),
    ('<p class="de-bai">Phần trên là em bắt lỗi của máy. Phần này đảo lại: em tự viết một câu',
     '<p class="de-bai">Phần trên là bắt lỗi của máy. Phần này đảo lại, tự viết một câu', 1),
    ("thì bài của em đạt.</p>",
     "thì bài đạt yêu cầu.</p>", 1),
    # ---- Tầng 3 ----
    ("Tầng 3 — Bản đồ năng lực AI của em</h2>",
     "Tầng 3 — Bản đồ năng lực AI cá nhân</h2>", 1),
    ("Hệ thống tự tổng hợp từ nhật ký làm bài của em. Không cần thầy/cô chấm.",
     "Hệ thống tự tổng hợp từ nhật ký làm bài, không cần giáo viên chấm.", 1),
    # ---- Lôgic & AI ----
    ("Ở trang này em sẽ thấy",
     "Trang này cho thấy", 1),
    ("<b>chính trò chơi em vừa chơi là một biểu thức lôgic</b>",
     "<b>chính trò chơi vừa chơi là một biểu thức lôgic</b>", 1),
    ("<h3>3. Bảng chân lí của chính em (bảng nhầm lẫn)</h3>",
     "<h3>3. Bảng chân lí cá nhân (bảng nhầm lẫn)</h3>", 1),
    ("Hệ thống tự đếm từ nhật ký làm bài của em — không cần thầy/cô chấm.",
     "Hệ thống tự đếm từ nhật ký làm bài, không cần giáo viên chấm.", 1),
    # ---- Kiến thức nền ----
    ("Mỗi mục có ghi nguồn tra cứu để em tự kiểm chứng.",
     "Mỗi mục có ghi nguồn tra cứu để tự kiểm chứng.", 1),
    ("Với mỗi tình huống, em chọn nhóm tính năng",
     "Với mỗi tình huống, chọn nhóm tính năng", 1),
    ("AI em đang dùng trong việc học của chính mình.",
     "AI đang dùng trong việc học của bản thân.", 1),
    ("<p class=\"chu2\">Em tự viết prompt cho tình huống, hệ thống sẽ đối chiếu với các tiêu chí bắt buộc",
     "<p class=\"chu2\">Viết prompt cho tình huống, hệ thống sẽ đối chiếu với các tiêu chí bắt buộc", 1),
    ("và chỉ ra em còn thiếu gì.",
     "và chỉ ra những tiêu chí còn thiếu.", 1),
    # ---- Nhà máy ----
    ("em hãy quay lại Tầng 1 để trả lời và được ghi nhận vào nhật ký lớp.",
     "quay lại Tầng 1 để trả lời và được ghi nhận vào nhật ký lớp.", 1),
    ("Em quan sát hiện tượng rồi đoán xem trạm nào đang hỏng. Hệ thống biết trước đáp án",
     "Quan sát hiện tượng rồi đoán xem trạm nào đang hỏng. Hệ thống biết trước đáp án", 1),
    ("nên báo ngay sau mỗi lần em đoán.</p>",
     "nên báo ngay sau mỗi lần đoán.</p>", 1),
    ("<h3>Em đoán trạm nào đang hỏng?</h3>",
     "<h3>Đoán trạm nào đang hỏng?</h3>", 1),
    ("Em đi lần lượt từ trái sang phải. Trạm nào em cũng tự tay làm một việc,",
     "Đi lần lượt từ trái sang phải. Trạm nào cũng tự tay làm một việc,", 1),
    ('<p class="chu2">Máy tính không "nhìn" ảnh như em. Nó chỉ đọc các <b>con số</b>.',
     '<p class="chu2">Máy tính không "nhìn" ảnh như con người. Nó chỉ đọc các <b>con số</b>.', 1),
    ("Trạm này mở nắp cho em thấy ba dạng dữ liệu và cách mỗi dạng được đổi thành số.</p>",
     "Trạm này mở nắp cho thấy ba dạng dữ liệu và cách mỗi dạng được đổi thành số.</p>", 1),
    ("<b>chính em dán nhãn</b>. Sau đó hệ thống huấn luyện hai mô hình: một mô hình học",
     "<b>chính người học dán nhãn</b>. Sau đó hệ thống huấn luyện hai mô hình, một mô hình học", 1),
    ("từ nhãn của em, một mô hình học từ nhãn đúng. Cả hai được kiểm tra trên cùng một",
     "từ nhãn vừa dán, một mô hình học từ nhãn đúng. Cả hai được kiểm tra trên cùng một", 1),
    ("bộ ảnh mới. Nếu em dán sai, em sẽ thấy hậu quả bằng con số — không ai cần chấm bài em.</p>",
     "bộ ảnh mới. Nếu dán sai, hậu quả hiện ra bằng con số, không ai cần chấm bài.</p>", 1),
    ("rất chăm chỉ và học đúng những gì em dạy — kể cả khi em dạy sai. Đây chính là nội dung",
     "rất chăm chỉ và học đúng những gì được dạy, kể cả khi dạy sai. Đây chính là nội dung", 1),
    ("<h3>Trạm 5 · ỨNG DỤNG — em dùng một hệ AI thật, chạy ngay trong máy này</h3>",
     "<h3>Trạm 5 · ỨNG DỤNG — dùng một hệ AI thật, chạy ngay trong máy này</h3>", 1),
    ('<label for="nm-prompt">Em hãy hỏi hệ một câu:</label>',
     '<label for="nm-prompt">Đặt một câu hỏi cho hệ thống</label>', 1),
    ("Việc của em là tìm ra câu đó.</p>",
     "Nhiệm vụ là tìm ra câu đó.</p>", 1),
    ("</svg> Bây giờ em làm người kiểm định.</b>",
     "</svg> Bây giờ đến vai người kiểm định.</b>", 1),
    # ---- Tình huống ----
    ("Em chọn cách xử lí, hệ thống giải thích ngay và nêu biện pháp hạn chế rủi ro.</p>",
     "Chọn cách xử lí, hệ thống giải thích ngay và nêu biện pháp hạn chế rủi ro.</p>", 1),
    # ---- Phiên bản chân trang (G10d khoá khớp meta.js) ----
    ("Phiên bản 1.1.0 · Đóng gói 08/10/2026",
     "Phiên bản 1.2.0 · Đóng gói 08/10/2026", 1),
]

def main():
    ghi = "--ghi" in sys.argv
    s = io.open(TARGET, encoding="utf-8").read()
    loi = []
    for cu, moi, n in CAPS:
        k = s.count(cu)
        if k != n:
            loi.append(f"khớp {k}/{n}: {cu[:70]!r}")
        s = s.replace(cu, moi)
    if loi:
        print(f"DỪNG — {len(loi)} chuỗi không khớp kỳ vọng, KHÔNG ghi:")
        for l in loi:
            print("  !", l)
        return 1
    print(f"  ✅ {len(CAPS)}/{len(CAPS)} chuỗi khớp kỳ vọng")

    # Chốt chặn sau thay: còn "em" NGÔI (không phải "trẻ em", không trong comment) không?
    import re
    song = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    con = re.findall(r"(?<!trẻ )\bem\b|\bEm\b", song)
    print(f"  còn 'em' ngôi trong mã sống (bỏ comment, bỏ 'trẻ em'): {len(con)}")
    for m in re.finditer(r".{0,60}(?:(?<!trẻ )\bem\b|\bEm\b).{0,60}", song):
        print("    |", m.group(0).replace("\n", " ")[:130])

    if not ghi:
        print("\n(CHẾ ĐỘ CHỈ KIỂM — thêm --ghi để ghi.)")
        return 0
    io.open(TARGET, "w", encoding="utf-8").write(s)
    print("\nĐÃ GHI index.html")
    return 0

if __name__ == "__main__":
    sys.exit(main())
