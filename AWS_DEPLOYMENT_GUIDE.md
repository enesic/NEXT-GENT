# AWS Backend Deployment Kılavuzu - NextGent CRM

## 🎯 AWS Deployment Seçenekleri

NextGent backend'inizi AWS'ye deploy etmek için 3 seçenek var:

### Seçenek 1: AWS App Runner (⭐ ÖNERİLEN - En Kolay)
- ✅ Docker containerları direkt deploy
- ✅ Otomatik ölçeklendirme
- ✅ HTTPS otomatik
- ✅ Minimal konfigürasyon
- 💰 Maliyet: ~$25-50/ay

### Seçenek 2: AWS Elastic Beanstalk (Dengeli)
- ✅ Docker support
- ✅ Tam kontrol
- ✅ Load balancing
- ✅ Auto-scaling
- 💰 Maliyet: ~$30-80/ay

### Seçenek 3: AWS ECS Fargate (İleri Seviye)
- ✅ Tam container kontrolü
- ✅ Mikroservis mimarisi
- ✅ En esnek
- ⚠️ Daha kompleks
- 💰 Maliyet: ~$40-100/ay

---

## 🚀 Seçenek 1: AWS App Runner (ÖNERİLEN)

AWS App Runner, Docker containerlarını otomatik olarak deploy eder ve yönetir.

### Adım 1: AWS Hesabı ve IAM Kurulumu

**1.1. AWS Hesabı Oluşturun:**
- https://aws.amazon.com adresine gidin
- **Create an AWS Account** butonuna tıklayın
- Email, şifre ve kredi kartı bilgilerini girin
- Free tier kullanabilirsiniz (12 ay)

**1.2. IAM User Oluşturun (Güvenlik için):**
1. AWS Console → **IAM** service
2. **Users** → **Add user**
3. User name: `nextgent-deployer`
4. **Attach policies directly** seçin
5. Şu policy'leri ekleyin:
   - `AWSAppRunnerFullAccess`
   - `AmazonEC2ContainerRegistryPowerUser`
   - `IAMReadOnlyAccess`
6. **Create user**
7. **Security credentials** → **Create access key**
8. Access key type: **Command Line Interface (CLI)**
9. Access Key ID ve Secret Access Key'i kaydedin

### Adım 2: AWS CLI Kurulumu ve Login

**2.1. AWS CLI Kurulumu:**

**Windows:**
```powershell
# MSI Installer ile
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Ya da Chocolatey ile
choco install awscli
```

**2.2. AWS CLI Yapılandırması:**
```bash
aws configure

# Sorulan bilgileri girin:
AWS Access Key ID: YOUR_ACCESS_KEY_ID
AWS Secret Access Key: YOUR_SECRET_ACCESS_KEY
Default region name: eu-central-1  # Frankfurt
Default output format: json
```

### Adım 3: Docker Image'ı ECR'a Push Etme

**3.1. ECR Repository Oluşturun:**
```bash
# ECR repository oluştur
aws ecr create-repository --repository-name nextgent-backend --region eu-central-1
```

**3.2. Docker Image Build ve Push:**
```powershell
# Backend klasörüne gidin
cd backend

# ECR login
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com

# Docker image build
docker build -t nextgent-backend .

# Tag
docker tag nextgent-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest

# Push
docker push YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest
```

**Not:** `YOUR_ACCOUNT_ID` yerine AWS Account ID'nizi yazın (12 haneli numara).

**AWS Account ID Bulma:**
```bash
aws sts get-caller-identity --query Account --output text
```

### Adım 4: App Runner Service Oluşturma

**4.1. AWS Console'dan:**

1. AWS Console → **App Runner** service
2. **Create service** butonuna tıklayın

**Source:**
- Source type: **Container registry**
- Provider: **Amazon ECR**
- Container image URI: 
  ```
  YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest
  ```
- Deployment trigger: **Manual** (şimdilik)
- ECR access role: **Create new service role**

**Service settings:**
- Service name: `nextgent-backend`
- Virtual CPU: **1 vCPU**
- Memory: **2 GB**
- Port: **8000**

**Environment variables:**

*Environment variables* sekmesinde aşağıdaki değişkenleri ekleyin:

```env
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Güvenlik Anahtarları (YENİ OLUŞTURUN!)
SECRET_KEY=your-new-secret-key
ENCRYPTION_KEY=your-new-encryption-key

# Vercel Postgres
POSTGRES_URL=postgres://default:xxx@ep-xxx.vercel-storage.com:5432/verceldb
POSTGRES_SERVER=ep-xxx.vercel-storage.com
POSTGRES_USER=default
POSTGRES_PASSWORD=xxx
POSTGRES_DB=verceldb
POSTGRES_PORT=5432

# Vercel KV (Redis)
REDIS_URL=redis://default:xxx@xxx.vercel-storage.com:6379
REDIS_HOST=xxx.vercel-storage.com
REDIS_PORT=6379
REDIS_PASSWORD=xxx

# CORS (Vercel frontend URL)
BACKEND_CORS_ORIGINS=https://next-gent-bbxs21jcs-enesics-projects.vercel.app,https://nextgent.co

# OpenAI (opsiyonel)
OPENAI_API_KEY=sk-proj-your-key
AI_MODEL=gpt-4o-mini
AI_ENABLED=true
```

**Auto scaling:**
- Min instances: **1**
- Max instances: **5**

**Health check:**
- Path: `/api/v1/health`
- Interval: **20 seconds**
- Timeout: **5 seconds**

3. **Create & deploy** butonuna tıklayın

**4.2. CLI ile (Alternatif):**

```bash
# apprunner.json dosyası oluşturun
cat > apprunner.json << 'EOF'
{
  "ServiceName": "nextgent-backend",
  "SourceConfiguration": {
    "ImageRepository": {
      "ImageIdentifier": "YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest",
      "ImageConfiguration": {
        "Port": "8000",
        "RuntimeEnvironmentVariables": {
          "PROJECT_NAME": "NextGent",
          "API_V1_STR": "/api/v1",
          "ENVIRONMENT": "production",
          "DEBUG": "false"
        }
      },
      "ImageRepositoryType": "ECR"
    },
    "AutoDeploymentsEnabled": false
  },
  "InstanceConfiguration": {
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }
}
EOF

# Service oluştur
aws apprunner create-service --cli-input-json file://apprunner.json --region eu-central-1
```

### Adım 5: Backend URL'yi Alın

Service oluştuktan sonra (3-5 dakika):

```bash
# Service URL'yi alın
aws apprunner list-services --region eu-central-1

# Service details
aws apprunner describe-service --service-arn YOUR_SERVICE_ARN --region eu-central-1
```

URL formatı:
```
https://xxxxx.eu-central-1.awsapprunner.com
```

### Adım 6: Frontend .env Güncelleme

`frontend\.env.production` dosyasını güncelleyin:

```env
VITE_API_BASE_URL=https://xxxxx.eu-central-1.awsapprunner.com/api/v1
```

Vercel'e tekrar deploy edin:
```bash
vercel --prod --yes
```

### Adım 7: Test

1. Backend health check:
   ```bash
   curl https://xxxxx.eu-central-1.awsapprunner.com/api/v1/health
   ```

2. Frontend'i açın: https://nextgent.co
3. Test hesapları ile giriş yapın

---

## 🔧 Seçenek 2: AWS Elastic Beanstalk

Daha fazla kontrol istiyorsanız Elastic Beanstalk kullanın.

### Adım 1: EB CLI Kurulumu

```bash
pip install awsebcli
```

### Adım 2: Elastic Beanstalk Uygulaması Oluşturma

```bash
cd backend

# EB init
eb init -p docker nextgent-backend --region eu-central-1

# Environment oluştur
eb create nextgent-backend-prod --instance-type t3.small --envvars \
  PROJECT_NAME=NextGent,\
  API_V1_STR=/api/v1,\
  ENVIRONMENT=production,\
  DEBUG=false,\
  POSTGRES_URL=your-vercel-postgres-url,\
  REDIS_URL=your-vercel-redis-url,\
  BACKEND_CORS_ORIGINS=https://nextgent.co
```

### Adım 3: Deploy

```bash
# Deploy
eb deploy

# Status
eb status

# Logs
eb logs

# URL'yi al
eb open
```

---

## 🐳 Seçenek 3: AWS ECS Fargate

En esnek ve ölçeklenebilir seçenek.

### Hızlı Kurulum

**1. ECR'a Push (Adım 3'teki gibi)**

**2. ECS Cluster Oluştur:**
```bash
aws ecs create-cluster --cluster-name nextgent-cluster --region eu-central-1
```

**3. Task Definition Oluştur:**

`task-definition.json` dosyası oluşturun:

```json
{
  "family": "nextgent-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "1024",
  "memory": "2048",
  "containerDefinitions": [
    {
      "name": "nextgent-backend",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "PROJECT_NAME", "value": "NextGent"},
        {"name": "API_V1_STR", "value": "/api/v1"},
        {"name": "ENVIRONMENT", "value": "production"}
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/nextgent-backend",
          "awslogs-region": "eu-central-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

**4. Service Oluştur:**
```bash
aws ecs create-service \
  --cluster nextgent-cluster \
  --service-name nextgent-backend-service \
  --task-definition nextgent-backend \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}" \
  --region eu-central-1
```

---

## 💰 Maliyet Karşılaştırması

| Servis | CPU/RAM | Aylık Maliyet (Tahmini) |
|--------|---------|------------------------|
| **App Runner** | 1 vCPU, 2GB | $25-50 |
| **Elastic Beanstalk** | t3.small | $30-80 |
| **ECS Fargate** | 1 vCPU, 2GB | $40-100 |
| **Vercel Postgres** | - | $5-10 |
| **Vercel KV** | - | $0-1 |
| **Vercel Frontend** | - | $0-20 |
| **TOPLAM** | | **$60-180/ay** |

**Not:** Free tier (12 ay) kullanırsanız ilk yıl daha ucuz olabilir.

---

## 📋 Environment Variables Listesi

Tüm AWS seçenekleri için gerekli environment variables:

```env
# Uygulama
PROJECT_NAME=NextGent
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Güvenlik (YENİ OLUŞTUR!)
SECRET_KEY=<python -c "import secrets; print(secrets.token_urlsafe(32))">
ENCRYPTION_KEY=<python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())">

# Vercel Postgres (Vercel dashboard'dan)
DATABASE_URL=postgres://default:xxx@ep-xxx.vercel-storage.com:5432/verceldb
POSTGRES_SERVER=ep-xxx.vercel-storage.com
POSTGRES_USER=default
POSTGRES_PASSWORD=xxx
POSTGRES_DB=verceldb
POSTGRES_PORT=5432

# Vercel KV / Redis (Vercel dashboard'dan)
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

---

## 🔒 Güvenlik Best Practices

### 1. IAM Roles
- App Runner için en az yetki prensibi
- Sadece gerekli policy'leri ekleyin

### 2. Secrets Manager (Opsiyonel)
Database şifrelerini AWS Secrets Manager'da saklayın:

```bash
# Secret oluştur
aws secretsmanager create-secret \
  --name nextgent/database \
  --secret-string '{"POSTGRES_PASSWORD":"xxx","REDIS_PASSWORD":"xxx"}' \
  --region eu-central-1
```

App Runner'da secret'ları kullanın:
```json
{
  "Secrets": [
    {
      "Name": "POSTGRES_PASSWORD",
      "ValueFrom": "arn:aws:secretsmanager:eu-central-1:xxx:secret:nextgent/database:POSTGRES_PASSWORD::"
    }
  ]
}
```

### 3. VPC Configuration
Production'da VPC kullanın:
- Private subnet'ler
- NAT Gateway
- Security groups

### 4. SSL/HTTPS
- App Runner otomatik HTTPS sağlar
- Custom domain için AWS Certificate Manager kullanın

---

## 🚀 Deployment Automation

### GitHub Actions ile Otomatik Deployment

`.github/workflows/deploy-aws.yml` oluşturun:

```yaml
name: Deploy to AWS App Runner

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-central-1
      
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
      
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: nextgent-backend
          IMAGE_TAG: ${{ github.sha }}
        run: |
          cd backend
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
      
      - name: Deploy to App Runner
        run: |
          aws apprunner start-deployment \
            --service-arn ${{ secrets.APP_RUNNER_SERVICE_ARN }} \
            --region eu-central-1
```

GitHub Secrets'a ekleyin:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `APP_RUNNER_SERVICE_ARN`

---

## 📊 Monitoring ve Logging

### CloudWatch Logs

```bash
# Logs görüntüle
aws logs tail /aws/apprunner/nextgent-backend/xxxxx/application --follow

# Specific log stream
aws logs get-log-events \
  --log-group-name /aws/apprunner/nextgent-backend/xxxxx/application \
  --log-stream-name xxxxx
```

### CloudWatch Metrics

App Runner otomatik olarak metrics toplar:
- Request count
- Response time
- Error rate
- CPU/Memory usage

AWS Console → CloudWatch → Metrics → App Runner

---

## 🆘 Troubleshooting

### Service Başlamıyor
```bash
# Service status
aws apprunner describe-service --service-arn YOUR_ARN

# Logs kontrol
aws logs tail /aws/apprunner/nextgent-backend/xxxxx/application --follow
```

### Health Check Fail
- Health check path doğru mu: `/api/v1/health`
- Port 8000 expose edilmiş mi
- Environment variables doğru mu

### Database Connection Error
- Vercel Postgres connection string doğru mu
- Security group outbound rules açık mı
- IP whitelist varsa App Runner IP'si eklenmiş mi

### CORS Hataları
- `BACKEND_CORS_ORIGINS` değişkeninde Vercel URL var mı
- Service redeploy edildi mi

---

## ✅ Deployment Kontrol Listesi

- [ ] AWS hesabı oluşturuldu
- [ ] IAM user ve access keys oluşturuldu
- [ ] AWS CLI kuruldu ve yapılandırıldı
- [ ] ECR repository oluşturuldu
- [ ] Docker image build edildi
- [ ] Image ECR'a push edildi
- [ ] App Runner service oluşturuldu
- [ ] Environment variables eklendi
- [ ] Service başarıyla deploy edildi
- [ ] Backend URL alındı
- [ ] Frontend .env.production güncellendi
- [ ] Frontend Vercel'e tekrar deploy edildi
- [ ] Health check testi yapıldı
- [ ] Login testi yapıldı
- [ ] CORS çalışıyor

---

## 🎯 Özet Komutlar

```bash
# AWS CLI yapılandır
aws configure

# Account ID
aws sts get-caller-identity --query Account --output text

# ECR repository oluştur
aws ecr create-repository --repository-name nextgent-backend --region eu-central-1

# ECR login
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com

# Docker build & push
cd backend
docker build -t nextgent-backend .
docker tag nextgent-backend:latest ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest
docker push ACCOUNT_ID.dkr.ecr.eu-central-1.amazonaws.com/nextgent-backend:latest

# App Runner service oluştur (AWS Console'dan daha kolay)
# Ya da CLI ile: aws apprunner create-service ...

# Frontend güncelle
cd ../frontend
# .env.production dosyasını güncelle
vercel --prod --yes
```

---

**Başarılar! AWS deployment ile production-ready bir sistem kuruyorsunuz! 🚀**

*Son güncelleme: 12 Şubat 2026*
