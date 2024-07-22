FROM python:3.12

RUN mkdir /src

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD uvicorn src.main:app --host=0.0.0.0 --port=8000 --workers=4
