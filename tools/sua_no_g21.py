#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Xử lý 3 khoản nợ G21 (G21b/c/d) đồng bộ trên data/bank_gen_g1_1.json
và data/cauhoi_moRong.js (cùng nội dung, hai định dạng — probe G21 chỉ đọc JS)."""
import json, re, io, sys

JSON_PATH = "data/bank_gen_g1_1.json"
JS_PATH = "data/cauhoi_moRong.js"

# ---------------- G21b: viết lại 14 lời giải không khoá vị trí ----------------
GIAITHICH_MOI = {
 "g1-01": "Lời khuyên kèm số liệu '73,6%' và '4,1/10 em' cùng tên một báo cáo nghe rất chuyên nghiệp nhưng không kiểm chứng được — con số 4,1/10 người cũng phi lý về mặt logic (không thể có 0,1 người trong cách đếm này kiểu 'cứ 10 em'). Dấu hiệu nhận biết: số quá lẻ, quá chính xác, gắn với 'báo cáo/nghiên cứu' mà không dẫn nguồn tra cứu được. Luôn hỏi: nguồn này tồn tại thật không, và ai đếm được con số lẻ kiểu đó?",
 "g1-02": "Lời khuyên viện một 'Công ước quốc tế về an toàn chatbot trường học' — không tồn tại công ước nào như vậy, và cũng không có quy định nào bắt chatbot học đường phải được 'ủy ban quốc tế' phê duyệt. Đây là lỗi kinh điển 'nguồn không tồn tại': AI bịa ra tên văn bản nghe rất trang trọng. Cách kiểm tra: tìm tên văn bản trên cổng thông tin chính thức (chinhphu.vn, moet.gov.vn) — không thấy là bịa.",
 "g1-03": "Lời khuyên 'học sinh miền Trung luôn giỏi tư duy thuật toán hơn hẳn học sinh miền Bắc' chứa định kiến vùng miền: khẳng định năng lực tư duy của một nhóm người theo nơi sinh sống là suy diễn không căn cứ — năng lực lập trình phụ thuộc vào rèn luyện, không vào xuất xứ. Dấu hiệu nhận biết: câu trả lời chia học sinh theo vùng/giới/ngoại hình rồi kết luận nhóm này 'luôn giỏi/kém' hơn nhóm kia là thiên kiến, và thêm lời khuyên 'bạn cứ yên tâm vì thuộc nhóm ưu thế' càng làm sai lệch thêm. Hai lời khuyên còn lại đúng: năng lực không phụ thuộc trường, và lời khuyên luyện tập là hợp lý.",
 "g1-04": "Lời hứa 'chắc chắn đỗ' sai vì suy luận 'số đông nói vậy thì đúng' — đây là lối tin theo đám đông (ad populum), chưa hề có bằng chứng cho trường hợp riêng của Bình; hơn nữa không ai, kể cả AI, bảo đảm được kết quả thi của một học sinh cụ thể. Dấu hiệu nhận biết: các từ 'chắc chắn', 'gần như 100%' đi kèm lý do 'nhiều người nói vậy' là tín hiệu suy luận vô căn cứ. Hai câu còn lại đúng về mặt nội dung.",
 "g1-05": "Cả ba câu đều đúng và là cách dùng AI chuẩn mực. Mô hình ngôn ngữ thực sự hay tự tin sai ở bài nhiều bước; tự giải lại giúp học sâu hơn và kiểm chứng được kết quả; và nguyên tắc dùng AI là luôn kiểm chứng thông tin, coi lời AI là tham khảo chứ không phải chân lý. Không có con số bịa, nguồn bịa, định kiến hay suy luận vô căn cứ nào ở đây.",
 "g1-06": "Mẹo 'gửi mật khẩu kèm tên đăng nhập cho mình lưu giúp' xúi gửi mật khẩu và tên đăng nhập cho một công cụ AI lưu lại — đó là lộ dữ liệu cá nhân nhạy cảm: mật khẩu không bao giờ nên chia sẻ với bất kì ai hay bất kì hệ thống nào ngoài nền tảng đăng nhập chính thức, và các hội thoại với AI có thể được lưu trữ, xem lại. Dấu hiệu nhận biết: mọi gợi ý 'gửi cho mình thông tin X' khi thông tin đó không cần thiết cho nhiệm vụ (đặc biệt là mật khẩu, CCCD, địa chỉ nhà) đều là tín hiệu đỏ. Hai câu còn lại là khuyến nghị an toàn chuẩn.",
 "g1-07": "Khẳng định nêu 'nghiên cứu' với số liệu cực kì chính xác (89,3%, giảm 23,7% sau 12 tuần) của một trung tâm không tồn tại — dù thông điệp 'tự viết tốt hơn' đúng, số liệu là bịa. Dấu hiệu: khi thấy phần trăm nhiều chữ số thập phân gắn với 'nghiên cứu/trung tâm' lạ, hãy hỏi: ai làm nghiên cứu? Xin được bản gốc ở đâu? Câu đúng cũng có thể chứa số liệu rởm, đừng để thông điệp hợp lý làm mình mất cảnh giác.",
 "g1-08": "Lời khuyên đọc 'Chương trình Kiến tạo số cho học đường' nêu một chương trình và tổ chức không tồn tại, kèm quy định lạ lùng 'tối đa 1 giờ trợ lý AI/ngày' — không có văn bản nào như vậy. Dấu hiệu nhận biết: khi AI nói 'theo chương trình X của tổ chức Y, quy định Z', hãy tách ba thành phần ra kiểm tra: tổ chức có thật không, chương trình có thật không, và quy định đó có thật không. Hai lời khuyên còn lại đúng và an toàn.",
 "g1-09": "Đề xuất gửi kèm ảnh chụp bảng xếp lớp xúi gửi họ tên và số điện thoại cá nhân của người khác cho một công cụ AI — đó là lộ dữ liệu cá nhân của tập thể, vi phạm sự riêng tư của cả lớp và không cần thiết cho yêu cầu đổi lịch. Dấu hiệu nhận biết: mỗi khi gợi ý yêu cầu gửi thông tin cá nhân (của mình hay người khác) nhiều hơn mức cần cho mục đích, hãy dừng lại và hỏi 'cái này có thật sự cần không?'. Hai câu còn lại là thực hành riêng tư an toàn.",
 "g1-10": "Cả ba câu đều đúng. Phân biệt ở trên đúng bản chất dữ liệu có cấu trúc và hệ thống học từ dữ liệu; phần mô tả cách hoạt động cho thấy mô hình thống kê tìm quy luật trong dữ liệu huấn luyện và có thể sai ở tình huống chưa từng thấy; và nhận xét cuối nêu đúng mối quan hệ giữa chất lượng dữ liệu và chất lượng đầu ra của AI ('rác vào, rác ra'). Không có số liệu bịa, nguồn không tồn tại, định kiến hay suy luận vô căn cứ.",
 "g1-11": "Lời khuyên 'nên chọn các lĩnh vực xã hội cho chắc' chia nhóm theo giới và ngầm kết luận 'con gái thua kém con trai về ý tưởng kỹ thuật' — định kiến giới rõ ràng, không có căn cứ; năng lực sáng tạo không phụ thuộc giới tính. Dấu hiệu nhận biết: mọi khẳng định dạng 'nhóm X thường kém/giỏi hơn nhóm Y' về năng lực cần bằng chứng chất lượng cao, và với giới tính thì sự đa dạng cá nhân luôn lớn hơn bất kì 'trung bình nhóm' nào. Hai câu còn lại đúng: không cần chuyên Tin vẫn tham gia được, và chia vai trong nhóm là chiến lược hợp lý.",
 "g1-12": "Kết luận vội 'chắc chắn là do ứng dụng' sai vì lẫn tương quan với nhân quả: hai việc đi cùng nhau (dùng ứng dụng tăng và điểm tăng) chưa chứng minh việc này gây ra việc kia — có thể còn yếu tố chung nào đó khiến cả hai cùng tăng, ví dụ lớp chăm chỉ hơn. Dấu hiệu nhận biết: các cụm 'cùng lúc', 'sau đó' được dùng làm bằng chứng nhân quả là tín hiệu suy luận vội; cần so sánh có kiểm soát. Hai câu còn lại đúng về phương pháp.",
 "g1-13": "Cả ba câu đều đúng: chatbot hỏi đáp tài liệu học theo chính kho dữ liệu được cung cấp; việc kết nối nguồn ngoài cần được thiết kế ưu tiên nguồn chính thức; và nguyên tắc 'rác vào, rác ra' — chất lượng dữ liệu quyết định chất lượng đầu ra. Không có số liệu bịa, nguồn không tồn tại, định kiến, suy luận sai hay gợi ý lộ dữ liệu cá nhân nào.",
 "g1-14": "Cả ba câu đều đúng: việc chấm văn cần ngữ cảnh mà AI không có; AI phù hợp với hỗ trợ kĩ thuật, còn nhận xét giáo dục — động viên, định hướng — cần con người; và AI thiếu hiểu biết cá nhân hóa về từng học sinh. Không có lỗi về số liệu, nguồn, định kiến hay suy luận — đây là câu trả lời đúng tiêu chuẩn.",
}

# ---------------- G21d: rút ngắn 3 claim lỗi đang là dài nhất ----------------
CLAIM_RUT_NGON = {
 "g1-04": ("Mình dám khẳng định là 'chắc chắn đỗ', vì hàng nghìn học sinh trên mạng đều kể rằng cứ kiên trì học theo lời AI thì đều đỗ — số đông cùng nói vậy thì gần như chắc chắn đúng.",
           "Mình dám khẳng định 'chắc chắn đỗ': hàng nghìn học sinh trên mạng kể rằng học theo lời AI là đều đỗ — số đông nói vậy thì chắc chắn đúng."),
 "g1-07": ("Nghiên cứu của Trung tâm Đánh giá Năng lực Học tập công bố năm 2025 cho thấy 89,3% học sinh để AI viết hộ mở bài đều bị cuốn hút theo cách diễn đạt của AI, trí nhớ chủ động của học sinh được ghi nhận giảm trung bình 23,7% sau 12 tuần.",
           "Nghiên cứu của 'Trung tâm Đánh giá Năng lực Học tập' năm 2025 cho thấy 89,3% học sinh để AI viết hộ mở bài bị giảm trí nhớ chủ động trung bình 23,7% sau 12 tuần."),
 "g1-08": ("Ngoài ra em nên đọc 'Chương trình Kiến tạo số cho học đường' của Liên minh Giáo dục số Việt Nam — chương trình này quy định mỗi học sinh THPT được dùng tối đa 1 giờ trợ lý AI mỗi ngày.",
           "Em nên đọc 'Chương trình Kiến tạo số cho học đường' của Liên minh Giáo dục số Việt Nam — quy định học sinh THPT dùng tối đa 1 giờ trợ lý AI mỗi ngày."),
}

# ---------------- G21c: 6 câu ĐÚNG mới, có số liệu thật kiểm chứng được ----------------
CAU_DUNG_MOI = [
 {"id":"g1-15","mach":"A","unesco":"A1","loai":"dung","loaiLoi":None,"claimLoi":-1,
  "boiCanh":"Nam hỏi AI về mức độ phổ biến của ChatGPT để làm bài thu hoạch chủ đề AI.",
  "claims":[
   "ChatGPT ra mắt ngày 30/11/2022 và được ước tính đạt khoảng 100 triệu người dùng chỉ sau 2 tháng — một trong những ứng dụng phổ biến nhanh nhất lịch sử, nhưng phổ biến nhanh không tự động nghĩa là câu trả lời luôn chính xác.",
   "Trước khi trích số liệu người dùng hay bất kì con số nào do AI nêu vào bài, em nên kiểm chứng lại với nguồn báo chí hoặc báo cáo gốc có dẫn rõ.",
   "AI không tự tra cứu internet trừ khi được thiết kế riêng, nên kiến thức của nó có thể dừng ở thời điểm cắt dữ liệu huấn luyện."],
  "giaiThich":"Cả ba câu đều đúng và đều dùng con số thật, kiểm chứng được: ngày ra mắt 30/11/2022 và mốc 100 triệu người dùng sau khoảng 2 tháng được nhiều hãng thông tấn lớn dẫn lại. Điểm sư phạm: số liệu thật vẫn cần dẫn nguồn, và 'nhiều người dùng' không chứng minh 'đúng' — hai điều học sinh dễ lẫn. Không có số liệu bịa, nguồn không tồn tại, định kiến hay suy luận vô căn cứ."},
 {"id":"g1-16","mach":"B","unesco":"B1","loai":"dung","loaiLoi":None,"claimLoi":-1,
  "boiCanh":"Chi hỏi AI giúp sắp lịch ôn tập và được gợi ý phương pháp Pomodoro.",
  "claims":[
   "Kĩ thuật Pomodoro chia việc học thành các phiên 25 phút tập trung, nghỉ khoảng 5 phút giữa các phiên, và nghỉ dài hơn sau khoảng 4 phiên — có thể dùng để sắp giờ luyện tập với trợ lý AI.",
   "Học với AI hiệu quả hơn khi em đặt từng câu hỏi nhỏ cho mỗi phiên thay vì nhồi nhiều chủ đề cùng lúc, vì não cần thời gian củng cố.",
   "Nếu cảm thấy mệt hoặc mất tập trung, nghỉ ngơi đúng lúc là cách học khoa học, không phải là lười."],
  "giaiThich":"Cả ba câu đều đúng. Thông số 25 phút tập trung và 5 phút nghỉ là quy ước gốc của kĩ thuật Pomodoro — một quy ước phương pháp công khai, khác với số liệu thống kê cần truy nguồn; chia nhỏ câu hỏi giúp củng cố kiến thức tốt hơn học dồn; và nghỉ ngơi đúng lúc là nguyên tắc học khoa học. Không có lỗi về số liệu bịa, nguồn, định kiến hay suy luận."},
 {"id":"g1-17","mach":"C","unesco":"C1","loai":"dung","loaiLoi":None,"claimLoi":-1,
  "boiCanh":"Thư hỏi AI về kĩ thuật bảo vệ mắt khi học online nhiều giờ.",
  "claims":[
   "Quy tắc 20-20-20 khuyên cứ sau mỗi 20 phút nhìn màn hình thì nhìn một vật cách xa khoảng 6 mét (20 feet) trong 20 giây để giảm mỏi mắt — hữu ích khi học với AI nhiều giờ.",
   "Học online ở nơi đủ sáng và giữ mắt cách màn hình khoảng 50–70 cm cũng giúp giảm mỏi mắt.",
   "Nếu mắt khô hoặc mờ sau khi học, em nên nghỉ hoàn toàn và nói với phụ huynh hoặc thầy cô thay vì tự ý nhỏ thuốc."],
  "giaiThich":"Cả ba câu đều đúng và là khuyến cáo sức khỏe mắt phổ biến: quy tắc 20-20-20, khoảng cách mắt với màn hình hợp lí, và nguyên tắc không tự ý dùng thuốc khi mắt bất thường. Số trong câu này là quy tắc ứng xử dễ nhớ, không phải con số thống kê cần truy nguồn — phân biệt được hai loại số này là một phần của kĩ năng đọc số liệu. Không có lỗi về số liệu bịa, nguồn, định kiến hay suy luận."},
 {"id":"g1-18","mach":"D","unesco":"D2","loai":"dung","loaiLoi":None,"claimLoi":-1,
  "boiCanh":"Hạo hỏi AI về pháp luật bảo vệ dữ liệu cá nhân ở Việt Nam khi làm bài về quyền riêng tư.",
  "claims":[
   "Ở Việt Nam, Luật An ninh mạng có hiệu lực từ ngày 01/01/2019, và Nghị định 13/2023/NĐ-CP quy định chi tiết về bảo vệ dữ liệu cá nhân — hai văn bản này tra được trên cổng thông tin của Chính phủ.",
   "Nghị định 13/2023/NĐ-CP có hiệu lực từ 01/7/2023, hiểu thông tin cá nhân là thông tin gắn với một người cụ thể, và việc xử lí dữ liệu phải có sự đồng ý của chủ dữ liệu.",
   "Khi dùng AI, em vẫn có trách nhiệm không nhập thông tin cá nhân của mình hay người khác nhiều hơn mức nhiệm vụ cần."],
  "giaiThich":"Cả ba câu đều đúng và trỏ tới văn bản thật, tra cứu được: Luật An ninh mạng (có hiệu lực 01/01/2019) và Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân. Khác với các câu dùng nguồn bịa, nguồn ở đây có số hiệu đầy đủ và nằm trên cổng công báo — cách kiểm tra là gõ số hiệu văn bản vào cổng thông tin chính phủ. Không có định kiến hay suy luận vô căn cứ."},
 {"id":"g1-19","mach":"A","unesco":"A2","loai":"dung","loaiLoi":None,"claimLoi":-1,
  "boiCanh":"Vy hỏi AI có nên tin con số về tỉ lệ học sinh dùng AI mà bạn đọc trên mạng.",
  "claims":[
   "Một con số như '85% học sinh dùng AI' chỉ có nghĩa khi biết nguồn, năm công bố và cách đặt câu hỏi của khảo sát — khi trích lại, em phải ghi rõ cả ba.",
   "Hai khảo sát khác nhau có thể cho hai kết quả khác biệt lớn mà vẫn đều trung thực, vì mẫu và cách hỏi khác nhau.",
   "Thay vì nhớ một con số duy nhất, quan trọng hơn là hiểu phép đo đó nói lên điều gì và giới hạn của nó ở đâu."],
  "giaiThich":"Cả ba câu đều đúng và dạy thái độ đúng với số liệu: con số khảo sát phụ thuộc thời điểm, mẫu và cách hỏi; hai khảo sát trung thực vẫn có thể khác nhau; và hiểu giới hạn phép đo quan trọng hơn ghi nhớ con số. Đây là kĩ năng đọc số liệu đúng, đi ngược lại lỗi 'số liệu bịa': không phải thấy số là nghi, mà là thấy số phải hỏi nguồn, năm và cách đo."},
 {"id":"g1-20","mach":"B","unesco":"B2","loai":"dung","loaiLoi":None,"claimLoi":-1,
  "boiCanh":"Quy cho rằng AI giỏi Toán thì chắc giỏi mọi môn và hỏi AI để kiểm chứng.",
  "claims":[
   "Tháng 3/2023, GPT-4 được công bố đạt mức trong top 10% thí sinh ở kì thi Luật của bang California (Mỹ), trong khi các mô hình trước đó đạt dưới trung bình — nhưng chính nhà phát triển cũng ghi rõ hạn chế của nó ở nhiều lĩnh vực khác.",
   "Mỗi mô hình được huấn luyện trên dữ liệu khác nhau nên mạnh yếu khác nhau, và bảng so sánh năng lực phải đọc kèm kì thi và điều kiện cụ thể.",
   "Kết quả thi của AI là bằng chứng về dữ liệu huấn luyện, không phải bằng chứng về sự hiểu biết như con người."],
  "giaiThich":"Cả ba câu đều đúng: kết quả GPT-4 ở kì thi Luật bang California công bố tháng 3/2023 là dữ liệu công khai từ nhà phát triển, kèm chính lời khai về hạn chế; mỗi mô hình mạnh yếu khác nhau tùy dữ liệu huấn luyện; và điểm thi không đồng nghĩa hiểu biết như con người. Suy luận 'giỏi cái này thì giỏi mọi cái' là khái quát hóa vội — câu trả lời này đi ngược lại suy luận vô căn cứ."},
]

LOCK = re.compile(r"[Cc]â[u y]\s*(?:thứ\s*)?\d")

def xu_ly(data, la_json_gen):
    da_sua_gt, da_sua_claim = [], []
    for it in data:
        i = it["id"]
        if i in GIAITHICH_MOI:
            assert LOCK.search(it["giaiThich"]), f"{i}: lời giải gốc không khớp mẫu khoá vị trí"
            it["giaiThich"] = GIAITHICH_MOI[i]
            assert not LOCK.search(it["giaiThich"]), f"{i}: lời giải mới vẫn khoá vị trí"
            da_sua_gt.append(i)
        if i in CLAIM_RUT_NGON:
            cu, moi = CLAIM_RUT_NGON[i]
            idx = it["claims"].index(cu)
            it["claims"][idx] = moi
            da_sua_claim.append(i)
    return da_sua_gt, da_sua_claim

# ---- JSON ----
with io.open(JSON_PATH, encoding="utf-8") as f:
    j = json.load(f)
gt, cl = xu_ly(j["good"], True)
assert gt == sorted(GIAITHICH_MOI) and cl == sorted(CLAIM_RUT_NGON)
j["generated"] = len(j["good"]) + len(CAU_DUNG_MOI)
j["good"].extend(CAU_DUNG_MOI)
with io.open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(j, f, ensure_ascii=False, indent=1)
    f.write("\n")

# ---- JS (cùng dữ liệu, định dạng +1 dấu cách) ----
with io.open(JS_PATH, encoding="utf-8") as f:
    s = f.read()
m = re.search(r"window\.MX_BANK_MORE = (\[.*\]);\s*$", s, re.S)
body = m.group(1)
data = json.loads(body)
gt2, cl2 = xu_ly(data, False)
assert gt2 == gt and cl2 == cl
data.extend(CAU_DUNG_MOI)
new_body = json.dumps(data, ensure_ascii=False, indent=1)
new_body = "\n".join((" " + ln if ln else ln) for ln in new_body.split("\n"))
s = s[:m.start(1)] + new_body + s[m.end(1):]

# cập nhật chú thích phân bố đầu tệp
s = s.replace('{"tong": 56, "loai": {"co_loi": 39, "dung": 17}',
              '{"tong": 62, "loai": {"co_loi": 39, "dung": 23}')
s = s.replace('"mach": {"C": 15, "D": 11, "B": 16, "A": 14}',
              '"mach": {"C": 16, "D": 12, "B": 18, "A": 16}')
with io.open(JS_PATH, "w", encoding="utf-8") as f:
    f.write(s)

# ---------------- tự kiểm ----------------
assert not LOCK.search(s), "JS vẫn còn lời giải khoá vị trí"
assert "tong\": 62" in s and "dung\": 23" in s
print(f"đã viết lại {len(gt)} lời giải (G21b): {','.join(gt)}")
print(f"đã rút ngắn {len(cl)} claim lỗi (G21d): {','.join(cl)}")
for i, (cu, moi) in CLAIM_RUT_NGON.items():
    print(f"  {i}: {len(cu)} -> {len(moi)} kí tự ({100*len(moi)//len(cu)}%)")
print(f"đã thêm {len(CAU_DUNG_MOI)} câu đúng có số liệu (G21c): " +
      ",".join(x["id"] for x in CAU_DUNG_MOI))
for x in CAU_DUNG_MOI:
    assert re.search(r"[0-9]", " ".join(x["claims"])), x["id"] + " thiếu chữ số"
    assert not LOCK.search(x["giaiThich"]), x["id"] + " lời giải mới khoá vị trí"
    assert x["loai"] == "dung" and x["claimLoi"] == -1
print("tự kiểm: OK")
