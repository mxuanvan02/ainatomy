#!/usr/bin/env python3
"""Gộp nhật ký CSV/JSON của HỌC AI từ nhiều máy phòng lab thành 1 báo cáo lớp.

TỆP NÀY TỪNG NẰM NGOÀI REPO (06/10 mới đưa vào): README.md §4 hướng dẫn giáo viên chạy
`python3 tools/gop_csv.py`, nhưng tệp thật nằm ở ieeai2026/tools/ — NGOÀI repo. Nghĩa là
một giáo viên clone repo về, làm đúng từng chữ trong README, và nhận `No such file or
directory` ở đúng khâu cuối cùng của tiết học (gộp dữ liệu cả lớp). Đây là chỗ gãy đúng
vào mắt xích "nhân rộng": sản phẩm tự chứa mà thiếu công cụ mà chính tài liệu của nó
hướng dẫn dùng. Nay tệp nằm trong repo, đã test end-to-end (2 máy giả lập -> 3 báo cáo).

Tên cũ "MỔ XẺ AI" đã được thay bằng SOI AI (tên chính thức trong hồ sơ dự thi).

Bối cảnh: app lưu log trong localStorage của TỪNG máy (phòng máy 20 máy = 20 log rời).
Giáo viên thu file bằng nút "Xuất CSV/JSON" trên mỗi máy vào 1 USB, rồi chạy script này.

Cách dùng:
    python3 gop_csv.py <thư_mục_chứa_các_file_xuất> [-o báo_cáo.xlsx] [--prefix mã_lớp]

Đầu ra:
    - nhatky_gop.csv      : toàn bộ sự kiện (đã khử trùng lặp theo máy+mã HS+timestamp)
    - baocao_lop.csv      : recall theo 5 loại lỗi + bản đồ 12 khối UNESCO (cả lớp)
    - baocao_ca_nhan.csv  : từng mã HS một dòng
"""
import argparse, csv, datetime, glob, json, os, re, sys
from collections import defaultdict

LOAI_LOI = {
    "so_lieu_bia": "Số liệu bịa đặt",
    "nguon_khong_ton_tai": "Nguồn/văn bản không tồn tại",
    "thien_kien": "Thiên kiến, định kiến",
    "suy_luan_sai": "Suy luận sai",
    # "Xúi" — phải khớp với ten trong data/meta.js và js/nhamay_text.js. Đây là bản sao
    # thứ ba của cùng một nhãn; lệch thì tệp baocao_lop.csv in ra tên khác với tên học
    # sinh nhìn thấy trong app, và giáo viên không nối được hai bên. Cổng G14 canh ba
    # bản sao này. Xem giải thích về chữ "Xúi" ở data/meta.js.
    "lo_du_lieu_ca_nhan": "Xúi lộ dữ liệu cá nhân",
}
UNESCO = {
    "A1": "A1 Hiểu: AI phục vụ con người", "A2": "A2 Vận dụng: đánh giá AI theo nhu cầu",
    "A3": "A3 Sáng tạo: đề xuất giải pháp AI", "B1": "B1 Hiểu: vấn đề đạo đức AI",
    "B2": "B2 Vận dụng: xử lí tình huống đạo đức", "B3": "B3 Sáng tạo: nguyên tắc dùng AI",
    "C1": "C1 Hiểu: kĩ thuật và ứng dụng AI", "C2": "C2 Vận dụng: dùng công cụ AI",
    "C3": "C3 Sáng tạo: tạo sản phẩm với AI", "D1": "D1 Hiểu: quá trình huấn luyện AI",
    "D2": "D2 Vận dụng: huấn luyện/cải tiến mô hình", "D3": "D3 Sáng tạo: thiết kế hệ thống AI",
}
HDR = ["ma_hs","ma_lop","loai_su_kien","item_id","mach","unesco",
       "dap_an_dung","loai_loi_that","tra_loi","tra_loi_loai","diem","bat_oan","bo_sot",
       "che_do","phien_tong","phien_dung","phien_bat_oan","phien_bo_sot","thoi_gian_ISO",
       # Cột `su_kien` (06/10): phân biệt ba trạng thái của Mức 3 — chot / doiChieu / boQua.
       # PHẢI có trong HDR: tệp gộp được ghi bằng DictWriter(fieldnames=HDR,
       # extrasaction="ignore"), nên cột nào không nằm ở đây sẽ bị VỨT ÂM THẦM khi ghi ra,
       # dù bên đọc (js/engine.js xuatCSV) đã có nó. Đặt cuối để tệp CSV 19 cột cũ vẫn đọc
       # đúng theo tên (doc_csv dùng dict(zip(head, row)), không phụ thuộc thứ tự).
       "su_kien",
       # Cột `phai_lap` (07/10): cờ cho biết phiên pre/post phải lặp lại câu cũ vì ngân hàng
       # đã cạn sau khi loại trừ những câu học sinh đã gặp. Cần nó để LOẠI các phiên đó khỏi
       # tiến trình pre/post trong bao_cao() — một phiên lặp câu không còn là phép đo sạch.
       # App đã ghi cờ này từ commit trước nhưng CSV không có cột nào mang nó, nên lời hứa
       # "gop_csv.py lọc được" chưa thành sự thật cho tới khi cột này tồn tại.
       "phai_lap"]

def doc_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows: return []
    head = rows[0]
    out = []
    # CANH ĐỘ DÀI DÒNG — thêm 06/10.
    #
    # `dict(zip(head, r))` IM LẶNG khi r ngắn hơn head: nó chỉ ghép được len(r) cặp, nên các
    # cột cuối header mất hẳn, và TỆ HƠN là nếu r ngắn vì thiếu một trường ở GIỮA thì mọi giá
    # trị sau chỗ thiếu bị XÊ DỊCH sang cột bên trái. Đã xảy ra thật trong test: một dòng 19
    # trường ghép với header 20 cột làm `thoi_gian_ISO` nhận giá trị rỗng và `su_kien` biến mất.
    # Hậu quả dây chuyền: khóa khử trùng lặp thiếu mốc thời gian nên rơi vào nhánh miễn trừ,
    # tức trùng lặp không bị gộp — và không một dòng cảnh báo nào in ra.
    #
    # Không tự "sửa" bằng cách chèn rỗng: đoán vị trí trường bị thiếu là đoán mò, và đoán sai
    # thì xê dịch dữ liệu còn tệ hơn là báo lỗi. Chỉ CẢNH BÁO rồi ghép như cũ, để giáo viên
    # biết tệp nào cần xuất lại.
    n = len(head)
    for i, r in enumerate(rows[1:], start=2):
        if len(r) != n:
            print(f"  ! {os.path.basename(path)} dòng {i}: có {len(r)} trường nhưng tiêu đề có "
                  f"{n} — cột có thể bị xê dịch. Nên xuất lại tệp này từ app.", file=sys.stderr)
        d = dict(zip(head, r))
        out.append(d)
    return out

def _iso(t_ms):
    """Đổi mốc thời gian epoch-mili giây (số nguyên) sang chuỗi ISO 8601 UTC.

    VÌ SAO HÀM NÀY TỒN TẠI — lỗi tìm được 06/10, và nó âm thầm hơn hai lỗi trước:
    app GHI sự kiện bằng `sk.t = Date.now()` (js/engine.js logSuKien) — tức chỉ có `t`.
    Bản cũ của hàm này đọc `sk.get("t_iso", "")`, một trường KHÔNG TỒN TẠI trong JSON app
    xuất ra. Hệ quả: với mọi tệp JSON, cột thoi_gian_ISO rỗng 100%, mà khóa khử trùng lặp
    ở gop() là (_src, ma_hs, item_id, thoi_gian_ISO) — thời gian rỗng thì MỌI bản ghi cùng
    HS + cùng bài bị coi là trùng và bị xoá mất. Dữ liệu thật mất mà không một dòng lỗi nào
    in ra. Đường CSV không dính lỗi này vì xuatCSV tự đổi `new Date(sk.t).toISOString()`.

    Sửa ở ĐÂY (bên đọc) chứ không sửa bên ghi: tệp JSON mà giáo viên đã tải về trước đây
    chỉ có `t`; nếu chỉ sửa writer thì mọi tệp cũ vẫn hỏng. Đọc cả hai: có `t_iso` thì dùng,
    không thì suy ra từ `t`.

    Định dạng cố ý khớp xuatCSV (đuôi 'Z', có phần mili giây) để hai đường CSV và JSON cho
    ra cùng một chuỗi — nếu không thì cùng một sự kiện tải về hai kiểu sẽ không so được.
    """
    if t_ms is None:
        return ""
    try:
        dt = datetime.datetime.fromtimestamp(float(t_ms) / 1000.0, datetime.timezone.utc)
    except (TypeError, ValueError, OSError, OverflowError):
        return ""            # mốc hỏng thì để rỗng, không làm sập cả báo cáo
    return dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{int(float(t_ms)) % 1000:03d}Z"


def doc_json(path):
    """JSON xuất từ app = {maHS: {maHS, maLop, suKien:[...]}}"""
    d = json.load(open(path, encoding="utf-8"))
    out = []
    for ma, hs in d.items():
        for sk in hs.get("suKien", []):
            kq = sk.get("kq") or {}
            out.append({
                "ma_hs": ma, "ma_lop": hs.get("maLop", ""),
                "loai_su_kien": sk.get("loai", ""),
                # Sự kiện Mức 3 không có kq.itemId (nó không phải nhiệm vụ đấu trường) mà
                # mang mã bài ở sk["baiToan"] ("BT-10"...). Không fallback thì cả 13 ô đổ về
                # item_id rỗng, và vì khóa khử trùng lặp có item_id nên chúng bị coi là bản
                # sao của nhau rồi bị xoá.
                "item_id": kq.get("itemId") or (sk.get("nhiemVu") or {}).get("id", "")
                           or sk.get("baiToan", ""),
                "mach": kq.get("mach") or (sk.get("nhiemVu") or {}).get("mach", ""),
                "unesco": kq.get("unesco") or (sk.get("nhiemVu") or {}).get("unesco", ""),
                "dap_an_dung": kq.get("loaiThat") or kq.get("dapAn", ""),
                # Với Mức 3, câu trả lời của HS là kq["duDoan"] (con số dự đoán, id phương
                # án, hoặc "6/6" với ô tự luận). Ô tự luận đã được cắt còn 400 ký tự ở phía
                # app (js/muc3.js ghi(...slice(0,400))) nên ô này không phình vô hạn.
                "tra_loi": kq.get("traLoiVerdict") or kq.get("chon", "")
                           or kq.get("duDoan", ""),
                "diem": "" if kq.get("diem") is None else kq.get("diem"),
                "bat_oan": 1 if kq.get("batOan") else 0,
                "bo_sot": 1 if kq.get("boSot") else 0,
                # BẢY CỘT BỊ MẤT — thêm 07/10. Đây là lỗi nặng nhất tìm được ở công cụ gộp,
                # và nó KHÔNG do đợt vá này tạo ra: nó có từ khi doc_json được viết.
                #
                # doc_json dựng dict BẰNG TAY theo từng trường, nên cột nào không được gõ ra
                # thì mất hẳn. Trước khi sửa, hàm này chỉ xuất 14/21 cột của HDR; bảy cột thiếu
                # là: loai_loi_that, tra_loi_loai, che_do, phien_tong, phien_dung,
                # phien_bat_oan, phien_bo_sot. Hệ quả trên đường JSON (một trong HAI nút giáo
                # viên bấm được — nút kia là CSV):
                #   · che_do/phien_tong/phien_dung mất -> bao_cao() lọc `r.get("che_do") in
                #     phien` nên MỌI phiên pre/post từ JSON bị bỏ qua. Khối "TIẾN TRÌNH
                #     PRE/POST" trống trơn. Mà hiệu pre/post chính là con số dùng làm bằng
                #     chứng tác động trong hồ sơ dự thi.
                #   · loai_loi_that mất -> bao_cao() lấy key = None -> không khối "RECALL THEO
                #     LOẠI LỖI" nào được đếm, cả 5 loại lỗi ra 0.
                #   · Không một dòng cảnh báo: script vẫn in "✅ N sự kiện" và vẫn ghi đủ 3 tệp.
                #
                # Vì sao đường CSV không dính: xuatCSV (js/engine.js) ghi theo VỊ TRÍ cột từ một
                # mảng header duy nhất, nên thêm cột là tự có. Chỉ doc_json mới liệt kê bằng tay.
                #
                # CÁCH CHỐNG TÁI DIỄN: cổng G16 trong tools/nghiem_thu.py đối chiếu tập cột của
                # doc_json với HDR và với header của xuatCSV — thêm cột mới mà quên sửa doc_json
                # thì cổng FAIL. Không dựa vào trí nhớ của người sửa sau.
                #
                # LƯU Ý HAI CẶP DỄ NHẦM: `bat_oan`/`bo_sot` đọc từ kq (của từng CÂU đấu trường),
                # còn `phien_bat_oan`/`phien_bo_sot` đọc từ sk (tổng kết của cả PHIÊN) — đúng
                # như xuatCSV đang làm. Trộn hai cặp này thì số liệu sai mà không có dấu hiệu.
                "loai_loi_that": kq.get("loaiLoiThat") or "",
                "tra_loi_loai": kq.get("traLoiLoai") or "",
                "che_do": sk.get("cheDo", ""),
                "phien_tong": "" if sk.get("tong") is None else sk.get("tong"),
                "phien_dung": "" if sk.get("dung") is None else sk.get("dung"),
                "phien_bat_oan": "" if sk.get("batOan") is None else sk.get("batOan"),
                "phien_bo_sot": "" if sk.get("boSot") is None else sk.get("boSot"),
                "thoi_gian_ISO": sk.get("t_iso") or _iso(sk.get("t")),
                # Ba trạng thái của Mức 3: chot / doiChieu / boQua. Thiếu cột này thì báo
                # cáo gộp không phân biệt được "dự đoán sai" với "không thèm dự đoán".
                "su_kien": sk.get("suKien", ""),
                # Cờ phiên pre/post phải lặp câu cũ vì ngân hàng đã cạn sau khi loại trừ.
                # ĐƯỜNG JSON TỪNG MẤT CỜ NÀY (07/10): cột phai_lap được thêm vào HDR và vào
                # xuatCSV, nhưng doc_json dựng dict THỦ CÔNG theo từng trường nên nó không tự
                # có — nghĩa là GV xuất CSV thì lọc được phiên bẩn, còn GV xuất JSON thì không.
                # Cùng một dữ liệu, hai kết quả khác nhau tuỳ nút bấm. Đây là cái giá của việc
                # doc_json liệt kê trường bằng tay thay vì suy ra từ HDR; mỗi lần thêm cột phải
                # nhớ sửa cả ba nơi: HDR, xuatCSV (engine.js), doc_json.
                "phai_lap": "" if sk.get("phaiLap") is None else sk.get("phaiLap"),
            })
    return out

def gop(thu_muc):
    rows, nguon = [], []
    for p in sorted(glob.glob(os.path.join(thu_muc, "*"))):
        if not os.path.isfile(p): continue
        low = p.lower()
        try:
            if low.endswith(".csv"): r = doc_csv(p)
            elif low.endswith(".json"): r = doc_json(p)
            else: continue
        except Exception as e:
            print(f"  ! bỏ qua {os.path.basename(p)}: {e}", file=sys.stderr); continue
        nguon.append((os.path.basename(p), len(r)))
        # đánh dấu máy nguồn để khử trùng
        for x in r: x["_src"] = os.path.basename(p)
        rows.extend(r)
    # khử trùng lặp (cùng máy, cùng HS, cùng loại sự kiện, cùng item, cùng trạng thái, cùng thời điểm)
    #
    # SỬA 06/10 — HAI LỖI, MỘT LỖI DO CHÍNH ĐỢT VÁ NÀY GÂY RA:
    #
    # (1) Khoá cũ là (_src, ma_hs, item_id, thoi_gian_ISO) — KHÔNG có `su_kien`. Trước đợt vá
    #     này hai cột item_id và thoi_gian_ISO đều RỖNG với sự kiện Mức 3, nên chúng rơi vào
    #     nhánh miễn trừ và không bao giờ bị khử trùng. Khi doc_json/xuatCSV bắt đầu lấp đúng
    #     hai cột đó, các dòng Mức 3 LẦN ĐẦU TIÊN bị dedup soi tới — và `chot` với `doiChieu`
    #     của cùng một bài (ô tự luận tự chấm qua setTimeout(0), rất dễ chung một mili-giây)
    #     có khoá giống hệt nhau, nên một trong hai bị xoá. Test fixture chứng minh: 3 sự kiện
    #     vào, chỉ 2 ra, và công cụ vẫn in "✅" — mất dữ liệu mà không một dòng cảnh báo.
    #     Thêm `su_kien` (và `loai_su_kien`) vào khoá: hai TRẠNG THÁI khác nhau của cùng một
    #     bài không phải là bản sao của nhau.
    #
    # (2) Nhánh miễn trừ cũ viết là `k != (_src, ma_hs, "", "")` — một tuple CỐ ĐỊNH 4 phần tử.
    #     Nếu chỉ nối dài khoá mà không sửa dòng này thì phép so luôn True (khác độ dài), tức
    #     miễn trừ biến mất hoàn toàn và những dòng không có danh tính bắt đầu bị xoá. Viết lại
    #     thành kiểm tra trường, không so tuple: dòng thiếu item_id HOẶC thiếu mốc thời gian thì
    #     không có cách nào phân biệt với dòng khác, nên GIỮ LẠI thay vì đoán nó trùng.
    seen, uniq = set(), []
    for r in rows:
        if not r.get("item_id") or not r.get("thoi_gian_ISO"):
            uniq.append(r); continue
        k = (r.get("_src"), r.get("ma_hs"), r.get("loai_su_kien"), r.get("item_id"),
             r.get("su_kien"), r.get("thoi_gian_ISO"))
        if k in seen: continue
        seen.add(k); uniq.append(r)
    return uniq, nguon

def bao_cao(rows):
    # recall theo loại lỗi (toàn lớp)
    theo_loai = {k: {"dung":0, "co_loi":0, "bat_oan":0} for k in LOAI_LOI}
    unesco = {k: {"dung":0, "tong":0} for k in UNESCO}
    # `dd_*`: số liệu Mức 3 theo từng học sinh — thêm 07/10. Xem chú thích ở vòng lặp dưới.
    ca_nhan = defaultdict(lambda: {"tong":0, "dung":0, "lab":0, "lop":"", "pre":[], "post":[],
                                   "dd_doi_chieu":0, "dd_khop":0, "dd_bo_qua":0})
    for r in rows:
        if r.get("loai_su_kien") == "dauTruong":
            u = r.get("unesco","")
            if u in unesco:
                unesco[u]["tong"] += 1
                if str(r.get("diem")) == "1": unesco[u]["dung"] += 1
            loai_that = r.get("dap_an_dung","")
            if loai_that == "co_loi":
                key = r.get("loai_loi_that") or None
                if key and key in theo_loai:
                    theo_loai[key]["co_loi"] += 1
                    if str(r.get("diem")) == "1": theo_loai[key]["dung"] += 1
            if str(r.get("bat_oan")) == "1":
                key = r.get("tra_loi_loai") or None
                if key and key in theo_loai: theo_loai[key]["bat_oan"] += 1
        if r.get("loai_su_kien") == "lab":
            ca_nhan[r.get("ma_hs","")]["lab"] += 1
        cn = ca_nhan[r.get("ma_hs","")]
        cn["lop"] = r.get("ma_lop","") or cn["lop"]
        if r.get("loai_su_kien") == "dauTruong":
            cn["tong"] += 1
            if str(r.get("diem")) == "1": cn["dung"] += 1
        # MỨC 3 THEO TỪNG HỌC SINH — thêm 07/10.
        #
        # VÌ SAO: hai ngày trước tôi nối dây để app GHI được ba trạng thái của ô dự đoán
        # (chot / doiChieu / boQua) và hiện chúng trong báo cáo trên màn hình. Nhưng
        # baocao_ca_nhan.csv — tệp giáo viên thật sự dùng để ghi nhận xét cho 40 học sinh —
        # chỉ có 6 cột về đấu trường và lab, KHÔNG có cột nào về dự đoán. Hệ quả: công sức nối
        # dây đó chỉ sống trên từng máy một và biến mất ngay khi gộp 20 máy về một mối, đúng
        # chỗ giáo viên cần nó nhất. Phản biện vòng 9 đã nêu đúng điểm này ("CSV của giáo viên
        # không phân biệt được dự đoán sai với không thèm dự đoán") và tôi mới sửa được một nửa.
        #
        # Đếm `doiChieu` (đã đối chiếu với kết quả thật) chứ không đếm `chot`: `chot` chỉ là
        # lúc học sinh bấm nút, chưa biết đúng sai. Và giữ `bo_qua` thành cột RIÊNG, không cộng
        # gộp vào mẫu số — gộp thì một lớp toàn người bỏ qua trông như một lớp dự đoán sai hết,
        # và giáo viên sẽ dạy sai chỗ. Hai con số trả lời hai câu hỏi khác nhau:
        # "em có tham gia không" và "em hiểu tới đâu".
        if r.get("loai_su_kien") == "duDoan":
            sk_name = r.get("su_kien", "")
            if sk_name == "doiChieu":
                cn["dd_doi_chieu"] += 1
                if str(r.get("diem")) == "1": cn["dd_khop"] += 1
            elif sk_name == "boQua":
                cn["dd_bo_qua"] += 1
    # phiên pre/post: mỗi sự kiện loai_su_kien == "phien" là một phiên hoàn tất
    #
    # LOẠI PHIÊN BỊ NHIỄM — thêm 07/10, và đây là chỗ biến một lời hứa thành sự thật.
    # Commit trước tôi cho app loại những câu học sinh đã gặp khi bốc phiên post-test (vì đo
    # được pre∩post trùng trung bình 1,54/12 câu, 64% số cặp có ít nhất một câu trùng — tức
    # post-test đang đo trí nhớ chứ không đo tiến bộ). Khi ngân hàng cạn, app cho lặp lại và
    # ghi cờ phaiLap, kèm lời hứa NGUYÊN VĂN trong comment: "ghi cờ phaiLap vào nhật ký để
    # tools/gop_csv.py ... lọc bỏ được những phiên không còn là phép đo sạch".
    # Nhưng hàm này vẫn cộng mọi phiên như nhau, nên lời hứa đó chưa thành sự thật cho tới
    # dòng này. Một phiên lặp câu mà vẫn được tính vào "tiến trình pre/post" thì con số tiến
    # bộ trong hồ sơ là con số sai — và sai theo hướng CÓ LỢI, nên sẽ không ai nghi ngờ.
    # Đếm riêng số phiên bị loại để in ra, không âm thầm vứt dữ liệu.
    phien = {"pre": [], "post": []}
    phien_loai = {"pre": 0, "post": 0}
    for r in rows:
        if r.get("loai_su_kien") == "phien" and r.get("che_do") in phien:
            if str(r.get("phai_lap", "")).strip() in ("1", "1.0", "true", "True"):
                phien_loai[r["che_do"]] += 1
                continue
            try:
                t = int(r.get("phien_tong") or 0); dg = int(r.get("phien_dung") or 0)
                if t: phien[r["che_do"]].append(dg / t)
            except ValueError:
                pass
    return theo_loai, unesco, ca_nhan, phien, phien_loai

def ghi(rows, theo_loai, unesco, ca_nhan, phien, phien_loai, outdir):
    p1 = os.path.join(outdir, "nhatky_gop.csv")
    with open(p1, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HDR, extrasaction="ignore"); w.writeheader()
        for r in rows: w.writerow(r)
    p2 = os.path.join(outdir, "baocao_lop.csv")
    with open(p2, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["== RECALL THEO LOẠI LỖI (cả lớp) =="])
        w.writerow(["loai_loi","ten","phat_hien_dung","tong_cau_co_loi","recall","bat_oan"])
        for k, v in theo_loai.items():
            rec = (v["dung"]/v["co_loi"]) if v["co_loi"] else ""
            w.writerow([k, LOAI_LOI[k], v["dung"], v["co_loi"],
                        f"{rec:.3f}" if rec != "" else "", v["bat_oan"]])
        w.writerow([])
        w.writerow(["== TIẾN TRÌNH PRE/POST (trung bình tỉ lệ đúng của các phiên) =="])
        # Cột `phien_bi_loai` — thêm 07/10. Phiên bị loại là phiên mà ngân hàng đã cạn câu mới
        # nên phải lặp lại câu học sinh đã gặp; phiên đó không còn là phép đo sạch và bị bỏ ra
        # khỏi trung bình (xem bao_cao()). IN CON SỐ NÀY RA thay vì âm thầm vứt: giáo viên nhìn
        # thấy "post: 18 phiên, bị loại 3" thì biết ngay 3 phiên nào đáng ngờ, còn nếu chỉ thấy
        # "post: 18" thì không ai biết dữ liệu đã bị lọc.
        w.writerow(["phien","so_phien_tinh","trung_binh_ti_le_dung","so_phien_bi_loai_vi_lap_cau"])
        for mode in ("pre", "post"):
            arr = phien.get(mode, [])
            avg = sum(arr) / len(arr) if arr else ""
            w.writerow([mode, len(arr), f"{avg:.3f}" if avg != "" else "",
                        phien_loai.get(mode, 0)])
        w.writerow([])
        w.writerow(["== BẢN ĐỒ 12 KHỐI NĂNG LỰC UNESCO × QĐ 2422 =="])
        w.writerow(["khoi","ten","dung","tong","ti_le"])
        for k, v in unesco.items():
            t = (v["dung"]/v["tong"]) if v["tong"] else ""
            w.writerow([k, UNESCO[k], v["dung"], v["tong"], f"{t:.3f}" if t != "" else ""])
    p3 = os.path.join(outdir, "baocao_ca_nhan.csv")
    with open(p3, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        # BA CỘT DỰ ĐOÁN — thêm 07/10. Trước đây tệp này chỉ có 6 cột về đấu trường và lab,
        # nên toàn bộ công sức nối dây Mức 3 (app ghi chot/doiChieu/boQua, engine tổng hợp,
        # báo cáo trên màn hình hiện ra) BIẾN MẤT ngay khi gộp 20 máy về một mối — đúng chỗ
        # giáo viên cần nó nhất để ghi nhận xét cho từng em.
        #
        # `du_doan_da_doi_chieu` và `du_doan_khop` là MỘT CẶP (tử/mẫu), không phải hai số rời:
        # chỉ nhìn `khop` thì không biết em đó đối chiếu 1 lần hay 10 lần.
        # `du_doan_bo_qua` để CỘT RIÊNG và cố ý KHÔNG cộng vào mẫu số của `khop`: cộng gộp thì
        # một lớp toàn người bỏ qua sẽ trông như một lớp dự đoán sai hết, và giáo viên sẽ dạy
        # sai chỗ. Hai con số trả lời hai câu hỏi khác nhau — "em có tham gia không" và
        # "em hiểu tới đâu" — nên phải tách ra.
        w.writerow(["ma_hs","ma_lop","so_cau_dau_truong","so_cau_dung","ti_le_dung",
                    "so_nhiem_vu_lab","du_doan_da_doi_chieu","du_doan_khop",
                    "ti_le_du_doan_khop","du_doan_bo_qua"])
        for ma, v in sorted(ca_nhan.items()):
            if not ma: continue
            t = (v["dung"]/v["tong"]) if v["tong"] else ""
            ddc = v["dd_doi_chieu"]
            tk = (v["dd_khop"]/ddc) if ddc else ""
            w.writerow([ma, v["lop"], v["tong"], v["dung"],
                        f"{t:.3f}" if t != "" else "", v["lab"],
                        ddc, v["dd_khop"], f"{tk:.3f}" if tk != "" else "",
                        v["dd_bo_qua"]])
    return p1, p2, p3

def main():
    ap = argparse.ArgumentParser(
        description="Gộp nhật ký HỌC AI từ nhiều máy phòng lab thành một báo cáo lớp.")
    ap.add_argument("thu_muc", help="Thư mục chứa các file CSV/JSON xuất từ các máy")
    ap.add_argument("-o", "--outdir", default=".", help="Thư mục xuất báo cáo (mặc định: hiện tại)")
    args = ap.parse_args()
    if not os.path.isdir(args.thu_muc):
        print(f"LỖI: không thấy thư mục {args.thu_muc}", file=sys.stderr); sys.exit(1)
    rows, nguon = gop(args.thu_muc)
    print(f"Đã đọc {len(nguon)} file nguồn:")
    for n, c in nguon: print(f"  - {n}: {c} dòng")
    if not rows:
        print("KHÔNG có dữ liệu nào. Kiểm tra thư mục có file CSV/JSON xuất từ app không.", file=sys.stderr)
        sys.exit(1)
    # `bao_cao()` nay trả 5 giá trị (thêm phien_loai) và `ghi()` nhận 7 tham số — sửa 07/10.
    # Kiểu trả về của một hàm đổi thì MỌI chỗ gọi phải đổi theo; nếu quên thì script chết ngay
    # khi chạy thật (ValueError: too many values to unpack), và đây là công cụ giáo viên dùng
    # sau tiết học — hỏng lúc đó thì không còn thời gian để sửa.
    theo_loai, unesco, ca_nhan, phien, phien_loai = bao_cao(rows)
    os.makedirs(args.outdir, exist_ok=True)
    p1, p2, p3 = ghi(rows, theo_loai, unesco, ca_nhan, phien, phien_loai, args.outdir)
    print(f"\n✅ {len(rows)} sự kiện từ {len(nguon)} máy, {len(ca_nhan)} mã HS.")
    print(f"   {p1}\n   {p2}\n   {p3}")
    # Nói ra nếu có phiên bị loại khỏi tiến trình pre/post. Không in thì giáo viên chỉ thấy
    # con số tiến bộ đẹp mà không biết nó đã bị lọc — và lọc vì lý do chính đáng (phiên đó lặp
    # câu học sinh đã gặp nên không còn đo được tiến bộ) thì càng phải nói rõ, không giấu.
    loai = sum(phien_loai.values())
    if loai:
        print(f"\n⚠ Đã LOẠI {loai} phiên khỏi tiến trình pre/post vì phải lặp lại câu học sinh "
              f"đã gặp (ngân hàng hết câu mới): "
              + ", ".join(f"{k}: {v}" for k, v in phien_loai.items() if v)
              + ". Những phiên đó không đo được tiến bộ thật — xem cột "
                "'so_phien_bi_loai_vi_lap_cau' trong baocao_lop.csv.")

if __name__ == "__main__":
    main()
