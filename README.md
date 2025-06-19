# WebHookGen

WebHookGen is a minimal Flask application used to receive webhook requests and display them in a simple web UI.

## Getting Started

### Local Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

### Repository Setup

```bash
git clone https://github.com/sherafyk/WebHookGen.git
cd WebHookGen
```

#### Updating

Pull the latest changes and rebuild with Docker Compose:

```bash
docker compose down
git pull
docker compose up -d --build
```

##### Additional diagnostic checks

```bash
docker ps
docker logs <container_name> --tail=100
```

### Build and Run with Docker

```bash
docker build -t webhook-gen .
docker run -d \
  --name webhook-gen \
  -e WEBHOOK_PASS=AppPass1 \
  -p 5000:5000 \
  -v "$PWD/app/data.json":/app/data.json \
  webhook-gen
```

### Run with Docker Compose

The repository includes a `docker-compose.yml` file that exposes the app on port `50011`.

```bash
docker compose up -d --build
```

Visit `http://localhost:50011/`.

The application listens on the port defined by the `PORT` environment variable (default `5000`). When using Docker Compose it is configured to run on `50011`. Authenticate with `admin` and the password set in `WEBHOOK_PASS` (defaults to `AppPass1`).

## Webhook Usage

Send `POST` requests to `/webhook` with a JSON body or form data. Submissions are stored in `app/data.json` and displayed on the home page.

## Project Structure

```
app/
├── main.py        - Flask application
├── data.json      - Stored submissions
└── templates/
    └── index.html - Simple UI to list submissions
Dockerfile         - Container build instructions
docker-compose.yml - Example compose setup
requirements.txt   - Python dependencies
```

## Notes

`WEBHOOK_PASS` can be set as an environment variable to change the admin password. Mount `app/data.json` when using Docker to ensure submissions persist between runs.
