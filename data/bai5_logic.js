/* HỌC AI — BÀI TẬP BÀI 5 "DỮ LIỆU LÔGIC" (Tin học 10, Chủ đề 1)
 * Bám nội dung Bài 5 sách Kết nối tri thức / Chân trời sáng tạo:
 *   (1) Các giá trị chân lí và các phép toán lôgic (AND, OR, NOT)
 *   (2) Biểu diễn dữ liệu lôgic (1 bit: 1 = TRUE, 0 = FALSE)
 * Mọi item đặt trong NGỮ CẢNH AI để nối bài học với sản phẩm.
 * NHÃN ĐÚNG có sẵn từ lúc thiết kế → hệ tự chấm, không cần giáo viên.
 */
window.MX_BAI5 = [
  {
    id: "b5-01", mach: "C", unesco: "C1",
    cauHoi: "Một bộ lọc AI hiển thị cảnh báo khi biểu thức sau TRUE:\n(điểm < 5) OR (số buổi vắng > 3)\nBạn An có điểm = 6 và vắng 4 buổi. Bộ lọc có hiện cảnh báo không?",
    luaChon: [
      { id: "a", text: "Có — vì phép OR chỉ cần MỘT vế đúng: (6 < 5) là FALSE nhưng (4 > 3) là TRUE." },
      { id: "b", text: "Không — vì điểm 6 lớn hơn 5 nên vế đầu sai, cả biểu thức sai." },
      { id: "c", text: "Không — vì phép OR yêu cầu cả hai vế đều đúng." },
      { id: "d", text: "Có — vì phép OR luôn cho kết quả TRUE với mọi giá trị." }
    ],
    dapAn: "a",
    giaiThich: "(điểm < 5) = FALSE; (vắng > 3) = TRUE. FALSE OR TRUE = TRUE → có hiện cảnh báo. Phép OR chỉ cần ít nhất một vế TRUE. Đáp án (c) nhầm OR với AND — đây là lỗi rất hay gặp."
  },
  {
    id: "b5-02", mach: "C", unesco: "C1",
    cauHoi: "Một hệ thống chỉ cho nộp bài khi biểu thức sau TRUE:\n(đã đăng nhập) AND (còn trong thời hạn)\nBình đã đăng nhập nhưng đã hết hạn nộp. Hệ thống có cho nộp không?",
    luaChon: [
      { id: "a", text: "Có — vì Bình đã đăng nhập nên vế đầu TRUE là đủ." },
      { id: "b", text: "Không — vì phép AND đòi hỏi CẢ HAI vế TRUE; ở đây (còn thời hạn) = FALSE nên kết quả là FALSE." },
      { id: "c", text: "Không — vì phép AND luôn cho kết quả FALSE." },
      { id: "d", text: "Có — vì hệ thống sẽ tự gia hạn cho Bình." }
    ],
    dapAn: "b",
    giaiThich: "TRUE AND FALSE = FALSE → không cho nộp. Phép AND chỉ TRUE khi cả hai vế cùng TRUE. Đây chính là lí do trong 'Đấu trường bắt lỗi AI', một câu trả lời chỉ được coi là ĐÚNG khi cả 3 câu của nó đều đúng."
  },
  {
    id: "b5-03", mach: "C", unesco: "C2",
    cauHoi: "Trong máy tính, một giá trị lôgic (TRUE/FALSE) được biểu diễn bằng bao nhiêu bit?",
    luaChon: [
      { id: "a", text: "1 bit — quy ước 1 là TRUE, 0 là FALSE." },
      { id: "b", text: "8 bit — vì mọi dữ liệu đều cần 1 byte." },
      { id: "c", text: "2 bit — một bit cho TRUE, một bit cho FALSE." },
      { id: "d", text: "Không biểu diễn được bằng bit." }
    ],
    dapAn: "a",
    giaiThich: "Giá trị lôgic chỉ có HAI trạng thái nên chỉ cần 1 bit: quy ước 1 = TRUE, 0 = FALSE. Đây là nội dung mục 'Biểu diễn dữ liệu lôgic' của Bài 5. (Trong thực tế phần mềm có thể cấp phát 1 byte cho tiện truy cập, nhưng về mặt biểu diễn thông tin thì chỉ cần 1 bit.)"
  },
  {
    id: "b5-04", mach: "C", unesco: "C2",
    cauHoi: "Cho A = TRUE, B = TRUE. Giá trị của biểu thức NOT (A AND B) là gì?",
    luaChon: [
      { id: "a", text: "TRUE" },
      { id: "b", text: "FALSE" },
      { id: "c", text: "Không xác định được" },
      { id: "d", text: "Bằng A OR B" }
    ],
    dapAn: "b",
    giaiThich: "A AND B = TRUE AND TRUE = TRUE. NOT TRUE = FALSE. Chú ý thứ tự thực hiện: tính trong ngoặc trước, rồi mới lấy NOT."
  },
  {
    id: "b5-05", mach: "D", unesco: "D1",
    cauHoi: "Một mô hình AI phân loại ảnh quyết định theo quy tắc:\nz = w₁x₁ + w₂x₂ + b ,  nếu z ≥ 0 thì kết luận TRUE (có đối tượng cần tìm).\nPhần nào của quy tắc này là một phép so sánh lôgic?",
    luaChon: [
      { id: "a", text: "Phần tính z = w₁x₁ + w₂x₂ + b." },
      { id: "b", text: "Phần 'nếu z ≥ 0' — nó biến một con số thành TRUE hoặc FALSE." },
      { id: "c", text: "Các trọng số w₁, w₂." },
      { id: "d", text: "Không có phần nào là phép lôgic cả." }
    ],
    dapAn: "b",
    giaiThich: "Đúng. 'z ≥ 0' là một phép so sánh cho ra TRUE/FALSE — chính là dữ liệu lôgic của Bài 5. Điểm khác biệt so với biểu thức lôgic thông thường: các trọng số w KHÔNG do người lập trình viết ra mà do mô hình HỌC từ dữ liệu, nên nó có thể học sai và cho kết luận sai có hệ thống."
  },
  {
    id: "b5-06", mach: "B", unesco: "B2",
    cauHoi: "Hệ thống AI chấm bài đặt biến:\nT = 'bài thật sự có lỗi',  P = 'hệ thống báo có lỗi'.\nTrường hợp 'bắt oan' (hệ báo có lỗi nhưng bài thật ra đúng) tương ứng với biểu thức nào?",
    luaChon: [
      { id: "a", text: "T AND P" },
      { id: "b", text: "(NOT T) AND P" },
      { id: "c", text: "T AND (NOT P)" },
      { id: "d", text: "(NOT T) AND (NOT P)" }
    ],
    dapAn: "b",
    giaiThich: "'Bài thật ra đúng' = NOT T; 'hệ báo có lỗi' = P. Vậy bắt oan = (NOT T) AND P. Bốn tổ hợp này tạo thành BẢNG NHẦM LẪN: T∧P = bắt đúng, (¬T)∧P = bắt oan, T∧(¬P) = bỏ sót, (¬T)∧(¬P) = xác nhận đúng. Em xem bảng của chính mình ở mục 3 trang này."
  },
  {
    id: "b5-07", mach: "B", unesco: "B2",
    cauHoi: "Hai biểu thức sau có luôn cho cùng kết quả với mọi giá trị của A và B không?\n(1) NOT (A OR B)        (2) (NOT A) AND (NOT B)",
    luaChon: [
      { id: "a", text: "Có — hai biểu thức này luôn bằng nhau (quy tắc De Morgan)." },
      { id: "b", text: "Không — chỉ bằng nhau khi A và B cùng TRUE." },
      { id: "c", text: "Không — biểu thức (1) luôn TRUE còn (2) luôn FALSE." },
      { id: "d", text: "Không thể so sánh vì hai biểu thức khác số phép toán." }
    ],
    dapAn: "a",
    giaiThich: "Đây là quy tắc De Morgan: NOT(A OR B) = (NOT A) AND (NOT B). Kiểm bằng bảng chân lí 4 dòng: A=T,B=T → F=F; A=T,B=F → F=F; A=F,B=T → F=F; A=F,B=F → T=T. Luôn bằng nhau. Quy tắc này rất hữu dụng khi đọc điều kiện lọc của một hệ thống AI."
  },
  {
    id: "b5-08", mach: "A", unesco: "A2",
    cauHoi: "Một đèn báo an toàn được thiết kế để SÁNG khi đúng MỘT trong hai cảm biến phát hiện nguy cơ (không phải cả hai, không phải không cái nào). Với A, B là trạng thái hai cảm biến, biểu thức nào mô tả đúng?",
    luaChon: [
      { id: "a", text: "A AND B" },
      { id: "b", text: "A OR B" },
      { id: "c", text: "(A OR B) AND NOT (A AND B)" },
      { id: "d", text: "NOT (A OR B)" }
    ],
    dapAn: "c",
    giaiThich: "'Ít nhất một' = A OR B; 'không phải cả hai' = NOT (A AND B). Ghép bằng AND ta được (A OR B) AND NOT (A AND B) — chính là phép XOR. Kiểm bằng bảng chân lí: T,T → FALSE; T,F → TRUE; F,T → TRUE; F,F → FALSE. Đúng yêu cầu 'đúng một'."
  }
];
