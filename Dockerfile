FROM python:latest

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8501

CMD ["python", "server.py"]
