FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV DATABASE_URL=sqlite:///./data/catalog.db
# Ensure Python can import the src package
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/

# copy entrypoint
COPY entrypoint.sh /app/entrypoint.sh
# install curl and ensure entrypoint uses LF line endings, make executable
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i 's/\r$//' /app/entrypoint.sh \
    && chmod +x /app/entrypoint.sh

EXPOSE 8080

# Run entrypoint which seeds DB (idempotent) then execs uvicorn so /health is served on port 8080
ENTRYPOINT ["/app/entrypoint.sh"]