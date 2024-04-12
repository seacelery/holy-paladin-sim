# FROM pypy:3.10-slim

# WORKDIR /app

# RUN apt-get update && apt-get install -y git

# COPY requirements.txt /app/
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . /app

# EXPOSE 5500

# ENV FLASK_APP=run.py
# ENV FLASK_RUN_PORT=5500

# CMD ["pypy", "run.py"]


# heroku
FROM pypy:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5500

ENV FLASK_APP=run.py

CMD ["sh", "-c", "pypy run.py run --host=0.0.0.0 --port=$PORT"]