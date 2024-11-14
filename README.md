docker build -t taskapi .
docker run -d -p 8000:8000 taskapi

Idea is to rotate bot accounts with their respective proxies to avoid rate limitation.