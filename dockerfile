FROM python:3.10-slim

WORKDIR /app

COPY pkg/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY pkg/server.py /app/server.py
COPY pkg/tools /app/tools

ENTRYPOINT ["python", "server.py"]
