FROM apache/airflow:2.7.1

USER root

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        python3-pip \
        git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Copy and install requirements from project root
COPY ../requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

WORKDIR /app

COPY . .

COPY src/ src/
COPY models/ models/

EXPOSE 8000

CMD ["python", "src/app.py"] 