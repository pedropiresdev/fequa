import base64
import json
import logging
from fastapi import FastAPI
from fastapi import APIRouter, Request, status
from sqlmodel import Session, select

from app.business.api import rpc_request
from app.model.models import User, Tool, ToolRead, ToolUpdate, ToolCreate, UserRead, UserCreate, ToolBase
from app.db import db

from app.settings import PROXY_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=f"FEQUA", root_path=PROXY_PATH)

router = APIRouter()
# db = DBConnection()


@app.post("/tools/insert_item/", response_model=ToolRead)
async def create_tool(_tool: ToolCreate):
    tool = db.create_tool(_tool)
    return tool


@app.post("/users/insert_item/", response_model=UserRead)
async def create_user(_user: UserCreate):
    action = "save_credentials"
    user_credentials = db.create_user(_user)
    if not user_credentials:
        logging.info(f"Não foi possível cadastrar o usuário {_user.username}")
        return

    rpc_service = "user_auth"
    message = json.dumps(user_credentials.dict())
    message_bytes = message.encode('utf-8')
    settings_bytes = base64.b64encode(message_bytes)
    breakpoint()
    rpc_request(settings_bytes.decode("utf-8"), rpc_service, action)


@app.get("/tools/")
async def read_tools():
    tools = db.read_tools()
    return tools


@app.get("/tools/id/{tool_id}")
async def read_tools_by_id(tool_id: int):
    tools = db.read_tools_by_id(tool_id)
    return tools


@app.get("/tools/tag/{tool_tag}")
async def read_tools_by_tag(tool_tag: str):
    tools = db.read_tools_by_tag(tool_tag)
    return tools


@app.patch("/tools/{tool_id}", response_model=ToolRead)
async def add_tags_by_id(tool_id: int, _tool: ToolUpdate):
    tool = db.add_tags_by_id(tool_id, _tool)
    return tool



# @app.get("/tools", status_code=status.HTTP_202_ACCEPTED)
# async def get_all_tools():
#     data = db.get_tools()
#     return data
#
# @app.get("/tools/get_tools_id/{id}")
# async def get_tools_by_id(tool_id: int):
#     data = db.get_tool_by_id(tool_id)
#     return data
#
# @app.get("/tools/get_tools_tag/{tag}")
# async def _get_tools_by_tag(tag: str):
#     data = db.get_tools_by_tag(tag)
#     return data
#
# @app.delete("/tools/{tools_id}")
# async def _remove_tool(tool_id: int):
#     data = db.delete_tool_by_id(tool_id)
#     return data

