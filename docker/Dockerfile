FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances système pour WeasyPrint (export PDF)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf-xlib-2.0-0 libffi-dev shared-mime-info \
    gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# En prod : collectstatic + gunicorn
# En dev  : le command dans docker-compose.dev.yml override cette ligne
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
