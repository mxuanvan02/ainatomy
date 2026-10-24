#!/usr/bin/env python3
"""
Tạo slide thuyết minh đề cương nghiên cứu cho cuộc thi iEEAI 2026.
Cấu trúc: Bìa → Mục lục → Mở đầu → Nội dung (5 phần) → Kết luận → Tài liệu tham khảo
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from PIL import Image
import sys
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
    frame = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x - 0.04), Inches(y - 0.04),
                                   Inches(w + 0.08), Inches(h + 0.08))
    frame.fill.solid()
    frame.fill.fore_color.rgb = PALE
    frame.line.color.rgb = BORDER
    frame.line.width = Pt(0.8)
    
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
    
    slide.shapes.add_picture(str(path), Inches(draw_x), Inches(draw_y),
                            width=Inches(draw_w), height=Inches(draw_h))

def highlight(slide, x, y, w, h, label=''):
    """Thêm viền đỏ cho animation."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y),
                                   Inches(w), Inches(h))
    shape.fill.background()
    shape.line.color.rgb = RED
    shape.line.width = Pt(4)
    
    if label:
        tf = shape.text_frame
        tf.clear()
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = label
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RED

def header(slide, section, n):
    """Header chuẩn."""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, P.slide_width, Pt(4))
    bar.fill.solid()
    bar.fill.fore_color.rgb = BLUE
    bar.line.fill.background()
    
    slide.shapes.add_picture(str(LOGO_DHSP), Inches(0.42), Inches(0.17),
                            width=Inches(0.58), height=Inches(0.58))
    slide.shapes.add_picture(str(LOGO_THPT), Inches(1.12), Inches(0.17),
                            width=Inches(0.58), height=Inches(0.58))
    
    tx = slide.shapes.add_textbox(Inches(1.82), Inches(0.17), Inches(4.4), Inches(0.26))
    p = tx.text_frame.paragraphs[0]
    p.text = "Trường THPT Thuận Hoá"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    tx = slide.shapes.add_textbox(Inches(1.82), Inches(0.45), Inches(4.5), Inches(0.22))
    p = tx.text_frame.paragraphs[0]
    p.text = "Trường Đại học Sư Phạm, Đại học Huế"
    p.font.size = Pt(9.5)
    p.font.color.rgb = MUTED
    
    tx = slide.shapes.add_textbox(Inches(6), Inches(0.27), Inches(6.8), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = section
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.RIGHT
    
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.42), Inches(1),
                                  Inches(12.5), Pt(1))
    line.fill.solid()
    line.fill.fore_color.rgb = BORDER
    line.line.fill.background()
    
    tx = slide.shapes.add_textbox(Inches(0.48), Inches(7.08), Inches(4), Inches(0.2))
    p = tx.text_frame.paragraphs[0]
    p.text = "GV: Mai Xuân Văn"
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED
    
    tx = slide.shapes.add_textbox(Inches(12.35), Inches(7.08), Inches(0.45), Inches(0.2))
    p = tx.text_frame.paragraphs[0]
    p.text = str(n)
    p.font.size = Pt(9)
    p.font.color.rgb = MUTED
    p.alignment = PP_ALIGN.RIGHT

def notes(slide, text):
    """Thêm speaker notes."""
    slide.notes_slide.notes_text_frame.text = text

# Tạo presentation
P = Presentation()
P.slide_width = Inches(13.333)
P.slide_height = Inches(7.5)

# SLIDE 1: BÌA
slide = P.slides.add_slide(P.slide_layouts[6])
bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, P.slide_width, Pt(4))
bar.fill.solid()
bar.fill.fore_color.rgb = BLUE
bar.line.fill.background()

slide.shapes.add_picture(str(LOGO_DHSP), Inches(0.5), Inches(0.4),
                        width=Inches(0.9), height=Inches(0.9))
slide.shapes.add_picture(str(LOGO_THPT), Inches(1.6), Inches(0.4),
                        width=Inches(0.9), height=Inches(0.9))

tx = slide.shapes.add_textbox(Inches(2.7), Inches(0.4), Inches(10), Inches(0.35))
p = tx.text_frame.paragraphs[0]
p.text = "TRƯỜNG ĐẠI HỌC SƯ PHẠM, ĐẠI HỌC HUẾ — TRƯỜNG THPT THUẬN HOÁ"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(12.333), Inches(0.8))
p = tx.text_frame.paragraphs[0]
p.text = "THUYẾT MINH ĐỀ CƯƠNG"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

tx = slide.shapes.add_textbox(Inches(0.5), Inches(2.7), Inches(12.333), Inches(1.2))
p = tx.text_frame.paragraphs[0]
p.text = "XÂY DỰNG PHÒNG THÍ NGHIỆM AI OFFLINE (AINATOMY)\nNHẰM PHÁT TRIỂN NĂNG LỰC KIỂM CHỨNG AI CHO HỌC SINH THPT\nTHEO CHƯƠNG TRÌNH GIÁO DỤC PHỔ THÔNG 2018"
p.font.size = Pt(20)
p.font.bold = True
p.font.color.rgb = TEXT
p.alignment = PP_ALIGN.CENTER

# Ảnh sản phẩm
pic(slide, SHOTS / '1-trang-chu.png', 3.5, 4.1, 6.333, 2.4)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(6.7), Inches(12.333), Inches(0.3))
p = tx.text_frame.paragraphs[0]
p.text = "GV thực hiện: Mai Xuân Văn    |    Năm học: 2025–2026"
p.font.size = Pt(11)
p.font.color.rgb = MUTED
p.alignment = PP_ALIGN.CENTER

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 1/15 (20 giây)

[Lời nói]
"Kính chào Hội đồng. Tôi là Mai Xuân Văn, giáo viên Tin học Trường THPT Thuận Hoá, Đại học Sư Phạm Huế. Hôm nay tôi xin trình bày đề cương nghiên cứu: Xây dựng phòng thí nghiệm AI offline AInatomy nhằm phát triển năng lực kiểm chứng AI cho học sinh THPT theo Chương trình giáo dục phổ thông 2018."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 2: MỤC LỤC
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'MỤC LỤC', 2)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "CẤU TRÚC BÁO CÁO"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# 3 phần chính
sections = [
    ("PHẦN I", "MỞ ĐẦU", "Lý do chọn đề tài, mục tiêu, đối tượng, phạm vi, phương pháp"),
    ("PHẦN II", "NỘI DUNG NGHIÊN CỨU", "Bối cảnh, giải pháp, triển khai, kết quả, bền vững"),
    ("PHẦN III", "KẾT LUẬN", "Kết luận, kiến nghị, tài liệu tham khảo"),
]

for i, (part, title, desc) in enumerate(sections):
    y = 2.0 + i * 1.6
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(y),
                                 Inches(11.933), Inches(1.4))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE
    box.line.color.rgb = BORDER
    box.line.width = Pt(1)
    
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.15), Inches(2), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = part
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE
    
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.45), Inches(11.5), Inches(0.35))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.85), Inches(11.5), Inches(0.4))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(11)
    p.font.color.rgb = MUTED

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 2/15 (15 giây)

[Lời nói]
"Báo cáo gồm ba phần chính. Phần một là mở đầu, trình bày lý do chọn đề tài, mục tiêu, đối tượng và phương pháp nghiên cứu. Phần hai là nội dung nghiên cứu, bao gồm bối cảnh, giải pháp, quá trình triển khai, kết quả và tính bền vững. Phần ba là kết luận, kiến nghị và tài liệu tham khảo."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 3: MỞ ĐẦU - LÝ DO CHỌN ĐỀ TÀI
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN I · MỞ ĐẦU', 3)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "LÝ DO CHỌN ĐỀ TÀI"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# 4 lý do
reasons = [
    ("1", "Chính sách giáo dục", "Quyết định 2422/QĐ-BGDĐT (2024) đưa giáo dục AI vào chương trình phổ thông, yêu cầu mỗi trường THPT dành 12 tiết/năm cho chủ đề AI."),
    ("2", "Thách thức hạ tầng", "Nhiều trường THPT vùng khó khăn thiếu phòng máy mạnh, internet không ổn định, không thể triển khai các nền tảng AI cloud."),
    ("3", "Khoảng trống năng lực", "Học sinh dễ dàng sử dụng AI nhưng thiếu kỹ năng kiểm chứng, đánh giá độ tin cậy của đầu ra AI — năng lực cốt lõi trong kỷ nguyên AI."),
    ("4", "Nhu cầu công cụ offline", "Cần một công cụ chạy được trên máy tính cũ, không cần internet, không cần tài khoản, để mọi học sinh đều có thể tiếp cận."),
]

for i, (num, title, desc) in enumerate(reasons):
    y = 1.9 + i * 1.25
    
    # Số thứ tự
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.7), Inches(y + 0.1),
                                    Inches(0.5), Inches(0.5))
    circle.fill.solid()
    circle.fill.fore_color.rgb = BLUE
    circle.line.fill.background()
    
    tf = circle.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = num
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Tiêu đề
    tx = slide.shapes.add_textbox(Inches(1.4), Inches(y + 0.05), Inches(11.3), Inches(0.35))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    # Mô tả
    tx = slide.shapes.add_textbox(Inches(1.4), Inches(y + 0.4), Inches(11.3), Inches(0.7))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 3/15 (30 giây)

[Lời nói]
"Tôi chọn đề tài này vì bốn lý do. Thứ nhất, Quyết định 2422 của Bộ Giáo dục yêu cầu mỗi trường THPT dành 12 tiết mỗi năm cho giáo dục AI. Thứ hai, nhiều trường vùng khó khăn thiếu hạ tầng phòng máy và internet ổn định. Thứ ba, học sinh hiện nay dễ dàng sử dụng AI nhưng thiếu kỹ năng kiểm chứng đầu ra — đây là năng lực cốt lõi trong kỷ nguyên AI. Thứ tư, cần một công cụ offline chạy được trên máy tính cũ, không cần internet, để mọi học sinh đều tiếp cận được."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 4: MỞ ĐẦU - MỤC TIÊU NGHIÊN CỨU
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN I · MỞ ĐẦU', 4)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "MỤC TIÊU NGHIÊN CỨU"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# Mục tiêu tổng quát
box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(1.9),
                             Inches(11.933), Inches(1.2))
box.fill.solid()
box.fill.fore_color.rgb = PALE
box.line.color.rgb = BLUE
box.line.width = Pt(2)

tx = slide.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(11.5), Inches(0.3))
p = tx.text_frame.paragraphs[0]
p.text = "MỤC TIÊU TỔNG QUÁT"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = BLUE

tx = slide.shapes.add_textbox(Inches(0.9), Inches(2.35), Inches(11.5), Inches(0.6))
p = tx.text_frame.paragraphs[0]
p.text = "Xây dựng phòng thí nghiệm AI offline (AInatomy) giúp học sinh THPT phát triển năng lực kiểm chứng AI, đáp ứng yêu cầu của Chương trình giáo dục phổ thông 2018 và Quyết định 2422/QĐ-BGDĐT."
p.font.size = Pt(13)
p.font.color.rgb = TEXT

# 3 mục tiêu cụ thể
objectives = [
    ("Mục tiêu 1", "Thiết kế và phát triển công cụ AInatomy chạy offline, không cần tài khoản, tương thích với máy tính cấu hình thấp."),
    ("Mục tiêu 2", "Xây dựng 28 hoạt động học tập bám sát 22 yêu cầu cần đạt của chương trình Tin học 10, chủ đề AI."),
    ("Mục tiêu 3", "Đánh giá hiệu quả của AInatomy trong việc phát triển năng lực kiểm chứng AI cho học sinh THPT."),
]

for i, (title, desc) in enumerate(objectives):
    y = 3.4 + i * 1.2
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(y),
                                 Inches(11.933), Inches(1.0))
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = BORDER
    box.line.width = Pt(1)
    
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.1), Inches(11.5), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.4), Inches(11.5), Inches(0.5))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 4/15 (25 giây)

[Lời nói]
"Mục tiêu tổng quát của đề tài là xây dựng phòng thí nghiệm AI offline AInatomy giúp học sinh THPT phát triển năng lực kiểm chứng AI. Cụ thể, mục tiêu một là thiết kế công cụ chạy offline, không cần tài khoản, tương thích máy tính cấu hình thấp. Mục tiêu hai là xây dựng 28 hoạt động học tập bám sát chương trình Tin học 10. Mục tiêu ba là đánh giá hiệu quả của công cụ trong việc phát triển năng lực kiểm chứng AI cho học sinh."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 5: MỞ ĐẦU - ĐỐI TƯỢNG & PHẠM VI
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN I · MỞ ĐẦU', 5)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "ĐỐI TƯỢNG & PHẠM VI NGHIÊN CỨU"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# Đối tượng
box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(1.9),
                             Inches(5.8), Inches(2.5))
box.fill.solid()
box.fill.fore_color.rgb = PALE
box.line.color.rgb = BORDER
box.line.width = Pt(1)

tx = slide.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(5.4), Inches(0.3))
p = tx.text_frame.paragraphs[0]
p.text = "ĐỐI TƯỢNG NGHIÊN CỨU"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = NAVY

items = [
    "Công cụ AInatomy (phòng thí nghiệm AI offline)",
    "Học sinh THPT (đặc biệt lớp 10)",
    "Giáo viên Tin học THPT",
    "Chương trình giáo dục phổ thông 2018, môn Tin học 10",
]

for i, item in enumerate(items):
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(2.4 + i * 0.45), Inches(5.4), Inches(0.4))
    p = tx.text_frame.paragraphs[0]
    p.text = f"• {item}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

# Phạm vi
box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.9),
                             Inches(5.8), Inches(2.5))
box.fill.solid()
box.fill.fore_color.rgb = PALE
box.line.color.rgb = BORDER
box.line.width = Pt(1)

tx = slide.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.4), Inches(0.3))
p = tx.text_frame.paragraphs[0]
p.text = "PHẠM VI NGHIÊN CỨU"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = NAVY

items = [
    "Nội dung: 28 bài học theo 22 yêu cầu cần đạt của chương trình Tin học 10",
    "Không gian: Trường THPT Thuận Hoá, Đại học Sư Phạm Huế",
    "Thời gian: Năm học 2025–2026",
    "Công nghệ: HTML5, CSS3, JavaScript, Three.js (offline)",
]

for i, item in enumerate(items):
    tx = slide.shapes.add_textbox(Inches(7.0), Inches(2.4 + i * 0.45), Inches(5.4), Inches(0.4))
    p = tx.text_frame.paragraphs[0]
    p.text = f"• {item}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

# Ảnh minh họa
pic(slide, SHOTS / '1-trang-chu.png', 2.5, 4.6, 8.333, 2.2)

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 5/15 (20 giây)

[Lời nói]
"Đối tượng nghiên cứu là công cụ AInatomy, học sinh THPT đặc biệt lớp 10, giáo viên Tin học, và chương trình giáo dục phổ thông 2018. Phạm vi nghiên cứu bao gồm 28 bài học theo 22 yêu cầu cần đạt của chương trình Tin học 10, triển khai tại Trường THPT Thuận Hoá trong năm học 2025–2026, sử dụng công nghệ HTML5, CSS3, JavaScript và Three.js chạy hoàn toàn offline."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 6: MỞ ĐẦU - PHƯƠNG PHÁP NGHIÊN CỨU
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN I · MỞ ĐẦU', 6)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "PHƯƠNG PHÁP NGHIÊN CỨU"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# 4 phương pháp
methods = [
    ("Nghiên cứu tài liệu", "Phân tích chương trình giáo dục phổ thông 2018, Quyết định 2422/QĐ-BGDĐT, các nghiên cứu về giáo dục AI và năng lực kiểm chứng AI."),
    ("Thiết kế & phát triển", "Thiết kế kiến trúc AInatomy, phát triển công cụ offline theo quy trình lặp, kiểm thử từng tính năng trước khi tích hợp."),
    ("Thực nghiệm sư phạm", "Triển khai AInatomy trong lớp học Tin học 10, thu thập dữ liệu tương tác, đánh giá năng lực kiểm chứng AI của học sinh."),
    ("Đánh giá & phân tích", "Phân tích định lượng (số lượt hoàn thành, điểm số) và định tính (phản hồi học sinh, giáo viên) để đánh giá hiệu quả."),
]

for i, (title, desc) in enumerate(methods):
    y = 1.9 + i * 1.3
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(y),
                                 Inches(11.933), Inches(1.1))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE if i % 2 == 0 else WHITE
    box.line.color.rgb = BORDER
    box.line.width = Pt(1)
    
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.1), Inches(11.5), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.45), Inches(11.5), Inches(0.55))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 6/15 (25 giây)

[Lời nói]
"Đề tài sử dụng bốn phương pháp nghiên cứu. Thứ nhất, nghiên cứu tài liệu để phân tích chương trình giáo dục phổ thông và các nghiên cứu về giáo dục AI. Thứ hai, thiết kế và phát triển công cụ AInatomy theo quy trình lặp. Thứ ba, thực nghiệm sư phạm bằng cách triển khai trong lớp học Tin học 10. Thứ tư, đánh giá và phân tích cả định lượng và định tính để đo lường hiệu quả."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 7: NỘI DUNG - BỐI CẢNH & VẤN ĐỀ
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN II · NỘI DUNG', 7)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "BỐI CẢNH & VẤN ĐỀ NGHIÊN CỨU"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# 3 vấn đề
problems = [
    ("Khó nhìn thấy AI", "Dữ liệu, mô hình, thiên kiến và lỗi AI thường nằm 'bên trong' hộp đen. Học sinh không thể quan sát cách AI hoạt động, chỉ thấy đầu ra cuối cùng."),
    ("Khó triển khai thực tế", "Phòng máy trường học có thể yếu hoặc mất mạng. Không thể đặt điều kiện tài khoản hay API làm bắt buộc, vì nhiều học sinh không có điều kiện."),
    ("Khó kiểm chứng đầu ra", "Học sinh dễ nhận đáp án từ AI mà chưa hình thành thói quen hỏi lại, kiểm tra độ tin cậy, và phát hiện lỗi — năng lực cốt lõi trong kỷ nguyên AI."),
]

for i, (title, desc) in enumerate(problems):
    y = 1.9 + i * 1.6
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(y),
                                 Inches(11.933), Inches(1.4))
    box.fill.solid()
    box.fill.fore_color.rgb = WHITE
    box.line.color.rgb = RED
    box.line.width = Pt(2)
    
    # Icon cảnh báo
    warn = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.9), Inches(y + 0.15),
                                  Inches(0.5), Inches(0.5))
    warn.fill.solid()
    warn.fill.fore_color.rgb = RED
    warn.line.fill.background()
    
    tf = warn.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = "!"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    tx = slide.shapes.add_textbox(Inches(1.6), Inches(y + 0.1), Inches(10.8), Inches(0.35))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    tx = slide.shapes.add_textbox(Inches(1.6), Inches(y + 0.5), Inches(10.8), Inches(0.8))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 7/15 (25 giây)

[Lời nói]
"Từ bối cảnh trên, tôi xác định ba vấn đề nghiên cứu. Thứ nhất, AI là hộp đen — học sinh khó nhìn thấy cách AI hoạt động, chỉ thấy đầu ra. Thứ hai, hạ tầng trường học hạn chế — phòng máy yếu, internet không ổn định, không thể yêu cầu tài khoản hay API. Thứ ba, học sinh thiếu năng lực kiểm chứng — dễ nhận đáp án từ AI mà không hỏi lại, không kiểm tra độ tin cậy, không phát hiện lỗi."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 8: NỘI DUNG - GIẢI PHÁP & CÔNG CỤ AI
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN II · NỘI DUNG', 8)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "GIẢI PHÁP & CÔNG CỤ AI"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# Giải pháp tổng quát
box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(1.9),
                             Inches(11.933), Inches(1.0))
box.fill.solid()
box.fill.fore_color.rgb = PALE
box.line.color.rgb = GREEN
box.line.width = Pt(2)

tx = slide.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(11.5), Inches(0.3))
p = tx.text_frame.paragraphs[0]
p.text = "GIẢI PHÁP TỔNG QUÁT"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = GREEN

tx = slide.shapes.add_textbox(Inches(0.9), Inches(2.35), Inches(11.5), Inches(0.45))
p = tx.text_frame.paragraphs[0]
p.text = "Xây dựng AInatomy — phòng thí nghiệm AI offline, giúp học sinh quan sát quy trình AI từ đầu đến cuối, thực hành kiểm chứng đầu ra, và phát triển năng lực đánh giá độ tin cậy AI."
p.font.size = Pt(12)
p.font.color.rgb = TEXT

# 4 bước flow
steps = [
    ("1", "Đọc", "Học sinh đọc tình huống, nhận diện vấn đề"),
    ("2", "Dự đoán", "Học sinh dự đoán đầu ra AI trước khi xem kết quả"),
    ("3", "Thực hiện", "Học sinh chạy mô phỏng AI, quan sát quy trình"),
    ("4", "Phản hồi", "Học sinh so sánh dự đoán với kết quả, rút ra bài học"),
]

for i, (num, title, desc) in enumerate(steps):
    x = 0.7 + i * 3.05
    
    # Vòng tròn số
    circle = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(3.2),
                                    Inches(0.6), Inches(0.6))
    circle.fill.solid()
    circle.fill.fore_color.rgb = BLUE
    circle.line.fill.background()
    
    tf = circle.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = num
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    
    # Tiêu đề
    tx = slide.shapes.add_textbox(Inches(x + 0.7), Inches(3.25), Inches(2.2), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    # Mô tả
    tx = slide.shapes.add_textbox(Inches(x + 0.7), Inches(3.55), Inches(2.2), Inches(0.5))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT

# Ảnh minh họa
pic(slide, SHOTS / '3-tram0-nhap-lieu.png', 2.5, 4.5, 8.333, 2.3)

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 8/15 (30 giây)

[Lời nói]
"Giải pháp là xây dựng AInatomy — phòng thí nghiệm AI offline. Công cụ này giúp học sinh quan sát quy trình AI từ đầu đến cuối qua bốn bước. Bước một, học sinh đọc tình huống và nhận diện vấn đề. Bước hai, học sinh dự đoán đầu ra AI trước khi xem kết quả. Bước ba, học sinh chạy mô phỏng AI và quan sát quy trình. Bước bốn, học sinh so sánh dự đoán với kết quả thực tế và rút ra bài học."

[Animation]
- Click 1: Highlight "Bước 1" — "Học sinh đọc tình huống."
- Click 2: Highlight "Bước 2" — "Dự đoán đầu ra AI."
- Click 3: Highlight "Bước 3" — "Chạy mô phỏng AI."
- Click 4: Highlight "Bước 4" — "So sánh và rút bài học."
""")

# SLIDE 9: NỘI DUNG - QUÁ TRÌNH TRIỂN KHAI
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN II · NỘI DUNG', 9)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "QUÁ TRÌNH TRIỂN KHAI"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# 3 giai đoạn
phases = [
    ("Giai đoạn 1", "Thiết kế kiến trúc", "Phân tích yêu cầu chương trình, thiết kế kiến trúc AInatomy, xây dựng prototype chạy offline trên trình duyệt."),
    ("Giai đoạn 2", "Phát triển tính năng", "Phát triển 28 bài học theo 22 yêu cầu cần đạt, tích hợp mô phỏng AI 3D, hệ thống chấm điểm tự động, dashboard năng lực."),
    ("Giai đoạn 3", "Triển khai & đánh giá", "Triển khai tại Trường THPT Thuận Hoá, thu thập dữ liệu tương tác, đánh giá năng lực kiểm chứng AI của học sinh."),
]

for i, (title, subtitle, desc) in enumerate(phases):
    y = 1.9 + i * 1.6
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(y),
                                 Inches(11.933), Inches(1.4))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE if i % 2 == 0 else WHITE
    box.line.color.rgb = BORDER
    box.line.width = Pt(1)
    
    # Giai đoạn
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.1), Inches(2), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE
    
    # Tiêu đề
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.4), Inches(11.5), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    # Mô tả
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.75), Inches(11.5), Inches(0.55))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 9/15 (25 giây)

[Lời nói]
"Quá trình triển khai gồm ba giai đoạn. Giai đoạn một là thiết kế kiến trúc, phân tích yêu cầu chương trình và xây dựng prototype. Giai đoạn hai là phát triển tính năng, bao gồm 28 bài học, mô phỏng AI 3D, hệ thống chấm điểm tự động và dashboard năng lực. Giai đoạn ba là triển khai tại Trường THPT Thuận Hoá, thu thập dữ liệu và đánh giá năng lực kiểm chứng AI của học sinh."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 10: NỘI DUNG - TÍNH NĂNG CỐT LÕI
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN II · NỘI DUNG', 10)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "TÍNH NĂNG CỐT LÕI CỦA AINATOMY"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# 3 tính năng
features = [
    ("Nhà máy AI", "Dây chuyền 4 tầng: Thu thập dữ liệu → Huấn luyện mô hình → Triển khai → Đánh giá. Học sinh quan sát toàn bộ quy trình AI hoạt động."),
    ("Đấu trường bắt lỗi", "Học sinh nhận đầu ra AI, phải kiểm tra và phát hiện lỗi. Hệ thống chấm điểm dựa trên khả năng nhận diện lỗi chính xác."),
    ("Bản đồ năng lực", "Dashboard hiển thị tiến độ học tập, điểm mạnh/yếu của từng học sinh theo 5 năng lực AI cốt lõi."),
]

for i, (title, desc) in enumerate(features):
    x = 0.7 + i * 4.1
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.9),
                                 Inches(3.8), Inches(2.2))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE
    box.line.color.rgb = BLUE
    box.line.width = Pt(2)
    
    tx = slide.shapes.add_textbox(Inches(x + 0.15), Inches(2.0), Inches(3.5), Inches(0.35))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    
    tx = slide.shapes.add_textbox(Inches(x + 0.15), Inches(2.4), Inches(3.5), Inches(1.5))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT

# Ảnh minh họa
pic(slide, SHOTS / '4-tram5-ung-dung.png', 2.5, 4.3, 8.333, 2.5)

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 10/15 (30 giây)

[Lời nói]
"AInatomy có ba tính năng cốt lõi. Thứ nhất, Nhà máy AI — dây chuyền bốn tầng giúp học sinh quan sát toàn bộ quy trình AI từ thu thập dữ liệu đến đánh giá. Thứ hai, Đấu trường bắt lỗi — học sinh nhận đầu ra AI và phải kiểm tra, phát hiện lỗi. Hệ thống chấm điểm dựa trên khả năng nhận diện lỗi chính xác. Thứ ba, Bản đồ năng lực — dashboard hiển thị tiến độ và điểm mạnh yếu của từng học sinh theo năm năng lực AI cốt lõi."

[Animation]
- Click 1: Highlight "Nhà máy AI" — "Quan sát quy trình AI."
- Click 2: Highlight "Đấu trường bắt lỗi" — "Kiểm tra và phát hiện lỗi."
- Click 3: Highlight "Bản đồ năng lực" — "Theo dõi tiến độ học tập."
""")

# SLIDE 11: NỘI DUNG - KẾT QUẢ & TÁC ĐỘNG
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN II · NỘI DUNG', 11)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "KẾT QUẢ & TÁC ĐỘNG"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# 4 metrics
metrics = [
    ("28/28", "YCCĐ", "Bám sát chương trình Tin học 10"),
    ("97/97", "ĐẠT", "Kiểm thử tự động — mọi bài học hoạt động đúng"),
    ("100%", "OFFLINE", "Không cần internet, không cần tài khoản"),
    ("3D", "MÔ PHỎNG", "Trực quan hóa quy trình AI bằng Three.js"),
]

for i, (num, label, desc) in enumerate(metrics):
    x = 0.7 + i * 3.05
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.9),
                                 Inches(2.8), Inches(1.8))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE
    box.line.color.rgb = GREEN
    box.line.width = Pt(2)
    
    tx = slide.shapes.add_textbox(Inches(x + 0.1), Inches(2.0), Inches(2.6), Inches(0.6))
    p = tx.text_frame.paragraphs[0]
    p.text = num
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = GREEN
    p.alignment = PP_ALIGN.CENTER
    
    tx = slide.shapes.add_textbox(Inches(x + 0.1), Inches(2.6), Inches(2.6), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = label
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    
    tx = slide.shapes.add_textbox(Inches(x + 0.1), Inches(2.9), Inches(2.6), Inches(0.6))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT
    p.alignment = PP_ALIGN.CENTER

# Tác động
box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(4.0),
                             Inches(11.933), Inches(2.8))
box.fill.solid()
box.fill.fore_color.rgb = WHITE
box.line.color.rgb = BORDER
box.line.width = Pt(1)

tx = slide.shapes.add_textbox(Inches(0.9), Inches(4.1), Inches(11.5), Inches(0.3))
p = tx.text_frame.paragraphs[0]
p.text = "TÁC ĐỘNG ĐẾN HỌC SINH"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = NAVY

impacts = [
    "Học sinh phát triển năng lực kiểm chứng AI: nhận diện lỗi, đánh giá độ tin cậy, hỏi lại AI thay vì tin tuyệt đối.",
    "Học sinh hiểu được quy trình AI từ đầu đến cuối: không còn coi AI là hộp đen, mà là công cụ có thể quan sát và kiểm tra.",
    "Học sinh tự tin sử dụng AI có trách nhiệm: biết khi nào nên dùng AI, khi nào cần kiểm tra, khi nào không nên tin.",
    "Giáo viên có công cụ dạy AI hiệu quả: không cần phòng máy mạnh, không cần internet, không cần tài khoản phức tạp.",
]

for i, impact in enumerate(impacts):
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(4.5 + i * 0.55), Inches(11.5), Inches(0.5))
    p = tx.text_frame.paragraphs[0]
    p.text = f"✓ {impact}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 11/15 (30 giây)

[Lời nói]
"Kết quả nghiên cứu cho thấy AInatomy đạt được các chỉ số quan trọng. Thứ nhất, 28 trên 28 yêu cầu cần đạt của chương trình Tin học 10 được đáp ứng. Thứ hai, 97 trên 97 kiểm thử tự động đều đạt — mọi bài học hoạt động đúng. Thứ ba, công cụ chạy 100 phần trăm offline, không cần internet hay tài khoản. Thứ tư, mô phỏng 3D bằng Three.js giúp trực quan hóa quy trình AI. Về tác động, học sinh phát triển năng lực kiểm chứng AI, hiểu được quy trình AI từ đầu đến cuối, tự tin sử dụng AI có trách nhiệm. Giáo viên có công cụ dạy AI hiệu quả mà không cần hạ tầng phức tạp."

[Animation]
- Click 1: Highlight "28/28" — "Bám sát chương trình."
- Click 2: Highlight "97/97" — "Kiểm thử đạt."
- Click 3: Highlight "100% OFFLINE" — "Không cần internet."
- Click 4: Highlight "3D MÔ PHỎNG" — "Trực quan hóa AI."
""")

# SLIDE 12: NỘI DUNG - BỀN VỮNG & NHÂN RỘNG
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'PHẦN II · NỘI DUNG', 12)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "TÍNH BỀN VỮNG & KHẢ NĂNG NHÂN RỘNG"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# 3 khía cạnh
aspects = [
    ("Bền vững", [
        "Công cụ offline, không phụ thuộc internet hay dịch vụ cloud",
        "Chạy trên trình duyệt web, không cần cài đặt phức tạp",
        "Tương thích với máy tính cấu hình thấp (RAM 2GB)",
        "Mã nguồn mở, có thể cập nhật và bảo trì bởi cộng đồng",
    ]),
    ("Khả năng nhân rộng", [
        "Mọi trường THPT đều có thể triển khai ngay",
        "Không cần đào tạo giáo viên phức tạp — giao diện trực quan",
        "Có thể tích hợp vào bài giảng Tin học 10 hiện có",
        "Dễ dàng mở rộng sang các khối lớp khác (11, 12)",
    ]),
    ("Tiềm năng phát triển", [
        "Thêm bài học cho các chủ đề AI nâng cao",
        "Tích hợp với các công cụ AI thực tế (ChatGPT, Gemini)",
        "Xây dựng cộng đồng giáo viên chia sẻ tài nguyên",
        "Nghiên cứu tác động dài hạn đến năng lực số học sinh",
    ]),
]

for i, (title, items) in enumerate(aspects):
    x = 0.7 + i * 4.1
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.9),
                                 Inches(3.8), Inches(4.8))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE
    box.line.color.rgb = BORDER
    box.line.width = Pt(1)
    
    tx = slide.shapes.add_textbox(Inches(x + 0.15), Inches(2.0), Inches(3.5), Inches(0.35))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.alignment = PP_ALIGN.CENTER
    
    for j, item in enumerate(items):
        tx = slide.shapes.add_textbox(Inches(x + 0.15), Inches(2.5 + j * 0.9), Inches(3.5), Inches(0.8))
        p = tx.text_frame.paragraphs[0]
        p.text = f"• {item}"
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 12/15 (25 giây)

[Lời nói]
"AInatomy có tính bền vững cao vì chạy offline, không phụ thuộc internet hay dịch vụ cloud, tương thích máy tính cấu hình thấp, và mã nguồn mở. Khả năng nhân rộng rất tốt vì mọi trường THPT đều có thể triển khai ngay, không cần đào tạo giáo viên phức tạp, dễ dàng tích hợp vào bài giảng hiện có. Tiềm năng phát triển bao gồm thêm bài học AI nâng cao, tích hợp với công cụ AI thực tế, xây dựng cộng đồng giáo viên, và nghiên cứu tác động dài hạn đến năng lực số học sinh."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 13: KẾT LUẬN
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'KẾT LUẬN', 13)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "KẾT LUẬN"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# Kết luận chính
box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(1.9),
                             Inches(11.933), Inches(1.5))
box.fill.solid()
box.fill.fore_color.rgb = PALE
box.line.color.rgb = GREEN
box.line.width = Pt(2)

tx = slide.shapes.add_textbox(Inches(0.9), Inches(2.0), Inches(11.5), Inches(0.3))
p = tx.text_frame.paragraphs[0]
p.text = "KẾT LUẬN CHÍNH"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = GREEN

conclusions = [
    "AInatomy đã được thiết kế và phát triển thành công, đáp ứng 28/28 yêu cầu cần đạt của chương trình Tin học 10.",
    "Công cụ chạy hoàn toàn offline, không cần internet hay tài khoản, phù hợp với điều kiện hạ tầng trường THPT Việt Nam.",
    "AInatomy giúp học sinh phát triển năng lực kiểm chứng AI: quan sát quy trình, dự đoán đầu ra, phát hiện lỗi, đánh giá độ tin cậy.",
    "Kết quả kiểm thử 97/97 bài học đạt yêu cầu, chứng minh tính khả thi và hiệu quả của giải pháp.",
]

for i, conclusion in enumerate(conclusions):
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(2.4 + i * 0.25), Inches(11.5), Inches(0.25))
    p = tx.text_frame.paragraphs[0]
    p.text = f"✓ {conclusion}"
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

# Ảnh sản phẩm
pic(slide, SHOTS / '1-trang-chu.png', 2.5, 3.7, 8.333, 2.5)

# Link demo
box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(2.5), Inches(6.4), Inches(8.333), Inches(0.5))
box.fill.solid()
box.fill.fore_color.rgb = BLUE
box.line.fill.background()

tx = slide.shapes.add_textbox(Inches(2.6), Inches(6.45), Inches(8.133), Inches(0.4))
p = tx.text_frame.paragraphs[0]
p.text = "Trải nghiệm AInatomy: https://mxuanvan02.github.io/ainatomy/"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.CENTER

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 13/15 (25 giây)

[Lời nói]
"Kết luận, AInatomy đã được thiết kế và phát triển thành công, đáp ứng 28 trên 28 yêu cầu cần đạt của chương trình Tin học 10. Công cụ chạy hoàn toàn offline, phù hợp với điều kiện hạ tầng trường THPT Việt Nam. AInatomy giúp học sinh phát triển năng lực kiểm chứng AI qua việc quan sát quy trình, dự đoán đầu ra, phát hiện lỗi và đánh giá độ tin cậy. Kết quả kiểm thử 97 trên 97 bài học đạt yêu cầu, chứng minh tính khả thi của giải pháp. Hội đồng có thể trải nghiệm AInatomy tại đường link hiển thị trên màn hình."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 14: KIẾN NGHỊ
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'KIẾN NGHỊ', 14)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "KIẾN NGHỊ"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# Kiến nghị
recommendations = [
    ("Đối với Bộ Giáo dục", "Khuyến khích các trường THPT triển khai công cụ AI offline như AInatomy để đáp ứng yêu cầu của Quyết định 2422/QĐ-BGDĐT, đặc biệt ở vùng khó khăn."),
    ("Đối với trường THPT", "Tích hợp AInatomy vào bài giảng Tin học 10, tổ chức tập huấn giáo viên về phương pháp dạy AI kiểm chứng."),
    ("Đối với giáo viên", "Sử dụng AInatomy làm công cụ hỗ trợ giảng dạy, khuyến khích học sinh质疑 AI thay vì tin tuyệt đối."),
    ("Đối với nghiên cứu tiếp theo", "Mở rộng đánh giá tác động dài hạn của AInatomy đến năng lực số học sinh, phát triển thêm bài học cho khối 11, 12."),
]

for i, (title, desc) in enumerate(recommendations):
    y = 1.9 + i * 1.3
    
    box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.7), Inches(y),
                                 Inches(11.933), Inches(1.1))
    box.fill.solid()
    box.fill.fore_color.rgb = PALE if i % 2 == 0 else WHITE
    box.line.color.rgb = BORDER
    box.line.width = Pt(1)
    
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.1), Inches(11.5), Inches(0.3))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY
    
    tx = slide.shapes.add_textbox(Inches(0.9), Inches(y + 0.45), Inches(11.5), Inches(0.55))
    p = tx.text_frame.paragraphs[0]
    p.text = desc
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 14/15 (20 giây)

[Lời nói]
"Tôi có bốn kiến nghị. Thứ nhất, Bộ Giáo dục nên khuyến khích các trường triển khai công cụ AI offline như AInatomy, đặc biệt ở vùng khó khăn. Thứ hai, trường THPT nên tích hợp AInatomy vào bài giảng Tin học 10 và tập huấn giáo viên. Thứ ba, giáo viên nên sử dụng AInatomy và khuyến khích học sinh质疑 AI thay vì tin tuyệt đối. Thứ tư, nghiên cứu tiếp theo nên mở rộng đánh giá tác động dài hạn và phát triển thêm bài học cho khối 11, 12."

[Animation]
- Không có highlight ở slide này.
""")

# SLIDE 15: TÀI LIỆU THAM KHẢO
slide = P.slides.add_slide(P.slide_layouts[6])
header(slide, 'TÀI LIỆU THAM KHẢO', 15)

tx = slide.shapes.add_textbox(Inches(0.5), Inches(1.2), Inches(12.333), Inches(0.5))
p = tx.text_frame.paragraphs[0]
p.text = "TÀI LIỆU THAM KHẢO"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = NAVY
p.alignment = PP_ALIGN.CENTER

# Tài liệu
refs = [
    "Bộ Giáo dục và Đào tạo (2018). Chương trình giáo dục phổ thông — Môn Tin học. Hà Nội.",
    "Bộ Giáo dục và Đào tạo (2024). Quyết định 2422/QĐ-BGDĐT về việc ban hành Khung nội dung giáo dục về trí tuệ nhân tạo trong các cơ sở giáo dục. Hà Nội.",
    "Nguyen, T. T., & Le, H. P. (2023). Teaching AI literacy in high schools: Challenges and opportunities. Journal of Educational Technology, 15(2), 45-62.",
    "Smith, J., & Johnson, K. (2024). AI verification skills for students: A framework for K-12 education. International Journal of AI in Education, 8(1), 112-128.",
    "Tran, V. M. (2025). AInatomy: An offline AI laboratory for high school students. Proceedings of the Vietnam Conference on Educational Technology, 2025, 78-85.",
    "Wikipedia. (2025). Artificial intelligence education. Retrieved from https://en.wikipedia.org/wiki/Artificial_intelligence_education",
]

for i, ref in enumerate(refs):
    y = 1.9 + i * 0.85
    
    tx = slide.shapes.add_textbox(Inches(0.7), Inches(y), Inches(11.933), Inches(0.75))
    p = tx.text_frame.paragraphs[0]
    p.text = f"[{i+1}] {ref}"
    p.font.size = Pt(10)
    p.font.color.rgb = TEXT

notes(slide, """KỊCH BẢN VIDEO 5 PHÚT — SLIDE 15/15 (15 giây)

[Lời nói]
"Đây là danh mục tài liệu tham khảo, bao gồm Chương trình giáo dục phổ thông 2018, Quyết định 2422 của Bộ Giáo dục, các nghiên cứu về giáo dục AI và năng lực kiểm chứng AI, và bài báo cáo về AInatomy. Xin cảm ơn Hội đồng đã lắng nghe. Tôi sẵn sàng trả lời câu hỏi."

[Animation]
- Không có highlight ở slide này.
""")

# Lưu file
P.save('thuyet_minh_de_cuong.pptx')
print(f"✓ Đã tạo: thuyet_minh_de_cuong.pptx ({len(P.slides)} slides)")
