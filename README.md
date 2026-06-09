# GOGOLEE 機器維修保養系統

Django 後台管理系統，用於管理咖啡機器的客戶、訂單、電路板、維修保養紀錄與品質測試。

## 技術架構

| 項目 | 技術 |
|------|------|
| 後端框架 | Django 5.2 + Django REST Framework |
| 資料庫 | PostgreSQL + PostGIS（地理座標支援） |
| 靜態檔案 | WhiteNoise |
| 媒體檔案 | Google Cloud Storage（生產）/ 本地 volume（開發） |
| 部署 | Google Cloud Run |
| 容器化 | Docker + Docker Compose |

## 本地開發

### 前置需求

- Docker & Docker Compose
- Python 3.10+（若不用 Docker 直接跑）

### 快速啟動

```bash
# 1. 複製 env 範本
cp .env.example .env
# 編輯 .env，填入 DB_HOST、DB_USER、DB_PASSWORD 等

# 2. 啟動（連 Neon DB）
docker compose up

# 3. 建立 admin 帳號（第一次）
docker compose exec web python manage.py createsuperuser

# 4. 開啟後台
# http://localhost:8000/admin/
```

### 環境變數說明

| 變數 | 說明 | 預設值 |
|------|------|--------|
| `SECRET_KEY` | Django 金鑰 | 必填 |
| `DEBUG` | 開啟 debug mode | `False` |
| `ALLOWED_HOSTS` | 允許的 host，逗號分隔 | `localhost,127.0.0.1` |
| `DB_NAME` | 資料庫名稱 | `coffeedb` |
| `DB_USER` | 資料庫帳號 | 必填 |
| `DB_PASSWORD` | 資料庫密碼 | 必填 |
| `DB_HOST` | 資料庫 host | `localhost` |
| `DB_PORT` | 資料庫 port | `5432` |
| `DB_SSLMODE` | SSL 模式（Neon 用 `require`） | `disable` |
| `GCS_BUCKET_NAME` | GCS bucket 名稱（留空用本地） | 空 |
| `CSRF_TRUSTED_ORIGINS` | 信任的 HTTPS 來源，逗號分隔 | 空 |

## 資料模型

```
Customer（客戶）
  └── Contact（聯絡人）
  └── Order（訂單）
        └── Machine（機器）

Circuit（電路板）
  └── CircuitUpgrade（電路板升級紀錄）
  └── Machine（機器）
        ├── TemperatureSensor（溫度感測器）
        ├── MachineComponent（機器組件）
        └── Maintain（維護紀錄）
              └── MissionMaintain（維修任務）
                    └── Mission（維修項目）

QualityTest（品質測試）
```

## 部署（Google Cloud Run）

### 更版流程

```bash
# 1. Build + push image
docker build -t us-east1-docker.pkg.dev/coherent-ranger-400313/coffeedb/web:latest .
docker push us-east1-docker.pkg.dev/coherent-ranger-400313/coffeedb/web:latest

# 2. 跑 migration（有新 migration 時才需要）
gcloud run jobs execute coffeedb-migrate --region us-east1 --wait

# 3. 部署
gcloud run deploy coffeedb \
  --image us-east1-docker.pkg.dev/coherent-ranger-400313/coffeedb/web:latest \
  --region us-east1
```

### 生產環境設定

- **資料庫**：Neon Postgres（`DB_SSLMODE=require`）
- **媒體檔案**：GCS bucket `coffeedb-media`，需登入 Django admin 才能下載
- **自訂網域**：`gogolee.ap-duo.com`（透過 Cloudflare Worker 代理到 Cloud Run）
- **帳號鎖定**：登入失敗 5 次後鎖定 1 小時（django-axes）

## 安全性

- 登入失敗 5 次鎖定帳號 1 小時
- 媒體檔案需登入後才能存取
- 生產環境強制 HTTPS Cookie
- 機密資訊透過環境變數載入，不進版本控制
