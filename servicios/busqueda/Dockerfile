FROM python:3.9

WORKDIR /app

COPY ./requerimientos.txt /app/requerimientos.txt

RUN pip install -r /app/requerimientos.txt

COPY . /app/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005"]

