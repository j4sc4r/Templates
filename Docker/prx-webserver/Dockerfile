FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["python3", "proxmox_start-stop.py"]
