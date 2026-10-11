/* TEST THẬT cho js/vaitro_connguoi.js — chạy bằng node, không cần trình duyệt.
 *
 * Vì sao phải test oracle chứ không chỉ `node --check`: hoạt động này là BẰNG CHỨNG cho một
 * yêu cầu cần đạt trong hồ sơ nộp. Nếu oracle chấm sai, giáo viên sẽ ghi điểm sai cho học
 * sinh thật — lỗi nặng hơn nhiều so với một nút không hiện.
 *
 * Bốn nhóm ca phải qua:
 *   1. đáp án đúng  -> dung:true  và điểm 1
 *   2. đáp án sai   -> dung:false và điểm 0, kèm đáp án đúng để báo cáo
 *   3. id không tồn tại -> null (KHÔNG được coi là "sai": im lặng ghi 0 là đổ lỗi học sinh
 *      vì lỗi của mã)
 *   4. phương án không hợp lệ -> null (chống bấm bừa / chống payload lạ lọt vào log)
 *   5. tính toàn vẹn dữ liệu: mỗi câu đúng 1 đáp án, đáp án phải nằm trong danh sách phương
 *      án (nếu không thì không ô nào được tô xanh và học sinh tưởng mình sai dù chọn đúng)
 */
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const S = "/home/hitokiri/ieeai2026/soi-ai";

/* Nạp tệp dữ liệu trong một ngữ cảnh giả lập có `window`. */
const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(S, "js/vaitro_connguoi.js"), "utf8"), sandbox,
  { filename: "js/vaitro_connguoi.js" });
const M = sandbox.window.MX_VAI_TRO;

assert.ok(M, "MX_VAI_TRO phải được export");
let pass = 0, fail = 0;
function ktra(ten, fn) {
  try { fn(); pass++; console.log("  [OK ] " + ten); }
  catch (e) { fail++; console.log("  [LỖI] " + ten + "\n        " + e.message); }
}

console.log("=== 1. cấu trúc dữ liệu ===");
ktra("có đúng 3 câu", () => assert.strictEqual(M.CAU.length, 3));
ktra("soCau khớp độ dài", () => assert.strictEqual(M.soCau, M.CAU.length));
ktra("mọi câu khai đúng mã 10.A1.1", () => {
  M.CAU.forEach(c => assert.strictEqual(c.yccd, "10.A1.1", c.id + " khai " + c.yccd));
});
ktra("3 câu phủ đúng 3 vế của động từ (không trùng)", () => {
  /* So bằng CHUỖI, không dùng deepStrictEqual với mảng: M.CAU được tạo trong ngữ cảnh vm
   * (khác realm), nên prototype của mảng không khớp với mảng ở realm của test và
   * deepStrictEqual báo "not reference-equal" dù nội dung giống hệt. Đó là lỗi của test,
   * không phải của sản phẩm. */
  const vai = M.CAU.map(c => c.vai).slice().sort();
  const mongMuon = ["SỬ DỤNG", "TÙY CHỈNH", "VẬN HÀNH"].sort();
  assert.strictEqual(JSON.stringify(vai), JSON.stringify(mongMuon),
    "3 vế của động từ không khớp: " + JSON.stringify(vai));
  assert.strictEqual(new Set(M.cacVai).size, M.cacVai.length, "vai bị trùng");
});
ktra("mọi câu có đủ 4 trường bắt buộc cho báo cáo (mach/unesco/yccd/vai)", () => {
  M.CAU.forEach(c => ["mach", "unesco", "yccd", "vai", "cauHoi", "giaiThich", "dapAn"]
    .forEach(k => assert.ok(c[k], c.id + " thiếu " + k)));
});

console.log("\n=== 2. tính toàn vẹn đáp án (lỗi ở đây = học sinh chọn đúng vẫn bị báo sai) ===");
M.CAU.forEach(c => {
  ktra(c.id + ": đúng 1 đáp án và nó nằm trong danh sách phương án", () => {
    const ids = c.luaChon.map(l => l.id);
    assert.strictEqual(new Set(ids).size, ids.length, "id phương án trùng nhau");
    assert.ok(ids.includes(c.dapAn),
      "đáp án khai '" + c.dapAn + "' không có trong phương án " + JSON.stringify(ids));
  });
  ktra(c.id + ": có đúng 4 phương án, chữ đủ dài để đọc", () => {
    assert.strictEqual(c.luaChon.length, 4);
    c.luaChon.forEach(l => assert.ok(l.text.length > 25, "phương án " + l.id + " quá ngắn: " + l.text));
  });
});

console.log("\n=== 2b. CHỐNG CUE 'chọn phương án dài nhất' (cổng G12c đo cue này trên toàn ngân hàng) ===");
/* Luật: mỗi câu phải có ÍT NHẤT một phương án SAI dài hơn đáp án đúng. Nếu đáp án đúng luôn là
 * phương án dài nhất thì học sinh bấm câu dài là ăn điểm mà không cần hiểu bài — điểm đó không
 * chứng minh được yêu cầu cần đạt nào. Ba câu đầu tiên của bộ này đã dính đúng cue đó và đẩy tỉ
 * lệ toàn ngân hàng từ 82.9% lên 84.2%; ca test này để nó không quay lại. */
M.CAU.forEach(c => {
  ktra(c.id + ": đáp án KHÔNG phải phương án dài nhất (có nhiễu sai dài hơn)", () => {
    const daiNhat = Math.max(...c.luaChon.map(l => l.text.length));
    const dap = c.luaChon.find(l => l.id === c.dapAn);
    assert.ok(dap, "không tìm thấy phương án mang id đáp án '" + c.dapAn + "'");
    assert.ok(dap.text.length < daiNhat,
      "đáp án '" + c.dapAn + "' dài " + dap.text.length + " ký tự = dài nhất (" + daiNhat
      + ") -> học sinh bấm câu dài là ăn điểm. Hãy kéo dài MỘT phương án SAI, "
      + "đừng cắt ngắn đáp án đúng.");
    const nhieuDai = c.luaChon.filter(l => l.id !== c.dapAn && l.text.length > dap.text.length);
    assert.ok(nhieuDai.length >= 1, "không có nhiễu sai nào dài hơn đáp án");
  });
});
ktra("không câu nào có HAI phương án dài bằng nhau ở mức dài nhất (tránh may rủi khi xáo)", () => {
  M.CAU.forEach(c => {
    const ds = c.luaChon.map(l => l.text.length);
    const daiNhat = Math.max(...ds);
    assert.strictEqual(ds.filter(n => n === daiNhat).length, 1,
      c.id + " có nhiều phương án cùng dài nhất (" + daiNhat + ")");
  });
});

console.log("\n=== 3. oracle: chọn ĐÚNG ===");
M.CAU.forEach(c => {
  ktra(c.id + " (" + c.vai + ") chọn đúng -> dung:true, diem 1", () => {
    const r = M.cham(c.id, c.dapAn);
    assert.ok(r, "cham trả null với ca hợp lệ");
    assert.strictEqual(r.dung, true);
    assert.strictEqual(r.diem, 1);
    assert.strictEqual(r.dapAn, c.dapAn);
    assert.strictEqual(r.chon, c.dapAn);
    assert.strictEqual(r.yccd, "10.A1.1", "log phải kèm mã YCCĐ");
  });
});

console.log("\n=== 4. oracle: chọn SAI (mỗi phương án sai một lần) ===");
M.CAU.forEach(c => {
  c.luaChon.filter(l => l.id !== c.dapAn).forEach(l => {
    ktra(c.id + " chọn '" + l.id + "' -> dung:false, diem 0, vẫn báo đáp án đúng", () => {
      const r = M.cham(c.id, l.id);
      assert.ok(r, "cham trả null với phương án hợp lệ");
      assert.strictEqual(r.dung, false);
      assert.strictEqual(r.diem, 0);
      assert.strictEqual(r.chon, l.id);
      assert.strictEqual(r.dapAn, c.dapAn, "phải trả đáp án đúng để GV chấm lại được");
    });
  });
});

console.log("\n=== 5. ca biên: phải trả NULL, không được coi là 'sai' ===");
ktra("id không tồn tại -> null", () => assert.strictEqual(M.cham("khong-co", "a"), null));
ktra("id rỗng -> null", () => assert.strictEqual(M.cham("", "a"), null));
ktra("id null -> null", () => assert.strictEqual(M.cham(null, "a"), null));
ktra("phương án không hợp lệ -> null", () => {
  const c = M.CAU[0];
  assert.strictEqual(M.cham(c.id, "zzz"), null);
});
ktra("phương án rỗng -> null", () => assert.strictEqual(M.cham(M.CAU[0].id, ""), null));
ktra("thiếu tham số -> null", () => assert.strictEqual(M.cham(M.CAU[0].id), null));
ktra("payload tiêm HTML không được nhận là hợp lệ -> null", () => {
  assert.strictEqual(M.cham(M.CAU[0].id, '<img src=x onerror=alert(1)>'), null);
});

console.log("\n=== 6. tim() và tính bất biến ===");
ktra("tim() trả đúng câu", () => assert.strictEqual(M.tim("a11-02").vai, "VẬN HÀNH"));
ktra("tim() id lạ -> null", () => assert.strictEqual(M.tim("a11-99"), null));
ktra("cham() không làm biến đổi dữ liệu gốc", () => {
  const truoc = JSON.stringify(M.CAU);
  M.CAU.forEach(c => { M.cham(c.id, c.dapAn); M.cham(c.id, "zzz"); });
  assert.strictEqual(JSON.stringify(M.CAU), truoc, "cham() đã sửa dữ liệu câu hỏi");
});
ktra("chấm cùng ca 2 lần cho kết quả giống nhau (tất định)", () => {
  const c = M.CAU[1];
  assert.deepStrictEqual(M.cham(c.id, c.dapAn), M.cham(c.id, c.dapAn));
});

console.log("\n=========================================");
console.log("KẾT QUẢ: " + pass + " đạt · " + fail + " lỗi");
console.log("=========================================");
process.exit(fail ? 1 : 0);
