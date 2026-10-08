#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tạo Google Sheet quản lý dự án HỌC AI — bản thiết kế v2 (chi tiết).

Sheet cũ (1MxGyHgOD0AK_TZ8chm_XzDl7rINCxVyx9tjpSVEecU0) chứa YCCĐ bản v1 BỊ LỘN CỘT
("vai trò của con động của con hệ thống AI người") -> bỏ, không dùng.
Sheet này lấy YCCĐ từ yccd_lop10_sach.json (đã verify 22/22) và TÍNH LẠI tương phản
màu tại chỗ thay vì chép số, để không có số liệu transcription sai.
"""
import json, os, urllib.request, urllib.parse, sys

TOK = os.environ.get("GOOGLE_TOKEN_JSON") or os.path.expanduser("~/.hermes/google_token.json")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "out", "sheet_thietke.json")

# ---------- tương phản WCAG: TÍNH, không chép ----------
def _lin(c):
    c /= 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

def L(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def ratio(a, b):
    la, lb = L(a), L(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)

NEN_TRANG, NEN_APP, NEN_3D = "#FFFFFF", "#FAF5FF", "#F8FAFC"

MAU = [
    # (vai trò, hex, nền so sánh, ngưỡng cần, ghi chú)
    ("Chữ chính (foreground)", "#1E1B4B", NEN_APP, 4.5, "chữ thường"),
    ("Chữ chính trên thẻ", "#1E1B4B", NEN_TRANG, 4.5, "chữ thường"),
    ("Chữ phụ (muted)", "#475569", NEN_TRANG, 4.5, "chú thích, nhãn"),
    ("Chủ đạo (primary)", "#7C3AED", NEN_TRANG, 4.5, "tiêu đề, liên kết"),
    ("Nhấn dùng cho CHỮ", "#0E7490", NEN_TRANG, 4.5, "accent gốc #0891B2 chỉ 3.68 -> không đạt cho chữ thường"),
    ("NỀN nút hành động chính (chữ trắng)", "#0E7490", "#FFFFFF", 4.5,
     "LỖI ĐÃ SỬA: #0891B2 + chữ trắng chỉ 3.68:1 (tương phản có tính đối xứng; 5.70:1 là cặp chữ ĐEN, không dùng được cho nút chữ trắng)"),
    ("Accent #0891B2 — CHỈ chữ lớn & đồ hoạ", "#0891B2", NEN_TRANG, 3.0,
     "3.68:1 -> đạt ngưỡng 3.0 của chữ lớn (18pt+/14pt bold) và WCAG 1.4.11 cho đồ hoạ; KHÔNG đạt 4.5 cho chữ thường"),
    ("Chữ trắng trên primary", "#FFFFFF", "#7C3AED", 4.5, "nút chính"),
    ("Cảnh báo (destructive)", "#DC2626", NEN_TRANG, 4.5, "thông báo lỗi"),
    ("3D · ảnh BAN NGÀY", "#B45309", NEN_3D, 3.0, "màu cũ #FFD43B chỉ 1.43 -> FAIL"),
    ("3D · ảnh BAN ĐÊM", "#1D4ED8", NEN_3D, 3.0, "màu cũ #4DABF7 chỉ 2.48 -> FAIL"),
    ("3D · AI đoán SAI", "#B91C1C", NEN_3D, 3.0, "màu cũ #FF6B6B chỉ 2.78 -> FAIL"),
    ("3D · AI đoán ĐÚNG", "#15803D", NEN_3D, 3.0, ""),
    ("3D · mặt phẳng quyết định", "#EF4444", NEN_3D, 3.0, "thành phần đồ hoạ"),
    ("3D · lưới toạ độ", "#CBD5E1", NEN_3D, 1.0, "chỉ trang trí, KHÔNG mang thông tin"),
]


def build():
    # ================= TAB 1: Tổng quan =================
    tong = [
        ["HỌC AI — THIẾT KẾ TỔNG QUAN & QUẢN LÝ DỰ ÁN (v2)"],
        ["Lập", "04/10/2026", "Thay thế sheet cũ (bản YCCĐ v1 bị lộn cột)"],
        ["Khẩu hiệu", "Soi AI để hiểu AI", "Học sinh không hỏi AI — học sinh bắt lỗi AI"],
        ["Repo", "github.com/mxuanvan02/soi-ai-lop10", "public"],
        ["Website", "https://mxuanvan02.github.io/soi-ai-lop10/", "đã verify HTTP 200 + nội dung đúng"],
        ["Tài liệu thiết kế", "THIET_KE_TONG_QUAN.md — thư mục làm việc cha, NGOÀI repo", "30 KB, 8 phần"],
        ["Design system", "soi-ai/design-system/soi-ai/MASTER.md", "sinh bởi ui-ux-pro-max (repo ai-agent-tools của anh Văn)"],
        ["Chuẩn viết nội dung", "academic-prose (repo ai-agent-tools)", "giữ lực nhận thức, tránh văn phong quảng cáo"],
        [""],
        ["RÀNG BUỘC CHI PHỐI THIẾT KẾ (không được vi phạm)"],
        ["1", "Không yêu cầu HS có tài khoản cá nhân", "CV 5588/BGDĐT-GDPT"],
        ["2", "Không tạo phụ thuộc nhà cung cấp", "CV 5588 -> cấm Supabase/Firebase"],
        ["3", "Không buộc mua tài khoản/thiết bị/dịch vụ", "CV 5588"],
        ["4", "Ưu tiên mã nguồn mở, có bản ngoại tuyến/in ấn", "CV 5588"],
        ["5", "KHÔNG xác lập đầu điểm riêng cho nội dung GD AI", "Khung 2422 phần VI -> chỉ 'mức độ đáp ứng'"],
        ["6", "Không suy rộng năng lực từ 1 sản phẩm/1 lần làm", "Khung 2422 phần VI -> ghi rõ giới hạn"],
        ["7", "Có phương án không dùng thiết bị / thiết bị dùng chung", "Khung 2422 phần VI -> phiếu in + mô hình giấy"],
        ["8", "Chạy được trên file:// (USB, máy yếu, mất mạng)", "thực tế phòng lab trường VN"],
        ["9", "Chỉ lưu mã ẩn danh, không họ tên/ảnh", "Luật BV dữ liệu cá nhân 91/2025/QH15"],
        [""],
        ["MỐC CỨNG"],
        ["Giải đáp trực tuyến BTC", "09h00 CN 11/10/2026", "https://ieeai.net/hoidap"],
        ["HẠN NỘP", "23h59 (GMT+7) CN 25/10/2026", "apps.rmit.edu.vn/r/nopsanphamGTTP2026"],
        ["Công bố sơ tuyển", "15/11/2026", "Top 50 -> hỗ trợ 3.000.000đ"],
        ["Chung kết", "05/12/2026 (dự kiến)", "ĐH RMIT VN, Nam Sài Gòn"],
        [""],
        ["HỒ SƠ NỘP (mỗi GV tối đa 1 sản phẩm cá nhân)"],
        ["Slide", "tối đa 15", "CẦN file mẫu BTC"],
        ["Video", "tối đa 5 phút", "cần cảnh dạy thật"],
        ["Poster", "theo mẫu BTC", "CẦN file mẫu BTC"],
        [""],
        ["VĂN BẢN CĂN CỨ (đã đọc bản gốc)"],
        ["QĐ 2422/QĐ-BGDĐT", "18/08/2026", "Khung GD AI — research/src/2422_PL_khung.pdf"],
        ["QĐ 3439/QĐ-BGDĐT", "18/02/2026", "Khung THÍ điểm — file tải về là HTML, chỉ dùng nguồn phụ"],
        ["CV 5588/BGDĐT-GDPT", "19/08/2026", "Hướng dẫn triển khai — research/notes/01_policy.md"],
        ["CV 1875/NGCBQLGD-PTNGCB", "01/10/2026", "Phát động giải thưởng"],
        ["Luật An ninh mạng", "24/2018/QH14", "sửa đổi bởi 116/2025/QH15"],
        ["Luật Dữ liệu", "60/2024/QH15", "hiệu lực 1/7/2025"],
        ["Luật BV dữ liệu cá nhân", "91/2025/QH15", "hiệu lực 1/1/2026"],
        ["Luật Trí tuệ nhân tạo", "134/2025/QH15", "hiệu lực 1/3/2026"],
    ]

    # ================= TAB 2: Chức năng =================
    func = [
        ["#", "Khung nhìn", "Người dùng", "Chức năng", "YCCĐ phủ", "Minh chứng ghi lại", "Trạng thái"],
        [1, "Vào lớp", "HS", "Nhập mã HS + mã lớp do GV phát. Không đăng ký, không email, không SĐT.",
         "—", "mã HS, mã lớp, thời điểm", "ĐÃ CÓ"],
        [2, "Xưởng huấn luyện 2D", "HS", "Tạo bộ ảnh (canvas) -> perceptron học thật -> phát hiện thiên kiến ngày/đêm -> sửa bằng dữ liệu cân bằng -> 4 nhiệm vụ phân tích",
         "10.C4.1, 10.D2.2, 10.B3.1", "số lần huấn luyện, tỉ lệ đúng tách ngày/đêm, đáp án 4 nhiệm vụ", "ĐÃ CÓ"],
        [3, "Phòng 3D — Soi mô hình", "HS", "Đám mây điểm 4 đặc trưng + mặt phẳng quyết định từ trọng số thật; kéo tỉ lệ ngày; huấn luyện từng vòng; đánh giá bộ ảnh mới; chế độ nhẹ; fallback 2D",
         "10.C4.1, 10.C5, 10.D2.2", "epoch, trọng số, kết quả tách nhóm", "ĐANG DỰNG — chưa kiểm chứng toán mặt phẳng"],
        [4, "Ống dẫn 3D — Soi luồng AI", "HS", "5 trạm + hạt dữ liệu chảy; hệ làm hỏng NGẪU NHIÊN 1 trạm; HS đoán; bấm trạm xem vai trò & hậu quả; fallback bảng chữ",
         "10.D1.1, 10.D2.1, 10.A1.2", "trạm hỏng, trạm HS đoán, đúng/sai", "ĐANG DỰNG — CHƯA TEST LẦN NÀO"],
        [5, "Đấu trường soi lỗi", "HS", "78 câu; 5 nhóm lỗi (bịa số liệu / nguồn không tồn tại / thiên kiến / suy luận sai / xui lộ dữ liệu cá nhân); chế độ luyện + pre + post",
         "10.B2.MR1", "phán quyết, nhóm lỗi chọn, recall theo nhóm", "ĐÃ CÓ"],
        [6, "Kiến thức nền + prompt", "HS", "4 luật VN; ứng dụng AI theo tính năng; AI tạo sinh vs phân loại; tiêu chí prompt; 3 bài thực hành prompt chấm rubric",
         "10.A3.1, 10.C2.2, 10.C3.1, 10.C3.2, 10.C3.3", "kết quả quiz, rubric prompt", "ĐÃ CÓ (v0.4.0)"],
        [7, "Lôgic & AI — Bài 5 Tin 10", "HS", "Dữ liệu lôgic, AND/OR/NOT, bảng chân lí, bảng nhầm lẫn; nối dấu so sánh z>=0 với trọng số HỌC được",
         "nối Bài 5 CT GDPT", "kết quả bài tập lôgic", "ĐÃ CÓ (v0.3.0)"],
        [8, "Bản đồ năng lực", "HS + GV", "13 chủ đề QĐ 2422 làm trục chính; UNESCO là cột đối chiếu; 3 chủ đề không có YCCĐ lớp 10 hiển thị mờ; CHỈ 'mức độ đáp ứng', không điểm",
         "tổng hợp", "mức đáp ứng từng chủ đề", "ĐÃ ĐỔI TRỤC (v1.0.0)"],
        [9, "Báo cáo lớp + xuất minh chứng", "GV", "Tổng hợp nhiều HS; xuất CSV/JSON; nút xoá dữ liệu",
         "Khung VI#2", "tệp CSV có timestamp", "ĐÃ CÓ"],
        [10, "Phiếu khai báo sử dụng AI", "HS", "Sinh phiếu từ nhật ký: công cụ / mục đích / phạm vi AI hỗ trợ / phần HS tự làm / cách kiểm chứng",
         "Khung 2422 (chữ nguyên văn)", "phiếu in/nộp", "CHƯA LÀM — chưa sản phẩm nào có"],
        [11, "Tự đánh giá + đánh giá đồng đẳng", "HS", "Rubric có sẵn, hệ vẫn chấm được; HS chấm chéo sản phẩm nhóm (tiết 10-11)",
         "Khung VI (khuyến khích)", "rubric đã chấm", "CHƯA LÀM"],
        [12, "Đồng bộ nhật ký lên máy chủ", "GV", "POST 1 sự kiện/lần; lỗi thì im lặng rơi về localStorage; KHÔNG bao giờ chặn HS làm bài",
         "—", "log tập trung", "TUỲ CHỌN — chờ anh Văn quyết"],
    ]

    # ================= TAB 3: Mô phỏng =================
    mo = [
        ["#", "Mô phỏng", "Trạng thái", "YCCĐ phủ", "Cơ chế tự chấm (không cần người kiểm chứng)", "Ưu tiên"],
        [1, "Perceptron học thật, trọng số đổi theo lỗi", "ĐÃ CÓ", "10.C4.1, 10.C5", "nhãn ảnh có sẵn, đối chiếu dự đoán", "—"],
        [2, "Thiên kiến dữ liệu ngày/đêm", "ĐÃ CÓ", "10.C4.1, 10.D2.2, 10.B3.1", "bộ kiểm tra tách nhóm, khác seed", "—"],
        [3, "Mặt phẳng quyết định trong không gian 3D", "ĐANG DỰNG", "10.C4.1, 10.C5", "suy từ trọng số thật; kiểm bằng số", "P2"],
        [4, "Ống dẫn 5 trạm, đoán trạm hỏng", "ĐANG DỰNG", "10.D1.1, 10.D2.1, 10.A1.2", "hệ chọn ngẫu nhiên -> đáp án biết trước", "P2"],
        [5, "Bắt lỗi nội dung AI tạo sinh (5 nhóm)", "ĐÃ CÓ", "10.B2.MR1", "lỗi cài sẵn, nhãn cứng", "—"],
        [6, "Thực hành viết prompt theo rubric", "ĐÃ CÓ", "10.C3.1, 10.C3.2", "rubric từ khoá, tất định", "—"],
        [7, "Phân biệt AI tạo sinh và AI phân loại", "ĐÃ CÓ", "10.C3.3", "nhiều lựa chọn có nhãn", "—"],
        [8, "Quy định pháp luật bảo vệ người dùng", "ĐÃ CÓ", "10.A3.1", "có nhãn; số hiệu luật đã kiểm chứng", "—"],
        [9, "Bảng nhầm lẫn và chỉ số đánh giá", "ĐÃ CÓ", "10.D2.2", "tính từ phán quyết của HS", "—"],
        [10, "Dữ liệu lôgic, phép AND/OR/NOT", "ĐÃ CÓ", "nối Bài 5 Tin 10", "bảng chân lí có nhãn", "—"],
        [11, "Học tủ: tách dữ liệu huấn luyện/kiểm tra", "CHƯA LÀM", "10.C4.1, 10.C5", "hai bộ khác seed, so độ chính xác", "P3-CAO"],
        [12, "Quá khớp và dưới khớp", "CHƯA LÀM", "10.C5, 10.D2.2", "đường cong lỗi theo số vòng", "P3-CAO"],
        [13, "Dạng dữ liệu: ảnh, âm thanh, văn bản", "CHƯA LÀM", "10.C4.MR1", "phân loại mẫu có nhãn", "P3"],
        [14, "Vai trò con người trong vận hành hệ AI", "CHƯA LÀM", "10.A1.1, 10.A1.2", "tình huống quyết định có nhãn", "P3-CAO"],
        [15, "Rủi ro của sản phẩm AI với người và xã hội", "CHƯA LÀM", "10.A2.1, 10.A2.MR1", "tình huống có nhãn", "P3-CAO"],
        [16, "Hành vi dùng AI vi phạm quy định nhà trường", "CHƯA LÀM", "10.B2.1", "tình huống có nhãn", "P3-CAO"],
        [17, "Chọn vấn đề Việt Nam để ứng dụng AI", "CHƯA LÀM", "10.C2.1", "rubric tiêu chí, tất định", "P3"],
        [18, "Ứng dụng AI theo tính năng hệ thống", "CHƯA LÀM", "10.C2.2", "phân nhóm có nhãn", "P3"],
        [19, "Yêu cầu cần có khi ứng dụng AI cho nhiệm vụ", "CHƯA LÀM", "10.C2.MR1", "checklist có nhãn", "P3"],
        [20, "Công nghệ để thiết kế và tạo AI", "CHƯA LÀM", "10.C3.MR1", "câu hỏi có nhãn", "P3"],
        ["", "GIỚI HẠN TRUNG THỰC: 10.C2.MR2 (sử dụng được ứng dụng AI trong học tập) và phần thực hành đầy đủ của 10.C3.2 cần AI thật + mạng -> KHÔNG mô phỏng được ngoại tuyến. Xử lý: ghi rõ phạm vi ở chế độ offline, mở khoá ở chế độ online.", "", "", "", ""],
    ]

    # ================= TAB 4: YCCĐ (đã verify) =================
    _r = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    yc = json.load(open(os.path.join(_r, "data-source", "yccd_lop10_sach.json")))
    yccd = [["Mã", "Chủ đề", "Mạch", "Loại", "Nguyên văn (đã verify)", "subseq", "từ khoá", "Sản phẩm phủ ở đâu", "Mức phủ"]]
    # ánh xạ mức phủ theo thiết kế v2
    PHU = {
        "10.A1.1": ("Mô phỏng #14 (chưa làm)", "CHƯA PHỦ"),
        "10.A1.2": ("Ống dẫn 3D + Mô phỏng #14", "MỘT PHẦN"),
        "10.A2.1": ("Mô phỏng #15 (chưa làm)", "CHƯA PHỦ"),
        "10.A2.MR1": ("Mô phỏng #15 (chưa làm)", "CHƯA PHỦ"),
        "10.A3.1": ("Kiến thức nền — 4 luật VN", "PHỦ"),
        "10.B2.1": ("Mô phỏng #16 (chưa làm)", "CHƯA PHỦ"),
        "10.B2.MR1": ("Đấu trường soi lỗi (78 câu)", "PHỦ MẠNH"),
        "10.B3.1": ("Xưởng huấn luyện + Phòng 3D", "PHỦ MẠNH"),
        "10.C2.1": ("Mô phỏng #17 (chưa làm)", "CHƯA PHỦ"),
        "10.C2.2": ("Kiến thức nền — ứng dụng theo tính năng", "PHỦ"),
        "10.C2.3": ("Đấu trường + Bài 5 (AI hỗ trợ học tập)", "MỘT PHẦN"),
        "10.C2.MR1": ("Mô phỏng #19 (chưa làm)", "CHƯA PHỦ"),
        "10.C2.MR2": ("KHÔNG THỂ ngoại tuyến — cần AI thật + mạng", "NGOÀI PHẠM VI"),
        "10.C3.1": ("Kiến thức nền — tiêu chí prompt", "PHỦ"),
        "10.C3.2": ("3 bài thực hành prompt chấm rubric", "PHỦ"),
        "10.C3.3": ("Kiến thức nền — bảng so sánh", "PHỦ"),
        "10.C3.MR1": ("Mô phỏng #20 (chưa làm)", "CHƯA PHỦ"),
        "10.C4.1": ("Xưởng huấn luyện + Phòng 3D", "PHỦ MẠNH"),
        "10.C4.MR1": ("Mô phỏng #13 (chưa làm)", "CHƯA PHỦ"),
        "10.D1.1": ("Ống dẫn 3D — 5 trạm", "PHỦ"),
        "10.D2.1": ("Ống dẫn 3D — thành phần hệ thống", "PHỦ"),
        "10.D2.2": ("Xưởng huấn luyện + bảng nhầm lẫn", "PHỦ MẠNH"),
    }
    for r in yc:
        v = r.get("verify", {})
        p = PHU.get(r["ma"], ("?", "?"))
        yccd.append([r["ma"], r.get("chuDe", ""), r["ma"][3], r.get("loai", ""),
                     r["text"], v.get("subseq", ""), v.get("tuKhoa", ""), p[0], p[1]])

    # ================= TAB 5: Design system =================
    ds = [["Vai trò", "Hex", "Nền so sánh", "Tỉ lệ tương phản (TÍNH LẠI)", "Ngưỡng cần", "Kết luận", "Ghi chú"]]
    for vai, hexm, nen, nguong, note in MAU:
        # chữ trắng trên nền màu đó (nếu là nền nút)
        if "NỀN nút" in vai:
            r = ratio("#FFFFFF", hexm)
        else:
            r = ratio(hexm, nen)
        ket = "ĐẠT" if r >= nguong else "KHÔNG ĐẠT"
        if "trang trí" in note:
            ket = "chỉ trang trí"
        ds.append([vai, hexm, nen, round(r, 2), nguong, ket, note])

    ds += [
        [""],
        ["QUYẾT ĐỊNH VỀ 4 XUNG ĐỘT GIỮA MASTER.md VÀ RÀNG BUỘC SẢN PHẨM"],
        ["Xung đột", "MASTER.md đề xuất", "Vấn đề (đã kiểm chứng)", "Quyết định"],
        ["Phông chữ", "Inter qua @import Google Fonts",
         "Phép thử tải thật: CSS 916 byte, 0 subset tiếng Việt; và gọi mạng trái ràng buộc ngoại tuyến",
         "Dùng chuỗi phông hệ thống: Inter, Segoe UI, system-ui, DejaVu Sans. Máy trường Windows luôn có Segoe UI phủ tiếng Việt."],
        ["Màu 3D", "kế thừa bảng màu nền tối",
         "Đo WCAG: vàng #FFD43B = 1.43:1, xanh #4DABF7 = 2.48:1, đỏ #FF6B6B = 2.78:1 — đều dưới 3.0:1",
         "Đổi sang bảng màu đã đo ở trên (mọi cặp >= 3.0:1, phần lớn >= 4.5:1)"],
        ["Biểu tượng", "cấm emoji-as-icon, dùng SVG nhất quán",
         "App hiện dùng emoji ở hầu hết nút",
         "Thay bằng SVG nội tuyến Lucide (giấy phép ISC, đã verify tải được), lưu vendor/lucide/. Emoji chỉ còn trong văn bản thân thiện."],
        ["Màu nhấn", "#0891B2",
         "Đo được 3.68:1 trên nền trắng — dưới 4.5:1 cho chữ thường",
         "Giữ #0891B2 làm NỀN nút (chữ trắng đạt 5.70:1); dùng #0E7490 (5.36:1) khi là chữ"],
        [""],
        ["DANH SÁCH KIỂM TRƯỚC KHI BÀN GIAO (từ skill)"],
        ["[ ] Không dùng emoji làm biểu tượng"],
        ["[ ] Biểu tượng cùng một bộ (Lucide)"],
        ["[ ] cursor:pointer trên mọi phần tử bấm được"],
        ["[ ] Hover có chuyển tiếp 150-300ms"],
        ["[ ] Chữ thường tương phản >= 4.5:1"],
        ["[ ] Focus state nhìn thấy được (bàn phím)"],
        ["[ ] Tôn trọng prefers-reduced-motion"],
        ["[ ] Responsive 375 / 768 / 1024 / 1440"],
        ["[ ] Không nội dung bị navbar che"],
        ["[ ] Không scroll ngang trên mobile"],
        ["[ ] NỀN SÁNG đúng yêu cầu anh Văn"],
        ["[ ] Chạy được trên file:// (không mạng)"],
    ]

    # ================= TAB 6: Tasks =================
    tasks = [
        ["ID", "Giai đoạn", "Việc", "Tiêu chí nghiệm thu (đo được)", "Trạng thái", "Bắt đầu", "Hạn", "Người làm", "Ghi chú"],
        # P0 đã xong
        ["P0-1", "0. Nghiên cứu", "Đọc Khung 2422 lớp 10 + mục Đánh giá", "Trích đúng 22 YCCĐ", "XONG", "04/10", "04/10", "Agent", ""],
        ["P0-2", "0. Nghiên cứu", "Verify 22 YCCĐ bằng 4 phép kiểm", "22/22 đạt (subseq + ô đặc hiệu + từ khoá + tập mã)", "XONG", "04/10", "04/10", "Agent", "6 lần thất bại trước đã ghi trong docstring"],
        ["P0-3", "0. Nghiên cứu", "Verify số hiệu 5 luật VN", "khớp cổng văn bản Chính phủ", "XONG", "04/10", "04/10", "Agent", ""],
        ["P0-4", "0. Nghiên cứu", "Probe three.js trên file://", "REVISION=137, render OK", "XONG", "04/10", "04/10", "Agent", ""],
        ["P0-5", "0. Nghiên cứu", "Pull repo ai-agent-tools + đọc 2 skill", "ui-ux-pro-max, academic-prose", "XONG", "04/10", "04/10", "Agent", "~/ai-agent-tools"],
        ["P0-6", "0. Nghiên cứu", "Sinh + persist MASTER.md", "design-system/soi-ai/MASTER.md", "XONG", "04/10", "04/10", "Agent", ""],
        ["P0-7", "0. Nghiên cứu", "Đo tương phản WCAG toàn bảng màu", "mọi cặp có số đo thật", "XONG", "04/10", "04/10", "Agent", "phát hiện 4 xung đột"],
        ["P0-8", "0. Nghiên cứu", "Viết THIẾT KẾ TỔNG QUAN v2", "8 phần, 30KB", "XONG", "04/10", "04/10", "Agent", ""],
        ["P0-9", "1. Nền móng", "Tạo repo + deploy GitHub Pages", "HTTP 200 + nội dung đúng", "XONG", "04/10", "04/10", "Agent", "commit 5c46f41"],
        ["P0-10", "1. Nền móng", "Đổi trục bản đồ sang 13 chủ đề Bộ", "13 chủ đề A1-D2 hiển thị", "XONG", "04/10", "04/10", "Agent", "đã verify trên link công khai"],
        ["P0-11", "1. Nền móng", "Bỏ ngôn ngữ điểm số -> mức độ đáp ứng", "không còn 'điểm' ở UI kết quả", "XONG", "04/10", "04/10", "Agent", "còn 1 lần trong câu phủ định"],
        # P1
        ["P1-1", "1. Hoàn tất 3D", "Kiểm chứng toán mặt phẳng 4D->3D bằng số", "mặt phẳng tách đúng 2 cụm; dự đoán khớp engine.dudoan 100%", "CHƯA LÀM", "04/10", "05/10", "Agent", "chỗ dễ sai nhất"],
        ["P1-2", "1. Hoàn tất 3D", "Test scene ống dẫn end-to-end", "hỏng ngẫu nhiên -> đoán -> chấm đúng; log ghi được", "CHƯA LÀM", "05/10", "05/10", "Agent", "CHƯA TEST LẦN NÀO"],
        ["P1-3", "1. Hoàn tất 3D", "Sửa text giải thích khớp số đo thật", "nói đúng cơ chế 'đoán hằng số', không nói 'sai gần nửa'", "CHƯA LÀM", "05/10", "05/10", "Agent", "phát hiện từ số đo 59%"],
        ["P1-4", "1. Hoàn tất 3D", "Test nút Đánh giá theo đường bấm UI", "bấm nút -> KPI hiện đủ 3 ô", "CHƯA LÀM", "05/10", "05/10", "Agent", "trước đó chỉ test hàm"],
        ["P1-5", "1. Hoàn tất 3D", "Hiển thị rõ số vòng cộng dồn khi bấm lại", "epoch hiển thị đúng ngữ cảnh", "CHƯA LÀM", "05/10", "05/10", "Agent", "đo được 77 thay vì 60"],
        # P2
        ["P2-1", "2. Giao diện sáng", "Thay bảng màu theo tab Design system", "mọi cặp >= ngưỡng, đo lại bằng script", "CHƯA LÀM", "05/10", "07/10", "Agent", ""],
        ["P2-2", "2. Giao diện sáng", "Vendor Lucide SVG, thay emoji ở nút điều khiển", "0 emoji làm icon; file svg nằm trong repo", "CHƯA LÀM", "06/10", "08/10", "Agent", "ISC license"],
        ["P2-3", "2. Giao diện sáng", "Đổi nền cảnh 3D sang sáng + màu dữ liệu mới", "4 màu dữ liệu >= 3.0:1 trên nền #F8FAFC", "CHƯA LÀM", "07/10", "08/10", "Agent", ""],
        ["P2-4", "2. Giao diện sáng", "Bỏ @import font mạng, dùng phông hệ thống", "không còn request ra ngoài khi mở file://", "CHƯA LÀM", "05/10", "05/10", "Agent", ""],
        ["P2-5", "2. Giao diện sáng", "Focus state + prefers-reduced-motion + cursor:pointer", "checklist 4.4 đạt hết", "CHƯA LÀM", "08/10", "09/10", "Agent", ""],
        ["P2-6", "2. Giao diện sáng", "Test responsive 375/768/1024/1440", "không scroll ngang, không che nội dung", "CHƯA LÀM", "09/10", "09/10", "Agent", ""],
        # P3
        ["P3-1", "3. Mở rộng mô phỏng", "Mô phỏng #11 học tủ (tách train/test)", "2 bộ khác seed, so độ chính xác, tự chấm", "CHƯA LÀM", "09/10", "11/10", "Agent", "P3-CAO"],
        ["P3-2", "3. Mở rộng mô phỏng", "Mô phỏng #12 quá khớp/dưới khớp", "đường cong lỗi theo số vòng", "CHƯA LÀM", "09/10", "11/10", "Agent", "P3-CAO"],
        ["P3-3", "3. Mở rộng mô phỏng", "Mô phỏng #14 vai trò con người", "tình huống có nhãn", "CHƯA LÀM", "11/10", "13/10", "Agent", "P3-CAO"],
        ["P3-4", "3. Mở rộng mô phỏng", "Mô phỏng #15 rủi ro sản phẩm AI", "tình huống có nhãn", "CHƯA LÀM", "11/10", "13/10", "Agent", "P3-CAO"],
        ["P3-5", "3. Mở rộng mô phỏng", "Mô phỏng #16 vi phạm quy định nhà trường", "tình huống có nhãn", "CHƯA LÀM", "13/10", "14/10", "Agent", "P3-CAO"],
        ["P3-6", "3. Mở rộng mô phỏng", "Chức năng #10 phiếu khai báo sử dụng AI", "sinh phiếu từ log, in được", "CHƯA LÀM", "13/10", "15/10", "Agent", "độc đáo, chưa sản phẩm nào có"],
        ["P3-7", "3. Mở rộng mô phỏng", "Chức năng #11 tự đánh giá + đồng đẳng", "rubric có sẵn, hệ chấm được", "CHƯA LÀM", "15/10", "16/10", "Agent", "Khung VI khuyến khích"],
        ["P3-8", "3. Mở rộng mô phỏng", "Mô phỏng #13,#17,#18,#19,#20", "mỗi cái có nhãn tự chấm", "NẾU KỊP", "16/10", "19/10", "Agent", "nhóm thấp hơn"],
        # P4
        ["P4-1", "4. Dạy thật", "Anh chốt NGÀY DẠY", "có ngày cụ thể", "CHỜ ANH", "04/10", "06/10", "Anh Văn", "NÚT THẮT CỔ CHAI"],
        ["P4-2", "4. Dạy thật", "Dạy Bài 5 Dữ liệu lôgic (Tin 10)", "log có timestamp của lớp thật", "CHỜ", "", "", "Anh Văn", "giáo án 2 tiết sẵn"],
        ["P4-3", "4. Dạy thật", "Dạy pilot 4 tiết chuyên đề AI", "tiết 6,7,8,10 theo kế hoạch 12 tiết", "CHỜ", "13/10", "19/10", "Anh Văn", ""],
        ["P4-4", "4. Dạy thật", "Anh duyệt nhãn 56 câu hỏi", "checklist_duyet_nhan.html xong 100%", "CHỜ ANH", "04/10", "06/10", "Anh Văn", ""],
        ["P4-5", "4. Dạy thật", "Gom log + tính pre/post", "ra con số thật cho slide", "CHỜ", "19/10", "20/10", "Agent", "tools/gop_csv.py"],
        ["P4-6", "4. Dạy thật", "Quay video + chụp ảnh lớp học", "có cảnh dạy thật", "CHỜ", "", "", "Anh Văn", "ĐIỀU KIỆN THỂ LỆ"],
        # P5
        ["P5-1", "5. Hồ sơ", "Anh tải 2 file mẫu BTC (slide + poster)", "gửi được cho Agent", "CHỜ ANH", "04/10", "18/10", "Anh Văn", "máy Agent lỗi certificate"],
        ["P5-2", "5. Hồ sơ", "Dựng 15 slide", "dẫn YCCĐ bằng mã Bộ; đúng mẫu", "CHỜ", "20/10", "22/10", "Agent", ""],
        ["P5-3", "5. Hồ sơ", "Dựng video <= 5 phút", "có cảnh dạy thật + màn hình 3D", "CHỜ", "20/10", "22/10", "Agent + Anh", ""],
        ["P5-4", "5. Hồ sơ", "Poster A0 theo mẫu", "đúng khổ, đúng font mẫu", "CHỜ", "21/10", "22/10", "Agent", ""],
        ["P5-5", "5. Hồ sơ", "Rà pháp lý + dọn ghi chú nội bộ", "không còn placeholder/ghi chú vận hành", "CHỜ", "23/10", "23/10", "Agent", "quy tắc của anh Văn"],
        ["P5-6", "5. Hồ sơ", "Đệm dự phòng", "—", "CHỜ", "24/10", "24/10", "—", ""],
        # P6
        ["P6-1", "6. Nộp bài", "Dự giải đáp trực tuyến 09h00 11/10", "hỏi rõ tiêu chí chấm Bảng B", "CHỜ", "11/10", "11/10", "Anh Văn", "ieeai.net/hoidap"],
        ["P6-2", "6. Nộp bài", "Nộp tại apps.rmit.edu.vn TRƯỚC 12h00 25/10", "có xác nhận nộp", "CHỜ", "25/10", "25/10", "Anh Văn", "Agent không bấm hộ cổng trường"],
        # Tuỳ chọn
        ["P7-1", "7. TUỲ CHỌN", "Backend log tập trung trên máy fleet", "3 endpoint, HTTPS, không chặn HS", "CHỜ ANH", "", "", "Agent + Anh", "không chặn tiến độ"],
    ]

    # ================= TAB 7: Rủi ro =================
    rr = [
        ["Rủi ro", "Mức", "Hậu quả", "Phòng / chống", "Trạng thái"],
        ["Không kịp DẠY THẬT trước 20/10", "CAO NHẤT", "Mất điều kiện thể lệ 'đã triển khai thực tế trong lớp học' -> rớt sơ tuyển",
         "Anh chốt ngày ngay; nếu chưa xếp được tiết chuyên đề thì dạy lồng Bài 5 Tin 10 (giáo án sẵn) vẫn tính là triển khai", "CHỜ ANH"],
        ["Cảnh ống dẫn 3D chưa test lần nào", "CAO", "Hỏng khi demo trước giám khảo",
         "P1-2 test end-to-end trước 05/10; luôn có fallback bảng chữ", "ĐÃ LÊN LỊCH"],
        ["Toán mặt phẳng 4D->3D có thể sai", "CAO", "HS thấy mặt phẳng không tách đúng cụm -> mất niềm tin vào mô phỏng",
         "P1-1 kiểm chứng bằng số: so dự đoán từ mặt phẳng với engine.dudoan trên toàn bộ điểm", "ĐÃ LÊN LỊCH"],
        ["3D lag trên máy trường yếu", "CAO", "HS không dùng được", "fallback 2D tự động; chế độ nhẹ; <=60 hạt; antialias tắt; pixelRatio<=2", "ĐÃ CÓ PHƯƠNG ÁN"],
        ["Đổi sang nền sáng làm mất tương phản đồ hoạ", "TRUNG", "Vi phạm WCAG 1.4.11", "đã đo và chốt bảng màu mới, mọi cặp >= 3.0:1", "ĐÃ GIẢI QUYẾT"],
        ["Font Google không có subset tiếng Việt", "TRUNG", "Chữ tiếng Việt hiển thị xấu/rơi font", "dùng phông hệ thống (Segoe UI trên Windows trường)", "ĐÃ GIẢI QUYẾT"],
        ["21 ngày cho 3D + UI sáng + 10 mô phỏng mới + dạy + hồ sơ", "TRUNG", "Nộp trễ hoặc hồ sơ mỏng",
         "P3-8 đánh dấu 'NẾU KỊP'; ưu tiên 6 mô phỏng P3-CAO phủ YCCĐ cốt lõi đang trống", "ĐÃ THU HẸP"],
        ["File mẫu BTC không tải được", "TRUNG", "Slide/poster sai định dạng -> trừ điểm", "Cần anh tải giúp (máy Agent lỗi certificate với apps.rmit.edu.vn)", "CHỜ ANH"],
        ["Giám khảo nghi 'nhờ làm thay'", "TRUNG", "Bị loại vì quy định 'không nhờ làm thay'",
         "Git history công khai từng commit nhỏ + video quay lúc dạy thật + phiếu khai báo rõ AI hỗ trợ phần nào", "ĐÃ TÍNH"],
        ["Sheet cũ chứa YCCĐ bản lộn cột", "THẤP", "Nếu ai đọc sheet cũ sẽ thấy văn bản sai",
         "Sheet này thay thế; sheet cũ ghi rõ đã loại bỏ ở dòng 2 tab Tổng quan", "ĐÃ XỬ LÝ"],
        ["Host cloud nước ngoài (Supabase/Firebase)", "—", "Vi phạm tinh thần CV 5588 + dữ liệu HS VN ở server nước ngoài",
         "ĐÃ LOẠI — chỉ GitHub Pages tĩnh + backend tự chủ nếu cần", "ĐÃ QUYẾT"],
    ]

    # ================= TAB 8: Quyết định cần anh =================
    qd = [
        ["#", "Cần anh quyết", "Vì sao Agent không tự quyết", "Khuyến nghị của Agent", "Ảnh hưởng nếu trễ"],
        [1, "Chốt NGÀY DẠY Bài 5 + 4 tiết chuyên đề", "Lịch trường và phân công tiết thuộc thẩm quyền của anh",
         "Dạy càng sớm càng tốt, chậm nhất 19/10 để kịp dựng video 20-22/10", "MẤT điều kiện thể lệ 'đã triển khai' -> rớt sơ tuyển"],
        [2, "Duyệt nhãn 56 câu hỏi (ho-so/checklist_duyet_nhan.html)", "Nhãn là trách nhiệm chuyên môn của tác giả, Agent không tự xác nhận",
         "Duyệt trước 06/10 để kịp đưa vào bản dạy thật", "Không được dùng 56 câu đó khi dạy -> ngân hàng mỏng đi"],
        [3, "Tải 2 file mẫu BTC (slide + poster)", "Máy Agent lỗi certificate với apps.rmit.edu.vn",
         "Tải trước 18/10", "Slide/poster sai mẫu -> trừ điểm hình thức"],
        [4, "Tên sản phẩm 'SOI AI' — giữ hay đổi?", "Đặt tên là quyết định của tác giả",
         "Giữ SOI AI: thuần Việt 1 âm tiết, đúng cơ chế 'soi lỗi', làm khẩu hiệu được", "Đổi tên muộn phải sửa repo/domain/slide"],
        [5, "Có dựng backend log tập trung trên máy fleet không?", "Liên quan hạ tầng và quyền riêng tư dữ liệu HS",
         "Chưa cần cho hạn 25/10; localStorage + xuất CSV đã đủ minh chứng", "Không ảnh hưởng tiến độ"],
        [6, "Tông sáng: giữ tím-chủ đạo #7C3AED hay đổi sang xanh giáo dục?", "Sở thích thẩm mỹ của anh",
         "Giữ tím (MASTER.md đã chọn, đạt 5.70:1, đúng chất 'AI'); nền #FAF5FF rất nhạt nên vẫn 'trắng sáng'", "Đổi muộn phải đo lại toàn bộ tương phản"],
    ]

    return {
        "Tổng quan": tong,
        "Chức năng": func,
        "Mô phỏng": mo,
        "YCCĐ lớp 10": yccd,
        "Design system": ds,
        "Tasks": tasks,
        "Rủi ro": rr,
        "Cần anh quyết": qd,
    }


def access_token():
    d = json.load(open(TOK))
    body = urllib.parse.urlencode({
        "client_id": d["client_id"], "client_secret": d["client_secret"],
        "refresh_token": d["refresh_token"], "grant_type": "refresh_token"}).encode()
    r = urllib.request.urlopen(urllib.request.Request(d["token_uri"], data=body), timeout=30)
    return json.loads(r.read())["access_token"]


def api(method, url, tok, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + tok)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        return json.loads(urllib.request.urlopen(req, timeout=120).read())
    except urllib.error.HTTPError as e:
        print("HTTP", e.code, e.read().decode()[:500])
        raise


# Sheet đã tạo lần chạy trước — CẬP NHẬT vào đó thay vì tạo mới,
# để anh Văn không phải quản lý 2 file. Đổi thành None nếu muốn tạo sheet mới.
SID_HIENTAI = "1SzJwN1Pt3CQwxfS5QJP3SP6t_cR23ZZOuLRJIMM4sSU"


def main():
    tabs = build()
    tok = access_token()

    if SID_HIENTAI:
        sid = SID_HIENTAI
        meta = api("GET", f"https://sheets.googleapis.com/v4/spreadsheets/{sid}"
                        "?fields=spreadsheetUrl,sheets.properties.title,sheets.properties.gridProperties.rowCount,"
                        "sheets.properties.gridProperties.columnCount", tok)
        url = meta.get("spreadsheetUrl")
        co = [s["properties"]["title"] for s in meta["sheets"]]
        print("Cập nhật sheet có sẵn:", sid)
        print("  tab hiện có:", co)

        # xoá dữ liệu cũ ở các tab trùng tên (clearValues) để không sót dòng thừa
        ranges = [f"'{t}'!A1:ZZ500" for t in tabs if t in co]
        if ranges:
            api("POST", f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values:batchClear",
                tok, {"ranges": ranges})
            print("  đã clear", len(ranges), "tab")

        # tạo tab còn thiếu
        thieu = [t for t in tabs if t not in co]
        if thieu:
            api("POST", f"https://sheets.googleapis.com/v4/spreadsheets/{sid}:batchUpdate", tok,
                {"requests": [{"addSheet": {"properties": {"title": t}}} for t in thieu]})
            print("  đã tạo thêm tab:", thieu)
    else:
        sp = api("POST", "https://sheets.googleapis.com/v4/spreadsheets", tok, {
            "properties": {"title": "HỌC AI — Thiết kế tổng quan & Quản lý dự án v2",
                           "locale": "vi_VN", "timeZone": "Asia/Ho_Chi_Minh"},
            "sheets": [{"properties": {"title": t}} for t in tabs],
        })
        sid, url = sp["spreadsheetId"], sp.get("spreadsheetUrl")
        print("Tạo sheet mới:", sid)

    body = {"valueInputOption": "USER_ENTERED",
            "data": [{"range": f"'{t}'!A1", "values": rows} for t, rows in tabs.items()]}
    api("POST", f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values:batchUpdate", tok, body)

    # ---- VERIFY: đọc lại từng tab, so số dòng với dữ liệu nguồn ----
    print("\n=== VERIFY (đọc lại từ server) ===")
    allok = True
    for t, rows in tabs.items():
        rng = urllib.parse.quote(f"'{t}'!A1:Z200")
        v = api("GET", f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/{rng}", tok)
        got = len(v.get("values", []))
        ok = got == len(rows)
        allok &= ok
        print(f"  [{'OK ' if ok else 'LỆCH'}] {t:16s} server={got:3d} nguồn={len(rows):3d}")

    # kiểm tra riêng: YCCĐ phải là bản SẠCH (không còn chuỗi lộn cột)
    rng = urllib.parse.quote("'YCCĐ lớp 10'!E1:E30")
    v = api("GET", f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/{rng}", tok)
    texts = " ".join(r[0] for r in v.get("values", []) if r)
    ban = ["con động của con", "người hệ thống", "của con hệ thống", "hệ thống AI người"]
    nhem = [b for b in ban if b in texts]
    print(f"\n  [{'OK ' if not nhem else 'LỖI'}] YCCĐ không còn chuỗi lộn cột: {nhem or 'sạch'}")
    print(f"  Số YCCĐ trong sheet: {len(v.get('values', [])) - 1} (kì vọng 22)")
    allok &= (not nhem) and len(v.get("values", [])) - 1 == 22

    # kiểm tra tương phản: mọi dòng màu phải ĐẠT (trừ dòng trang trí)
    rng = urllib.parse.quote("'Design system'!A1:G20")
    v = api("GET", f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/{rng}", tok)
    fail = [r[0] for r in v.get("values", [])[1:]
            if len(r) > 5 and r[5] == "KHÔNG ĐẠT"]
    print(f"  [{'OK ' if not fail else 'LỖI'}] Màu không đạt tương phản: {fail or 'không có'}")
    allok &= not fail

    json.dump({"id": sid, "url": url}, open(OUT, "w"))
    print("\nKẾT LUẬN:", "SHEET ĐẦY ĐỦ VÀ SẠCH" if allok else "CÒN LỖI — xem ở trên")
    print("LINK:", url)
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
