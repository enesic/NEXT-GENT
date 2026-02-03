# 📋 NEXT-GENT Handover Plan & Prompts

This document outlines the remaining tasks to complete the system restoration.
**Instructions for the next developer:** Copy and paste the "🤖 Prompt for Agent" into your AI agent *one by one* to execute the tasks sequentially.

---

## 🚨 TASK 1: Fix Admin Dashboard Redirect (CRITICAL)
**Context:**  
The admin login (`/admin/login`) works successfully, but when redirecting to `/admin/dashboard`, the user is wrongly redirected to the *customer* login page (`/login`). This suggests a flaw in the Vue Router navigation guards in `frontend/src/router/index.js`.

**🤖 Prompt for Agent:**
```text
Check the `src/router/index.js` file and the `src/stores/admin.js` store. 
There is a bug where logging in as an admin redirects the user to the customer login page ('/login') instead of the Admin Dashboard ('/admin/dashboard').
1. Analyze the `router.beforeEach` guard logic. likely the check for `requiresAuth` (customer) is triggering for admin routes mistakenly.
2. Ensure that `AdminDashboard` route metadata correctly includes `requiresAdminAuth: true`.
3. Fix the logic so that admin routes strictly check `adminStore.isAuthenticated` and do NOT fall through to the customer auth check.
4. Verify the fix by reviewing the code logic.
```

---

## 📂 TASK 2: Implement Documents System
**Context:**  
The `DocumentsView.vue` page currently uses static mock data. It needs a real backend implementation to list, upload, and download files.

**🤖 Prompt for Agent:**
```text
We need to implement the Documents system.
1. Backend: Create a `Document` SQLAlchemy model (id, tenant_id, filename, file_url, file_type, size, created_at).
2. Backend: Create `app/services/document_service.py` to handle logic (mock the actual S3/storage part for now, just store metadata in DB).
3. Backend: Create API endpoints in `app/api/v1/endpoints/documents.py` (GET /documents, POST /documents/upload).
4. Frontend: Update `src/views/DocumentsView.vue` to fetch data from the real API instead of using mock data.
```

---

## 🔐 TASK 3: PII Encryption
**Context:**  
Customer phone numbers and sensitive PII must be encrypted in the database for security compliance.

**🤖 Prompt for Agent:**
```text
Implement PII encryption for the `Customer` model.
1. Modify `app/models/customer.py` to use an encrypted type for the `phone` field.
2. Use `app/core/security.py` or create a helper for encryption/decryption using the `fernet` or `passlib` key.
3. Update `app/api/v1/endpoints/user_management_endpoints.py` and `vapi.py` to ensure they handle the encryption transparently (encrypt on save, decrypt on read).
4. Update `seed_real_data.py` to ensure new seed data is encrypted.
```

---

## 📊 TASK 4: Survey Logic & Notification Fixes
**Context:**  
The `function_calling_service.py` has TODOs for survey sending. Also, `NotificationPanel.vue` has broken navigation links.

**🤖 Prompt for Agent:**
```text
Complete the following small features:
1. Backend: In `app/services/function_calling_service.py`, find the `send_survey` method and implement the logic (it currently has a TODO). It should create a `Satisfaction` record in the DB.
2. Frontend: Open `src/components/NotificationPanel.vue` and fix the `handleNotificationClick` function to correctly navigate to the target routes (e.g., /appointments, /settings).
```

---

## 🧹 TASK 5: Final Quality Check & Cleanup
**Context:**  
Final polish before "Sunday Launch" readiness.

**🤖 Prompt for Agent:**
```text
Perform final quality checks:
1. Analyze `backend/error.log` (if it exists) and fix any recurring errors.
2. Run standard linting on the backend (`flake8` or `black` if available) to fix formatting.
3. Ensure `backend/requirements.txt` is clean and has no duplicates (check for 'bcrypt' or 'passlib' duplicates again).
4. Update `walkthrough.md` to reflect the final state of the system.
```
