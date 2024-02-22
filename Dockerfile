FROM python:3.11.6

WORKDIR /app

COPY main.py /app/
COPY storage/data.json /app/storage/
COPY static/error.html /app/static/
COPY static/index.html /app/static/
COPY static/message.html /app/static/
COPY static/style.css /app/static/
COPY static/logo.png /app/static/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]
