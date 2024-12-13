# Data Collector Application Demo - Hashtag Generator
### Serverless Real-time Data Applications: Leveraging Pub/Sub and BigQuery

## Overview
A real-time hashtag generation application using Google Cloud Platform services:
- Frontend: Simple HTML/CSS/JS application
- Backend: Cloud Run functions
- AI: Gemini 2.0 flash model
- Data Pipeline: Cloud Pub/Sub -> BigQuery

## Architecture
```
Frontend (HTML/JS) -> Cloud Run Function -> Pub/Sub -> BigQuery
                           |
                        Gemini AI
```

## Features
- Real-time hashtag generation from text input
- Serverless backend processing
- Data persistence in BigQuery
- AI-powered hashtag suggestions

## Prerequisites
- Google Cloud Platform account
- Enable required APIs:
  - Cloud Run
  - Cloud Pub/Sub
  - BigQuery
  - Vertex AI (Gemini)

## Setup

### Backend
1. Deploy Cloud Run function:
```bash
gcloud run deploy hashtag-generator \
  --source functions/ \
  --region us-central1
```

2. Create Pub/Sub topic and subscription:
```bash
gcloud pubsub topics create hashtag-events
gcloud pubsub subscriptions create hashtag-to-bq --topic hashtag-events
```

### Frontend
1. Update `action` URL in index.html with your Cloud Run endpoint
2. Host the static files (index.html, style.css, script.js)

## Environment Variables
Plese set up the environment variable to Cloud Secret Manager before deploying.
```
TOPIC=projects/{project-id}/topics/hashtag-events
API_KEY=your-gemini-api-key
```
