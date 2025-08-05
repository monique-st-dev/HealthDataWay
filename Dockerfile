# 1. Use official slim Python image
FROM python:3.12-slim

# 2. Environment settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Workdir
WORKDIR /code

# 4. Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Copy app
COPY . .

# 7. Collect static files
RUN python src/manage.py collectstatic --noinput

# 8. Expose port
EXPOSE 8000

# 9. Start app with Gunicorn (no Nginx, no entrypoint.sh)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]




## 1. Use the official Python 3.12 slim image
#FROM python:3.12-slim
#
## 2. Set environment variables
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#
## 3. Set working directory inside the container
#WORKDIR /code
#
## 4. Install system dependencies
#RUN apt-get update && apt-get install -y \
#    netcat-openbsd \
#    libjpeg-dev \
#    zlib1g-dev \
#    libtiff-dev \
#    libfreetype6-dev \
#    liblcms2-dev \
#    libwebp-dev \
#    tcl8.6-dev \
#    tk8.6-dev \
#    python3-tk \
#    nginx \
#    && rm -rf /var/lib/apt/lists/*
#
## 5. Copy and install Python dependencies
#COPY requirements.txt .
#RUN pip install --upgrade pip
#RUN pip install -r requirements.txt
#
## 6. Copy project files
#COPY . .
#
## 7. Copy nginx config and create static/media folders
#RUN mkdir -p /vol/web/static /vol/web/media
#COPY nginx/nginx.conf /etc/nginx/sites-available/default
#
## 8. Make entrypoint executable
#RUN chmod +x /code/entrypoint.sh
#
## 9. Expose ports
#EXPOSE 80
#
## 10. Run the entrypoint script (which will run gunicorn + nginx)
#CMD ["/code/entrypoint.sh"]
