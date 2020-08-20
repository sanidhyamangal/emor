FROM python:3

LABEL Name=emor Version=0.0.1
EXPOSE 80

WORKDIR /app
ADD . /app


# Install libreoffice
RUN apt-get -y update 

# # Using pip:
RUN python -m pip install -r requirements.txt