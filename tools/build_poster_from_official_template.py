#!/usr/bin/env python3
"""Build iEEAI poster by editing the official BTC poster template."""
from pathlib import Path
from copy import deepcopy
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "references/ieeai-2026/mau_poster_2026.pptx"
OUT = ROOT / "poster_ieeai2026_official_template.pptx"

BLUE = RGBColor(24, 67, 122)
CYAN = RGBColor(28, 146, 190)
GOLD = RGBColor(219, 160, 35)
GREEN = RGBColor(37, 139, 93)
DARK = RGBColor(35, 45, 58)
MUTED = RGBColor(95, 105, 115)
PALE = RGBColor(245, 248, 252)
WHITE = RGBColor(255, 255, 255)
LINE = RGBColor(205, 215, 225)


def emu(value):
    return Inches(value)


def add_box(slide, x, y, w, h, fill=WHITE, line=LINE, radius=False):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, emu(x), emu(y), emu(w), emu(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line
    shape.line.width = Pt(1.2)
    return shape


def add_text(slide, text, x, y, w, h, size=18, color=DARK, bold=False,
             align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, font="Arial"):
    box = slide.shapes.add_textbox(emu(x), emu(y), emu(w), emu(h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.margin_left = emu(0.10)
    tf.margin_right = emu(0.10)
    tf.margin_top = emu(0.05)
    tf.margin_bottom = emu(0.05)
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.font.name = font
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    return box


def add_section(slide, number, title, x, y, w, h, body, accent=BLUE, size=16):
    add_box(slide, x, y, w, h, fill=PALE, line=LINE, radius=True)
    add_box(slide, x, y, w, 0.52, fill=accent, line=accent, radius=True)
    add_text(slide, f"{number}. {title}", x + 0.12, y + 0.06, w - 0.24, 0.38,
             size=17, color=WHITE, bold=True, valign=MSO_ANCHOR.MIDDLE)
    add_text(slide, body, x + 0.14, y + 0.68, w - 0.28, h - 0.78,
             size=size, color=DARK)


def add_metric(slide, value, label, x, y, w, h, color=GREEN):
    add_box(slide, x, y, w, h, fill=WHITE, line=color, radius=True)
    add_text(slide, value, x + 0.06, y + 0.18, w - 0.12, 0.52,
             size=27, color=color, bold=True, align=PP_ALIGN.CENTER)
    add_text(slide, label, x + 0.06, y + 0.82, w - 0.12, h - 0.88,
             size=13, color=DARK, bold=True, align=PP_ALIGN.CENTER)


def add_picture_fit(slide, path, x, y, w, h):
    im = Image.open(path)
    ratio = im.width / im.height
    box_ratio = w / h
    if ratio >= box_ratio:
        dw, dh = w, w / ratio
    else:
        dh, dw = h, h * ratio
    dx, dy = x + (w - dw) / 2, y + (h - dh) / 2
    frame = add_box(slide, x, y, w, h, fill=WHITE, line=LINE, radius=True)
    slide.shapes.add_picture(str(path), emu(dx), emu(dy), width=emu(dw), height=emu(dh))
    return frame


def remove_shape(slide, shape):
    sp = shape._element
    sp.getparent().remove(sp)


def main():
    prs = Presentation(str(TEMPLATE))
    slide = prs.slides[0]

    # Replace official template placeholders.
    for shape in list(slide.shapes):
        text = getattr(shape, "text", "")
        if "[VUI LÒNG THAY TÊN SẢN PHẨM" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "AINATOMY — PHÒNG THÍ NGHIỆM AI OFFLINE"
            p.alignment = PP_ALIGN.CENTER
            p.font.name = "Arial"
            p.font.size = Pt(31)
            p.font.bold = True
            p.font.color.rgb = BLUE
        elif "Giáo viên thực hiện:" in text:
            shape.text_frame.clear()
            p = shape.text_frame.paragraphs[0]
            p.text = "Giáo viên thực hiện: Mai Xuân Văn\nĐơn vị công tác: Trường THPT Thuận Hoá, Đại học Sư Phạm, Đại học Huế"
            p.font.name = "Arial"
            p.font.size = Pt(19)
            p.font.color.rgb = DARK
        elif "Nội dung gợi ý cho Poster:" in text:
            shape.text_frame.clear()

    # Content canvas inside the official dashed content region.
    x0, y0, W, H = 3.45, 12.75, 24.65, 25.25
    gap = 0.35
    col = (W - gap) / 2
    left, right = x0, x0 + col + gap

    # Remove the old instruction box border only; keep official header and title.
    # The group border remains as the official content boundary.

    add_section(slide, "1", "BỐI CẢNH & VẤN ĐỀ", left, y0, col, 4.55,
                "• QĐ 2422/QĐ-BGDĐT: 12 tiết/năm cho giáo dục AI.\n"
                "• Phòng máy yếu, internet không ổn định.\n"
                "• Học sinh dùng AI nhưng thiếu kỹ năng kiểm chứng.\n\n"
                "Đối tượng hưởng lợi: học sinh THPT và giáo viên Tin học.", BLUE, 15)

    add_section(slide, "2", "GIẢI PHÁP & CÔNG CỤ AI", left, y0 + 4.9, col, 5.3,
                "AInatomy là phòng thí nghiệm AI offline giúp học sinh:\n\n"
                "• Quan sát quy trình AI từ đầu đến cuối.\n"
                "• Dự đoán, kiểm tra và bắt lỗi đầu ra AI.\n"
                "• Học trên máy cấu hình thấp, không cần tài khoản.\n\n"
                "Công cụ: HTML5, CSS3, JavaScript, Three.js.", CYAN, 15)

    add_section(slide, "3", "TRIỂN KHAI TRONG THỰC TẾ", left, y0 + 10.55, col, 4.7,
                "Giai đoạn 1 — Thiết kế: phân tích CT GDPT 2018, xây dựng prototype.\n\n"
                "Giai đoạn 2 — Phát triển: 28 bài học theo 22 YCCĐ, mô phỏng 3D, chấm điểm tự động.\n\n"
                "Giai đoạn 3 — Đánh giá: triển khai tại THPT Thuận Hoá, thu thập dữ liệu tương tác.", GOLD, 15)

    # Right column: evidence and results.
    add_box(slide, right, y0, col, 3.3, fill=WHITE, line=LINE, radius=True)
    add_text(slide, "MINH CHỨNG SẢN PHẨM", right + 0.12, y0 + 0.08, col - 0.24, 0.4,
             size=18, color=BLUE, bold=True)
    shot_dir = ROOT.parent / "shot_sang"
    shots = [shot_dir / "1-trang-chu.png", shot_dir / "3-tram0-nhap-lieu.png", shot_dir / "4-tram5-ung-dung.png"]
    thumb_w = (col - 0.5) / 3
    for i, path in enumerate(shots):
        if path.exists():
            add_picture_fit(slide, path, right + 0.12 + i * (thumb_w + 0.08), y0 + 0.65, thumb_w, 2.25)

    add_box(slide, right, y0 + 3.65, col, 4.35, fill=PALE, line=LINE, radius=True)
    add_text(slide, "4. KẾT QUẢ & TÁC ĐỘNG", right + 0.12, y0 + 3.78, col - 0.24, 0.45,
             size=18, color=GREEN, bold=True)
    metric_y = y0 + 4.45
    mw = (col - 0.55) / 2
    add_metric(slide, "28/28", "YCCĐ Tin học 10", right + 0.12, metric_y, mw, 1.55, GREEN)
    add_metric(slide, "97/97", "kiểm thử đạt", right + 0.25 + mw, metric_y, mw, 1.55, GREEN)
    add_metric(slide, "100%", "offline", right + 0.12, metric_y + 1.78, mw, 1.55, CYAN)
    add_metric(slide, "3D", "mô phỏng AI", right + 0.25 + mw, metric_y + 1.78, mw, 1.55, CYAN)

    add_section(slide, "5", "BỀN VỮNG & KHẢ NĂNG MỞ RỘNG", right, y0 + 8.35, col, 5.0,
                "• Chạy offline, không phụ thuộc internet hay cloud.\n"
                "• Mã nguồn mở, dễ bảo trì và cập nhật.\n"
                "• Mọi trường THPT có thể triển khai.\n"
                "• Có thể mở rộng sang khối 11, 12 và các chủ đề AI nâng cao.", BLUE, 15)

    # QR and call-to-action inside lower content region.
    qr = ROOT / "qr_ainatomy.png"
    if qr.exists():
        add_picture_fit(slide, qr, right + 0.1, y0 + 13.65, 2.0, 2.0)
    add_text(slide, "Trải nghiệm AInatomy\nmxuanvan02.github.io/ainatomy/",
             right + 2.35, y0 + 14.0, col - 2.55, 1.2, size=17, color=BLUE, bold=True)

    prs.save(str(OUT))
    print(f"Created {OUT}")


if __name__ == "__main__":
    main()
