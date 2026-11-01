from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid
from backend.config import TABLE_USERS
from backend.db import dynamodb, decimal_to_native, native_to_decimal
from backend.auth import verify_password, get_password_hash, create_access_token, get_current_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class CreateUserRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str  # "Inventory Manager", "Maintenance Team", "Purchase Manager"
    department: str

@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    table = dynamodb.Table(TABLE_USERS)
    # Query by EmailIndex GSI
    res = table.query(
        IndexName="EmailIndex",
        KeyConditionExpression="email = :email",
        ExpressionAttributeValues={":email": req.email}
    )
    items = res.get("Items", [])
    if not items:
        # Fallback scan in case GSI has eventual consistency
        scan_res = table.scan()
        for item in scan_res.get("Items", []):
            if item.get("email") == req.email:
                items = [item]
                break
                
    if not items:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    user = decimal_to_native(items[0])
    if not verify_password(req.password, user.get("password_hash", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
        
    token = create_access_token(data={"sub": user["user_id"], "email": user["email"], "role": user["role"]})
    user_data = {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "department": user.get("department", "")
    }
    return LoginResponse(access_token=token, user=user_data)

@router.get("/me")
def get_current_user_profile(user: dict = Depends(get_current_user)):
    return {
        "user_id": user["user_id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"],
        "department": user.get("department", "")
    }

@router.get("/users")
def list_users(user: dict = Depends(get_current_user)):
    table = dynamodb.Table(TABLE_USERS)
    res = table.scan()
    users = decimal_to_native(res.get("Items", []))
    for u in users:
        u.pop("password_hash", None)
    return users

