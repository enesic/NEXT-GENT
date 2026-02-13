# 🚀 AWS Backend - Hızlı Başlangıç

## ✅ Hazır Olan

- ✅ Frontend Vercel'de: https://nextgent.co
- ✅ Veritabanı export edildi: `backups\nextgent_backup_20260212_110141.dump`
- ✅ Docker image hazır: `backend/Dockerfile`
- ✅ Tüm yapılandırmalar tamam

## 🎯 3 Adımda AWS Deployment

### Adım 1: AWS Hesabı ve CLI (10 dakika)

**1.1. AWS Hesabı:**
- https://aws.amazon.com → **Create AWS Account**
- Email, şifre, kredi kartı
- Free tier aktif (12 ay bedava!)

**1.2. AWS CLI Kurulumu:**
```powershell
# Chocolatey ile
choco install awscli

# Veya MSI Installer
# https://awscli.amazonaws.com/AWSCLIV2.msi
```

**1.3. AWS Yapılandırma:**
```bash
aws configure

# Sorulan bilgileri girin:
AWS Access Key ID: [IAM'den alın]
AWS Secret Access Key: [IAM'den alın]
Default region: eu-central-1
Default output format: json
```

**IAM Access Key Alma:**
1. AWS Console → **IAM** → **Users** → **Create user**
2. User name: `nextgent-deployer`
3. Policies: `AWSAppRunnerFullAccess`, `AmazonEC2ContainerRegistryPowerUser`
4. **Security credentials** → **Create access key** → CLI seçin
5. Access Key ID ve Secret Key'i kaydedin

### Adım 2: Docker Image'ı ECR'a Yükle (10 dakika)

**2.1. Account ID'nizi alın:**
```bash
aws sts get-caller-identity --query Account --output text
```

**2.2. ECR Repository:**
```bash
# Repository oluştur
aws ecr create-repository --repository-name nextgent-backend --region eu-central-1
```

**2.3. ECR Login:**
```bash
# Account ID'nizi değiştirin
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com
```

**2.4. Image Build ve Push:**
```bash
cd backend

# Build
docker build -t nextgent-backend .

# Tag (YOUR_ACCOUNT_ID değiştirin!)
docker tag nextgent-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest

# Push
docker push YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest
```

### Adım 3: App Runner Service (15 dakika)

**3.1. AWS Console:**
- https://console.aws.amazon.com → **App Runner**
- **Create service**

**3.2. Source Configuration:**
- Source: **Container registry**
- Provider: **Amazon ECR**
- Image URI: `YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest`
- Deployment: **Manual**
- Create new service role

**3.3. Service Settings:**
- Service name: `nextgent-backend`
- CPU: **1 vCPU**
- Memory: **2 GB**
- Port: **8000**

**3.4. Environment Variables:**

```env
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# GÜVENLİK - YENİ OLUŞTUR!
SECRET_KEY=<python -c "import secrets; print(secrets.token_urlsafe(32))">
ENCRYPTION_KEY=<python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">

# Vercel Postgres (Vercel dashboard'dan kopyalayın)
POSTGRES_URL=postgres://default:xxx@ep-xxx.vercel-storage.com:5432/verceldb
POSTGRES_SERVER=ep-xxx.vercel-storage.com
POSTGRES_USER=default
POSTGRES_PASSWORD=xxx
POSTGRES_DB=verceldb
POSTGRES_PORT=5432

# Vercel KV (Vercel dashboard'dan kopyalayın)
REDIS_URL=redis://default:xxx@xxx.vercel-storage.com:6379
REDIS_HOST=xxx.vercel-storage.com
REDIS_PORT=6379
REDIS_PASSWORD=xxx

# CORS
BACKEND_CORS_ORIGINS=https://next-gent-bbxs21jcs-enesics-projects.vercel.app,https://nextgent.co

# OpenAI (opsiyonel)
OPENAI_API_KEY=sk-proj-your-key
AI_MODEL=gpt-4o-mini
AI_ENABLED=true
```

**3.5. Health Check:**
- Path: `/api/v1/health`
- Interval: **20 seconds**
- Timeout: **5 seconds**

**3.6. Auto Scaling:**
- Min: **1**
- Max: **5**

**3.7. Deploy:**
- **Create & deploy** butonuna tıklayın
- 3-5 dakika bekleyin
- Service URL'yi kopyalayın: `https://xxxxx.eu-central-1.awsapprunner.com`

### Adım 4: Frontend Güncelle ve Test (5 dakika)

**4.1. Environment Variable Güncelle:**

`frontend\.env.production` dosyasını açın:
```env
VITE_API_BASE_URL=https://xxxxx.eu-central-1.awsapprunner.com/api/v1
```

**4.2. Vercel'e Yeniden Deploy:**
```bash
vercel --prod --yes
```

**4.3. Test:**

1. Backend health check:
   ```bash
   curl https://xxxxx.eu-central-1.awsapprunner.com/api/v1/health
   ```

2. Frontend: https://nextgent.co
3. Login test:
   - Beauty: `BEA-000001` / PIN: `1234`
   - Hotel: `HOS-000001` / PIN: `1234`
   - Medical: `MED-000001` / PIN: `1234`

## ✅ Tamamlandı!

Sisteminiz artık tamamen AWS üzerinde çalışıyor:

- ✅ Frontend: Vercel (https://nextgent.co)
- ✅ Backend: AWS App Runner
- ✅ Database: Vercel Postgres
- ✅ Redis: Vercel KV

## 📊 Maliyet

| Servis | Aylık |
|--------|-------|
| Vercel (Frontend) | $0 |
| Vercel Postgres | $5-10 |
| Vercel KV | $0 |
| AWS App Runner | $25-50 |
| **Toplam** | **$30-70** |

**Free Tier:** İlk 12 ay AWS free tier ile daha ucuz!

## 🔧 Yararlı Komutlar

```bash
# Service listele
aws apprunner list-services --region eu-central-1

# Service durumu
aws apprunner describe-service --service-arn YOUR_ARN --region eu-central-1

# Logs
aws logs tail /aws/apprunner/nextgent-backend/xxxxx/application --follow

# Yeniden deploy
aws apprunner start-deployment --service-arn YOUR_ARN --region eu-central-1
```

## 🆘 Sorun Giderme

**"AccessDenied" Hatası:**
- IAM policy'leri kontrol edin
- `AWSAppRunnerFullAccess` ve `ECRPowerUser` gerekli

**Image Push Edilemiyor:**
- ECR login tekrar yapın
- Account ID doğru mu kontrol edin

**Service Başlamıyor:**
- CloudWatch logs kontrol edin
- Environment variables doğru mu
- Port 8000 açık mı

**Health Check Fail:**
- `/api/v1/health` endpoint çalışıyor mu
- Database bağlantısı var mı

## 📚 Detaylı Kılavuz

Daha fazla bilgi için: [`AWS_DEPLOYMENT_GUIDE.md`](AWS_DEPLOYMENT_GUIDE.md)

---

**Başarılar! 🚀**
