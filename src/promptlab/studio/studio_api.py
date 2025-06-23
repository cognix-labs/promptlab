from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from promptlab.db.sqlite import SQLAlchemyClient
from promptlab.tracer.tracer import Tracer
from promptlab.types import TracerConfig
from promptlab._utils import Utils
from promptlab.enums import AssetType
from promptlab.db.models import User
import asyncio
import json

# Secret key for JWT (in production, use env var)
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Utility functions

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class StudioApi:
    def __init__(self, tracer: Tracer):
        self.tracer = tracer

        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._setup_routes()

    def get_tracer(self):
        return self.tracer

    async def get_current_user(self, token: str = Depends(oauth2_scheme), tracer: Tracer = Depends(lambda: None)):
        # Use self.tracer if tracer is None (for FastAPI dependency)
        tracer = tracer or self.tracer
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = tracer.db_client.get_user_by_username(username)
        if user is None:
            raise credentials_exception
        return user

    def admin_required(self, current_user: User = Depends(lambda: None)):
        if current_user is None or current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Admin privileges required")
        return current_user

    def _setup_routes(self):
        @self.app.post("/login")
        async def login(form_data: OAuth2PasswordRequestForm = Depends()):
            user = self.tracer.db_client.get_user_by_username(form_data.username)
            if not user or not verify_password(form_data.password, user.password_hash):
                raise HTTPException(status_code=400, detail="Incorrect username or password")
            access_token = create_access_token(data={"sub": user.username, "role": user.role})
            return {"access_token": access_token, "token_type": "bearer", "role": user.role}

        @self.app.post("/users")
        async def create_user(
            request: Request,
            username: str,
            password: str,
            role: str,
            current_user: User = Depends(lambda: self.admin_required(current_user=Depends(lambda: self.get_current_user(tracer=Depends(self.get_tracer)))))
        ):
            if role not in ["admin", "engineer"]:
                raise HTTPException(status_code=400, detail="Invalid role")
            if self.tracer.db_client.get_user_by_username(username):
                raise HTTPException(status_code=400, detail="Username already exists")
            user = User(username=username, password_hash=get_password_hash(password), role=role)
            self.tracer.db_client.add_user(user)
            return {"msg": f"User {username} created"}

        @self.app.get("/me")
        async def get_me(current_user: User = Depends(lambda: self.get_current_user(tracer=Depends(self.get_tracer)))):
            return {"username": current_user.username, "role": current_user.role}

        # Protect all other routes
        @self.app.get("/experiments")
        async def get_experiments(current_user: User = Depends(lambda: self.get_current_user(tracer=Depends(self.get_tracer)))):
            try:
                experiments = await asyncio.to_thread(self.tracer.db_client.get_experiments)
                processed_experiments = []
                for experiment in experiments:
                    system_prompt, user_prompt, _ = Utils.split_prompt_template(experiment.asset_binary)

                    experiment_data = {
                        k: v for k, v in experiment.items() if k != "asset_binary"
                    }
                    experiment_data["system_prompt_template"] = system_prompt
                    experiment_data["user_prompt_template"] = user_prompt

                    processed_experiments.append(experiment_data)
                return {"experiments": processed_experiments}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/prompttemplates")
        async def get_prompt_templates(current_user: User = Depends(lambda: self.get_current_user(tracer=Depends(self.get_tracer)))):
            try:
                prompt_templates = await asyncio.to_thread(self.tracer.db_client.get_assets_by_type, AssetType.PROMPT_TEMPLATE.value)
                processed_templates = []
                for template in prompt_templates:
                    system_prompt, user_prompt, _ = Utils.split_prompt_template(template.asset_binary)
                    experiment_data = {
                        "asset_name": template.asset_name,
                        "asset_description": template.asset_description,
                        "asset_version": template.asset_version,
                        "asset_type": template.asset_type,
                        "created_at": template.created_at,
                        "system_prompt_template": system_prompt,
                        "user_prompt_template": user_prompt,
                        "is_deployed": template.is_deployed,
                        "deployment_time": template.deployment_time,
                    }
                    processed_templates.append(experiment_data)
                return {"prompt_templates": processed_templates}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/datasets")
        async def get_datasets(current_user: User = Depends(lambda: self.get_current_user(tracer=Depends(self.get_tracer)))):
            try:
                datasets = await asyncio.to_thread(self.tracer.db_client.get_assets_by_type, AssetType.DATASET.value)
                processed_datasets = []
                for dataset in datasets:
                    file_path = json.loads(dataset.asset_binary)["file_path"]
                    data = {
                        "asset_name": dataset.asset_name,
                        "asset_description": dataset.asset_description,
                        "asset_version": dataset.asset_version,
                        "asset_type": dataset.asset_type,
                        "created_at": dataset.created_at,
                        "file_path": file_path,
                    }
                    processed_datasets.append(data)
                return {"datasets": processed_datasets}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    def get_app(self):
        return self.app
