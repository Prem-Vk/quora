# Quora

#### Requirements:-
* Python3.10+ ---- (Beacuse latest djangov5.2 is used.)
* PostgreSQL 8.3+
OR
* Docker

## To Setup ats application please follow below steps:
1. Clone the repo using command `git clone https://github.com/Prem-Vk/quora.git`
2. Docker command to run application `docker-compose up`. If you don't have docker installed please continue with step3.
3. Create a env file with this config `postgres://quora:quora@localhost:5432/quoradb`
4. Create & activate virtualenv of python using below command.
	```
	python3.10 -m venv venv && source venv/bin/activate
	```
5. Install python requirements:- `pip install -r requirements.txt`
6. Run sql script to create a database using command:- `psql < setup_postgres.sql`
7. Running Migration `python manage.py migrate` .
8. Run django server `python manage.py runserver 127.0.0.1:8080`.
