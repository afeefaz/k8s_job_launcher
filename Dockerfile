FROM python:3.10-slim
EXPOSE 80
WORKDIR /app
COPY . .
RUN apt update -y && pip install --upgrade pip && pip install -r requirements.txt
CMD python3 main.py