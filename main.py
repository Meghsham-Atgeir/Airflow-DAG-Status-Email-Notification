import configparser
from datetime import datetime, timedelta
import airflow_client.client
from rich.console import Console
from airflow_client.client.api import dag_api, dag_run_api, task_instance_api
from airflow_client.client.model.list_dag_runs_form import ListDagRunsForm
from email_sender import send_email

console = Console()

# Read configurations from project.ini
config = configparser.ConfigParser()
config.read('project.ini')

# Configuration parameters
airflow_config = {
    'host': config['Airflow']['host'],
    'username': config['Airflow']['username'],
    'password': config['Airflow']['password']
}

include_success = config.getboolean('Settings', 'include_success')
include_failed = config.getboolean('Settings', 'include_failed')
days_to_check = int(config['Parameters']['days_to_check'])

# Determine states based on parameters
states = ["success", "failed"] if include_success and include_failed else ["success"] if include_success else ["failed"]

# Function to initialize Airflow API client
def initialize_api_client():
    configuration = airflow_client.client.Configuration(
        host=airflow_config['host'], 
        username=airflow_config['username'], 
        password=airflow_config['password']
    )
    return airflow_client.client.ApiClient(configuration)

# Function to get DAG IDs
def get_dag_ids(api_client):
    dag_api_instance = dag_api.DAGApi(api_client)
    api_response = dag_api_instance.get_dags()
    return [dag.dag_id for dag in api_response.dags]

# Function to get DAG runs
def get_dag_runs(api_client, dag_ids):
    list_dag_runs_form = ListDagRunsForm(
        dag_ids=dag_ids,
        states=states,
    )
    dag_run_api_instance = dag_run_api.DAGRunApi(api_client)
    dag_runs_batch = dag_run_api_instance.get_dag_runs_batch(list_dag_runs_form)
    return {dag.dag_run_id: dag.dag_id for dag in dag_runs_batch.dag_runs}

# Function to get task instances
def get_task_instances(api_client, dag_id, dag_run_id):
    task_api_instance = task_instance_api.TaskInstanceApi(api_client)
    response = task_api_instance.get_task_instances(dag_id, dag_run_id)
    return response.task_instances

# Function to fetch task instances for each DAG run
def fetch_task_instances(api_client, dag_runs):
    task_instances_data = []
    for dag_run_id, dag_id in dag_runs.items():
        task_instances = get_task_instances(api_client, dag_id, dag_run_id)
        for task_instance in task_instances:
            task_execution_date = datetime.strptime(task_instance.execution_date, '%Y-%m-%dT%H:%M:%S+00:00')
            if task_execution_date >= datetime.now() - timedelta(days=days_to_check):
                task_instances_data.append([
                    task_instance.dag_id,
                    task_instance.dag_run_id,
                    task_instance.task_id,
                    task_instance.duration,
                    task_instance.execution_date,
                    task_instance.state
                ])
    return task_instances_data

# Main function to orchestrate the process
def main(states):
    api_client = initialize_api_client()
    try:
        dag_ids = get_dag_ids(api_client)
        dag_runs = get_dag_runs(api_client, dag_ids)
        task_instances_data = fetch_task_instances(api_client, dag_runs)
        print(task_instances_data)

        # send_email(task_instances_data, states)

    except airflow_client.client.OpenApiException as e:
        console.print(f"[red]Exception occurred: {e}\n")

if __name__ == "__main__":
    main(states)
