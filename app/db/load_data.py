from app.model import models
from app.db.db import engine, create_db_and_tables
from sqlmodel import Session
from app.server_mock import MockService


def load_users_and_tools_data():
    with Session(engine) as session:
        for tool in MockService.tools_data:
            tool_model = models.Tool(
                title=tool["title"],
                link=tool["link"],
                description=tool["description"],
                tags=tool["tags"],
            )
            session.add(tool_model)

        for user in MockService.users_data:
            user_model = models.User(
                username=user["username"],
                full_name=user["full_name"],
                email=user["email"],
                disable=user["disable"],
                hashed_password=user["hashed_password"],
            )
            session.add(user_model)
        session.commit()


if __name__ == "__main__":
    create_db_and_tables()
    load_users_and_tools_data()
