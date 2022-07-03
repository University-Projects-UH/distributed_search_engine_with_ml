FROM docker.uclv.cu/python:3.8.10

WORKDIR /app

COPY requirements.txt /app
COPY install_ntlk_packages.py /app

RUN pip install -r requirements.txt \
        --index-url http://nexus.prod.uci.cu/repository/pypi-proxy/simple/ --trusted-host nexus.prod.uci.cu

RUN python install_ntlk_packages.py

COPY . .
