FROM python:latest

COPY . .

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "server.py"]
