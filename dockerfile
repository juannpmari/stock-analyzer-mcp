# Use Python 3.10 as the base image for broad compatibility
FROM python:3.10-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Install Node.js (for npx) and system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g @modelcontextprotocol/inspector@0.15.0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app


# Copy requirements and install Python dependencies
COPY mcp-server/requirements.txt ./requirements.txt
# Install uv (modern Python package manager)
RUN pip install --upgrade pip && pip install uv

# Create a uv-managed virtual environment and install Python dependencies inside it
# Copy the rest of the code
COPY mcp-server/ ./mcp-server/

# Expose the port the server runs on
EXPOSE 3001

# Set the default command to activate the venv and run the server with mcp dev
# CMD bash -c 'uv venv && \
#   . .venv/bin/activate && \
#   uv pip install "mcp[cli]" && \
#   uv pip install yfinance && \
#   npx @modelcontextprotocol/inspector uv run /app/mcp-server/yf_server.py'

ENTRYPOINT ["bash", "-c", "uv venv && . .venv/bin/activate && uv pip install \"mcp[cli]\" && uv pip install yfinance && npx @modelcontextprotocol/inspector uv run /app/mcp-server/yf_server.py"]
# Default arguments for ENTRYPOINT
CMD ["stdio"]