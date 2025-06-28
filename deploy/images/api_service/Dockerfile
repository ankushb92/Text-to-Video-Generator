FROM python:3.10-slim


WORKDIR /app

# Copy the api_service code into the container
COPY api_service /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8080

CMD ["python", "service.py"]
