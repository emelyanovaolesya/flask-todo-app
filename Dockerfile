FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p instance

RUN echo '#!/bin/sh' > /start.sh && \
    echo 'echo "Creating database"' >> /start.sh && \
    echo 'python create_db.py' >> /start.sh && \
    echo 'echo "Starting Flask app"' >> /start.sh && \
    echo 'flask run --host=0.0.0.0 --port=5000' >> /start.sh && \
    chmod +x /start.sh

EXPOSE 5000

CMD ["/start.sh"]