#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""Sinh TRANG DUYỆT NHÃN cho ngân hàng câu hỏi sinh bằng LLM — chạy trên điện thoại được.

VÌ SAO CÓ TỆP NÀY. `data/cauhoi_moRong.js` có 56 câu sinh bằng LLM (4 batch × 2 model), đã qua QC
schema 12 luật tự động, nhưng NHÃN thì chưa được tác giả duyệt 100%. Hồ sơ dự thi vì thế phải
khai thẳng giới hạn đó ("56/86 câu sinh bằng LLM và CHƯA được tác giả duyệt nhãn"), và kịch bản
video còn dặn: nếu chưa duyệt xong thì KHÔNG nói trần trụi "86 câu hỏi". Tức đây là việc chặn một
lời khai trong hồ sơ nộp giám khảo — không phải việc làm đẹp.

Trang cũ `ho-so/checklist_duyet_nhan.html` KHÔNG DÙNG ĐƯỢC, đo bằng grep:
  · `viewport` = 0 lần          -> không hiển thị đúng trên điện thoại
  · `localStorage` = 0 lần      -> đóng trình duyệt là MẤT hết kết quả duyệt
  · `download`/`Blob` = 0 lần    -> không xuất được kết quả thành tệp
Một checklist mà tích xong rồi mất thì không tạo ra bằng chứng, và việc duyệt 56 câu sẽ phải làm
lại từ đầu mỗi lần — đó là lý do nó chưa bao giờ được duyệt xong.

HAI QUYẾT ĐỊNH THIẾT KẾ:

1. SINH TỪ MÃ NGUỒN, KHÔNG GÕ TAY. Script này đọc câu hỏi từ `data/cauhoi_moRong.js` và đọc TÊN
   5 loại lỗi từ `data/meta.js`. Không chép tay danh sách nhãn: chép tay là tạo thêm một bản sao
   cần đồng bộ, và bản sao đó sẽ lệch ngay lần đầu ngân hàng đổi (đúng lớp lỗi mà cổng G14 của
   repo này sinh ra để chặn — nhãn trùng nhau ở nhiều bản sao).

2. `claimLoi` là CHỈ SỐ 0-BASED — đã đo, không suy đoán. Đối chiếu 8 câu đầu giữa `claimLoi` và
   chữ trong `giaiThich`:
       g1-01  claimLoi=2  giải thích nói "Câu 3"
       g1-07  claimLoi=0  giải thích nói "Câu 1"
   Tức `claimLoi = N` nghĩa là claims[N] là claim thứ N+1 mà học sinh phải bắt. Nếu trang tô sáng
   theo 1-based thì nó tô SAI claim, và tác giả sẽ duyệt nhãn dựa trên một câu bị dẫn sai — tệ hơn
   là không tô gì, vì trông vẫn có vẻ đúng. Script assert điều này trước khi sinh.

CÁCH CHẠY (từ gốc repo):
    python3 tools/sinh_trang_duyet_nhan.py            # chỉ kiểm + in thống kê, chưa ghi
    python3 tools/sinh_trang_duyet_nhan.py --ghi      # sinh duyet_nhan.html

Đầu ra là MỘT tệp HTML tự chứa (dữ liệu nhúng), mở bằng file:// là chạy, không cần server, không
cần mạng — gửi qua điện thoại cũng mở được. Kết quả duyệt lưu trong localStorage của máy người
duyệt và xuất ra JSON/CSV bằng nút trong trang.
"""
import io
import json
import os
import re
import sys

# Gốc repo suy từ vị trí tệp: <repo>/tools/x.py -> hai lần dirname. KHÔNG ghi cứng đường dẫn máy
# tác giả — cổng G18a/G18b của chính repo này canh điều đó, và tệp này nằm trong tầm quét.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NGUON = os.path.join(ROOT, "data", "cauhoi_moRong.js")
META = os.path.join(ROOT, "data", "meta.js")
OUT = os.path.join(ROOT, "duyet_nhan.html")

# Khoá localStorage của TRANG DUYỆT. Đặt khác khoá của app (`soiai_dulieu_v1`) để hai bên không
# giẫm nhau: app lưu tiến trình học sinh, trang này lưu phán quyết của tác giả.
KHOA_LUU = "hocai_duyetnhan_v1"


def doc(p):
    return io.open(p, encoding="utf-8").read()


def lay_items():
    """Đọc 56 item từ data/cauhoi_moRong.js."""
    s = doc(NGUON)
    m = re.search(r"window\.MX_BANK_MORE\s*=\s*(\[.*\])\s*;?\s*$", s, re.S)
    if not m:
        raise SystemExit(f"!!! không tìm thấy window.MX_BANK_MORE trong {NGUON}")
    return json.loads(m.group(1))


def lay_nhan_loai_loi():
    """Đọc TÊN 5 loại lỗi từ data/meta.js — không gõ tay.

    meta.js khai dạng `loaiLoi: { so_lieu_bia: { ten: "…", … }, … }`. Lấy khoá + ten.
    """
    s = doc(META)
    m = re.search(r"loaiLoi\s*:\s*\{(?P<body>.*?)\n\s{2}\},", s, re.S)
    if not m:
        # Fallback có chủ ý: nếu định dạng đổi thì NÓI RA, không đoán danh sách thay thế.
        raise SystemExit("!!! không định vị được khối loaiLoi trong data/meta.js — định dạng đã đổi?"
                         " Sửa hàm này, đừng gõ tay danh sách nhãn.")
    out = {}
    for khoa, ten in re.findall(r"(\w+)\s*:\s*\{[^{}]*?ten\s*:\s*\"([^\"]+)\"", m.group("body"), re.S):
        out[khoa] = ten
    if not out:
        raise SystemExit("!!! đọc được khối loaiLoi nhưng không trích ra nhãn nào")
    return out


def kiem_claim_loi(items):
    """Assert `claimLoi` là 0-based và nằm trong phạm vi claims.

    Đây là phép kiểm cho chính giả thuyết đã dùng để tô sáng. Nếu một ngày ngân hàng đổi sang
    1-based, phép này KÊU thay vì để trang âm thầm tô sai claim.
    """
    loi = []
    for it in items:
        if it["loai"] != "co_loi":
            continue
        cl = it["claimLoi"]
        n = len(it["claims"])
        if not (0 <= cl < n):
            loi.append(f"{it['id']}: claimLoi={cl} ngoài phạm vi 0..{n-1}")
        # Đối chiếu chữ trong giaiThich: nó phải nhắc tới claim thứ (cl+1).
        m = re.search(r"[Cc]â[u y]\s*(?:thứ\s*)?([0-9]+)", it["giaiThich"])
        if m and int(m.group(1)) != cl + 1:
            loi.append(f"{it['id']}: claimLoi={cl} nhưng giaiThich nhắc câu {m.group(1)} "
                       f"— 0-based sẽ là câu {cl+1}. NGÂN HÀNG ĐÃ ĐỔI ƯỚC?")
    return loi


TEMPLATE = r"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<!-- viewport: trang cũ THIẾU cái này nên không dùng được trên điện thoại -->
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TEN__ — Duyệt nhãn __SO__ câu sinh bằng LLM</title>
<style>
:root{
  --primary:#7C3AED; --dung:#146B33; --sai:#B91C1C;
  --nen:#FAF5FF; --the:#FFFFFF; --chu:#1E1B4B; --chu2:#5B5675; --vien:#E4DCF2;
}
*{box-sizing:border-box}
body{margin:0;background:var(--nen);color:var(--chu);
  font:16px/1.55 Carlito,Calibri,"Segoe UI",system-ui,sans-serif}
header{position:sticky;top:0;z-index:5;background:var(--the);border-bottom:1px solid var(--vien);
  padding:10px 12px;box-shadow:0 1px 3px rgba(30,27,75,.08)}
h1{margin:0 0 2px;font-size:17px}
.mo{margin:0;font-size:13px;color:var(--chu2)}
#tien{margin-top:7px;height:7px;background:var(--vien);border-radius:4px;overflow:hidden}
#tien i{display:block;height:100%;background:var(--primary);width:0;transition:width .2s}
#dem{margin-top:5px;font-size:13px;font-weight:700}
nav{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}
nav button{flex:1;min-width:74px;padding:7px 4px;border:1px solid var(--vien);background:var(--the);
  color:var(--chu);border-radius:7px;font-size:13px;cursor:pointer}
nav button[aria-pressed="true"]{background:var(--primary);border-color:var(--primary);color:#fff;font-weight:700}
.xuat{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}
.xuat button,.xoab button{padding:8px 10px;border-radius:7px;border:1px solid var(--vien);
  background:var(--the);color:var(--chu);font-size:13px;cursor:pointer;flex:1;min-width:110px}
main{padding:12px;max-width:820px;margin:0 auto}
article{background:var(--the);border:1px solid var(--vien);border-radius:11px;padding:12px;margin-bottom:12px}
article.da-dung{border-left:5px solid var(--dung)}
article.da-sai{border-left:5px solid var(--sai)}
.dau{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:7px}
.id{font-weight:700;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:14px}
.nhan{font-size:12px;padding:2px 7px;border-radius:20px;border:1px solid var(--vien);color:var(--chu2)}
.nhan.loi{background:#FDECEC;border-color:#F3C7C7;color:var(--sai);font-weight:700}
.nhan.ok{background:#EAF5EE;border-color:#C6E3D0;color:var(--dung);font-weight:700}
.boi{font-style:italic;color:var(--chu2);font-size:14px;margin:0 0 8px}
ol{margin:0 0 9px;padding-left:22px}
ol li{margin-bottom:6px}
ol li.claim-loi{background:#FDECEC;border-left:3px solid var(--sai);padding:4px 6px;
  margin-left:-9px;border-radius:0 5px 5px 0;list-style-position:inside}
.gt{font-size:14px;color:var(--chu2);border-top:1px dashed var(--vien);padding-top:7px;margin-bottom:9px}
.gt summary{cursor:pointer;color:var(--primary);font-weight:700;font-size:14px}
.phim{display:flex;gap:8px}
.phim button{flex:1;padding:13px 6px;border-radius:9px;border:2px solid var(--vien);background:var(--the);
  font-size:15px;font-weight:700;cursor:pointer;color:var(--chu)}
.phim button.dung[aria-pressed="true"]{background:var(--dung);border-color:var(--dung);color:#fff}
.phim button.sai[aria-pressed="true"]{background:var(--sai);border-color:var(--sai);color:#fff}
.sua{margin-top:9px;padding-top:9px;border-top:1px dashed var(--vien)}
.sua label{display:block;font-size:13px;font-weight:700;margin-bottom:4px}
.sua select,.sua textarea{width:100%;padding:9px;border:1px solid var(--vien);border-radius:7px;
  font:14px/1.45 inherit;color:var(--chu);background:#fff}
.sua textarea{min-height:62px;margin-bottom:8px}
.rong{text-align:center;color:var(--chu2);padding:40px 12px}
.xoab{margin:18px auto 40px;max-width:820px;padding:0 12px}
.xoab button{border-color:#F3C7C7;color:var(--sai)}
footer{padding:0 12px 30px;max-width:820px;margin:0 auto;font-size:12px;color:var(--chu2)}
@media (max-width:420px){ body{font-size:15px} h1{font-size:16px} }
</style>
</head>
<body>
<header>
  <h1>__TEN__ — Duyệt nhãn câu hỏi sinh bằng LLM</h1>
  <p class="mo">__SO__ câu trong <code>data/cauhoi_moRong.js</code>. QC tự động đã đạt schema 12 luật;
     đây là bước TÁC GIẢ xác nhận nhãn. Claim có lỗi được tô đỏ (chỉ số <code>claimLoi</code> là 0-based).</p>
  <div id="tien"><i></i></div>
  <div id="dem">Chưa duyệt câu nào</div>
  <nav id="loc"></nav>
  <div class="xuat">
    <button type="button" id="b-json">Xuất JSON</button>
    <button type="button" id="b-csv">Xuất CSV</button>
  </div>
</header>

<main id="ds"></main>

<div class="xoab"><button type="button" id="b-xoa">Xóa kết quả duyệt trên máy này</button></div>

<footer>
  Kết quả lưu trong <code>localStorage</code> của máy này dưới khoá <code>__KHOA__</code> — đóng
  trình duyệt không mất, nhưng máy phòng lab có thể bị đóng băng ổ nên hãy XUẤT tệp sau mỗi đợt duyệt.
  Trang này do <code>tools/sinh_trang_duyet_nhan.py</code> sinh ra từ mã nguồn; sửa tay tệp HTML sẽ bị
  lần sinh kế tiếp ghi đè.
</footer>

<script>
// DỮ LIỆU NHÚNG — do script Python sinh từ data/cauhoi_moRong.js và data/meta.js, KHÔNG gõ tay.
const ITEMS = __ITEMS__;
const NHAN_LOAI_LOI = __NHAN__;
const KHOA = "__KHOA__";

let loc = "tatca";
let ket = {};
try { ket = JSON.parse(localStorage.getItem(KHOA) || "{}") || {}; } catch (e) { ket = {}; }

const $ = (s, r) => (r || document).querySelector(s);

// VỀ innerHTML VÀ XSS — đây là điểm cần nói rõ, không phải để bỏ qua cảnh báo.
//
// Trang này dựng DOM bằng innerHTML, và dữ liệu đưa vào gồm BA loại:
//   (1) câu hỏi do LLM sinh ra (claims, giaiThich, boiCanh) — KHÔNG phải nguồn tin cậy tuyệt đối;
//   (2) ghi chú do chính người duyệt gõ vào ô textarea — đầu vào người dùng, đúng nghĩa untrusted;
//   (3) nhãn loại lỗi đọc từ data/meta.js.
// Cả ba đều đi qua esc() ở MỌI chỗ nội suy, không có ngoại lệ.
//
// esc() thoát cả NĂM ký tự `& < > " '`. Bản đầu chỉ thoát bốn (thiếu `'`), và tuy mọi thuộc tính
// trong mẫu này đều đặt trong dấu nháy kép nên chưa hở, nhưng "chưa hở" là do may mắn về cách viết
// chứ không phải do thiết kế: ai đó thêm một thuộc tính dùng nháy đơn là thành lỗ hổng thật. Thoát cả
// `'` là phòng thủ theo chiều sâu, chi phí bằng 0.
//
// ĐÃ CHỨNG MINH BẰNG TEST, không chỉ bằng lời: tools/tests/xss_duyet_nhan.py cấy payload
// `"><img src=x onerror=alert(1)>` vào cả claims lẫn ghi chú, rồi kiểm trang sinh ra KHÔNG cho phép
// payload thoát khỏi chuỗi. Một phép kiểm chưa từng FAIL thì chưa chứng minh được nó có thể fail.
const esc = s => String(s == null ? "" : s).replace(/[&<>"']/g,
  c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

function luu() {
  try { localStorage.setItem(KHOA, JSON.stringify(ket)); } catch (e) { /* hết chỗ: bỏ qua */ }
  veTienDo();
}

const LOCS = [
  ["tatca", "Tất cả"],
  ["chua", "Chưa duyệt"],
  ["dung", "Nhãn đúng"],
  ["sai", "Cần sửa"],
];

function veLoc() {
  $("#loc").innerHTML = LOCS.map(([k, ten]) => {
    let n = ITEMS.length;
    if (k === "chua") n = ITEMS.filter(i => !ket[i.id]).length;
    else if (k === "dung") n = ITEMS.filter(i => ket[i.id] && ket[i.id].p === "dung").length;
    else if (k === "sai") n = ITEMS.filter(i => ket[i.id] && ket[i.id].p === "sai").length;
    return '<button type="button" data-k="' + k + '" aria-pressed="' + (loc === k) + '">'
      + esc(ten) + " (" + n + ")</button>";
  }).join("");
  $("#loc").querySelectorAll("button").forEach(b =>
    b.onclick = () => { loc = b.dataset.k; veLoc(); veDs(); });
}

function veTienDo() {
  const da = ITEMS.filter(i => ket[i.id]).length;
  const n = ITEMS.length;
  $("#tien i").style.width = (n ? Math.round(da / n * 100) : 0) + "%";
  const d = ITEMS.filter(i => ket[i.id] && ket[i.id].p === "dung").length;
  const s = ITEMS.filter(i => ket[i.id] && ket[i.id].p === "sai").length;
  $("#dem").textContent = da === n && n > 0
    ? "ĐÃ DUYỆT XONG " + n + "/" + n + " — nhãn đúng " + d + " · cần sửa " + s
    : "Đã duyệt " + da + "/" + n + " — nhãn đúng " + d + " · cần sửa " + s
      + (da === 0 ? "" : " · còn " + (n - da) + " câu");
  veLoc();
}

function veDs() {
  const ds = ITEMS.filter(i => {
    if (loc === "chua") return !ket[i.id];
    if (loc === "dung") return ket[i.id] && ket[i.id].p === "dung";
    if (loc === "sai") return ket[i.id] && ket[i.id].p === "sai";
    return true;
  });
  if (!ds.length) { $("#ds").innerHTML = '<p class="rong">Không có câu nào trong bộ lọc này.</p>'; return; }

  $("#ds").innerHTML = ds.map(it => {
    const k = ket[it.id] || {};
    const cls = k.p === "dung" ? "da-dung" : (k.p === "sai" ? "da-sai" : "");
    const claims = it.claims.map((c, idx) => {
      // claimLoi là 0-BASED: claims[claimLoi] mới là claim có lỗi (đã đo trước khi sinh).
      const loi = (it.loai === "co_loi" && idx === it.claimLoi);
      return '<li class="' + (loi ? "claim-loi" : "") + '">' + esc(c)
        + (loi ? ' <strong>← nhãn nói đây là chỗ có lỗi</strong>' : "") + "</li>";
    }).join("");

    const nhan = it.loai === "co_loi"
      ? '<span class="nhan loi">có lỗi · ' + esc(NHAN_LOAI_LOI[it.loaiLoi] || it.loaiLoi) + "</span>"
      : '<span class="nhan ok">không có lỗi</span>';

    const opts = ['<option value="">— chọn nhãn đúng —</option>']
      .concat(Object.keys(NHAN_LOAI_LOI).map(kk =>
        '<option value="' + kk + '"' + (k.nhan === kk ? " selected" : "") + ">"
        + esc(NHAN_LOAI_LOI[kk]) + "</option>"))
      .concat(['<option value="dung"' + (k.nhan === "dung" ? " selected" : "") + ">Không có lỗi</option>"])
      .join("");

    return '<article class="' + cls + '" data-id="' + esc(it.id) + '">'
      + '<div class="dau"><span class="id">' + esc(it.id) + "</span>"
      + '<span class="nhan">mạch ' + esc(it.mach) + "</span>"
      + '<span class="nhan">' + esc(it.unesco) + "</span>" + nhan + "</div>"
      + '<p class="boi">' + esc(it.boiCanh) + "</p>"
      + "<ol>" + claims + "</ol>"
      + '<details class="gt"><summary>Lời giải của hệ (mở ra để đối chiếu)</summary>'
      + esc(it.giaiThich) + "</details>"
      + '<div class="phim">'
      + '<button type="button" class="dung" data-p="dung" aria-pressed="' + (k.p === "dung") + '">Nhãn đúng</button>'
      + '<button type="button" class="sai" data-p="sai" aria-pressed="' + (k.p === "sai") + '">Cần sửa</button>'
      + "</div>"
      + (k.p === "sai"
        ? '<div class="sua"><label for="n-' + esc(it.id) + '">Nhãn đúng phải là</label>'
          + '<select id="n-' + esc(it.id) + '" data-f="nhan">' + opts + "</select>"
          + '<label for="g-' + esc(it.id) + '">Ghi chú (vì sao sai, sửa thế nào)</label>'
          + '<textarea id="g-' + esc(it.id) + '" data-f="ghiChu">' + esc(k.ghiChu || "") + "</textarea></div>"
        : "")
      + "</article>";
  }).join("");

  $("#ds").querySelectorAll("article").forEach(a => {
    const id = a.dataset.id;
    a.querySelectorAll(".phim button").forEach(b => b.onclick = () => {
      const cu = ket[id] || {};
      if (cu.p === b.dataset.p) delete ket[id];       // bấm lại = bỏ đánh dấu
      else ket[id] = { p: b.dataset.p, nhan: cu.nhan || "", ghiChu: cu.ghiChu || "", t: Date.now() };
      luu(); veDs();
    });
    a.querySelectorAll("[data-f]").forEach(f => f.onchange = () => {
      ket[id] = ket[id] || { p: "sai", t: Date.now() };
      ket[id][f.dataset.f] = f.value;
      ket[id].t = Date.now();
      luu();
    });
    a.querySelectorAll("textarea").forEach(f => f.oninput = f.onchange);
  });
}

function taiFile(noiDung, ten, mime) {
  const b = new Blob([noiDung], { type: mime });
  const u = URL.createObjectURL(b);
  const a = document.createElement("a");
  a.href = u; a.download = ten; document.body.appendChild(a); a.click();
  setTimeout(() => { URL.revokeObjectURL(u); a.remove(); }, 400);
}

function goi() {
  const da = ITEMS.filter(i => ket[i.id]);
  return {
    nguon: "data/cauhoi_moRong.js",
    sinhLuc: new Date().toISOString(),
    tongItem: ITEMS.length,
    daDuyet: da.length,
    nhanDung: da.filter(i => ket[i.id].p === "dung").length,
    canSua: da.filter(i => ket[i.id].p === "sai").length,
    chiTiet: da.map(i => Object.assign({ id: i.id }, ket[i.id], {
      loaiGoc: i.loai, loaiLoiGoc: i.loaiLoi || null,
    })),
  };
}

$("#b-json").onclick = () => taiFile(JSON.stringify(goi(), null, 1),
  "duyet_nhan_" + Date.now() + ".json", "application/json");

$("#b-csv").onclick = () => {
  const cot = ["id", "mach", "unesco", "loai_goc", "loai_loi_goc", "phan_quyet", "nhan_dung", "ghi_chu", "luc"];
  const esc2 = v => '"' + String(v == null ? "" : v).replace(/"/g, '""') + '"';
  const dong = ITEMS.filter(i => ket[i.id]).map(i => {
    const k = ket[i.id];
    return [i.id, i.mach, i.unesco, i.loai, i.loaiLoi || "", k.p, k.nhan || "", k.ghiChu || "",
      new Date(k.t).toISOString()].map(esc2).join(",");
  });
  taiFile("\ufeff" + cot.join(",") + "\n" + dong.join("\n") + "\n",
    "duyet_nhan_" + Date.now() + ".csv", "text/csv;charset=utf-8");
};

// Nút xóa: phải gõ chữ XÓA thay vì bấm một lần, và tự tải bản dự phòng TRƯỚC khi hỏi — cùng cách
// phòng vệ mà app chính đang dùng cho nút "Xóa dữ liệu trên máy này", vì đây là công sức duyệt tay.
$("#b-xoa").onclick = () => {
  if (!Object.keys(ket).length) { alert("Chưa có kết quả duyệt nào trên máy này."); return; }
  taiFile(JSON.stringify(goi(), null, 1), "duyet_nhan_SAO_LUU_truoc_khi_xoa_" + Date.now() + ".json",
    "application/json");
  const c = prompt("Đã tải bản sao lưu. Gõ chữ XÓA để xóa kết quả duyệt trên máy này:");
  if (c === "XÓA") { ket = {}; luu(); veDs(); }
  else if (c !== null) alert("Không đúng chữ XÓA — chưa xóa gì cả.");
};

veTienDo();
veDs();
</script>
</body>
</html>
"""


def main():
    ghi = "--ghi" in sys.argv
    items = lay_items()
    nhan = lay_nhan_loai_loi()

    print(f"ROOT (suy từ vị trí tệp): {ROOT}")
    print("=" * 92)
    print(f"  đọc {os.path.relpath(NGUON, ROOT)}: {len(items)} item")
    print(f"  đọc {os.path.relpath(META, ROOT)}: {len(nhan)} nhãn loại lỗi -> {json.dumps(nhan, ensure_ascii=False)}")

    # ASSERT trước khi sinh: mọi item phải đủ trường, và claimLoi phải 0-based.
    loi = []
    for it in items:
        for k in ("id", "mach", "unesco", "loai", "boiCanh", "claims", "giaiThich"):
            if k not in it:
                loi.append(f"{it.get('id','?')}: thiếu trường {k}")
        if len(it.get("claims", [])) != 3:
            loi.append(f"{it['id']}: có {len(it.get('claims', []))} claims, kỳ vọng 3")
        if it["loai"] == "co_loi":
            if "loaiLoi" not in it:
                loi.append(f"{it['id']}: loai=co_loi mà thiếu loaiLoi")
            elif it["loaiLoi"] not in nhan:
                loi.append(f"{it['id']}: loaiLoi={it['loaiLoi']!r} không có trong data/meta.js")
        elif it["loai"] != "dung":
            loi.append(f"{it['id']}: loai={it['loai']!r} lạ")
    loi += kiem_claim_loi(items)
    ids = [i["id"] for i in items]
    if len(set(ids)) != len(ids):
        loi.append(f"id trùng nhau: {len(ids)} item nhưng chỉ {len(set(ids))} id duy nhất")

    if loi:
        print(f"\nDỪNG — {len(loi)} vấn đề, KHÔNG sinh gì:")
        for l in loi[:20]:
            print("  !", l)
        print("\nSửa dữ liệu hoặc sửa giả thuyết trước khi sinh trang. Đừng sinh một trang tô sai")
        print("claim: tác giả sẽ duyệt nhãn dựa trên câu bị dẫn sai, và trông vẫn có vẻ đúng.")
        return 1

    print(f"\n  ASSERT đạt: {len(items)} item đủ trường · {len(nhan)} nhãn khớp data/meta.js ·")
    print(f"              claimLoi là 0-based (đối chiếu với chữ trong giaiThich) · id không trùng")

    # NHÚNG JSON VÀO <script> — PHẢI THOÁT `<`, và đây không phải phòng xa suông.
    # `json.dumps(..., ensure_ascii=False)` giữ nguyên `<`, `>`, `/`. Nghĩa là nếu một claim do LLM
    # sinh ra có chứa chuỗi `</script>`, nó sẽ ĐÓNG SỚM khối script và phần sau đó thành HTML sống —
    # thoát hoàn toàn khỏi esc(), vì esc() chỉ chạy khi dựng DOM chứ không chạy lúc parse HTML.
    # Hiện dữ liệu thật chưa có ký tự `<` nào (đã đo), nhưng "chưa có" là do may mắn về nội dung,
    # không phải do thiết kế: thêm một câu hỏi có `<` là thành lỗ hổng. Nên thoát `<` thành \u003c
    # lúc nhúng — JSON vẫn parse ra đúng ký tự `<`, còn trình duyệt thì không bao giờ thấy thẻ.
    def nhungs(obj):
        return (json.dumps(obj, ensure_ascii=False)
                .replace("<", "\\u003c").replace(">", "\\u003e"))

    html = (TEMPLATE
            .replace("__TEN__", "AInatomy")
            .replace("__SO__", str(len(items)))
            .replace("__KHOA__", KHOA_LUU)
            .replace("__NHAN__", nhungs(nhan))
            .replace("__ITEMS__", nhungs(items)))

    # Chốt cuối: không còn placeholder nào sót (sót thì trang hiển thị chữ __TEN__ thô).
    con = re.findall(r"__[A-Z_]+__", html)
    if con:
        print(f"\nDỪNG — còn placeholder chưa thay: {sorted(set(con))}")
        return 1

    # Chốt thứ hai: khối dữ liệu nhúng không được chứa dấu `<` thô. Nếu có thì chính tệp này đã
    # sinh ra một trang breakout được, và test xss_duyet_nhan.py sẽ kêu — thà kêu ở đây trước.
    m_items = re.search(r"const ITEMS = (\[.*?\]);\nconst NHAN_LOAI_LOI", html, re.S)
    if not m_items:
        print("\nDỪNG — không định vị được khối ITEMS trong trang vừa dựng")
        return 1
    dau_nho = m_items.group(1).count("<")
    if dau_nho:
        print(f"\nDỪNG — khối ITEMS chứa {dau_nho} dấu `<` thô, trang breakout được")
        return 1
    try:
        json.loads(m_items.group(1))
    except json.JSONDecodeError as e:
        print(f"\nDỪNG — khối ITEMS không parse được thành JSON sau khi thoát: {e}")
        return 1
    print("  ASSERT đạt: khối dữ liệu nhúng không có `<` thô và vẫn parse được thành JSON")

    print(f"\n  kích thước trang sẽ sinh: {len(html.encode('utf-8'))/1024:.1f} KB")
    if not ghi:
        print("\n(Chế độ CHỈ KIỂM — chưa ghi gì. Thêm --ghi để sinh tệp.)")
        return 0

    io.open(OUT, "w", encoding="utf-8").write(html)
    print(f"\nĐÃ GHI {os.path.relpath(OUT, ROOT)}")
    print("  mở bằng trình duyệt: file://" + OUT)
    print("  hoặc gửi tệp đó qua điện thoại — không cần server, không cần mạng.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
