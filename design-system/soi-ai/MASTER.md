# Design System Master File

> **LOGIC:** When building a specific page, first check `design-system/pages/[page-name].md`.
> If that file exists, its rules **override** this Master file.
> If not, strictly follow the rules below.

---

**Project:** SOI AI
**Generated:** 2026-10-04 13:29:12
**Category:** AI/Chatbot Platform

---

## Global Rules

### Color Palette

| Role | Hex | CSS Variable |
|------|-----|--------------|
| Primary | `#7C3AED` | `--color-primary` |
| On Primary | `#FFFFFF` | `--color-on-primary` |
| Secondary | `#A78BFA` | `--color-secondary` |
| On Secondary | `#0F172A` | `--color-on-secondary` |
| Accent/CTA | `#0891B2` | `--color-accent` |
| On Accent/CTA | `#000000` | `--color-on-accent` |
| Background | `#FAF5FF` | `--color-background` |
| Foreground | `#1E1B4B` | `--color-foreground` |
| Card | `#FFFFFF` | `--color-card` |
| Card Foreground | `#1E1B4B` | `--color-card-foreground` |
| Muted | `#ECEEF9` | `--color-muted` |
| Muted Foreground | `#475569` | `--color-muted-foreground` |
| Border | `#DDD6FE` | `--color-border` |
| Destructive | `#DC2626` | `--color-destructive` |
| On Destructive | `#FFFFFF` | `--color-on-destructive` |
| Ring | `#7C3AED` | `--color-ring` |

**Color Notes:** AI purple + cyan interactions [Accent adjusted from #06B6D4]

### Typography

- **Heading Font:** Inter
- **Body Font:** Inter
- **Mood:** flat, clean, system, bold, geometric, cross-platform, icon, poster, minimal, functional, responsive
- **Google Fonts:** [Inter + Inter](https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap)

**CSS Import:**
```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
```

### Spacing Variables

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | `4px` / `0.25rem` | Tight gaps |
| `--space-sm` | `8px` / `0.5rem` | Icon gaps, inline spacing |
| `--space-md` | `16px` / `1rem` | Standard padding |
| `--space-lg` | `24px` / `1.5rem` | Section padding |
| `--space-xl` | `32px` / `2rem` | Large gaps |
| `--space-2xl` | `48px` / `3rem` | Section margins |
| `--space-3xl` | `64px` / `4rem` | Hero padding |

### Shadow Depths

| Level | Value | Usage |
|-------|-------|-------|
| `--shadow-sm` | `0 1px 2px rgba(0,0,0,0.05)` | Subtle lift |
| `--shadow-md` | `0 4px 6px rgba(0,0,0,0.1)` | Cards, buttons |
| `--shadow-lg` | `0 10px 15px rgba(0,0,0,0.1)` | Modals, dropdowns |
| `--shadow-xl` | `0 20px 25px rgba(0,0,0,0.15)` | Hero images, featured cards |

---

### 3D palette (bắt buộc — nền cảnh 3D là SÁNG)

Nền cảnh three.js: `scene.background = #F8FAFC`. Màu cũ kế thừa từ giao diện tối
không dùng được; bảng dưới đây đã đo theo WCAG 1.4.11 (đồ hoạ cần >= 3.0:1).

| Vai trò trong cảnh 3D | Hex | Tỉ lệ trên #F8FAFC | Tỉ lệ trên #FFFFFF |
|---|---|---|---|
| Ảnh BAN NGÀY | `#B45309` | 4.80:1 | 5.02:1 |
| Ảnh BAN ĐÊM | `#1D4ED8` | 6.41:1 | 6.70:1 |
| AI đoán SAI | `#B91C1C` | 6.18:1 | 6.47:1 |
| AI đoán ĐÚNG | `#15803D` | 4.79:1 | 5.02:1 |
| Mặt phẳng quyết định | `#EF4444` | 3.60:1 | 3.76:1 |
| Lưới toạ độ (chỉ trang trí) | `#CBD5E1` | 1.48:1 | — |

Lưới toạ độ dưới ngưỡng nên **không được dùng để mang thông tin**; nó chỉ là nền.
Màu bị loại vì không đạt: `#FFD43B` (1.43:1), `#4DABF7` (2.48:1), `#FF6B6B` (2.78:1).

---

## Component Specs

### Buttons

> **ĐIỀU CHỈNH THEO RÀNG BUỘC SẢN PHẨM (04/10/2026).** Ba điểm của MASTER.md gốc
> không áp dụng được nguyên trạng, đã đo/kiểm chứng trước khi sửa:
> 1. **Nền nút chính `#0891B2` + chữ trắng chỉ đạt 3.68:1** (dưới 4.5:1 cho chữ thường).
>    Tương phản WCAG có tính đối xứng, nên con số 5.70:1 trong bảng gốc thuộc về cặp
>    chữ ĐEN trên nền đó và không dùng được cho nút chữ trắng. → Dùng **`#0E7490`** (5.36:1).
>    `#0891B2` chỉ còn dùng cho chữ cỡ lớn và thành phần đồ hoạ (đạt ngưỡng 3.0:1).
> 2. **Không nạp Inter từ Google Fonts.** Phép thử tải trả về CSS 916 byte, 0 subset tiếng Việt,
>    và gọi mạng trái ràng buộc chạy ngoại tuyến. → Dùng phông hệ thống:
>    `Inter, "Segoe UI", system-ui, -apple-system, "DejaVu Sans", Arial, sans-serif`.
> 3. **Màu đồ hoạ 3D phải đổi khi nền sang sáng.** Đo WCAG: `#FFD43B` = 1.43:1,
>    `#4DABF7` = 2.48:1, `#FF6B6B` = 2.78:1 — đều dưới 3.0:1. → Dùng bảng màu ở
>    "3D palette" bên dưới (mọi cặp >= 3.0:1).

```css
/* Primary Button — nền đã đổi từ #0891B2 sang #0E7490 vì tương phản chữ trắng */
.btn-primary {
  background: #0E7490;   /* 5.36:1 với chữ trắng */
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 200ms ease;
  cursor: pointer;
}

.btn-primary:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

/* Secondary Button */
.btn-secondary {
  background: transparent;
  color: #7C3AED;
  border: 2px solid #7C3AED;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 200ms ease;
  cursor: pointer;
}
```

### Cards

```css
.card {
  background: #FAF5FF;
  border-radius: 12px;
  padding: 24px;
  box-shadow: var(--shadow-md);
  transition: all 200ms ease;
  cursor: pointer;
}

.card:hover {
  box-shadow: var(--shadow-lg);
  transform: translateY(-2px);
}
```

### Inputs

```css
.input {
  padding: 12px 16px;
  border: 1px solid #E2E8F0;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 200ms ease;
}

.input:focus {
  border-color: #7C3AED;
  outline: none;
  box-shadow: 0 0 0 3px #7C3AED20;
}
```

### Modals

```css
.modal-overlay {
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.modal {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: var(--shadow-xl);
  max-width: 500px;
  width: 90%;
}
```

---

## Style Guidelines

**Style:** AI-Native UI

**Keywords:** Chatbot, conversational, voice, assistant, agentic, ambient, minimal chrome, streaming text, AI interactions

**Best For:** AI products, chatbots, voice assistants, copilots, AI-powered tools, conversational interfaces

**Key Effects:** Typing indicators (3-dot pulse), streaming text animations, pulse animations, context cards, smooth reveals

### Page Pattern

**Pattern Name:** Product Demo + Features

- **Conversion Strategy:** Use an interactive demo only when it explains value better than static media. Provide captions, transcript, visible play/pause controls, and a non-video fallback; do not autoplay under reduced motion. Pause media when offscreen or hidden and keep the final product state available as static content.
- **CTA Placement:** Video center + CTA right/bottom
- **Section Order:** Hero > Product video/mockup (center) > Feature breakdown per section > Comparison (optional) > CTA

---

## Anti-Patterns (Do NOT Use)

- ❌ Heavy chrome
- ❌ Slow response feedback

### Additional Forbidden Patterns

- ❌ **Emojis as icons** — Use SVG icons (Heroicons, Lucide, Simple Icons)
- ❌ **Missing cursor:pointer** — All clickable elements must have cursor:pointer
- ❌ **Layout-shifting hovers** — Avoid scale transforms that shift layout
- ❌ **Low contrast text** — Maintain 4.5:1 minimum contrast ratio
- ❌ **Instant state changes** — Always use transitions (150-300ms)
- ❌ **Invisible focus states** — Focus states must be visible for a11y

---

## Pre-Delivery Checklist

Before delivering any UI code, verify:

- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set (Heroicons/Lucide)
- [ ] `cursor-pointer` on all clickable elements
- [ ] Hover states with smooth transitions (150-300ms)
- [ ] Light mode: text contrast 4.5:1 minimum
- [ ] Focus states visible for keyboard navigation
- [ ] `prefers-reduced-motion` respected
- [ ] Responsive: 375px, 768px, 1024px, 1440px
- [ ] No content hidden behind fixed navbars
- [ ] No horizontal scroll on mobile
