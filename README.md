# WebHookGen

WebHookGen is a minimal Flask application used to receive webhook requests and display them in a web UI.

## Getting Started

1. Install dependencies and run the app locally:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app/main.py
   ```

   ### Setup
```
git clone https://github.com/sherafyk/WebHookGen.git
```
```
cd WebHookGen
```
   #### Updating

Pull the latest changes and rebuild:
```bash
docker-compose down
git pull
docker-compose up -d --build
```
##### Additional diagnostic checks

```
docker ps
```
```
docker logs sfk3-app-1 --tail=100
```

2. Build and run with Docker:

   ```bash
   docker build -t webhook-gen .
   docker run -d \
     --name webhook-gen \
     -e WEBHOOK_PASS=AppPass1 \
     -p 5000:5000 \
     -v "$PWD/app/data.json":/app/data.json \
     webhook-gen
   ```

The application listens on port `5000`. Use `http://localhost:5000/` in your browser and authenticate with `admin` and the password specified by `WEBHOOK_PASS` (defaults to `AppPass1`).

## Webhook Usage

Send `POST` requests to `/webhook` with a JSON body or form data. Submissions are stored in `app/data.json` and displayed on the home page.

## Project Structure

```
app/
├── main.py        - Flask application
├── data.json      - Stored submissions
└── templates/
    └── index.html - Simple UI to list submissions
Dockerfile          - Container build instructions
requirements.txt    - Python dependencies
```

## Notes

`WEBHOOK_PASS` can be set as an environment variable to change the admin password. Mounting `app/data.json` when using Docker ensures submissions persist between runs.
