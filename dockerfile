FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir \
      mcp[cli] \
      yfinance

COPY pkg/server.py /app/server.py

EXPOSE 3001

ENTRYPOINT ["python", "server.py"]
