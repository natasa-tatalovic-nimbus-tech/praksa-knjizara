# Dockerfile, Image, Container
# FROM python:3.11-slim 
# WORKDIR /app 
# COPY requirements.txt . 
# RUN pip install -r requirements.txt 
# COPY . . 
# CMD ["bash", "-c", "python seed.py && python migration.py"]

FROM python:3.11-slim
# copy whole project
WORKDIR /app 
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["bash","-c", "python seed.py && python migration.py"]
