/* SOI AI — tinhhuong.js : TRẠM "TÌNH HUỐNG" — phủ 5 yêu cầu cần đạt còn trống.
 *
 * Trước khi có tệp này, độ phủ 22 YCCĐ lớp 10 (đo bằng tools/tinh_do_phu.py trên
 * bằng chứng thật trong code) là: 8 PHỦ MẠNH · 9 PHỦ · 5 CHƯA PHỦ. Năm yêu cầu trống:
 *   10.A2.1    Nêu được một số rủi ro đối với con người, xã hội mà một sản phẩm AI
 *              có thể đem lại.
 *   10.A2.MR1  Nêu được một số biện pháp hạn chế các rủi ro ... thông qua một dự án
 *              sáng tạo AI.
 *   10.B2.1    Nêu được ví dụ về hành vi sử dụng AI hoặc sự cố liên quan đến AI vi phạm
 *              quy định của nhà trường hoặc các văn bản pháp luật liên quan.
 *   10.C2.MR1  Xác định được các yêu cầu cần có đối với việc ứng dụng AI thực hiện
 *              nhiệm vụ cụ thể.
 *   10.C3.MR1  Trình bày được ví dụ mô tả một số công nghệ để thiết kế và tạo AI.
 *
 * Tất cả năm yêu cầu đều là dạng "nêu được / trình bày được / xác định được", tức là
 * có thể đo bằng tình huống nhiều lựa chọn có nhãn đúng cố định. Vì nhãn do chính hệ
 * đặt ra nên việc chấm là phép so sánh tất định — giữ đúng nguyên tắc oracle của toàn
 * bộ sản phẩm, không cần giáo viên và không cần người kiểm chứng bên ngoài.
 *
 * RÀNG BUỘC ĐÃ TUÂN THỦ:
 *   Khung 2422 phần VI: "không xác lập đầu điểm riêng cho nội dung giáo dục AI".
 *   Vì vậy tệp này KHÔNG có biến nào tên là diem/diemSo, và mọi nhãn phản hồi chỉ dùng
 *   "đáp ứng" / "chưa đáp ứng". Kết quả ghi vào nhật ký dưới dạng số lần đáp ứng để
 *   giáo viên tổng hợp minh chứng, không phải để xếp loại học sinh.
 *
 * AN TOÀN: nội dung câu hỏi là HẰNG SỐ trong tệp này; phần động duy nhất đưa ra màn
 *   hình là chữ cái phương án và chuỗi đã qua esc(). Không có innerHTML với dữ liệu
 *   người dùng trong tệp này (giao diện dựng bằng createElement + textContent).
 */
(function(){
  "use strict";

  function esc(s){
    return String(s == null ? "" : s).replace(/[&<>"]/g, c =>
      ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));
  }

  /* ====================== NHÓM 1 — RỦI RO CỦA SẢN PHẨM AI (10.A2.1, 10.A2.MR1) ===== */
  const NHOM_RUI_RO = [
    { id:"rr-01", yccd:"10.A2.1", chuDe:"A2", mach:"A",
      tinhHuong:"Một bệnh viện dùng hệ AI đọc ảnh X-quang để sàng lọc. Hệ được huấn luyện hoàn toàn bằng ảnh chụp của người trưởng thành, sau đó được áp dụng cho cả khoa nhi.",
      cauHoi:"Rủi ro đối với con người mà sản phẩm AI này có thể đem lại là gì?",
      luaChon:[
        {id:"a", text:"Không có rủi ro, vì ảnh X-quang thì trẻ em hay người lớn đều như nhau."},
        {id:"b", text:"Trẻ em có thể bị bỏ sót bệnh hoặc bị chẩn đoán sai một cách có hệ thống, vì hệ chưa từng học đặc điểm ảnh của trẻ em; người bị thiệt lại là nhóm không có tiếng nói trong quyết định triển khai."},
        {id:"c", text:"Rủi ro duy nhất là bệnh viện tốn thêm tiền bảo trì."},
        {id:"d", text:"Rủi ro là bác sĩ sẽ thất nghiệp ngay lập tức."}],
      dapAn:"b",
      giaiThich:"Đây là rủi ro về công bằng: hệ hoạt động kém với đúng nhóm yếu thế nhất, và lỗi lặp lại có hệ thống chứ không ngẫu nhiên. Rủi ro không nằm ở việc máy hỏng mà ở việc máy vẫn chạy trơn tru trong khi cho kết quả sai với một nhóm người.",
      bienPhap:"Yêu cầu nhà cung cấp công bố dữ liệu huấn luyện theo nhóm tuổi; kiểm tra độ chính xác tách riêng cho trẻ em TRƯỚC khi triển khai; giữ bác sĩ là người quyết định cuối cùng."},

    { id:"rr-02", yccd:"10.A2.1", chuDe:"A2", mach:"A",
      tinhHuong:"Một trường học lắp hệ AI nhận diện khuôn mặt để điểm danh tự động và chấm điểm chuyên cần.",
      cauHoi:"Rủi ro đối với xã hội của sản phẩm này là gì?",
      luaChon:[
        {id:"a", text:"Điểm danh nhanh hơn nên học sinh có nhiều thời gian học hơn."},
        {id:"b", text:"Dữ liệu khuôn mặt của trẻ vị thành niên bị thu thập và lưu trữ lâu dài; một khi lộ thì không thể 'đổi khuôn mặt' như đổi mật khẩu, và học sinh không có khả năng từ chối."},
        {id:"c", text:"Máy ảnh có thể bị hỏng do thời tiết."},
        {id:"d", text:"Không có rủi ro vì trường là nơi an toàn."}],
      dapAn:"b",
      giaiThich:"Rủi ro xã hội ở đây là sự mất cân xứng quyền lực: người bị thu thập dữ liệu không phải người quyết định. Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 đặt dữ liệu trẻ em dưới sự bảo vệ chặt hơn và cần sự đồng ý của cha mẹ hoặc người giám hộ.",
      bienPhap:"Chỉ dùng mã ẩn danh thay cho dữ liệu sinh trắc học; nếu buộc phải dùng thì có văn bản đồng ý của cha mẹ, công bố thời hạn lưu và cách xoá; luôn có phương án điểm danh thủ công."},

    { id:"rr-03", yccd:"10.A2.MR1", chuDe:"A2", mach:"A",
      tinhHuong:"Nhóm em được giao làm một dự án sáng tạo: ứng dụng AI gợi ý ngành học cho học sinh lớp 12 dựa trên bài trắc nghiệm sở thích.",
      cauHoi:"Biện pháp hạn chế rủi ro nào là QUAN TRỌNG NHẤT và phải làm ngay từ lúc thiết kế?",
      luaChon:[
        {id:"a", text:"Làm giao diện thật đẹp để học sinh tin tưởng kết quả."},
        {id:"b", text:"Công bố rõ dữ liệu dùng để huấn luyện, cho học sinh xem vì sao hệ đưa ra gợi ý đó, và ghi rõ đây chỉ là gợi ý để tham khảo chứ không phải quyết định thay con người."},
        {id:"c", text:"Chạy thật nhiều vòng huấn luyện để độ chính xác cao nhất có thể."},
        {id:"d", text:"Không cho học sinh biết đây là hệ AI để tránh lo lắng."}],
      dapAn:"b",
      giaiThich:"Minh bạch là biện pháp hạn chế rủi ro hiệu quả nhất vì nó trao lại quyền kiểm soát cho người dùng: họ biết hệ dựa vào đâu, và biết mình vẫn là người quyết định. Phương án (d) là che giấu, làm rủi ro tăng lên chứ không giảm. Độ chính xác cao (c) không thay thế được minh bạch — một hệ rất chính xác nhưng không giải thích được vẫn gây hại khi nó sai.",
      bienPhap:"Ghi trong sản phẩm: nguồn dữ liệu, cách hệ suy ra gợi ý, phạm vi áp dụng, và nút để người dùng tự quyết định khác với gợi ý."},

    { id:"rr-04", yccd:"10.A2.MR1", chuDe:"A2", mach:"A",
      tinhHuong:"Dự án của nhóm em dùng AI dự báo sâu bệnh cho ruộng lúa ở địa phương. Dữ liệu thu được chỉ từ các ruộng gần đường lớn, còn ruộng ở vùng sâu thì không có.",
      cauHoi:"Nhóm nên làm gì để hạn chế rủi ro cho chính người cần sản phẩm nhất?",
      luaChon:[
        {id:"a", text:"Ghi chú nhỏ trong tài liệu là dữ liệu chưa đầy đủ, còn sản phẩm vẫn phát hành rộng rãi như cũ."},
        {id:"b", text:"Công bố rõ phạm vi áp dụng, bổ sung dữ liệu từ vùng sâu trước khi mở rộng, và trong lúc chưa đủ dữ liệu thì khuyến cáo người dùng vùng đó kiểm tra lại bằng cán bộ khuyến nông."},
        {id:"c", text:"Bỏ hẳn vùng sâu khỏi kế hoạch vì thu thập dữ liệu ở đó tốn công."},
        {id:"d", text:"Tăng số vòng huấn luyện để mô hình tự suy ra đặc điểm vùng sâu."}],
      dapAn:"b",
      giaiThich:"Mô hình không thể tự suy ra đặc điểm của nhóm mà nó chưa từng thấy dữ liệu, nên (d) vô ích. (c) là loại trừ chính nhóm cần được phục vụ nhất. (a) là hình thức của minh bạch nhưng không bảo vệ ai cả. Biện pháp đúng gồm ba phần: nói rõ phạm vi, sửa dữ liệu, và có người thật làm chỗ dựa trong lúc chưa sửa xong.",
      bienPhap:"Ghi phạm vi áp dụng ngay trên màn hình kết quả; lập kế hoạch thu dữ liệu vùng sâu; nêu rõ kênh kiểm chứng thay thế."}
  ];

  /* ====================== NHÓM 2 — VI PHẠM QUY ĐỊNH, PHÁP LUẬT (10.B2.1) ========= */
  const NHOM_VI_PHAM = [
    { id:"vp-01", yccd:"10.B2.1", chuDe:"B2", mach:"B",
      tinhHuong:"Trong giờ kiểm tra 15 phút, một học sinh dùng điện thoại ẩn dưới ngăn bàn để hỏi AI lời giải rồi chép lại nguyên văn, không ghi chú rằng mình đã dùng AI.",
      cauHoi:"Hành vi này vi phạm điều gì?",
      luaChon:[
        {id:"a", text:"Không vi phạm gì, vì AI cũng là một nguồn tài liệu học tập."},
        {id:"b", text:"Vi phạm nội quy kiểm tra của nhà trường (dùng thiết bị không được phép và không trung thực trong kiểm tra), đồng thời vi phạm nguyên tắc khai báo sử dụng AI."},
        {id:"c", text:"Chỉ vi phạm nếu bị giám thị phát hiện."},
        {id:"d", text:"Vi phạm Luật Trí tuệ nhân tạo vì học sinh chưa đủ tuổi dùng AI."}],
      dapAn:"b",
      giaiThich:"Hành vi này có hai lớp vi phạm: lớp thứ nhất là nội quy nhà trường về kiểm tra; lớp thứ hai là nguyên tắc trung thực học thuật — Khung 2422 yêu cầu học sinh nêu được công cụ, mục đích và phạm vi AI hỗ trợ cùng phần việc do chính mình thực hiện. Phương án (c) sai vì vi phạm không phụ thuộc vào việc có bị phát hiện hay không. Không có quy định nào cấm học sinh dùng AI theo độ tuổi, nên (d) sai.",
      bienPhap:""},

    { id:"vp-02", yccd:"10.B2.1", chuDe:"B2", mach:"B",
      tinhHuong:"Một học sinh dán bảng điểm của cả lớp (có họ tên đầy đủ, ngày sinh và ghi chú về hoàn cảnh gia đình) vào một công cụ AI miễn phí trên mạng để nhờ tổng hợp, mà không xin phép ai.",
      cauHoi:"Hành vi này vi phạm điều gì?",
      luaChon:[
        {id:"a", text:"Không vi phạm, vì công cụ đó miễn phí và học sinh chỉ muốn làm việc tốt cho lớp."},
        {id:"b", text:"Vi phạm quy định về bảo vệ dữ liệu cá nhân: dữ liệu của trẻ em là dữ liệu nhạy cảm, cần sự đồng ý của cha mẹ hoặc người giám hộ, và học sinh không có quyền đưa dữ liệu của các bạn cho bên thứ ba."},
        {id:"c", text:"Chỉ vi phạm nếu công cụ đó bán dữ liệu cho người khác."},
        {id:"d", text:"Vi phạm nội quy vì dùng điện thoại trong giờ học."}],
      dapAn:"b",
      giaiThich:"Đây là tình huống phổ biến nhất và nguy hiểm nhất vì người làm có thiện ý. Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 (có hiệu lực từ 1/1/2026) bảo vệ dữ liệu trẻ em và yêu cầu sự đồng ý của cha mẹ hoặc người giám hộ. Việc đưa dữ liệu lên công cụ trực tuyến còn có nghĩa là dữ liệu đã rời khỏi tầm kiểm soát của nhà trường, không lấy lại được.",
      bienPhap:""},

    { id:"vp-03", yccd:"10.B2.1", chuDe:"B2", mach:"B",
      tinhHuong:"Một học sinh dùng AI tạo ảnh giả ghép mặt bạn cùng lớp vào một tình huống phản cảm rồi gửi trong nhóm chat của lớp để 'đùa cho vui'.",
      cauHoi:"Hành vi này vi phạm những gì?",
      luaChon:[
        {id:"a", text:"Chỉ là trò đùa trong lớp nên không vi phạm gì."},
        {id:"b", text:"Vi phạm nội quy nhà trường về bạo lực học đường trên không gian mạng, xâm phạm danh dự và hình ảnh cá nhân của bạn, và có thể bị xử lí theo quy định pháp luật về an ninh mạng."},
        {id:"c", text:"Vi phạm bản quyền vì AI đã dùng ảnh có sẵn trên mạng."},
        {id:"d", text:"Không vi phạm vì ảnh là do AI tạo ra, không phải ảnh thật."}],
      dapAn:"b",
      giaiThich:"Việc ảnh do AI tạo ra không làm giảm hậu quả với người bị ghép mặt — thiệt hại về danh dự và tâm lí là thật. Luật An ninh mạng 24/2018/QH14 (được sửa đổi, bổ sung bởi 116/2025/QH15) điều chỉnh hành vi trên không gian mạng. Phương án (d) là ngụy biện phổ biến nhất: công cụ tạo ra sản phẩm không làm người sử dụng thoát trách nhiệm.",
      bienPhap:""},

    { id:"vp-04", yccd:"10.B2.1", chuDe:"B2", mach:"B",
      tinhHuong:"Một học sinh nộp bài tập làm văn do AI viết hoàn toàn, đứng tên mình, và không khai báo đã dùng AI.",
      cauHoi:"Vấn đề cốt lõi của hành vi này là gì?",
      luaChon:[
        {id:"a", text:"Bài văn có thể bị sai chính tả nên chất lượng không đảm bảo."},
        {id:"b", text:"Đây là gian lận trong học tập: người học khai báo sai về tác giả của sản phẩm, làm mất ý nghĩa của việc đánh giá năng lực và khiến giáo viên nhận được minh chứng giả về sự tiến bộ."},
        {id:"c", text:"Không có vấn đề gì vì AI viết hay hơn học sinh thì nên dùng."},
        {id:"d", text:"Chỉ vi phạm nếu giáo viên phát hiện ra."}],
      dapAn:"b",
      giaiThich:"Vấn đề cốt lõi không nằm ở chất lượng bài văn mà ở tính trung thực của minh chứng. Đánh giá trong giáo dục dựa trên giả định rằng sản phẩm phản ánh năng lực của người nộp; khi giả định đó bị phá vỡ thì mọi kết quả đánh giá đều vô nghĩa. Đây cũng là lí do sản phẩm SOI AI có phiếu khai báo sử dụng AI: khai báo không phải để trừ điểm mà để minh chứng còn giá trị.",
      bienPhap:""}
  ];

  /* ============ NHÓM 3 — YÊU CẦU KHI ỨNG DỤNG AI (10.C2.MR1) VÀ CÔNG NGHỆ (10.C3.MR1) ============ */
  const NHOM_YEU_CAU = [
    { id:"yc-01", yccd:"10.C2.MR1", chuDe:"C2", mach:"C",
      tinhHuong:"Nhà trường muốn ứng dụng AI để tự động phân loại thư góp ý của phụ huynh thành ba nhóm: cơ sở vật chất, chương trình học, và các vấn đề khác.",
      cauHoi:"Yêu cầu nào KHÔNG phải là điều kiện cần có để ứng dụng này chạy được?",
      luaChon:[
        {id:"a", text:"Một tập dữ liệu thư góp ý đã được phân loại sẵn để huấn luyện và kiểm tra."},
        {id:"b", text:"Tiêu chí rõ ràng để quyết định một bức thư thuộc nhóm nào, kể cả các trường hợp nằm giữa hai nhóm."},
        {id:"c", text:"Người rà soát kết quả trước khi nhà trường dùng nó để trả lời phụ huynh."},
        {id:"d", text:"Một mô hình ngôn ngữ lớn chạy trên máy chủ có card đồ họa mạnh."}],
      dapAn:"d",
      giaiThich:"Ba yêu cầu đầu là điều kiện cần cho bất kì ứng dụng phân loại nào: có dữ liệu, có tiêu chí, và có con người rà soát. Yêu cầu về phần cứng thì không: bài toán ba nhóm với văn bản ngắn có thể giải bằng mô hình đơn giản, và Khung 2422 nêu rõ việc triển khai không phụ thuộc vào phần cứng, phần mềm hay nền tảng công nghệ cụ thể.",
      bienPhap:""},

    { id:"yc-02", yccd:"10.C2.MR1", chuDe:"C2", mach:"C",
      tinhHuong:"Một nhóm học sinh muốn làm ứng dụng AI nhắc lịch tưới cây cho vườn trường.",
      cauHoi:"Trước khi viết bất kì dòng lệnh nào, nhóm cần xác định điều gì?",
      luaChon:[
        {id:"a", text:"Chọn ngôn ngữ lập trình và thư viện nào đang phổ biến nhất."},
        {id:"b", text:"Xác định nhiệm vụ cụ thể (dự báo khi nào cần tưới), dữ liệu đầu vào có thật sự thu được không (cảm biến độ ẩm hay chỉ quan sát bằng mắt), đầu ra là gì, và ai chịu trách nhiệm khi hệ báo sai."},
        {id:"c", text:"Thiết kế logo và tên ứng dụng cho hấp dẫn."},
        {id:"d", text:"Tìm mô hình AI mạnh nhất hiện nay để dùng cho chắc."}],
      dapAn:"b",
      giaiThich:"Đây chính là nội dung của yêu cầu 10.D1.1: xác định nhiệm vụ hoặc mục tiêu cụ thể và nêu mối liên hệ giữa mục tiêu đó với các thành phần chính của hệ thống. Phần lớn dự án AI của học sinh thất bại không phải vì thiếu công nghệ mà vì dữ liệu đầu vào không thu được trên thực tế.",
      bienPhap:""},

    { id:"yc-03", yccd:"10.C3.MR1", chuDe:"C3", mach:"C",
      tinhHuong:"Trong sản phẩm SOI AI, mô hình nhận diện mũ bảo hiểm được huấn luyện ngay trong trình duyệt, không cần máy chủ.",
      cauHoi:"Công nghệ nào cho phép việc đó, và cái giá phải trả là gì?",
      luaChon:[
        {id:"a", text:"Gọi API của một nhà cung cấp AI; cái giá là phải trả phí theo số lần gọi."},
        {id:"b", text:"Chạy mô hình học máy ngay trong trình duyệt bằng JavaScript và cập nhật trọng số theo lỗi; cái giá là mô hình phải đơn giản nên chỉ giải được bài toán nhỏ với đặc trưng đã tính sẵn, không xử lí được ảnh hay ngôn ngữ phức tạp."},
        {id:"c", text:"Dùng mô hình ngôn ngữ lớn đã tải sẵn; cái giá là máy phải có card đồ họa."},
        {id:"d", text:"Không có công nghệ nào làm được việc đó."}],
      dapAn:"b",
      giaiThich:"Trong SOI AI, mô hình là một perceptron bốn đặc trưng: tỉ lệ điểm ảnh rất sáng, tỉ lệ điểm ảnh sáng vừa, độ sáng vùng đầu và tỉ lệ điểm tối. Bốn đặc trưng này được tính từ ảnh vẽ bằng canvas, rồi trọng số được cập nhật ngay trong trình duyệt. Đổi lại sự đơn giản đó là hai lợi ích quyết định cho trường học: không cần mạng và học sinh nhìn thấy toàn bộ trọng số — mô hình càng đơn giản thì bài học về thiên kiến càng rõ.",
      bienPhap:""},

    { id:"yc-04", yccd:"10.C3.MR1", chuDe:"C3", mach:"C",
      tinhHuong:"Trạm ỨNG DỤNG của SOI AI sinh ra câu trả lời bằng một máy học từ ngữ liệu có sẵn trong ứng dụng, thay vì gọi một mô hình ngôn ngữ lớn trên mạng.",
      cauHoi:"Vì sao lựa chọn công nghệ này lại phù hợp với mục tiêu dạy học về hiện tượng bịa đặt?",
      luaChon:[
        {id:"a", text:"Vì mô hình nhỏ thì luôn chính xác hơn mô hình lớn."},
        {id:"b", text:"Vì hệ biết trước chủ đề nào có trong ngữ liệu nên biết trước câu trả lời nào có căn cứ và câu nào là bịa; nhờ đó chấm được tự động, và học sinh thấy tận mắt một hệ trả lời trôi chảy về chủ đề nó chưa từng học."},
        {id:"c", text:"Vì không cần viết mã nguồn cho mô hình nhỏ."},
        {id:"d", text:"Vì mô hình ngôn ngữ lớn không bao giờ bịa thông tin."}],
      dapAn:"b",
      giaiThich:"Đây là ví dụ về việc chọn công nghệ theo ràng buộc sư phạm thay vì theo sức mạnh. Điều kiện thể lệ yêu cầu sản phẩm đã triển khai trong lớp học và hệ thống tự đánh giá được; một mô hình lớn trên mạng không đáp ứng được cả hai điều đó ở trường vùng khó. Phương án (d) sai về bản chất: bịa thông tin là vấn đề cố hữu của mô hình sinh nội dung, không phụ thuộc kích thước.",
      bienPhap:""}
  ];

  const TAT_CA = NHOM_RUI_RO.concat(NHOM_VI_PHAM, NHOM_YEU_CAU);

  /* ================= GIAO DIỆN: dựng bằng createElement + textContent =================
   * Không dùng innerHTML cho bất kì nội dung nào trong tệp này. */
  function veTinhHuong(host, onCham){
    host.textContent = "";
    TAT_CA.forEach((q, qi) => {
      const box = document.createElement("div");
      box.className = "card";
      box.style.background = "var(--nen2)";

      const h = document.createElement("h3");
      h.textContent = "Tình huống " + (qi + 1) + " · " + q.yccd;
      box.appendChild(h);

      const t = document.createElement("p");
      t.className = "chu2";
      t.textContent = q.tinhHuong;
      box.appendChild(t);

      const ch = document.createElement("p");
      const b = document.createElement("b");
      b.textContent = q.cauHoi;
      ch.appendChild(b);
      box.appendChild(ch);

      const chips = document.createElement("div");
      chips.className = "chips";
      const fb = document.createElement("div");

      q.luaChon.forEach(l => {
        const nut = document.createElement("button");
        nut.type = "button";
        nut.className = "chip";
        nut.textContent = l.id.toUpperCase() + ". " + l.text;
        nut.onclick = () => {
          const dapUng = (l.id === q.dapAn);
          fb.className = "phanhoi " + (dapUng ? "dung" : "sai");
          fb.textContent = "";
          const p1 = document.createElement("p");
          const b1 = document.createElement("b");
          /* KHÔNG dùng chữ "đúng/sai" làm nhãn năng lực: Khung 2422 phần VI quy định
           * không xác lập đầu điểm riêng cho nội dung giáo dục AI. Phản hồi ở đây là
           * xác nhận đáp án của một câu hỏi kiến thức, không phải điểm của học sinh. */
          b1.textContent = dapUng ? "✅ Đáp án đúng. " : "❌ Chưa phải đáp án đúng. ";
          p1.appendChild(b1);
          p1.appendChild(document.createTextNode(q.giaiThich));
          fb.appendChild(p1);
          if(q.bienPhap){
            const p2 = document.createElement("p");
            p2.className = "nho chu2";
            const b2 = document.createElement("b");
            b2.textContent = "Biện pháp hạn chế (nội dung của 10.A2.MR1): ";
            p2.appendChild(b2);
            p2.appendChild(document.createTextNode(q.bienPhap));
            fb.appendChild(p2);
          }
          const p3 = document.createElement("p");
          p3.className = "nho chu2";
          p3.textContent = "Phương án đúng: " + q.dapAn.toUpperCase()
                         + " · Yêu cầu cần đạt " + q.yccd + " · chủ đề " + q.chuDe;
          fb.appendChild(p3);
          [...chips.children].forEach(c => { c.disabled = true; });
          nut.classList.add("chon");
          if(onCham) onCham(q, l.id, dapUng);
        };
        chips.appendChild(nut);
      });

      box.appendChild(chips);
      box.appendChild(fb);
      host.appendChild(box);
    });
  }

  /** Danh sách 5 YCCĐ mà tệp này phủ — dùng cho báo cáo và bản đồ năng lực. */
  function yccdPhu(){
    const s = new Set();
    TAT_CA.forEach(q => s.add(q.yccd));
    return [...s].sort();
  }

  window.MX_TINH_HUONG = {
    TAT_CA, NHOM_RUI_RO, NHOM_VI_PHAM, NHOM_YEU_CAU,
    veTinhHuong, yccdPhu,
    thongTin(){
      const theoYccd = {};
      TAT_CA.forEach(q => { theoYccd[q.yccd] = (theoYccd[q.yccd] || 0) + 1; });
      return { soTinhHuong: TAT_CA.length, theoYccd, yccdPhu: yccdPhu() };
    }
  };
})();
