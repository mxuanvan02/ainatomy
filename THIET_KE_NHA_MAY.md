# THIẾT KẾ "NHÀ MÁY AI" — dây chuyền sản xuất thay cho các module rời

**Phiên bản:** 2.1 — thay thế Phần 1 đến Phần 3 của `THIET_KE_TONG_QUAN.md` (v2.0)
**Ngày lập:** 04/10/2026
**Yêu cầu của anh Văn:** *"thiết kế phải dạng nhà máy AI. Tức là học được toàn bộ, kể cả ứng dụng AI ấy. Thấy được cách thức hoạt động."*

---

## 1. Vấn đề của kiến trúc cũ

Bản v1.x và v2.0 tổ chức sản phẩm thành mười khung nhìn song song: trang chủ, vào lớp, xưởng huấn luyện, đấu trường, báo cáo, lôgic, kiến thức nền, phòng 3D, ống dẫn 3D, giới thiệu. Học sinh thấy một thực đơn gồm các nút ngang hàng. Cấu trúc này có ba nhược điểm.

Thứ nhất, nó không cho thấy quan hệ nhân quả giữa các khâu. Học sinh làm bài bắt lỗi mà không thấy lỗi đó sinh ra từ đâu trong quy trình sản xuất. Thứ hai, khâu **ứng dụng AI** hoàn toàn vắng mặt: sản phẩm dạy về AI nhưng học sinh không bao giờ được dùng một hệ AI để làm việc. Thứ ba, yêu cầu cần đạt 10.C2.MR2 ("sử dụng được một số ứng dụng AI trong học tập") bị xếp loại ngoài phạm vi vì cho rằng cần AI thật và kết nối mạng.

## 2. Kiến trúc nhà máy

Sản phẩm được tổ chức lại thành **một dây chuyền sản xuất bảy trạm**, đi từ nguyên liệu đến thành phẩm rồi quay vòng phản hồi. Các module đã viết không bị bỏ đi mà trở thành các trạm của dây chuyền; phần mới duy nhất là Trạm 5.

```
        ┌──────────────── VÒNG PHẢN HỒI (dữ liệu mới quay về Trạm 0) ──────────────┐
        │                                                                            │
  ┌─────▼─────┐  ┌─────────┐  ┌──────────┐  ┌────────┐  ┌─────────┐  ┌──────────┐  ┌▼──────────┐
  │ 0. NHẬP   │→ │ 1. DÁN  │→ │ 2. HUẤN  │→ │ 3. MÔ  │→ │ 4. KIỂM │→ │ 5. ỨNG   │→ │ 6. CON    │
  │   LIỆU    │  │  NHÃN   │  │  LUYỆN   │  │  HÌNH  │  │  ĐỊNH   │  │  DỤNG ★  │  │ NGƯỜI KIỂM│
  └───────────┘  └─────────┘  └──────────┘  └────────┘  └─────────┘  └──────────┘  └───────────┘
   nguyên liệu    sơ chế       dây chuyền    thành phẩm   KCS          xuất xưởng    KCS cuối
   thô                         sản xuất      bán thành                (AI làm việc)  + phản hồi
  ─────────────────────────────────────────────────────────────────────────────────────────────
   SỔ VẬN HÀNH: bản đồ năng lực 13 chủ đề · nhật ký lớp · phiếu khai báo sử dụng AI
```

### Đặc tả từng trạm

| Trạm | Tên | Học sinh thấy gì / làm gì | Mô phỏng | YCCĐ phủ | Trạng thái |
|---|---|---|---|---|---|
| **0** | **NHẬP LIỆU** (nguyên liệu thô) | Ba dạng dữ liệu thật: ảnh vẽ bằng canvas, chuỗi văn bản, và tín hiệu số. Kéo thanh để thấy dữ liệu lệch ngay từ đầu vào. | sinh ảnh + đo đặc trưng | 10.C4.MR1, 10.C2.1 | một phần (đã có ở Tầng 1, cần tách thành trạm riêng) |
| **1** | **DÁN NHÃN** (sơ chế) | Học sinh tự gán nhãn cho ảnh, hệ so với nhãn thật và chỉ ra nhãn sai. Nhãn sai thì mô hình học sai. | có nhãn đúng sẵn | 10.C4.1 | **chưa làm** |
| **2** | **HUẤN LUYỆN** (dây chuyền) | Perceptron học thật: trọng số cập nhật theo lỗi qua từng vòng. Xem cả bản 2D và bản 3D với mặt phẳng quyết định dịch dần. | `lab.js` + `lab3d.js` | 10.C4.1, 10.C5 | **đã có** |
| **3** | **MÔ HÌNH** (thành phẩm bán thành) | Mở nắp mô hình: xem bốn trọng số thật, xem nó là "kiến thức" máy mang theo. Bấm vào điểm dữ liệu để xem nhãn thật và dự đoán. | `lab3d.js` | 10.D2.1, 10.C5 | **đã có** |
| **4** | **KIỂM ĐỊNH** (KCS) | Đánh giá trên bộ ảnh MỚI khác seed. Tách theo ngày và đêm. Thấy 100% so với 59%. | `kiemTra` | 10.D2.2, 10.C4.1 | **đã có** (cần thêm học tủ và quá khớp) |
| **5** | **ỨNG DỤNG ★** (xuất xưởng) | **Trạm mới.** Học sinh đặt prompt cho một hệ AI chạy ngay trong trình duyệt, chọn chủ đề, rồi phán đoán câu trả lời có căn cứ hay là bịa. Hệ chấm bằng nhãn nó tự biết. | `nhamay_text.js` | **10.C2.MR2**, 10.C2.1, 10.C2.2, 10.C2.3, 10.C3.1, 10.C3.2, 10.B2.MR1 | **đã build engine, đang dựng UI** |
| **6** | **CON NGƯỜI KIỂM** (KCS cuối + phản hồi) | Đấu trường soi lỗi: 5 nhóm lỗi cài sẵn. Rồi trả lời "ai chịu trách nhiệm". Phản hồi quay về Trạm 0. | `dautruong` + `pipeline3d.js` | 10.A1.1, 10.A1.2, 10.B2.1, 10.B3.1 | **đã có** (cần nối thành trạm cuối) |
| — | **SỔ VẬN HÀNH** | Bản đồ 13 chủ đề, nhật ký lớp, xuất CSV, phiếu khai báo sử dụng AI. | `engine.js` | Khung phần VI | đã có (phiếu khai báo **chưa làm**) |

## 3. Trạm 5 — chỗ thay đổi cục diện

Đây là trạm anh Văn chỉ ra khi nói "kể cả ứng dụng AI ấy". Ba quyết định thiết kế.

**Quyết định một: dùng máy sinh văn bản huấn luyện ngay trong trình duyệt, không tải model.** Em đã đo kích thước thật: Qwen2.5-0.5B là 988 MB, LaMini-Flan-T5-248M lượng tử hoá là 157 MB. Cả hai đều quá nặng cho USB ở trường vùng khó và đều cần mạng cho lần tải đầu. Máy n-gram mức kí tự huấn luyện trong **2.7 mili-giây**, tải về **0 MB**, chạy **0.266 mili-giây mỗi câu**. Kiến trúc vẫn chừa ba tầng: tầng một n-gram (mặc định), tầng hai Transformers.js khi có mạng, tầng ba WebLLM qua WebGPU khi máy có GPU. Hệ tự dò năng lực máy và không bao giờ bắt người dùng chọn.

**Quyết định hai: biến giới hạn thành bài học.** Máy chỉ biết những gì trong ngữ liệu. Ngữ liệu có bốn chủ đề: nông nghiệp, y tế, giáo dục, môi trường — đều là vấn đề Việt Nam mà yêu cầu cần đạt 10.C2.1 nêu đích danh. Nếu học sinh hỏi đúng bốn chủ đề đó, câu trả lời có căn cứ. Nếu hỏi chủ đề khác, máy **vẫn sinh ra văn bản trôi chảy** — và đó là bịa. Học sinh thấy tận mắt hiện tượng bịa đặt thay vì nghe mô tả.

**Quyết định ba: giữ nguyên tắc oracle.** Việc chủ đề có trong ngữ liệu hay không là điều **hệ biết trước vì chính hệ quyết định ngữ liệu**. Nên trạm kiểm định chấm được bằng phép so sánh tất định. Không cần giáo viên, không cần người kiểm chứng bên ngoài. Đây là điều kiện sống còn của hồ sơ dự thi.

**Một bug đã phát hiện và sửa bằng số liệu.** Bộ sinh ngẫu nhiên dùng LCG với seed liên tiếp cho giá trị rút đầu gần như nhau: seed 5 ra 0.238006, seed 6 ra 0.238393, seed 7 ra 0.238781. Hệ quả đo được là **200 trên 200 seed đầu tiên (100%) đều ra "có lỗi"** trong khi mục tiêu thiết kế là 60%. Hai phiên tiền kiểm tra và hậu kiểm tra vì thế không độc lập, làm hỏng phép đo tiến bộ. Sửa bằng cách trộn seed qua splitmix32 trước khi đưa vào LCG. Sau khi sửa, đo trên 200 seed: **59% có lỗi**, năm nhóm lỗi phân bố đều (24, 22, 29, 23, 20), oracle chấm đúng **60 trên 60** ở cả hai nhánh, và cùng seed cho ra cùng văn bản.

## 4. Những gì thay đổi so với thiết kế v2.0

**Yêu cầu cần đạt 10.C2.MR2 chuyển từ "ngoài phạm vi" sang "phủ".** Ở bản v2.0 em ghi rằng yêu cầu này không thể mô phỏng ngoại tuyến vì cần AI thật và mạng. Trạm 5 bác bỏ kết luận đó: một hệ AI thật theo nghĩa thống kê, huấn luyện và suy luận ngay trong trình duyệt, là đủ để học sinh "sử dụng được một số ứng dụng AI trong học tập". Giới hạn còn lại chỉ là phần thực hành đầy đủ của 10.C3.2 với một mô hình ngôn ngữ lớn thật, và phần đó mở khoá ở chế độ trực tuyến.

**Mười khung nhìn song song gộp thành một dây chuyền.** Các view cũ không xoá mà trở thành trạm; điều hướng chính là sơ đồ nhà máy, không phải thực đơn nút.

**Bốn mô phỏng mới phát sinh từ kiến trúc nhà máy:** trạm dán nhãn (Trạm 1), học tủ và quá khớp (Trạm 4), vòng phản hồi đưa dữ liệu mới về Trạm 0, và phiếu khai báo sử dụng AI ở Sổ vận hành.

## 5. Nguyên tắc bất biến khi triển khai

Mọi trạm phải có bản thay thế khi máy không đáp ứng: không WebGL thì có bản 2D và bản chữ; không mạng thì có tầng một; không phòng máy thì có phiếu in. Không trạm nào được hiển thị điểm số hay xếp loại, chỉ mức độ đáp ứng kèm minh chứng, theo phần VI của Khung 2422. Mọi con số trên giao diện phải truy ngược được về tệp nhật ký. Và mỗi trạm phải trả lời được câu hỏi: học sinh hiểu thêm điều gì nhờ trạm này, nếu không trả lời được thì bỏ trạm đó.
