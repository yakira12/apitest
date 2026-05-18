# Use an official, lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to optimize Python inside the container
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disk
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr (crucial for clean logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*



# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file first to leverage Docker's caching mechanism
COPY ./requirements.txt /code/requirements.txt

# Install the application dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt



# Copy the application folder into the container
COPY . /code/app

#RUN chmod -R 777 /code/app/data

# Expose the internal port that Uvicorn will listen on
EXPOSE 8000

# Run Uvicorn when the container launches, optimized for container architectures
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["fastapi", "run"]



