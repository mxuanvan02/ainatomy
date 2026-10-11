#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""INSTRUMENT ĐO GIÁ TRỊ KIẾN TẠO (construct validity) của hai hàm chấm prompt.

VÌ SAO CÓ TỆP NÀY. Anh Văn yêu cầu: chấm từng THAO TÁC thực thi và xét xem thao tác đó có
chứng minh được yêu cầu cần đạt (YCCĐ) không. Với 10.C3.2 "Thực hành đặt prompt giải quyết một
số vấn đề gần gũi trong cuộc sống, học tập MỘT CÁCH HIỆU QUẢ", thao tác app cho làm là GÕ prompt
rồi máy chấm. Máy chấm bằng DÒ TỪ KHOÁ. Loại probe đó có thể đo hình thức thay vì chất lượng —
nên phải ĐO sai số của nó thay vì tin nó.

CÁCH LÀM (không chép lại mã, không đoán):
  1. Nạp MÃ THẬT và DỮ LIỆU THẬT bằng node: eval chính data/kienthuc.js, js/kienthuc.js,
     js/nhamay_text.js với stub document/$ tối thiểu, rồi gọi hàm thật.
  2. Chạy trên tập có nhãn: CA DƯƠNG = prompt thật có nghĩa; CA ÂM = vô nghĩa nhưng nhồi từ khoá.
     Ca âm là ĐƯỜNG SAI CÓ VẺ ĐÚNG: nếu instrument không phân biệt được thì nó phải báo, và báo
     bằng con số, không bằng cảm nhận.
  3. In tỉ lệ dương tính giả / âm tính giả cho TỪNG hàm, kèm nguyên văn ca biên giới.

PHÂN BIỆT HAI HÀM (quan trọng, dễ lẫn):
  · chamPrompt (js/kienthuc.js) — chấm theo de.tuKhoa + de.batBuoc của TỪNG bài, và KẾT QUẢ NÀY
    được log vào nhật ký kèm yccd:"10.C3.2" (kt:143). Đây là hàm chảy vào báo cáo giáo viên.
  · danhGiaPrompt (js/nhamay_text.js) — rubric 3 tiêu chí chung, chỉ HIỆN phản hồi ở ô nm-rubric
    (app.js:1469), không vào điểm nhật ký.
Nên phải đo cả hai: hàm nào sai số lớn hơn, và hàm nào mới là hàm quyết định con số trong hồ sơ.
"""
import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))

# ---------- tập có nhãn ----------
# CA DƯƠNG: prompt thật, có mục tiêu + ngữ cảnh + ràng buộc. Viết theo đúng tinh thần 10.C3.2
# (vấn đề gần gũi trong học tập/cuộc sống, bối cảnh Việt Nam).
CA_DUONG = [
    ("D1_nongNghiep",
     "Hãy giải thích cho nông dân ở Thừa Thiên Huế vì sao mô hình phân loại ảnh cây lúa của em "
     "nhận nhầm ảnh ruộng ngập nước thành ảnh lúa chín. Trả lời bằng bảng 3 cột: nguyên nhân, "
     "dấu hiệu nhận biết, cách khắc phục. Không bịa số liệu."),
    ("D2_hocTap",
     "Em là học sinh lớp 10. Hãy lập dàn ý bài thuyết trình 5 phút về thiên vị dữ liệu trong "
     "hệ thống chấm điểm tự động, gồm 4 phần, mỗi phần tối đa 60 chữ, dùng ví dụ ở trường học "
     "Việt Nam."),
    ("D3_ngan_ma_du",
     "Hãy viết đoạn văn 100 chữ giải thích quá khớp cho học sinh lớp 10, dùng ví dụ ôn thi, "
     "kèm một bảng so sánh 2 cột."),
    ("D4_cau_hoi_hieu",
     "Vì sao ảnh chụp ngược sáng làm mô hình dự đoán sai nhãn, và em nên thu thêm dữ liệu loại "
     "nào để khắc phục? Trình bày thành 3 gạch đầu dòng."),
]
# CA ÂM: vô nghĩa / không phải prompt, nhưng NHỒI đủ từ khoá của rubric. Đây là đường sai có vẻ
# đúng — nếu instrument cho 3/3 thì nó đo sự có mặt của từ, không đo chất lượng.
CA_AM = [
    ("A1_nhoi_tu_toi_thieu", "hãy viết bảng việt nam"),
    ("A2_nhoi_tu_dai", "hãy liệt kê bảng danh sách ví dụ bước tóm tắt việt nam học sinh lớp 10 trường"),
    ("A3_tu_khoa_lien_tiep",
     "bảng danh sách gạch đầu dòng đoạn văn câu ví dụ bước tóm tắt dưới dạng hãy viết giải thích "
     "liệt kê so sánh tìm cho biết đề xuất việt nam học sinh lớp 10 trường nông dân giáo viên "
     "trong vòng không quá dành cho"),
    ("A4_khong_phai_prompt", "aaaa bbbb cccc hãy bảng việt nam"),
]


def tao_harness():
    """Sinh tệp JS nạp mã THẬT + dữ liệu THẬT rồi chạy tập có nhãn."""
    return r"""
const fs = require('fs');
const path = require('path');
const ROOT = %s;

// stub tối thiểu để eval được các module trình duyệt
const el = () => ({ style:{}, className:'', innerHTML:'', textContent:'', value:'',
  appendChild(){}, setAttribute(){}, addEventListener(){}, children:[], focus(){},
  querySelector(){return null;}, insertAdjacentHTML(){} });
global.document = { createElement: el, getElementById: () => null,
  querySelector: () => null, querySelectorAll: () => [], addEventListener(){},
  body: el(), documentElement: el() };
global.$ = () => null;
global.window = {};
global.localStorage = { getItem: () => null, setItem(){}, removeItem(){} };
global.navigator = { userAgent: 'node' };

function nap(p, ten){
  const f = path.join(ROOT, p);
  try { (0, eval)(fs.readFileSync(f, 'utf8')); return true; }
  catch(e){ console.log(JSON.stringify({nap_loi: ten, loi: String(e).slice(0,180)})); return false; }
}

const okData = nap('data/kienthuc.js', 'data/kienthuc.js');
const okKT   = nap('js/kienthuc.js',   'js/kienthuc.js');
const okNM   = nap('js/nhamay_text.js','js/nhamay_text.js');

const KT = window.MX_KIEN_THUC || null;
const NM = window.MX_NHAMAY_TEXT || null;
const DATA = window.MX_KT || null;

console.log(JSON.stringify({
  nap: {data: okData, kienthuc: okKT, nhamay: okNM},
  co: {chamPrompt: !!(KT && KT.chamPrompt), danhGiaPrompt: !!(NM && NM.danhGiaPrompt),
       duLieuBai: !!(DATA && (DATA.promptBaiTap || DATA.baiTapPrompt))}
}));

// tìm bài tập prompt THẬT trong data
let de = null, tenKho = null;
if (DATA) {
  for (const k of Object.keys(DATA)) {
    const v = DATA[k];
    if (Array.isArray(v)) {
      const co = v.find(x => x && typeof x === 'object' && x.tuKhoa && x.batBuoc);
      if (co) { de = co; tenKho = k; break; }
    }
  }
}
console.log(JSON.stringify({de_tim_thay: tenKho, de_id: de ? (de.id||de.ma||null) : null,
  batBuoc: de ? de.batBuoc : null,
  soTieuChi: de ? Object.keys(de.tuKhoa||{}).length : 0}));

const CA_DUONG = %s;
const CA_AM = %s;

function chayChamPrompt(nhan, nhom, txt){
  if (!de || !KT || !KT.chamPrompt) { console.log(JSON.stringify({ham:'chamPrompt', nhom, id:nhan, loi:'khong chay duoc'})); return; }
  let r;
  try { r = KT.chamPrompt(de, txt); } catch(e){ console.log(JSON.stringify({ham:'chamPrompt', nhom, id:nhan, loi:String(e).slice(0,120)})); return; }
  console.log(JSON.stringify({ham:'chamPrompt', nhom, id:nhan, diem:r.diem, datBB:r.datBB,
    tongBB:r.tongBB, datDuoc:r.datDuoc, thieu:r.thieu, doDai:r.doDai}));
}
function chayDanhGia(nhan, nhom, txt){
  if (!NM || !NM.danhGiaPrompt) { console.log(JSON.stringify({ham:'danhGiaPrompt', nhom, id:nhan, loi:'khong chay duoc'})); return; }
  let r;
  try { r = NM.danhGiaPrompt(txt); } catch(e){ console.log(JSON.stringify({ham:'danhGiaPrompt', nhom, id:nhan, loi:String(e).slice(0,120)})); return; }
  console.log(JSON.stringify({ham:'danhGiaPrompt', nhom, id:nhan, diem:r.diem, tong:r.tong, muc:r.muc, dat:r.dat}));
}

for (const [id, txt] of CA_DUONG) { chayChamPrompt(id,'duong',txt); chayDanhGia(id,'duong',txt); }
for (const [id, txt] of CA_AM)    { chayChamPrompt(id,'am',txt);    chayDanhGia(id,'am',txt);    }
"""


def main():
    harness = tao_harness() % (
        json.dumps(ROOT),
        json.dumps(CA_DUONG, ensure_ascii=False),
        json.dumps(CA_AM, ensure_ascii=False),
    )
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
        tf.write(harness)
        tmp = tf.name
    try:
        p = subprocess.run(["node", tmp], capture_output=True, text=True, timeout=120, cwd=ROOT)
    finally:
        os.unlink(tmp)

    if p.returncode != 0:
        print("node LỖI (returncode " + str(p.returncode) + "):")
        print(p.stderr[:1200])
        return 1
    if p.stderr.strip():
        print("  stderr: " + p.stderr.strip()[:400])

    dong = [x for x in p.stdout.strip().split("\n") if x.strip()]
    thong_tin = []
    ket_qua = []
    for d in dong:
        try:
            o = json.loads(d)
        except Exception:
            print("  (không parse) " + d[:200])
            continue
        if "ham" in o:
            ket_qua.append(o)
        else:
            thong_tin.append(o)
            print("  " + json.dumps(o, ensure_ascii=False)[:300])

    # ===== tổng hợp sai số =====
    print("\n" + "=" * 78)
    print("KẾT QUẢ ĐO GIÁ TRỊ KIẾN TẠO")
    print("=" * 78)
    for ham in ("chamPrompt", "danhGiaPrompt"):
        rows = [r for r in ket_qua if r.get("ham") == ham]
        if not rows:
            print("\n" + ham + ": KHÔNG CHẠY ĐƯỢC")
            continue
        print("\n### " + ham + " ###")
        for r in rows:
            if "loi" in r:
                print("  " + r["nhom"] + " " + r["id"] + " LỖI: " + r["loi"])
                continue
            if ham == "chamPrompt":
                diem, tong = r["diem"], r["tongBB"]
                muc = "ĐẠT" if diem >= 0.999 else ("chưa đủ" if diem > 0 else "KHÔNG ĐẠT")
            else:
                diem, tong = r["diem"], r["tong"]
                muc = r["muc"]
            print("  [" + r["nhom"].upper() + "] " + r["id"].ljust(24)
                  + " điểm " + str(round(diem, 3)) + "/" + str(tong) + "  " + muc
                  + ("  đạt=" + ",".join(r["dat"]) if ham == "danhGiaPrompt" and r.get("dat") else ""))

        # sai số: ca ÂM mà ĐẠT = dương tính giả; ca DƯƠNG mà KHÔNG đạt = âm tính giả
        am = [r for r in rows if r.get("nhom") == "am" and "loi" not in r]
        duong = [r for r in rows if r.get("nhom") == "duong" and "loi" not in r]

        def dat(r):
            if ham == "chamPrompt":
                return r["diem"] >= 0.999
            return r["diem"] == r["tong"]

        fp = [r["id"] for r in am if dat(r)]
        fn = [r["id"] for r in duong if not dat(r)]
        print("  --- SAI SỐ ---")
        print("  dương tính giả (vô nghĩa mà ĐẠT): " + str(len(fp)) + "/" + str(len(am))
              + ("  " + str(fp) if fp else ""))
        print("  âm tính giả  (prompt thật mà TRƯỢT): " + str(len(fn)) + "/" + str(len(duong))
              + ("  " + str(fn) if fn else ""))
        if am:
            print("  tỉ lệ dương tính giả: " + str(round(100.0 * len(fp) / len(am), 1)) + "%")
        if duong:
            print("  tỉ lệ âm tính giả   : " + str(round(100.0 * len(fn) / len(duong), 1)) + "%")

    # ghi bằng chứng ra JSON để cổng/tài liệu đọc lại được
    out = os.path.join(ROOT, "data-source", "do_gia_tri_kien_tao.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    io.open(out, "w", encoding="utf-8").write(json.dumps(
        {"mo_ta": "Đo sai số của hai hàm chấm prompt bằng dò từ khoá, chạy trên MÃ THẬT trong node",
         "ca_duong": [x[0] for x in CA_DUONG], "ca_am": [x[0] for x in CA_AM],
         "ket_qua": ket_qua, "thong_tin_nap": thong_tin},
        ensure_ascii=False, indent=2))
    print("\nĐã ghi bằng chứng: " + os.path.relpath(out, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
