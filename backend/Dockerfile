
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency list first (for better build caching) and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and the serialized model
COPY app.py .
COPY superkart_model.joblib .

# Expose the port the Flask API listens on
EXPOSE 7860

# Start the API
CMD ["python", "app.py"]
