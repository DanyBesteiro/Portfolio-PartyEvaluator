# Django LangGraph

AI-powered political party and candidacy evaluation service built with Python, Django REST Framework and LangGraph.

## Overview

This module provides an API for AI-assisted political party and candidacy comparison. It uses LangGraph to orchestrate the evaluation workflow and integrates with an LLM provider through LangChain.

The service is designed to operate independently from the main application, separating AI processing from business logic.

## Tech Stack

- **Python 3.11**
- **Django 5.2**
- **Django REST Framework**
- **LangChain**
- **LangGraph**
- **OpenRouter** for LLM integration
- **Docker Compose** for local development

## Architecture

The service receives requests through its REST API, processes the information using the configured AI workflow and returns structured results to the calling application.

It does not require a dedicated database.

## Getting Started

### Requirements

- Docker and Docker Compose.
- An API key for the configured LLM provider.

### Configuration

Configure the required environment variables in your local environment file, including the credentials needed to access the LLM provider.

Never commit secrets or API keys to version control.

### Run with Docker

```bash
docker compose up --build -d
```

View the logs:

```bash
docker compose logs -f django-langgraph
```

### Run locally

With Python 3.11 and the required environment variables configured:

```bash
pip install -r requirements.txt
python manage.py check
python manage.py runserver
```

## Design Principles

- **Separation of concerns:** AI processing remains independent from the main application's business logic.
- **API-first:** functionality is exposed through HTTP endpoints.
- **Modular workflows:** LangGraph orchestrates the evaluation process.
- **Structured outputs:** results can be consumed and validated by the calling application.

## License

Specify the repository's applicable license if the project is distributed publicly.