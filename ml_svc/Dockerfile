# # Start from the specified base image with Python and dependencies
# FROM iseletkov/sklearn

# WORKDIR /app

# COPY requirements.txt .

# RUN pip install -r requirements.txt

# COPY . .

# EXPOSE 8000
# # Run the Python script
# CMD ["uvicorn", "ml:app", "--host", "0.0.0.0", "--port", "8000"]

FROM python:3.9

WORKDIR /code

COPY ./temperature_model.pkl /code/temperature_model.pkl
COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# python3 -m uvicorn app.main:app --reload