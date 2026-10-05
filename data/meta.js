/* SOI AI — siêu dữ liệu: 4 mạch + 13 chủ đề QĐ 2422/QĐ-BGDĐT, 5 loại lỗi.
   UNESCO AI CFS 2024 (12 khối) chỉ dùng làm cột ĐỐI CHIẾU PHỤ — trục báo cáo chính
   là 13 chủ đề của Bộ, xem data/yccd.js (đã verify 22/22 bằng tools/verify_yccd.py).
   Chạy offline, không cần máy chủ. Dữ liệu nhúng dạng JS để mở trực tiếp bằng file:// (USB). */
window.MX_META = {
  ten: "SOI AI",
  dinhDanh: "Phòng thực hành Trí tuệ nhân tạo lớp 10",
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

  /* 5 loại lỗi AI cài sẵn trong "Đấu trường bắt lỗi"
   *
   * Trường `dauHieu` (thêm 05/10, cùng lúc với js/bt09.js) là TẬP DẤU HIỆU ĐỌC ĐƯỢC
   * BẰNG MÁY của từng loại lỗi, và nó phục vụ đúng Mức 3 của BT-09: học sinh tự soạn
   * một câu trả lời AI có cài ĐÚNG MỘT lỗi rồi khai loại lỗi đó ra. Hệ không đọc được
   * câu học sinh viết để phán "câu này có lỗi hay không" — việc đó cần hiểu ngữ nghĩa.
   * Nên hệ chỉ kiểm được ĐÚNG một điều: câu em viết có chứa những dấu hiệu HÌNH THỨC
   * của loại lỗi em khai hay không. Nói rõ giới hạn này trên giao diện, không để học
   * sinh tưởng hệ đã xác nhận câu của mình là một câu hỏng thật.
   *
   * Mỗi dấu hiệu là một chuỗi so khớp sau khi bỏ dấu + hạ chữ thường (cùng quy ước
   * chuanHoa() trong js/kienthuc.js và js/bt13.js). Từ nào ngắn quá thì dễ khớp oan,
   * nên mỗi mục phải là một CỤM có nghĩa, không dùng từ đơn như "vì" một mình.
   */
  loaiLoi: {
    so_lieu_bia: {
      ten: "Số liệu bịa đặt",
      moTa: "AI nêu con số/thống kê rất cụ thể nhưng không có nguồn thật, hoặc phi lí.",
      mau: "#e8590c",
      dauHieu: {
        /* canChuSo: yêu cầu câu phải có CHỮ SỐ thật. Bản đầu em viết từ khoá "trên \\d"
         * như một regex, nhưng phép so khớp là String.includes() nên nó đi tìm đúng
         * chuỗi có dấu gạch chéo ngược — không bao giờ khớp. Nay chữ số được kiểm bằng
         * mã (/\\d/), không nhét vào danh sách từ khoá nữa.
         *
         * "gấp" và "lần" đã BỊ BỎ (05/10, bắt bằng battery 5 câu sạch): phép so khớp bỏ
         * dấu, nên "gấp" -> "gap" khớp luôn "gặp khó khăn", và "lần" -> "lan" khớp "lan
         * tỏa". Cả hai đều là từ ngắn mà sau khi mất dấu thì trùng với từ khác nghĩa.
         * "%" và phép kiểm chữ số đã đủ để nhận ra một câu có số liệu; giữ hai từ này chỉ
         * tạo cảnh báo sai khiến học sinh học cách bỏ qua cảnh báo. */
        canChuSo: true,
        buocPhaiCo: ["%", "phần trăm", "triệu", "tỉ lệ", "trên tổng số", "con số"],
        moTaBatBuoc: "phải có một CON SỐ cụ thể (phần trăm, số lượng, tỉ lệ)",
        khongNenCo: ["nguồn", "theo báo", "trích dẫn", "khảo sát", "nghiên cứu"],
        moTaKhongNen: "không được nêu nguồn kiểm chứng được — có nguồn thật thì không còn là số liệu bịa"
      }
    },
    nguon_khong_ton_tai: {
      ten: "Nguồn/văn bản không tồn tại",
      moTa: "AI trích một văn bản pháp luật, bài báo, cuốn sách hoặc tổ chức không có thật.",
      mau: "#c2255c",
      dauHieu: {
        /* Từ khoá ở đây là CỤM dẫn nguồn, không phải từ đơn. Bản đầu có "theo " và
         * "vien " — hai cụm quá ngắn, khớp oan gần như mọi câu. */
        buocPhaiCo: ["theo luật", "theo nghị định", "theo thông tư", "theo nghiên cứu",
                     "theo báo cáo", "theo khảo sát", "điều ", "khoản ", "nghị định",
                     "thông tư", "luật số", "giáo sư", "tiến sĩ", "tổ chức"],
        moTaBatBuoc: "phải có một DẪN NGUỒN trông trang trọng (tên luật, điều khoản, tổ chức, chức danh)",
        khongNenCo: [],
        moTaKhongNen: ""
      }
    },
    thien_kien: {
      ten: "Thiên kiến, định kiến",
      moTa: "AI suy xét dựa trên giới tính, vùng miền, hoàn cảnh... thay vì năng lực thực tế.",
      mau: "#9c36b5",
      dauHieu: {
        /* Battery 5 câu sạch (05/10) bắt được hai lỗi ở danh sách đầu:
         *   - "nữ sinh" KHÔNG khớp vì em chỉ viết "học sinh nữ" (đảo thứ tự là trượt).
         *   - "miền " và "quê " quá ngắn: bỏ dấu thì "miễn phí" khớp "mien ", "que củi"
         *     khớp "que ". Nay nói rõ vùng nào và nhóm người nào thay vì để từ trần. */
        buocPhaiCo: ["nam giới", "nữ giới", "phụ nữ", "đàn ông", "con gái", "con trai",
                     "nữ sinh", "nam sinh", "giáo viên nam",
                     "miền bắc", "miền nam", "miền trung", "miền núi", "vùng sâu", "vùng xa",
                     "nông thôn", "thành phố", "dân tộc", "giới tính", "hoàn cảnh gia đình",
                     "gia đình khó khăn"],
        moTaBatBuoc: "phải nêu một NHÓM NGƯỜI theo giới tính, vùng miền, dân tộc hoặc hoàn cảnh",
        khongNenCo: [],
        moTaKhongNen: ""
      }
    },
    suy_luan_sai: {
      ten: "Suy luận sai",
      moTa: "Kết luận không theo logic: vội khái quát, vin vào số đông, nhầm tương quan với nhân quả.",
      mau: "#1971c2",
      dauHieu: {
        /* "vi " và "nen " bị bỏ: "nên" xuất hiện trong gần như mọi câu tiếng Việt nên
         * không phải dấu hiệu của suy luận sai. Nay chỉ nhận cụm mang tính KẾT LUẬN. */
        buocPhaiCo: ["do đó", "vì vậy", "vì thế", "cho nên", "chứng tỏ", "suy ra",
                     "kéo theo", "đồng nghĩa", "có nghĩa là", "kết luận", "tất cả",
                     "luôn luôn", "hầu hết", "mọi người đều"],
        moTaBatBuoc: "phải có một BƯỚC NỐI mang tính kết luận (do đó, chứng tỏ, suy ra) hoặc một câu khái quát tuyệt đối",
        khongNenCo: [],
        moTaKhongNen: ""
      }
    },
    lo_du_lieu_ca_nhan: {
      ten: "Xui lộ dữ liệu cá nhân",
      moTa: "AI khuyên đưa thông tin cá nhân của mình hoặc của người khác cho hệ thống/không gian công khai.",
      mau: "#2f9e44",
      dauHieu: {
        buocPhaiCo: ["tên em là", "họ tên", "số điện thoại", "số tài khoản", "cccd", "cmnd", "căn cước", "địa chỉ nhà",
                     "ngày sinh", "ảnh cá nhân", "đăng lên", "chia sẻ công khai", "mật khẩu", "email"],
        moTaBatBuoc: "phải nêu một LOẠI THÔNG TIN CÁ NHÂN cụ thể, hoặc hành vi đăng/chia sẻ nó ra công khai",
        khongNenCo: [],
        moTaKhongNen: ""
      }
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
