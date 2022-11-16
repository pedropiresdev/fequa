import logging
import sqlite3
from typing import Optional

from app.model.models import Tool
from app.server_mock import MockService

# local_db = "staging_db.sqlite"


class DBConnection:
    def __init__(self):
        """
        Cria e popula a tabela de Ferramentas (tools)
        """
        # self.conn = self.create_connection(local_db)
        # self.create_table()
        # self.load_tools_data(MockService.tools_data)
        # self.load_users_data(MockService.users_data)

    @staticmethod
    def create_connection(db_name):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_name: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_name)
            logging.info(f"Conexão criada com sucesso com o banco {db_name}")

        except Exception as e:
            logging.info(f'Falha ao tentar conectar ao banco {db_name}. Erro --> {e}')

        return conn

    def create_table(self):
        """
        Cria a tabela 'tools' caso não exista.
        """
        sql_statements = [
            """
                CREATE TABLE IF NOT EXISTS tools (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    description TEXT NOT NULL,
                    tags TEXT,
                    UNIQUE (title, link)
                    )
            """,
            """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    hashed_password TEXT NOT NULL,
                    disable INTEGER DEFAULT 1)
            """

        ]
        try:
            with self.conn as con:
                for statement in sql_statements:
                    con.execute(statement)
                    logging.info("Tabela criada com sucesso")

        except Exception as e:
            logging.info(f'Falha ao tentar criar tabela. Erro --> {e}')

    def load_tools_data(self, data: list):
        """ Popula a tabela tools com dados pré-definidos.
        :param data: Lista de dicionários do tipo Ferramenta
        """
        for indice, tool in enumerate(data):
            if tool.get("tags"):
                tags_to_string = '_'.join(map(str, tool["tags"]))
                data[indice].update({"tags": tags_to_string})

        sql = """
            INSERT OR IGNORE INTO tools VALUES(
                NULL,
                :title, 
                :link, 
                :description, 
                :tags
                )
        """
        try:
            with self.conn as con:
                con.executemany(sql, data)
                con.commit()

                logging.info("Tabela de ferramentas populada com sucesso!!!")

        except Exception as e:
            logging.info(f'Falha ao tentar popular tabela de ferramentas. Erro --> {e}')

    def load_users_data(self, data: list):
        """ Popula a tabela users com dados pré-definidos.
        :param data: Lista de dicionários do tipo Ferramenta
        """
        sql = """
            INSERT OR IGNORE INTO users VALUES(
                NULL,
                :username, 
                :full_name, 
                :email, 
                :hashed_password,
                :disable
                )
            """
        try:
            with self.conn as con:
                con.executemany(sql, data)
                con.commit()
                logging.info("Tabela de usuários populada com sucesso!!!")

        except Exception as e:
            logging.info(f'Falha ao tentar popular tabela de usuários. Erro --> {e}')

    def insert_tool(self, data: Tool):
        """ Insere no banco uma ferramenta e retorna a
        ferramenta cadastrada com o ID.
        :param data: List[dict] - lista de ferramentas sem ID
        :return: List[dict] - lista de ferramentas com ID
        """
        item = dict(data)
        item.update({"tags": '_'.join(map(str, item["tags"]))})
        sql = """
            INSERT INTO tools VALUES(
                NULL,
                :title, 
                :link, 
                :description, 
                :tags
                ) RETURNING *
            """
        try:
            cur = self.conn.cursor()
            cur.execute(sql, item)
            if result := cur.fetchone():
                _id, title, link, description, tags = result
                tool = {
                    "id": _id,
                    "title:": title,
                    "link:": link,
                    "description:": description,
                    "tags:": tags.split("_"),
                }
                logging.info("Ferramenta inserida com sucesso")
                return tool

        except Exception as e:
            logging.info(f'Falha ao tentar inserir ferramenta. Erro --> {e}')

    def get_tool_by_id(self, tool_id: int):
        """ Consulta uma ferramenta pelo seu id.
        :param tool_id: id da ferramenta
        :return: Dados da ferramenta ou None.
        """
        sql = f"""
            SELECT *
            FROM tools
            WHERE id = {tool_id}
            """
        try:

            cur = self.conn.cursor()
            cur.execute(sql)
            if result := cur.fetchone():
                _id, title, link, description, tags = result
                tool = {
                    "id": _id,
                    "title:": title,
                    "link:": link,
                    "description:": description,
                    "tags:": tags.split("_"),
                }
                logging.info("Consulta de ferramenta por id realizada com sucesso")
                return tool

        except Exception as e:
            logging.info(f'Falha ao tentar consultar ferramenta por id. Erro --> {e}')

    def get_tools_by_tag(self, tag: str):
        """ Consulta ferramentas que possuam uma tag específica.
        :param tag: tag da ferramenta
        :return: Dados da ferramenta ou None.
        """
        sql = f"""
            SELECT *
            FROM tools
            WHERE tags LIKE '%{tag}%'
            """
        try:

            cur = self.conn.cursor()
            cur.execute(sql)
            if result := cur.fetchall():
                tools = []
                for item in result:
                    _id, title, link, description, tags = item
                    tools.append({
                        "id": _id,
                        "title:": title,
                        "link": link,
                        "description:": description,
                        "tags:": tags.split("_"),
                    })

                logging.info("Consulta de ferramentas por tag realizada com sucesso")
                return tools

        except Exception as e:
            logging.info(f'Falha ao tentar consultar ferramenta por tag. Erro --> {e}')

    def delete_tool_by_id(self, tool_id: int) -> Optional[dict]:
        """ Remove uma ferramenta à partir do ID.
        :param tool_id: ID da ferramenta
        :return: None.
        """
        sql = f"""
            DELETE
            FROM tools
            WHERE id = {tool_id}
            """
        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            logging.info(f"Ferramenta de id {tool_id} removida com sucesso")
            return {}

        except Exception as e:
            logging.info(f'Falha ao tentar consultar ferramenta por tag. Erro --> {e}')

    def get_tools(self):
        """ Consulta todas as ferramentas cadastradas no banco.
        :return: Ferramentas ou None.
        """
        sql = f"""
            SELECT *
            FROM tools
            """

        try:
            cur = self.conn.cursor()
            cur.execute(sql)
            if result := cur.fetchall():
                tools = []
                for item in result:
                    _id, title, link, description, tags = item
                    tools.append({
                        "id": _id,
                        "title:": title,
                        "link": link,
                        "description:": description,
                        "tags:": tags.split("_"),
                    })

                logging.info("Consulta de ferramenta realizada com sucesso")
                return tools

        except Exception as e:
            logging.info(f'Falha ao tentar consultar ferramenta. Erro --> {e}')

    def get_user(self, username):
        """ Consulta usuário pelo seu username.
        :param username: id da ferramenta
        :return: Dados da ferramenta ou None.
        """
        sql = f"""
            SELECT *
            FROM users
            WHERE username = {username}
        """
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql)
                if result := cur.fetchone():
                    logging.info("Consulta de usuário realizada com sucesso")
                    return result

        except Exception as e:
            logging.info(f'Falha ao tentar consultar usuário. Erro --> {e}')
