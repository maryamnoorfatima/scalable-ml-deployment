FROM apache/airflow:2.7.1

USER airflow

# Create a requirements file directly in the container
RUN echo "scikit-learn==1.2.2" > /tmp/requirements.txt && \
    echo "pandas==1.5.3" >> /tmp/requirements.txt && \
    echo "numpy==1.23.5" >> /tmp/requirements.txt && \
    echo "mlflow==2.3.1" >> /tmp/requirements.txt && \
    echo "seaborn==0.12.2" >> /tmp/requirements.txt && \
    echo "matplotlib==3.7.1" >> /tmp/requirements.txt && \
    echo "joblib==1.2.0" >> /tmp/requirements.txt

# Install as airflow user
RUN pip install --user -r /tmp/requirements.txt

WORKDIR /opt/airflow 