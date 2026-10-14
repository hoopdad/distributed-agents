FROM python:3.13-slim@sha256:8d9d0b8bcf6506481eae4907c18f5e3e7902e629f5f6d684f9e7c32e85e3ddf0
ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_INDEX_URL=https://packagefeedproxy.microsoft.io/pypi/simple \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.lock.txt .
RUN python -m pip install --requirement requirements.lock.txt
COPY demo demo
COPY config/routing-corpus.json config/routing-calibration.json config/
COPY scripts/calibrate_routing.py scripts/calibrate_routing.py
EXPOSE 8088
CMD ["python", "-m", "demo.host"]
