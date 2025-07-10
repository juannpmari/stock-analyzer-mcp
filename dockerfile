FROM python:3.10-slim

WORKDIR /app

COPY src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY src/server.py /app/server.py
COPY src/tools /app/tools

ENTRYPOINT ["python", "server.py"]
