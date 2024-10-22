FROM python:3.12-alpine3.20

RUN pip install poetry==1.8.3

WORKDIR /app

COPY . ./

RUN poetry install

EXPOSE 5000

CMD [ "poetry", "run", "python", "server.py" ]