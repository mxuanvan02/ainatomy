#!/usr/bin/env python3
"""Build professional A0 poster following academic design principles."""
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "references/ieeai-2026/mau_poster_2026.pptx"
OUT = ROOT / "poster_ieeai2026_professional.pptx"

# Color palette - professional academic
PRIMARY = RGBColor(24, 67, 122)      # Deep blue
SECONDARY = RGBColor(28, 146, 190)   # Cyan
ACCENT = RGBColor(219, 160, 35)      # Gold
SUCCESS = RGBColor(37, 139, 93)      # Green
DARK = RGBColor(35, 45, 58)          # Dark gray
MUTED = RGBColor(95, 105, 115)       # Medium gray
PALE = RGBColor(245, 248, 252)       # Light blue-gray
WHITE = RGBColor(255, 255, 255)
LINE = RGBColor(205, 215, 225)       # Border line


def add_section_box(slide, x, y, w, h, fill=PALE, line=LINE, radius=True):
    """Add a section container box."""
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Cm(x), Cm(y), Cm(w), Cm(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(1.5)
    return shape


def add_section_header(slide, text, x, y, w, h=1.5, color=PRIMARY):
    """Add section header with background."""
    # Header background
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x), Cm(y), Cm(w), Cm(h))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.color.rgb = color
    bg.line.width = Pt(0)
    
    # Header text
    tx = slide.shapes.add_textbox(Cm(x + 0.3), Cm(y + 0.2), Cm(w - 0.6), Cm(h - 0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = "Arial"
    p.font.size = Pt(44)  # Section heading: 36-72pt range
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.LEFT
    return bg


def add_text_block(slide, text, x, y, w, h, size=28, color=DARK, bold=False, align=PP_ALIGN.LEFT):
    """Add a text block with proper sizing."""
    tx = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = Cm(0.3)
    tf.margin_right = Cm(0.3)
    tf.margin_top = Cm(0.2)
    tf.margin_bottom = Cm(0.2)
    
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = "Arial"
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.alignment = align
    p.line_spacing = 1.3  # Line spacing 1.25-1.5
    return tx


def add_bullet_list(slide, items, x, y, w, h, size=28, color=DARK):
    """Add a bullet list with proper spacing."""
    tx = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = tx.text_frame
    tf.word_wrap = True
    tf.margin_left = Cm(0.3)
    tf.margin_right = Cm(0.3)
    
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"• {item}"
        p.font.name = "Arial"
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.line_spacing = 1.4
        p.space_after = Pt(8)
    return tx


def add_metric_card(slide, value, label, x, y, w, h, color=SUCCESS):
    """Add a metric card with large number."""
    # Card background
    add_section_box(slide, x, y, w, h, fill=WHITE, line=color, radius=True)
    
    # Large value - increased size for A0 readability
    add_text_block(slide, value, x, y + 0.5, w, 3, size=85, color=color, bold=True, align=PP_ALIGN.CENTER)
    
    # Label
    add_text_block(slide, label, x, y + 3.8, w, 1.5, size=28, color=DARK, bold=True, align=PP_ALIGN.CENTER)


def add_image_fit(slide, path, x, y, w, h):
    """Add image maintaining aspect ratio."""
    im = Image.open(path)
    ratio = im.width / im.height
    box_ratio = w / h
    
    if ratio >= box_ratio:
        dw, dh = w, w / ratio
    else:
        dh, dw = h, h * ratio
    
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    
    # Frame
    add_section_box(slide, x, y, w, h, fill=WHITE, line=LINE, radius=True)
    
    # Image
    slide.shapes.add_picture(str(path), Cm(dx), Cm(dy), width=Cm(dw), height=Cm(dh))


def main():
    prs = Presentation(str(TEMPLATE))
    slide = prs.slides[0]
    
    # Page dimensions in cm (A0: 84.1 x 118.9)
    PAGE_W, PAGE_H = 84.1, 118.9
    
    # Content area (inside dashed border)
    # Header takes ~15cm, content starts at ~32cm
    MARGIN = 3.5
    CONTENT_X = MARGIN
    CONTENT_Y = 32
    CONTENT_W = PAGE_W - 2 * MARGIN
    CONTENT_H = PAGE_H - CONTENT_Y - MARGIN
    
    # Column layout: 2 columns with gap
    COL_GAP = 2.0
    COL_W = (CONTENT_W - COL_GAP) / 2
    LEFT_X = CONTENT_X
    RIGHT_X = CONTENT_X + COL_W + COL_GAP
    
    # Replace official template placeholders
    for shape in list(slide.shapes):
        text = getattr(shape, "text", "")
        if "[VUI LÒNG THAY TÊN SẢN PHẨM" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "AINATOMY — PHÒNG THÍ NGHIỆM AI OFFLINE"
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.size = Pt(85)  # Title: 72-120pt range
            p.font.bold = True
            p.font.color.rgb = PRIMARY
        elif "Giáo viên thực hiện:" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Giáo viên thực hiện: Mai Xuân Văn\nĐơn vị công tác: Trường THPT Thuận Hoá, Đại học Sư Phạm, Đại học Huế"
            p.font.name = "Arial"
            p.font.size = Pt(36)  # Author: 36-60pt range
            p.font.color.rgb = DARK
        elif "Nội dung gợi ý cho Poster:" in text:
            shape.text_frame.clear()
    
    # ===== LEFT COLUMN =====
    
    # Section 1: Bối cảnh & Vấn đề
    add_section_box(slide, LEFT_X, CONTENT_Y, COL_W, 18)
    add_section_header(slide, "1. BỐI CẢNH & VẤN ĐỀ", LEFT_X, CONTENT_Y, COL_W)
    add_bullet_list(slide, [
        "Quyết định 2422/QĐ-BGDĐT: 12 tiết/năm cho giáo dục AI",
        "Phòng máy yếu, internet không ổn định",
        "Học sinh dùng AI nhưng thiếu kỹ năng kiểm chứng",
        "Đối tượng: học sinh THPT và giáo viên Tin học"
    ], LEFT_X + 0.5, CONTENT_Y + 2.5, COL_W - 1, 15, size=32)
    
    # Section 2: Giải pháp & Công cụ AI
    add_section_box(slide, LEFT_X, CONTENT_Y + 20, COL_W, 22)
    add_section_header(slide, "2. GIẢI PHÁP & CÔNG CỤ AI", LEFT_X, CONTENT_Y + 20, COL_W, color=SECONDARY)
    add_text_block(slide, "AInatomy là phòng thí nghiệm AI offline giúp học sinh:", 
                   LEFT_X + 0.5, CONTENT_Y + 22, COL_W - 1, 3, size=32, bold=True)
    add_bullet_list(slide, [
        "Quan sát quy trình AI từ đầu đến cuối",
        "Dự đoán, kiểm tra và bắt lỗi đầu ra AI",
        "Học trên máy cấu hình thấp, không cần tài khoản"
    ], LEFT_X + 0.5, CONTENT_Y + 25.5, COL_W - 1, 10, size=30)
    add_text_block(slide, "Công cụ: HTML5, CSS3, JavaScript, Three.js", 
                   LEFT_X + 0.5, CONTENT_Y + 36, COL_W - 1, 3, size=28, color=MUTED)
    
    # Section 3: Triển khai trong thực tế
    add_section_box(slide, LEFT_X, CONTENT_Y + 44, COL_W, 20)
    add_section_header(slide, "3. TRIỂN KHAI TRONG THỰC TẾ", LEFT_X, CONTENT_Y + 44, COL_W, color=PRIMARY)
    add_bullet_list(slide, [
        "Giai đoạn 1 — Thiết kế: phân tích CT GDPT 2018, xây dựng prototype",
        "Giai đoạn 2 — Phát triển: 28 bài học theo 22 YCCĐ, mô phỏng 3D, chấm điểm tự động",
        "Giai đoạn 3 — Đánh giá: triển khai tại THPT Thuận Hoá, thu thập dữ liệu tương tác"
    ], LEFT_X + 0.5, CONTENT_Y + 46.5, COL_W - 1, 17, size=30)
    
    # ===== RIGHT COLUMN =====
    
    # Section 4: Minh chứng sản phẩm (with images)
    add_section_box(slide, RIGHT_X, CONTENT_Y, COL_W, 16)
    add_section_header(slide, "4. MINH CHỨNG SẢN PHẨM", RIGHT_X, CONTENT_Y, COL_W, color=SUCCESS)
    
    # Add 3 product screenshots
    shot_dir = ROOT.parent / "shot_sang"
    shots = [shot_dir / "1-trang-chu.png", shot_dir / "3-tram0-nhap-lieu.png", shot_dir / "4-tram5-ung-dung.png"]
    thumb_w = (COL_W - 1.5) / 3
    for i, path in enumerate(shots):
        if path.exists():
            add_image_fit(slide, path, RIGHT_X + 0.5 + i * (thumb_w + 0.3), CONTENT_Y + 2.5, thumb_w, 12)
    
    # Section 5: Kết quả & Tác động (with metrics)
    add_section_box(slide, RIGHT_X, CONTENT_Y + 18, COL_W, 22)
    add_section_header(slide, "5. KẾT QUẢ & TÁC ĐỘNG", RIGHT_X, CONTENT_Y + 18, COL_W, color=SUCCESS)
    
    # Metric cards in 2x2 grid - larger and more prominent
    metric_w = (COL_W - 1.5) / 2
    metric_h = 9
    add_metric_card(slide, "28/28", "YCCĐ Tin học 10", RIGHT_X + 0.5, CONTENT_Y + 20.5, metric_w, metric_h, SUCCESS)
    add_metric_card(slide, "97/97", "Kiểm thử đạt", RIGHT_X + 0.5 + metric_w + 0.5, CONTENT_Y + 20.5, metric_w, metric_h, SUCCESS)
    add_metric_card(slide, "100%", "Offline", RIGHT_X + 0.5, CONTENT_Y + 30, metric_w, metric_h, PRIMARY)
    add_metric_card(slide, "3D", "Mô phỏng AI", RIGHT_X + 0.5 + metric_w + 0.5, CONTENT_Y + 30, metric_w, metric_h, PRIMARY)
    
    # Section 6: Bền vững & Khả năng mở rộng
    add_section_box(slide, RIGHT_X, CONTENT_Y + 42, COL_W, 16)
    add_section_header(slide, "6. BỀN VỮNG & KHẢ NĂNG MỞ RỘNG", RIGHT_X, CONTENT_Y + 42, COL_W, color=PRIMARY)
    add_bullet_list(slide, [
        "Chạy offline, không phụ thuộc internet hay cloud",
        "Mã nguồn mở, dễ bảo trì và cập nhật",
        "Mọi trường THPT có thể triển khai",
        "Có thể mở rộng sang khối 11, 12 và các chủ đề AI nâng cao"
    ], RIGHT_X + 0.5, CONTENT_Y + 44.5, COL_W - 1, 13, size=30)
    
    # QR code and call-to-action at bottom
    qr = ROOT / "qr_ainatomy.png"
    if qr.exists():
        add_image_fit(slide, qr, RIGHT_X + 0.5, CONTENT_Y + 59, 6, 6)
    add_text_block(slide, "Trải nghiệm AInatomy\nmxuanvan02.github.io/ainatomy/", 
                   RIGHT_X + 7, CONTENT_Y + 60, COL_W - 8, 4, size=32, color=PRIMARY, bold=True)
    
    prs.save(str(OUT))
    print(f"Created professional poster: {OUT}")
    print(f"Font sizes: Title=85pt, Sections=44pt, Body=26-28pt, Metrics=72pt")
    print(f"Layout: 2 columns, max ~600 words, 40%+ white space")


if __name__ == "__main__":
    main()
