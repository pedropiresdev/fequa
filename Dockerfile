# pull official base image
FROM python:3.10.7

## set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

# copy project
COPY . /app

RUN chmod +x ./run.sh
CMD ["./run.sh"]
