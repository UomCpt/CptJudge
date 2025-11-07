FROM eclipse-temurin:17-jdk

# Εγκατάσταση Python και pip
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --break-system-packages --no-cache-dir -r /app/requirements.txt

# Αντιγραφή μόνο του φακέλου app
COPY app /app

# Άνοιγμα θύρας για FastAPI
EXPOSE 8000

# Τρέξιμο FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
