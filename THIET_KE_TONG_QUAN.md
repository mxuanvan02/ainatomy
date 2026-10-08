# THIẾT KẾ TỔNG QUAN HỆ THỐNG "AInatomy"

**Phiên bản thiết kế:** 2.0 (thay thế định hướng giao diện tối của v1.x)
**Ngày lập:** 04/10/2026
**Trạng thái:** bản thiết kế để duyệt trước khi triển khai — chưa phải sản phẩm hoàn chỉnh
**Sản phẩm dự thi:** Giải thưởng Tiên phong Ứng dụng AI trong Giáo dục Việt Nam 2026 (Bảng B — THPT)

**Quy ước trình bày.** Tài liệu này là văn bản kĩ thuật nên dùng bảng và nhãn có cấu trúc cho các đặc tả; phần lập luận và căn cứ được viết thành câu hoàn chỉnh. Số thập phân trong tài liệu dùng dấu chấm để nhất quán với mã nguồn và số liệu đo; giao diện hiển thị cho học sinh sẽ dùng dấu phẩy theo quy ước tiếng Việt. Mọi giá trị đo lường đều kèm cách đo, không nêu số liệu mà không chỉ ra nguồn.

---

## PHẦN 0. CĂN CỨ VÀ BA RÀNG BUỘC CHI PHỐI TOÀN BỘ THIẾT KẾ

Thiết kế này chịu ràng buộc bởi ba văn bản và một điều kiện vận hành thực tế. Các ràng buộc được nêu trước vì chúng quyết định kiến trúc, không phải ngược lại.

**Khung nội dung giáo dục trí tuệ nhân tạo cho học sinh phổ thông**, ban hành kèm Quyết định 2422/QĐ-BGDĐT ngày 18/8/2026, quy định bốn mạch nội dung, mười ba chủ đề thành phần và hệ thống mã yêu cầu cần đạt theo cấu trúc `[lớp].[chủ đề].[thứ tự]`. Riêng lớp 10 có hai mươi hai yêu cầu cần đạt, phân bố trên mười trong số mười ba chủ đề; ba chủ đề B1, C1 và C5 không có yêu cầu cần đạt ở lớp này. Toàn bộ hai mươi hai yêu cầu đã được trích nguyên văn và kiểm chứng tự động bằng công cụ `tools/verify_yccd.py` với kết quả 22/22 đạt cả bốn phép kiểm (khớp chuỗi con đầy đủ, ô đặc hiệu nhất, từ khoá bắt buộc, và đối chiếu tập mã).

**Công văn 5588/BGDĐT-GDPT** ngày 19/8/2026 đặt ra bốn điều kiện mà sản phẩm phải thoả mãn đồng thời: không yêu cầu học sinh có tài khoản cá nhân; không tạo sự phụ thuộc vào nhà cung cấp; không buộc học sinh hoặc cha mẹ học sinh mua tài khoản, thiết bị hay dịch vụ; và ưu tiên phần mềm mã nguồn mở, miễn phí, có phiên bản dùng ngoại tuyến hoặc in ấn.

**Phần VI của Khung 2422** quy định về đánh giá, trong đó có hai điểm chi phối trực tiếp thiết kế giao diện. Thứ nhất, nội dung giáo dục AI không xác lập đầu điểm riêng và không tổ chức bài kiểm tra định kì, nên hệ thống chỉ được trình bày mức độ đáp ứng kèm minh chứng, không được hiển thị điểm số hay xếp loại. Thứ hai, Khung khuyến khích tự đánh giá và đánh giá đồng đẳng theo tiêu chí phù hợp, đồng thời yêu cầu nhiệm vụ đánh giá có phương án không sử dụng thiết bị hoặc sử dụng thiết bị dùng chung.

**Điều kiện vận hành thực tế** là máy tính trong phòng lab của trường phổ thông Việt Nam thường có cấu hình thấp, có thể không có card đồ hoạ rời, và nhiều trường vùng khó không có kết nối Internet ổn định. Sản phẩm vì thế phải chạy được khi mở trực tiếp từ thư mục hoặc USB bằng giao thức `file://`, không phụ thuộc máy chủ.

Bốn ràng buộc này dẫn đến một hệ quả kiến trúc quan trọng: **mọi thành phần tải từ mạng đều phải là tuỳ chọn tăng cường, không phải điều kiện hoạt động.** Nếu một tính năng chỉ chạy khi có Internet, tính năng đó phải có bản thay thế dùng ngoại tuyến và phải nói rõ với người dùng.

---

## PHẦN 1. KIẾN TRÚC TỔNG QUAN

### 1.1. Ba tầng kiến trúc

Hệ thống được tổ chức thành ba tầng tách biệt, trong đó tầng dưới không phụ thuộc tầng trên.

**Tầng nội dung** gồm các tệp dữ liệu tĩnh dạng JavaScript đặt trong `data/`. Dữ liệu được nhúng dưới dạng biến toàn cục thay vì tải bằng `fetch` vì giao thức `file://` chặn truy vấn tài nguyên cục bộ ở nhiều trình duyệt do chính sách CORS. Tầng này chứa ngân hàng câu hỏi, hai mươi hai yêu cầu cần đạt, siêu dữ liệu chủ đề, và nội dung kiến thức nền.

**Tầng mô phỏng** gồm các mô-đun tính toán chạy hoàn toàn trong trình duyệt: perceptron học thật với trọng số cập nhật theo lỗi, bộ sinh ảnh tổng hợp vẽ bằng canvas, engine chấm tất định dựa trên nhãn đúng có sẵn, và hai cảnh đồ hoạ ba chiều dựng trên three.js. Không có thành phần nào gọi ra mạng.

**Tầng giao diện** gồm các khung nhìn được chuyển đổi bằng cách ẩn hiện, không dùng bộ định tuyến phía máy chủ, để đường dẫn tương đối hoạt động đúng trên cả `file://` và HTTPS.

### 1.2. Hai chế độ vận hành trên một bộ mã

Cùng một thư mục mã nguồn phục vụ hai chế độ. Chế độ ngoại tuyến mở `index.html` trực tiếp từ USB hoặc máy trường. Chế độ trực tuyến đặt thư mục lên GitHub Pages để có đường dẫn công khai, phục vụ việc nhân rộng và thu thập bằng chứng triển khai. Sự khác biệt duy nhất giữa hai chế độ là việc đồng bộ nhật ký lên máy chủ, và tính năng này được thiết kế để im lặng bỏ qua khi không có mạng.

### 1.3. Đồ hoạ ba chiều: quyết định kĩ thuật đã kiểm chứng

Thư viện three.js được chọn ở phiên bản r137.5, nạp bằng bản dựng UMD và lưu trong thư mục `vendor/` của chính kho mã. Ba lí do dẫn đến quyết định này đều đã được kiểm chứng bằng phép thử thật. Bản dựng theo mô-đun ES bị chính sách CORS chặn khi trang mở bằng `file://`. Các phiên bản từ r150 trở đi không còn phát hành `three.min.js` dạng UMD. Và việc dùng CDN sẽ vi phạm ràng buộc hoạt động khi trường mất mạng. Phép thử `_probe3d.html` trên `file://` trả về `THREE.REVISION=137`, điều khiển quỹ đạo gắn đúng vào đối tượng THREE, WebGL 1.0 khả dụng, và lệnh render đồng bộ cho ra mười hai tam giác.

Một đặc điểm vận hành cần lưu ý: hàm `requestAnimationFrame` bị trình duyệt giảm tần suất khi thẻ không hiển thị. Vì thế mỗi cảnh đều có phương thức render đồng bộ một khung hình, vừa để kiểm thử được, vừa để không tiêu tốn tài nguyên khi người dùng chuyển thẻ.

### 1.4. Bốn xung đột giữa design system đề xuất và ràng buộc sản phẩm

Bộ design system sinh ra từ công cụ `ui-ux-pro-max` trong kho `ai-agent-tools` của tác giả được dùng làm cơ sở, nhưng có bốn điểm không áp dụng được nguyên trạng. Mỗi điểm đều đã đo hoặc kiểm chứng trước khi quyết định.

**Xung đột thứ nhất: phông chữ tải từ mạng.** Tệp MASTER.md đề xuất nạp Inter bằng `@import url('https://fonts.googleapis.com/...')`. Phép thử tải thật trả về tệp CSS 916 byte với **không có** subset tiếng Việt nào, và bản thân việc gọi ra mạng đã trái ràng buộc ngoại tuyến. Quyết định: dùng chuỗi phông hệ thống, không nạp phông từ mạng. Chuỗi ưu tiên là Inter (nếu máy đã cài), Segoe UI (mặc định trên Windows của trường), system-ui, DejaVu Sans, rồi các phông không chân dự phòng. Tất cả đều phủ tiếng Việt trên máy trường. Việc nhúng tệp WOFF2 subset tiếng Việt của Inter được xếp vào hạng mục tăng cường tuỳ chọn ở giai đoạn sau, không nằm trong đường găng.

**Xung đột thứ hai: màu đồ hoạ ba chiều.** Bảng màu hiện tại của cảnh 3D được thiết kế cho nền tối. Khi nền chuyển sang sáng theo yêu cầu, phép đo tương phản WCAG cho kết quả không đạt: vàng `#FFD43B` trên nền trắng chỉ 1.43:1, xanh `#4DABF7` đạt 2.48:1, đỏ `#FF6B6B` đạt 2.78:1. Tiêu chí WCAG 1.4.11 yêu cầu tối thiểu 3.0:1 cho thành phần đồ hoạ. Bảng màu mới ở Phần 4 đã được đo lại và mọi cặp đều đạt.

**Xung đột thứ ba: biểu tượng cảm xúc.** MASTER.md xếp "emoji làm biểu tượng" vào nhóm mẫu cần tránh và yêu cầu dùng bộ SVG nhất quán. Ứng dụng hiện tại dùng biểu tượng cảm xúc ở hầu hết nút. Phép thử xác nhận thư viện Lucide phát hành dạng tĩnh tại `icons/*.svg`, giấy phép ISC, cho phép lưu vào kho. Quyết định: thay biểu tượng cảm xúc bằng SVG nội tuyến của Lucide, lưu cục bộ, không gọi CDN.

**Xung đột thứ tư: màu nhấn không đạt tương phản cho chữ.** Màu accent `#0891B2` trên nền trắng đo được 3.68:1, dưới ngưỡng 4.5:1 cho chữ thường. Tỉ lệ tương phản có tính đối xứng nên chữ trắng đặt trên nền `#0891B2` cũng chỉ đạt 3.68:1; con số 5.70:1 thuộc về cặp chữ đen trên nền đó và không áp dụng được cho nút chữ trắng. Quyết định: nền nút hành động chính dùng `#0E7490` với chữ trắng, đạt 5.36:1; còn `#0891B2` chỉ dùng cho chữ cỡ lớn (ngưỡng 3.0:1) và cho thành phần đồ hoạ theo tiêu chí WCAG 1.4.11.

---

## PHẦN 2. ĐẶC TẢ TOÀN BỘ CHỨC NĂNG

Hệ thống có mười khung nhìn. Mỗi khung nhìn được mô tả theo bốn mục: người dùng là ai, chức năng làm gì, yêu cầu cần đạt nào được phủ, và minh chứng nào được ghi lại.

### 2.1. Màn hình vào lớp

Học sinh vào bằng mã do giáo viên phát và mã lớp, không đăng ký, không thư điện tử, không số điện thoại. Thiết kế này nhằm thoả mãn đồng thời hai điều: Công văn 5588 cấm yêu cầu tài khoản cá nhân, và Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 đặt dữ liệu trẻ em dưới sự bảo vệ chặt hơn, cần sự đồng ý của cha mẹ hoặc người giám hộ. Vì hệ thống chỉ lưu mã ẩn danh nên về bản chất không xử lý dữ liệu cá nhân của trẻ em. Minh chứng vẫn nên có văn bản cho phép của ban giám hiệu.

### 2.2. Xưởng huấn luyện hai chiều

Học sinh tạo bộ dữ liệu ảnh do hệ vẽ bằng canvas, quan sát perceptron học thật với trọng số cập nhật theo lỗi qua từng vòng, rồi phát hiện mô hình đạt độ chính xác cao trên ảnh ban ngày nhưng sai gần một nửa trên ảnh ban đêm. Bốn nhiệm vụ phân tích có nhãn đúng cố định nên hệ tự chấm.

Phủ yêu cầu cần đạt 10.C4.1 về ảnh hưởng của chất lượng dữ liệu đến chất lượng AI, 10.D2.2 về vấn đề phát sinh khi vận hành và ý nghĩa của việc khắc phục, 10.B3.1 về thiên vị dữ liệu. Minh chứng ghi lại là số lần huấn luyện, tỉ lệ đúng tách theo ngày và đêm, và đáp án bốn nhiệm vụ.

Kết quả đo thực tế trên phiên bản hiện tại: với dữ liệu lệch 92 phần trăm ảnh ngày, mô hình đạt 100 phần trăm trên ảnh ngày và 59 phần trăm trên ảnh đêm. Quan sát chi tiết hơn cho thấy ở các ảnh ban đêm mô hình dự đoán "có mũ bảo hiểm" cho mọi trường hợp, kể cả ảnh không có mũ. Con số 59 phần trăm vì thế không phản ánh năng lực nhận diện mà chỉ là tỉ lệ ảnh đêm tình cờ có mũ trong bộ kiểm tra. Đây là hiện tượng đáng giá về mặt sư phạm và cần được trình bày đúng bản chất trong giao diện: mô hình không học sai, mô hình không học gì về ban đêm.

### 2.3. Phòng ba chiều soi mô hình

Cảnh này biểu diễn cùng bộ dữ liệu và cùng mô hình của xưởng huấn luyện trong không gian ba chiều. Mỗi chấm là một bức ảnh thật, vị trí được tính từ bốn đặc trưng mà mô hình đọc được. Mặt phẳng đỏ mờ là ranh giới quyết định dựng từ trọng số thật.

Vì mô hình có bốn đặc trưng còn không gian hiển thị chỉ ba chiều, mặt phẳng được vẽ là lát cắt của biên bốn chiều tại giá trị trung bình của đặc trưng thứ tư. Đây là phép chiếu hợp lệ về mặt toán học và được ghi rõ trên giao diện để người xem không hiểu nhầm rằng mô hình chỉ dùng ba đặc trưng. Phép dựng mặt phẳng từ trọng số được suy dẫn trong phần chú thích đầu tệp `js/lab3d.js` và cần được kiểm chứng bằng số ở bước triển khai.

Học sinh kéo thanh tỉ lệ ảnh ngày, bấm huấn luyện để xem mặt phẳng dịch dần theo từng vòng, rồi đánh giá trên bộ ảnh mới khác seed với bộ huấn luyện. Chế độ nhẹ tắt hoạt ảnh và giảm số chấm cho máy yếu. Khi máy không có WebGL, hệ thống in thông báo và hướng dẫn quay về xưởng hai chiều với cùng nội dung bài học.

### 2.4. Ống dẫn ba chiều soi luồng hoạt động

Năm trạm của một hệ thống AI được biểu diễn dọc theo một đường ống, với các hạt sáng là dòng dữ liệu chảy qua. Hệ thống làm hỏng ngẫu nhiên một trạm, học sinh quan sát hiện tượng và đoán trạm nào. Vì trạm hỏng do hệ chọn nên đáp án đã biết trước và việc chấm là phép so sánh tất định. Bấm vào từng trạm để xem vai trò và hậu quả khi trạm đó hỏng.

Cảnh này phủ yêu cầu cần đạt 10.D1.1 về mối liên hệ giữa mục tiêu và các thành phần chính của hệ thống, 10.D2.1 về các thành phần cơ bản gồm dữ liệu, mô hình, thuật toán, đầu ra và phản hồi, cùng 10.A1.2 về tầm quan trọng của việc con người kiểm soát AI. Đây là yêu cầu mà phiên bản hai chiều chưa phủ. Khi không có WebGL, hệ thống in bảng năm trạm dạng chữ để bài học vẫn đầy đủ.

### 2.5. Đấu trường soi lỗi

Học sinh đọc các câu trả lời do trợ lý AI tạo ra, trong đó một số câu có lỗi được cài sẵn thuộc năm nhóm: bịa số liệu, trích nguồn không tồn tại, thiên kiến định kiến, suy luận sai, và xui lộ dữ liệu cá nhân. Học sinh phán quyết có lỗi hay không, rồi chọn đúng nhóm lỗi. Hệ chấm ngay và giải thích.

Ngân hàng hiện có bảy mươi tám câu. Chế độ luyện tập, tiền kiểm tra và hậu kiểm tra dùng cùng một hệ đo để so sánh tiến bộ. Yêu cầu cần đạt 10.B2.MR1 mô tả gần như đúng cơ chế này: nhận biết dấu hiệu của nội dung do AI tạo sinh, kiểm tra và nhận xét mức độ minh bạch của việc khai báo sử dụng AI.

### 2.6. Kiến thức nền và thực hành viết prompt

Năm mục nội dung phủ các yêu cầu còn thiếu: quy định pháp luật bảo vệ người dùng theo 10.A3.1, ứng dụng AI theo tính năng hệ thống theo 10.C2.2, phân biệt AI tạo sinh với hệ thống phân loại và dự đoán theo 10.C3.3, tiêu chí của một prompt phù hợp mục tiêu theo 10.C3.1, và ba bài thực hành đặt prompt được chấm theo rubric từ khoá theo 10.C3.2.

Các luật được nêu đã kiểm chứng số hiệu: Luật An ninh mạng 24/2018/QH14 sửa đổi bởi 116/2025/QH15, Luật Dữ liệu 60/2024/QH15 có hiệu lực từ 1/7/2025, Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15 có hiệu lực từ 1/1/2026, và Luật Trí tuệ nhân tạo 134/2025/QH15 có hiệu lực từ 1/3/2026.

### 2.7. Lôgic và AI nối với Bài 5 Tin học 10

Mô-đun này nối trực tiếp với bài học đang dạy: dữ liệu lôgic, phép AND OR NOT, bảng chân lí, và bảng nhầm lẫn. Điểm mấu chốt về mặt sư phạm là dấu so sánh trong biểu thức của perceptron chính là một phép lôgic, nhưng các trọng số không do người lập trình viết ra mà do mô hình học từ dữ liệu, nên nó có thể học sai một cách có hệ thống.

### 2.8. Bản đồ năng lực theo mười ba chủ đề

Báo cáo trình bày mức độ đáp ứng theo mười ba chủ đề của Khung 2422, kèm số minh chứng và cột đối chiếu UNESCO. Ba chủ đề không có yêu cầu cần đạt ở lớp 10 được hiển thị mờ để học sinh thấy toàn cảnh. Giao diện dùng cách diễn đạt "đáp ứng tốt", "đáp ứng một phần", "cần luyện thêm", và ghi rõ đây là minh chứng chứ không phải điểm số, không dùng để xếp loại.

Báo cáo lớp tổng hợp nhiều học sinh, có nút xuất CSV và JSON làm minh chứng cuối kì, và nút xoá dữ liệu.

### 2.9. Phiếu khai báo sử dụng AI

Khung 2422 yêu cầu học sinh nêu được công cụ, mục đích và phạm vi hỗ trợ của AI, phần việc do học sinh trực tiếp thực hiện, và cách kiểm chứng. Hệ thống sinh sẵn phiếu này từ nhật ký hoạt động để học sinh in hoặc nộp. Đây là tính năng chưa có sản phẩm nào trong danh sách đạt giải năm 2025 thực hiện, và nó dùng đúng chữ của văn bản Bộ.

### 2.10. Tự đánh giá và đánh giá đồng đẳng

Khung khuyến khích hai hình thức này theo tiêu chí phù hợp. Thiết kế dùng rubric có sẵn để hệ thống vẫn chấm được mà không cần giáo viên, đồng thời cho phép học sinh chấm chéo sản phẩm của nhau trong hoạt động nhóm ở tiết 10 và 11 của kế hoạch mười hai tiết.

---

## PHẦN 3. DANH MỤC MÔ PHỎNG BÀI HỌC

Yêu cầu đặt ra là bài học có thể mô phỏng được mọi nội dung cần dạy. Danh mục dưới đây liệt kê từng mô phỏng, trạng thái hiện tại, yêu cầu cần đạt được phủ, và cơ chế tự chấm. Nguyên tắc xuyên suốt là **mô phỏng chỉ được tính là đạt khi hệ thống tự chấm được bằng nhãn đúng có sẵn**, vì điều kiện thể lệ không cho phép dựa vào người kiểm chứng bên ngoài.

| # | Mô phỏng | Trạng thái | YCCĐ phủ | Cơ chế tự chấm |
|---|---|---|---|---|
| 1 | Perceptron học thật, trọng số đổi theo lỗi | đã có | 10.C4.1, 10.C5 | nhãn ảnh có sẵn, đối chiếu dự đoán |
| 2 | Thiên kiến dữ liệu ngày và đêm | đã có | 10.C4.1, 10.D2.2, 10.B3.1 | bộ kiểm tra tách nhóm, khác seed |
| 3 | Mặt phẳng quyết định trong không gian 3D | đang dựng | 10.C4.1, 10.C5 | suy từ trọng số thật, kiểm bằng số |
| 4 | Ống dẫn năm trạm, đoán trạm hỏng | đang dựng | 10.D1.1, 10.D2.1, 10.A1.2 | hệ chọn ngẫu nhiên, đáp án biết trước |
| 5 | Bắt lỗi nội dung AI tạo sinh, năm nhóm lỗi | đã có | 10.B2.MR1 | lỗi cài sẵn, nhãn cứng |
| 6 | Thực hành viết prompt theo rubric | đã có | 10.C3.1, 10.C3.2 | rubric từ khoá, tất định |
| 7 | Phân biệt AI tạo sinh và AI phân loại | đã có | 10.C3.3 | câu hỏi nhiều lựa chọn có nhãn |
| 8 | Quy định pháp luật bảo vệ người dùng | đã có | 10.A3.1 | câu hỏi có nhãn, số hiệu luật đã kiểm chứng |
| 9 | Bảng nhầm lẫn và các chỉ số đánh giá | đã có | 10.D2.2 | tính từ phán quyết của học sinh |
| 10 | Dữ liệu lôgic, phép AND OR NOT | đã có | nối Bài 5 Tin học 10 | bảng chân lí có nhãn |
| 11 | Học tủ: tách dữ liệu huấn luyện và kiểm tra | **chưa làm** | 10.C4.1, 10.C5 | hai bộ khác seed, so độ chính xác |
| 12 | Quá khớp và dưới khớp | **chưa làm** | 10.C5, 10.D2.2 | đường cong lỗi theo số vòng |
| 13 | Dạng dữ liệu huấn luyện: ảnh, âm thanh, văn bản | **chưa làm** | 10.C4.MR1 | phân loại mẫu, có nhãn |
| 14 | Vai trò con người trong vận hành hệ AI | **chưa làm** | 10.A1.1, 10.A1.2 | tình huống quyết định có nhãn |
| 15 | Rủi ro của một sản phẩm AI với người và xã hội | **chưa làm** | 10.A2.1, 10.A2.MR1 | tình huống có nhãn |
| 16 | Hành vi dùng AI vi phạm quy định nhà trường | **chưa làm** | 10.B2.1 | tình huống có nhãn |
| 17 | Chọn vấn đề Việt Nam để ứng dụng AI | **chưa làm** | 10.C2.1 | rubric tiêu chí, tất định |
| 18 | Ứng dụng AI theo tính năng hệ thống | **chưa làm** | 10.C2.2 | phân nhóm có nhãn |
| 19 | Yêu cầu cần có khi ứng dụng AI cho một nhiệm vụ | **chưa làm** | 10.C2.MR1 | checklist có nhãn |
| 20 | Công nghệ để thiết kế và tạo AI | **chưa làm** | 10.C3.MR1 | câu hỏi có nhãn |

Mười mục đã có hoặc đang dựng, mười mục chưa làm. Trong số chưa làm, các mục 11 đến 16 là cốt lõi và nên ưu tiên vì chúng phủ những yêu cầu cần đạt mà hiện tại sản phẩm bỏ trống. Các mục 17 đến 20 thuộc nhóm mở rộng hoặc ít trọng số hơn.

**Giới hạn cần nói rõ.** Hai yêu cầu cần đạt không thể mô phỏng ngoại tuyến: 10.C2.MR2 yêu cầu học sinh sử dụng được một số ứng dụng AI trong học tập, và phần thực hành đầy đủ của 10.C3.2 cần một hệ AI tạo sinh thật. Cả hai đều cần kết nối mạng và tài khoản. Thiết kế xử lí bằng cách ghi rõ phạm vi ở chế độ ngoại tuyến, và mở khoá khi chạy ở chế độ trực tuyến có mạng. Đây là ranh giới trung thực, không phải thiếu sót cần che giấu.

---

## PHẦN 4. HỆ THỐNG THIẾT KẾ GIAO DIỆN, TÔNG SÁNG

### 4.1. Bảng màu đã kiểm chứng tương phản

Mọi cặp màu dưới đây đã đo bằng công thức tương phản WCAG. Cột "tỉ lệ" là giá trị nhỏ hơn khi so với hai nền dùng trong ứng dụng.

**Màu giao diện.** Nền trang `#FAF5FF`, nền thẻ `#FFFFFF`, nền phụ `#ECEEF9`, viền `#DDD6FE`. Chữ chính `#1E1B4B` đạt 14.90:1 trên nền trang và 15.99:1 trên nền thẻ. Chữ phụ `#475569` đạt 7.58:1. Màu chủ đạo `#7C3AED` đạt 5.70:1. Nền nút hành động chính là `#0E7490` với chữ trắng, đạt 5.36:1. Màu `#0891B2` chỉ dùng cho chữ cỡ lớn và thành phần đồ hoạ vì đạt 3.68:1, trên ngưỡng 3.0:1 nhưng dưới ngưỡng 4.5:1 của chữ thường. Màu cảnh báo `#DC2626` đạt 4.83:1.

**Màu đồ hoạ ba chiều trên nền sáng.** Nền cảnh 3D chuyển sang `#F8FAFC`. Bốn màu dữ liệu đã đo lại: ảnh ban ngày `#B45309` đạt 4.80:1, ảnh ban đêm `#1D4ED8` đạt 6.41:1, dự đoán sai `#B91C1C` đạt 6.18:1, dự đoán đúng `#15803D` đạt 4.79:1. Mặt phẳng quyết định dùng `#EF4444` đạt 3.60:1, đủ cho thành phần đồ hoạ. Lưới toạ độ `#CBD5E1` chỉ đạt 1.48:1 nên chỉ dùng làm nền trang trí, không mang thông tin.

### 4.2. Phông chữ

Không nạp phông từ mạng. Chuỗi khai báo là Inter, Segoe UI, system-ui, -apple-system, DejaVu Sans, Arial, sans-serif. Lý do: máy trường dùng Windows nên Segoe UI gần như luôn có và phủ đủ tiếng Việt; việc gọi Google Fonts vừa trái ràng buộc ngoại tuyến vừa không trả về subset tiếng Việt trong phép thử.

### 4.3. Biểu tượng

Thay biểu tượng cảm xúc bằng SVG nội tuyến của Lucide, giấy phép ISC, lưu trong `vendor/lucide/`. Chỉ lưu những biểu tượng thực sự dùng để giữ kho nhẹ. Biểu tượng cảm xúc còn được phép xuất hiện trong nội dung văn bản mang tính thân thiện với học sinh, nhưng không dùng làm biểu tượng điều khiển.

### 4.4. Danh sách kiểm trước khi bàn giao

Không dùng biểu tượng cảm xúc làm biểu tượng. Mọi phần tử bấm được có con trỏ bàn tay. Trạng thái di chuột có chuyển tiếp từ 150 đến 300 mili-giây. Chữ thường đạt tương phản tối thiểu 4.5:1. Trạng thái tiêu điểm nhìn thấy được khi điều hướng bằng bàn phím. Tôn trọng thiết lập giảm chuyển động của hệ điều hành. Hiển thị đúng ở bốn bề rộng 375, 768, 1024 và 1440 điểm ảnh. Không có nội dung bị thanh điều hướng che. Không xuất hiện thanh cuộn ngang trên thiết bị di động.

---

## PHẦN 5. CHUẨN VIẾT NỘI DUNG

Nội dung trong ứng dụng phục vụ mục đích giáo dục nên theo chuẩn văn phong học thuật tiếng Việt, với thứ tự ưu tiên là nghĩa, thuật ngữ, lập trường khoa học, mạch lạc, rồi mới đến diễn đạt và trau chuốt bề mặt. Ba quy tắc cần giữ khi viết nội dung bài học.

**Giữ đúng lực nhận thức.** Kết quả mô phỏng được trình bày bằng "kết quả cho thấy" hoặc "ghi nhận", không nâng cấp thành "chứng minh". Diễn giải dùng "gợi ý" hoặc "có thể cho thấy". Quan hệ giữa thiên kiến dữ liệu và kết quả sai được nêu là "có liên quan đến" trừ khi mô phỏng thực sự thiết lập được quan hệ nhân quả trong phạm vi đã kiểm soát.

**Tránh văn phong quảng cáo.** Không dùng "đột phá", "vượt trội", "toàn diện", "thông minh" khi mô tả chính sản phẩm. Mọi khẳng định về hiệu quả phải kèm số liệu và cách đo.

**Không viết theo lối dán nhãn.** Trừ các nhãn cấu trúc bắt buộc của tài liệu và tiêu đề bảng, nội dung giải thích cho học sinh được viết thành câu đầy đủ, không dồn thành chuỗi "Thứ nhất: ... Thứ hai: ...".

---

## PHẦN 6. KIẾN TRÚC DỮ LIỆU VÀ NHẬT KÝ

Nhật ký lưu trong bộ nhớ cục bộ của trình duyệt theo khoá `soiai_dulieu_v1`, tổ chức theo mã học sinh, mỗi học sinh có mã lớp, thời điểm tạo, và mảng sự kiện. Mỗi sự kiện ghi loại hoạt động, thời điểm, và kết quả chấm. Không lưu họ tên, ảnh, hay bất kỳ định danh cá nhân nào.

Khi chạy ở chế độ trực tuyến có máy chủ, nhật ký được đồng bộ lên máy chủ bằng một yêu cầu POST duy nhất cho mỗi sự kiện. Nếu yêu cầu thất bại, hệ thống im lặng bỏ qua và dữ liệu vẫn nằm ở bộ nhớ cục bộ. Không bao giờ để việc đồng bộ làm gián đoạn hoạt động học.

Giáo viên xuất nhật ký thành CSV hoặc JSON để làm minh chứng cuối kì. Đây là hình thức minh chứng mà phần VI của Khung 2422 yêu cầu, và nó được tổng hợp tự động nên không phát sinh công việc chấm bài.

---

## PHẦN 7. LỘ TRÌNH TRIỂN KHAI

Việc triển khai chia thành năm giai đoạn, mỗi giai đoạn có tiêu chí nghiệm thu đo được. Thời hạn nộp hồ sơ là 23 giờ 59 phút ngày 25 tháng 10 năm 2026, còn hai mươi mốt ngày kể từ thời điểm lập thiết kế này.

**Giai đoạn một, hoàn tất nền tảng ba chiều.** Kiểm chứng toán dựng mặt phẳng bằng số, kiểm thử cảnh ống dẫn, sửa ba lỗi giao diện đã phát hiện: văn bản giải thích chưa khớp số đo thật, nút đánh giá chưa kiểm thử theo đường bấm, và số vòng học cộng dồn khi bấm lại chưa hiển thị rõ.

**Giai đoạn hai, áp dụng giao diện tông sáng.** Thay bảng màu theo Phần 4, thay biểu tượng cảm xúc bằng SVG Lucide, chuyển nền cảnh 3D sang sáng và đổi màu dữ liệu theo bảng đã đo. Tiêu chí nghiệm thu là mọi cặp màu đạt ngưỡng tương phản và danh sách kiểm ở mục 4.4 không còn mục nào chưa đạt.

**Giai đoạn ba, mở rộng mô phỏng.** Dựng các mô phỏng 11 đến 16 trong danh mục, ưu tiên những mục phủ yêu cầu cần đạt cốt lõi đang trống.

**Giai đoạn bốn, dạy thật và thu dữ liệu.** Đây là chặng quyết định vì thể lệ yêu cầu sản phẩm đã triển khai thực tế trong lớp học. Cần chốt ngày dạy, thu nhật ký có dấu thời gian, và quay video cùng ảnh lớp học.

**Giai đoạn năm, hồ sơ dự thi.** Dựng mười lăm slide theo mẫu ban tổ chức, video không quá năm phút, và poster theo mẫu. Cần tải hai tệp mẫu từ cổng của ban tổ chức vì máy phát triển gặp lỗi chứng chỉ với tên miền đó.

---

## PHẦN 8. NHỮNG ĐIỂM CẦN NGƯỜI DÙNG QUYẾT ĐỊNH

Ba việc nằm ngoài phạm vi tự quyết của hệ thống phát triển.

Thứ nhất là ngày dạy Bài 5 và các tiết chuyên đề. Không có tiết dạy thật trước ngày 20 tháng 10 thì không có minh chứng triển khai, và hồ sơ sẽ không qua vòng sơ tuyển.

Thứ hai là hai tệp mẫu của ban tổ chức cho slide và poster.

Thứ ba là việc duyệt nhãn cho năm mươi sáu câu hỏi trong ngân hàng mở rộng. Hoạt động này mở tệp `ho-so/checklist_duyet_nhan.html`.

Ngoài ra còn một quyết định tuỳ chọn về việc dựng máy chủ ghi nhật ký tập trung trên hạ tầng sẵn có. Quyết định này không chặn tiến độ vì giai đoạn một đến ba vẫn hoàn thành được với kiến trúc tĩnh.
