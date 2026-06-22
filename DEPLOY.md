# Deploy Nexus AI — Gratis

## Arsitektur Deployment

```
Vercel (Free)          Render (Free)           Supabase (Free)
┌─────────────┐       ┌──────────────┐       ┌──────────────┐
│  Next.js     │──────▶│  FastAPI      │──────▶│  PostgreSQL   │
│  Frontend    │       │  Backend      │       │  500MB        │
│  nexus-ai    │       │  nexus-api    │       └──────────────┘
│  .vercel.app │       │  onrender.com │              │
└─────────────┘       └──────┬───────┘       ┌──────────────┐
                             │               │  Upstash      │
                             └──────────────▶│  Redis        │
                                              │  Free 100MB   │
                                              └──────────────┘
```

**Biaya per bulan: $0** (semua pakai free tier)

---

## 1. Deploy Frontend ke Vercel

### Cara 1: Auto via GitHub (termudah)

```bash
# Push ke GitHub dulu
cd nexus-ai
git remote add origin https://github.com/NAMA_KAMU/nexus-ai.git
git branch -M main
git push -u origin main
```

- Buka https://vercel.com/new
- Import repository `nexus-ai`
- **JANGAN ubah Root Directory** (biarkan default `/`)
- **JANGAN ubah Framework** (biarkan otomatis)
- Vercel akan otomatis baca `vercel.json` di root project
- Tambah Environment Variables:
  - `NEXT_PUBLIC_API_URL` = `https://nexus-api.onrender.com` (nanti diisi)
  - `NEXT_PUBLIC_WS_URL` = `wss://nexus-api.onrender.com`
- Deploy!

> **⚠️ Penting:** Jangan set Root Directory ke `apps/web` karena `workspace:*` butuh akses ke root monorepo!

### Cara 2: Vercel CLI

```bash
npm install -g vercel
vercel login
cd nexus-ai
vercel --prod
```

---

## 2. Setup Database (Supabase — Gratis)

1. Buka https://supabase.com → Sign up
2. Create project:
   - Name: `nexus-db`
   - Password: simpan
   - Region: Singapore (biar dekat)
3. Tunggu provisioning (~2 menit)
4. Copy `Project Settings > Database > Connection string`:
   ```
   postgresql://postgres:xxxx@xxxx.supabase.co:5432/postgres
   ```
5. Di **SQL Editor**, jalankan migration:
```sql
-- Copy paste isi file: backend/alembic/versions/0001_initial_schema.py
-- Hapus baris "revision" dan "down_revision", jalanin semua CREATE TABLE
```

Atau via terminal:
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
```

---

## 3. Setup Redis (Upstash — Gratis)

1. Buka https://upstash.com → Sign up
2. Create Redis database:
   - Name: `nexus-redis`
   - Region: Singapore
3. Copy `UPSTASH_REDIS_REST_URL` dan `UPSTASH_REDIS_REST_TOKEN`

---

## 4. Deploy Backend ke Render

1. Buka https://render.com → Sign up (pakai GitHub)
2. Klik **New +** → **Web Service**
3. Connect repository `nexus-ai`
4. Set:
   - **Name:** `nexus-api`
   - **Root Directory:** `backend`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free
5. Add Environment Variables:
   - `JWT_SECRET` = (isi random string panjang)
   - `DATABASE_URL` = `postgresql+asyncpg://postgres:password@host.supabase.co:5432/postgres`
   - `REDIS_URL` = `rediss://default:token@upstash.io:6379`
   - `CORS_ORIGINS` = `https://nexus-ai.vercel.app`
   - `ENCRYPTION_KEY` = (isi random 32 karakter hex)
6. Deploy!

**Catatan:** Render free tier akan **sleep** setelah 15 menit gak dipakai. Butuh ~30 detik untuk bangun lagi.

---

## 5. Update Env Vars di Vercel

Setelah backend terdeploy, update di Vercel:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://nexus-api.onrender.com` |
| `NEXT_PUBLIC_WS_URL` | `wss://nexus-api.onrender.com` |

Redeploy Vercel:
```bash
cd apps/web
vercel --prod
```

---

## 6. Selesai!

- Frontend: `https://nexus-ai.vercel.app`
- Backend API: `https://nexus-api.onrender.com`
- API Docs: `https://nexus-api.onrender.com/docs`
- Health Check: `https://nexus-api.onrender.com/health`

---

## Alternatif Gratis Lainnya

| Service | Untuk | Free Tier |
|---------|-------|-----------|
| **Railway** | Backend + DB | $5 credit, cukup buat 1 project |
| **Fly.io** | Backend | 3 VM gratis, perlu kartu kredit |
| **Koyeb** | Backend | 1 service gratis, tidur gak dipake |
| **Neon** | PostgreSQL | 500MB gratis, serverless |
| **TiDB Serverless** | MySQL-compatible | 5GB gratis |
| **Aiven** | Redis/Postgres | $0 (free tier) |
| **Cloudflare Pages** | Frontend | Unlimited, edge network |

---

## Troubleshooting

### CORS Error di Frontend
Pastikan `CORS_ORIGINS` di backend berisi domain Vercel:
```
CORS_ORIGINS=https://nexus-ai.vercel.app
```

### Database Connection Error
Di Supabase:
- Buka **Project Settings > Database > Connection pooling**
- Gunakan port `6543` untuk pooler (lebih stabil di free tier)

### Build Error di Vercel
```bash
# Coba build local dulu
cd apps/web
pnpm build

# Pastikan gak ada error TypeScript
npx tsc --noEmit
```

### Redis Connection Error
Di Render, environment variables harus di-set ulang kalau pindah region.
