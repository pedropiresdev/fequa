import os

ENV = os.getenv("ENV", "local")


if ENV != "production":
    path_db = "app/db/staging/db.sqlite"
    echo = True

else:
    path_db = "app/db/production/db.sqlite"
    echo = False
