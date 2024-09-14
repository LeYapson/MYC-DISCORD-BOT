# Use a Python base image
FROM python:3.12.3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the bot code into the container
COPY . .

# Set up a virtual environment
RUN python -m venv /app/venv

# Activate the virtual environment and install dependencies
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the bot and database
CMD ["bash", "-c", "python bot.py"]