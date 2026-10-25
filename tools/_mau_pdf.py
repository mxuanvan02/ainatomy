#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sinh PDF mẫu tối giản bằng Python thuần, để tự kiểm bộ đo bố cục.

VÌ SAO TỰ VIẾT THAY VÌ DÙNG ps2pdf:
  Máy không có ps2pdf. Nếu self-test cứ bị skip thì bộ đo KHÔNG BAO GIỜ được thử —
  đó chính là kiểu "gate mù" mà dự án này đã dính lỗi một lần. Bộ đo phải tự
  sinh được đầu vào để chứng minh là nó bắt đúng và không báo bừa.
"""
import os


def _pdf_escape(text):
    return text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def make_pdf(path, lines, page_w=612, page_h=792):
    """lines: list of (x, y, size, text). Tọa độ theo PDF (origin bottom-left)."""
    parts = []
    for x, y, size, text in lines:
        parts.append(
            f"BT /F1 {size} Tf {x} {y} Td ({_pdf_escape(text)}) Tj ET"
        )
    stream = "\n".join(parts).encode("latin-1", "replace")

    objs = []
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objs.append(
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {page_w} {page_h}] "
        f"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>".encode()
    )
    objs.append(
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream"
    )
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")

    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + body + b"\nendobj\n"

    xref_pos = len(out)
    n = len(objs) + 1
    out += f"xref\n0 {n}\n".encode()
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (
        f"trailer\n<< /Size {n} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode()
    )

    with open(path, "wb") as fh:
        fh.write(bytes(out))
    return path
