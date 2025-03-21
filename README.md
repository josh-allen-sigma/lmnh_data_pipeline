# LMNH Data Pipeline

This folder should contain all code, documentation and resources required for the LMNH data pipeline.

## Project Context

The Liverpool Museum of Natural History (LMNH) welcomes hundreds of thousands of visitors annually to its award-winning exhibitions. Committed to serving the community, LMNH collects visitor feedback to improve exhibitions. Traditionally using surveys and reviews, the museum is now trialing "Smiley Face Survey Kiosks" at key exhibitions, allowing visitors to rate their experience and request assistance. While the kiosks are operational, the data is not yet being utilized. LMNH aims to develop an automated system to collect, store, and analyze this data in real time for better operational insights.

## The Solution 

A cloud based data pipeline was developed for LMNH, the pipeline used a variety of technologies including Kafka, AWS EC2, AWS RDS Postgresql and Tableau.

Please find an architecture diagram of the pipeline below:
![Architecture Diagram](architecture-diagram.png)

## File Explanation 

### .venv
It's a good idea to first create and activate a virtual environment, you can do this by running the following commands:
- python3 -m venv .venv
- source .venv/bin/activate

### requirements.txt
Before running the script, in order to ensure all necessary packages are installed run the following command in the terminal:
- pip3 install -r requirements.txt

### .env
An .env file containing the following details (fill the blanks '=      ') will need to be created:
For your target RDS:
- DATABASE_USERNAME=
- DATABASE_PASSWORD=
- DATABASE_PORT=5432
- DATABASE_NAME="
- DATABASE_IP=

For your target kafka stream:
- BOOTSTRAP_SERVERS=
- SECURITY_PROTOCOL=
- SASL_MECHANISM=
- USERNAME=
- PASSWORD=
- GROUP=

AWS access
- aws_access_key_id=
- aws_secret_access_key=

### lmnh_etl.py file
This etl script consumes messages from kafka, validates them and transforms them before loading them into a AWS RDS. This script also comes equipped with a command line interface:

CLI:
- "-t", "--topic", default="lmnh", help="Choose the consumers topic 'lmnh' is the default" - optional argument
- "-f", "--filename", default="errors.txt", help="Choose an output filename - default is errors.txt" - optional argument
- "-l", "--log_destination", default="terminal", help="Choose to log errors to a 'file' or 'terminal'" - optional argument

It is not necessary to enter any cli arguments to run the script unless you want to modify one of the cli inputs as explained in CLI.

### Tableau Dashboard
PNGs of the wireframe dashboard concepts and the actual Tableau dashboards can be found in the Dashboard directory.

### Terraform Setup
The terraform resources including security groups, an ec2 instance and an rds were set up using the main scripts in the ec2_terraform_config and rds_terraform_config files.

### db_clear.bash
To clear the database before running the lmnh_etl.py script run the db_clear.bash file using 'bash db_clear.bash' this will reset the database but keep the static information e.g exhibitions, floors, rating values etc.

### db_connect.bash
To connect to the database run 'bash db_connect.bash'.

### ec2-connect.bash
To connect to the ec2 instance run 'bash ec2_connect.bash'.

Some very basic pytests were carried out to ensure transform functions were working as intended.

