# Quora

#### Requirements:-
* Python3.10+ ---- (Beacuse latest djangov5.2 is used.)
* PostgreSQL 8.3+

## To Setup ats application please follow below steps:
1. Clone the repo using command `git clone https://github.com/Prem-Vk/quora.git`
2. Create a env file with this config `postgres://quora:quora@localhost:5432/quoradb`
3. Create & activate virtualenv of python using below command.
	```
	python3.10 -m venv venv && source venv/bin/activate
	```
4. Install python requirements:- `pip install -r requirements.txt`
5. Run sql script to create a database using command:- `psql < setup_postgres.sql`
6. Running Migration `python manage.py migrate` .
7. Run django server `python manage.py runserver 127.0.0.1:8080`.
