FROM docker.uclv.cu/python:3.8.10

WORKDIR /app

COPY requirements.txt /app
COPY install.py /app

RUN pip install --no-cache-dir -r requirements.txt \
        --index-url http://nexus.prod.uci.cu/repository/pypi-proxy/simple/ \
        --trusted-host nexus.prod.uci.cu
        
RUN python3 install.py

COPY . .
