#!/usr/bin/env python3
"""
Tạo poster A0 cho cuộc thi iEEAI 2026.
Kích thước: 84.1 x 118.9 cm (A0)
"""

from pptx import Presentation
from pptx.util import Cm, Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
from pathlib import Path

# Colors
WHITE = RGBColor(255, 255, 255)
NAVY = RGBColor(24, 55, 91)
BLUE = RGBColor(0, 102, 204)
TEXT = RGBColor(45, 55, 65)
MUTED = RGBColor(100, 110, 120)
BORDER = RGBColor(210, 220, 230)
PALE = RGBColor(242, 247, 252)
GOLD = RGBColor(211, 153, 42)
GREEN = RGBColor(37, 139, 93)
RED = RGBColor(220, 50, 50)

# Paths
LOGO_DHSP = Path('/home/hitokiri/ieeai2026/soi-ai/logo_dhsp_hue.png')
LOGO_THPT = Path('/home/hitokiri/ieeai2026/soi-ai/logo_thpt_thuan_hoa.png')
SHOTS = Path('/home/hitokiri/ieeai2026/shot_sang')

def pic(slide, path, x, y, w, h):
    """Chèn ảnh giữ tỷ lệ khung hình."""
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x - 0.3), Cm(y - 0.3),
                                   Cm(w + 0.6), Cm(h + 0.6))
    frame.fill.solid()
    frame.fill.fore_color.rgb = PALE
    frame.line.color.rgb = BORDER
    frame.line.width = Pt(1)
    
    im = Image.open(path)
    ratio = im.width / im.height
    box_ratio = w / h
    
    if ratio >= box_ratio:
        draw_w = w
        draw_h = w / ratio
    else:
        draw_h = h
        draw_w = h * ratio
    
    draw_x = x + (w - draw_w) / 2
    draw_y = y + (h - draw_h) / 2
    
    slide.shapes.add_picture(str(path), Cm(draw_x), Cm(draw_y),
                            width=Cm(draw_w), height=Cm(draw_h))

# Tạo poster A0 (84.1 x 118.9 cm)
P = Presentation()
P.slide_width = Cm(84.1)
P.slide_height = Cm(118.9)

slide = P.slides.add_slide(P.slide_layouts[6])

# === HEADER (0-20 cm) ===
# Background header
header_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Cm(84.1), Cm(20))
header_bg.fill.solid()
header_bg.fill.fore_color.rgb = NAVY
header_bg.line.fill.background()

# Logos
slide.shapes.add_picture(str(LOGO_DHSP), Cm(2), Cm(2), width=Cm(6), height=Cm(6))
slide.shapes.add_picture(str(LOGO_THPT), Cm(10), Cm(2), width=Cm(6), height=Cm(6))

# Tên trường
tx = slide.shapes.add_textbox(Cm(18), Cm(2), Cm(64), Cm(2))
p = tx.text_frame.paragraphs[0]
p.text = "TRƯỜNG ĐẠI HỌC SƯ PHẠM, ĐẠI HỌC HUẾ — TRƯỜNG THPT THUẬN HOÁ"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

# Tiêu đề chính
tx = slide.shapes.add_textbox(Cm(2), Cm(9), Cm(80), Cm(3))
p = tx.text_frame.paragraphs[0]
p.text = "THUYẾT MINH ĐỀ CƯƠNG"
p.font.size = Pt(48)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

# Tên đề tài
tx = slide.shapes.add_textbox(Cm(2), Cm(13), Cm(80), Cm(4))
p = tx.text_frame.paragraphs[0]
p.text = "XÂY DỰNG PHÒNG THÍ NGHIỆM AI OFFLINE (AINATOMY)\nNHẰM PHÁT TRIỂN NĂNG LỰC KIỂM CHỨNG AI CHO HỌC SINH THPT"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = GOLD
p.alignment = PP_ALIGN.CENTER

# Tác giả
tx = slide.shapes.add_textbox(Cm(2), Cm(18), Cm(80), Cm(1.5))
p = tx.text_frame.paragraphs[0]
p.text = "GV thực hiện: Mai Xuân Văn    |    Năm học: 2025–2026"
p.font.size = Pt(20)
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

# === PHẦN 1: BỐI CẢNH & VẤN ĐỀ (20-40 cm) ===
y_start = 22

tx = slide.shapes.add_textbox(Cm(2), Cm(y_start), Cm(80), Cm(2))
p = tx.text_frame.paragraphs[0]
p.text = "1. BỐI CẢNH & VẤN ĐỀ NGHIÊN CỨU"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = NAVY

# 3 vấn đề
problems = [
    ("Chính sách giáo dục", "QĐ 2422/QĐ-BGDĐT yêu cầu 12 tiết/năm cho giáo dục AI"),
    ("Thách thức hạ tầng", "Phòng máy yếu, internet không ổn định ở vùng khó khăn"),
    ("Khoảng trống năng lực", "Học sinh thiếu kỹ năng kiểm chứng đầu ra AI"),
]

for i, (title, desc) in enumerate(problems):
    y = y_start + 3 + i * 4.5
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(2), Cm(y), Cm(80), Cm(4))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE
    box.line.color.rgb = BLUE
    box.line.width = Pt(2)
    
    # Số thứ tự
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Cm(3), Cm(y + 0.5), Cm(3), Cm(3))
    circle.fill.solid()
    circle.fill.fore_color.rgb = BLUE
    circle.line.fill.background()
    
    tf = circle.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = str(i + 1)
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Tiêu đề
    tx = slide.shapes.add_textbox(Cm(7), Cm(y + 0.5), Cm(73), Cm(1.5))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    # Mô tả
    tx = slide.shapes.add_textbox(Cm(7), Cm(y + 2), Cm(73), Cm(1.5))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(18)
    p.font.color.rgb = TEXT

# === PHẦN 2: GIẢI PHÁP AINATOMY (40-65 cm) ===
y_start = 42

tx = slide.shapes.add_textbox(Cm(2), Cm(y_start), Cm(80), Cm(2))
p = tx.text_frame.paragraphs[0]
p.text = "2. GIẢI PHÁP: AINATOMY — PHÒNG THÍ NGHIỆM AI OFFLINE"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = NAVY

# Ảnh sản phẩm lớn
pic(slide, SHOTS / '1-trang-chu.png', 2, y_start + 3, 80, 15)

# 3 tính năng cốt lõi
features = [
    ("Nhà máy AI", "Dây chuyền 4 tầng: Thu thập → Huấn luyện → Triển khai → Đánh giá"),
    ("Đấu trường bắt lỗi", "Học sinh kiểm tra và phát hiện lỗi trong đầu ra AI"),
    ("Bản đồ năng lực", "Dashboard theo dõi tiến độ và điểm mạnh/yếu của học sinh"),
]

for i, (title, desc) in enumerate(features):
    x = 2 + i * 27
    y = y_start + 19
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x), Cm(y), Cm(25), Cm(5))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE
    box.line.color.rgb = GREEN
    box.line.width = Pt(2)
    
    tx = slide.shapes.add_textbox(Cm(x + 0.5), Cm(y + 0.5), Cm(24), Cm(1.5))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    
    tx = slide.shapes.add_textbox(Cm(x + 0.5), Cm(y + 2.5), Cm(24), Cm(2))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT
    p.alignment = PP_ALIGN.CENTER

# === PHẦN 3: KẾT QUẢ & TÁC ĐỘNG (65-90 cm) ===
y_start = 67

tx = slide.shapes.add_textbox(Cm(2), Cm(y_start), Cm(80), Cm(2))
p = tx.text_frame.paragraphs[0]
p.text = "3. KẾT QUẢ & TÁC ĐỘNG"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = NAVY

# 4 metrics
metrics = [
    ("28/28", "YCCĐ", "Bám sát chương trình Tin học 10"),
    ("97/97", "ĐẠT", "Kiểm thử tự động — mọi bài học hoạt động đúng"),
    ("100%", "OFFLINE", "Không cần internet, không cần tài khoản"),
    ("3D", "MÔ PHỎNG", "Trực quan hóa quy trình AI bằng Three.js"),
]

for i, (num, label, desc) in enumerate(metrics):
    x = 2 + i * 20.5
    y = y_start + 3
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x), Cm(y), Cm(19), Cm(10))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE
    box.line.color.rgb = GREEN
    box.line.width = Pt(3)
    
    tx = slide.shapes.add_textbox(Cm(x + 0.5), Cm(y + 1), Cm(18), Cm(3))
    p = tx.text_frame.paragraphs[0]
    p.text = num
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.alignment = PP_ALIGN.CENTER
    
    tx = slide.shapes.add_textbox(Cm(x + 0.5), Cm(y + 4), Cm(18), Cm(1.5))
    p = tx.text_frame.paragraphs[0]
    p.text = label
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    
    tx = slide.shapes.add_textbox(Cm(x + 0.5), Cm(y + 6), Cm(18), Cm(3))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(14)
    p.font.color.rgb = TEXT
    p.alignment = PP_ALIGN.CENTER

# Tác động
y = y_start + 14
tx = slide.shapes.add_textbox(Cm(2), Cm(y), Cm(80), Cm(1.5))
p = tx.text_frame.paragraphs[0]
p.text = "TÁC ĐỘNG ĐẾN HỌC SINH:"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = NAVY

impacts = [
    "✓ Phát triển năng lực kiểm chứng AI: nhận diện lỗi, đánh giá độ tin cậy",
    "✓ Hiểu quy trình AI từ đầu đến cuối: không còn coi AI là hộp đen",
    "✓ Tự tin sử dụng AI có trách nhiệm: biết khi nào nên dùng, khi nào cần kiểm tra",
]

for i, impact in enumerate(impacts):
    tx = slide.shapes.add_textbox(Cm(2), Cm(y + 2 + i * 2), Cm(80), Cm(1.8))
    p = tx.text_frame.paragraphs[0]
    p.text = impact
    p.font.size = Pt(18)
    p.font.color.rgb = TEXT

# === PHẦN 4: TÍNH BỀN VỮNG & NHÂN RỘNG (90-105 cm) ===
y_start = 92

tx = slide.shapes.add_textbox(Cm(2), Cm(y_start), Cm(80), Cm(2))
p = tx.text_frame.paragraphs[0]
p.text = "4. TÍNH BỀN VỮNG & KHẢ NĂNG NHÂN RỘNG"
p.font.size = Pt(32)
p.font.bold = True
p.font.color.rgb = NAVY

# 3 cột
aspects = [
    ("Bền vững", ["Chạy offline, không phụ thuộc internet", "Tương thích máy tính cấu hình thấp", "Mã nguồn mở, cộng đồng bảo trì"]),
    ("Nhân rộng", ["Mọi trường THPT đều triển khai được", "Không cần đào tạo phức tạp", "Dễ dàng tích hợp vào bài giảng hiện có"]),
    ("Phát triển", ["Thêm bài học AI nâng cao", "Tích hợp công cụ AI thực tế", "Nghiên cứu tác động dài hạn"]),
]

for i, (title, items) in enumerate(aspects):
    x = 2 + i * 27
    y = y_start + 3
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x), Cm(y), Cm(25), Cm(10))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE
    box.line.color.rgb = BORDER
    box.line.width = Pt(2)
    
    tx = slide.shapes.add_textbox(Cm(x + 0.5), Cm(y + 0.5), Cm(24), Cm(1.5))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    
    for j, item in enumerate(items):
        tx = slide.shapes.add_textbox(Cm(x + 0.5), Cm(y + 2.5 + j * 2.2), Cm(24), Cm(2))
        p = tx.text_frame.paragraphs[0]
        p.text = f"• {item}"
        p.font.size = Pt(16)
        p.font.color.rgb = TEXT

# === FOOTER (105-118.9 cm) ===
y_start = 107

# Background footer
footer_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Cm(y_start), Cm(84.1), Cm(11.9))
footer_bg.fill.solid()
footer_bg.fill.fore_color.rgb = NAVY
footer_bg.line.fill.background()

# Link demo
tx = slide.shapes.add_textbox(Cm(2), Cm(y_start + 1), Cm(80), Cm(2))
p = tx.text_frame.paragraphs[0]
p.text = "TRẢI NGHIỆM AINATOMY:"
p.font.size = Pt(24)
p.font.bold = True
p.font.color.rgb = GOLD
p.alignment = PP_ALIGN.CENTER

tx = slide.shapes.add_textbox(Cm(2), Cm(y_start + 3.5), Cm(80), Cm(2))
p = tx.text_frame.paragraphs[0]
p.text = "https://mxuanvan02.github.io/ainatomy/"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

# QR code
slide.shapes.add_picture('qr_ainatomy.png', Cm(35), Cm(y_start + 6), width=Cm(14), height=Cm(14))

# Thông tin liên hệ
tx = slide.shapes.add_textbox(Cm(2), Cm(y_start + 7), Cm(80), Cm(1.5))
p = tx.text_frame.paragraphs[0]
p.text = "GV: Mai Xuân Văn    |    Trường THPT Thuận Hoá, Đại học Sư Phạm Huế    |    Năm học: 2025–2026"
p.font.size = Pt(18)
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

# Lưu file
P.save('poster_A0_AInatomy.pptx')
print(f"✓ Đã tạo: poster_A0_AInatomy.pptx (A0: 84.1 x 118.9 cm)")
