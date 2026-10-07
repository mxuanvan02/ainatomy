#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MUTATION TEST CỔNG G18 — bốn ca, có một ca đối chứng âm.

VÌ SAO CÓ TỆP NÀY. G18 được thêm ngày 07/10 để canh lời khai ở README §0 ("mọi công cụ trong
tools/ tự suy gốc repo, không ghi cứng đường dẫn máy tác giả"). Nhưng một cổng mới mà chưa có
mutation test thì chỉ là một lời khai khác: nó ĐẠT ngay lần chạy đầu chưa chứng minh nó thấy
được gì — có thể nó mù. Mọi cổng khác trong repo này đều có script mutation riêng (G10f, G11,
G12, G12c, G13, G14, G15, G16, G17, G17def, html_song); G18 mà thiếu thì hồ sơ khai "mọi cổng
đều được chứng minh có răng" là khai quá.

CÁCH PHÁ KHÁC MỌI SCRIPT TRONG THƯ MỤC NÀY. Các script kia sửa một tệp có thật rồi khôi phục.
Script này TẠO MỘT TỆP THĂM DÒ rồi xoá, vì ba lý do:
· G18 quét MỌI tệp .py dưới tools/, nên một tệp mới đủ để nó nhìn thấy — không cần đụng tới
  công cụ thật.
· Không có rủi ro để lại một công cụ đang chạy bị hỏng giữa chừng nếu script chết giữa đường.
· Việc khôi phục là xoá tệp, kiểm chứng được bằng "tệp không còn tồn tại" — chắc hơn so khớp hash.
Tệp thăm dò được đặt tên có tiền tố để thấy ngay nó không phải công cụ thật, và luôn bị xoá
trong khối finally.

BỐN CA:
  CA 1 — tệp thăm dò ghi cứng đường dẫn /home/<user>/... trong MÃ SỐNG        -> G18a PHẢI kêu
  CA 2 — tệp thăm dò ghi cứng tên thư mục dự án cha (trỏ ngược ra ngoài repo)  -> G18b PHẢI kêu
  CA 3 — tệp thăm dò dùng os.walk mà KHÔNG import os                          -> G18c PHẢI kêu
  CA 4 — ĐỐI CHỨNG ÂM: tệp thăm dò hợp lệ, có nhắc đường dẫn cũ nhưng chỉ trong
         DOCSTRING (kể lại lịch sử lỗi) và import đủ                          -> G18 PHẢI IM

CA 4 là ca quan trọng nhất, và nó có thật từ một lỗi đã xảy ra. G18a được thiết kế bỏ qua
docstring vì docstring kể lại lịch sử lỗi là hợp lệ; nếu bỏ sót luật đó thì chính docstring của
nghiem_thu.py (nơi ghi lại đường dẫn cũ để giải thích vì sao có G18) sẽ làm cổng đỏ vĩnh viễn.
Cổng đỏ vì lý do không ai sửa được thì người ta bắt đầu bỏ qua mọi cảnh báo của nó — đó là bài
học G11b. Ca này kiểm luật miễn trừ đó vẫn còn tác dụng.

MỘT RÀNG BUỘC CỦA CHÍNH TỆP NÀY: nó nằm dưới tools/, nên chính nó bị G18 quét. Vì thế mọi
chuỗi nhạy cảm trong đây đều được GHÉP lúc chạy, không viết nguyên chữ — nếu không thì tệp đi
kiểm lỗi lại tự chứa lỗi. Đây là lần thứ tư trong dự án một cổng/script bắt oan chính nó.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

# Gốc repo suy từ vị trí tệp: <repo>/tools/tests/mutation/x.py -> bốn lần dirname.
# KHÔNG ghi cứng đường dẫn máy tác giả — chính G18a canh điều đó, và tệp này nằm trong tầm quét.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
GATE = [sys.executable, os.path.join(ROOT, "tools", "nghiem_thu.py")]

# Ghép lúc chạy, không viết nguyên chữ (xem ràng buộc ở docstring).
HOME_CUNG = "/ho" + "me/nguoikhac/duan/soi-ai"
TEN_THU_MUC_CHA = "iee" + "ai2026"

THU_MUC_TOOLS = os.path.join(ROOT, "tools")
TEN_THAM_DO = "_mut_tham_do_g18.py"
DUONG_DAN_THAM_DO = os.path.join(THU_MUC_TOOLS, TEN_THAM_DO)

# Nội dung bốn tệp thăm dò. Mỗi cái vi phạm đúng một tiêu chí, để khi cổng kêu thì biết chắc
# nó kêu vì tiêu chí nào chứ không vì trùng nhiều lỗi một lúc.
NOI_DUNG = {
    "G18a": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tệp THĂM DÒ do mutation_g18.py tạo ra — không phải công cụ thật, sẽ bị xoá ngay."""
import os
ROOT = "%s"
print(os.listdir(ROOT))
''' % HOME_CUNG,

    "G18b": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tệp THĂM DÒ do mutation_g18.py tạo ra — không phải công cụ thật, sẽ bị xoá ngay."""
import os
DU_LIEU = "%s/du_lieu.csv"
print(os.path.exists(DU_LIEU))
''' % TEN_THU_MUC_CHA,

    "G18c": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tệp THĂM DÒ do mutation_g18.py tạo ra — không phải công cụ thật, sẽ bị xoá ngay."""
import sys
print(sys.argv)
for d, _, fs in os.walk("."):
    print(d, len(fs))
''',

    # ĐỐI CHỨNG ÂM: hợp lệ. Nhắc đường dẫn cũ nhưng chỉ trong docstring (kể lại lịch sử lỗi),
    # và import đủ mọi mô-đun nó dùng. G18 phải IM cho tệp này.
    "IM": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tệp THĂM DÒ do mutation_g18.py tạo ra — không phải công cụ thật, sẽ bị xoá ngay.

GHI CHÚ LỊCH SỬ: bản đầu của công cụ này từng ghi cứng
%s
rồi được sửa thành suy gốc từ __file__. Đường dẫn đó được nhắc lại ở đây để giải thích vì sao
có cổng G18, và nó nằm trong DOCSTRING nên không phải vi phạm.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(ROOT, sys.argv)
''' % HOME_CUNG,
}

# Mã tiêu chí con mà mỗi ca phải làm cho kêu.
MA_KY_VONG = {"G18a": "G18a", "G18b": "G18b", "G18c": "G18c", "IM": None}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def chay_cong():
    r = subprocess.run(GATE, cwd=ROOT, capture_output=True, text=True, timeout=900)
    out = r.stdout + r.stderr
    m = re.search(r"KẾT QUẢ: (\d+)/(\d+)", out)
    return r.returncode, (m.group(0) if m else "KHONG DOC DUOC"), out


def xoa_tham_do():
    if os.path.exists(DUONG_DAN_THAM_DO):
        os.remove(DUONG_DAN_THAM_DO)


def ca(ten, noi_dung, ky_vong_keu):
    """Tạo tệp thăm dò, chạy cổng, kiểm kết quả, rồi xoá — luôn xoá kể cả khi lỗi."""
    try:
        with open(DUONG_DAN_THAM_DO, "w", encoding="utf-8") as f:
            f.write(noi_dung)
        rc, ket, out = chay_cong()
        ma = MA_KY_VONG[ten]
        keu = f"[LỖI] {ma}" in out if ma else None
        if ky_vong_keu:
            bat = (rc != 0 and keu)
            tt = ("BẮT ĐƯỢC" if bat else
                  ("IM (KHÔNG RĂNG)" if rc == 0 else "KÊU NHƯNG SAI MÃ"))
        else:
            # Đối chứng âm: cổng phải XANH và G18 không được nêu tên tệp thăm dò.
            bat = (rc == 0 and TEN_THAM_DO not in out)
            tt = ("KHÔNG BẮT OAN (đúng)" if bat else "BẮT OAN — luật miễn trừ docstring hỏng")
        print(f"  [{ten}] {ket}  rc={rc}  ->  {tt}")
        if not bat:
            for l in out.splitlines():
                if "G18" in l or "KẾT QUẢ" in l or TEN_THAM_DO in l:
                    print("       | " + l.strip()[:160])
        return bat
    finally:
        xoa_tham_do()


def main():
    print("=" * 100)
    print("MUTATION TEST CỔNG G18 — ba ca phá đúng thứ cổng khai là canh, một ca đối chứng âm")
    print("=" * 100)
    print(f"  ROOT (suy từ __file__) = {ROOT}")
    print(f"  tệp thăm dò sẽ tạo ở   = {os.path.relpath(DUONG_DAN_THAM_DO, ROOT)}")
    print(f"  ROOT có thật không     = {os.path.isdir(os.path.join(ROOT, 'tools'))}")
    if not os.path.isdir(os.path.join(ROOT, "tools")):
        print("  !!! ROOT sai — không tìm thấy tools/. Kiểm tra số lần dirname.")
        return 2
    if os.path.exists(DUONG_DAN_THAM_DO):
        print("  !!! tệp thăm dò đã tồn tại từ lần chạy trước — xoá nó rồi chạy lại.")
        return 2

    # CA 0 — baseline: cây nguyên trạng phải xanh, nếu không thì mọi ca sau đều vô nghĩa
    # (cổng đỏ sẵn thì "bắt được" không chứng minh gì). Đây là lỗi thứ tự đã xảy ra thật
    # ngày 07/10: sửa tools/ xong chưa sinh lại manifest, hai script mutation thoát ngay ở CA 0.
    rc, ket, out = chay_cong()
    print(f"\n[CA 0] nguyên trạng — cổng phải ĐẠT: {ket}  rc={rc}")
    if rc != 0:
        print("       !!! nguyên trạng đã đỏ: sửa cây trước khi mutation test.")
        for l in out.splitlines():
            if "[LỖI]" in l:
                print("       | " + l.strip()[:160])
        return 1

    ket_luan = []
    print()
    for ten in ("G18a", "G18b", "G18c"):
        ket_luan.append(ca(ten, NOI_DUNG[ten], True))
    ket_luan.append(ca("IM", NOI_DUNG["IM"], False))

    # Xác nhận cuối: tệp thăm dò phải không còn, và cây phải về nguyên trạng.
    con_sot = os.path.exists(DUONG_DAN_THAM_DO)
    print(f"\n[XÁC NHẬN] tệp thăm dò còn sót trên đĩa: {con_sot} (phải False)")
    rc2, ket2, _ = chay_cong()
    print(f"[XÁC NHẬN SAU CÙNG] rc={rc2}  {ket2}   (phải về ĐẠT: hai số bằng nhau)")

    print(f"\nKẾT LUẬN: {sum(ket_luan)}/{len(ket_luan)} ca đúng như kỳ vọng"
          f" (3 ca phá bị G18 bắt + 1 ca đối chứng âm không bị bắt oan)")
    for ten, o in zip(("G18a", "G18b", "G18c", "đối chứng âm"), ket_luan):
        print(f"  {ten}: {'ĐÚNG' if o else 'SAI KỲ VỌNG'}")
    print("=" * 100)
    return 0 if (all(ket_luan) and not con_sot and rc2 == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
