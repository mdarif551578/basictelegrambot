# Using `python:3.12.7-alpine3.20` as base image
FROM python:3.12.7-alpine3.20 as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user
ARG UID=10001
RUN adduser --disabled-password --gecos "" --home "/nonexistent" --shell "/sbin/nologin" --no-create-home --uid "${UID}" appuser

# Copy the source code into the container.
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

EXPOSE 8000

# Run the application.
CMD ["python", "main.py"]

