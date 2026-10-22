# Deploy AInatomy lên Cloudflare Pages

## Cách 1: Deploy qua Dashboard (Đơn giản nhất, không cần token)

1. **Truy cập Cloudflare Dashboard**
   - Vào: https://dash.cloudflare.com/
   - Đăng nhập tài khoản đã tạo

2. **Tạo project Pages**
   - Click "Workers & Pages" ở menu trái
   - Click "Create application"
   - Chọn tab "Pages"
   - Click "Connect to Git"

3. **Kết nối GitHub**
   - Click "GitHub"
   - Chọn repo `mxuanvan02/ainatomy`
   - Click "Begin setup"

4. **Cấu hình build**
   - Project name: `ainatomy`
   - Production branch: `main`
   - Framework preset: "None"
   - Build command: (để trống)
   - Build output directory: `soi-ai`
   - Click "Save and Deploy"

5. **Chờ deploy xong** (~30 giây)
   - URL sẽ là: `https://ainatomy.pages.dev`

6. **Mỗi lần push code lên GitHub, Cloudflare tự động deploy lại**

---

## Cách 2: Deploy qua Wrangler CLI (Cần API token)

### Bước 1: Tạo API Token

1. Vào: https://dash.cloudflare.com/profile/api-tokens
2. Click "Create Token"
3. Chọn template "Edit Cloudflare Workers"
4. Đặt tên: "AInatomy Deploy"
5. Permissions:
   - Account: Cloudflare Pages: Edit
   - Zone: (chọn zone nếu cần custom domain)
6. Click "Continue to summary" → "Create Token"
7. **Copy token** (chỉ hiện 1 lần!)

### Bước 2: Cài Wrangler CLI

```bash
npm install -g wrangler
```

### Bước 3: Đăng nhập Wrangler

```bash
cd /home/hitokiri/ieeai2026/soi-ai
wrangler login
```

Hoặc dùng token:

```bash
export CLOUDFLARE_API_TOKEN="your-token-here"
```

### Bước 4: Deploy

```bash
wrangler pages deploy . --project-name=ainatomy
```

---

## Kiểm tra

Sau khi deploy, truy cập:
- **Production**: https://ainatomy.pages.dev
- **Preview** (mỗi PR): https://<commit-hash>.ainatomy.pages.dev

---

## Custom Domain (tùy chọn)

Nếu muốn dùng domain riêng (ví dụ: ainatomy.vn):

1. Vào Cloudflare Dashboard → Workers & Pages → ainatomy
2. Tab "Custom domains"
3. Click "Set up a custom domain"
4. Nhập domain và làm theo hướng dẫn

---

## Troubleshooting

### Lỗi "ERR_NAME_NOT_RESOLVED"
- Đợi 1-2 phút sau khi deploy
- Kiểm tra URL đúng: `https://ainatomy.pages.dev` (không phải `ainatomy.pages.dev`)

### Lỗi "Build failed"
- Kiểm tra build output directory đúng: `soi-ai`
- Kiểm tra repo có file `index.html` trong thư mục `soi-ai/`

### Muốn deploy lại thủ công
```bash
wrangler pages deploy . --project-name=ainatomy
```
