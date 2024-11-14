docker build -t taskapi .
docker run -d -p 8000:8000 taskapi

Idea is to rotate bot accounts with their respective proxies to avoid rate limitation.

URL: http://127.0.0.1:8000/api/kabish
