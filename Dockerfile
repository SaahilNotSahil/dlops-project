FROM python:3.8-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install -r requirements.txt

EXPOSE 6969

HEALTHCHECK CMD curl --fail http://localhost:6969/_stcore/health

ENTRYPOINT ["streamlit", "run", "ui.py", "--server.port=6969", "--server.address=0.0.0.0"]
