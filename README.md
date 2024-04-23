
# Airflow DAG Monitoring and Email Notification Script

This repository contains scripts to monitor Apache Airflow DAG runs and send email notifications about their status.
Based on the essential parameters in project.ini

## Installation

1. Clone the repository to your local machine:

```bash
git clone <repository_url>
```

2. Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Configuration

1. Configure the `project.ini` file:

    - **Airflow Configuration**: Set the `host`, `username`, and `password` parameters under the `[Airflow]` section to connect to your Airflow instance.
    
    - **Settings**: Set `include_success` and `include_failed` to `True` or `False` based on whether you want to include successful or failed DAG runs in the email notification.
    
    - **Email Configuration**: Configure the SMTP server (`smtp_server`), SMTP port (`smtp_port`), sender email address (`sender_email`), sender email password (`sender_password`), and receiver email addresses (`receivers`).

    - **Parameters**: Set the `days_to_check` parameter to specify the number of days to check DAG runs.

2. Customize the `send_email.py` script if necessary:

    - Modify the email content or formatting in the `send_email` function as needed.

3. Run the `main.py` script:

```bash
python main.py
```

This script fetches information about DAG runs from the Airflow instance, filters them based on the specified criteria, and sends an email notification with the relevant information.

## Usage

- Ensure that the Airflow instance is running and accessible at the specified URL.
- Run the `main.py` script to fetch DAG run information and send email notifications based on the configured settings.

## Example

Here's an example `project.ini` configuration:

```ini
[Airflow]
host = http://localhost:8080/api/v1
username = my_username
password = my_password

[Settings]

include_success = False 
include_failed = True

[Email]
smtp_server = smtp.gmail.com
smtp_port = 587
sender_email = my_email@gmail.com
sender_password = my_email_password
receivers = recipient1@example.com, recipient2@example.com

[Parameters]
days_to_check = 7
```

This configuration will connect to a local Airflow instance, include failed DAG runs in the email notifications, use Gmail's SMTP server for sending emails, and check DAG runs for the last 7 days.


This `README.md` file provides instructions on how to install, configure, and use the scripts for monitoring Apache Airflow DAG runs and sending email notifications. You may need to adjust the instructions or add more details based on your specific use case. If you have any questions or need further assistance, feel free to ask!
