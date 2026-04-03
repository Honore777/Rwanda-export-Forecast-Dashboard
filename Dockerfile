FROM python:3.11-slim

ARG INSTALL_AI=false
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    TZ=UTC

# Install system dependencies needed for some Python packages and OCR/POPPLER
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       git \
       curl \
       poppler-utils \
       libpoppler-cpp-dev \
       tesseract-ocr \
       pkg-config \
       libgl1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies (core). Optionally install AI extras at build time.
COPY requirements.txt requirements.txt
COPY requirements-ai.txt requirements-ai.txt

RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt \
    && if [ "$INSTALL_AI" = "1" ] || [ "$INSTALL_AI" = "true" ]; then pip install -r requirements-ai.txt; fi

# Copy project files
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
