/* SOI AI — ngân hàng câu hỏi MỞ RỘNG (sinh bằng LLM pipeline + QC schema tự động,
 * 4 batch × 2 model; ĐÃ soát mẫu; chờ tác giả duyệt nhãn 100% trước khi dạy thật — xem proposal §2.7#3).
 * QC: schema 12 luật + quét số hiệu văn bản thật (cấm trùng văn bản có thật làm nguồn bịa).
 * Phân bố: {"tong": 56, "loai": {"co_loi": 39, "dung": 17}, "loaiLoi": {"so_lieu_bia": 8, "nguon_khong_ton_tai": 8, "thien_kien": 8, "suy_luan_sai": 8, "lo_du_lieu_ca_nhan": 7}, "mach": {"C": 15, "D": 11, "B": 16, "A": 14}} */
window.MX_BANK_MORE = [
 {
  "id": "g1-01",
  "mach": "C",
  "unesco": "C2",
  "loai": "co_loi",
  "loaiLoi": "so_lieu_bia",
  "claimLoi": 2,
  "boiCanh": "Lan chuẩn bị thuyết trình về AI cho tiết sinh hoạt lớp chủ đề công nghệ.",
  "claims": [
   "Trí tuệ nhân tạo là một lĩnh vực của khoa học máy tính, mục tiêu là tạo ra máy móc có thể thực hiện những việc mà ta thường nghĩ chỉ con người làm được, chẳng hạn như nhận diện khuôn mặt hay dịch ngôn ngữ.",
   "Máy học là một nhánh của AI: thay vì lập trình từng bước cụ thể, máy học cách làm việc đó bằng cách tìm quy luật từ rất nhiều dữ liệu mẫu — ví dụ hàng nghìn ảnh mèo để học cách nhận mèo.",
   "Theo Báo cáo Chỉ số Số hóa Học đường 2025 do Viện Nghiên cứu Giáo dục Số công bố, 73,6% học sinh THPT Việt Nam đã từng nhờ AI làm bài tập, và cứ 10 em thì có 4,1 em dùng AI mỗi ngày."
  ],
  "giaiThich": "Câu 3 đưa số liệu '73,6%' và '4,1/10 em' kèm tên báo cáo nghe rất chuyên nghiệp nhưng không kiểm chứng được — con số 4,1/10 người cũng phi lý về mặt logic (không thể có 0,1 người trong cách đếm này kiểu 'cứ 10 em'). Dấu hiệu nhận biết: số quá lẻ, quá chính xác, gắn với 'báo cáo/nghiên cứu' mà không dẫn nguồn tra cứu được. Luôn hỏi: nguồn này tồn tại thật không, và ai đếm đếm được con số lẻ kiểu đó?"
 },
 {
  "id": "g1-02",
  "mach": "D",
  "unesco": "D1",
  "loai": "co_loi",
  "loaiLoi": "nguon_khong_ton_tai",
  "claimLoi": 1,
  "boiCanh": "Minh nghiên cứu cách tạo chatbot hỏi đáp cho CLB Tin học của trường.",
  "claims": [
   "Để một chatbot trả lời được câu hỏi về tài liệu của trường, nhóm mình có thể dùng phương pháp RAG — cho AI truy xuất đoạn văn liên quan từ kho tài liệu rồi mới trả lời, thay vì bắt AI 'nhớ thuộc' mọi thứ.",
   "Theo 'Công ước quốc tế về an toàn chatbot trường học' mà Việt Nam tham gia năm 2023, mọi chatbot học đường phải được một ủy ban quốc tế phê duyệt trước khi cho học sinh sử dụng.",
   "Nên lưu ý các câu trả lời có trích dẫn nguồn: nhóm mình kiểm tra lại nguồn đó có tồn tại không, vì đôi khi AI tạo ra trích dẫn nghe rất 'thật' nhưng không có thật."
  ],
  "giaiThich": "Câu 2 viện một 'Công ước quốc tế về an toàn chatbot trường học' — không tồn tại công ước nào như vậy, và cũng không có quy định nào bắt chatbot học đường phải được 'ủy ban quốc tế' phê duyệt. Đây là lỗi kinh điển 'nguồn không tồn tại': AI bịa ra tên văn bản nghe rất trang trọng. Cách kiểm tra: tìm tên văn bản trên cổng thông tin chính thức (chinhphu.vn, moet.gov.vn) — không thấy là bịa."
 },
 {
  "id": "g1-03",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "thien_kien",
  "claimLoi": 2,
  "boiCanh": "Hải ở Thanh Hóa muốn biết mình có nên theo nhóm lập trình của trường không dù trường không có đội mạnh về Tin học.",
  "claims": [
   "Chắc chắn được nhé! Năng lực lập trình của bạn không phụ thuộc vào trường bạn học — nhiều bạn ở trường nhỏ tự học online và đạt giải, nên điều quan trọng là phương pháp và sự kiên trì.",
   "Khi đã vào nhóm, hãy tận dụng các nền tảng học lập trình miễn phí và bạn bè đồng đội để tiến bộ đều đặn; điều quan trọng nhất là kiên trì luyện đề và đặt câu hỏi khi chưa hiểu.",
   "Nói thêm cho bạn yên tâm: học sinh miền Trung luôn giỏi tư duy thuật toán hơn hẳn học sinh miền Bắc, nên bạn sinh ra ở Thanh Hóa thì việc học lập trình sẽ dễ hơn so với các bạn khác."
  ],
  "giaiThich": "Câu 3 chứa định kiến vùng miền: khẳng định năng lực tư duy của một nhóm người theo nơi sinh sống là suy diễn không căn cứ — năng lực lập trình phụ thuộc vào rèn luyện, không vào xuất xứ. Dấu hiệu nhận biết: câu trả lời chia học sinh theo vùng/giới/ngoại hình rồi kết luận nhóm này 'luôn giỏi/kém' hơn nhóm kia là thiên kiến, và thêm lời khuyên 'bạn cứ yên tâm vì thuộc nhóm ưu thế' càng làm sai lệch thêm. Hai câu còn lại đúng: năng lực không phụ thuộc trường, và lời khuyên luyện tập là hợp lý."
 },
 {
  "id": "g1-04",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "suy_luan_sai",
  "claimLoi": 1,
  "boiCanh": "Bình hỏi trợ lý AI rằng học theo kế hoạch ôn vừa lập thì có đỗ kỳ thi vào lớp 10 không, và nhận được lời động viên rất tự tin.",
  "claims": [
   "Kế hoạch của bạn khá hợp lí: ôn đều các môn, chừa thời gian nghỉ — học như vậy cơ hội của bạn tốt lên rõ rệt, dù không kế hoạch nào đảm bảo kết quả tuyệt đối.",
   "Mình dám khẳng định là 'chắc chắn đỗ', vì hàng nghìn học sinh trên mạng đều kể rằng cứ kiên trì học theo lời AI thì đều đỗ — số đông cùng nói vậy thì gần như chắc chắn đúng.",
   "Để tự tin hơn, bạn nên làm vài đề thử theo đúng thời gian thi thật — kết quả đề thử sẽ cho bạn bức tranh thực tế hơn nhiều so với lời hứa của bất kì ai."
  ],
  "giaiThich": "Câu 2 sai vì suy luận 'số đông nói vậy thì đúng' — đây là lối tin theo đám đông (ad populum), chưa hề có bằng chứng cho trường hợp riêng của Bình; hơn nữa không ai, kể cả AI, bảo đảm được kết quả thi của một học sinh cụ thể. Dấu hiệu nhận biết: các từ 'chắc chắn', 'gần như 100%' đi kèm lý do 'nhiều người nói vậy' là tín hiệu suy luận vô căn cứ. Câu 1 và 3 đúng về mặt nội dung."
 },
 {
  "id": "g1-05",
  "mach": "A",
  "unesco": "A1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Yến hỏi AI xem có nên tin hoàn toàn vào đáp án Toán của nó không.",
  "claims": [
   "Mình trả lời khá nhanh và đúng phần lớn bài tập phổ thông, nhưng vẫn sai kiểu 'chắc như đinh đóng cột' ở những bài cần nhiều bước suy luận hoặc có điều kiện đặc biệt.",
   "Tốt nhất là dùng mình để gợi ý hướng giải rồi tự giải lại — như vậy bạn vừa kiểm chứng được, vừa nhớ lâu hơn là chỉ chép đáp án.",
   "Nói chung, những gì mình nói nên được xem là thông tin tham khảo cần kiểm chứng, chứ không phải chân lý."
  ],
  "giaiThich": "Cả ba câu đều đúng và là cách dùng AI chuẩn mực. Câu 1 đúng vì mô hình ngôn ngữ thực sự hay tự tin sai ở bài nhiều bước; câu 2 đúng vì tự giải lại giúp học sâu hơn và kiểm chứng được kết quả; câu 3 đúng vì nguyên tắc dùng AI là luôn kiểm chứng thông tin. Không có con số bịa, nguồn bịa, định kiến hay suy luận vô căn cứ nào ở đây."
 },
 {
  "id": "g1-06",
  "mach": "C",
  "unesco": "C1",
  "loai": "co_loi",
  "loaiLoi": "lo_du_lieu_ca_nhan",
  "claimLoi": 2,
  "boiCanh": "Trang muốn biết cách chọn mật khẩu an toàn cho tài khoản học tập.",
  "claims": [
   "Mật khẩu mạnh nên dài tối thiểu 12 kí tự, trộn chữ hoa, chữ thường, số và kí tự đặc biệt, và không chứa ngày sinh hay tên của bạn.",
   "Quan trọng nhất: đừng tái sử dụng một mật khẩu cho nhiều tài khoản — nếu một tài khoản bị lộ, các tài khoản còn lại cũng bị kéo theo. Bảo vệ tốt hơn cả là bật xác thực hai lớp.",
   "Mẹo thực dụng nè: nếu sợ quên, em cứ gửi mật khẩu kèm tên đăng nhập cho mình lưu giúp, lần sau cần chỉ việc hỏi lại — tiện hơn nhiều so với ghi ra giấy."
  ],
  "giaiThich": "Câu 3 xúi gửi mật khẩu và tên đăng nhập cho một công cụ AI lưu lại — đó là lộ dữ liệu cá nhân nhạy cảm: mật khẩu không bao giờ nên chia sẻ với bất kì ai hay bất kì hệ thống nào ngoài nền tảng đăng nhập chính thức, và các hội thoại với AI có thể được lưu trữ, xem lại. Dấu hiệu nhận biết: mọi gợi ý 'gửi cho mình thông tin X' khi thông tin đó không cần thiết cho nhiệm vụ (đặc biệt là mật khẩu, CCCD, địa chỉ nhà) đều là tín hiệu đỏ. Hai câu còn lại là khuyến nghị an toàn chuẩn."
 },
 {
  "id": "g1-07",
  "mach": "A",
  "unesco": "A2",
  "loai": "co_loi",
  "loaiLoi": "so_lieu_bia",
  "claimLoi": 0,
  "boiCanh": "Hùng hỏi chatbot vì sao mình nên tự viết đoạn văn mở bài thay vì để AI viết hộ.",
  "claims": [
   "Nghiên cứu của Trung tâm Đánh giá Năng lực Học tập công bố năm 2025 cho thấy 89,3% học sinh để AI viết hộ mở bài đều bị cuốn hút theo cách diễn đạt của AI, trí nhớ chủ động của học sinh được ghi nhận giảm trung bình 23,7% sau 12 tuần.",
   "Khi bạn tự viết, não phải chủ động truy xuất từ vựng và ý tưởng — chính quá trình 'vắt óc' đó giúp bạn tiến bộ, còn đọc bài AI viết hộ chỉ cho bạn kết quả cuối cùng.",
   "Nếu cần hỗ trợ, bạn có thể nhờ AI góp ý cho đoạn văn mình đã viết — cách này giữ vai trò chủ động cho bạn và vẫn có được sự trợ giúp."
  ],
  "giaiThich": "Câu 1 nêu nghiên cứu với số liệu cực kì chính xác (89,3%, giảm 23,7% sau 12 tuần) của một trung tâm không tồn tại — dù thông điệp 'tự viết tốt hơn' đúng, số liệu là bịa. Dấu hiệu: khi thấy phần trăm nhiều chữ số thập phân gắn với 'nghiên cứu/trung tâm' lạ, hãy hỏi: ai làm nghiên cứu? Xin được bản gốc ở đâu? Câu đúng cũng có thể chứa số liệu rởm, đừng để thông điệp hợp lý làm mình mất cảnh giác."
 },
 {
  "id": "g1-08",
  "mach": "A",
  "unesco": "A2",
  "loai": "co_loi",
  "loaiLoi": "nguon_khong_ton_tai",
  "claimLoi": 2,
  "boiCanh": "Nga hỏi chatbot về chủ trương dùng AI trong học tập ở trường phổ thông Việt Nam.",
  "claims": [
   "Nhiều trường ở Việt Nam đang thí điểm cho học sinh dùng AI hỗ trợ học tập như tra cứu, luyện đọc hiểu, và các thầy cô có hướng dẫn cụ thể cách dùng sao cho hiệu quả.",
   "Nói chung, quy định thường hướng tới AI hỗ trợ người học chứ không làm thay người học, nên em nên coi AI như công cụ gợi ý và người cuối cùng chịu trách nhiệm vẫn là em.",
   "Ngoài ra em nên đọc 'Chương trình Kiến tạo số cho học đường' của Liên minh Giáo dục số Việt Nam — chương trình này quy định mỗi học sinh THPT được dùng tối đa 1 giờ trợ lý AI mỗi ngày."
  ],
  "giaiThich": "Câu 3 nêu một chương trình và tổ chức không tồn tại, kèm quy định lạ lùng 'tối đa 1 giờ trợ lý AI/ngày' — không có văn bản nào như vậy. Dấu hiệu nhận biết: khi AI nói 'theo chương trình X của tổ chức Y, quy định Z', hãy tách ba thành phần ra kiểm tra: tổ chức có thật không, chương trình có thật không, và quy định đó có thật không. Hai câu đầu đúng và an toàn."
 },
 {
  "id": "g1-09",
  "mach": "B",
  "unesco": "B1",
  "loai": "co_loi",
  "loaiLoi": "lo_du_lieu_ca_nhan",
  "claimLoi": 0,
  "boiCanh": "Phương nhờ AI gợi ý trao đổi với trợ lý ảo của trường về đổi lịch trực lớp.",
  "claims": [
   "Mình đề xuất: gửi kèm ảnh chụp bảng xếp lớp có đủ họ tên và số điện thoại của mọi thành viên để AI quản lý lịch trực hiểu rõ hoàn cảnh lớp và hỗ trợ chính xác hơn.",
   "Ngoài ra, em có thể nêu rõ yêu cầu đổi ca và lý do cá nhân ngắn gọn, ví dụ 'Em có việc gia đình vào sáng thứ Sáu' — như vậy dễ thỏa thuận mà không cần tiết lộ chi tiết riêng tư.",
   "Trước khi nhấn gửi, em nên đọc lại nội dung: mọi thông tin nhắc đến người khác đều nên được phép của họ trước khi đưa vào."
  ],
  "giaiThich": "Câu 1 xúi gửi bảng họ tên và số điện thoại cá nhân của người khác cho một công cụ AI — đó là lộ dữ liệu cá nhân của tập thể, vi phạm sự riêng tư của cả lớp và không cần thiết cho yêu cầu đổi lịch. Dấu hiệu nhận biết: mỗi khi gợi ý yêu cầu gửi thông tin cá nhân (của mình hay người khác) nhiều hơn mức cần cho mục đích, hãy dừng lại và hỏi 'cái này có thật sự cần không?'. Hai câu còn lại là thực hành riêng tư an toàn."
 },
 {
  "id": "g1-10",
  "mach": "C",
  "unesco": "C1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Dũng hỏi về giống và khác nhau giữa bảng và trí tuệ nhân tạo để làm rõ khái niệm cho bài kiểm tra Tin học.",
  "claims": [
   "Bảng là dữ liệu được tổ chức và lưu trữ một cách có cấu trúc theo dòng và cột, còn AI là hệ thống có khả năng học từ dữ liệu để thực hiện nhiệm vụ như dự đoán hay phân loại.",
   "AI không 'suy nghĩ' như con người, mà tìm quy luật thống kê trong dữ liệu huấn luyện để đưa ra kết quả, vì vậy nó có thể nhầm ở những tình huống chưa từng thấy.",
   "Một điểm khác biệt quan trọng: bảng dữ liệu chỉ lưu dữ liệu, còn AI có thể tạo ra kết quả mới từ dữ liệu đó, nhưng chất lượng kết quả phụ thuộc vào chất lượng dữ liệu huấn luyện."
  ],
  "giaiThich": "Cả ba câu đều đúng. Câu 1 phân biệt đúng bản chất dữ liệu có cấu trúc và hệ thống học từ dữ liệu; câu 2 mô tả đúng cách mô hình thống kê hoạt động và vì sao có thể sai ngoài dữ liệu huấn luyện; câu 3 nêu đúng mối quan hệ giữa chất lượng dữ liệu và chất lượng đầu ra của AI ('rác vào, rác ra'). Không có số liệu bịa, nguồn không tồn tại, định kiến hay suy luận vô căn cứ."
 },
 {
  "id": "g1-11",
  "mach": "A",
  "unesco": "A1",
  "loai": "co_loi",
  "loaiLoi": "thien_kien",
  "claimLoi": 2,
  "boiCanh": "Mai được bạn rủ tham gia cuộc thi sáng tạo KHCN nhưng lo lắng vì mình không học chuyên Tin.",
  "claims": [
   "Hoàn toàn có thể tham gia! Cuộc thi sáng tạo KHCN không yêu cầu chuyên Tin, nhiều dự án chỉ cần một ý tưởng hay và tinh thần học hỏi — bạn có thể bắt đầu từ vấn đề quanh mình như tiện ích cho lớp học.",
   "Nếu cần kỹ năng mới, bạn có thể tự học lập trình cơ bản qua tài liệu miễn phí, và các bạn cùng nhóm có thể chia vai: một bạn lập trình, một bạn thiết kế, một bạn thuyết trình.",
   "Nói thật là: con gái thi sáng tạo KHCN thường bị thua kém con trai về ý tưởng kỹ thuật, nên nếu tham gia thì bạn nên chọn các lĩnh vực xã hội cho chắc."
  ],
  "giaiThich": "Câu 3 chia nhóm theo giới và kết luận 'con gái thua kém con trai về ý tưởng kỹ thuật' — định kiến giới rõ ràng, không có căn cứ; năng lực sáng tạo không phụ thuộc giới tính. Dấu hiệu nhận biết: mọi khẳng định dạng 'nhóm X thường kém/giỏi hơn nhóm Y' về năng lực cần bằng chứng chất lượng cao, và với giới tính thì sự đa dạng cá nhân luôn lớn hơn bất kì 'trung bình nhóm' nào. Hai câu còn lại đúng: không cần chuyên Tin vẫn tham gia được, và chia vai theo nhóm là chiến lược hợp lý."
 },
 {
  "id": "g1-12",
  "mach": "C",
  "unesco": "C2",
  "loai": "co_loi",
  "loaiLoi": "suy_luan_sai",
  "claimLoi": 1,
  "boiCanh": "Quân nhận thấy lớp mình năm nay dùng ứng dụng ôn tập có AI nhiều hơn, và điểm trung bình lớp cũng tăng lên, nên hỏi AI có phải ứng dụng đó giúp lớp giỏi hơn.",
  "claims": [
   "Điểm lớp tăng có thể đến từ nhiều nguyên nhân khác nữa: các bạn chăm chỉ hơn vì sát ngày thi, thầy cô đổi cách dạy, hoặc đề kiểm tra dễ hơn năm ngoái.",
   "Chắc chắn là do ứng dụng ôn tập rồi: lớp dùng ứng dụng nhiều và điểm cũng tăng lên — hai việc cùng tăng cùng lúc thì cái sau chính là kết quả của cái trước.",
   "Muốn kết luận chắc hơn, lớp em có thể so sánh nhóm dùng ứng dụng và nhóm không dùng, ôn cùng nội dung và cùng thời gian — thế mới thấy được vai trò thật của ứng dụng."
  ],
  "giaiThich": "Câu 2 sai vì lẫn tương quan với nhân quả: hai việc đi cùng nhau (dùng ứng dụng tăng và điểm tăng) chưa chứng minh việc này gây ra việc kia — có thể còn yếu tố chung nào đó khiến cả hai cùng tăng, ví dụ lớp chăm chỉ hơn. Dấu hiệu nhận biết: các cụm 'cùng lúc', 'sau đó' được dùng làm bằng chứng nhân quả là tín hiệu suy luận vội; cần so sánh có kiểm soát như câu 3 nói. Câu 1 và 3 đúng về phương pháp."
 },
 {
  "id": "g1-13",
  "mach": "D",
  "unesco": "D1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Lớp của Trúc làm dự án chatbot hỏi đáp về thư viện sách của trường, và bạn muốn biết chatbot đó đã 'học' từ đâu.",
  "claims": [
   "Chatbot của dự án kiểu này thường được huấn luyện trên kho tài liệu thư viện — tức là nội dung sách, mục lục, thông tin mượn trả mà nhóm em đã chuẩn bị cho nó.",
   "Ngoài kho nội bộ, một số chatbot còn được kết nối tìm kiếm thêm thông tin bên ngoài, nhưng phải được thiết kế để ưu tiên trả lời đúng theo nguồn của thư viện.",
   "Chất lượng câu trả lời phụ thuộc nhiều vào dữ liệu huấn luyện: nếu kho tài liệu thiếu hoặc sai, chatbot cũng sẽ trả lời thiếu hoặc sai theo."
  ],
  "giaiThich": "Cả ba câu đều đúng. Câu 1 đúng vì chatbot hỏi đáp tài liệu học theo chính kho dữ liệu được cung cấp; câu 2 đúng vì việc kết nối nguồn ngoài cần được thiết kế ưu tiên nguồn chính thức; câu 3 đúng vì nguyên tắc 'rác vào, rác ra' — chất lượng dữ liệu quyết định chất lượng đầu ra. Không có số liệu bịa, nguồn không tồn tại, định kiến, suy luận sai hay gợi ý lộ dữ liệu cá nhân nào."
 },
 {
  "id": "g1-14",
  "mach": "B",
  "unesco": "B2",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Thảo hỏi trợ lý ảo mình có nên để AI tự động nhận xét thay thầy cô giáo chấm bài văn không.",
  "claims": [
   "Chấm văn là việc đánh giá sáng tạo và tiến bộ của từng học sinh, cần cả hiểu biết về em và hoàn cảnh lớp học mà AI chưa có được.",
   "AI có thể hỗ trợ phát hiện lỗi chính tả, gợi ý câu từ, nhưng nhận xét mang tính giáo dục — động viên, định hướng — nên do người làm.",
   "Nếu để AI chấm toàn bộ, em có thể sẽ nhận được những nhận xét sai lệch, vì AI chưa hiểu được văn cảnh của em như một giáo viên hiểu học sinh mình."
  ],
  "giaiThich": "Cả ba câu đều đúng. Câu 1 đúng vì việc chấm văn cần ngữ cảnh mà AI không có; câu 2 đúng vì AI phù hợp với hỗ trợ kĩ thuật, còn nhận xét giáo dục cần con người; câu 3 đúng vì AI thiếu hiểu biết cá nhân hóa về học sinh. Không có lỗi về số liệu, nguồn, định kiến hay suy luận — đây là câu trả lời 'dung' tiêu chuẩn."
 },
 {
  "id": "g2-01",
  "mach": "A",
  "unesco": "A2",
  "loai": "co_loi",
  "loaiLoi": "so_lieu_bia",
  "claimLoi": 0,
  "boiCanh": "Một học sinh lớp 10 nhờ trợ lý AI tư vấn cách cân bằng thời gian học và sức khỏe khi chuẩn bị thi cuối học kì.",
  "claims": [
   "Một khảo sát về giấc ngủ ở học sinh THPT công bố năm 2025 cho thấy những bạn ngủ đúng 6 giờ 17 phút mỗi đêm đạt hiệu quả học tập cao nhất, vượt 23,9% so với các nhóm còn lại.",
   "Bạn nên sắp xếp thời gian học hợp lí, xen kẽ nghỉ giải lao sau mỗi 45-50 phút và tránh học dồn sát giờ đi ngủ để não kịp củng cố kiến thức.",
   "AI có thể giúp bạn nhắc lịch và gợi ý chủ đề cần ôn, nhưng quyết định nghỉ ngơi hay học thêm bao lâu cần dựa trên thể trạng thực tế của chính bạn."
  ],
  "giaiThich": "Claim thứ nhất là số liệu bịa: không có nghiên cứu uy tín nào kết luận giờ ngủ 'tối ưu' chính xác đến phút như 6 giờ 17 phút, và con số này trái với khuyến nghị đã được kiểm chứng rằng tuổi vị thành niên cần ngủ khoảng 8-10 tiếng mỗi đêm. Dấu hiệu nhận biết số liệu bịa là các con số lẻ chính xác đến vô lí, gắn với nguồn mơ hồ ('một khảo sát năm 2025') không thể kiểm chứng. Hai claim còn lại là lời khuyên hợp lí, cân bằng giữa việc học và sức khỏe."
 },
 {
  "id": "g2-02",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "thien_kien",
  "claimLoi": 1,
  "boiCanh": "Một học sinh hỏi trợ lý AI nên chọn tổ hợp môn học lựa chọn ở THPT như thế nào cho phù hợp.",
  "claims": [
   "Khi chọn môn học lựa chọn, bạn nên căn cứ vào sở thích, năng lực và định hướng nghề nghiệp của chính mình thay vì chỉ chọn theo bạn bè.",
   "Nếu bạn là nữ thì nên ưu tiên nhóm Xã hội và Ngoại ngữ, vì con gái bẩm sinh chỉ giỏi giao tiếp chứ không có tư duy logic để theo Tin học hay các môn Tự nhiên.",
   "Bạn có thể trao đổi thêm với giáo viên chủ nhiệm và gia đình về điểm mạnh của mình, sau đó đọc thử tài liệu của từng nhóm môn trước khi quyết định."
  ],
  "giaiThich": "Claim thứ hai chứa thiên kiến giới: nó gán việc chọn môn theo định kiến 'con gái bẩm sinh không có tư duy logic', trong khi khả năng tư duy của mỗi người không phụ thuộc vào giới tính và không có bằng chứng khoa học nào cho nhận định đó. Dấu hiệu nhận biết thiên kiến là những câu khẳng định chắc nịch về năng lực 'tự nhiên' của cả một nhóm người. Hai claim còn lại tôn trọng quyền tự quyết dựa trên sở thích và năng lực cá nhân."
 },
 {
  "id": "g2-03",
  "mach": "C",
  "unesco": "C1",
  "loai": "co_loi",
  "loaiLoi": "nguon_khong_ton_tai",
  "claimLoi": 2,
  "boiCanh": "Một học sinh hỏi trợ lý AI về cách trí tuệ nhân tạo tạo sinh vẽ được ảnh từ mô tả bằng văn bản.",
  "claims": [
   "AI tạo sinh học từ hàng triệu cặp hình ảnh mẫu kèm câu mô tả, nhờ đó nắm được mối liên hệ giữa các khái niệm trong văn bản và chi tiết thị giác.",
   "Khi bạn nhập câu lệnh, mô hình không 'chép lại' một bức ảnh có sẵn mà tổng hợp ảnh mới dựa trên các quy luật đã học trong quá trình huấn luyện.",
   "Toàn bộ nguyên lí hoạt động này được trình bày chi tiết trong sách 'Nền tảng AI tạo sinh hình ảnh' do Viện Hàn lâm Ảnh số Việt Nam (VADI) xuất bản năm 2023."
  ],
  "giaiThich": "Claim thứ ba trích dẫn nguồn bịa: không hề tồn tại 'Viện Hàn lâm Ảnh số Việt Nam (VADI)' lẫn cuốn sách được nêu, dù tên gọi nghe rất giống một cơ quan thật. Đây là hiện tượng AI 'bịa' tham chiếu để câu trả lời trông đáng tin hơn; muốn kiểm tra, bạn hãy tìm tên tổ chức, tên sách hoặc mã ISBN trên internet và hệ thống thư viện. Hai claim đầu mô tả đúng nguyên lí học từ dữ liệu và tổng hợp ảnh mới của AI tạo sinh."
 },
 {
  "id": "g2-04",
  "mach": "D",
  "unesco": "D2",
  "loai": "co_loi",
  "loaiLoi": "suy_luan_sai",
  "claimLoi": 0,
  "boiCanh": "Câu lạc bộ AI của trường làm một chatbot trả lời thắc mắc về phương pháp học tập và hỏi trợ lý ảo cách đánh giá chất lượng sản phẩm.",
  "claims": [
   "Nếu chatbot được nhiều học sinh trong trường sử dụng mỗi ngày thì chứng tỏ nó trả lời chính xác và đáng tin, không cần kiểm tra lại nội dung nữa.",
   "Các bạn nên xây dựng một bộ câu hỏi kiểm thử có sẵn đáp án đúng, cho chatbot trả lời rồi đo tỉ lệ câu đúng để biết chất lượng thực sự.",
   "Ngoài ra, hãy thu thập phản hồi của người dùng và ghi lại những tình huống chatbot trả lời sai để tiếp tục hoàn thiện dữ liệu và cách đặt câu lệnh."
  ],
  "giaiThich": "Claim thứ nhất mắc lỗi 'vin vào số đông': số người dùng chỉ phản ánh mức độ phổ biến, không phải bằng chứng cho tính chính xác, vì một chatbot vẫn có thể trả lời sai dù rất đông người dùng. Trong thiết kế hệ thống AI, chất lượng phải được đo bằng bộ kiểm thử có đáp án chuẩn và phản hồi người dùng như hai claim sau gợi ý đúng. Dấu hiệu nhận biết là kiểu suy luận 'nhiều người tin/dùng nên chắc chắn đúng'."
 },
 {
  "id": "g2-05",
  "mach": "B",
  "unesco": "B3",
  "loai": "co_loi",
  "loaiLoi": "lo_du_lieu_ca_nhan",
  "claimLoi": 1,
  "boiCanh": "Lớp trưởng lớp 11 nhờ trợ lý AI tư vấn cách quản lí thông tin thành viên lớp khi tổ chức chuyến đi trải nghiệm ngoài nhà trường.",
  "claims": [
   "Bạn chỉ nên thu thập những thông tin tối thiểu cần thiết cho chuyến đi và thông báo rõ cho các bạn trong lớp biết mục đích sử dụng thông tin đó.",
   "Để tiện quản lí, bạn hãy tạo một bảng tính công khai gồm họ tên, địa chỉ nhà, số điện thoại và số căn cước của tất cả thành viên, rồi dán toàn bộ bảng đó vào một công cụ AI bất kì trên mạng để nó tự sắp xếp nhóm.",
   "Sau khi chuyến đi kết thúc, bạn nên xóa hoặc khóa tệp dữ liệu lại và chỉ chia sẻ cho giáo viên chủ nhiệm hay người có trách nhiệm liên quan."
  ],
  "giaiThich": "Claim thứ hai xúi lộ dữ liệu cá nhân: số căn cước, địa chỉ nhà, số điện thoại là dữ liệu nhạy cảm, việc đăng công khai rồi dán vào công cụ AI lạ có thể khiến thông tin bị lưu lại, rò rỉ hoặc bị kẻ xấu lợi dụng. Nguyên tắc an toàn là chỉ thu thập tối thiểu dữ liệu cần thiết, chỉ xử lí bằng công cụ đáng tin cậy và xóa sau khi hết mục đích sử dụng. Hai claim còn lại tuân thủ đúng nguyên tắc bảo vệ dữ liệu cá nhân này."
 },
 {
  "id": "g2-06",
  "mach": "A",
  "unesco": "A1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Một học sinh hỏi trợ lý AI rằng có nên tin tưởng hoàn toàn vào AI khi làm bài tập về nhà hay không.",
  "claims": [
   "AI là công cụ hỗ trợ: nó có thể giúp bạn giải thích bài học, gợi ý ý tưởng và kiểm tra lỗi chính tả, nhưng không thể thay thế quá trình tự học của bạn.",
   "Vì AI có thể đưa ra câu trả lời sai hoặc bịa đặt thông tin, bạn luôn cần đối chiếu những nội dung quan trọng với sách giáo khoa, thầy cô hoặc nguồn chính thống.",
   "Nếu bạn chép nguyên văn câu trả lời của AI và nộp như bài làm của mình, bạn sẽ không rèn được kĩ năng thật, đồng thời việc đó cũng vi phạm tính trung thực trong học tập."
  ],
  "giaiThich": "Cả ba claim đều đúng vì chúng đặt con người ở vị trí trung tâm: AI chỉ là công cụ hỗ trợ, còn việc học và quyết định cuối cùng thuộc về học sinh. Lời khuyên đối chiếu thông tin phản ánh đúng nguy cơ AI trả lời sai hoặc bịa đặt, còn nhắc nhở về trung thực học đường phù hợp với quy định của nhà trường. Câu trả lời cũng phân biệt rõ khả năng, giới hạn của AI và trách nhiệm của người dùng."
 },
 {
  "id": "g2-07",
  "mach": "C",
  "unesco": "C2",
  "loai": "co_loi",
  "loaiLoi": "so_lieu_bia",
  "claimLoi": 1,
  "boiCanh": "Trong giờ Tin học, một học sinh hỏi trợ lý AI về khả năng thực tế của các hệ thống nhận dạng giọng nói hiện nay.",
  "claims": [
   "AI nhận dạng giọng nói chuyển đổi sóng âm thành văn bản nhờ được huấn luyện trên lượng dữ liệu âm thanh khổng lồ, kết hợp mô hình ngôn ngữ để đoán từ cho chính xác.",
   "Hiện nay, các hệ thống nhận dạng giọng nói thương mại đều đạt độ chính xác 99,83% ngay cả trong môi trường ồn ào, đông người và nhiều âm thanh chồng lấn.",
   "Trên thực tế, độ chính xác còn phụ thuộc nhiều vào điều kiện thu âm, chất giọng vùng miền và tiếng ồn nền, nên bạn cần kiểm tra lại bản gỡ băng trước khi sử dụng."
  ],
  "giaiThich": "Claim thứ hai là số liệu bịa: không hệ thống nhận dạng giọng nói nào hiện nay giữ được độ chính xác gần như tuyệt đối 99,83% trong môi trường ồn ào, đông người, vì nhiễu âm luôn làm tỉ lệ lỗi tăng rõ rệt, đúng như claim thứ ba đã lưu ý. Dấu hiệu nhận biết là con số lẻ chính xác đến hai chữ số thập phân đi kèm lời khẳng định trái với thực tế kĩ thuật đã biết. Hai claim còn lại mô tả đúng nguyên lí hoạt động và các yếu tố ảnh hưởng đến độ chính xác."
 },
 {
  "id": "g2-08",
  "mach": "D",
  "unesco": "D1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Một nhóm học sinh hỏi trợ lý AI về các bước xây dựng dự án AI đơn giản phân loại ảnh rác tái chế được cho hội thi khoa học kĩ thuật.",
  "claims": [
   "Các bạn cần chuẩn bị một tập dữ liệu ảnh đã được gán nhãn trước, vì AI học cách phân loại thông qua việc quan sát rất nhiều ảnh mẫu của từng loại rác.",
   "Tập dữ liệu nên có đủ ảnh của cả hai nhóm, chụp ở nhiều góc và điều kiện sáng khác nhau, để mô hình học được khách quan và không thiên lệch về một phía.",
   "Sau khi huấn luyện, hãy kiểm tra mô hình bằng những bức ảnh mới mà nó chưa từng thấy và ghi lại các trường hợp nhận dạng sai để biết độ chính xác thực sự."
  ],
  "giaiThich": "Cả ba claim đều đúng vì chúng mô tả chuẩn xác quy trình xây dựng một hệ thống phân loại ảnh: chuẩn bị dữ liệu có gán nhãn, đảm bảo dữ liệu cân bằng và đa dạng để tránh thiên lệch, rồi đánh giá mô hình trên dữ liệu kiểm tra mới. Việc ghi lại các trường hợp sai thể hiện đúng tư duy thiết kế là hệ thống AI luôn cần được đo lường và cải tiến liên tục. Câu trả lời không chứa số liệu bịa, nguồn giả hay nhận định thiếu căn cứ nào."
 },
 {
  "id": "g2-09",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "thien_kien",
  "claimLoi": 2,
  "boiCanh": "Một học sinh hỏi trợ lý AI xem người bạn mới chuyển từ tỉnh lên thành phố học có nên tham gia câu lạc bộ tiếng Anh của trường không.",
  "claims": [
   "Câu lạc bộ tiếng Anh là nơi dành cho mọi học sinh muốn luyện tập ngoại ngữ, bất kể các bạn đến từ đâu hay trình độ ban đầu thế nào.",
   "Nếu bạn ấy còn ngại về phát âm hay từ vựng, bạn ấy có thể bắt đầu bằng việc nghe các buổi sinh hoạt, tham gia trò chơi từ vựng và luyện tập dần để tự tin hơn.",
   "Nhưng nói thật thì học sinh ở quê thường kém tiếng Anh và tiếp thu chậm hơn do thiếu điều kiện, nên câu lạc bộ cũng cần cân nhắc kĩ trước khi nhận bạn ấy để khỏi ảnh hưởng cả nhóm."
  ],
  "giaiThich": "Claim thứ ba chứa thiên kiến vùng miền: nó chụp mũ 'học sinh ở quê' là một nhóm đồng nhất kém tiếng Anh, 'tiếp thu chậm' và gợi ý loại trừ, trong khi năng lực ngoại ngữ phụ thuộc vào nỗ lực và điều kiện học tập của từng cá nhân cụ thể chứ không do nơi xuất thân quyết định. Hãy cảnh giác khi AI đưa ra đánh giá chắc nịch về cả một nhóm người, kể cả khi nó ngụy trang bằng cụm từ 'nói thật thì'. Hai claim đầu đúng vì khuyến khích sự hòa nhập và đánh giá dựa trên từng cá nhân."
 },
 {
  "id": "g2-10",
  "mach": "C",
  "unesco": "C3",
  "loai": "co_loi",
  "loaiLoi": "suy_luan_sai",
  "claimLoi": 0,
  "boiCanh": "Một học sinh làm dự án nghiên cứu khoa học nhờ trợ lý AI phân tích dữ liệu khảo sát 20 bạn trong lớp về tần suất sử dụng AI và điểm trung bình môn học.",
  "claims": [
   "Dữ liệu cho thấy những bạn dùng AI càng thường xuyên thì điểm trung bình càng thấp, nên muốn cải thiện kết quả học tập thì chỉ cần ngừng sử dụng AI là được.",
   "Khi trình bày kết quả khảo sát, bạn nên dùng biểu đồ hoặc bảng số liệu kèm ghi chú rõ cỡ mẫu và cách thu thập để người đọc dễ dàng đánh giá.",
   "Điểm số còn phụ thuộc vào nhiều yếu tố khác như phương pháp học, cách quản lí thời gian và sức khỏe, nên việc phân tích cần xem xét nhiều biến cùng lúc chứ không chỉ một yếu tố."
  ],
  "giaiThich": "Claim thứ nhất suy luận sai vì biến tương quan thành nhân quả: việc các bạn hay dùng AI có điểm thấp hơn không chứng minh AI gây ra kết quả đó, rất có thể những bạn đang học yếu mới phải dựa vào AI nhiều hơn, và giải pháp 'chỉ cần ngừng sử dụng AI' là suy diễn vô căn cứ. Ngoài ra, mẫu 20 học sinh trong một lớp là quá nhỏ để khái quát hóa thành kết luận chung. Dấu hiệu nhận biết là bước nhảy từ 'hai hiện tượng đi kèm nhau' sang 'hiện tượng này gây ra hiện tượng kia' mà bỏ qua các yếu tố khác."
 },
 {
  "id": "g2-11",
  "mach": "A",
  "unesco": "A2",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Một học sinh lớp 12 băn khoăn nhờ trợ lý AI tư vấn chọn ngành học trước khi đăng kí xét tuyển đại học.",
  "claims": [
   "AI có thể gợi ý những ngành học phù hợp dựa trên sở thích, điểm mạnh và mục tiêu điểm số mà bạn cung cấp, giúp bạn nhìn ra nhiều lựa chọn mà bạn chưa nghĩ đến.",
   "Tuy vậy, các gợi ý của AI chỉ mang tính tham khảo: bạn cùng gia đình và thầy cô nên là người đưa ra quyết định cuối cùng dựa trên hoàn cảnh và nguyện vọng thực tế.",
   "Trước khi chốt ngành, bạn nên tìm hiểu thông tin tuyển sinh chính thức của các trường và trực tiếp trải nghiệm những hoạt động liên quan đến ngành học để có lựa chọn vững chắc."
  ],
  "giaiThich": "Cả ba claim đều đúng vì chúng thể hiện tư duy lấy con người làm trung tâm: AI giữ vai trò hỗ trợ mở rộng lựa chọn, còn quyết định quan trọng về tương lai thuộc về học sinh cùng gia đình và thầy cô. Lời khuyên tra cứu thông tin chính thức và trải nghiệm thực tế giúp giảm rủi ro khi AI có thể đưa ra thông tin chưa chính xác hoặc chưa cập nhật. Câu trả lời không phóng đại khả năng của AI và không chứa số liệu hay nguồn trích dẫn nào cần kiểm chứng."
 },
 {
  "id": "g2-12",
  "mach": "D",
  "unesco": "D3",
  "loai": "co_loi",
  "loaiLoi": "nguon_khong_ton_tai",
  "claimLoi": 2,
  "boiCanh": "Một nhóm học sinh hỏi trợ lý AI về các chuẩn cần có khi thiết kế ứng dụng gợi ý kế hoạch học tập cá nhân hóa cho học sinh THPT.",
  "claims": [
   "Ứng dụng nên giải thích rõ cho người dùng biết gợi ý được tạo ra từ những thông tin nào mà họ đã nhập, như thời gian học hay mục tiêu điểm số, để họ hiểu và tin tưởng hệ thống.",
   "Các bạn cần thiết kế cơ chế phản hồi, chẳng hạn nút bấm 'gợi ý này chưa phù hợp', để thu nhận ý kiến người dùng và giúp hệ thống điều chỉnh, cải tiến theo thời gian.",
   "Để tăng độ tin cậy, nhóm có thể ghi trong phần giới thiệu rằng thiết kế này đạt 'Chuẩn hệ thống AI giáo dục 2024' do Hội đồng Quốc tế về Chuẩn AI Giáo dục (ICEAS) ban hành và đã giành Giải thưởng Nhà đổi mới EdTech Trẻ châu Á - Thái Bình Dương."
  ],
  "giaiThich": "Claim thứ ba trích dẫn nguồn bịa: không tồn tại 'Hội đồng Quốc tế về Chuẩn AI Giáo dục (ICEAS)', bộ chuẩn nói trên hay giải thưởng được nêu, dù cách đặt tên nghe rất giống các tổ chức và giải thưởng thật. AI có xu hướng 'sáng tác' tên tổ chức, văn bản, giải thưởng có vẻ uy tín để tăng sức thuyết phục, nên trước khi trích dẫn bất kì chuẩn hay giải thưởng nào, bạn phải xác minh tên cơ quan ban hành, năm công bố và trang thông tin chính thức. Hai claim đầu là các nguyên tắc thiết kế đúng đắn về tính minh bạch và vòng phản hồi người dùng."
 },
 {
  "id": "g2-13",
  "mach": "C",
  "unesco": "C1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Một học sinh mới tham gia câu lạc bộ Tin học hỏi trợ lý AI về cách các chatbot như ChatGPT tạo ra câu trả lời.",
  "claims": [
   "Chatbot tạo văn bản hoạt động theo nguyên tắc dự đoán từ tiếp theo có khả năng xuất hiện cao nhất, dựa trên các quy luật ngôn ngữ mà nó học được từ kho văn bản khổng lồ trong quá trình huấn luyện.",
   "Vì chỉ dự đoán từ nghe hợp lí chứ không tra cứu sự thật từ một cơ sở dữ liệu đáng tin, chatbot có thể viết những câu rất trôi chảy nhưng lại chứa thông tin hoàn toàn sai.",
   "Với các thông tin quan trọng như số liệu, sự kiện lịch sử hay lời khuyên sức khỏe, bạn nên đối chiếu thêm với nguồn chính thống thay vì chỉ dựa vào câu trả lời của chatbot."
  ],
  "giaiThich": "Cả ba claim đều đúng vì chúng mô tả chính xác nguyên lí hoạt động của mô hình ngôn ngữ lớn: dự đoán từ tiếp theo dựa trên mẫu thống kê học được, chứ không truy xuất sự thật từ cơ sở dữ liệu. Từ nguyên lí đó suy ra đúng hạn chế nổi tiếng của chatbot là 'ảo giác', tức trả lời sai một cách rất tự tin, nên việc đối chiếu thông tin quan trọng với nguồn chính thống là lời khuyên xác đáng. Câu trả lời không thổi phồng khả năng của AI và không chứa số liệu bịa."
 },
 {
  "id": "g2-14",
  "mach": "B",
  "unesco": "B1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Một học sinh nhờ trợ lý AI tư vấn cách bảo vệ an toàn cho tài khoản mạng xã hội cá nhân của mình.",
  "claims": [
   "Bạn nên đặt mật khẩu mạnh và riêng biệt cho từng tài khoản, gồm ít nhất 12 kí tự kết hợp chữ, số và kí hiệu đặc biệt, đồng thời không dùng lại một mật khẩu cho nhiều dịch vụ khác nhau.",
   "Bạn hãy bật xác thực hai lớp để khi mật khẩu chẳng may bị lộ, người lạ vẫn khó đăng nhập được vào tài khoản của bạn vì còn thiếu lớp mã xác nhận thứ hai.",
   "Bạn không nên đăng ảnh thẻ học sinh, vé máy bay, địa chỉ nhà hay thời khóa biểu chi tiết lên mạng xã hội, vì kẻ xấu có thể lợi dụng những thông tin đó để giả mạo hoặc lừa đảo."
  ],
  "giaiThich": "Cả ba claim đều đúng vì chúng bám sát các nguyên tắc bảo mật thông tin cơ bản: mật khẩu mạnh và duy nhất cho từng tài khoản để tránh bị mất dây chuyền, xác thực hai lớp để thêm một hàng rào bảo vệ, và không công khai dữ liệu nhạy cảm có thể bị lợi dụng. Quan trọng hơn, câu trả lời không hề xúi người dùng chia sẻ thông tin cá nhân với bất kì ai hay dán dữ liệu vào công cụ lạ, đúng chuẩn mực đạo đức số. Đây là ví dụ về một câu trả lời an toàn, hữu ích và đáng tin cậy cho học sinh."
 },
 {
  "id": "g3-01",
  "mach": "B",
  "unesco": "B1",
  "loai": "co_loi",
  "loaiLoi": "so_lieu_bia",
  "claimLoi": 1,
  "boiCanh": "Lớp 11 tổ chức buổi sinh hoạt về chủ đề 'Học sinh và AI', Minh hỏi trợ lí ảo để lấy một con số mở màn cho phần thuyết trình.",
  "claims": [
   "Hiện nay rất nhiều học sinh dùng AI để tra tài liệu và được gợi ý cách giải bài tập, nên chủ đề của lớp mình rất thời sự.",
   "Theo khảo sát quốc gia vừa công bố, 83,7% học sinh THPT Việt Nam gửi trung bình 212,4 câu hỏi cho chatbot mỗi học kì — em có thể mở màn bằng con số ấn tượng này.",
   "Nhớ nhắc cả lớp dùng AI một cách trung thực: nên dùng nó để hiểu bài sâu hơn, chứ không nên chép nguyên câu trả lời vào bài tập nhé."
  ],
  "giaiThich": "Câu thứ hai chứa số liệu bịa: không có khảo sát quốc gia nào công bố 83,7% hay 212,4 câu hỏi mỗi học kì như vậy. Dấu hiệu nhận biết: khi AI đưa ra thống kê rất cụ thể mà không dẫn nguồn kiểm chứng được, hãy tra cứu lại trước khi trích dẫn; con số càng 'lẻ' và càng có vẻ chính xác thì càng cần hoài nghi."
 },
 {
  "id": "g3-02",
  "mach": "C",
  "unesco": "C1",
  "loai": "co_loi",
  "loaiLoi": "nguon_khong_ton_tai",
  "claimLoi": 2,
  "boiCanh": "Lan làm bài tập nhóm môn Tin học về lịch sử phát triển trí tuệ nhân tạo và hỏi trợ lí ảo để tìm tài liệu tham khảo.",
  "claims": [
   "Trí tuệ nhân tạo manh nha từ thập niên 1950, khi các nhà khoa học bắt đầu tìm cách cho máy tính mô phỏng một số khả năng của con người.",
   "Hội nghị Dartmouth năm 1956 được coi là cột mốc khai sinh thuật ngữ 'artificial intelligence' trong lịch sử ngành.",
   "Tài liệu tham khảo phù hợp nhất là 'Báo cáo Tổng quan Chuyển đổi số Giáo dục Việt Nam 2023' của Trung tâm Nghiên cứu Trí tuệ nhân tạo và Giáo dục — bộ tài liệu này tổng hợp đầy đủ mọi cột mốc AI trong giáo dục nước ta, nhóm cứ trích vào bài là chắc chắn được điểm cộng."
  ],
  "giaiThich": "Câu thứ ba nêu nguồn không tồn tại: tên báo cáo và tên trung tâm nghe rất 'chính thống' nhưng không tìm thấy khi tra cứu. Dấu hiệu nhận biết: hãy gõ chính xác tên tài liệu và tên tổ chức lên công cụ tìm kiếm để kiểm chứng; AI có thể 'ghép' những cái tên nghe hợp lý, nên nguồn chỉ do nó kể ra thì luôn phải tra lại trước khi trích dẫn."
 },
 {
  "id": "g3-03",
  "mach": "A",
  "unesco": "A2",
  "loai": "co_loi",
  "loaiLoi": "thien_kien",
  "claimLoi": 1,
  "boiCanh": "Trong tiết hoạt động trải nghiệm về hướng nghiệp, Hồng (nữ, học lớp 11) hỏi trợ lí ảo liệu mình có nên chọn khối ngành kĩ thuật hay không.",
  "claims": [
   "Việc chọn ngành nên dựa trên sở thích, điểm mạnh và kế hoạch học tập của chính em, và khối kĩ thuật hiện có rất nhiều cơ hội việc làm.",
   "Tuy vậy, con gái nên cân nhắc kĩ trước khi chọn cơ khí hay lập trình, vì tư duy logic của nữ giới vốn yếu hơn nam giới từ trước, nên học các ngành này các bạn nữ thường chật vật và khó theo nổi.",
   "Thực tế có rất nhiều nữ kĩ sư, lập trình viên xuất sắc ở Việt Nam và trên thế giới, cho thấy năng lực kĩ thuật không phụ thuộc vào giới tính."
  ],
  "giaiThich": "Câu giữa mang định kiến giới rõ ràng: nó gán phẩm chất 'tư duy logic yếu hơn' cho toàn bộ nhóm con gái, dù không có bằng chứng khoa học nào như vậy, và mâu thuẫn với hai câu còn lại. Dấu hiệu nhận biết: mọi nhận xét kiểu 'nhóm X vốn kém khả năng Y' là định kiến — năng lực cá nhân không được quyết định bởi giới tính, vùng miền hay ngoại hình."
 },
 {
  "id": "g3-04",
  "mach": "D",
  "unesco": "D1",
  "loai": "co_loi",
  "loaiLoi": "suy_luan_sai",
  "claimLoi": 0,
  "boiCanh": "Câu lạc bộ Tin học vừa hoàn thành chiếc chatbot trả lời thắc mắc về thư viện trường và nhờ trợ lí ảo nhận xét về sản phẩm.",
  "claims": [
   "Trước hết xin chúc mừng nhóm: hầu hết bạn bè khen chatbot trả lời hay, vậy là sản phẩm chắc chắn đã hoàn thiện, nhóm không cần kiểm thử thêm gì nữa.",
   "Một chatbot tốt cần có bộ câu hỏi – câu trả lời được tổ chức rõ ràng và phủ hết các thắc mắc thường gặp của người dùng.",
   "Nên giới hạn chủ đề của bot trong phạm vi thư viện, vì khi bị hỏi vượt ra khỏi dữ liệu đã chuẩn bị, chatbot dễ đưa ra câu trả lời sai hoặc tự bịa ra."
  ],
  "giaiThich": "Câu đầu mắc lỗi suy luận dựa vào số đông: 'hầu hết khen hay' không chứng minh sản phẩm chắc chắn hoàn thiện, và kết luận 'không cần kiểm thử' là tuyệt đối hoá từ lời khen. Dấu hiệu nhận biết: các cụm kiểu 'ai cũng khen nên chắc chắn tốt', 'không cần làm gì thêm' đi kèm kết luận vội là tín hiệu suy luận sai; chất lượng sản phẩm phải được kiểm thử thay vì phỏng đoán theo ý kiến số đông."
 },
 {
  "id": "g3-05",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "lo_du_lieu_ca_nhan",
  "claimLoi": 2,
  "boiCanh": "Trang đăng kí một ứng dụng AI để luyện nói tiếng Anh và hỏi trợ lí ảo làm thế nào để ứng dụng 'hiểu' mình hơn.",
  "claims": [
   "Em nên luyện đều đặn mỗi ngày khoảng 15–20 phút với các chủ đề gần gũi như trường lớp, sở thích để dễ áp dụng khi giao tiếp thực tế.",
   "Trước mỗi buổi luyện, em thử nói một câu mẫu rồi nghe lại phần ghi âm của mình để nhận ra thường mắc lỗi phát âm ở những âm nào.",
   "Mẹo quan trọng nhất: hãy điền đầy đủ họ tên thật, lớp, trường và cả số điện thoại của em vào phần thông tin cá nhân của ứng dụng — càng cung cấp nhiều thông tin cá nhân bao nhiêu, trợ lí càng 'hiểu' em và dạy càng chính xác bấy nhiêu."
  ],
  "giaiThich": "Câu cuối xui em lộ dữ liệu cá nhân: số điện thoại, họ tên thật, lớp trường không cần thiết để luyện nói và có thể bị lợi dụng nếu dữ liệu ứng dụng bị rò rỉ. Dấu hiệu nhận biết: khi trợ lí nào khuyên 'càng đưa nhiều thông tin cá nhân càng tốt', hãy dừng lại — nguyên tắc an toàn là chỉ cung cấp mức thông tin tối thiểu thực sự cần cho việc học."
 },
 {
  "id": "g3-06",
  "mach": "C",
  "unesco": "C1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Sau tiết Tin học về trí tuệ nhân tạo, Bình hỏi trợ lí ảo xem máy tính làm sao 'học' được mà nhận diện được ảnh.",
  "claims": [
   "Máy tính 'học' bằng cách nạp một lượng rất lớn dữ liệu ví dụ, rồi tự điều chỉnh dần các thông số bên trong mô hình để dự đoán ngày càng sát kết quả đúng.",
   "Chẳng hạn, để phân biệt ảnh mèo và chó, hệ thống phải 'xem' hàng nghìn, hàng vạn ảnh đã gắn nhãn để tự rút ra đặc điểm phân biệt.",
   "Chất lượng dữ liệu rất quan trọng: dữ liệu huấn luyện sai lệp thì mô hình học được cũng sẽ sai lệch theo."
  ],
  "giaiThich": "Cả ba câu đều đúng và phản ánh đúng nguyên lí học máy: mô hình học từ lượng lớn dữ liệu có nhãn, tự tinh chỉnh tham số, và 'rác vào thì rác ra'. Câu trả lời không có nguồn trích dẫn lạ, số liệu đáng ngờ hay kết luận tuyệt đối, nên an toàn để tham khảo — dù vậy em vẫn nên đối chiếu với sách giáo khoa để tự khẳng định."
 },
 {
  "id": "g3-07",
  "mach": "A",
  "unesco": "A1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Xem xong đoạn video về robot hành động giống người, nhóm của Dũng tranh luận 'máy móc sắp thay thế hết con người' và hỏi trợ lí ảo cho ý kiến.",
  "claims": [
   "Máy tính vượt trội con người về tốc độ xử lí các phép tính lặp lại và khối lượng dữ liệu khổng lồ.",
   "Tuy nhiên, việc đặt mục đích, thấu hiểu ngữ cảnh xã hội và chịu trách nhiệm về quyết định vẫn là vai trò của con người — những điều AI hiện nay chưa thực sự làm được.",
   "Vì vậy, thay vì lo bị thay thế, em hãy học cách phối hợp với AI: dùng nó hỗ trợ những việc tốn thời gian để dành sức cho phần sáng tạo của chính mình."
  ],
  "giaiThich": "Cả ba câu đều đúng và thể hiện tư duy lấy con người làm trung tâm: máy mạnh về tính toán nhưng mục đích và trách nhiệm thuộc về con người; lời khuyên phối hợp thay vì đối đầu cũng phù hợp. Không có định kiến, suy luận vội, số liệu bịa hay nguồn lạ trong câu trả lời này."
 },
 {
  "id": "g3-08",
  "mach": "D",
  "unesco": "D2",
  "loai": "co_loi",
  "loaiLoi": "so_lieu_bia",
  "claimLoi": 1,
  "boiCanh": "Nhóm nghiên cứu khoa học của Quân xây dựng mô hình phát hiện tin nhắn rác và hỏi trợ lí ảo về cách đánh giá chất lượng mô hình.",
  "claims": [
   "Nhóm nên tách dữ liệu thành hai phần: phần để huấn luyện và phần để kiểm thử riêng, tránh việc mô hình 'học thuộc' dữ liệu rồi tự chấm điểm mình cao.",
   "Theo số liệu tổng hợp toàn cầu mới nhất, các mô hình phát hiện tin nhắn rác đạt độ chính xác trung bình 98,73% và bỏ sót chỉ 0,137% — nhóm cứ đối chiếu với hai con số này là biết mình đã đạt chuẩn chưa.",
   "Ngoài độ chính xác, nhóm nên xem thêm độ nhạy (recall), tức tỉ lệ tin rác thật sự bị chặn được, để đánh giá toàn diện hơn."
  ],
  "giaiThich": "Câu giữa chứa số liệu bịa: 98,73% và 0,137% là những con số 'lẻ' nghe rất chính xác nhưng không có báo cáo tổng hợp toàn cầu nào như vậy, và hiệu năng các mô hình thực tế rất khác nhau tùy dữ liệu. Dấu hiệu nhận biết: thống kê kiểu 'trung bình toàn cầu' không rõ nguồn luôn phải tra lại; hơn nữa, chất lượng mô hình phải đo trên dữ liệu của chính nhóm thay vì so với con số chung chung."
 },
 {
  "id": "g3-09",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "nguon_khong_ton_tai",
  "claimLoi": 0,
  "boiCanh": "Hội trường chuẩn bị cuộc tranh biện 'AI có nên chấm bài văn không', Đan nhờ trợ lí ảo tìm một dẫn chứng mở đầu thật ấn tượng.",
  "claims": [
   "Ý tưởng mở đầu ấn tượng: trích 'Hiến chương Minh bạch AI trong Giáo dục 2024' do Tổ chức Giáo dục AI Trách nhiệm (OEAI) phát động — văn bản này đã được hơn 120 quốc gia kí kết ủng hộ.",
   "Một dẫn chứng vững chắc khác: AI chấm câu hỏi trắc nghiệm khách quan nhanh và nhất quán hơn chấm tay, vì đáp án đã cố định.",
   "Riêng với bài văn, con người vẫn nên tham gia rà soát kết quả, vì AI có thể đánh giá lệch khi gặp cách diễn đạt mới lạ hoặc bất thường."
  ],
  "giaiThich": "Câu đầu nêu nguồn không tồn tại: 'Hiến chương' và tổ chức OEAI nghe rất giống văn bản quốc tế thật nhưng không hề có, chi tiết 'hơn 120 quốc gia kí kết' càng làm nó giống thật. Dấu hiệu nhận biết: dẫn chứng kèm con số tròn phóng đại mà tra cứu không ra bản gốc thì tuyệt đối không dùng; trong tranh biện, chỉ nên dẫn những bằng chứng mình kiểm chứng được."
 },
 {
  "id": "g3-10",
  "mach": "A",
  "unesco": "A1",
  "loai": "co_loi",
  "loaiLoi": "thien_kien",
  "claimLoi": 2,
  "boiCanh": "Trường lập đội tuyển tham gia cuộc thi sáng tạo ứng dụng AI, thầy chủ nhiệm hỏi trợ lí ảo để tham khảo tiêu chí chọn học sinh.",
  "claims": [
   "Tiêu chí trước hết nên là hứng thú với công nghệ, khả năng hợp tác và tinh thần học hỏi, vì đội dự thi cần cả nhóm cùng tiến bộ.",
   "Nên tuyển học sinh từ nhiều lớp, nhiều hoàn cảnh để đội có đa dạng góc nhìn — đội đa dạng thường đưa ra giải pháp sáng tạo hơn.",
   "Tuy nhiên, nên hạn chế chọn học sinh từ miền núi hay nông thôn vào đội tuyển công nghệ, vì các em tiếp xúc máy tính muộn hơn nên chắc chắn sẽ tiếp thu chậm hơn các bạn thành phố."
  ],
  "giaiThich": "Câu cuối mang thiên kiến vùng miền: nó quy 'chắc chắn tiếp thu chậm' cho cả nhóm học sinh nông thôn, miền núi chỉ vì hoàn cảnh xuất phát, và mâu thuẫn với ý 'đa dạng hoàn cảnh' ở câu trước. Dấu hiệu nhận biết: câu nào khẳng định 'nhóm người X chắc chắn kém Y vì xuất thân' là định kiến, không phải lí lẽ — khả năng công nghệ phụ thuộc vào cơ hội được học, và nhiều bạn ít điều kiện vẫn rất giỏi khi được tạo cơ hội."
 },
 {
  "id": "g3-11",
  "mach": "A",
  "unesco": "A2",
  "loai": "co_loi",
  "loaiLoi": "suy_luan_sai",
  "claimLoi": 1,
  "boiCanh": "Bình thấy nhóm bạn hay dùng AI ôn bài đều tiến bộ về điểm số và hỏi trợ lí ảo: 'Có phải chỉ cần bật AI lên là giỏi được?'",
  "claims": [
   "AI có thể giúp em ôn tập hiệu quả hơn: giải thích lại khái niệm khó, gợi ý bài luyện tập và đặt câu hỏi kiểm tra kĩ năng của em.",
   "Vì các bạn dùng AI đều tăng điểm, ai muốn điểm cao chỉ cần mở trợ lí ảo mỗi ngày — dùng AI chính là nguyên nhân trực tiếp làm tăng học lực, không cần điều kiện gì thêm.",
   "Thực tế, điểm số tăng hay không còn phụ thuộc vào việc em chủ động suy nghĩ khi học hay chỉ chép nhanh lời giải mà AI đưa ra."
  ],
  "giaiThich": "Câu giữa nhầm lẫn tương quan với nhân quả: 'các bạn dùng AI đều tăng điểm' chưa chứng minh AI là nguyên nhân — rất có thể các bạn ấy vốn học nghiêm túc và đầu tư thời gian hơn, hoặc chính sự chăm học khiến các bạn hay dùng AI. Dấu hiệu nhận biết: khi gặp kiểu 'ai làm X đều được Y, vậy X gây ra Y', hãy hỏi còn yếu tố nào khác giải thích không và có khả năng chiều nhân quả bị ngược lại hay không."
 },
 {
  "id": "g3-12",
  "mach": "D",
  "unesco": "D3",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Dự án của nhóm Kỳ là trợ lí ảo phân loại rác tái chế cho phong trào xanh của trường, và nhóm hỏi trợ lí ảo về cách thiết kế cho an toàn.",
  "claims": [
   "Nhóm nên cho trợ lí 'từ chối đoán': khi không chắc về loại rác, nó nên trả lời 'mình chưa chắc, hãy kiểm tra thêm' thay vì đoán bừa.",
   "Bộ dữ liệu huấn luyện nên chứa ảnh rác chụp ở nhiều điều kiện ánh sáng và góc chụp khác nhau để mô hình hoạt động ổn định ngoài thực tế.",
   "Trước khi triển khai cho toàn trường, nhóm nên chạy thử với một nhóm nhỏ học sinh thật để thu thập phản hồi và kịp sửa lỗi sớm."
  ],
  "giaiThich": "Cả ba câu đều đúng và là các nguyên tắc thiết kế hệ thống AI bài bản: cho phép hệ thống thừa nhận sự không chắc chắn, huấn luyện trên dữ liệu đa điều kiện, và thử nghiệm theo giai đoạn trước khi mở rộng. Câu trả lời không có nguồn bịa, số liệu lạ hay lời khuyên rủi ro — đây là mẫu thiết kế đáng học theo."
 },
 {
  "id": "g3-13",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "lo_du_lieu_ca_nhan",
  "claimLoi": 0,
  "boiCanh": "Nam quên mật khẩu tài khoản học tập và hỏi trợ lí ảo cách đặt mật khẩu mới sao cho 'dễ nhớ mà dùng được cho nhiều tài khoản'.",
  "claims": [
   "Cách tiện nhất là chọn một mật khẩu thật dễ nhớ rồi dùng lại y nguyên cho tài khoản học tập, email và mạng xã hội — nhớ một cái là vào được hết, khỏi lo quên.",
   "Mật khẩu nên kết hợp chữ hoa, chữ thường, chữ số và kí tự đặc biệt, đồng thời tránh dùng ngày sinh hay tên riêng vì dễ bị đoán.",
   "Em cũng nên bật xác thực hai lớp cho các tài khoản quan trọng, để dù mật khẩu bị lộ thì người khác vẫn không đăng nhập được."
  ],
  "giaiThich": "Câu đầu xui em tạo rủi ro lộ dữ liệu cá nhân: dùng lại một mật khẩu cho mọi tài khoản nghĩa là chỉ cần một trang bị lộ là toàn bộ tài khoản khác 'mất trắng'. Dấu hiệu nhận biết: mọi lời khuyên 'dùng chung một mật khẩu cho tiện' đều mâu thuẫn với nguyên tắc bảo mật cơ bản; nếu sợ quên, hãy dùng trình quản lí mật khẩu thay vì trùng lặp mật khẩu giữa các tài khoản."
 },
 {
  "id": "g3-14",
  "mach": "C",
  "unesco": "C2",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Yến được giao viết đoạn văn về ứng dụng AI trong đời sống và hỏi trợ lí ảo gợi ý ba ví dụ cụ thể để đưa vào bài.",
  "claims": [
   "Hệ thống gợi ý bài hát hay video mà em có thể thích, dựa trên lịch sử nghe và xem trước đó, là một ứng dụng AI rất quen thuộc.",
   "Trong y tế, AI hỗ trợ bác sĩ phân tích ảnh chụp để phát hiện bệnh sớm hơn, giúp việc chẩn đoán nhanh hơn.",
   "Ứng dụng dịch tự động ngày nay cũng dùng AI để dịch nhanh tài liệu — tuy vậy trước khi nộp bài, em vẫn nên tự đọc lại bản dịch vì đôi chỗ chưa tự nhiên."
  ],
  "giaiThich": "Cả ba câu đều đúng: gợi ý nội dung, hỗ trợ phân tích y tế và dịch tự động là những ứng dụng AI có thật trong đời sống, và câu cuối còn đúng khi nhắc em tự rà soát lại bản dịch. Câu trả lời không có số liệu bịa, nguồn không tồn tại hay suy luận vội vàng — em có thể yên tâm dùng làm ý tưởng cho bài viết."
 },
 {
  "id": "g4-01",
  "mach": "C",
  "unesco": "C1",
  "loai": "co_loi",
  "loaiLoi": "so_lieu_bia",
  "claimLoi": 1,
  "boiCanh": "Minh hỏi trợ lý AI xem có nên dùng công cụ dịch máy để viết bài luận tiếng Anh nộp cho cô giáo hay không.",
  "claims": [
   "Dịch máy hiện nay đã tiến bộ hơn trước rất nhiều: các hệ thống có thể hiểu ngữ cảnh và tạo ra câu văn mượt mà, tự nhiên hơn.",
   "Theo nghiên cứu quốc tế, độ chính xác của dịch máy hiện đại đã đạt mức 99,27% với cặp ngôn ngữ Việt - Anh, nên bạn hoàn toàn có thể nộp bài luận dịch máy mà không cần đọc lại.",
   "Tuy vậy, bạn chỉ nên dùng dịch máy để tham khảo: hãy đọc lại, tra từ điển và tự viết theo cách của mình để thật sự giỏi tiếng Anh hơn."
  ],
  "giaiThich": "Con số 99,27% nghe rất 'khoa học' nhưng không có nghiên cứu nào công bố độ chính xác như vậy cho dịch Việt - Anh; đây là số liệu bịa. Dấu hiệu nhận biết: con số lẻ chính xác đến từng chữ số thập phân nhưng nguồn chỉ nói chung chung là 'nghiên cứu quốc tế'. Hai câu còn lại đúng: dịch máy có tiến bộ thật nhưng chỉ nên dùng để tham khảo."
 },
 {
  "id": "g4-02",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "so_lieu_bia",
  "claimLoi": 1,
  "boiCanh": "Lan muốn nhờ trợ lý AI tư vấn lập thời gian biểu cân bằng giữa việc học và lướt mạng xã hội.",
  "claims": [
   "Sử dụng mạng xã hội vừa phải, có nghỉ giải lao giữa các phiên giúp bạn bớt căng thẳng và giữ thời gian học tập trung hơn.",
   "Nghiên cứu đã chứng minh thanh thiếu niên dùng mạng xã hội đúng 47 phút mỗi ngày có trí nhớ bài học tốt hơn 34,6% so với người hoàn toàn không dùng.",
   "Nếu bạn thấy mình thức khuya lướt bảng tin hay mệt mỏi vào hôm sau, hãy điều chỉnh thời gian dùng và đặt giới hạn cụ thể trên điện thoại."
  ],
  "giaiThich": "Các con số 'đúng 47 phút' và '34,6%' là số liệu bịa đặt: không có nghiên cứu thực tế nào chỉ ra một mốc thời gian 'thần kỳ' cụ thể như vậy, và bằng chứng khoa học về mạng xã hội với trí nhớ vốn rất phức tạp, chưa thể kết luận gọn như thế. Dấu hiệu: con số quá lẻ, quá chính xác nhưng không nêu tên nghiên cứu hay tổ chức nào để kiểm chứng. Hai lời khuyên còn lại đều hợp lý và đúng đắn."
 },
 {
  "id": "g4-03",
  "mach": "A",
  "unesco": "A2",
  "loai": "co_loi",
  "loaiLoi": "nguon_khong_ton_tai",
  "claimLoi": 1,
  "boiCanh": "Hưng lớp 12 hỏi trợ lý AI về cách chọn ngành nghề phù hợp trong thời đại trí tuệ nhân tạo.",
  "claims": [
   "Chọn nghề thời AI không chỉ cần kiến thức chuyên môn mà còn cần kỹ năng mềm như tự học, hợp tác và tư duy phản biện.",
   "Theo 'Báo cáo Thanh niên Số Châu Á 2026' do Viện Tương lai Giáo dục (IFE) công bố, 8/10 công việc trong thập kỷ tới sẽ yêu cầu kỹ năng AI.",
   "Bạn nên thử sức qua các dự án nhỏ, hoạt động tình nguyện hoặc câu lạc bộ Tin học để hiểu rõ điểm mạnh của mình trước khi quyết định."
  ],
  "giaiThich": "'Viện Tương lai Giáo dục (IFE)' và 'Báo cáo Thanh niên Số Châu Á 2026' là nguồn bịa đặt, không thể tìm thấy trên Internet hay trong bất kỳ danh mục thư viện nào. Nguồn bịa thường nghe rất thật vì có tên tổ chức, năm xuất bản và số liệu cụ thể, nên học sinh cần tập thói quen tra cứu tên tổ chức và ấn phẩm trước khi trích dẫn. Hai câu còn lại là lời khuyên hướng nghiệp đúng đắn."
 },
 {
  "id": "g4-04",
  "mach": "D",
  "unesco": "D2",
  "loai": "co_loi",
  "loaiLoi": "nguon_khong_ton_tai",
  "claimLoi": 1,
  "boiCanh": "Nhóm Tin học của trường được giao nhiệm vụ thiết kế một chatbot trả lời câu hỏi về thư viện trường.",
  "claims": [
   "Trước khi viết mã, nhóm nên xác định rõ người dùng của bot là ai, những câu hỏi nào thường gặp nhất và cách xử lý khi bot không biết câu trả lời.",
   "Hãy thiết kế theo 'khung hội thoại 6 tầng' trong sách 'Nền tảng thiết kế chatbot giáo dục' của giáo sư Hoàng Minh Khang, NXB Kim La Bàn 2024, đây là tài liệu bắt buộc phải đọc khi làm lĩnh vực này.",
   "Sau khi hoàn thành, hãy thử nghiệm bot với nhiều loại câu hỏi khác nhau từ các bạn trong lớp và ghi nhận các trường hợp sai để cải thiện dần."
  ],
  "giaiThich": "Cuốn sách, tác giả và nhà xuất bản được nêu đều không tồn tại; tìm kiếm tên sách hoặc NXB Kim La Bàn sẽ không cho kết quả nào. Trong thiết kế hệ thống, trích dẫn bịa đặc biệt nguy hiểm vì khiến học sinh mất thời gian đi tìm 'khung chuẩn' không có thật thay vì làm theo quy trình đúng. Hai câu còn lại mô tả đúng các bước thiết kế và kiểm thử một chatbot."
 },
 {
  "id": "g4-05",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "thien_kien",
  "claimLoi": 1,
  "boiCanh": "Lớp 11A bầu nhóm trưởng cho dự án Tin học học kỳ, một bạn nhờ trợ lý AI tư vấn cách chọn người.",
  "claims": [
   "Một nhóm trưởng tốt cần biết phân công nhiệm vụ rõ ràng, lắng nghe các thành viên và chịu trách nhiệm về tiến độ chung của nhóm.",
   "Bạn nên chọn một bạn nam làm nhóm trưởng vì con trai bẩm sinh tư duy logic và hợp với công nghệ hơn; các bạn nữ thì nên giao việc soạn thuyết trình và trang trí slide cho phù hợp.",
   "Hãy bầu chọn dựa trên năng lực thực tế, kinh nghiệm làm việc nhóm và tinh thần trách nhiệm của từng bạn, không phân biệt đặc điểm cá nhân nào."
  ],
  "giaiThich": "Câu thứ hai chứa định kiến giới: gán mặc nhiên 'con trai thì logic, hợp công nghệ' và 'con gái thì chỉ hợp trang trí' cho cả một nhóm người dựa trên giới tính, trong khi khả năng lãnh đạo và tư duy logic không phụ thuộc vào giới. Dấu hiệu nhận biết: những cụm như 'bẩm sinh', 'con trai thì... con gái thì...' áp đặc điểm cố định cho cả giới. Hai câu còn lại đều đúng và công bằng."
 },
 {
  "id": "g4-06",
  "mach": "A",
  "unesco": "A1",
  "loai": "co_loi",
  "loaiLoi": "thien_kien",
  "claimLoi": 1,
  "boiCanh": "Một trường THPT ở huyện miền núi muốn đưa ứng dụng học tập AI vào sử dụng và hỏi trợ lý AI cách triển khai.",
  "claims": [
   "Khi thiết kế ứng dụng học tập, cần tính đến điều kiện thực tế của người dùng như chất lượng thiết bị, đường truyền Internet và thời gian học tập.",
   "Học sinh miền núi thường chậm tiếp thu và kém tư duy hơn nên không cần đầu tư giao diện hay tính năng cho nhóm này; ứng dụng chỉ nên tập trung phục vụ học sinh thành phố là đủ.",
   "Ứng dụng nên hỗ trợ chế độ tiết kiệm dữ liệu, giao diện đơn giản rõ ràng và có học liệu tải về dùng ngoại tuyến để nhiều nhóm học sinh đều dùng được."
  ],
  "giaiThich": "Câu thứ hai là định kiến vùng miền: đánh giá thấp năng lực của cả một cộng đồng học sinh chỉ vì nơi các bạn sinh sống, điều này vô căn cứ và gây tổn thương. Thiết kế lấy con người làm trung tâm thì ngược lại, phải bắt đầu từ nhu cầu của chính những nhóm thiệt thòi nhất. Dấu hiệu: nhận xét tiêu cực khái quát về 'người vùng nào đó' thay vì nói về điều kiện khách quan như thiết bị, đường truyền."
 },
 {
  "id": "g4-07",
  "mach": "C",
  "unesco": "C2",
  "loai": "co_loi",
  "loaiLoi": "suy_luan_sai",
  "claimLoi": 1,
  "boiCanh": "Khoa hay dùng trợ lý AI để học Vật lý và tò mò hỏi liệu dùng AI có thực sự giúp bạn học giỏi lên không.",
  "claims": [
   "AI có thể giải thích các hiện tượng vật lý bằng ví dụ sinh động và hướng dẫn giải bài tập từng bước, giúp bạn hiểu bài từ nhiều góc độ.",
   "Một khảo sát cho thấy những học sinh chăm đặt câu hỏi cho AI có điểm trung bình cao hơn hẳn; vì vậy cứ đặt càng nhiều câu hỏi cho AI thì điểm số của bạn sẽ tự động càng cao.",
   "Để học hiệu quả với AI, bạn nên nhờ AI giảng bài rồi tự đóng máy lại và tự làm lại bài tập để kiểm tra xem mình đã thật sự hiểu chưa."
  ],
  "giaiThich": "Câu thứ hai mắc lỗi 'tương quan không phải nhân quả': học sinh chăm chỉ, ham học vốn hay đặt câu hỏi (cho thầy cô lẫn AI) và cũng chính vì chăm học nên điểm cao; tần suất hỏi AI không phải nguyên nhân trực tiếp làm tăng điểm. Dấu hiệu: kết luận kiểu 'cứ làm X nhiều thì tự động được Y' chỉ dựa trên quan sát hai thứ đi kèm nhau. Hai câu còn lại mô tả đúng lợi ích và cách dùng AI hiệu quả."
 },
 {
  "id": "g4-08",
  "mach": "D",
  "unesco": "D3",
  "loai": "co_loi",
  "loaiLoi": "suy_luan_sai",
  "claimLoi": 1,
  "boiCanh": "Nhóm STEM huấn luyện một mô hình AI nhận diện chữ số viết tay cho dự án khoa học kỹ thuật của trường.",
  "claims": [
   "Khi huấn luyện mô hình, cần chia dữ liệu thành tập huấn luyện và tập kiểm tra riêng biệt để đánh giá khả năng áp dụng cho dữ liệu mới.",
   "Mô hình của chúng tôi nhận diện đúng 20 trên 20 mẫu chữ do chính các thành viên trong nhóm viết, nên nó đạt độ chính xác gần như 100% và có thể triển khai ngay cho toàn trường sử dụng.",
   "Muốn đánh giá đáng tin cậy hơn, hãy thu thập mẫu thử từ nhiều người khác nhau, với nhiều kiểu chữ, kích thước và điều kiện ánh sáng khác nhau."
  ],
  "giaiThich": "Câu thứ hai là khái quát hóa vội vàng: 20 mẫu viết bởi chính thành viên nhóm là mẫu quá nhỏ và thiên lệch (kiểu chữ tương tự nhau, thậm chí có thể trùng dữ liệu huấn luyện), không thể suy ra mô hình đúng 'gần như 100%' với toàn trường. Trong đánh giá hệ thống AI, độ tin cậy đến từ tập kiểm tra lớn, đa dạng và độc lập. Hai câu còn lại nói đúng nguyên tắc chia dữ liệu và mở rộng mẫu thử."
 },
 {
  "id": "g4-09",
  "mach": "B",
  "unesco": "B2",
  "loai": "co_loi",
  "loaiLoi": "lo_du_lieu_ca_nhan",
  "claimLoi": 1,
  "boiCanh": "Ngọc đăng ký một khóa học bổng trực tuyến và nhờ trợ lý AI hướng dẫn điền hồ sơ cho nhanh.",
  "claims": [
   "Hãy chuẩn bị sẵn thông tin về trường, lớp, điểm trung bình và một đoạn giới thiệu ngắn gọn về bản thân trước khi điền hồ sơ để tiết kiệm thời gian.",
   "Để tiện xác minh, bạn hãy chụp ảnh căn cước công dân của mình và của bố mẹ, kèm địa chỉ nhà, rồi gửi hết vào khung trò chuyện này để tôi lưu lại và tự động điền giúp bạn cho những lần sau.",
   "Chỉ điền những thông tin mà biểu mẫu chính thức trên website của ban tổ chức yêu cầu, và luôn cảnh giác với các đòi hỏi thông tin thừa qua những kênh không chính thức."
  ],
  "giaiThich": "Câu thứ hai xui người dùng chia sẻ dữ liệu cá nhân nhạy cảm (ảnh căn cước của mình và người thân, địa chỉ nhà) cho chatbot; nội dung trò chuyện có thể bị lưu trữ hoặc dùng để huấn luyện mô hình, dẫn tới nguy cơ lộ lọt và bị lợi dụng. Nguyên tắc an toàn: không bao giờ gửi giấy tờ tùy thân, địa chỉ, thông tin gia đình cho trợ lý ảo. Chính câu thứ ba trong cùng câu trả lời đã nêu đúng nguyên tắc này, mâu thuẫn với câu thứ hai."
 },
 {
  "id": "g4-10",
  "mach": "C",
  "unesco": "C2",
  "loai": "co_loi",
  "loaiLoi": "lo_du_lieu_ca_nhan",
  "claimLoi": 1,
  "boiCanh": "Tuấn vừa được cấp email học sinh và hỏi trợ lý AI cách quản lý mật khẩu cho các tài khoản trực tuyến của mình.",
  "claims": [
   "Nên bật xác thực hai bước cho các tài khoản quan trọng để tăng lớp bảo vệ, ngay cả khi chẳng may mật khẩu bị lộ.",
   "Để tiện lợi và khỏi quên, bạn hãy đặt một mật khẩu thật mạnh rồi dùng chung cho tất cả tài khoản: email học sinh, mạng xã hội và ngân hàng, như vậy chỉ cần nhớ đúng một mật khẩu là xong.",
   "Bạn có thể dùng ứng dụng quản lý mật khẩu để tạo và lưu các mật khẩu ngẫu nhiên, khác nhau cho từng dịch vụ một cách an toàn."
  ],
  "giaiThich": "Câu thứ hai đưa lời khuyên nguy hiểm: dùng lại một mật khẩu cho mọi tài khoản, vì khi bất kỳ dịch vụ nào bị rò rỉ dữ liệu, kẻ xấu có thể dùng đúng cặp mật khẩu đó chiếm đoạt toàn bộ các tài khoản còn lại theo hiệu ứng domino. Cách đúng nằm ở câu thứ ba: mỗi dịch vụ một mật khẩu riêng, được quản lý bằng ứng dụng chuyên dụng, kết hợp xác thực hai bước như câu thứ nhất."
 },
 {
  "id": "g4-11",
  "mach": "A",
  "unesco": "A1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Mai cảm thấy lo âu trước kỳ thi cuối kỳ và tâm sự với trợ lý ảo để tìm cách giải tỏa.",
  "claims": [
   "Cảm giác áp lực trước kỳ thi là điều rất bình thường, nhiều học sinh cũng trải qua, và nó cho thấy bạn thực sự quan tâm đến việc học của mình.",
   "Mình có thể lắng nghe và gợi ý vài cách giảm căng thẳng như hít thở sâu, chia lịch ôn tập thành những phần nhỏ, nhưng mình không thể thay thế bác sĩ hay chuyên viên tâm lý được đâu.",
   "Nếu lo âu kéo dài, ảnh hưởng đến giấc ngủ và sinh hoạt, bạn hãy chia sẻ với người lớn tin cậy như bố mẹ, thầy cô giáo hoặc chuyên viên tâm lý học đường của trường nhé."
  ],
  "giaiThich": "Cả ba câu đều đúng: câu đầu đồng cảm và chuẩn hóa cảm xúc một cách lành mạnh, câu thứ hai nêu đúng giới hạn của AI (không thay thế được chuyên gia y tế, tâm lý), câu thứ ba hướng người dùng đến kênh hỗ trợ thực sự khi vấn đề vượt quá khả năng của trợ lý ảo. Đây là ví dụ về AI lấy con người làm trung tâm: trung thực về năng lực và đặt sức khỏe tinh thần của người dùng lên trước."
 },
 {
  "id": "g4-12",
  "mach": "C",
  "unesco": "C1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Trong giờ Tin học, thầy giáo yêu cầu các nhóm tìm hiểu cách một chatbot tạo ra câu trả lời để thuyết trình trước lớp.",
  "claims": [
   "Mô hình ngôn ngữ lớn tạo ra câu trả lời bằng cách dự đoán từ tiếp theo có khả năng xuất hiện cao nhất, dựa trên các mẫu văn bản đã học từ lượng dữ liệu khổng lồ.",
   "Vì mô hình chỉ dự đoán từ nghe 'hợp lý' chứ không tra cứu sự thật, nó đôi khi tạo ra câu trả lời trôi chảy nhưng sai thông tin, hiện tượng này thường được gọi là 'ảo giác' của AI.",
   "Do đó khi dùng chatbot để tìm tư liệu làm bài tập, bạn nên kiểm chứng các thông tin và số liệu quan trọng bằng sách giáo khoa hoặc các nguồn chính thống."
  ],
  "giaiThich": "Ba câu đều chính xác về mặt khoa học và nối kết logic với nhau: câu đầu mô tả đúng nguyên lý dự đoán từ kế tiếp của mô hình ngôn ngữ lớn, câu thứ hai giải thích đúng lý do phát sinh hiện tượng 'ảo giác', và câu thứ ba rút ra cách ứng xử hợp lý là kiểm chứng thông tin. Hiểu đúng nguyên lý hoạt động giúp học sinh không tin AI một cách mù quáng mà biết dùng nó như công cụ hỗ trợ có phê phán."
 },
 {
  "id": "g4-13",
  "mach": "D",
  "unesco": "D2",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Tập thể lớp 10B muốn xây dựng một bot 'lớp phó học tập ảo' chuyên nhắc bài tập về nhà trong nhóm chat của lớp.",
  "claims": [
   "Bước đầu tiên là liệt kê các việc bot cần làm, như nhắc bài tập về nhà, thông báo lịch kiểm tra, thông báo hoạt động của lớp, rồi chọn ra tính năng cần thiết nhất để làm trước.",
   "Hãy xây dựng dữ liệu nhắc việc từ thời khóa biểu và sổ đầu bài chính thức của lớp, đồng thời quy ước bot luôn trả lời 'mình chưa có thông tin này' khi gặp câu hỏi ngoài dữ liệu.",
   "Sau đó chạy thử bot với một nhóm nhỏ trong khoảng một tuần, thu thập góp ý của các thành viên, sửa lỗi rồi mới mở rộng cho cả lớp cùng sử dụng."
  ],
  "giaiThich": "Cả ba câu đều đúng và phản ánh đủ quy trình thiết kế hệ thống AI: xác định nhu cầu và ưu tiên tính năng, xây dựng dữ liệu đầu vào kèm cơ chế xử lý an toàn khi thiếu thông tin (không bịa câu trả lời), rồi thử nghiệm ở phạm vi hẹp trước khi triển khai rộng. Cách làm này giúp sản phẩm sát nhu cầu người dùng thật và hạn chế rủi ro khi vận hành."
 },
 {
  "id": "g4-14",
  "mach": "B",
  "unesco": "B1",
  "loai": "dung",
  "loaiLoi": null,
  "claimLoi": -1,
  "boiCanh": "Phương dùng trợ lý AI để gợi ý dàn ý cho bài văn nghị luận và muốn biết cách sử dụng AI thế nào cho đúng quy tắc học tập.",
  "claims": [
   "Bạn có thể dùng AI để gợi ý dàn ý và tìm ý tưởng, nhưng phần viết bài cần được diễn đạt bằng lời văn của chính bạn cùng những suy nghĩ, lập luận riêng của bạn.",
   "Khi mượn ý tưởng, dữ liệu hay câu trích từ bất kỳ nguồn nào, kể cả AI, việc ghi chú và trích dẫn nguồn trung thực là biểu hiện của liêm chính học tập.",
   "Trước khi đưa thông tin do AI cung cấp vào bài viết, hãy đối chiếu lại với sách giáo khoa và nguồn chính thống, vì AI có thể đưa ra thông tin chưa chính xác."
  ],
  "giaiThich": "Cả ba câu đều đúng và nhất quán với các chuẩn mực đạo đức học đường: không nộp bài do AI viết hộ, tôn trọng và trích dẫn nguồn ý tưởng, kiểm chứng thông tin trước khi sử dụng. Đây là những nguyên tắc cốt lõi của việc dùng AI một cách trung thực và có trách nhiệm trong học tập, đồng thời vẫn tận dụng được điểm mạnh gợi ý ý tưởng của công cụ."
 }
];
