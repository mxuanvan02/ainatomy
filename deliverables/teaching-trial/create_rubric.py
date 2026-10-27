#!/usr/bin/env python3
"""
Tạo Bảng kiểm đánh giá năng lực AI của học sinh
Dựa trên khung năng lực số và QĐ 2422/QĐ-BGDĐT
"""

from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def create_assessment_rubric():
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    
    # Header
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("BẢNG KIỂM ĐÁNH GIÁ NĂNG LỰC AI")
    run.bold = True
    run.font.size = Pt(13)
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Dành cho giáo viên đánh giá học sinh sau khi sử dụng AInatomy")
    run.italic = True
    run.font.size = Pt(10)
    
    doc.add_paragraph()
    
    # Student info
    p = doc.add_paragraph()
    run = p.add_run("Mã học sinh: ")
    run.bold = True
    p.add_run("____________    ")
    run = p.add_run("Lớp: ")
    run.bold = True
    p.add_run("__________    ")
    run = p.add_run("Ngày đánh giá: ")
    run.bold = True
    p.add_run("__________")
    
    doc.add_paragraph()
    
    # Instructions
    p = doc.add_paragraph()
    run = p.add_run("Hướng dẫn: ")
    run.bold = True
    p.add_run("Giáo viên đánh giá từng năng lực theo thang: 0 = Không đạt, 1 = Đạt mức cơ bản, 2 = Đạt mức tốt")
    
    doc.add_paragraph()
    
    # Assessment table
    table = doc.add_table(rows=16, cols=4)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Set column widths
    for row in table.rows:
        row.cells[0].width = Cm(4.5)
        row.cells[1].width = Cm(7.5)
        row.cells[2].width = Cm(1.5)
        row.cells[3].width = Cm(3.5)
    
    # Header row
    headers = ["Năng lực", "Tiêu chí đánh giá", "Điểm\n(0-1-2)", "Minh chứng\n(ghi nhận từ AInatomy]"]
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header)
        run.bold = True
        run.font.size = Pt(10)
    
    # Content rows
    criteria = [
        # Năng lực 1: Hiểu quy trình AI
        ["1. Hiểu quy trình AI", "Trình bày được 4 bước: thu thập dữ liệu, huấn luyện, triển khai, đánh giá", "", "Câu trả lời trong Tầng 1"],
        ["", "Giải thích được tại sao dữ liệu huấn luyện ảnh hưởng đến chất lượng AI", "", "Thảo luận trên lớp"],
        ["", "Nhận biết được thiên kiến dữ liệu khi thấy kết quả AI chênh lệch", "", "Quan sát trong Tầng 1"],
        
        # Năng lực 2: Phân biệt loại AI
        ["2. Phân biệt loại AI", "Phân biệt được AI phân loại và AI tạo sinh", "", "Phiếu học tập"],
        ["", "Nêu được ví dụ cụ thể cho từng loại", "", "Câu trả lời trên lớp"],
        ["", "Giải thích được tại sao AI tạo sinh khó kiểm chứng hơn", "", "Thảo luận Tầng 2"],
        
        # Năng lực 3: Kiểm chứng AI
        ["3. Kiểm chứng AI", "Áp dụng được ít nhất 2 cách kiểm chứng (đối chiếu nguồn, kiểm tra logic, thử nghiệm)", "", "Quan sát Tầng 2"],
        ["", "Phát hiện được câu trả lời sai của AI trong 12 tình huống", "", "File JSON: số câu đúng"],
        ["", "Giải thích được lý do AI sai (thiên kiến, bịa đặt, thiếu dữ liệu)", "", "Câu trả lời trên lớp"],
        
        # Năng lực 4: Sử dụng công cụ
        ["4. Sử dụng công cụ", "Mở và điều hướng được AInatomy (Tầng 1, 2, 3)", "", "Quan sát trực tiếp"],
        ["", "Tạo được bộ dữ liệu huấn luyện với tỉ lệ tùy chỉnh", "", "File JSON: thao tác"],
        ["", "Xuất được file JSON nhật ký học tập", "", "File JSON nộp"],
        
        # Năng lực 5: Tư duy phản biện
        ["5. Tư duy phản biện", "Đặt câu hỏi về độ tin cậy của kết quả AI", "", "Câu hỏi trên lớp"],
        ["", "Đề xuất được cách khắc phục khi AI sai", "", "Phiếu học tập"],
        ["", "Nhận thức được trách nhiệm của người sử dụng AI", "", "Phiếu tự đánh giá"],
    ]
    
    row_idx = 1
    for criterion in criteria:
        for i, text in enumerate(criterion):
            cell = table.cell(row_idx, i)
            p = cell.paragraphs[0]
            run = p.add_run(text)
            run.font.size = Pt(9)
            if i == 0 and text:  # Bold for energy name
                run.bold = True
            if i == 2:  # Center score column
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        row_idx += 1
    
    doc.add_paragraph()
    
    # Scoring guide
    p = doc.add_paragraph()
    run = p.add_run("Hướng dẫn chấm điểm:")
    run.bold = True
    
    p = doc.add_paragraph("• 0 điểm: Học sinh không thực hiện được tiêu chí")
    p = doc.add_paragraph("• 1 điểm: Học sinh thực hiện được ở mức cơ bản, cần hỗ trợ thêm")
    p = doc.add_paragraph("• 2 điểm: Học sinh thực hiện tốt, độc lập")
    
    doc.add_paragraph()
    
    # Total score
    p = doc.add_paragraph()
    run = p.add_run("Tổng điểm: ")
    run.bold = True
    run.font.size = Pt(12)
    p.add_run("______ / 30")
    
    doc.add_paragraph()
    
    # Interpretation
    p = doc.add_paragraph()
    run = p.add_run("Diễn giải kết quả:")
    run.bold = True
    
    p = doc.add_paragraph("• 24-30 điểm: Hiểu sâu về AI, có kỹ năng kiểm chứng tốt")
    p = doc.add_paragraph("• 18-23 điểm: Hiểu khá về AI, có kỹ năng kiểm chứng cơ bản")
    p = doc.add_paragraph("• 12-17 điểm: Hiểu ở mức cơ bản, cần luyện tập thêm")
    p = doc.add_paragraph("• Dưới 12 điểm: Cần hỗ trợ thêm, chưa nắm được khái niệm cốt lõi")
    
    doc.add_paragraph()
    
    # Teacher comments
    p = doc.add_paragraph()
    run = p.add_run("Nhận xét của giáo viên:")
    run.bold = True
    
    p = doc.add_paragraph("_________________________________________________________________")
    p = doc.add_paragraph("_________________________________________________________________")
    p = doc.add_paragraph("_________________________________________________________________")
    
    doc.add_paragraph()
    doc.add_paragraph()
    
    # Signature
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("Giáo viên đánh giá")
    run.italic = True
    
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("(Ký và ghi rõ họ tên)")
    run.italic = True
    run.font.size = Pt(10)
    
    # Save
    output_path = "/home/hitokiri/ieeai2026/soi-ai/deliverables/teaching-trial/Bang_kiem_danh_gia.docx"
    doc.save(output_path)
    print(f"✓ Đã tạo bảng kiểm đánh giá: {output_path}")

if __name__ == "__main__":
    create_assessment_rubric()
