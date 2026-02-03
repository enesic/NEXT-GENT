# Admin Panel Login Guide

## 🔐 Admin Login Credentials

**Username:** `admin`  
**Password:** `admin123`

---

## 📍 Admin Panel Access

### Login URL
```
http://localhost/admin/login
```

Or if using frontend dev server:
```
http://localhost:5173/admin/login
```

---

## 🚀 How to Login

1. **Open Browser** → Navigate to admin login page

2. **Enter Credentials:**
   - Username: `admin`
   - Password: `admin123`

3. **Click "Giriş Yap"** (Sign In)

4. **You'll be redirected to:** `/admin/dashboard`

---

## 📊 Admin Panel Features

After login, you'll have access to:

### Dashboard
- `GET /admin/dashboard` - System statistics
- Total customers, revenue, calls, subscriptions
- Growth metrics

### Cards Management  
- `GET /admin/cards` - View all subscription tiers
- `PATCH /admin/cards/{id}/toggle` - Enable/disable cards

### Flow Engine
- Automation workflows
- Flow executions
- FlowEngine management

### Analytics
- Traffic data (`GET /admin/traffic`)
- Token consumption (`GET /admin/tokens`)
- Performance metrics

### Audit Logs
- `GET /admin/logs` - KVKK compliant logs
- Filter by action type
- Pagination support

---

## 🔒 Admin User Details

| Field | Value |
|-------|-------|
| Username | `admin` |
| Email | `admin@nextgent.com` |
| Full Name | System Administrator |
| Role | SUPER_ADMIN |
| Status | Active |

---

## 🛡️ Security Features

### JWT Authentication
- Access tokens expire in 24 hours
- Token refresh endpoint: `POST /auth/admin/refresh`
- Secure HTTP Bearer authentication

### Audit Logging
- All admin actions logged
- IP address tracking
- User agent logging
- KVKK compliant

### Password Security
- bcrypt hashing (salt rounds: 12)
- Case-sensitive passwords
- No password in plaintext

---

## 🔧 API Endpoints

### Authentication
```bash
# Login
POST /api/v1/auth/admin/login
{
  "username": "admin",
  "password": "admin123"
}

# Response
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer",
  "admin_user": {
    "id": "...",
    "username": "admin",
    "email": "admin@nextgent.com",
    "full_name": "System Administrator",
    "role": "super_admin"
  }
}

# Logout
POST /api/v1/auth/admin/logout
Headers: Authorization: Bearer <token>

# Get Current Admin
GET /api/v1/auth/admin/me
Headers: Authorization: Bearer <token>

# Refresh Token
POST /api/v1/auth/admin/refresh
Headers: Authorization: Bearer <token>
```

### Admin Operations
```bash
# Dashboard Stats
GET /api/v1/admin/dashboard

# Cards
GET /api/v1/admin/cards
PATCH /api/v1/admin/cards/{id}/toggle

# Traffic Data
GET /api/v1/admin/traffic?days=7

# Token Analytics
GET /api/v1/admin/token-analytics?days=30

# Audit Logs
GET /api/v1/admin/logs?page=1&page_size=50
```

---

## 🔄 Creating Additional Admin Users

To create more admin users, edit `backend/create_admin.py`:

```python
admin = AdminUser(
    username="new_admin",
    email="new_admin@nextgent.com",
    password_hash=bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
    full_name="New Administrator",
    role=AdminRole.ADMIN,  # or AdminRole.SUPER_ADMIN
    is_active=True
)
```

Then run:
```bash
docker-compose exec backend python create_admin.py
```

---

## 🎭 Admin Roles

| Role | Permissions |
|------|-------------|
| `SUPER_ADMIN` | Full system access, user management |
| `ADMIN` | Dashboard, analytics, basic operations |
| `MODERATOR` | Read-only dashboard access |

---

## ⚠️ Security Best Practices

### Production Deployment
1. **Change default password immediately**
2. **Use strong passwords:** Minimum 12 characters, mixed case, symbols
3. **Enable 2FA** (implement in production)
4. **Use HTTPS only**
5. **Set up rate limiting** for login endpoint
6. **Regular audit log reviews**
7. **Rotate JWT secrets** periodically

### Password Change
```bash
# Update password via database
docker-compose exec backend python -c "
import bcrypt
from app.core.database import SessionLocal
from app.models.admin_user import AdminUser

db = SessionLocal()
admin = db.query(AdminUser).filter_by(username='admin').first()
new_password = 'YourNewStrongPassword123!'
admin.password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
db.commit()
print('Password updated!')
"
```

---

## 🐛 Troubleshooting

### "Invalid username or password"
- Verify credentials: `admin` / `admin123`
- Username is case-sensitive
- Re-run `create_admin.py` if needed

### "Account is inactive"
- Admin user `is_active` field is False
- Update in database manually

### "Token has expired"
- Use the refresh token endpoint
- Re-login to get new token

### Backend Not Responding
```bash
# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

---

## 📞 Support

**Admin Issues?**
1. Check backend logs: `docker-compose logs backend -f`
2. Verify database: Admin user exists in `admin_users` table
3. Test login endpoint: `curl -X POST http://localhost:8001/api/v1/auth/admin/login`

**Need Help?**
- Check API docs: `http://localhost:8001/api/v1/docs`
- Review audit logs for debugging
- Enable debug logging in backend

---

**Created:** 2026-02-03  
**Admin Panel:** ✅ Ready for Use  
**Default Credentials:** admin / admin123
