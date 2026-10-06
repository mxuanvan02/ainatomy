/* SOI AI — NGÂN HÀNG "ĐẤU TRƯỜNG BẮT LỖI AI" (Tầng 2)
 * Mỗi item có NHÃN ĐÚNG CỨNG (oracle) vì lỗi do chính hệ cài sẵn:
 *   - loai: "co_loi" | "dung"  (đáp án đúng)
 *   - loaiLoi: khóa trong MX_META.loaiLoi (chỉ khi loai="co_loi")
 *   - mach: A/B/C/D theo QĐ 2422
 *   - unesco: khóa khối năng lực UNESCO (12 khối)
 *   - claims: mảng câu trong câu trả lời AI; claimLỗi = chỉ số claim chứa lỗi
 *   - giaiThich: hiện ra sau khi HS phán quyết (feedback tức thời, oracle-based)
 * HS phải: (1) chọn "Có lỗi"/"Không có lỗi"; (2) nếu có lỗi → chọn ĐÚNG loại lỗi.
 * Điểm do hệ tự chấm, không cần giáo viên.
 */
window.MX_BANK = [
  /* ===== LOẠI 1: SỐ LIỆU BỊA ===== */
  {
    id: "slb-01", mach: "B", unesco: "B1", loai: "co_loi", loaiLoi: "so_lieu_bia", claimLoi: 1,
    boiCanh: "Trợ lý AI trả lời câu hỏi của học sinh về an toàn thông tin.",
    claims: [
      "Việc bảo vệ dữ liệu cá nhân trên mạng là rất quan trọng với học sinh.",
      "Theo thống kê, 97,3% học sinh Việt Nam từng bị đánh cắp tài khoản ít nhất một lần trong năm 2025.",
      "Em nên đặt mật khẩu dài, khác nhau cho mỗi tài khoản và bật xác thực hai lớp."
    ],
    giaiThich: "Con số '97,3%' nghe rất thuyết phục nhưng không có nguồn nào kiểm chứng được — đây là số liệu AI bịa ra. Dấu hiệu nhận biết: số lẻ bất thường + khẳng định tuyệt đối + không nêu nguồn."
  },
  {
    id: "slb-02", mach: "C", unesco: "C1", loai: "co_loi", loaiLoi: "so_lieu_bia", claimLoi: 0,
    boiCanh: "AI giới thiệu về một mô hình học máy.",
    claims: [
      "Mô hình AI này đạt độ chính xác 100% trên mọi loại dữ liệu và không bao giờ sai.",
      "Học máy có giám sát cần dữ liệu đã được gán nhãn để huấn luyện.",
      "Càng nhiều dữ liệu chất lượng, mô hình thường càng học tốt hơn."
    ],
    giaiThich: "Không mô hình AI nào đạt 100% trên mọi dữ liệu. Khẳng định 'không bao giờ sai' là dấu hiệu kinh điển của số liệu/tuyên bố bịa. AI thật luôn có sai số."
  },
  {
    id: "slb-03", mach: "A", unesco: "A2", loai: "dung", claimLoi: -1,
    boiCanh: "AI tư vấn cách dùng công cụ tìm kiếm cho bài tập.",
    claims: [
      "Khi tra cứu thông tin, em nên đối chiếu ít nhất hai nguồn khác nhau trước khi tin.",
      "Nếu một con số quan trọng, hãy kiểm tra xem nó được lấy từ đâu.",
      "Không nên chép nguyên văn nội dung tìm được mà hãy đọc hiểu rồi viết lại bằng lời của mình."
    ],
    giaiThich: "Câu này KHÔNG có lỗi. Đây là lời khuyên đúng về tư duy phản biện và kiểm chứng thông tin — đúng tinh thần Khung 2422."
  },

  /* ===== LOẠI 2: NGUỒN/VĂN BẢN KHÔNG TỒN TẠI ===== */
  {
    id: "ngk-01", mach: "B", unesco: "B2", loai: "co_loi", loaiLoi: "nguon_khong_ton_tai", claimLoi: 1,
    boiCanh: "AI trích dẫn văn bản pháp luật về bảo vệ dữ liệu.",
    claims: [
      "Pháp luật Việt Nam có quy định về bảo vệ dữ liệu cá nhân.",
      "Điều này được nêu rõ tại 'Nghị định 999/2019/NĐ-CP về quyền riêng tư học đường', điều 42.",
      "Em không nên chia sẻ thông tin cá nhân của mình và bạn bè lên mạng."
    ],
    giaiThich: "'Nghị định 999/2019/NĐ-CP về quyền riêng tư học đường' KHÔNG tồn tại. AI bịa ra số hiệu + tên văn bản nghe rất 'thật'. Cách phát hiện: tra cứu số hiệu trên cổng văn bản chính thức (vanban.chinhphu.vn) — không có là bịa."
  },
  {
    id: "ngk-02", mach: "C", unesco: "C2", loai: "co_loi", loaiLoi: "nguon_khong_ton_tai", claimLoi: 2,
    boiCanh: "AI kể về lịch sử trí tuệ nhân tạo.",
    claims: [
      "Thuật ngữ 'Trí tuệ nhân tạo' được dùng phổ biến từ giữa thế kỉ XX.",
      "Học máy là một nhánh của trí tuệ nhân tạo.",
      "Nhà khoa học Nguyễn Văn A (Giải Nobel Tin học 2001) là người phát minh ra mạng nơ-ron đầu tiên."
    ],
    giaiThich: "Không có 'Giải Nobel Tin học' (Nobel không có hạng mục Tin học), và chi tiết này là bịa. Dấu hiệu: giải thưởng/vinh danh không tồn tại + tên nhân vật chung chung."
  },
  {
    id: "ngk-03", mach: "D", unesco: "D1", loai: "dung", claimLoi: -1,
    boiCanh: "AI mô tả các bước huấn luyện một mô hình phân loại.",
    claims: [
      "Để huấn luyện AI phân loại, trước hết cần thu thập một tập dữ liệu mẫu.",
      "Dữ liệu được chia thành phần để huấn luyện và phần để kiểm thử.",
      "Mô hình học từ dữ liệu huấn luyện, rồi được đánh giá bằng dữ liệu kiểm thử chưa từng thấy."
    ],
    giaiThich: "Câu này KHÔNG có lỗi. Mô tả đúng quy trình huấn luyện – kiểm thử cơ bản của học máy."
  },

  /* ===== LOẠI 3: THIÊN KIẾN, ĐỊNH KIẾN ===== */
  {
    id: "tk-01", mach: "B", unesco: "B2", loai: "co_loi", loaiLoi: "thien_kien", claimLoi: 1,
    boiCanh: "AI tư vấn hướng nghiệp cho học sinh lớp 12.",
    claims: [
      "Việc chọn ngành nghề nên dựa trên sở thích và năng lực của em.",
      "Tuy nhiên, là học sinh nữ nên em phù hợp với các ngành nhẹ nhàng như sư phạm mầm non hơn là kĩ thuật hay công nghệ.",
      "Em có thể làm bài trắc nghiệm hướng nghiệp để hiểu rõ hơn điểm mạnh của mình."
    ],
    giaiThich: "Đây là thiên kiến giới. Gán ngành nghề theo giới tính thay vì theo năng lực, sở thích của cá nhân. AI đã học định kiến này từ dữ liệu lệch. Không có cơ sở nào nói nữ kém phù hợp với kĩ thuật/công nghệ."
  },
  {
    id: "tk-02", mach: "A", unesco: "A1", loai: "co_loi", loaiLoi: "thien_kien", claimLoi: 2,
    boiCanh: "AI nhận xét về một bức ảnh chân dung dùng trong hệ thống điểm danh.",
    claims: [
      "Hệ thống nhận diện khuôn mặt hoạt động bằng cách so sánh các đặc điểm trên ảnh.",
      "Độ chính xác phụ thuộc vào chất lượng ảnh và dữ liệu đã dùng để huấn luyện.",
      "Hệ thống này nhận diện kém với người có làn da sẫm màu, nên các trường ở vùng dân tộc thiểu số tốt nhất không nên dùng công nghệ này."
    ],
    giaiThich: "Hai phần đầu đúng, nhưng phần cuối là thiên kiến, vì nó biến một hạn chế kĩ thuật (do dữ liệu huấn luyện lệch) thành kết luận loại trừ cả một nhóm người. Cách đúng là bổ sung dữ liệu đa dạng để cải thiện mô hình, không phải loại bỏ người dùng."
  },
  {
    id: "tk-03", mach: "B", unesco: "B1", loai: "dung", claimLoi: -1,
    boiCanh: "AI giải thích vì sao cần dữ liệu đa dạng khi huấn luyện.",
    claims: [
      "Nếu dữ liệu huấn luyện chỉ gồm một nhóm người, mô hình sẽ nhận diện kém các nhóm còn lại.",
      "Hiện tượng này gọi là thiên kiến của AI (AI bias).",
      "Vì vậy cần thu thập dữ liệu đa dạng, đại diện cho nhiều nhóm khác nhau."
    ],
    giaiThich: "Câu này KHÔNG có lỗi. Giải thích đúng và trung lập về thiên kiến dữ liệu, không nhắm vào nhóm người cụ thể nào."
  },

  /* ===== LOẠI 4: SUY LUẬN SAI ===== */
  {
    id: "sls-01", mach: "A", unesco: "A2", loai: "co_loi", loaiLoi: "suy_luan_sai", claimLoi: 1,
    boiCanh: "AI lí giải vì sao nên dùng một ứng dụng học tập.",
    claims: [
      "Ứng dụng này có rất nhiều lượt tải về.",
      "Vì có nhiều người tải nên chắc chắn đây là ứng dụng học tập tốt nhất và an toàn nhất cho học sinh.",
      "Em có thể dùng thử và tự đánh giá xem nó có phù hợp với mình không."
    ],
    giaiThich: "Suy luận sai: 'nhiều người dùng' không đồng nghĩa 'tốt nhất và an toàn nhất'. Đây là lỗi vin vào số đông — lấy số người dùng thay cho bằng chứng. Số lượt tải không phải bằng chứng về chất lượng hay độ an toàn."
  },
  {
    id: "sls-02", mach: "C", unesco: "C1", loai: "co_loi", loaiLoi: "suy_luan_sai", claimLoi: 2,
    boiCanh: "AI phân tích mối liên hệ giữa việc dùng AI và kết quả học tập.",
    claims: [
      "Một khảo sát cho thấy học sinh dùng AI thường có điểm trung bình cao hơn.",
      "Có thể AI giúp các em tra cứu và luyện tập hiệu quả hơn.",
      "Như vậy chắc chắn cứ dùng AI nhiều là điểm sẽ cao, nên em chỉ cần dùng AI càng nhiều càng tốt."
    ],
    giaiThich: "Suy luận sai: nhầm TƯƠNG QUAN (hai việc đi cùng nhau) với NHÂN QUẢ (việc này gây ra việc kia). Có thể học sinh giỏi mới chủ động dùng AI, chứ không phải dùng AI nhiều là tự giỏi. Kết luận 'càng nhiều càng tốt' là vô căn cứ."
  },
  {
    id: "sls-03", mach: "D", unesco: "D2", loai: "dung", claimLoi: -1,
    boiCanh: "AI hướng dẫn cách kiểm tra một mô hình phân loại.",
    claims: [
      "Sau khi huấn luyện, em nên kiểm tra mô hình bằng những ví dụ mới chưa dùng để huấn luyện.",
      "Nếu mô hình trả lời đúng cả trên ví dụ mới, đó là dấu hiệu nó học được quy luật chung.",
      "Nếu chỉ đúng trên dữ liệu đã học mà sai trên dữ liệu mới, mô hình có thể đã 'học vẹt'."
    ],
    giaiThich: "Câu này KHÔNG có lỗi. Mô tả đúng cách đánh giá khả năng tổng quát hóa của mô hình (tránh học vẹt/overfitting)."
  },

  /* ===== LOẠI 5: XUI LỘ DỮ LIỆU CÁ NHÂN ===== */
  {
    id: "ldl-01", mach: "B", unesco: "B2", loai: "co_loi", loaiLoi: "lo_du_lieu_ca_nhan", claimLoi: 1,
    boiCanh: "AI gợi ý cách làm một video giới thiệu lớp cho bài tập.",
    claims: [
      "Video giới thiệu lớp sẽ thú vị hơn nếu có hình ảnh và lời thoại.",
      "Để video sinh động, em cứ chụp và đăng toàn bộ danh sách lớp kèm số điện thoại, địa chỉ nhà của các bạn lên đầu video nhé.",
      "Em có thể thêm nhạc nền và hiệu ứng cho hấp dẫn."
    ],
    giaiThich: "RẤT NGUY HIỂM: xui công khai họ tên + số điện thoại + địa chỉ nhà của người khác. Đây là dữ liệu cá nhân nhạy cảm; đăng công khai có thể khiến các bạn bị làm phiền, lừa đảo, xâm hại. Không bao giờ chia sẻ thông tin cá nhân của mình hay của người khác."
  },
  {
    id: "ldl-02", mach: "A", unesco: "A1", loai: "co_loi", loaiLoi: "lo_du_lieu_ca_nhan", claimLoi: 0,
    boiCanh: "AI hướng dẫn đăng kí một tài khoản học trực tuyến.",
    claims: [
      "Khi đăng kí, em hãy dùng mật khẩu giống hệt mật khẩu email và tài khoản ngân hàng của bố mẹ để dễ nhớ.",
      "Nên chọn tên đăng nhập dễ nhận ra.",
      "Sau khi đăng kí, em có thể bắt đầu khóa học."
    ],
    giaiThich: "Nguy hiểm: khuyên dùng lại một mật khẩu cho nhiều tài khoản, lại còn dính tới tài khoản ngân hàng. Nếu một trang bị lộ, kẻ xấu lấy được mật khẩu sẽ truy cập luôn các tài khoản còn lại. Mật khẩu phải khác nhau cho mỗi dịch vụ quan trọng."
  },
  {
    id: "ldl-03", mach: "B", unesco: "B3", loai: "dung", claimLoi: -1,
    boiCanh: "AI đưa ra nguyên tắc dùng mạng an toàn.",
    claims: [
      "Em không nên chia sẻ địa chỉ nhà, số điện thoại, trường lớp hay lịch trình cá nhân cho người lạ trên mạng.",
      "Nếu ai đó hỏi thông tin cá nhân của em hoặc của bạn bè, hãy hỏi ý kiến thầy cô hoặc bố mẹ trước.",
      "Một thông tin đã đưa lên mạng thì rất khó xóa hoàn toàn, nên hãy cân nhắc trước khi đăng."
    ],
    giaiThich: "Câu này KHÔNG có lỗi. Đây là những nguyên tắc bảo vệ dữ liệu cá nhân đúng đắn."
  },

  /* ===== THÊM CÂU ĐÚNG + CÂU LỖI để cân bằng tỉ lệ (giảm đoán mò) ===== */
  {
    id: "slb-04", mach: "C", unesco: "C3", loai: "co_loi", loaiLoi: "so_lieu_bia", claimLoi: 2,
    boiCanh: "AI gợi ý dùng công cụ vẽ sơ đồ tư duy.",
    claims: [
      "Sơ đồ tư duy giúp em sắp xếp ý tưởng trực quan hơn.",
      "Có nhiều công cụ miễn phí để vẽ sơ đồ tư duy.",
      "Theo báo cáo chính thức, công cụ này đã giúp 100% học sinh Việt Nam tăng điểm môn Toán thêm đúng 5,0 điểm chỉ sau một tuần."
    ],
    giaiThich: "Con số '100% học sinh' + 'tăng đúng 5,0 điểm' + 'chỉ sau một tuần' là bịa, vì quá tuyệt đối, quá đẹp, không nguồn. Kết quả giáo dục thật không bao giờ đồng loạt và tức thời như vậy."
  },
  {
    id: "tk-04", mach: "B", unesco: "B2", loai: "co_loi", loaiLoi: "thien_kien", claimLoi: 1,
    boiCanh: "AI nhận xét về bài thuyết trình của một học sinh.",
    claims: [
      "Bài thuyết trình có bố cục rõ ràng và hình ảnh minh họa tốt.",
      "Tuy nhiên vì em là học sinh ở vùng nông thôn nên chắc chắn kĩ năng công nghệ của em sẽ không bằng các bạn thành phố.",
      "Em nên luyện thêm phần trình bày để tự tin hơn."
    ],
    giaiThich: "Thiên kiến vùng miền: gán năng lực công nghệ theo nơi sống. Xuất thân nông thôn không quyết định kĩ năng của một cá nhân. Nhận xét phải dựa trên chính bài làm, không dựa trên định kiến."
  },
  {
    id: "sls-04", mach: "A", unesco: "A1", loai: "dung", claimLoi: -1,
    boiCanh: "AI giải thích khi nào con người nên và không nên dùng AI.",
    claims: [
      "AI giỏi xử lí nhanh lượng dữ liệu lớn và các việc lặp đi lặp lại.",
      "Nhưng những quyết định quan trọng liên quan đến con người thì vẫn cần con người cân nhắc và chịu trách nhiệm.",
      "Việc có dùng AI hay không nên dựa trên mục đích, nhu cầu và sự an toàn."
    ],
    giaiThich: "Câu này KHÔNG có lỗi. Thể hiện đúng tư duy 'lấy con người làm trung tâm' — AI hỗ trợ, con người quyết định và chịu trách nhiệm."
  },
  {
    id: "ngk-04", mach: "B", unesco: "B1", loai: "co_loi", loaiLoi: "nguon_khong_ton_tai", claimLoi: 0,
    boiCanh: "AI viện dẫn một tổ chức để tăng độ tin cậy.",
    claims: [
      "Theo 'Hiệp hội An toàn AI Đông Nam Á (AISA)', học sinh dưới 18 tuổi được phép chia sẻ mật khẩu với bạn thân.",
      "Việc này giúp các em hỗ trợ nhau khi quên mật khẩu.",
      "Em nên nhớ mật khẩu của mình."
    ],
    giaiThich: "'Hiệp hội AISA' này không kiểm chứng được là có thật, và nội dung khuyên chia sẻ mật khẩu là SAI về nguyên tắc bảo mật. Vừa bịa nguồn, vừa đưa lời khuyên nguy hiểm. Khi thấy một tổ chức lạ + lời khuyên bất thường, hãy nghi ngờ."
  },
  {
    id: "ldl-04", mach: "C", unesco: "C2", loai: "dung", claimLoi: -1,
    boiCanh: "AI hướng dẫn dùng trợ lí ảo để học ngoại ngữ.",
    claims: [
      "Em có thể luyện phát âm bằng cách nói và để trợ lí ảo nhận xét.",
      "Chỉ nên nói về chủ đề học tập, không cần kể thông tin riêng tư của gia đình cho trợ lí ảo.",
      "Ghi âm luyện tập có thể lưu lại để nghe và so sánh sự tiến bộ của chính mình."
    ],
    giaiThich: "Câu này KHÔNG có lỗi. Dùng AI hợp lí mà vẫn giữ ranh giới không chia sẻ thông tin riêng tư."
  },
  {
    id: "slb-05", mach: "D", unesco: "D3", loai: "co_loi", loaiLoi: "suy_luan_sai", claimLoi: 2,
    boiCanh: "AI góp ý cho dự án thiết kế hệ thống phân loại rác của học sinh.",
    claims: [
      "Ý tưởng dùng camera và AI để phân loại rác tự động là khả thi.",
      "Em cần thu thập ảnh các loại rác để huấn luyện mô hình.",
      "Vì rác hữu cơ thường có màu xanh nên em cứ lập trình cho AI hễ thấy vật màu xanh là xếp vào rác hữu cơ, như vậy là đủ chính xác."
    ],
    giaiThich: "Suy luận sai vì khái quát hóa vội. 'Màu xanh = rác hữu cơ' là quy tắc nông cạn, sẽ sai với rất nhiều trường hợp (túi nilon xanh, chai nhựa xanh...). Đây là ví dụ về việc gán một đặc điểm bề ngoài làm quy luật — đúng loại lỗi mà AI thật cũng hay mắc nếu huấn luyện ẩu."
  },
  {
    id: "tk-05", mach: "A", unesco: "A3", loai: "dung", claimLoi: -1,
    boiCanh: "AI đề xuất cách thiết kế một ứng dụng AI công bằng hơn.",
    claims: [
      "Trước khi xây dựng hệ thống AI, hãy nghĩ xem nó ảnh hưởng tới những ai.",
      "Nên kiểm tra xem dữ liệu huấn luyện có đại diện công bằng cho các nhóm người khác nhau không.",
      "Cần có cách để con người xem xét và điều chỉnh khi hệ thống đưa ra kết quả bất lợi cho ai đó."
    ],
    giaiThich: "Câu này KHÔNG có lỗi. Đây là các bước thiết kế AI có trách nhiệm, lấy con người làm trung tâm — đúng tinh thần mạch A và B của QĐ 2422."
  }
];

/* Trộn thứ tự tất định theo seed để mỗi lần mở không đoán được vị trí, nhưng tái lập được */
window.MX_shuffleBank = function(seed){
  const a = window.MX_BANK.slice();
  let s = seed >>> 0;
  const rnd = () => (s = (s*1664525 + 1013904223) >>> 0) / 4294967296;
  for(let i=a.length-1;i>0;i--){ const j = Math.floor(rnd()*(i+1)); [a[i],a[j]]=[a[j],a[i]]; }
  return a;
};
