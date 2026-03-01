FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p instance

EXPOSE 5000

RUN echo '#!/bin/sh\npython create_db.py\nflask run --host=0.0.0.0 --port=5000' > /start.sh && chmod +x /start.sh

CMD ["/start.sh"]