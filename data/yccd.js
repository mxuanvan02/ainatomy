/* HỌC AI — dữ liệu 13 chủ đề + 22 yêu cầu cần đạt (YCCĐ) của LỚP 10.
 * NGUỒN: Khung nội dung giáo dục Trí tuệ nhân tạo cho học sinh phổ thông,
 *        ban hành kèm QĐ 2422/QĐ-BGDĐT ngày 18/8/2026 (phụ lục, lớp 10).
 * Nội dung YCCĐ là NGUYÊN VĂN, đã verify tự động bằng tools/verify_yccd.py
 * (22/22 đạt: subsequence đầy đủ + ô đặc hiệu nhất + từ khoá + tập mã).
 * KHÔNG sửa tay file này — sửa nguồn rồi sinh lại bằng tools/gen_yccd_js.py.
 *
 * Trục năng lực CHÍNH của app là 13 chủ đề của Bộ (mã [lớp].[chủ đề].[thứ tự]).
 * UNESCO AI CFS 2024 chỉ là cột ĐỐI CHIẾU phụ.
 */
window.MX_YCCD = {
  nguon: "QĐ 2422/QĐ-BGDĐT (18/8/2026) — Khung nội dung giáo dục AI cho HS phổ thông, lớp 10",
  lop: 10,
  daVerify: "22/22 YCCĐ — tools/verify_yccd.py",

  /* 4 mạch nội dung (nguyên văn) */
  mach: {
      "A": "Tư duy lấy con người làm trung tâm",
      "B": "Đạo đức AI",
      "C": "Các kĩ thuật và ứng dụng AI",
      "D": "Thiết kế hệ thống AI"
  },

  /* 13 chủ đề thành phần (nguyên văn). Lớp 10 có YCCĐ ở 10/13 chủ đề:
     B1, C1, C5 không có YCCĐ lớp 10 trong Khung. */
  chuDe: {
      "A1": "Tính chủ động của con người",
      "A2": "AI vì sự tiến bộ của con người",
      "A3": "Công dân trong kỉ nguyên AI",
      "B1": "Các khía cạnh đạo đức của AI",
      "B2": "Sử dụng AI an toàn và có trách nhiệm",
      "B3": "Nguyên tắc đạo đức và trách nhiệm xã hội",
      "C1": "Đặc điểm chính của AI",
      "C2": "Ứng dụng AI trong học tập và cuộc sống",
      "C3": "Công nghệ AI",
      "C4": "Dữ liệu trong AI",
      "C5": "Kĩ thuật và thuật toán AI",
      "D1": "Nhận diện và hình thành giải pháp",
      "D2": "Cấu trúc và tương tác, cải tiến hệ thống"
  },

  /* Đối chiếu UNESCO AI Competency Framework for Students (2024) — PHỤ */
  unescoDoiChieu: {"A1": "A1", "A2": "A2", "A3": "A3", "B1": "B1", "B2": "B2", "B3": "B3", "C1": "C1", "C2": "C2", "C3": "C3", "C4": "D1", "C5": "D2", "D1": "D1", "D2": "D2"},

  /* 22 YCCĐ lớp 10 — nguyên văn */
  danhSach: [
    {
      ma: "10.A1.1",
      chuDe: "A1",
      mach: "A",
      loai: "cốt lõi",
      text: "Thực hành xác định được vai trò của con người trong sử dụng, vận hành, tùy chỉnh một hệ thống AI cụ thể.",
      verify: { subseq: "23/23", tuKhoa: "3/3" },
    },
    {
      ma: "10.A1.2",
      chuDe: "A1",
      mach: "A",
      loai: "cốt lõi",
      text: "Giải thích được tại sao việc con người kiểm soát AI là quan trọng, thông qua việc liên hệ đến các giá trị như an toàn, công bằng và quyền lợi con người.",
      verify: { subseq: "33/33", tuKhoa: "4/4" },
    },
    {
      ma: "10.A2.1",
      chuDe: "A2",
      mach: "A",
      loai: "cốt lõi",
      text: "Nêu được một số rủi ro đối với con người, xã hội mà một sản phẩm AI có thể đem lại.",
      verify: { subseq: "21/21", tuKhoa: "3/3" },
    },
    {
      ma: "10.A2.MR1",
      chuDe: "A2",
      mach: "A",
      loai: "mở rộng",
      text: "Nêu được một số biện pháp hạn chế các rủi ro đối với con người, xã hội mà một sản phẩm AI có thể đem lại thông qua một dự án sáng tạo AI.",
      verify: { subseq: "34/34", tuKhoa: "3/3" },
    },
    {
      ma: "10.A3.1",
      chuDe: "A3",
      mach: "A",
      loai: "cốt lõi",
      text: "Kể tên được một vài quy định hoặc luật lệ (ở mức độ khái niệm, ví dụ: Luật An ninh mạng, Luật Dữ liệu, Luật Bảo vệ dữ liệu cá nhân) có chức năng bảo vệ người dùng trong không gian số.",
      verify: { subseq: "41/41", tuKhoa: "4/4" },
    },
    {
      ma: "10.B2.1",
      chuDe: "B2",
      mach: "B",
      loai: "cốt lõi",
      text: "Nêu được ví dụ về hành vi sử dụng AI hoặc sự cố liên quan đến AI vi phạm quy định của nhà trường hoặc các văn bản pháp luật liên quan đến sử dụng công nghệ thông tin.",
      verify: { subseq: "39/39", tuKhoa: "5/5" },
    },
    {
      ma: "10.B2.MR1",
      chuDe: "B2",
      mach: "B",
      loai: "mở rộng",
      text: "Nhận biết được một số dấu hiệu của nội dung do AI tạo sinh tạo ra; kiểm tra và nhận xét được mức độ minh bạch của việc khai báo sử dụng AI trong một sản phẩm.",
      verify: { subseq: "37/37", tuKhoa: "4/4" },
    },
    {
      ma: "10.B3.1",
      chuDe: "B3",
      mach: "B",
      loai: "cốt lõi",
      text: "Trình bày được ví dụ minh họa một số vấn đề đạo đức có thể phát sinh trong quá trình thiết kế và vận hành AI (như thiên vị dữ liệu, vi phạm quyền riêng tư hoặc thiếu minh bạch).",
      verify: { subseq: "40/40", tuKhoa: "4/4" },
    },
    {
      ma: "10.C2.1",
      chuDe: "C2",
      mach: "C",
      loai: "cốt lõi",
      text: "Xác định được các vấn đề thực tế có thể ứng dụng AI để thực hiện. Ưu tiên các vấn đề gần gũi, cần thiết trong bối cảnh Việt Nam, chẳng hạn: sản xuất nông nghiệp, các vấn đề liên quan đến các cộng đồng thiểu số, …",
      verify: { subseq: "47/47", tuKhoa: "5/5" },
    },
    {
      ma: "10.C2.MR1",
      chuDe: "C2",
      mach: "C",
      loai: "mở rộng",
      text: "Xác định được các yêu cầu cần có đối với việc ứng dụng AI thực hiện nhiệm vụ cụ thể.",
      verify: { subseq: "20/20", tuKhoa: "2/2" },
    },
    {
      ma: "10.C2.2",
      chuDe: "C2",
      mach: "C",
      loai: "cốt lõi",
      text: "Liệt kê được tên các ứng dụng AI theo các tính năng của hệ thống.",
      verify: { subseq: "15/15", tuKhoa: "2/2" },
    },
    {
      ma: "10.C2.MR2",
      chuDe: "C2",
      mach: "C",
      loai: "mở rộng",
      text: "Sử dụng được một số ứng dụng AI trong học tập.",
      verify: { subseq: "11/11", tuKhoa: "2/2" },
    },
    {
      ma: "10.C2.3",
      chuDe: "C2",
      mach: "C",
      loai: "cốt lõi",
      text: "Nêu được ví dụ một số trường hợp sử dụng AI hỗ trợ quá trình học tập.",
      verify: { subseq: "17/17", tuKhoa: "3/3" },
    },
    {
      ma: "10.C3.1",
      chuDe: "C3",
      mach: "C",
      loai: "cốt lõi",
      text: "Mô tả được các yêu cầu để đưa ra prompt phù hợp với mục tiêu cụ thể.",
      verify: { subseq: "17/17", tuKhoa: "3/3" },
    },
    {
      ma: "10.C3.MR1",
      chuDe: "C3",
      mach: "C",
      loai: "mở rộng",
      text: "Trình bày được ví dụ mô tả một số công nghệ để thiết kế và tạo AI.",
      verify: { subseq: "17/17", tuKhoa: "2/2" },
    },
    {
      ma: "10.C3.2",
      chuDe: "C3",
      mach: "C",
      loai: "cốt lõi",
      text: "Thực hành đặt prompt giải quyết một số vấn đề gần gũi trong cuộc sống, học tập một cách hiệu quả.",
      verify: { subseq: "21/21", tuKhoa: "4/4" },
    },
    {
      ma: "10.C3.3",
      chuDe: "C3",
      mach: "C",
      loai: "cốt lõi",
      text: "Phân biệt được AI tạo sinh với các hệ thống AI phân loại, dự đoán qua ví dụ cụ thể.",
      verify: { subseq: "20/20", tuKhoa: "4/4" },
    },
    {
      ma: "10.C4.1",
      chuDe: "C4",
      mach: "C",
      loai: "cốt lõi",
      text: "Phân tích được sự ảnh hưởng của chất lượng dữ liệu đến chất lượng AI.",
      verify: { subseq: "15/15", tuKhoa: "4/4" },
    },
    {
      ma: "10.C4.MR1",
      chuDe: "C4",
      mach: "C",
      loai: "mở rộng",
      text: "Phân tích được các dạng dữ liệu (hình ảnh, âm thanh, từ ngữ, …) được sử dụng để huấn luyện AI.",
      verify: { subseq: "20/20", tuKhoa: "5/5" },
    },
    {
      ma: "10.D1.1",
      chuDe: "D1",
      mach: "D",
      loai: "cốt lõi",
      text: "Nêu được ví dụ cụ thể, xác định nhiệm vụ hoặc mục tiêu cụ thể mà một hệ thống AI cần thực hiện, nêu được mối liên hệ giữa mục tiêu đó với các thành phần chính của hệ thống.",
      verify: { subseq: "40/40", tuKhoa: "4/4" },
    },
    {
      ma: "10.D2.1",
      chuDe: "D2",
      mach: "D",
      loai: "cốt lõi",
      text: "Mô tả được các thành phần cơ bản của hệ thống AI (dữ liệu, mô hình, thuật toán, đầu ra, phản hồi) phù hợp với nhiệm vụ cụ thể.",
      verify: { subseq: "29/29", tuKhoa: "5/5" },
    },
    {
      ma: "10.D2.2",
      chuDe: "D2",
      mach: "D",
      loai: "cốt lõi",
      text: "Nêu được ví dụ về một số vấn đề phát sinh trong quá trình vận hành hoặc tối ưu hoá AI và trình bày được ý nghĩa của việc khắc phục các vấn đề đó.",
      verify: { subseq: "34/34", tuKhoa: "4/4" },
    },
  ],

  /* Chủ đề KHÔNG có YCCĐ lớp 10 — app vẫn hiện để HS thấy toàn cảnh 13 chủ đề */
  khongCoLop10: ["B1", "C1", "C5"],

  /* Tra cứu nhanh theo mã */
  lay(ma){ return this.danhSach.find(x => x.ma === ma) || null; },
  theoChuDe(cd){ return this.danhSach.filter(x => x.chuDe === cd); },
  tenChuDe(cd){ return this.chuDe[cd] || cd; },
};
