/* SOI AI — siêu dữ liệu: 4 mạch + 13 chủ đề QĐ 2422/QĐ-BGDĐT, 5 loại lỗi.
   UNESCO AI CFS 2024 (12 khối) chỉ dùng làm cột ĐỐI CHIẾU PHỤ — trục báo cáo chính
   là 13 chủ đề của Bộ, xem data/yccd.js (đã verify 22/22 bằng tools/verify_yccd.py).
   Chạy offline, không cần máy chủ. Dữ liệu nhúng dạng JS để mở trực tiếp bằng file:// (USB). */
window.MX_META = {
  ten: "SOI AI",
  khauHieu: "Soi AI để hiểu AI",
  phienBan: "1.0.0",
  ngayDongGoi: "2026-10-04",
  canCu: "QĐ 2422/QĐ-BGDĐT (18/8/2026) · CV 5588/BGDĐT-GDPT (19/8/2026)",

  /* 4 mạch nội dung — QĐ 2422/QĐ-BGDĐT (18/8/2026), Khung nội dung giáo dục AI cho HS phổ thông */
  mach: {
    A: "Tư duy lấy con người làm trung tâm",
    B: "Đạo đức AI",
    C: "Các kĩ thuật và ứng dụng AI",
    D: "Thiết kế hệ thống AI"
  },

  /* 12 khối năng lực — UNESCO AI Competency Framework for Students (2024)
     4 aspects × 3 levels (Understand / Apply / Create). Ánh xạ gần 1-1 với 4 mạch QĐ 2422. */
  unesco: {
    A1: { aspect: "A", level: 1, ten: "Hiểu: AI phục vụ con người" },
    A2: { aspect: "A", level: 2, ten: "Vận dụng: đánh giá AI theo nhu cầu con người" },
    A3: { aspect: "A", level: 3, ten: "Sáng tạo: đề xuất giải pháp AI lấy con người làm trung tâm" },
    B1: { aspect: "B", level: 1, ten: "Hiểu: vấn đề đạo đức của AI" },
    B2: { aspect: "B", level: 2, ten: "Vận dụng: xử lí tình huống đạo đức AI" },
    B3: { aspect: "B", level: 3, ten: "Sáng tạo: đề xuất nguyên tắc dùng AI có trách nhiệm" },
    C1: { aspect: "C", level: 1, ten: "Hiểu: kĩ thuật và ứng dụng AI" },
    C2: { aspect: "C", level: 2, ten: "Vận dụng: dùng công cụ AI" },
    C3: { aspect: "C", level: 3, ten: "Sáng tạo: tạo sản phẩm với AI" },
    D1: { aspect: "D", level: 1, ten: "Hiểu: quá trình huấn luyện hệ thống AI" },
    D2: { aspect: "D", level: 2, ten: "Vận dụng: huấn luyện/cải tiến mô hình đơn giản" },
    D3: { aspect: "D", level: 3, ten: "Sáng tạo: thiết kế hệ thống AI đơn giản" }
  },

  /* 5 loại lỗi AI cài sẵn trong "Đấu trường bắt lỗi" */
  loaiLoi: {
    so_lieu_bia: {
      ten: "Số liệu bịa đặt",
      moTa: "AI nêu con số/thống kê rất cụ thể nhưng không có nguồn thật, hoặc phi lí.",
      mau: "#e8590c"
    },
    nguon_khong_ton_tai: {
      ten: "Nguồn/văn bản không tồn tại",
      moTa: "AI trích một văn bản pháp luật, bài báo, cuốn sách hoặc tổ chức không có thật.",
      mau: "#c2255c"
    },
    thien_kien: {
      ten: "Thiên kiến, định kiến",
      moTa: "AI suy xét dựa trên giới tính, vùng miền, hoàn cảnh... thay vì năng lực thực tế.",
      mau: "#9c36b5"
    },
    suy_luan_sai: {
      ten: "Suy luận sai",
      moTa: "Kết luận không theo logic: vội khái quát, vin vào số đông, nhầm tương quan với nhân quả.",
      mau: "#1971c2"
    },
    lo_du_lieu_ca_nhan: {
      ten: "Xui lộ dữ liệu cá nhân",
      moTa: "AI khuyên đưa thông tin cá nhân của mình hoặc của người khác cho hệ thống/không gian công khai.",
      mau: "#2f9e44"
    }
  },

  /* Câu ĐÚNG (mồi nhử) — để đo tỉ lệ "bắt oan" */
  verdict: {
    co_loi: "Có lỗi",
    dung: "Không có lỗi"
  },

  /* Gợi ý nhận xét tự động (Tầng 3) — template tất định, không cần LLM khi chạy */
  nhanXetMau: {
    gioi: "Nhận diện lỗi AI rất tốt, đặc biệt ở nhóm {manh}. Cần lưu ý thêm nhóm {yeu} để tránh bỏ sót.",
    kha: "Nhận diện được phần lớn lỗi AI. Nên luyện thêm nhóm {yeu}: đọc chậm lại và kiểm tra từng con số, từng nguồn được nêu.",
    canCoGang: "Còn bỏ sót nhiều lỗi ở nhóm {yeu}. Nên luyện lại với các tình huống cùng loại và luôn tự hỏi: con số này lấy từ đâu, nguồn này có thật không."
  }
};
