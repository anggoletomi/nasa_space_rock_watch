#!/bin/bash
set -e

echo "[1/5] Checking environment variables..."
echo "AIRFLOW__CORE__FERNET_KEY=${AIRFLOW__CORE__FERNET_KEY}"
echo "POSTGRES_HOST=${POSTGRES_HOST}"
echo "POSTGRES_PORT=${POSTGRES_PORT}"
echo "POSTGRES_DB=${POSTGRES_DB}"
echo "POSTGRES_USER=${POSTGRES_USER}"

echo "[2/5] Checking connectivity with 'airflow db check'..."
airflow db check || {
  echo "Postgres not ready, exiting."
  exit 1
}

echo "[3/5] 'airflow db init'..."
airflow db init

echo "[4/5] Creating user..."
airflow users create \
  --username "${AIRFLOW_USERNAME}" \
  --password "${AIRFLOW_PASSWORD}" \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \

echo "[5/5] Start webserver & scheduler"
airflow webserver --port 8080 &
exec airflow scheduler