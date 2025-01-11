```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y python3 python3-dev python3-pip virtualenv
sudo apt-get install -y ffmpeg postgresql git gh
```

# DB - enter manually
```bash
sudo vi /etc/postgresql/14/main/pg_hba.conf
sudo systemctl restart postgresql
sudo systemctl status postgresql
sudo passwd postgres
su - postgres
createdb sgcdev
createuser -P sgc
psql
GRANT ALL PRIVILEGES ON DATABASE sgc TO sgc;
ALTER ROLE sgc SET client_encoding TO 'UTF8';
ALTER ROLE sgc SET default_transaction_isolation TO 'read committed';
ALTER ROLE sgc SET timezone TO 'UTC';
\q
exit
```

# Env
```bash
gh auth login   
gh repo clone acrawford73/sgc-media

virtualenv -p /usr/bin/python3 sgc-media
cd sgc-media/
source bin/activate
pip install -r requirements.txt

cd src
mkdir -p custom_auth/migrations
mkdir -p system_config/migrations
mkdir -p core/migrations
mkdir -p media/migrations
touch custom_auth/migrations/__init__.py
touch core/migrations/__init__.py
touch media/migrations/__init__.py
touch system_config/migrations/__init__.py

python manage.py makemigrations
python manage.py migrate

python manage.py loaddata media/fixtures/media/*

python manage.py createsuperuser
