# NEXT-GENT Login Guide

## 🔐 Test Login Credentials

The database has been seeded with **200+ demo accounts** across 10 sectors.

### Default PIN
**All accounts use PIN:** `1234`

### Customer ID Format
`SECTOR-NNNNNN` (e.g., `MED-000001`)

---

## 🎯 Demo Accounts by Sector

| Sector | Customer ID Range | Example Login |
|--------|------------------|---------------|
| **Medical (Sağlık)** | `MED-000001` to `MED-000020` | `MED-000001` / `1234` |
| **Legal (Hukuk)** | `LEG-000001` to `LEG-000020` | `LEG-000001` / `1234` |
| **Real Estate (Emlak)** | `EST-000001` to `EST-000020` | `EST-000001` / `1234` |
| **Manufacturing (Sanayi)** | `MFG-000001` to `MFG-000020` | `MFG-000001` / `1234` |
| **E-Commerce** | `ECM-000001` to `ECM-000020` | `ECM-000001` / `1234` |
| **Education (Eğitim)** | `EDU-000001` to `EDU-000020` | `EDU-000001` / `1234` |
| **Finance (Finans)** | `FIN-000001` to `FIN-000020` | `FIN-000001` / `1234` |
| **Hospitality (Otelcilik)** | `HTL-000001` to `HTL-000020` | `HTL-000001` / `1234` |
| **Automotive (Otomotiv)** | `AUTO-000001` to `AUTO-000020` | `AUTO-000001` / `1234` |
| **Retail (Perakende)** | `RTL-000001` to `RTL-000020` | `RTL-000001` / `1234` |

---

## 🚀 How to Login

### Option 1: Using Frontend (Recommended)

1. **Open Browser:** Navigate to `http://localhost` or `http://localhost:5173` (dev mode)

2. **Enter Credentials:**
   - **Customer ID:** `MED-000001` (or any from table above)
   - **PIN:** `1234`

3. **Click "Sign In"**

### Option 2: Using API Directly (Testing)

```bash
curl -X POST http://localhost:8001/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "MED-000001",
    "pin": "1234"
  }'
```

Expected response:
```json
{
  "token": "token_...",
  "user": {
    "id": "...",
    "customer_id": "MED-000001",
    "name": "Ahmet Yılmaz",
    "email": "...",
    "phone": "...",
    "segment": "vip"
  },
  "tenant_id": "...",
  "sector": "medical",
  "tenant_name": "NextGent Sağlık"
}
```

---

## 👥 Customer Segments

Each sector has customers in different segments:

- **VIP:** `SECTOR-000001`, `SECTOR-000002` (highest value)
- **GOLD:** `SECTOR-000003` to `SECTOR-000005`
- **SILVER:** `SECTOR-000006` to `SECTOR-000010`
- **REGULAR:** `SECTOR-000011` to `SECTOR-000020`

---

## 🔧 Troubleshooting

### "Invalid customer ID or PIN" Error

**Cause:** Database not seeded or wrong credentials

**Solution:**
```bash
# Re-run seed script
docker-compose exec backend python comprehensive_seed.py

# Or check if backend is running
docker-compose ps
```

### Customer ID Not Found

**Common Mistakes:**
- ❌ `med-000001` (lowercase - wrong)
- ✅ `MED-000001` (uppercase - correct)
- ❌ `MED-0001` (missing zeros - wrong)
- ✅ `MED-000001` (6 digits - correct)

### Backend Not Responding

```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

---

## 📊 Sample Data Included

After seeding, you'll have:
- ✅ **200 customers** (20 per sector)
- ✅ **500+ interactions** (appointments/meetings)
- ✅ **300+ satisfaction surveys**
- ✅ **10 tenants** (one per sector)

---

## 🎨 Testing Different Sectors

To test different sector dashboards, login with different sector codes:

```bash
# Medical Dashboard
Customer ID: MED-000001, PIN: 1234

# Legal Dashboard  
Customer ID: LEG-000001, PIN: 1234

# E-Commerce Dashboard
Customer ID: ECM-000001, PIN: 1234

# Automotive Dashboard
Customer ID: AUTO-000001, PIN: 1234
```

Each sector has its own:
- Custom dashboard
- Specific interaction types
- Tailored analytics
- Sector-specific branding

---

## 🔒 Security Note

> ⚠️ **IMPORTANT:** Default PIN `1234` is for DEMO purposes only!
> 
> In production:
> - Use strong PINs (minimum 6 digits)
> - Implement PIN change on first login
> - Add rate limiting for failed login attempts
> - Enable 2FA for sensitive sectors

---

## 📞 Support

**Login Issues?**
1. Verify backend is running: `docker-compose ps`
2. Check backend logs: `docker-compose logs backend`
3. Verify database seed: `docker-compose exec backend python comprehensive_seed.py`
4. Check frontend connection: Open browser console (F12)

**Need Different Credentials?**
Edit `backend/comprehensive_seed.py` and:
- Change default PIN (line 157)
- Add more customers (line 147)
- Customize sectors (lines 22-92)
