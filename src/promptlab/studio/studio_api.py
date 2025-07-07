import asyncio
import json
import secrets
import os
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import FastAPI, HTTPException, Request, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from promptlab.asset import Asset
from promptlab.tracer.tracer import Tracer
from promptlab.types import Dataset, PromptTemplate
from promptlab._utils import Utils
from promptlab.enums import AssetType


class StudioApi:
    def __init__(self, tracer: Tracer):
        self.tracer = tracer
        self.app = FastAPI()
        # Get SECRET_KEY from environment variable or generate a secure one
        self.SECRET_KEY = os.getenv("PROMPTLAB_SECRET_KEY")
        if not self.SECRET_KEY:
            self.SECRET_KEY = secrets.token_urlsafe(32)
            print(
                "WARNING: Using auto-generated SECRET_KEY. Set PROMPTLAB_SECRET_KEY environment variable for production."
            )
        elif len(self.SECRET_KEY) < 32:
            print(
                "WARNING: SECRET_KEY should be at least 32 characters long for security."
            )
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._setup_routes()

    def _create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.now() + (
            expires_delta or timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def _get_user_role(self, username):
        user = self.tracer.db_client.get_user_by_username(username)
        return user.role if user else None

    def _auth_dependency(self, authorization: str = Header(None)):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        token = authorization.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username = payload.get("sub")
            role = payload.get("role")
            if username is None or role is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return {"username": username, "role": role}
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def _setup_routes(self):
        @self.app.get("/experiments")
        async def get_experiments(auth=Depends(self._auth_dependency)):
            try:
                experiments = await asyncio.to_thread(self.tracer.get_experiments)
                processed_experiments = []
                for experiment in experiments:
                    system_prompt, user_prompt, _ = Utils.split_prompt_template(
                        experiment.asset_binary
                    )

                    experiment_data = {
                        k: v for k, v in experiment.items() if k != "asset_binary"
                    }
                    experiment_data["system_prompt_template"] = system_prompt
                    experiment_data["user_prompt_template"] = user_prompt
                    experiment_data["user_id"] = experiment.get("username", None)

                    processed_experiments.append(experiment_data)
                return {"experiments": processed_experiments}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/prompttemplates")
        async def get_prompt_templates(auth=Depends(self._auth_dependency)):
            try:
                prompt_templates = await asyncio.to_thread(
                    self.tracer.get_assets_by_type, AssetType.PROMPT_TEMPLATE.value
                )
                processed_templates = []
                for template in prompt_templates:
                    system_prompt, user_prompt, _ = Utils.split_prompt_template(
                        template.asset_binary
                    )
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
                        "user_id": template.user.username,
                    }
                    processed_templates.append(experiment_data)
                return {"prompt_templates": processed_templates}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/datasets")
        async def get_datasets(auth=Depends(self._auth_dependency)):
            try:
                datasets = await asyncio.to_thread(
                    self.tracer.get_assets_by_type, AssetType.DATASET.value
                )
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
                        "user_id": dataset.user.username,
                    }
                    processed_datasets.append(data)
                return {"datasets": processed_datasets}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/assets")
        async def get_asset(
            asset_name: str, asset_version: int, auth=Depends(self._auth_dependency)
        ):
            try:
                asset = await asyncio.to_thread(
                    self.tracer.get_asset, asset_name, asset_version
                )
                if not asset:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Asset {asset_name} with version {asset_version} not found",
                    )

                asset_data = {
                    "asset_name": asset.asset_name,
                    "asset_version": asset.asset_version,
                    "asset_description": asset.asset_description,
                    "asset_type": asset.asset_type,
                    "asset_binary": asset.asset_binary,
                    "created_at": asset.created_at.isoformat()
                    if asset.created_at
                    else None,
                    "user_id": asset.user_id,
                    "is_deployed": asset.is_deployed,
                    "deployment_time": asset.deployment_time.isoformat()
                    if asset.deployment_time
                    else None,
                }

                return {"success": True, "asset": asset_data}
            except ValueError as e:
                raise HTTPException(status_code=404, detail=str(e))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/login")
        async def login(request: Request):
            try:
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                data = await request.json()
                username = data.get("username")
                password = data.get("password")
                user = await asyncio.to_thread(
                    self.tracer.get_user_by_username, username
                )
                if user and pwd_context.verify(password, user.password_hash):
                    access_token = self._create_access_token(
                        data={"sub": username, "role": user.role}
                    )
                    return JSONResponse(
                        {
                            "success": True,
                            "access_token": access_token,
                            "token_type": "bearer",
                            "username": username,
                            "role": user.role,
                        }
                    )
                else:
                    return JSONResponse(
                        {"success": False, "message": "Invalid credentials"},
                        status_code=401,
                    )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/users")
        async def get_users(auth=Depends(self._auth_dependency)):
            if auth["role"] != "admin":
                raise HTTPException(status_code=403, detail="Admin access required")
            try:
                users = await asyncio.to_thread(self.tracer.get_users)
                return {
                    "users": [
                        {
                            "id": u.id,
                            "username": u.username,
                            "role": u.role,
                            "created_at": u.created_at.isoformat(),
                        }
                        for u in users
                    ]
                }
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/users")
        async def add_user(request: Request, auth=Depends(self._auth_dependency)):
            if auth["role"] != "admin":
                raise HTTPException(status_code=403, detail="Admin access required")

            try:
                data = await request.json()
                username = data.get("username")
                password = data.get("password")
                role = data.get("role")
                if not username or not password or role not in ("admin", "engineer"):
                    return JSONResponse(
                        {"success": False, "message": "Invalid input"}, status_code=400
                    )
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                password_hash = pwd_context.hash(password)
                from promptlab.sqlite.models import User

                user = User(username=username, password_hash=password_hash, role=role)
                await asyncio.to_thread(self.tracer.create_user, user)
                return JSONResponse({"success": True})
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.delete("/users/{username}")
        async def delete_user(username: str, auth=Depends(self._auth_dependency)):
            if auth["role"] != "admin":
                raise HTTPException(status_code=403, detail="Admin access required")
            try:
                # Don't allow deleting self
                if username == auth["username"]:
                    return JSONResponse(
                        {"success": False, "message": "Cannot delete yourself"},
                        status_code=400,
                    )
                await asyncio.to_thread(
                    self.tracer.deactivate_user_by_username, username
                )
                return JSONResponse({"success": True})
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/experiments")
        async def post_experiment(
            request: Request, auth=Depends(self._auth_dependency)
        ):
            try:
                data = await request.json()
                experiment_config_data = data.get("experiment_config")
                experiment_summary = data.get("experiment_summary")

                if not experiment_config_data or not experiment_summary:
                    return JSONResponse(
                        {
                            "success": False,
                            "message": "Missing experiment_config or experiment_summary data",
                        },
                        status_code=400,
                    )

                from promptlab.types import ExperimentConfig

                experiment_config = ExperimentConfig.model_validate(
                    experiment_config_data
                )

                experiment_config.user = auth["username"]

                # Use the trace_experiment method to properly save to database
                await asyncio.to_thread(
                    self.tracer.trace_experiment, experiment_config, experiment_summary
                )
                return JSONResponse({"success": True})
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/datasets")
        async def create_dataset(dataset: Dataset, auth=Depends(self._auth_dependency)):
            try:
                dataset.user = auth["username"]
                asset = Asset(self.tracer)
                created_dataset = await asyncio.to_thread(asset.create, dataset)

                return JSONResponse(
                    {
                        "success": True,
                        "message": "Dataset created successfully",
                        "dataset": {
                            "name": created_dataset.name,
                            "version": created_dataset.version,
                            "description": created_dataset.description,
                            "file_path": created_dataset.file_path,
                        },
                    }
                )
            except ValueError as e:
                return JSONResponse(
                    {"success": False, "message": str(e)}, status_code=400
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/templates")
        async def create_template(
            template: PromptTemplate, auth=Depends(self._auth_dependency)
        ):
            try:
                template.user = auth["username"]
                asset = Asset(self.tracer)
                created_template = await asyncio.to_thread(asset.create, template)

                return JSONResponse(
                    {
                        "success": True,
                        "message": "Prompt template created successfully",
                        "template": {
                            "name": created_template.name,
                            "version": created_template.version,
                            "description": created_template.description,
                            "system_prompt": created_template.system_prompt,
                            "user_prompt": created_template.user_prompt,
                        },
                    }
                )
            except ValueError as e:
                return JSONResponse(
                    {"success": False, "message": str(e)}, status_code=400
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    def get_app(self):
        return self.app
