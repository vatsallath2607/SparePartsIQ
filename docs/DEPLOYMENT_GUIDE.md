# SparePartsIQ AWS Deployment & IAM Guide

## 1. AWS Cloud Resources Overview
All infrastructure is deployed in region **`ap-south-1`** using the project profile **`antigravity-project`**.

### Deployed AWS Resources
- **Amazon S3:** `sparepartsiq-artifacts-985539784799` (Encrypted, public access blocked).
  - Model artifacts: `s3://sparepartsiq-artifacts-985539784799/models/`
  - Lambda packages: `s3://sparepartsiq-artifacts-985539784799/lambda/backend_lambda.zip`
  - Static frontend assets: `s3://sparepartsiq-artifacts-985539784799/frontend/`
- **Amazon DynamoDB:** 9 ACTIVE on-demand tables:
  1. `SparePartsIQ-Users`
  2. `SparePartsIQ-SpareParts`
  3. `SparePartsIQ-InventoryTransactions`
  4. `SparePartsIQ-MaintenanceSchedules`
  5. `SparePartsIQ-Suppliers`
  6. `SparePartsIQ-PurchaseOrders`
  7. `SparePartsIQ-ForecastResults`
  8. `SparePartsIQ-ReorderRecommendations`
  9. `SparePartsIQ-Notifications`
- **Amazon SNS:** `arn:aws:sns:ap-south-1:985539784799:SparePartsIQ-Alerts`
- **Amazon EventBridge:** `arn:aws:events:ap-south-1:985539784799:rule/SparePartsIQ-DailyForecastingRule`
- **Amazon API Gateway:** RestApi ID `ug4bzbni58` (`SparePartsIQ-API`)

---

## 2. IAM Permission Analysis & Smallest Required IAM Change

During testing of direct `lambda:CreateFunction` execution, the role:
`arn:aws:iam::985539784799:role/Antigravity-SparePartsIQ-Role`
encountered an `AccessDenied` error for the action `iam:PassRole`.

### Exact Missing IAM Action:
`iam:PassRole`

### Smallest Required Permission Statement:
To allow Lambda creation with `Antigravity-SparePartsIQ-Role` as its execution role, attach the following minimal inline policy statement to the role:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::985539784799:role/Antigravity-SparePartsIQ-Role"
    }
  ]
}
```

Once this permission statement is appended, CloudFormation / AWS CLI can automatically bind the existing execution role to `SparePartsIQ-BackendHandler`.

---

## 3. Local Development & Testing Instructions

### Running Backend:
```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

### Running Frontend:
```powershell
cd frontend
npm run preview -- --port 3000 --host 0.0.0.0
```

### Running Automated Test Suite:
```powershell
python -m pytest tests/test_backend.py -v
```

---

## 4. Cost Considerations & Assumptions
- **DynamoDB:** `PAY_PER_REQUEST` billing mode ensures **$0.00 base cost** when idle.
- **S3 Storage:** Low storage footprint (< 50 MB total for models, datasets, frontend assets) within AWS free tier limits.
- **SNS:** Standard tier allows 1,000,000 free requests per month.
- **No EC2 or NAT Gateways:** Strict zero-EC2 policy strictly adhered to.

