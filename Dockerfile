FROM python:3.10.13-slim

# Create a group and a user
RUN groupadd -g 1099 mygroup && \
    useradd -u 1099 -g 1099 -s /bin/bash -m myuser

# Set the working directory
WORKDIR /app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN python -m pip install -r requirements.txt

# Copy the application code
COPY . .

# Change ownership of the application directory
RUN chown -R myuser:mygroup /app
# Switch to the non-root user
USER myuser
RUN pip install pytest

# Wait for PostgreSQL to be ready and then execute commands
CMD ["./wait-for-db.sh", "db", "flask", "db", "init", "&&", "flask", "db", "migrate", "&&", "flask", "db", "upgrade", "&&", "flask", "run","pytest", "--host=0.0.0.0"]
