#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe vision trên từng model của account VSLLM qua omniproxy.

VÌ SAO: báo "503 Service Unavailable" từ relay không cho biết model nào chết vì
hết quota gói và model nào chết vì lý do khác. Relay trả 503 gộp cho mọi lỗi
upstream, nên phải probe từng model và đọc THÔNG ĐIỆP UPSTREAM thật.

Nguyên tắc đo (theo skill jev-routing-relay-ops):
  - max_tokens phải bằng ngân sách thật của agent, KHÔNG nhỏ. Thinking ẩn bị tính
    vào max_tokens, nên probe max_tokens=16..40 trả content rỗng và mọi model
    trông như mù.
  - Ảnh thử có ĐÁP ÁN BIẾT TRƯỚC: đọc đúng số "47" mới tính là model nhìn được.
  - Phân loại rõ: harness chết (không gửi được request) ≠ model chết (có HTTP
    status + thông điệp upstream).

Không in credential. Key đọc từ config omniproxy lúc chạy.
"""
import base64
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request

CFG = os.path.expanduser("~/.omniproxy-user/data/config.json")
RELAY = "http://127.0.0.1:20131/v1/chat/completions"
MAX_TOKENS = 16384          # ngân sách thật, không phải 16

MODELS = [
    "deepseek-v4.1-flash", "deepseek-v4-pro", "deepseek-v4.1-flash-官方",
    "qwen3.7-plus", "kimi-k3", "glm-5.3", "glm-5.3-flash",
    "minimax-m3", "minimax-m3.1-flash", "gemini-3.8-flash-api",
    "gpt-5.6-sol", "grok-4.7", "glm-5.3-flash-max", "glm-5.3-anthropic",
]


def relay_key():
    d = json.load(open(CFG))
    keys = [k for k in d.get("apiKeys", []) if k.get("enabled")]
    if not keys:
        raise SystemExit("không có apiKey đang bật trong config omniproxy")
    # ưu tiên key tên 'claude' (key chính đang dùng)
    for k in keys:
        if k.get("name", "").lower() == "claude":
            return k["key"]
    return keys[0]["key"]


def make_test_image():
    """Vẽ ảnh có số 47 cỡ lớn, trắng đen, đáp án biết trước."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return None
    img = Image.new("RGB", (420, 220), "white")
    dr = ImageDraw.Draw(img)
    font = None
    for path in ("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                 "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"):
        if os.path.exists(path):
            font = ImageFont.truetype(path, 150)
            break
    if font is None:
        font = ImageFont.load_default()
    dr.text((110, 25), "47", fill="black", font=font)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def probe(model, key, b64):
    body = {
        "model": model,
        "max_tokens": MAX_TOKENS,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Ảnh này có số mấy? Chỉ trả lời đúng con số."},
                {"type": "image_url",
                 "image_url": {"url": f"data:image/png;base64,{b64}"}},
            ],
        }],
    }
    req = urllib.request.Request(
        RELAY,
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read().decode())
        dt = time.time() - t0
        content = (data.get("choices", [{}])[0].get("message", {}).get("content") or "").strip()
        usage = data.get("usage", {})
        ok = "47" in content
        return {
            "model": model, "status": 200, "ok": ok,
            "content": content[:60], "latency_s": round(dt, 1),
            "completion_tokens": usage.get("completion_tokens"),
            "truncated": usage.get("completion_tokens") == MAX_TOKENS and not content,
        }
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode(errors="replace")[:200]
        return {"model": model, "status": e.code, "ok": False,
                "error": body_txt, "latency_s": round(time.time() - t0, 1)}
    except Exception as e:
        return {"model": model, "status": "harness", "ok": False,
                "error": f"{type(e).__name__}: {e}", "latency_s": round(time.time() - t0, 1)}


def main():
    key = relay_key()
    b64 = make_test_image()
    if not b64:
        print("LỖI: không có Pillow để vẽ ảnh thử", file=sys.stderr)
        return 2
    print(f"Probe {len(MODELS)} model · max_tokens={MAX_TOKENS} · đáp án '47'\n")
    rows = []
    for m in MODELS:
        r = probe(m, key, b64)
        rows.append(r)
        tag = "ĐỌC ĐÚNG" if r.get("ok") else ("LỖI " + str(r.get("status")))
        note = r.get("content") or r.get("error", "")
        print(f"  {tag:10s} {m:32s} {r.get('latency_s',0):6.1f}s  {note[:70]}")
    good = [r for r in rows if r.get("ok")]
    print(f"\n{len(good)}/{len(rows)} model đọc đúng số 47")
    if good:
        good.sort(key=lambda r: r["latency_s"])
        print(f"Nhanh nhất: {good[0]['model']} ({good[0]['latency_s']}s)")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..", "out", "vision_probe.json"), "w") as fh:
        json.dump({"checked_at": time.strftime("%Y-%m-%d %H:%M:%S"), "rows": rows}, fh,
                  ensure_ascii=False, indent=2)
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
