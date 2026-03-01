FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p instance

COPY start.sh /start.sh

RUN chmod +x /start.sh

EXPOSE 5000

CMD ["/start.sh"]