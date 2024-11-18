# Start from the specified base image with Python and dependencies
FROM iseletkov/sklearn

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
# Run the Python script
CMD ["uvicorn", "ml:app", "--host", "0.0.0.0", "--port", "8000"]
