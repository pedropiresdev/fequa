from sqlmodel import create_engine, SQLModel
from app.model.models import Tool, User
from app.utils import path_db, echo
from sqlmodel import Session, select, col
from fastapi import HTTPException
import os


connect_args = {"check_same_thread": False}  # Evitar utilizar a mesma sessão em mais de uma request
if os.path.exists(path_db):
    sqlite_url = os.path.join(f"sqlite:///{path_db}")
else:
    sqlite_url = "sqlite:///./staging/db.sqlite"

engine = create_engine(sqlite_url, echo=echo, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def create_tool(tool):
    with Session(engine) as session:
        db_tool = Tool.from_orm(tool)
        db_tool.tags.sort()
        session.add(db_tool)
        session.commit()
        session.refresh(db_tool)
        return db_tool


def create_user(user):
    with Session(engine) as session:
        db_user = User.from_orm(user)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def read_tools():
    with Session(engine) as session:
        tools = session.exec(select(Tool)).all()
        if not tools:
            raise HTTPException(status_code=404, detail="No tools found")

        return tools


def read_tools_by_id(tool_id: int):
    with Session(engine) as session:
        tool = session.get(Tool, tool_id)
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")

        return tool


def read_tools_by_tag(tool_tag: str):
    with Session(engine) as session:
        tools = session.exec(select(Tool).where(col(Tool.tags).contains(tool_tag))).all()
        return tools


def delete_tool_by_id(tool_id: str):
    with Session(engine) as session:
        tool = session.get(Tool, tool_id)
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")

        session.delete(tool)
        session.commit()
        return {}


def add_tags_by_id(tool_id, tool):
    with Session(engine) as session:
        db_tool = session.get(Tool, tool_id)
        if not db_tool:
            raise HTTPException(status_code=404, detail="Tool not found")

        db_tool.tags.extend(tool.tags)
        db_tool.tags.sort()
        session.add(db_tool)
        session.commit()
        session.refresh(db_tool)
        return db_tool
