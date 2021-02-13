# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')version: '3.7'

x-airflow-environments: &airflow-environments
  ## ----------------
  ## Database
  ## ----------------
  DATABASE_HOST: airflow-postgresql
  DATABASE_PORT: "5432"
  DATABASE_USER: airflow
  DATABASE_DB: airflow
  DATABASE_PASSWORD: airflow
  DATABASE_SQLALCHEMY: "postgresql+psycopg2://airflow:airflow@airflow-postgresql:5432/airflow"

  ## ----------------
  ## Airflow
  ## ----------------
  AIRFLOW__API__AUTH_BACKEND: "airflow.api.auth.backend.deny_all"

  AIRFLOW__CORE__DAG_PROCESSOR_MANAGER_LOG_LOCATION: "/opt/airflow/logs/dag_processor_manager/dag_processor_manager.log"
  AIRFLOW__CORE__EXECUTOR: "LocalExecutor"
  AIRFLOW__CORE__FERNET_KEY: "7T512UXSSmBOkpWimFHIVb8jK6lfmSAvx4mO6Arehnc="
  AIRFLOW__CORE__SQL_ALCHEMY_CONN: "postgresql+psycopg2://airflow:airflow@airflow-postgresql:5432/airflow"
  AIRFLOW__CORE__DAGS_FOLDER: "/opt/airflow/git-sync"
  AIRFLOW__CORE__LOAD_EXAMPLES: "False"
  AIRFLOW__CORE__SECURE_MODE: "True"
  AIRFLOW__CORE__DAG_RUN_CONF_OVERRIDES_PARAMS: "True"

  AIRFLOW__SCHEDULER__CHILD_PROCESS_LOG_DIRECTORY: "/opt/airflow/logs/scheduler"
  AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL: "15"
  AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL: "0"
  AIRFLOW__SCHEDULER__CATCHUP_BY_DEFAULT: "False"

  AIRFLOW__WEBSERVER__BASE_URL: "http://localhost"
  AIRFLOW__WEBSERVER__WEB_SERVER_PORT: "8080"
  AIRFLOW__WEBSERVER__AUTHENTICATE: "True"
  AIRFLOW__WEBSERVER__AUTH_BACKEND: "airflow.contrib.auth.backends.password_auth"
  AIRFLOW__WEBSERVER__COOKIE_SAMESITE: "Lax"

  GUNICORN_CMD_ARGS: --log-level WARNING

  ## ----------------
  ## Airflow - User Configs
  ## ----------------
  AIRFLOW__WEBSERVER__EXPOSE_CONFIG: "True"
  AIRFLOW__WEBSERVER__DEFAULT_DAG_RUN_DISPLAY_NUMBER: "50"
  AIRFLOW__CORE__DAG_CONCURRENCY: "1"
  AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG: "1"
  AIRFLOW__SCHEDULER__MAX_DAGRUNS_PER_LOOP_TO_SCHEDULE: "1"

  # LOGGING
  AIRFLOW__LOGGING__LOGGING_CONFIG_CLASS: "api.loggers.log_config.LOGGING_CONFIG"
  AIRFLOW__LOGGING__DAG_PROCESSOR_MANAGER_LOG_LOCATION: "/opt/airflow/logs/dag_processor_manager/dag_processor_manager.log"
  AIRFLOW__LOGGING__BASE_LOG_FOLDER: "/opt/airflow/logs"
  # ELK
  AIRFLOW__LOGGING__REMOTE_LOGGING: "True"
  AIRFLOW__ELASTICSEARCH__JSON_FORMAT: "True"
  AIRFLOW__ELASTICSEARCH__WRITE_STDOUT: "True"
  AIRFLOW__ELASTICSEARCH__HOST: "http://logging-fluentd-elasticsearch-aws-es-proxy.logging.svc.cluster.local:8080"
  AIRFLOW__ELASTICSEARCH__JSON_FIELDS: "asctime, name, levelname, filename, lineno, message"

  TZ: Etc/UTC
  PYTHONPATH: /opt/airflow/git-sync/airflow:/home/airflow/.local/lib/python3.8/site-packages


services:
  event-tracker-airflow-scheduler:
    image: event-tracker/airflow:dev
    container_name: airflow-scheduller
    depends_on:
      - airflow-postgresql
    environment: *airflow-environments
    ports:
      - 8793:8793
    user: airflow
    volumes:
      - src_airflow_common:/opt/airflow/git-sync/airflow/rc/src:ro
      - airflow_logs:/opt/airflow/logs
      - airflow_scripts:/opt/airflow/variables-pools:ro
      - airflow_scripts:/opt/airflow/connections:ro
    command:
      - "bash"
      - "-c"
      - |
        echo "*** executing Airflow upgradedb..." && airflow db upgrade \
        && echo "*** adding Airflow variables..." && /opt/airflow/variables-pools/add-variables.sh \
        && echo "*** adding Airflow connections..." && /opt/airflow/connections/add-connections.sh \
        && echo "*** running scheduler..." && exec airflow scheduler -n -1
    restart: always

  event-tracker-airflow-web:
    image: event-tracker/airflow:dev
    container_name: airflow-web
    depends_on:
      - airflow-postgresql
      - event-tracker-airflow-scheduler
    environment: *airflow-environments
    user: airflow
    volumes:
      - src_airflow_common:/opt/airflow/git-sync/airflow/rc/src:ro
      - airflow_logs:/opt/airflow/logs:ro
    command:
      - "bash"
      - "-c"
      - |
        echo "Creating user..." && airflow users create --username admin --lastname Tracker --firstname Event --email ivan.podhornyi@megogo.net --role Admin --password admin && \
        echo "Starting webserver..." && exec airflow webserver
    restart: always
    ports:
    - 8080:8080

  airflow-postgresql:
    image: postgres:12.4-alpine
    container_name: airflow-db
    environment:
      POSTGRES_PASSWORD: airflow
      POSTGRES_USER: airflow
      POSTGRES_DB: airflow
    ports:
      - 5432:5432


volumes:
  src_airflow_common:
    driver: local
    driver_opts:
      type: none
      device: "$PWD/api"
      o: bind

  airflow_scripts:
    driver: local
    driver_opts:
      type: none
      device: "$PWD/deployment/airflow/local"
      o: bind

  airflow_logs:
    name: airflow_logs

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
