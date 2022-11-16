from typing import Optional, List
from sqlmodel import Field, SQLModel, JSON, Column
from sqlalchemy import UniqueConstraint


class UserBase(SQLModel):
    __table_args__ = (UniqueConstraint("username"),)
    username: str = Field(None, title="Username único do usuário", max_length=20, index=True)
    full_name: str = Field(None, title="Nome completo do usuário")
    email: str = Field(None, title="E-mail do usuário", index=True)
    disable: Optional[bool] = Field(default=False, title="Status de usuário ativo ou inativo")
    hashed_password: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class UserRead(UserBase):
    id: int


class UserCreate(UserBase):
    pass


class ToolBase(SQLModel):
    __table_args__ = (UniqueConstraint("title", "link"),)
    title: str = Field(None, title="Nome da ferramenta", max_length=20)
    link: str = Field(None, title="Link da documentação da ferramenta")
    description: str = Field(None, title="Descrição da ferramenta")
    tags: List[str] = Field(sa_column=Column(JSON),
                            title="Tags relacionadas a ferramenta. Devem ser enviadas separadas por ';'", index=True)


class Tool(ToolBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ToolRead(ToolBase):
    id: int


class ToolCreate(ToolBase):
    pass


class ToolUpdate(SQLModel):
    tags: List[str] = None
