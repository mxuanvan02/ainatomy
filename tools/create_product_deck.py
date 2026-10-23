from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path
from PIL import Image

ROOT=Path('/home/hitokiri/ieeai2026'); REPO=ROOT/'soi-ai'
P=Presentation(); P.slide_width=Inches(13.333); P.slide_height=Inches(7.5)
WHITE=RGBColor(255,255,255); NAVY=RGBColor(24,55,91); BLUE=RGBColor(0,102,204); TEXT=RGBColor(45,55,65); MUTED=RGBColor(100,110,120); BORDER=RGBColor(210,220,230); PALE=RGBColor(242,247,252); GOLD=RGBColor(211,153,42); GREEN=RGBColor(37,139,93); PURPLE=RGBColor(135,78,170)
DHSP=str(REPO/'logo_dhsp_hue.png'); THPT=str(REPO/'logo_thpt_thuan_hoa.png')
I={k:str(ROOT/p) for k,p in {'home':'shot_sang/1-trang-chu.png','tram0':'shot_sang/3-tram0-nhap-lieu.png','tram5':'shot_sang/4-tram5-ung-dung.png','situation':'shot_sang/6-tinh-huong.png','menu':'out/an_hoc_sinh/02_menu.jpg','read':'out/an_hoc_sinh/03_man1_doan1_doc_va_doan.jpg','write':'out/an_hoc_sinh/05_man1_doan1_viet_du.jpg','answer':'out/an_hoc_sinh/06_man1_doan1_dap_an.jpg','evidence':'out/an_hoc_sinh/08_man1_bang_dau_hieu.jpg','prompt':'out/an_hoc_sinh/17_man4_da_chon_va_viet_lai.jpg','export':'out/an_hoc_sinh/25_da_gui_tep.jpg'}.items()}

def shp(s,x,y,w,h,fill=WHITE,line=BORDER,kind=MSO_SHAPE.ROUNDED_RECTANGLE):
    z=s.shapes.add_shape(kind,Inches(x),Inches(y),Inches(w),Inches(h)); z.fill.solid(); z.fill.fore_color.rgb=fill; z.line.color.rgb=line; z.line.width=Pt(.8); return z

def tx(s,x,y,w,h,t,sz=16,col=TEXT,bold=False,align=PP_ALIGN.LEFT):
    z=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); f=z.text_frame; f.clear(); f.word_wrap=True; f.margin_left=Inches(.06); f.margin_right=Inches(.06); f.margin_top=Inches(.04); p=f.paragraphs[0]; p.text=t; p.alignment=align; p.font.name='Arial'; p.font.size=Pt(sz); p.font.bold=bold; p.font.color.rgb=col; return z

def head(s,section,n):
    r=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,P.slide_width,Pt(4)); r.fill.solid(); r.fill.fore_color.rgb=BLUE; r.line.fill.background(); s.shapes.add_picture(DHSP,Inches(.42),Inches(.17),width=Inches(.58),height=Inches(.58)); s.shapes.add_picture(THPT,Inches(1.12),Inches(.17),width=Inches(.58),height=Inches(.58)); tx(s,1.82,.17,4.4,.26,'Trường THPT Thuận Hoá',11,NAVY,True); tx(s,1.82,.45,4.5,.22,'Trường Đại học Sư Phạm, Đại học Huế',9.5,MUTED); tx(s,6,.27,6.8,.3,section,14,NAVY,True,PP_ALIGN.RIGHT); d=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(.42),Inches(1),Inches(12.5),Pt(1)); d.fill.solid(); d.fill.fore_color.rgb=BORDER; d.line.fill.background(); tx(s,.48,7.08,4,.2,'GV: Mai Xuân Văn',9,MUTED); tx(s,12.35,7.08,.45,.2,str(n),9,MUTED,False,PP_ALIGN.RIGHT)

def title(s,t,sub=''):
    tx(s,.55,1.22,12.2,.42,t,26,NAVY,True)
    if sub: tx(s,.58,1.68,12,.28,sub,12,MUTED)

def pic(s,path,x,y,w,h):
    # Khung ảnh cố định; giữ nguyên tỉ lệ, không kéo giãn ảnh chụp thật.
    shp(s,x-.04,y-.04,w+.08,h+.08,PALE,BORDER,MSO_SHAPE.RECTANGLE)
    im=Image.open(path)
    ratio=im.width/im.height
    box_ratio=w/h
    if ratio >= box_ratio:
        draw_w=w; draw_h=w/ratio
    else:
        draw_h=h; draw_w=h*ratio
    draw_x=x+(w-draw_w)/2; draw_y=y+(h-draw_h)/2
    s.shapes.add_picture(path,Inches(draw_x),Inches(draw_y),width=Inches(draw_w),height=Inches(draw_h))

def card(s,x,y,w,h,hdr,body,accent=BLUE):
    shp(s,x,y,w,h); q=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Pt(5),Inches(h)); q.fill.solid(); q.fill.fore_color.rgb=accent; q.line.fill.background(); tx(s,x+.18,y+.15,w-.3,.28,hdr,14,accent,True); tx(s,x+.18,y+.58,w-.3,h-.7,body,14,TEXT)

def metric(s,x,y,w,num,label,accent=BLUE):
    shp(s,x,y,w,1.25,PALE,BORDER); tx(s,x,y+.18,w,.4,num,27,accent,True,PP_ALIGN.CENTER); tx(s,x+.1,y+.7,w-.2,.25,label,11,NAVY,True,PP_ALIGN.CENTER)

def slide(section,n,t,sub=''):
    s=P.slides.add_slide(P.slide_layouts[6]); head(s,section,n); title(s,t,sub); return s

s=P.slides.add_slide(P.slide_layouts[6]); head(s,'BÁO CÁO SẢN PHẨM',1); pic(s,I['home'],.7,1.35,11.95,4.6); shp(s,.7,5.98,11.95,.72,NAVY,NAVY,MSO_SHAPE.RECTANGLE); tx(s,.95,6.12,11.45,.3,'Học sinh không chỉ hỏi AI — các em học cách quan sát, kiểm tra và bắt lỗi AI.',20,WHITE,True,PP_ALIGN.CENTER)
s=slide('01 · BỐI CẢNH',2,'Một nhu cầu rất cụ thể trong lớp học','Dạy AI không dừng ở việc cho học sinh dùng một công cụ'); card(s,.7,2.15,3.85,2.15,'KHÓ NHÌN THẤY','Dữ liệu, mô hình, thiên kiến và lỗi AI thường nằm “bên trong” hộp đen.',BLUE); card(s,4.75,2.15,3.85,2.15,'KHÓ TRIỂN KHAI','Phòng máy có thể yếu hoặc mất mạng; không thể đặt tài khoản/API làm điều kiện bắt buộc.',GOLD); card(s,8.8,2.15,3.85,2.15,'KHÓ KIỂM CHỨNG','Học sinh dễ nhận đáp án mà chưa hình thành thói quen hỏi lại và kiểm tra.',GREEN); pic(s,I['menu'],.9,4.75,2.1,1.85); pic(s,I['situation'],3.35,4.75,4.1,1.85); pic(s,I['evidence'],8,4.75,3.9,1.85)
s=slide('02 · GIẢI PHÁP',3,'AInatomy biến “hộp đen” thành trải nghiệm có thể quan sát'); steps=[('01','Tình huống'),('02','Dự đoán'),('03','Thao tác'),('04','Phản hồi')]
for i,(no,lab) in enumerate(steps):
 x=.9+i*3.05; shp(s,x,2.25,2.25,1,PALE,BORDER); tx(s,x+.12,2.38,.5,.3,no,22,BLUE,True); tx(s,x+.7,2.42,1.35,.25,lab,16,NAVY,True)
 if i<3: tx(s,x+2.38,2.48,.6,.25,'→',24,GOLD,True,PP_ALIGN.CENTER)
for i,k in enumerate(['read','write','answer','evidence']): pic(s,I[k],.85+i*3.05,4.05,2.45,2.15)
tx(s,.85,6.35,11.6,.3,'Một hoạt động hoàn chỉnh: học sinh phán đoán trước, thao tác, nhận phản hồi rồi tự rút ra kết luận.',17,NAVY,True,PP_ALIGN.CENTER)
s=slide('03 · THAO TÁC THẬT',4,'Một phiên học diễn ra như thế nào?','Các trạng thái dưới đây là ảnh chụp thật của sản phẩm')
for i,k in enumerate(['read','write','answer','evidence']): pic(s,I[k],.75+i*3.05,2,2.55,3.95); tx(s,.75+i*3.05,6.1,2.55,.25,f'{i+1} · '+['Đọc tình huống','Đưa ra phán đoán','Nhận kết quả','Xem dấu hiệu'][i],10,MUTED,False,PP_ALIGN.CENTER)
tx(s,.85,6.55,11.6,.28,'Giá trị sư phạm nằm ở khoảng thời gian trước khi xem đáp án.',17,NAVY,True,PP_ALIGN.CENTER)
s=slide('04 · TÍNH NĂNG 1',5,'Đấu trường bắt lỗi AI','Học sinh phán xử đầu ra AI thay vì tin ngay vào câu trả lời'); pic(s,I['situation'],.7,2,6.3,4.35); card(s,7.45,2,5.1,1.25,'BƯỚC 1 · NHẬN DIỆN','Đọc một câu trả lời có thể đúng hoặc có lỗi.',BLUE); card(s,7.45,3.48,5.1,1.25,'BƯỚC 2 · PHÁN ĐOÁN','Chọn có lỗi/không có lỗi và nêu lý do.',GOLD); card(s,7.45,4.96,5.1,1.39,'BƯỚC 3 · KIỂM TRA','Xem phản hồi, dấu hiệu và nhóm lỗi tương ứng.',GREEN)
s=slide('05 · TÍNH NĂNG 2',6,'Nhà máy AI: nhìn thấy các bước phía sau một kết quả'); pic(s,I['tram0'],.65,2,5.9,4.2); pic(s,I['tram5'],6.8,2,5.9,4.2); shp(s,.65,6.35,12.05,.45,PALE,BORDER); tx(s,.85,6.45,11.65,.2,'Học sinh đi từ dữ liệu đầu vào đến cách AI được dùng — không chỉ nhìn vào kết quả cuối.',16,NAVY,True,PP_ALIGN.CENTER)
s=slide('06 · TÍNH NĂNG 3',7,'Xưởng huấn luyện: dữ liệu thay đổi thì kết quả cũng thay đổi'); pic(s,I['home'],.7,2,6,3.75); card(s,7.15,2,5.3,1.25,'DỮ LIỆU LỆCH','Học sinh quan sát mô hình học từ một bộ dữ liệu không cân bằng.',BLUE); card(s,7.15,3.48,5.3,1.25,'KẾT QUẢ KHÁC NHAU','So sánh kết quả trên các nhóm dữ liệu khác nhau.',GOLD); card(s,7.15,4.96,5.3,.8,'BÀI HỌC','AI không tự nhiên “khách quan”; dữ liệu và cách kiểm tra rất quan trọng.',GREEN); tx(s,.8,6.25,11.7,.28,'Các tỉ lệ trong slide là kết quả của mô phỏng trong sản phẩm, không phải số liệu tác động lớp học.',10,MUTED,False,PP_ALIGN.CENTER)
s=slide('07 · TÍCH HỢP CHƯƠNG TRÌNH',8,'Từ hoạt động trong app đến bài học Tin học 10'); metric(s,.8,2.05,2.75,'28','bài SGK được đối chiếu'); metric(s,3.8,2.05,2.75,'22/22','YCCĐ lớp 10'); metric(s,6.8,2.05,2.75,'12','tiết đề xuất'); metric(s,9.8,2.05,2.65,'5','phân hệ học tập'); pic(s,I['tram0'],.85,4,3.6,2.25); pic(s,I['situation'],4.85,4,3.6,2.25); pic(s,I['prompt'],8.85,4,3.6,2.25)
s=slide('08 · MINH CHỨNG CHO GIÁO VIÊN',9,'Sản phẩm không chỉ cho học sinh thao tác — còn để lại minh chứng'); pic(s,I['export'],.75,2,4.4,4.3); card(s,5.55,2,3,1.55,'THEO DÕI','Hoạt động được ghi theo mã ẩn danh.',BLUE); card(s,8.8,2,3.7,1.55,'PHẢN HỒI','Nhiệm vụ có nhãn đúng cố định được phản hồi ngay.',GOLD); card(s,5.55,3.85,3,1.55,'XUẤT TỆP','Giáo viên có thể xuất dữ liệu làm minh chứng.',GREEN); card(s,8.8,3.85,3.7,1.55,'BẢO VỆ DỮ LIỆU','Không yêu cầu tài khoản học sinh.',PURPLE)
s=slide('09 · KIỂM TRA SẢN PHẨM',10,'Những gì đã được kiểm tra','Đây là kiểm thử sản phẩm, không phải số liệu tác động học tập'); metric(s,.8,2.2,2.8,'97/97','tiêu chí nghiệm thu'); metric(s,3.85,2.2,2.8,'22/22','YCCĐ được phủ'); metric(s,6.9,2.2,2.8,'0','lỗi nội dung'); metric(s,9.95,2.2,2.5,'offline','chạy không cần mạng'); pic(s,I['home'],.85,4.15,4.1,2); pic(s,I['answer'],5.25,4.15,3,2); pic(s,I['export'],8.55,4.15,3.8,2)
s=slide('10 · TRIỂN KHAI VÀ GIỚI HẠN',11,'Bằng chứng hiện có và bước cần làm tiếp'); card(s,.8,2.05,5.7,3.75,'ĐÃ CÓ','Bản chạy thử công khai\nBộ ảnh thao tác sản phẩm\nVideo demo nháp\nCó thể chạy offline, USB hoặc mạng nội bộ',GREEN); card(s,6.8,2.05,5.7,3.75,'CẦN BỔ SUNG','Dữ liệu từ lớp học thật\nPhản hồi học sinh và giáo viên khác\nĐo tác động trước/sau\nBiên bản triển khai thực tế',GOLD); tx(s,.95,6.25,11.4,.32,'Không dùng ảnh thao tác phần mềm để thay thế cho bằng chứng tác động lớp học.',17,NAVY,True,PP_ALIGN.CENTER)
s=slide('11 · BỀN VỮNG VÀ NHÂN RỘNG',12,'Có thể bắt đầu từ một phòng máy'); card(s,.8,2.35,3.65,2.3,'CHÉP','Chép thư mục vào USB hoặc máy trường.',BLUE); card(s,4.8,2.35,3.65,2.3,'MỞ','Mở sản phẩm bằng trình duyệt.',GOLD); card(s,8.8,2.35,3.65,2.3,'DẠY','Giáo viên tổ chức hoạt động theo bài học.',GREEN); pic(s,I['menu'],1.15,5.15,2,1.45); pic(s,I['tram0'],4.95,5.15,2,1.45); pic(s,I['export'],8.75,5.15,2,1.45)
s=slide('12 · KẾT LUẬN',13,'Một sản phẩm có thể mở ra một cách học AI khác'); pic(s,I['home'],.7,2,6.3,3.9); card(s,7.45,2,5.05,1.35,'GIÁ TRỊ CỐT LÕI','Dạy học sinh kiểm chứng AI bằng trải nghiệm trực tiếp.',BLUE); card(s,7.45,3.65,5.05,1.35,'MINH CHỨNG HIỆN CÓ','Có thao tác thật, ảnh chụp thật và đầu ra có thể kiểm tra.',GOLD); card(s,7.45,5.3,5.05,1,'BƯỚC TIẾP THEO','Triển khai lớp học và thu dữ liệu tác động thật.',GREEN); tx(s,.8,6.55,11.8,.25,'https://mxuanvan02.github.io/ainatomy/  ·  GV: Mai Xuân Văn',12,BLUE,False,PP_ALIGN.CENTER)

P.save(REPO/'template_thuanhoa.pptx'); print('created',len(P.slides))
