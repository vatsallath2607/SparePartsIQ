# SparePartsIQ – AWS Deployment Guide

This guide details the steps to reproduce, build, and deploy the SparePartsIQ serverless platform.

---

## 1. Prerequisites & AWS Configuration

1. **AWS CLI:** Version 2.x installed.
2. **Target Region:** `ap-south-1`
3. **IAM Permissions:** Role with permissions for Lambda, S3, DynamoDB, API Gateway, SNS, and EventBridge.

---

## 2. Machine Learning Lambda Packaging

AWS Lambda uses an Amazon Linux environment. Compiled binary extensions (`numpy`, `scipy`, `scikit-learn`) must be downloaded as `manylinux` wheels:

```bash
# Download manylinux cp312 wheels into staging directory:
pip download --only-binary=:all: --platform manylinux2014_x86_64 --python-version 3.12 \
  numpy==2.2.6 scipy==1.16.3 scikit-learn==1.7.2 joblib==1.6.0 threadpoolctl==3.7.0 cloudpickle==3.1.2 \
  -d build/test_wheels
```

### Packaging Script
Run the automated packaging and deployment utility:
```bash
python scripts/package_and_deploy_lambda.py
```

Key rules applied:
- Keep all NumPy files, including `numpy/_core/tests` (required at module load by `array_api_compat`).
- Strip `tests/` directories from `scipy` and `sklearn` to stay within the 250 MB uncompressed limit.
- Total uncompressed size: **216.92 MB** (Limit: 250 MB).
- Compressed archive: **65.51 MB**.

---

## 3. Lambda Deployment

Upload zip to S3 and update Lambda code:
```bash
aws s3 cp build/backend_lambda.zip s3://sparepartsiq-artifacts-985539784799/lambda/backend_lambda.zip --region ap-south-1
aws lambda update-function-code \
  --function-name SparePartsIQ-Backend \
  --s3-bucket sparepartsiq-artifacts-985539784799 \
  --s3-key lambda/backend_lambda.zip \
  --region ap-south-1
aws lambda wait function-updated --function-name SparePartsIQ-Backend --region ap-south-1
```

---

## 4. Frontend Environment Setup

In `frontend/.env`:
```env
VITE_API_URL=https://ug4bzbni58.execute-api.ap-south-1.amazonaws.com/prod
```

Run Vite development server:
```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 3000
```

