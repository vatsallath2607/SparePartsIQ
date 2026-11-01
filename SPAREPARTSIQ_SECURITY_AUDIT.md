# SparePartsIQ – Comprehensive Security Audit & Remediation Report

**Date of Audit:** 2026-11-01  
**Project:** SparePartsIQ – AI-Powered Industrial Spare Parts Inventory Management and Predictive Maintenance System  
**Audited Target:** React Frontend, FastAPI / Mangum Backend, AWS Cloud Infrastructure (`ap-south-1`, Account ID: `985539784799`)  
**Security Status Post-Remediation:** **ALL IDENTIFIED HIGH & MEDIUM VULNERABILITIES REMEDIATED**  

---

## 1. Executive Summary

A comprehensive security audit and remediation was executed across the SparePartsIQ codebase, runtime configurations, and AWS cloud infrastructure. All three primary vulnerabilities identified in the initial assessment—**SEC-01 (Hardcoded client-side passwords)**, **SEC-02 (Static JWT secret fallback)**, and **SEC-03 (Permissive wildcard CORS with credentials)**—have been completely resolved, deployed, and verified with live test evidence against the deployed AWS environment.

---

## 2. Remediation & Findings Matrix

| Finding ID | Severity | Category | Title | Initial Status | Post-Remediation Status |
|---|---|---|---|---|---|
| **SEC-01** | **High** | Client-Side Security | Hardcoded Demo Passwords in Frontend Bundle | Action Required | **RESOLVED & VERIFIED** |
| **SEC-02** | **Medium** | Cryptography / Auth | Static Fallback Secret for JWT Signatures | Action Required | **RESOLVED & VERIFIED** |
| **SEC-03** | **Medium** | Network Security | Insecure CORS Origin (`*`) with Credentials Enabled | Action Required | **RESOLVED & VERIFIED** |
| **SEC-04** | **Low** | Cloud Hardening | Missing API Gateway Access Logging & Custom Throttling | Recommended | Documented / Remaining |
| **SEC-05** | **Low** | Data Protection | DynamoDB Point-in-Time Recovery (PITR) Inactive | Recommended | Documented / Zero-Cost Constraint |
| **SEC-06** | **Low** | Repository Hygiene | Missing Root `.gitignore` for Environment Files | Fixed | **RESOLVED & VERIFIED** |

---

## 3. Detailed Remediation Evidence

### SEC-01: Hardcoded Demo Passwords in Frontend Bundle
- **Problem:** `frontend/src/context/AuthContext.jsx` exposed cleartext passwords in `passwordMap` and automatically logged into the Inventory Manager role on initial page load.
- **Remediation Implemented:**
  1. Completely deleted `passwordMap` and `loginWithDemo` from `AuthContext.jsx`.
  2. Removed automatic demo login in `useEffect`; unauthenticated visitors are presented with the secure login screen.
  3. Updated `frontend/src/pages/Login.jsx` so that clicking a role card only populates the role's email address and focuses the password input. Passwords must be typed and submitted through `/api/auth/login`.
  4. Updated `frontend/src/components/layout/Navbar.jsx` so switching roles performs a secure logout and redirects to `/login`.
  5. Regex scans across `frontend/src` confirmed **0 occurrences** of hardcoded passwords.
  6. Frontend production build (`npm run build`) succeeded with 0 errors.

---

### SEC-02: Static Fallback Secret for JWT Signatures
- **Problem:** `backend/config.py` fell back to `"sparepartsiq-enterprise-jwt-secret-key-2026"` if `JWT_SECRET` was omitted from environment variables.
- **Remediation Implemented:**
  1. Updated `backend/config.py` to enforce `JWT_SECRET = os.getenv("JWT_SECRET")`. If missing, startup fails immediately with a `RuntimeError`.
  2. Generated a 256-bit cryptographically secure random token (`secrets.token_hex(32)`).
  3. Injected `JWT_SECRET` directly into AWS Lambda `SparePartsIQ-Backend` environment variables via `aws lambda update-function-configuration`.
  4. Stored `JWT_SECRET` in local `.env` (which is excluded by root `.gitignore`).
  5. Tested forged token rejection: An adversary attempting to forge a JWT signed with the old static key receives **HTTP 401 Unauthorized** (`detail: "Could not validate credentials"`).
- **Session Impact:** Rotating `JWT_SECRET` immediately invalidates any tokens signed with the previous static key. Users must re-authenticate with their credentials to receive fresh tokens signed by the new key.

---

### SEC-03: Permissive CORS Configuration (`*`) with Credentials Enabled
- **Problem:** `backend/main.py` configured `allow_origins=["*"]` with `allow_credentials=True`, violating RFC CORS standards and allowing untrusted origins to send credentialed requests.
- **Remediation Implemented:**
  1. Removed `allow_origins=["*"]`.
  2. Implemented scoped origin matching in `backend/main.py` allowing only authorized application origins (`http://localhost:3000`, `http://127.0.0.1:3000`, `http://localhost:5173`, `http://127.0.0.1:5173`), with optional extension via `ALLOWED_ORIGINS` environment variable.
  3. Explicitly declared allowed HTTP methods (`GET, POST, PUT, DELETE, OPTIONS, PATCH`) and allowed headers (`Authorization, Content-Type, Accept, Origin, X-Requested-With`).
  4. **Live Verification Evidence:**
     - Preflight request with `Origin: http://localhost:3000` -> **HTTP 200 OK**, `Access-Control-Allow-Origin: http://localhost:3000`, `Access-Control-Allow-Credentials: true`.
     - Preflight request with untrusted `Origin: http://malicious-attacker.com` -> **HTTP 400 Bad Request**, `Access-Control-Allow-Origin: None`.

---

## 4. Live Verification Test Suite Output

Executed against the production AWS API Gateway endpoint (`https://ug4bzbni58.execute-api.ap-south-1.amazonaws.com/prod`):

```
=======================================
SECURITY REMEDIATION TEST RESULTS:
1. Scoped CORS Allowed Origin: PASS (HTTP 200, Allow-Origin: http://localhost:3000)
2. Untrusted Origin Blocked:    PASS (HTTP 400, No CORS headers reflected)
3. Valid Login (JWT):          PASS (HTTP 200, Secure token issued)
4. Invalid Login (401):        PASS (HTTP 401, Invalid credentials rejected)
5. Protected Route Access:     PASS (HTTP 200, 64 parts retrieved)
6. Unauthenticated Rejected:   PASS (HTTP 401, Not authenticated)
7. Forged Token Rejected:      PASS (HTTP 401, Old static key rejected)
=======================================
```

---

## 5. Remaining Low-Risk Items & Production Recommendations

1. **API Gateway Stage Logging & Throttling (SEC-04):**
   - *Status:* Low risk. Currently protected by AWS account-level default limits (10,000 RPS).
   - *Recommendation:* When transitioning from prototype to public release, configure structured CloudWatch access logging and per-client throttling keys on `ug4bzbni58/prod`.
2. **DynamoDB Point-in-Time Recovery (SEC-05):**
   - *Status:* Low risk. Point-in-time continuous backups are disabled to strictly observe the ₹0 zero-cost budget constraint.
   - *Recommendation:* Enable PITR on high-value tables (`SparePartsIQ-SpareParts`, `SparePartsIQ-PurchaseOrders`) once a production maintenance budget is allocated.
3. **AWS WAF (Web Application Firewall):**
   - *Recommendation:* For public internet deployments, attach an AWS WAF WebACL to the API Gateway REST API stage to block SQL injection, cross-site scripting, and bot scrapers.
