from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pathlib import Path
from PIL import Image

ROOT=Path('/home/hitokiri/ieeai2026'); REPO=ROOT/'soi-ai'
P=Presentation(); P.slide_width=Inches(13.333); P.slide_height=Inches(7.5)
WHITE=RGBColor(255,255,255); NAVY=RGBColor(24,55,91); BLUE=RGBColor(0,102,204); TEXT=RGBColor(45,55,65); MUTED=RGBColor(100,110,120); BORDER=RGBColor(210,220,230); PALE=RGBColor(242,247,252); GOLD=RGBColor(211,153,42); GREEN=RGBColor(37,139,93); PURPLE=RGBColor(135,78,170); RED=RGBColor(220,50,50)
DHSP=str(REPO/'logo_dhsp_hue.png'); THPT=str(REPO/'logo_thpt_thuan_hoa.png')
I={k:str(ROOT/p) for k,p in {'home':'shot_sang/1-trang-chu.png','tram0':'shot_sang/3-tram0-nhap-lieu.png','tram5':'shot_sang/4-tram5-ung-dung.png','situation':'shot_sang/6-tinh-huong.png','menu':'out/an_hoc_sinh/02_menu.jpg','read':'out/an_hoc_sinh/03_man1_doan1_doc_va_doan.jpg','write':'out/an_hoc_sinh/05_man1_doan1_viet_du.jpg','answer':'out/an_hoc_sinh/06_man1_doan1_dap_an.jpg','evidence':'out/an_hoc_sinh/08_man1_bang_dau_hieu.jpg','prompt':'out/an_hoc_sinh/17_man4_da_chon_va_viet_lai.jpg','export':'out/an_hoc_sinh/25_da_gui_tep.jpg'}.items()}

def shp(s,x,y,w,h,fill=WHITE,line=BORDER,kind=MSO_SHAPE.ROUNDED_RECTANGLE,lw=.8):
    z=s.shapes.add_shape(kind,Inches(x),Inches(y),Inches(w),Inches(h)); z.fill.solid(); z.fill.fore_color.rgb=fill; z.line.color.rgb=line; z.line.width=Pt(lw); return z

def tx(s,x,y,w,h,t,sz=16,col=TEXT,bold=False,align=PP_ALIGN.LEFT):
    z=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); f=z.text_frame; f.clear(); f.word_wrap=True; f.margin_left=Inches(.06); f.margin_right=Inches(.06); f.margin_top=Inches(.04); p=f.paragraphs[0]; p.text=t; p.alignment=align; p.font.name='Arial'; p.font.size=Pt(sz); p.font.bold=bold; p.font.color.rgb=col; return z

def head(s,section,n):
    r=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,P.slide_width,Pt(4)); r.fill.solid(); r.fill.fore_color.rgb=BLUE; r.line.fill.background(); s.shapes.add_picture(DHSP,Inches(.42),Inches(.17),width=Inches(.58),height=Inches(.58)); s.shapes.add_picture(THPT,Inches(1.12),Inches(.17),width=Inches(.58),height=Inches(.58)); tx(s,1.82,.17,4.4,.26,'Trường THPT Thuận Hoá',11,NAVY,True); tx(s,1.82,.45,4.5,.22,'Trường Đại học Sư Phạm, Đại học Huế',9.5,MUTED); tx(s,6,.27,6.8,.3,section,14,NAVY,True,PP_ALIGN.RIGHT); d=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(.42),Inches(1),Inches(12.5),Pt(1)); d.fill.solid(); d.fill.fore_color.rgb=BORDER; d.line.fill.background(); tx(s,.48,7.08,4,.2,'GV: Mai Xuân Văn',9,MUTED); tx(s,12.35,7.08,.45,.2,str(n),9,MUTED,False,PP_ALIGN.RIGHT)

def title(s,t,sub=''):
    tx(s,.55,1.22,12.2,.42,t,26,NAVY,True)
    if sub: tx(s,.58,1.68,12,.28,sub,12,MUTED)

def pic(s,path,x,y,w,h):
    shp(s,x-.04,y-.04,w+.08,h+.08,PALE,BORDER,MSO_SHAPE.RECTANGLE)
    im=Image.open(path); ratio=im.width/im.height; box_ratio=w/h
    if ratio>=box_ratio: dw=w; dh=w/ratio
    else: dh=h; dw=h*ratio
    dx=x+(w-dw)/2; dy=y+(h-dh)/2
    s.shapes.add_picture(path,Inches(dx),Inches(dy),width=Inches(dw),height=Inches(dh))

def highlight(s,x,y,w,h,label=''):
    """Highlight đỏ để thêm animation Appear trong PowerPoint"""
    z=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    z.fill.background()
    z.line.color.rgb=RED; z.line.width=Pt(4)
    if label:
        tf=z.text_frame; tf.clear(); tf.word_wrap=True
        p=tf.paragraphs[0]; p.text=label; p.alignment=PP_ALIGN.CENTER
        p.font.name='Arial'; p.font.size=Pt(14); p.font.bold=True; p.font.color.rgb=RED

def card(s,x,y,w,h,hdr,body,accent=BLUE):
    shp(s,x,y,w,h); q=s.shapes.add_shape(MSO_SHAPE.RECTANGLE,Inches(x),Inches(y),Pt(5),Inches(h)); q.fill.solid(); q.fill.fore_color.rgb=accent; q.line.fill.background(); tx(s,x+.18,y+.15,w-.3,.28,hdr,14,accent,True); tx(s,x+.18,y+.58,w-.3,h-.7,body,14,TEXT)

def metric(s,x,y,w,num,label,accent=BLUE):
    shp(s,x,y,w,1.25,PALE,BORDER); tx(s,x,y+.18,w,.4,num,27,accent,True,PP_ALIGN.CENTER); tx(s,x+.1,y+.7,w-.2,.25,label,11,NAVY,True,PP_ALIGN.CENTER)

def slide(section,n,t,sub=''):
    s=P.slides.add_slide(P.slide_layouts[6]); head(s,section,n); title(s,t,sub); return s

def notes(s,text):
    """Thêm speaker notes"""
    ns=s.notes_slide; tf=ns.notes_text_frame; tf.text=text

# ===== SLIDE 1: BÌA =====
s=P.slides.add_slide(P.slide_layouts[6]); head(s,'BÁO CÁO SẢN PHẨM',1)
pic(s,I['home'],.7,1.35,11.95,4.6)
shp(s,.7,5.98,11.95,.72,NAVY,NAVY,MSO_SHAPE.RECTANGLE)
tx(s,.95,6.12,11.45,.3,'Học sinh không chỉ hỏi AI — các em học cách quan sát, kiểm tra và bắt lỗi AI.',20,WHITE,True,PP_ALIGN.CENTER)
notes(s,"""KỊCH BẢN VIDEO 5 PHÚT — SLIDE 1/15 (20 giây)

[Lời nói]
"Kính chào Hội đồng. Tôi là Mai Xuân Văn, giáo viên Tin học Trường THPT Thuận Hoá, Đại học Sư Phạm Huế. Hôm nay tôi xin giới thiệu AInatomy — một phòng thí nghiệm AI offline giúp học sinh không chỉ hỏi AI, mà còn học cách quan sát, kiểm tra và bắt lỗi AI."

[Animation]
- Không có highlight ở slide này.
""")

# ===== SLIDE 2: MỤC LỤC =====
s=slide('MỤC LỤC',2,'Nội dung báo cáo','5 phần chính theo thể lệ cuộc thi')
sections=[('01','Bối cảnh và vấn đề'),('02','Giải pháp và công cụ AI'),('03','Quá trình triển khai'),('04','Kết quả và tác động'),('05','Bền vững và nhân rộng')]
for i,(no,lab) in enumerate(sections):
    y=2.2+i*.95; shp(s,.9,y,11.5,.75,PALE,BORDER)
    tx(s,1.1,y+.12,.6,.5,no,24,BLUE,True)
    tx(s,1.9,y+.22,10,.3,lab,20,NAVY,True)
notes(s,"""KỊCH BẢN — SLIDE 2/15 (15 giây)

[Lời nói]
"Bài trình bày gồm 5 phần: bối cảnh và vấn đề, giải pháp và công cụ AI, quá trình triển khai, kết quả và tác động, cuối cùng là tính bền vững và khả năng nhân rộng."

[Animation]
- Không có highlight.
""")

# ===== SLIDE 3: GIỚI THIỆU SẢN PHẨM =====
s=slide('GIỚI THIỆU',3,'AInatomy — Phòng thí nghiệm AI offline','Sản phẩm đang chạy và có thể trải nghiệm')
pic(s,I['home'],.7,2,7,4.35)
card(s,8.1,2,4.3,1.25,'ĐỐI TƯỢNG','Học sinh THPT, đặc biệt lớp 10.',BLUE)
card(s,8.1,3.48,4.3,1.25,'PHẠM VI','28 bài SGK Tin học 10, 22/22 YCCĐ.',GOLD)
card(s,8.1,4.96,4.3,1.39,'VẬN HÀNH','Offline, không tài khoản, không API.',GREEN)
highlight(s,1.5,2.8,2.5,1.2,'Menu chính')
highlight(s,4.5,3.5,2.8,1.5,'Khu vực hoạt động')
notes(s,"""KỊCH BẢN — SLIDE 3/15 (20 giây)

[Lời nói]
"Đây là giao diện chính của AInatomy. Sản phẩm hướng đến học sinh THPT, đặc biệt lớp 10, phủ 28 bài SGK và 22 yêu cầu cần đạt theo QĐ 2422. Điểm quan trọng: AInatomy chạy hoàn toàn offline, không cần tài khoản hay API."

[Animation]
- Click 1: Hiện highlight "Menu chính" — "Học sinh chọn hoạt động từ menu này."
- Click 2: Hiện highlight "Khu vực hoạt động" — "Đây là nơi học sinh thao tác và quan sát."
""")

# ===== SLIDE 4: BỐI CẢNH VÀ VẤN ĐỀ =====
s=slide('01 · BỐI CẢNH',4,'Ba khó khăn rất cụ thể trong lớp học','Dạy AI không dừng ở việc cho học sinh dùng một công cụ')
card(s,.7,2.15,3.85,2.15,'KHÓ NHÌN THẤY','Dữ liệu, mô hình, thiên kiến và lỗi AI thường nằm "bên trong" hộp đen.',BLUE)
card(s,4.75,2.15,3.85,2.15,'KHÓ TRIỂN KHAI','Phòng máy có thể yếu hoặc mất mạng; không thể đặt tài khoản/API làm điều kiện bắt buộc.',GOLD)
card(s,8.8,2.15,3.85,2.15,'KHÓ KIỂM CHỨNG','Học sinh dễ nhận đáp án mà chưa hình thành thói quen hỏi lại và kiểm tra.',GREEN)
pic(s,I['menu'],.9,4.75,2.1,1.85); pic(s,I['situation'],3.35,4.75,4.1,1.85); pic(s,I['evidence'],8,4.75,3.9,1.85)
highlight(s,1.3,5.2,1.3,.8,'Vào hoạt động')
highlight(s,4.5,5.3,2.2,1,'Tình huống')
highlight(s,9,5.4,2,.9,'Dấu hiệu')
notes(s,"""KỊCH BẢN — SLIDE 4/15 (25 giây)

[Lời nói]
"Khi dạy AI, chúng tôi gặp ba khó khăn. Thứ nhất, AI là hộp đen — học sinh không thấy dữ liệu, mô hình hay lỗi. Thứ hai, phòng máy trường có thể yếu hoặc mất mạng, không thể yêu cầu tài khoản hay API. Thứ ba, học sinh dễ tin ngay đáp án AI mà không kiểm tra. AInatomy giải quyết cả ba vấn đề này."

[Animation]
- Click 1: Highlight "Vào hoạt động" — "Học sinh vào hoạt động dễ dàng, không cần đăng nhập."
- Click 2: Highlight "Tình huống" — "Mỗi hoạt động bắt đầu bằng một tình huống cụ thể."
- Click 3: Highlight "Dấu hiệu" — "Học sinh học cách nhận diện dấu hiệu để tự kiểm tra."
""")

# ===== SLIDE 5: GIẢI PHÁP =====
s=slide('02 · GIẢI PHÁP',5,'AInatomy biến "hộp đen" thành trải nghiệm có thể quan sát')
steps=[('01','Tình huống'),('02','Dự đoán'),('03','Thao tác'),('04','Phản hồi')]
for i,(no,lab) in enumerate(steps):
    x=.9+i*3.05; shp(s,x,2.25,2.25,1,PALE,BORDER); tx(s,x+.12,2.38,.5,.3,no,22,BLUE,True); tx(s,x+.7,2.42,1.35,.25,lab,16,NAVY,True)
    if i<3: tx(s,x+2.38,2.48,.6,.25,'→',24,GOLD,True,PP_ALIGN.CENTER)
for i,k in enumerate(['read','write','answer','evidence']): pic(s,I[k],.85+i*3.05,4.05,2.45,2.15)
tx(s,.85,6.35,11.6,.3,'Một hoạt động hoàn chỉnh: học sinh phán đoán trước, thao tác, nhận phản hồi rồi tự rút ra kết luận.',17,NAVY,True,PP_ALIGN.CENTER)
highlight(s,1.1,4.5,1.8,1.2,'Đọc')
highlight(s,4.15,4.5,1.8,1.2,'Viết')
highlight(s,7.2,4.5,1.8,1.2,'Xem')
highlight(s,10.25,4.5,1.8,1.2,'Đối chiếu')
notes(s,"""KỊCH BẢN — SLIDE 5/15 (25 giây)

[Lời nói]
"Giải pháp của chúng tôi là biến mỗi khái niệm AI thành một chuỗi 4 bước: tình huống, dự đoán, thao tác, phản hồi. Học sinh không nhận đáp án ngay — các em phải phán đoán trước, sau đó thao tác, nhận phản hồi và tự đối chiếu. Đây là cách học chủ động, không thụ động."

[Animation]
- Click 1: Highlight "Đọc" — "Bước 1: Học sinh đọc tình huống hoặc đầu ra AI."
- Click 2: Highlight "Viết" — "Bước 2: Học sinh viết phán đoán và lý do."
- Click 3: Highlight "Xem" — "Bước 3: Học sinh xem kết quả và phản hồi."
- Click 4: Highlight "Đối chiếu" — "Bước 4: Học sinh đối chiếu với dấu hiệu để tự rút ra bài học."
""")

# ===== SLIDE 6: THAO TÁC THẬT =====
s=slide('03 · TRIỂN KHAI',6,'Một phiên học diễn ra như thế nào?','Các trạng thái dưới đây là ảnh chụp thật của sản phẩm')
for i,k in enumerate(['read','write','answer','evidence']):
    pic(s,I[k],.75+i*3.05,2,2.55,3.95)
    tx(s,.75+i*3.05,6.1,2.55,.25,f'{i+1} · '+['Đọc tình huống','Đưa ra phán đoán','Nhận kết quả','Xem dấu hiệu'][i],10,MUTED,False,PP_ALIGN.CENTER)
tx(s,.85,6.55,11.6,.28,'Giá trị sư phạm nằm ở khoảng thời gian trước khi xem đáp án.',17,NAVY,True,PP_ALIGN.CENTER)
highlight(s,1,2.5,2,.8,'Câu hỏi')
highlight(s,4.05,3.5,2,1.2,'Lý do')
highlight(s,7.1,3,2,1,'Kết quả')
highlight(s,10.15,3.2,2,1.5,'Dấu hiệu')
notes(s,"""KỊCH BẢN — SLIDE 6/15 (20 giây)

[Lời nói]
"Đây là một phiên học thật. Học sinh đọc tình huống, đưa ra phán đoán và viết lý do — đây là bước quan trọng nhất, buộc các em phải tư duy trước khi xem đáp án. Sau đó, các em nhận kết quả và xem các dấu hiệu để tự kiểm tra."

[Animation]
- Click 1: Highlight "Câu hỏi" — "Tình huống được đặt ra rõ ràng."
- Click 2: Highlight "Lý do" — "Học sinh phải viết lý do trước khi xem đáp án."
- Click 3: Highlight "Kết quả" — "Hệ thống phản hồi ngay lập tức."
- Click 4: Highlight "Dấu hiệu" — "Học sinh học cách nhận diện dấu hiệu để tự kiểm tra."
""")

# ===== SLIDE 7: TÍNH NĂNG 1 =====
s=slide('04 · TÍNH NĂNG 1',7,'Đấu trường bắt lỗi AI','Học sinh phán xử đầu ra AI thay vì tin ngay vào câu trả lời')
pic(s,I['situation'],.7,2,6.3,4.35)
card(s,7.45,2,5.1,1.25,'BƯỚC 1 · NHẬN DIỆN','Đọc một câu trả lời có thể đúng hoặc có lỗi.',BLUE)
card(s,7.45,3.48,5.1,1.25,'BƯỚC 2 · PHÁN ĐOÁN','Chọn có lỗi/không có lỗi và nêu lý do.',GOLD)
card(s,7.45,4.96,5.1,1.39,'BƯỚC 3 · KIỂM TRA','Xem phản hồi, dấu hiệu và nhóm lỗi tương ứng.',GREEN)
highlight(s,1.5,2.8,4,1.5,'Đầu ra AI')
highlight(s,8.5,2.5,3,.8,'Bước 1')
highlight(s,8.5,4,3,.8,'Bước 2')
highlight(s,8.5,5.5,3,.8,'Bước 3')
notes(s,"""KỊCH BẢN — SLIDE 7/15 (25 giây)

[Lời nói]
"Một trong những tính năng cốt lõi là Đấu trường bắt lỗi AI. Học sinh đọc một câu trả lời do AI tạo ra — có thể đúng hoặc có lỗi. Các em phải nhận diện, phán đoán có lỗi hay không, nêu lý do, sau đó xem phản hồi và học cách phân loại lỗi. Đây là cách dạy học sinh tư duy phản biện với AI."

[Animation]
- Click 1: Highlight "Đầu ra AI" — "Đây là đầu ra AI mà học sinh phải kiểm tra."
- Click 2: Highlight "Bước 1" — "Bước 1: Nhận diện."
- Click 3: Highlight "Bước 2" — "Bước 2: Phán đoán."
- Click 4: Highlight "Bước 3" — "Bước 3: Kiểm tra và phân loại lỗi."
""")

# ===== SLIDE 8: TÍNH NĂNG 2 =====
s=slide('05 · TÍNH NĂNG 2',8,'Nhà máy AI: nhìn thấy các bước phía sau một kết quả')
pic(s,I['tram0'],.65,2,5.9,4.2); pic(s,I['tram5'],6.8,2,5.9,4.2)
shp(s,.65,6.35,12.05,.45,PALE,BORDER)
tx(s,.85,6.45,11.65,.2,'Học sinh đi từ dữ liệu đầu vào đến cách AI được dùng — không chỉ nhìn vào kết quả cuối.',16,NAVY,True,PP_ALIGN.CENTER)
highlight(s,1.5,2.8,3.5,1.5,'Trạm nhập liệu')
highlight(s,7.7,2.8,3.5,1.5,'Trạm ứng dụng')
notes(s,"""KỊCH BẢN — SLIDE 8/15 (20 giây)

[Lời nói]
"Tính năng thứ hai là Nhà máy AI. Học sinh không chỉ nhìn vào kết quả cuối — các em đi qua từng bước: từ nhập liệu, dán nhãn, huấn luyện, kiểm định, đến ứng dụng. Ở mỗi trạm, các em thấy vai trò và hậu quả khi bước đó bị hỏng."

[Animation]
- Click 1: Highlight "Trạm nhập liệu" — "Trạm 0: Học sinh thấy dữ liệu đầu vào."
- Click 2: Highlight "Trạm ứng dụng" — "Trạm 5: Học sinh thấy cách AI được dùng trong thực tế."
""")

# ===== SLIDE 9: TÍNH NĂNG 3 =====
s=slide('06 · TÍNH NĂNG 3',9,'Xưởng huấn luyện: dữ liệu thay đổi thì kết quả cũng thay đổi')
pic(s,I['home'],.7,2,6,3.75)
card(s,7.15,2,5.3,1.25,'DỮ LIỆU LỆCH','Học sinh quan sát mô hình học từ một bộ dữ liệu không cân bằng.',BLUE)
card(s,7.15,3.48,5.3,1.25,'KẾT QUẢ KHÁC NHAU','So sánh kết quả trên các nhóm dữ liệu khác nhau.',GOLD)
card(s,7.15,4.96,5.3,.8,'BÀI HỌC','AI không tự nhiên "khách quan"; dữ liệu và cách kiểm tra rất quan trọng.',GREEN)
tx(s,.8,6.25,11.7,.28,'Các tỉ lệ trong slide là kết quả của mô phỏng trong sản phẩm, không phải số liệu tác động lớp học.',10,MUTED,False,PP_ALIGN.CENTER)
highlight(s,1.5,2.8,3.5,2,'Mô phỏng')
notes(s,"""KỊCH BẢN — SLIDE 9/15 (20 giây)

[Lời nói]
"Tính năng thứ ba là Xưởng huấn luyện. Học sinh quan sát mô hình học từ dữ liệu lệch — ví dụ 92% ảnh ban ngày, chỉ 8% ảnh ban đêm. Kết quả: mô hình đúng 100% trên ảnh ngày, nhưng chỉ 59% trên ảnh đêm. Bài học: AI không tự nhiên khách quan, dữ liệu và cách kiểm tra rất quan trọng."

[Animation]
- Click 1: Highlight "Mô phỏng" — "Đây là mô phỏng trong sản phẩm, không phải số liệu lớp học."
""")

# ===== SLIDE 10: TÍCH HỢP =====
s=slide('07 · TÍCH HỢP',10,'Từ hoạt động trong app đến bài học Tin học 10')
metric(s,.8,2.05,2.75,'28','bài SGK được đối chiếu'); metric(s,3.8,2.05,2.75,'22/22','YCCĐ lớp 10'); metric(s,6.8,2.05,2.75,'12','tiết đề xuất'); metric(s,9.8,2.05,2.65,'5','phân hệ học tập')
pic(s,I['tram0'],.85,4,3.6,2.25); pic(s,I['situation'],4.85,4,3.6,2.25); pic(s,I['prompt'],8.85,4,3.6,2.25)
highlight(s,1.5,4.5,2,1,'Dữ liệu')
highlight(s,5.5,4.5,2,1,'Đạo đức')
highlight(s,9.5,4.5,2,1,'Prompt')
notes(s,"""KỊCH BẢN — SLIDE 10/15 (20 giây)

[Lời nói]
"AInatomy tích hợp vào 28 bài SGK Tin học 10, phủ 22/22 yêu cầu cần đạt theo QĐ 2422, với phân phối 12 tiết đề xuất. Mỗi hoạt động trong app đều gắn với một bài học cụ thể: từ dữ liệu, đạo đức, đến kỹ năng viết prompt."

[Animation]
- Click 1: Highlight "Dữ liệu" — "Hoạt động về dữ liệu và mô hình."
- Click 2: Highlight "Đạo đức" — "Hoạt động về đạo đức và kiểm chứng."
- Click 3: Highlight "Prompt" — "Hoạt động về kỹ năng viết prompt và phản hồi."
""")

# ===== SLIDE 11: MINH CHỨNG GV =====
s=slide('08 · MINH CHỨNG',11,'Sản phẩm không chỉ cho học sinh thao tác — còn để lại minh chứng')
pic(s,I['export'],.75,2,4.4,4.3)
card(s,5.55,2,3,1.55,'THEO DÕI','Hoạt động được ghi theo mã ẩn danh.',BLUE)
card(s,8.8,2,3.7,1.55,'PHẢN HỒI','Nhiệm vụ có nhãn đúng cố định được phản hồi ngay.',GOLD)
card(s,5.55,3.85,3,1.55,'XUẤT TỆP','Giáo viên có thể xuất dữ liệu làm minh chứng.',GREEN)
card(s,8.8,3.85,3.7,1.55,'BẢO VỆ DỮ LIỆU','Không yêu cầu tài khoản học sinh.',PURPLE)
highlight(s,1.5,3,2.5,1.5,'Xuất tệp')
notes(s,"""KỊCH BẢN — SLIDE 11/15 (20 giây)

[Lời nói]
"Đối với giáo viên, AInatomy cung cấp minh chứng rõ ràng. Hoạt động được ghi theo mã ẩn danh, không thu thập dữ liệu cá nhân. Giáo viên có thể xuất dữ liệu làm minh chứng, và nhiều nhiệm vụ được phản hồi ngay nhờ nhãn đúng cố định."

[Animation]
- Click 1: Highlight "Xuất tệp" — "Giáo viên xuất dữ liệu làm minh chứng."
""")

# ===== SLIDE 12: KIỂM TRA =====
s=slide('09 · KIỂM TRA',12,'Những gì đã được kiểm tra','Đây là kiểm thử sản phẩm, không phải số liệu tác động học tập')
metric(s,.8,2.2,2.8,'97/97','tiêu chí nghiệm thu'); metric(s,3.85,2.2,2.8,'22/22','YCCĐ được phủ'); metric(s,6.9,2.2,2.8,'0','lỗi nội dung'); metric(s,9.95,2.2,2.5,'offline','chạy không cần mạng')
pic(s,I['home'],.85,4.15,4.1,2); pic(s,I['answer'],5.25,4.15,3,2); pic(s,I['export'],8.55,4.15,3.8,2)
highlight(s,1.5,4.7,2.5,1,'Giao diện')
highlight(s,5.8,4.7,1.8,1,'Phản hồi')
highlight(s,9.2,4.7,2.5,1,'Minh chứng')
notes(s,"""KỊCH BẢN — SLIDE 12/15 (20 giây)

[Lời nói]
"Về kiểm thử sản phẩm: 97/97 tiêu chí nghiệm thu đạt, 22/22 yêu cầu cần đạt được phủ, 0 lỗi nội dung, và sản phẩm chạy offline. Lưu ý: đây là kiểm thử sản phẩm, không phải số liệu tác động lớp học — phần đó cần triển khai thật để thu thập."

[Animation]
- Click 1: Highlight "Giao diện" — "Giao diện sản phẩm."
- Click 2: Highlight "Phản hồi" — "Phản hồi trong hoạt động."
- Click 3: Highlight "Minh chứng" — "Minh chứng đầu ra."
""")

# ===== SLIDE 13: TRIỂN KHAI VÀ GIỚI HẠN =====
s=slide('10 · GIỚI HẠN',13,'Bằng chứng hiện có và bước cần làm tiếp')
card(s,.8,2.05,5.7,3.75,'ĐÃ CÓ','Bản chạy thử công khai\nBộ ảnh thao tác sản phẩm\nVideo demo nháp\nCó thể chạy offline, USB hoặc mạng nội bộ',GREEN)
card(s,6.8,2.05,5.7,3.75,'CẦN BỔ SUNG','Dữ liệu từ lớp học thật\nPhản hồi học sinh và giáo viên khác\nĐo tác động trước/sau\nBiên bản triển khai thực tế',GOLD)
tx(s,.95,6.25,11.4,.32,'Không dùng ảnh thao tác phần mềm để thay thế cho bằng chứng tác động lớp học.',17,NAVY,True,PP_ALIGN.CENTER)
notes(s,"""KỊCH BẢN — SLIDE 13/15 (20 giây)

[Lời nói]
"Về triển khai: chúng tôi đã có bản chạy thử công khai, bộ ảnh thao tác, video demo, và sản phẩm có thể chạy offline. Tuy nhiên, chúng tôi trung thực rằng chưa có dữ liệu từ lớp học thật, chưa có phản hồi học sinh, và chưa đo tác động trước/sau. Đây là bước tiếp theo cần thực hiện."

[Animation]
- Không có highlight ở slide này.
""")

# ===== SLIDE 14: BỀN VỮNG =====
s=slide('11 · BỀN VỮNG',14,'Có thể bắt đầu từ một phòng máy')
card(s,.8,2.35,3.65,2.3,'CHÉP','Chép thư mục vào USB hoặc máy trường.',BLUE)
card(s,4.8,2.35,3.65,2.3,'MỞ','Mở sản phẩm bằng trình duyệt.',GOLD)
card(s,8.8,2.35,3.65,2.3,'DẠY','Giáo viên tổ chức hoạt động theo bài học.',GREEN)
pic(s,I['menu'],1.15,5.15,2,1.45); pic(s,I['tram0'],4.95,5.15,2,1.45); pic(s,I['export'],8.75,5.15,2,1.45)
highlight(s,1.5,5.5,1.3,.9,'Menu')
highlight(s,5.3,5.5,1.3,.9,'Trạm')
highlight(s,9.1,5.5,1.3,.9,'Xuất')
notes(s,"""KỊCH BẢN — SLIDE 14/15 (20 giây)

[Lời nói]
"Về bền vững và nhân rộng: AInatomy rất đơn giản — chỉ cần chép thư mục vào USB, mở bằng trình duyệt, và giáo viên tổ chức hoạt động. Không cần tài khoản, không cần mạng, không cần cấu hình phức tạp. Đây là giải pháp zero-cost cho mọi trường."

[Animation]
- Click 1: Highlight "Menu" — "Bước 1: Chép và mở."
- Click 2: Highlight "Trạm" — "Bước 2: Chọn hoạt động."
- Click 3: Highlight "Xuất" — "Bước 3: Xuất minh chứng."
""")

# ===== SLIDE 15: KẾT LUẬN =====
s=slide('12 · KẾT LUẬN',15,'Một sản phẩm có thể mở ra một cách học AI khác')
pic(s,I['home'],.7,2,6.3,3.9)
card(s,7.45,2,5.05,1.35,'GIÁ TRỊ CỐT LÕI','Dạy học sinh kiểm chứng AI bằng trải nghiệm trực tiếp.',BLUE)
card(s,7.45,3.65,5.05,1.35,'MINH CHỨNG HIỆN CÓ','Có thao tác thật, ảnh chụp thật và đầu ra có thể kiểm tra.',GOLD)
card(s,7.45,5.3,5.05,1,'BƯỚC TIẾP THEO','Triển khai lớp học và thu dữ liệu tác động thật.',GREEN)
tx(s,.8,6.55,11.8,.25,'https://mxuanvan02.github.io/ainatomy/  ·  GV: Mai Xuân Văn',12,BLUE,False,PP_ALIGN.CENTER)
highlight(s,1.5,2.8,3.5,2,'Trang chủ')
notes(s,"""KỊCH BẢN — SLIDE 15/15 (25 giây)

[Lời nói]
"Kết luận: AInatomy mang lại một cách học AI khác — dạy học sinh kiểm chứng AI bằng trải nghiệm trực tiếp. Chúng tôi đã có thao tác thật, ảnh chụp thật, và đầu ra có thể kiểm tra. Bước tiếp theo là triển khai lớp học và thu dữ liệu tác động thật. Cảm ơn Hội đồng đã lắng nghe. Sản phẩm đang chạy tại địa chỉ trên màn hình."

[Animation]
- Click 1: Highlight "Trang chủ" — "Sản phẩm đang chạy và có thể trải nghiệm."

[Kết thúc video — tổng thời lượng: 5 phút]
""")

P.save(REPO/'template_thuanhoa.pptx'); print('created',len(P.slides))
