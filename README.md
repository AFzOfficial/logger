# Logger - Twitter Clone

Logger is a clone of Twitter. Users can post text, follow each other, like posts and reply.  
and other cool features such as premium users and etc.

### Technologies
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white) 
![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white) ![jQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)  

## How to Run?
### Clone the project
```bash
git clone https://github.com/AFzOfficial/logger.git

cd logger
```

### Setup env
```bash
python3 -m venv .venv
source .venv/bin/activate
```
### Install Depends
```bash
pip install -r requirements.txt
```
### Run Development Docker Compose
```bash
docker compose -f docker-compose.dev.yml up -d
```
### Run Development Server
```bash
python3 manage.py runserver
```

## Run With Docker

```bash
docker compose up -d
```

Open [127.0.0.1:8000](http://127.0.0.1:8000) in your browser

## Todos
- [ ] Add Email Authentication with Celery and Redis
- [ ] Reset Password
