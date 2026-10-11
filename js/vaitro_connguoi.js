/* AInatomy — vaitro_connguoi.js : ba câu hỏi cho yêu cầu cần đạt 10.A1.1.
 *
 * NGUYÊN VĂN YCCĐ (Khung 2422/QĐ-BGDĐT, lớp 10 — đã verify 22/22 bằng tools/verify_yccd.py):
 *   10.A1.1 [cốt lõi] "Thực hành xác định được vai trò của con người trong SỬ DỤNG, VẬN HÀNH,
 *   TÙY CHỈNH một hệ thống AI cụ thể."
 *
 * VÌ SAO CÓ TỆP NÀY
 * Ngày 11/10, sau phản biện của bốn giám khảo độc lập (review13/), bảng đối chiếu hai trục xác
 * nhận 10.A1.1 là mã DUY NHẤT rơi về CHƯA PHỦ. Lý do không phải thiếu nội dung — trạm CON NGƯỜI
 * KIỂM trong js/pipeline3d.js dạy đúng việc đó — mà vì nội dung ấy được khai cho 10.A1.2, còn
 * 10.A1.1 thì chỉ được viện dẫn bằng hai TÊN HẰNG CHUNG (`TRAM` xuất hiện 13 lần trong
 * pipeline3d.js, `CAU_HOI_T0` 4 lần trong nhamay_tram01.js) trong khi chuỗi "10.A1.1" không tồn
 * tại ở bất kỳ tệp js/ hay data/ nào ngoài bảng tra data/yccd.js. Hai giám khảo độc lập cùng kết
 * luận đó là bằng chứng rỗng, nên hồ sơ đã hạ từ "22/22" xuống "21/22 có bằng chứng trong mã".
 *
 * KẾT CỦA CHUYỆN ĐÓ: chính tệp này đưa con số trở lại 22/22 — nhưng lần này là bằng chứng THẬT,
 * vì chuỗi "10.A1.1" nằm trong tệp CÓ HOẠT ĐỘNG (chứ không phải trong bảng tra), và hoạt động
 * đó được chấm bằng oracle tất định với 34 ca kiểm thử trong tools/tests/test_vaitro_connguoi.js.
 * Vẫn KHÔNG phải PHỦ THẬT ở trục thao tác: ba câu này ở mức nhận diện, và giới hạn đó được ghi
 * thẳng trong hàm pipe3dVaiTro() ở js/app.js thay vì để người đọc tự suy ra.
 *
 * Ba yêu cầu của động từ, và cách tệp này đáp ứng:
 *   · "THỰC HÀNH"    — học sinh phải LÀM (chọn và nhận phán quyết ngay), không phải đọc. Vì vậy
 *                       tệp này là câu hỏi có chấm, không phải bảng chữ để đọc.
 *   · "XÁC ĐỊNH ĐƯỢC" — động từ này CÓ đáp án đúng, nên dùng trắc nghiệm có oracle tất định.
 *                       Cố ý KHÔNG dùng cơ chế tự luận đếm-phương-diện của js/muc3.js: chính thí
 *                       nghiệm đối kháng của dự án (data-source/do_gia_tri_kien_tao.json) đo được
 *                       loại chấm dò-từ-khoá đó có âm tính giả 3/4, tức bài viết tốt vẫn bị xử
 *                       trượt. Thêm một dụng cụ yếu vào hồ sơ là thổi phồng, không phải tăng
 *                       hàm lượng khoa học.
 *   · "MỘT HỆ THỐNG AI CỤ THỂ" — ba câu đều nói về CHÍNH HỆ THỐNG mà học sinh vừa vận hành ở
 *                       trạm này (ống dẫn 5 trạm, trạm CON NGƯỜI KIỂM, bộ dữ liệu lệch 92% ảnh
 *                       ban ngày), không phải một ví dụ tưởng tượng trong sách.
 *
 * MỖI CÂU MỘT ĐỘNG TỪ của YCCĐ, để khi giáo viên nhìn báo cáo thì biết học sinh đạt ở vế nào:
 *   a11-01 -> SỬ DỤNG   (người dùng cuối làm gì trước đầu ra của AI)
 *   a11-02 -> VẬN HÀNH  (ai chặn được lỗi trước khi nó tới người thật)
 *   a11-03 -> TÙY CHỈNH (sửa ở đâu để khắc phục thiên kiến đã đo được)
 *
 * CHUỖI "10.A1.1" NẰM TRONG TỆP NÀY là có chủ đích. tools/tinh_do_phu.py tính mức PHỦ bằng số
 * tệp CÓ CHỨA chuỗi mã YCCĐ (bằng chứng loại MẠNH); tệp nào chỉ được viện dẫn bằng tên hàm thì
 * là bằng chứng loại YẾU và không nâng mức phủ. Khai mã ngay trong dữ liệu câu hỏi — cùng cách
 * data/kienthuc.js đang làm cho 6 mã của nó — để bằng chứng kiểm chứng được bằng máy, không phải
 * bằng suy diễn của người viết bảng.
 *
 * LUẬT VIẾT PHƯƠNG ÁN (thêm 11/10 sau khi cổng G12c bắt được): trong MỖI câu phải có ít nhất
 * một phương án SAI dài hơn đáp án đúng. Nếu đáp án đúng luôn là phương án dài nhất thì học
 * sinh chỉ cần bấm câu dài là ăn điểm mà không cần hiểu bài — điểm đó không chứng minh được
 * yêu cầu cần đạt nào và làm rỗng chính cái claim mà hồ sơ đang nộp. Ca test "đáp án không phải
 * phương án dài nhất" trong tools/tests/test_vaitro_connguoi.js khoá luật này, và cổng G22d
 * chạy bộ test đó trong bộ nghiệm thu, nên câu mới dính cue sẽ ĐỎ ngay khi nghiệm thu.
 * KHÔNG sửa bằng cách cắt ngắn đáp án đúng: phương án đúng cụt thì không nói đủ vai trò, và
 * học sinh giỏi sẽ thấy nó "có vẻ thiếu" rồi chọn nhiễu.
 *
 * AN TOÀN: chữ trong tệp này là HẰNG SỐ do tác giả viết, không phải dữ liệu người dùng, nhưng
 * vẫn đi qua esc() ở nơi render (js/app.js) như mọi nội dung khác — một tệp dữ liệu mới không
 * được phép là ngoại lệ, vì người sửa sau sẽ chép khuôn này.
 */
(function(){
  "use strict";

  /* Ba câu hỏi. `mach`/`unesco` theo đúng trục đã dùng trong data/kienthuc.js: mạch A là "Tư duy
   * lấy con người làm trung tâm", khối UNESCO A1 là "Hiểu: AI phục vụ con người".
   * `loai` không phải trường để chấm — nó là NHÃN cho giáo viên biết câu này đo vế nào của động
   * từ, và để sau này báo cáo có thể tách theo vế thay vì gộp thành một tỉ lệ. */
  const CAU = [
    {
      id: "a11-01", mach: "A", unesco: "A1", yccd: "10.A1.1", vai: "SỬ DỤNG",
      cauHoi: "Em vừa cho trạm CON NGƯỜI KIỂM hỏng và thấy lỗi đi thẳng tới người dùng. "
        + "Trong một hệ thống AI đang dùng thật ở trường em (chấm điểm tự động, gợi ý học liệu, "
        + "điểm danh bằng ảnh), việc nào sau đây là VAI TRÒ của người DÙNG khi sử dụng hệ thống đó?",
      luaChon: [
        /* Nhiễu a cố ý DÀI HƠN đáp án đúng (đo bằng cổng G12c và ca test chống cue).
         * Nó sai vì "đã được kiểm thử" không có nghĩa "mọi đầu ra đều đúng với mục tiêu":
         * chính trạm CON NGƯỜI KIỂM mà học sinh vừa làm hỏng tồn tại vì lý do đó. */
        { id: "a", text: "Tin kết quả ngay vì hệ thống đã được kiểm thử và nghiệm thu đầy đủ "
          + "trước khi triển khai, nên mọi đầu ra của nó đều đã đúng với mục tiêu đặt ra" },
        { id: "b", text: "Đối chiếu kết quả với nguồn khác trước khi dựa vào nó để quyết định, và báo lại khi thấy sai" },
        { id: "c", text: "Tự sửa trọng số của mô hình để kết quả đúng hơn" },
        { id: "d", text: "Ngừng dùng hệ thống vì mọi đầu ra của AI đều không đáng tin" }
      ],
      dapAn: "b",
      giaiThich: "Vai trò của người dùng là KIỂM CHỨNG và PHẢN HỒI, không phải tin tuyệt đối cũng "
        + "không phải bác bỏ toàn bộ. Phương án c là việc của người vận hành hệ thống, không phải "
        + "của người dùng cuối. Chính trạm CON NGƯỜI KIỂM mà em vừa làm hỏng là chỗ tiếp nhận phản "
        + "hồi đó — hỏng nó thì không còn ai chịu trách nhiệm về quyết định cuối cùng. "
        + "Phương án a nghe có lý nhất và cũng dài nhất, nhưng 'đã kiểm thử' chỉ nói lên hệ "
        + "thống chạy đúng thiết kế, không bảo đảm đầu ra đúng với mục tiêu của em."
    },
    {
      id: "a11-02", mach: "A", unesco: "A1", yccd: "10.A1.1", vai: "VẬN HÀNH",
      cauHoi: "Trong năm trạm của ống dẫn em vừa vận hành, trạm nào là chỗ CON NGƯỜI có vai trò "
        + "QUYẾT ĐỊNH để một lỗi của AI không trở thành thiệt hại cho người thật?",
      luaChon: [
        /* Nhiễu a DÀI HƠN đáp án đúng (chống cue 'chọn câu dài'). Nó sai ở chữ "không thể":
         * dữ liệu sạch chỉ làm GIẢM lỗi, không loại được lỗi của mô hình — học sinh đã đo điều
         * đó ở xưởng huấn luyện: cùng bộ dữ liệu đã cân bằng mà mô hình vẫn sai ở ảnh khó. */
        { id: "a", text: "Trạm DỮ LIỆU — vì dữ liệu đã được làm sạch và cân bằng thì mô hình "
          + "không thể sinh ra lỗi, nên không cần ai kiểm tra đầu ra nữa" },
        { id: "b", text: "Trạm HUẤN LUYỆN — vì thuật toán tốt sẽ tự sửa sai" },
        { id: "c", text: "Trạm CON NGƯỜI KIỂM — rà soát, phản hồi và chịu trách nhiệm về quyết định cuối" },
        { id: "d", text: "Trạm ĐẦU RA — vì chỉ cần trình bày kết quả cho rõ ràng" }
      ],
      dapAn: "c",
      giaiThich: "Bốn trạm kia đều là máy và đều có thể sai: dữ liệu lệch, huấn luyện không hội "
        + "tụ, mô hình quá khớp, đầu ra trôi chảy nhưng bịa số liệu. Trạm CON NGƯỜI KIỂM là trạm "
        + "duy nhất có thể CHẶN lỗi trước khi nó gây hại — em vừa thấy điều đó khi làm hỏng nó: "
        + "lỗi đi thẳng tới người dùng và không ai chịu trách nhiệm. Phương án a dài nhất và "
        + "nghe chắc chắn nhất, nhưng chính em đã đo ở xưởng huấn luyện: dữ liệu đã cân bằng "
        + "mà mô hình vẫn sai ở ảnh khó, nên 'dữ liệu sạch thì hết lỗi' là sai."
    },
    {
      id: "a11-03", mach: "A", unesco: "A1", yccd: "10.A1.1", vai: "TÙY CHỈNH",
      cauHoi: "Ở xưởng huấn luyện, bộ dữ liệu 92% ảnh ban ngày làm mô hình sai gần một nửa số ảnh "
        + "ban đêm. Em đã cân bằng dữ liệu và đo lại. Việc đó cho thấy VAI TRÒ TÙY CHỈNH của con "
        + "người nằm ở đâu?",
      luaChon: [
        { id: "a", text: "Con người quyết định thu thập và cân bằng dữ liệu nào, rồi kiểm chứng bằng số đo" },
        /* Nhiễu b DÀI HƠN đáp án đúng (chống cue). Nó sai và sai ĐO ĐƯỢC: học sinh đã bấm tăng
         * vòng huấn luyện trên chính bộ dữ liệu lệch 92% và thấy độ chính xác trên ảnh ban đêm
         * không lên — huấn luyện thêm chỉ làm mô hình thuộc lòng thiên kiến sẵn có. */
        { id: "b", text: "Con người tăng số vòng huấn luyện và hạ thấp ngưỡng chấp nhận cho tới "
          + "khi mô hình tự hết thiên kiến, mà không cần đụng vào dữ liệu đã thu thập" },
        { id: "c", text: "Con người đổi cách trình bày đầu ra để kết quả trông công bằng hơn" },
        { id: "d", text: "Mô hình tự phát hiện và tự sửa thiên kiến trong dữ liệu của nó" }
      ],
      dapAn: "a",
      giaiThich: "Thiên kiến nằm ở DỮ LIỆU, nên sửa ở gốc là sửa dữ liệu — đó là quyết định của con "
        + "người, không phải của máy. Phương án b sai vì huấn luyện thêm trên đúng bộ dữ liệu lệch "
        + "chỉ củng cố thêm thiên kiến — em đã tự đo điều đó: tăng vòng huấn luyện trên bộ dữ "
        + "liệu lệch 92% ảnh ban ngày thì độ chính xác trên ảnh ban đêm không lên. Phương án b "
        + "dài nhất và nghe như một giải pháp kỹ thuật hợp lý, nhưng nó sửa ở ngọn. Phương án c "
        + "chỉ che hiện tượng. Phương án d là điều hệ thống này không tự làm được — và đó chính là "
        + "lý do cần con người trong vòng tùy chỉnh."
    }
  ];

  /* `veCau` trả về MÔ TẢ để app.js render, thay vì tự render. Lý do: tệp này nằm ở tầng dữ liệu,
   * còn app.js mới là nơi có $(), esc(), svgIco(), maHS và ENG. Cho tệp dữ liệu tự render sẽ phải
   * nạp lại cả đống phụ thuộc đó và tạo thêm một đường innerHTML cần kiểm XSS.
   *
   * `cham(id, chonId)` là ORACLE TẤT ĐỊNH: so với đáp án đã khai, không dò từ khoá, không đoán.
   * Trả null khi id không tồn tại — im lặng trả về false sẽ biến lỗi gõ sai id thành "học sinh
   * trả lời sai", tức là đổ lỗi cho học sinh vì lỗi của mã.
   *
   * `diem` là NGUỒN DUY NHẤT của điểm số (1/0). Nơi render (js/app.js pipe3dVaiTro) phải lấy
   * r.diem chứ không được tự tính lại từ r.dung: để hai chỗ cùng suy ra điểm thì khi đổi thang
   * (ví dụ chấm một phần) sẽ có một chỗ bị bỏ sót và CSV ghi điểm khác với điều học sinh thấy. */
  function tim(id){
    for (const c of CAU) { if (c.id === id) return c; }
    return null;
  }
  function cham(id, chonId){
    const c = tim(id);
    if (!c) return null;
    const hopLe = c.luaChon.some(l => l.id === chonId);
    if (!hopLe) return null;
    const dung = chonId === c.dapAn;
    return { id: c.id, dung: dung, diem: dung ? 1 : 0, dapAn: c.dapAn, chon: chonId,
             mach: c.mach, unesco: c.unesco, yccd: c.yccd, vai: c.vai,
             giaiThich: c.giaiThich };
  }

  window.MX_VAI_TRO = { CAU, tim, cham, soCau: CAU.length,
                        maYCCD: "10.A1.1",   /* khai rõ để công cụ độ phủ tìm thấy chuỗi mã */
                        cacVai: CAU.map(c => c.vai) };
})();
