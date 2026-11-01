"""
Packages the backend and ML inference modules into a Lambda deployment archive
and uploads it to Amazon S3.
"""
import os
import zipfile
import boto3

def make_lambda_zip(zip_filename="backend_lambda.zip"):
    print(f"Creating Lambda deployment archive: {zip_filename}...")
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as z:
        # Add backend
        for root, dirs, files in os.walk("backend"):
            for f in files:
                if not f.endswith(".pyc") and "__pycache__" not in root:
                    file_path = os.path.join(root, f)
                    arcname = file_path
                    z.write(file_path, arcname)
                    
        # Add ML models and data
        for root, dirs, files in os.walk("ml"):
            for f in files:
                if not f.endswith(".pyc") and "__pycache__" not in root:
                    file_path = os.path.join(root, f)
                    arcname = file_path
                    z.write(file_path, arcname)
                    
        for root, dirs, files in os.walk("data"):
            for f in files:
                file_path = os.path.join(root, f)
                z.write(file_path, file_path)
                
    print(f"Archive {zip_filename} created. Size: {os.path.getsize(zip_filename) / 1024:.1f} KB")
    
    # Upload to S3
    session = boto3.Session(profile_name='antigravity-project', region_name='ap-south-1')
    s3 = session.client('s3')
    bucket = "sparepartsiq-artifacts-985539784799"
    s3.upload_file(zip_filename, bucket, "lambda/backend_lambda.zip")
    print(f"Uploaded to s3://{bucket}/lambda/backend_lambda.zip")

if __name__ == "__main__":
    make_lambda_zip()

