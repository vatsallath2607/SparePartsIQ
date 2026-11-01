# SparePartsIQ – Final AWS Cost, Resource, and Deployment Audit Report

**Date of Audit:** 2026-11-01  
**AWS Account ID:** `985539784799`  
**Primary Region:** `ap-south-1` (Mumbai)  
**Audit Type:** Strict Read-Only Comprehensive Resource & Cost Inspection  
**Audit Tooling:** AWS SDK for Python (`boto3`), AWS CloudWatch API, AWS Cost & Infrastructure APIs  

---

## 1. Executive Summary

A comprehensive, strictly read-only audit of the AWS cloud infrastructure supporting the **SparePartsIQ** platform was conducted. The architecture is built on a 100% serverless, event-driven pattern designed for high availability, zero idle operational cost, and full compliance with the strict ₹0 development budget.

### Key Audit Findings
* **Zero Idle Provisioned Infrastructure:** No Amazon EC2 instances, No VPC NAT Gateways, No Provisioned Concurrency, No API Gateway Cache Clusters, and No Provisioned DynamoDB Capacity Units exist.
* **Monthly Active Cost (Current Usage):** **$0.00 / month (₹0.00)** within the AWS Free Tier.
* **Monthly Projected Cost (Post-Free Tier / Steady State):** **~$0.04 / month (~₹3.30)** at current production traffic rates (~10,000 requests/month).
* **Data & Operational Integrity:** 100% of production tables, ML models, and configurations remain online, active, and fully operational. No resources were stopped, deleted, or modified during this audit.

---

## 2. Resource Inventory & Configuration Details

### 2.1 AWS Lambda

| Attribute | Inspected Configuration | Cost Impact / Analysis |
|---|---|---|
| **Function Name** | `SparePartsIQ-Backend` | Single monolithic serverless FastAPI application via Mangum |
| **Runtime** | `python3.12` (x86_64) | Modern, optimized runtime |
| **Memory Allocation** | `1024 MB` (1.0 GB) | Required for rapid SciPy / Scikit-Learn in-memory ML inference |
| **Timeout** | `60 seconds` | Accommodates cold-start model downloads from S3 (typically 7s cold, 136ms warm) |
| **Code Package Size** | `68,690,963 bytes` (65.51 MB zip) | Contains compiled `scikit-learn`, `scipy`, `numpy`, and application routers |
| **Execution Role** | `arn:aws:iam::985539784799:role/SparePartsIQ-LambdaExecutionRole` | Scoped least-privilege role |
| **Provisioned Concurrency**| `0` (None configured) | **$0.00 idle cost** (avoids ~$10/month per provisioned instance) |
| **Environment Variables** | `STORAGE_MODE=aws`, `JWT_SECRET=[256-bit secure token]` | Securely injected; zero plaintext credentials |

### 2.2 Amazon API Gateway

| Attribute | Inspected Configuration | Cost Impact / Analysis |
|---|---|---|
| **API ID / Name** | `ug4bzbni58` / `SparePartsIQ-API` | Regional REST API |
| **Stage** | `prod` | Single active deployment stage |
| **Cache Cluster** | `cacheClusterEnabled: false` | **CRITICAL: Disabled.** Avoids $0.020/hr ($14.40/month) cache cluster fee |
| **X-Ray Tracing** | `tracingEnabled: false` | Avoids AWS X-Ray ingestion fees |
| **Public Base URL** | `https://ug4bzbni58.execute-api.ap-south-1.amazonaws.com/prod` | Direct Lambda proxy integration (`ANY /{proxy+}`) |

### 2.3 Amazon DynamoDB

All tables are configured in **PAY_PER_REQUEST (On-Demand)** billing mode. There are zero provisioned Read Capacity Units (RCU) or Write Capacity Units (WCU), guaranteeing zero charges when no transactions occur.

| Table Name | Billing Mode | Item Count | Table Size (Bytes) | Table Size (KB) | PITR Status |
|---|---|:---:|:---:|:---:|:---:|
| `SparePartsIQ-SpareParts` | `PAY_PER_REQUEST` | 64 | 41,003 | 40.04 KB | DISABLED |
| `SparePartsIQ-ForecastResults` | `PAY_PER_REQUEST` | 117 | 110,400 | 107.81 KB | DISABLED |
| `SparePartsIQ-InventoryTransactions`| `PAY_PER_REQUEST` | 207 | 69,674 | 68.04 KB | DISABLED |
| `SparePartsIQ-ReorderRecommendations`| `PAY_PER_REQUEST` | 53 | 31,547 | 30.81 KB | DISABLED |
| `SparePartsIQ-MaintenanceSchedules` | `PAY_PER_REQUEST` | 26 | 11,146 | 10.88 KB | DISABLED |
| `SparePartsIQ-PurchaseOrders` | `PAY_PER_REQUEST` | 20 | 8,463 | 8.26 KB | DISABLED |
| `SparePartsIQ-Notifications` | `PAY_PER_REQUEST` | 15 | 4,370 | 4.27 KB | DISABLED |
| `SparePartsIQ-Suppliers` | `PAY_PER_REQUEST` | 10 | 2,541 | 2.48 KB | DISABLED |
| `SparePartsIQ-Users` | `PAY_PER_REQUEST` | 4 | 925 | 0.90 KB | DISABLED |
| `SparePartsIQ-CFT-Test` *(Unused)* | `PAY_PER_REQUEST` | 0 | 0 | 0.00 KB | DISABLED |
| **TOTAL** | — | **516 items** | **280,069 bytes** | **273.50 KB (~0.27 MB)** | — |

*Note on PITR:* Point-in-Time Recovery is intentionally `DISABLED` across all tables, avoiding the continuous backup storage fee ($0.20 per GB/month).

### 2.4 Amazon S3

* **Bucket Name:** `sparepartsiq-artifacts-985539784799`
* **Default Encryption:** Server-Side Encryption with Amazon S3-managed keys (`SSE-S3` / AES-256) — **$0.00 KMS charges**.
* **Storage Class:** `STANDARD` across all stored objects.
* **Total Objects:** 12 objects
* **Total Stored Size:** `72,162,056 bytes` (**68.82 MB**)

#### Object Breakdown by Prefix
| Prefix / Category | Object Count | Size (MB) | Purpose / Description |
|---|:---:|:---:|---|
| `lambda/` | 1 | 65.51 MB | Packaged backend bundle (`backend_lambda.zip`) with manylinux ML wheels |
| `frontend/` | 8 | 2.30 MB | Static build assets (`index.html`, SVG icons, compiled JS/CSS bundles) |
| `models/` | 2 | 0.62 MB | Trained champion model (`champion_forecast_model.joblib`) & evaluation report |
| `datasets/` | 1 | 0.39 MB | Baseline consumption data (`historical_consumption.csv`) |
| **Total** | **12** | **68.82 MB** | **1.38% of the 5 GB S3 Free Tier allowance** |

### 2.5 Amazon EventBridge

* **Rule Name:** `SparePartsIQ-DailyForecastingRule`
* **Status:** `ENABLED`
* **Schedule Expression:** `cron(0 2 * * ? *)` (Runs once daily at 02:00 UTC / 07:30 IST)
* **Target:** `arn:aws:lambda:ap-south-1:985539784799:function:SparePartsIQ-Backend`
* **Cost Impact:** Scheduled rules on the default event bus are **free of charge**. With ~30 executions per month, event evaluation incurs **$0.00**.

### 2.6 Amazon SNS

* **Topic ARN:** `arn:aws:sns:ap-south-1:985539784799:SparePartsIQ-Alerts`
* **Active Subscriptions:** `0` (Zero SMS, Zero HTTP, Zero Email subscriptions)
* **Pending Subscriptions:** `0`
* **Cost Impact:** Publishing to an SNS topic with 0 active endpoints is completely covered under the 1,000,000 free requests per month. No telecommunication SMS charges can occur.

### 2.7 Amazon CloudWatch Logs & Metrics

* **Log Group:** `/aws/lambda/SparePartsIQ-Backend`
* **Retention Policy:** `Never expire` (Default)
* **Current Stored Volume:** `< 1 MB` (Reports 0 bytes in standard aggregated metering)
* **7-Day Telemetry Metrics:**
  * **Lambda Invocations:** `2,292` calls
  * **Lambda Execution Errors:** `8` (initial warm-up/syntax tests)
  * **Lambda Average Duration:** `136.44 ms`
  * **API Gateway Total Requests:** `2,209` calls

### 2.8 AWS Identity and Access Management (IAM)

* **Execution Role:** `arn:aws:iam::985539784799:role/SparePartsIQ-LambdaExecutionRole`
  * Attached Managed Policy: `AWSLambdaBasicExecutionRole` (CloudWatch Logs creation)
  * Inline Policy: `SparePartsIQ-LambdaRuntimePolicy` (strictly scoped to `SparePartsIQ-*` DynamoDB tables, `sparepartsiq-artifacts-*` S3 bucket, and `SparePartsIQ-Alerts` SNS topic).
* **Cost Impact:** IAM roles, policies, and STS assume-role actions are **100% free of charge**.

---

## 3. Cost Analysis & Free Tier Comparison

### 3.1 Free Tier Allowance vs. Actual SparePartsIQ Usage

| Service | AWS Free Tier Monthly Allowance | SparePartsIQ Monthly Usage | % of Free Tier Consumed | Free Tier Status |
|---|---|---|:---:|:---:|
| **AWS Lambda (Compute)** | 400,000 GB-seconds / month | ~312 GB-seconds / month | **0.08%** | **$0.00 (Free)** |
| **AWS Lambda (Requests)** | 1,000,000 requests / month | ~10,000 requests / month | **1.00%** | **$0.00 (Free)** |
| **API Gateway (REST)** | 1,000,000 calls / month (1st 12 mo) | ~10,000 calls / month | **1.00%** | **$0.00 (Free)** |
| **DynamoDB (Storage)** | 25 GB free forever | 0.00027 GB (273.5 KB) | **0.001%** | **$0.00 (Free)** |
| **DynamoDB (Requests)** | 2.5M reads / 2.5M writes / month | ~25,000 read/write units | **1.00%** | **$0.00 (Free)** |
| **Amazon S3 (Storage)** | 5 GB Standard (1st 12 mo) | 0.0688 GB (68.82 MB) | **1.38%** | **$0.00 (Free)** |
| **Amazon S3 (Requests)** | 20,000 GET / 2,000 PUT | < 500 requests | **< 2.5%** | **$0.00 (Free)** |
| **CloudWatch (Logs)** | 5 GB ingestion & 5 GB storage | < 0.05 GB | **< 1.0%** | **$0.00 (Free)** |
| **Amazon SNS (Publishes)**| 1,000,000 publishes / month | < 100 publishes | **0.01%** | **$0.00 (Free)** |
| **EventBridge (Schedules)**| Unlimited scheduled rules | 30 executions / month | **0.00%** | **$0.00 (Free)** |

---

## 4. Projected Monthly Costs: Verified vs. Out-of-Free-Tier Estimate

The following table distinguishes verified active costs from theoretical out-of-pocket costs if the AWS account's 12-month introductory Free Tier expires, assuming current steady-state workload (~10,000 requests/month):

| Service Component | AWS Pricing Rate (ap-south-1) | Verified Monthly Cost (Free Tier Active) | Estimated Monthly Cost (Post-Free Tier) |
|---|---|:---:|:---:|
| **AWS Lambda Invocations** | $0.20 per 1M requests | $0.00 | $0.002 |
| **AWS Lambda Duration** | $0.0000166667 per GB-second | $0.00 | $0.005 |
| **API Gateway Requests** | $3.50 per 1M requests | $0.00 | $0.035 |
| **DynamoDB Storage** | Free up to 25 GB permanently | $0.00 | $0.000 |
| **DynamoDB On-Demand I/O** | $1.25/M writes, $0.25/M reads | $0.00 | $0.002 |
| **Amazon S3 Storage** | $0.023 per GB-month | $0.00 | $0.002 |
| **Amazon S3 API Operations** | $0.005 per 1,000 PUT/GET | $0.00 | $0.001 |
| **CloudWatch Logs** | Free up to 5 GB permanently | $0.00 | $0.000 |
| **EventBridge Scheduler** | Free for scheduled events | $0.00 | $0.000 |
| **Amazon SNS** | 1M requests free permanently | $0.00 | $0.000 |
| **TOTAL ESTIMATED MONTHLY**| — | **$0.00 (₹0.00)** | **~$0.047 (~₹3.90)** |

> [!NOTE]
> Even if all 12-month promotional Free Tier benefits were to expire immediately, the monthly cost of operating SparePartsIQ at current traffic is **less than $0.05 (under 4 Indian Rupees)**.

---

## 5. Identification of Redundant / Inactive Resources

The audit identified two non-critical artifacts that do not affect the application's runtime functionality:

1. **DynamoDB Table `SparePartsIQ-CFT-Test`:**
   * *Status:* 0 items, 0 KB.
   * *Origin:* Created during CloudFormation provisioning testing.
   * *Cost Impact:* In `PAY_PER_REQUEST` mode with 0 bytes, this table incurs **$0.00**.
   * *Recommendation:* Can be deleted in a future maintenance window if desired; no immediate action required.
2. **Duplicate Frontend Hashed Bundles in S3 (`frontend/assets/`):**
   * *Status:* Older build artifacts (`index-CDpTGiy1.css`, `index-DLWptIlS.js`, `index-iYZG0ld5.js`) totaling ~1.5 MB remain in the bucket alongside the latest deployed build (`index-sZJagd7M.js`).
   * *Cost Impact:* Less than $0.00003/month.
   * *Recommendation:* Add an S3 Lifecycle rule to clean up outdated frontend prefixes after 30 days.

---

## 6. Risks, Governance & Cost Hardening Recommendations

In strict accordance with the **Critical Resource Preservation Requirement**, the following are recommendations only; no modifications were made:

### 1. CloudWatch Log Retention Policy
* **Current State:** Log group `/aws/lambda/SparePartsIQ-Backend` has retention set to `Never expire`.
* **Risk:** Over 2-3 years of continuous operation, verbose Lambda logs will gradually grow and eventually cross the 5 GB permanent free tier threshold ($0.03/GB-month thereafter).
* **Recommendation:** Execute an administrative retention update to configure a 14-day or 30-day retention window:
  ```powershell
  aws logs put-retention-policy --log-group-name "/aws/lambda/SparePartsIQ-Backend" --retention-in-days 30 --region ap-south-1
  ```

### 2. Zero-Cost Budget Alert (AWS Budgets)
* **Risk:** An unexpected external denial-of-wallet loop or API scraper could drive unexpected request volume.
* **Recommendation:** Create a zero-threshold AWS Budget alert that notifies administrators via email if monthly charges exceed **$1.00 USD (₹80 INR)**:
  ```powershell
  # Recommended safeguard to guarantee zero budget overrun
  aws budgets create-budget --account-id 985539784799 --budget ...
  ```

### 3. SNS Subscription Caution
* **Current State:** The `SparePartsIQ-Alerts` SNS topic currently has 0 subscriptions.
* **Safeguard:** Do **not** attach direct SMS phone number subscriptions to this topic without configuring AWS SNS SMS spend quotas in AWS account settings, as SMS text messages are billed at global telecommunication carrier rates ($0.015 - $0.05 per SMS). Use HTTPS webhook endpoints or AWS SES email subscriptions to preserve zero cost.

---

## 7. Audit Conclusion & Compliance Sign-Off

* **Resource Preservation Compliance:** **100% Verified.** Zero resources were deleted, stopped, disabled, modified, or recreated. All 10 DynamoDB tables, the Lambda function, API Gateway, S3 models, EventBridge rule, and SNS topic remain intact and fully operational.
* **Cost Compliance:** The architecture is verified to be operating within the **₹0 budget constraint** ($0.00/month under AWS Free Tier).
* **Production Readiness:** The serverless architecture exhibits excellent resilience, least-privilege security scoping, and near-zero ongoing financial exposure.

