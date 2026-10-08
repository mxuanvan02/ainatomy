#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""ĐỔI GIỌNG VĂN v1.2.0 cho tầng js/ — trung tính, không ngôi, học thuật (08/10/2026).

Anh em với tools/doi_giong_index.py (tệp kia làm index.html). Cùng nguyên tắc:
mỗi phép thay là CHUỖI NGUYÊN VĂN + số lần kỳ vọng, lệch là DỪNG; không replace mù.

BA NHÓM ĐƯỢC GIỮ CÓ CHỦ ĐÍCH (đây là phần quyết định của tệp này):
1. `tuKhoa` trong js/muc3.js — KHÔNG phải chữ hiển thị, mà là DANH SÁCH TỪ KHỚP để
   chấm bài học sinh TỰ VIẾT ("em sẽ", "em chỉ", "do em"…). Học sinh viết bằng ngôi
   thứ nhất, nên đổi các từ khoá này là LÀM HỎNG MÁY CHẤM: bài đúng sẽ bị chấm thiếu
   tiêu chí. Giữ nguyên toàn bộ mảng tuKhoa và goiY (câu ví dụ trích lời học sinh).
2. Comment kỹ thuật nói về học sinh thật ở phòng lab ("một em bấm nhầm", "hai em dùng
   chung một máy", "cho một em" trong chú thích CSV) — comment không phải câu chữ
   người dùng đọc, và "một em" ở đó là danh từ chỉ một học sinh, đúng nghĩa.
3. `mau` trong js/nhamay_text.js — đây là LỜI CỦA MỘT HỆ AI ĐANG XÚI học sinh lộ dữ
   liệu cá nhân, tức lời thoại trong bài học. Hệ ngoài đời thật xưng hô với người dùng
   bằng "em"; đổi thành trung tính sẽ làm弱 bài học về thủ đoạn thao túng. Giữ.
4. HAI NGÂN HÀNG CÂU HỎI data/cauhoi.js và data/cauhoi_moRong.js — "em" ở đây nằm
   TRONG NỘI DUNG HỌC THUẬT, không phải câu chữ giao diện:
     · cauhoi.js: "Em nên đặt mật khẩu dài…" là các CLAIM của đề bài (có claim đúng,
       có claim mang định kiến). Trường `giaiThich` và nhãn `loaiLoi` trích NGUYÊN VĂN
       chữ đó; đổi claim mà không đổi giải thích là làm đề lệch đáp án.
     · cauhoi_moRong.js: "cứ 10 em thì có 4,1 em" là SỐ LIỆU BỊA được cài làm lỗi, và
       `giaiThich` trích đúng cụm `'4,1/10 em'` để chỉ dấu hiệu nhận biết. Đổi chữ số
       liệu là xoá luôn bằng chứng của nhãn.
   Thêm lý do vận hành: 56 câu trong cauhoi_moRong.js ĐANG CHỜ tác giả duyệt nhãn qua
   duyet_nhan.html. Viết lại văn bản giữa lúc duyệt làm kết quả duyệt trỏ vào câu chữ
   không còn tồn tại. Việc đổi giọng văn trong ngân hàng (nếu muốn) phải là một lượt
   riêng, kèm chạy lại QC 12 luật và duyệt lại nhãn.
Ngoài ra "trẻ em" là danh từ, không phải đại từ — không đụng (đã đo âm giả: "Trẻ em"
viết hoa đầu chuỗi lọt lookbehind thường, nên hàm la_danh_tu_tre_em tự kiểm tiền tố).

CHẠY:  python3 tools/doi_giong_js.py [--ghi]
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# {tệp: [(chuỗi cũ, chuỗi mới, số lần kỳ vọng), …]}
BANG = {
"js/app.js": [
    ("Em chưa chốt dự đoán cho bài này.", "Chưa chốt dự đoán cho bài này.", 1),
    ("sẽ chỉ cho em thấy mình đã hiểu sai ở chỗ nào.", "sẽ cho thấy chỗ nào đang bị hiểu sai.", 1),
    ("Đúng như dự đoán: chủ đề em hỏi KHÔNG có trong ngữ liệu, nhưng máy vẫn ",
     "Đúng như dự đoán, chủ đề được hỏi KHÔNG có trong ngữ liệu nhưng máy vẫn ", 1),
    ('alert("Em hãy nhập mã của mình (ví dụ A001).")',
     'alert("Cần nhập mã học sinh (ví dụ A001).")', 1),
    ('p.title = "Bấm vào câu em nghi là SAI (nếu có)"',
     'p.title = "Bấm vào câu nghi là SAI (nếu có)"', 1),
    ('"Câu này ĐÚNG — em đã \'bắt oan\'. "', '"Câu này ĐÚNG, phán quyết vừa rồi là \'bắt oan\'. "', 1),
    ('") — em đã bỏ sót. "', '"), lỗi này đã bị bỏ sót. "', 1),
    ('" Xem kết quả của em"', '" Xem kết quả đã ghi"', 1),
    ("Kết quả của em đã được ghi vào nhật ký lớp (chỉ lưu mã ${esc(maHS)}, không lưu tên). "
     "Thầy/cô sẽ xem báo cáo tổng hợp của cả lớp.",
     "Kết quả đã được ghi vào nhật ký lớp (chỉ lưu mã ${esc(maHS)}, không lưu tên). "
     "Giáo viên sẽ xem báo cáo tổng hợp của cả lớp.", 1),
    ("trong dữ liệu huấn luyện, em dự đoán sau khi học xong",
     "trong dữ liệu huấn luyện, hãy dự đoán sau khi học xong", 1),
    ('"Theo em, MÔ HÌNH VỪA HỌC sẽ đoán ảnh này là CÓ mũ hay KHÔNG mũ?"',
     '"Theo dự đoán, MÔ HÌNH VỪA HỌC sẽ đoán ảnh này là CÓ mũ hay KHÔNG mũ?"', 1),
    ('"Máy này không chạy 3D — em vẫn làm được bài ở bảng dưới dạng chữ."',
     '"Máy này không chạy 3D, bài vẫn làm được ở bảng dưới dạng chữ."', 1),
    ("một trạm: em dự đoán hiện tượng gì sẽ xuất hiện",
     "một trạm, hãy dự đoán hiện tượng gì sẽ xuất hiện", 1),
    ("<b>Chưa đúng.</b> Em đoán <b>", "<b>Chưa đúng.</b> Dự đoán là <b>", 1),
    ('moTa:"Chính em dán nhãn cho từng ảnh. Hệ huấn luyện hai mô hình — một từ nhãn của em, '
     'một từ nhãn đúng — rồi so trên cùng bộ ảnh mới. Nhãn sai thì mô hình sai có hệ thống."',
     'moTa:"Nhãn do chính người học dán. Hệ huấn luyện hai mô hình, một từ nhãn vừa dán, '
     'một từ nhãn đúng, rồi so trên cùng bộ ảnh mới. Nhãn sai thì mô hình sai có hệ thống."', 1),
    ('anDuy:"xuất xưởng — em dùng AI thật"', 'anDuy:"xuất xưởng, dùng AI thật"', 1),
    ('moTa:"Em đặt câu hỏi cho một hệ AI chạy ngay trong máy này',
     'moTa:"Đặt câu hỏi cho một hệ AI chạy ngay trong máy này', 1),
    ("NHÃN DO EM DÁN. Em dự đoán mô hình A đạt",
     "NHÃN DO CHÍNH NGƯỜI HỌC DÁN. Hãy dự đoán mô hình A đạt", 1),
    ("<b>Prompt của em đạt ${r.diem}/${r.tong} tiêu chí — ${esc(r.muc)}</b>",
     "<b>Prompt đạt ${r.diem}/${r.tong} tiêu chí, mức ${esc(r.muc)}</b>", 1),
    ('alert("Em hãy viết câu hỏi trước đã.")', 'alert("Cần viết câu hỏi trước.")', 1),
    ('alert("Em hãy sinh câu trả lời trước đã.")', 'alert("Cần sinh câu trả lời trước.")', 1),
    ("Chủ đề em hỏi <b>không có</b> trong ngữ liệu máy đã học",
     "Chủ đề được hỏi <b>không có</b> trong ngữ liệu máy đã học", 1),
    ("Thật ra đây là lời bịa: chủ đề em hỏi không có trong ngữ liệu, máy chỉ ghép chữ nghe cho xuôi.",
     "Thật ra đây là lời bịa, chủ đề được hỏi không có trong ngữ liệu nên máy chỉ ghép chữ nghe cho xuôi.", 1),
],
"js/duDoan.js": [
    ("'Dự đoán của em: <b class=\"dd-gia-tri\">50%</b>'",
     "'Dự đoán đã chốt: <b class=\"dd-gia-tri\">50%</b>'", 1),
    ('"Em dự đoán " + pct(chot)', '"Dự đoán " + pct(chot)', 1),
    ('"Em đã hình dung được mô hình hoạt động thế nào trước khi thấy kết quả — đó là điều Mức 3 muốn rèn."',
     '"Mô hình đã được hình dung trước khi thấy kết quả, đó là điều Mức 3 muốn rèn."', 1),
    ('"Viết câu trả lời của em..."', '"Viết câu trả lời..."', 1),
    ('" <b>Bài viết của em chạm "', '" <b>Bài viết chạm "', 1),
    ("chỉ liệt kê em đã chạm những phương diện nào. Em tự đọc lại bài mình ",
     "chỉ liệt kê những phương diện đã chạm. Hãy tự đọc lại bài ", 1),
],
"js/logic.js": [
    ("Đó là lí do trong Đấu trường em chỉ cần tìm đúng 1 câu có lỗi.",
     "Đó là lí do trong Đấu trường chỉ cần tìm đúng 1 câu có lỗi.", 1),
    ('<b>Phán quyết của em</b> là một biến lôgic: <code>P = TRUE</code>',
     '<b>Phán quyết</b> là một biến lôgic, <code>P = TRUE</code>', 1),
    ("<th>Em phải phán quyết</th>", "<th>Phán quyết</th>", 1),
    ("Chưa có dữ liệu. Em hãy vào <b>Đấu trường bắt lỗi AI</b>",
     "Chưa có dữ liệu. Hãy vào <b>Đấu trường bắt lỗi AI</b>", 1),
    ("làm vài câu rồi quay lại đây — bảng này sẽ hiện chính kết quả của em dưới dạng bảng chân lí.",
     "làm vài câu rồi quay lại đây, bảng này sẽ hiện chính kết quả đã làm dưới dạng bảng chân lí.", 1),
    ('<code>P</code> = "em phán quyết CÓ lỗi".', '<code>P</code> = "phán quyết CÓ lỗi".', 1),
    ("Bốn ô dưới đây là <b>bảng chân lí của chính em</b> (${bl.tong} câu đã làm):</p>",
     "Bốn ô dưới đây là <b>bảng chân lí cá nhân</b> (${bl.tong} câu đã làm).</p>", 1),
    ('<th>Em nói "Có lỗi" (P)</th>', '<th>Phán quyết "Có lỗi" (P)</th>', 1),
    ('<th>Em nói "Không lỗi" (NOT P)</th>', '<th>Phán quyết "Không lỗi" (NOT P)</th>', 1),
],
"js/kienthuc.js": [
    ("Liên hệ với em: ${esc(l.lienHe)}", "Liên hệ thực tế · ${esc(l.lienHe)}", 1),
    (">Prompt của em</label>", ">Prompt cần chấm</label>", 1),
    (">Chấm prompt của em</button>", ">Chấm prompt</button>", 1),
    ("<th>Trong prompt của em</th>", "<th>Trong prompt</th>", 1),
    ("hệ thống đếm TIÊU CHÍ có mặt trong prompt của em",
     "hệ thống đếm TIÊU CHÍ có mặt trong prompt", 1),
    ("Thầy/cô sẽ nhận xét thêm về tính hợp lí của cách em diễn đạt.",
     "Giáo viên sẽ nhận xét thêm về tính hợp lí của cách diễn đạt.", 1),
],
"js/nhamay_text.js": [
    ('coSo = "câu trả lời lấy từ ngữ liệu của chính chủ đề em hỏi";',
     'coSo = "câu trả lời lấy từ ngữ liệu của chính chủ đề được hỏi";', 1),
    ('coSo = "máy không có dữ liệu về chủ đề em hỏi nên nó nói sang chuyện khác";',
     'coSo = "máy không có dữ liệu về chủ đề được hỏi nên nó nói sang chuyện khác";', 1),
],
"js/muc3.js": [
    ("Theo em, bốn con số mà máy đọc được ", "Theo dự đoán, bốn con số mà máy đọc được ", 1),
    ('+ "Theo em, độ chính xác của mô hình trên CHÍNH bộ dữ liệu nó vừa học là bao nhiêu?",',
     '+ "Theo dự đoán, độ chính xác của mô hình trên CHÍNH bộ dữ liệu nó vừa học là bao nhiêu?",', 1),
    ('+ "Theo em, độ chính xác trên ảnh BAN ĐÊM sẽ thành bao nhiêu?",',
     '+ "Theo dự đoán, độ chính xác trên ảnh BAN ĐÊM sẽ thành bao nhiêu?",', 1),
    ('+ "Nếu em hỏi một việc NGOÀI cả bốn chủ đề đó (ví dụ giá vàng hôm nay), "',
     '+ "Nếu hỏi một việc NGOÀI cả bốn chủ đề đó (ví dụ giá vàng hôm nay), "', 1),
    ('+ "theo em hệ sẽ làm gì?",', '+ "hệ sẽ làm gì?",', 1),
    ('cauHoi: "Hãy viết một prompt cho một việc em CHƯA TỪNG làm, rồi TỰ CHẤM xem prompt "',
     'cauHoi: "Hãy viết một prompt cho một việc CHƯA TỪNG làm, rồi TỰ CHẤM xem prompt "', 1),
    ('+ "của em có đủ các ý dưới đây không — trước khi bấm nút để hệ chấm.",',
     '+ "có đủ các ý dưới đây không, trước khi bấm nút để hệ chấm.",', 1),
    ('moTa: "nói rõ em muốn gì (mục tiêu của việc)"', 'moTa: "nói rõ việc cần làm (mục tiêu của việc)"', 1),
    ('moTa: "nói em sẽ kiểm lại kết quả thế nào"', 'moTa: "nói rõ cách kiểm lại kết quả"', 1),
    ('cauHoi: "Nghĩ về MỘT dự án AI mà nhóm em hoặc trường em đang làm (hoặc định làm). "',
     'cauHoi: "Nghĩ về MỘT dự án AI mà nhóm hoặc trường đang làm (hay đang dự định). "', 1),
    ('cauHoi: "Hãy viết MỘT nguyên tắc dùng AI của riêng em — và trong nguyên tắc đó phải "',
     'cauHoi: "Hãy viết MỘT nguyên tắc dùng AI của riêng mình, và trong nguyên tắc đó phải "', 1),
    ('+ "nói rõ: khi đầu ra của AI sai thì AI, em, hay thầy cô chịu trách nhiệm?",',
     '+ "nói rõ khi đầu ra của AI sai thì AI, người học hay giáo viên chịu trách nhiệm.",', 1),
],
"js/tinhhuong.js": [
    ('tinhHuong:"Nhóm em được giao làm một dự án sáng tạo — ứng dụng AI gợi ý ngành học '
     'cho học sinh lớp 12 dựa trên bài trắc nghiệm sở thích."',
     'tinhHuong:"Nhóm học sinh được giao làm một dự án sáng tạo, ứng dụng AI gợi ý ngành học '
     'cho học sinh lớp 12 dựa trên bài trắc nghiệm sở thích."', 1),
    ('tinhHuong:"Dự án của nhóm em dùng AI dự báo sâu bệnh',
     'tinhHuong:"Dự án của nhóm học sinh dùng AI dự báo sâu bệnh', 1),
],
"js/bt09.js": [
    ('" <b>Em tự cài một lỗi cho bạn bắt</b>"', '" <b>Tự cài một lỗi cho bạn cùng lớp bắt</b>"', 1),
    ('q.textContent = "Viết một câu trả lời của AI có cài ĐÚNG MỘT lỗi, rồi chọn loại lỗi em "',
     'q.textContent = "Viết một câu trả lời của AI có cài ĐÚNG MỘT lỗi, rồi chọn loại lỗi đã "', 1),
    ('+ "em đạt.";', '+ "bài đạt yêu cầu.";', 1),
    ('+ "câu em viết có lỗi hay không thì phải hiểu nội dung, mà máy không đọc hiểu thay em "',
     '+ "câu đã viết có lỗi hay không thì phải hiểu nội dung, mà máy không đọc hiểu thay người viết "', 1),
    ('+ "được. Hệ chỉ kiểm câu em viết có chứa những DẤU HIỆU của loại lỗi em khai hay không. "',
     '+ "được. Hệ chỉ kiểm câu đã viết có chứa những DẤU HIỆU của loại lỗi đã khai hay không. "', 1),
    ('labLoai.textContent = "1. Em định cài loại lỗi nào?";',
     'labLoai.textContent = "1. Chọn loại lỗi định cài";', 1),
    ('p2.innerHTML = "<b>Câu của em cần:</b> ";', 'p2.innerHTML = "<b>Câu viết ra cần có</b> ";', 1),
    ('labCau.textContent = "2. Câu trả lời của AI do em viết (cài đúng một lỗi)";',
     'labCau.textContent = "2. Câu trả lời của AI tự viết (cài đúng một lỗi)";', 1),
    ('labBan.textContent = "3. Em đưa câu này cho bạn nào bắt? (ghi mã hoặc tên bạn)";',
     'labBan.textContent = "3. Đưa câu này cho bạn nào bắt? (ghi mã hoặc tên bạn)";', 1),
    ('nutKiem.textContent = "Kiểm dấu hiệu trong câu của em";',
     'nutKiem.textContent = "Kiểm dấu hiệu trong câu đã viết";', 1),
    ('fb.textContent = "Em hãy chọn loại lỗi em định cài trước đã.";',
     'fb.textContent = "Cần chọn loại lỗi định cài trước.";', 1),
    ('fb.textContent = "Câu còn quá ngắn (dưới 20 kí tự). Hãy viết một câu trả lời AI đủ để bạn em đọc và bắt lỗi.";',
     'fb.textContent = "Câu còn quá ngắn (dưới 20 kí tự). Hãy viết một câu trả lời AI đủ để bạn cùng lớp đọc và bắt lỗi.";', 1),
    ('fb.textContent = "Em hãy ghi bạn sẽ đưa câu này cho ai bắt.";',
     'fb.textContent = "Cần ghi rõ sẽ đưa câu này cho ai bắt.";', 1),
    ('+ (kq.dat ? "Câu của em có dấu hiệu của loại lỗi đã khai."',
     '+ (kq.dat ? "Câu đã viết có dấu hiệu của loại lỗi đã khai."', 1),
    (': "Chưa thấy dấu hiệu của loại lỗi em khai.") + "</b>";',
     ': "Chưa thấy dấu hiệu của loại lỗi đã khai.") + "</b>";', 1),
    ('p2.textContent = "Loại em khai: " + tenLoai(chon)',
     'p2.textContent = "Loại đã khai: " + tenLoai(chon)', 1),
    ('p4.textContent = "Nhưng câu em có cả: " + kq.vuong.join(", ") + " — có nguồn kiểm "',
     'p4.textContent = "Nhưng câu viết ra có cả: " + kq.vuong.join(", ") + ", mà có nguồn kiểm "', 1),
    ('sw.textContent = "câu em viết còn có dấu hiệu của " + kq.loaiKhac.length + " loại lỗi "',
     'sw.textContent = "câu đã viết còn có dấu hiệu của " + kq.loaiKhac.length + " loại lỗi "', 1),
    ('+ "— cài nhiều lỗi thì bạn em không biết phải bắt lỗi nào.";',
     '"+ cài nhiều lỗi thì bạn đọc không biết phải bắt lỗi nào.";', 1),
    ('ok.textContent = "Không thấy dấu hiệu của các loại lỗi khác — câu em viết đang cài "',
     'ok.textContent = "Không thấy dấu hiệu của các loại lỗi khác, câu đã viết đang cài "', 1),
    ('+ "dung câu em viết, nên hệ không khẳng định được câu này có lỗi hay không. Bước cuối "',
     '+ "dung câu đã viết, nên hệ không khẳng định được câu này có lỗi hay không. Bước cuối "', 1),
    ('+ "vào nhật ký — chỉ loại lỗi và số dấu hiệu được ghi lại.";',
     '+ "vào nhật ký, chỉ loại lỗi và số dấu hiệu được ghi lại.";', 1),
    ('+ "vẫn là bạn " + (ban || "cùng lớp") + " đọc và bắt lỗi. Câu của em không được lưu "',
     '+ "vẫn là bạn " + (ban || "cùng lớp") + " đọc và bắt lỗi. Câu đã viết không được lưu "', 1),
],
"js/bt13.js": [
    ('inVao.placeholder = "Ví dụ: ảnh chụp bài giải viết tay của em...";',
     'inVao.placeholder = "Ví dụ: ảnh chụp bài giải viết tay...";', 1),
    ('fb.textContent = "Em hãy chọn một nhóm tính năng ở trên trước đã.";',
     'fb.textContent = "Cần chọn một nhóm tính năng ở trên trước.";', 1),
    ('fb.textContent = "Em hãy ghi cả ĐẦU VÀO và ĐẦU RA của hệ thống (mỗi ô ít nhất 3 kí tự).";',
     'fb.textContent = "Cần ghi cả ĐẦU VÀO và ĐẦU RA của hệ thống (mỗi ô ít nhất 3 kí tự).";', 1),
    ('p2.textContent = "Em chọn: " + tenNhom(chonNhom)',
     'p2.textContent = "Nhóm đã chọn: " + tenNhom(chonNhom)', 1),
    ('p7.textContent = "Cách chấm và giới hạn: hệ so nhóm em chọn với đáp án, và ĐẾM từ khoá "',
     'p7.textContent = "Cách chấm và giới hạn: hệ so nhóm đã chọn với đáp án, và ĐẾM từ khoá "', 1),
    ('+ "đã định nghĩa trước để biết em có nói tới đầu vào, đầu ra hay không. Hệ không "',
     '+ "đã định nghĩa trước để biết câu trả lời có nói tới đầu vào, đầu ra hay không. Hệ không "', 1),
    ('+ "đánh giá cách em diễn đạt. Thầy/cô sẽ nhận xét thêm.";',
     '+ "đánh giá cách diễn đạt. Giáo viên sẽ nhận xét thêm.";', 1),
    ('p8.textContent = "Lần kiểm tra này đã được ghi vào nhật ký. Em thử lại được để luyện tập.";',
     'p8.textContent = "Lần kiểm tra này đã được ghi vào nhật ký. Có thể thử lại để luyện tập.";', 1),
    ('" <b>Ứng dụng AI trong việc học của chính em</b>";',
     '" <b>Ứng dụng AI trong việc học của chính mình</b>";', 1),
    ('q.textContent = "Tìm một ứng dụng AI em ĐANG dùng trong việc học của chính mình "',
     'q.textContent = "Tìm một ứng dụng AI ĐANG dùng trong việc học của chính mình "', 1),
    ('+ "(không lấy ví dụ trong sách), xếp nó vào một nhóm tính năng, và giải thích vì sao em xếp như vậy.";',
     '+ "(không lấy ví dụ trong sách), xếp nó vào một nhóm tính năng, và giải thích vì sao xếp như vậy.";', 1),
    ('+ "Câu trả lời của em được ghi vào nhật ký để thầy/cô đọc và nhận xét.";',
     '+ "Câu trả lời được ghi vào nhật ký để giáo viên đọc và nhận xét.";', 1),
    ('labApp.textContent = "Tên ứng dụng AI em dùng (hoặc mô tả nó làm gì)";',
     'labApp.textContent = "Tên ứng dụng AI đang dùng (hoặc mô tả nó làm gì)";', 1),
    ('inApp.placeholder = "Ví dụ: công cụ dịch đoạn văn tiếng Anh em dùng khi làm bài đọc...";',
     'inApp.placeholder = "Ví dụ: công cụ dịch đoạn văn tiếng Anh dùng khi làm bài đọc...";', 1),
    ('labNhom3.textContent = "Em xếp nó vào nhóm tính năng nào?";',
     'labNhom3.textContent = "Xếp ứng dụng đó vào nhóm tính năng nào?";', 1),
    ('labVi.textContent = "Vì sao em xếp nó vào nhóm đó?";',
     'labVi.textContent = "Vì sao xếp nó vào nhóm đó?";', 1),
    ('inVi.placeholder = "Hệ thống nhận cái gì vào, và đưa ra cái gì? Vì sao đó là nhóm em chọn?";',
     'inVi.placeholder = "Hệ thống nhận cái gì vào, và đưa ra cái gì? Vì sao chọn nhóm đó?";', 1),
    ('gui.textContent = "Ghi lại câu trả lời của em";',
     'gui.textContent = "Ghi lại câu trả lời";', 1),
    ('fb3.textContent = "Em hãy ghi tên ứng dụng, chọn một nhóm, và giải thích ít nhất 10 kí tự.";',
     'fb3.textContent = "Cần ghi tên ứng dụng, chọn một nhóm, và giải thích ít nhất 10 kí tự.";', 1),
    ('fb3.textContent = "Đã ghi lại. Nhóm em chọn: " + tenNhom(chon3)',
     'fb3.textContent = "Đã ghi lại. Nhóm đã chọn: " + tenNhom(chon3)', 1),
    ('+ "Mỗi tình huống em làm ba việc: chọn đúng nhóm tính năng, nói rõ đầu vào, nói rõ đầu ra.";',
     '+ "Mỗi tình huống cần làm ba việc: chọn đúng nhóm tính năng, nói rõ đầu vào, nói rõ đầu ra.";', 1),
],
"js/nhamay_tram01.js": [
    ("giaiThich:\"Đúng. Ảnh với máy chỉ là các con số. Ở trạm này em thấy tận mắt bốn đặc trưng được trích từ mỗi ảnh",
     "giaiThich:\"Đúng. Ảnh với máy chỉ là các con số. Ở trạm này có thể thấy tận mắt bốn đặc trưng được trích từ mỗi ảnh", 1),
    ('<div class="nhan">nhãn em dán ĐÚNG</div>', '<div class="nhan">nhãn dán ĐÚNG</div>', 1),
    ('<div class="nhan">nhãn em dán SAI</div>', '<div class="nhan">nhãn dán SAI</div>', 1),
    ('<td>nhãn do em dán</td>', '<td>nhãn tự dán</td>', 1),
    ('? svgIco("check") + " Em dán nhãn đúng toàn bộ."', '? svgIco("check") + " Nhãn đã dán đúng toàn bộ."', 1),
    (': `${svgIco("x")} Em dán sai ${r.nhanSai} nhãn', ': `${svgIco("x")} Dán sai ${r.nhanSai} nhãn', 1),
    (': `Mô hình A học từ nhãn của em nên mất ${p(r.thietHai)} độ chính xác',
     ': `Mô hình A học từ nhãn tự dán nên mất ${p(r.thietHai)} độ chính xác', 1),
    ("học ĐÚNG những gì em dạy, kể cả khi em dạy sai.`}</p>",
     "học ĐÚNG những gì được dạy, kể cả khi dạy sai.`}</p>", 1),
    ("không được cập nhật. Em sẽ thấy tận mắt điều này ở Trạm 2 và Trạm 4 — đúng 100% ban ngày, 59% ban đêm.",
     "không được cập nhật. Điều này sẽ thấy tận mắt ở Trạm 2 và Trạm 4, đúng 100% ban ngày và 59% ban đêm.", 1),
],
"js/kichban.js": [
    ('sub:"Bây giờ đến lượt em kiểm tra.",', 'sub:"Bây giờ đến lượt người học kiểm tra.",', 1),
    ('el("div", "kb-ket-lon", "Đến lượt em kiểm tra")', 'el("div", "kb-ket-lon", "Đến lượt người học kiểm tra")', 1),
],
"js/lab3d.js": [
    ("<b>nội dung bài học không đổi</b>. Em hãy dùng",
     "<b>nội dung bài học không đổi</b>. Hãy dùng", 1),
],
"data/bai5_logic.js": [
    ("Em xem bảng của chính mình ở mục 3 trang này.",
     "Bảng của chính người học nằm ở mục 3 trang này.", 1),
],
"js/lab.js": [
    ("Sau khi phát hiện dữ liệu lệch, nhóm em cần đề xuất cách khắc phục.",
     "Sau khi phát hiện dữ liệu lệch, cần đề xuất cách khắc phục.", 1),
],
"data/kienthuc.js": [
    ("Khi em đăng nội dung lên mạng, em chịu trách nhiệm", "Khi đăng nội dung lên mạng, người đăng chịu trách nhiệm", 1),
    ("Dữ liệu em tạo ra khi học", "Dữ liệu tạo ra khi học", 1),
    ("Em chụp ảnh bài giải viết tay của mình, hệ đọc chữ trong ảnh rồi gán bài",
     "Chụp ảnh bài giải viết tay, hệ đọc chữ trong ảnh rồi gán bài", 1),
    ("ảnh mờ. Em cần biết ngưỡng này tồn tại trước khi tin kết quả.",
     "ảnh mờ. Ngưỡng sai này cần được biết trước khi tin kết quả.", 1),
    ("Hệ đọc bảng điểm giữa kì của em ở các môn", "Hệ đọc bảng điểm giữa kì ở các môn", 1),
    ("không có nghĩa là em chắc chắn sẽ sa sút — nó chỉ nói",
     "không có nghĩa chắc chắn sẽ sa sút, nó chỉ nói", 1),
    ("Em nhờ trợ lý AI soạn cho mình", "Nhờ trợ lý AI soạn", 1),
    ("và tài liệu em dán vào.", "và tài liệu được dán vào.", 1),
    ("không phải điểm của một em.", "không phải điểm của một học sinh.", 1),
    ("dữ liệu của lớp em có thể", "dữ liệu của lớp mình có thể", 1),
    ("Em dán một bài đọc tiếng Anh vào trợ lý AI", "Dán một bài đọc tiếng Anh vào trợ lý AI", 1),
    ("Văn bản tiếng Anh em dán vào", "Văn bản tiếng Anh được dán vào", 1),
    ("Với bài đọc quan trọng, em nên đối chiếu lại", "Với bài đọc quan trọng, cần đối chiếu lại", 1),
    ("Hệ nhận thời gian trống của em trong tuần", "Hệ nhận thời gian trống trong tuần", 1),
    ("không theo sức học của em. Em vẫn là người quyết định",
     "không theo sức học của từng người. Người học vẫn là người quyết định", 1),
    ("'đánh dấu chỗ nào em không chắc'", "'đánh dấu chỗ nào chưa chắc'", 1),
    ("Em muốn nhờ trợ lý AI giải thích khái niệm", "Cần nhờ trợ lý AI giải thích khái niệm", 1),
    ("bạn em", "bạn cùng lớp", 1),
    ("thiếu định dạng, em nhận về một bài dài không dùng được.",
     "thiếu định dạng, kết quả nhận về là một bài dài không dùng được.", 1),
    ("Lớp em có bảng điểm 40 bạn", "Lớp có bảng điểm 40 bạn", 1),
    ("Em muốn AI gợi ý bạn nào", "Cần AI gợi ý bạn nào", 1),
    ("cho một công cụ AI, em phải ẨN DANH trước", "cho một công cụ AI, phải ẨN DANH trước", 1),
    ("Em đọc được trên mạng câu này —", "Đọc được trên mạng câu này,", 1),
    ("Em muốn nhờ AI giúp kiểm tra thông tin này", "Cần nhờ AI kiểm tra thông tin này", 1),
    ("và cách em tự kiểm chứng", "và cách tự kiểm chứng", 1),
    ("và chỉ cho em cách tự tra cứu", "và chỉ cách tự tra cứu", 1),
],
}

# Vùng được MIỄN TRỪ: mảng tuKhoa / goiY trong js/muc3.js và mảng mau trong
# js/nhamay_text.js. Xem docstring đầu tệp — đổi chúng là phá máy chấm / phá bài học.
RE_MIEN_TRU = [
    re.compile(r'tuKhoa:\s*\[[^\]]*\]'),
    re.compile(r'goiY:\s*"[^"]*"'),
    re.compile(r'mau:\s*\[[^\]]*\]', re.S),
    # meta.js `buocPhaiCo` — dấu hiệu "xúi lộ dữ liệu cá nhân" trong LỜI THOẠI của hệ AI
    # ("tên em là", "địa chỉ nhà của em"…). Đây là mẫu câu nhận diện lỗi, không phải UI.
    re.compile(r'buocPhaiCo:\s*\[[^\]]*\]'),
]

# Dòng chỉ là COMMENT (block comment hoặc //) — không phải chữ người dùng đọc.
def la_comment(dong):
    t = dong.strip()
    return t.startswith("*") or t.startswith("/*") or t.startswith("//")

RE_EM_NGOI = re.compile(r"\bem\b|\bEm\b|của em|chính em|nhóm em")
# "Trẻ em" là DANH TỪ, không phải đại từ — lookbehind (?<!trẻ ) cũ lọt trường hợp
# "Trẻ em" viết hoa đầu chuỗi (đã đo: tinhhuong.js:54). Tự kiểm 4 ký tự trước match,
# không phân biệt hoa thường.
def la_danh_tu_tre_em(dong, pos):
    return dong[max(0, pos - 4):pos].lower() == "trẻ "


def vung_mien_tru(s):
    """Trả danh sách (start, end) của các vùng miễn trừ trong chuỗi s."""
    out = []
    for rx in RE_MIEN_TRU:
        for m in rx.finditer(s):
            out.append((m.start(), m.end()))
    return out


def trong_mien_tru(pos, vung):
    return any(a <= pos < b for a, b in vung)


def main():
    ghi = "--ghi" in sys.argv
    tong_doi = 0
    loi = []
    da_thay = {}   # f -> nội dung SAU thay thế. Quét sót PHẢI đọc từ đây, không đọc lại
                   # từ đĩa: ở chế độ chỉ-kiểm đĩa chưa đổi, quét đĩa sẽ báo sót oan đúng
                   # những chỗ BANG vừa thay (lỗi đã gặp: nhamay_tram01 5 chỗ, meta.js 4
                   # chỗ comment — tất cả đều âm giả).
    for f, caps in BANG.items():
        p = os.path.join(ROOT, f)
        s = io.open(p, encoding="utf-8").read()
        doi = 0
        for cu, moi, n in caps:
            k = s.count(cu)
            if k != n:
                loi.append(f"{f}: khớp {k}/{n} — {cu[:70]!r}")
            s = s.replace(cu, moi)
            doi += k
        tong_doi += doi
        da_thay[f] = s
        print(f"  [{f}] {doi} chỗ")
        if ghi:
            io.open(p, "w", encoding="utf-8").write(s)

    print("=" * 92)
    if loi:
        print(f"DỪNG — {len(loi)} chuỗi không khớp kỳ vọng, KHÔNG ghi gì:")
        for l in loi:
            print("  !", l)
        return 1
    print(f"LƯỢT ĐẾM: {tong_doi} chỗ thay (tất cả khớp kỳ vọng)")

    # QUÉT CÒN SÓT: "em" ngôi trong mã sống, loại comment và vùng miễn trừ.
    # Nguồn đọc: bản SAU thay thế (da_thay) với tệp trong BANG, đĩa với tệp ngoài.
    print("\n--- còn 'em' ngôi trong chữ người dùng đọc? ---")
    sot = 0
    for f in list(BANG) + ["js/pipeline3d.js", "js/scene3d.js", "js/engine.js",
                           "data/meta.js", "data/yccd.js"]:
        p = os.path.join(ROOT, f)
        if not os.path.isfile(p):
            continue
        s = da_thay.get(f) or io.open(p, encoding="utf-8").read()
        # KHỬ BLOCK COMMENT trước khi quét, thay bằng số dòng trống tương đương để số
        # dòng báo ra vẫn đúng (âm giả đã đo: muc3.js:129 nằm GIỮA block /* … */ nên
        # heuristic "dòng bắt đầu bằng *" không bắt được). Heuristic này có thể ăn một
        # chuỗi chứa "/*" — chấp nhận được vì cổng CHÍNH là đếm assert của BANG, quét
        # này chỉ là lưới vét.
        s = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), s, flags=re.S)
        vung = vung_mien_tru(s)
        lines = s.split("\n")
        offs = [0]
        for l in lines[:-1]:
            offs.append(offs[-1] + len(l) + 1)
        for i, dong in enumerate(lines):
            if la_comment(dong):
                continue
            # comment ĐUÔI dòng (code trước, // sau) — đã đo: app.js:355.
            duo = dong.find("//")
            for m in RE_EM_NGOI.finditer(dong):
                if trong_mien_tru(offs[i] + m.start(), vung):
                    continue
                if la_danh_tu_tre_em(dong, m.start()):
                    continue
                if duo >= 0 and m.start() > duo:
                    continue
                sot += 1
                print(f"  ! {f}:{i+1}| {dong.strip()[:150]}")
    print(f"  TỔNG còn sót: {sot}")

    if not ghi:
        print("\n(CHẾ ĐỘ CHỈ KIỂM — thêm --ghi để ghi.)")
        return 0 if not sot else 1
    if sot:
        print("\nDỪNG — còn chỗ sót, chưa ghi. Bổ sung bảng thay thế rồi chạy lại.")
        return 1
    print("\nĐÃ GHI")
    return 0


if __name__ == "__main__":
    sys.exit(main())
