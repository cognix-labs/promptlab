from fastapi import FastAPI, HTTPException, Request, Response, Depends, Cookie
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from promptlab.db.sql import SQLQuery
from promptlab.tracer.tracer import Tracer
from promptlab.types import TracerConfig
from promptlab._utils import Utils
from promptlab.enums import AssetType
import asyncio
import json
import secrets
from passlib.context import CryptContext

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

    def _auth_dependency(self, session_token: str = Cookie(default=None)):
        if not session_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        # In production, validate token from DB or memory
        # For now, just check presence
        return True

    def _setup_routes(self):
        @self.app.get("/experiments")
        async def get_experiments(auth=Depends(self._auth_dependency)):
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
                    experiment_data["user_id"] = experiment.get("user_id", None)

                    processed_experiments.append(experiment_data)
                return {"experiments": processed_experiments}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/prompttemplates")
        async def get_prompt_templates(auth=Depends(self._auth_dependency)):
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
                        "user_id": template.user_id,
                    }
                    processed_templates.append(experiment_data)
                return {"prompt_templates": processed_templates}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/datasets")
        async def get_datasets(auth=Depends(self._auth_dependency)):
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
                        "user_id": dataset.user_id,
                    }
                    processed_datasets.append(data)
                return {"datasets": processed_datasets}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/login")
        async def login(request: Request):
            try:
                pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
                data = await request.json()
                username = data.get("username")
                password = data.get("password")
                # Fetch user from DB
                user = await asyncio.to_thread(self.tracer.db_client.get_user_by_username, username)
                if user and pwd_context.verify(password, user.password_hash):
                    token = secrets.token_hex(16)
                    # In production, store token in DB or memory
                    response = JSONResponse({"success": True, "token": token, "username": username})
                    response.set_cookie(key="session_token", value=token, httponly=True)
                    return response
                else:
                    return JSONResponse({"success": False, "message": "Invalid credentials"}, status_code=401)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/logout")
        async def logout(response: Response, auth=Depends(self._auth_dependency)):
            response = JSONResponse({"success": True})
            response.delete_cookie(key="session_token")
            return response

    def get_app(self):
        return self.app
