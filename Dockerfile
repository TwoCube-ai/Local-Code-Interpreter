FROM python:3.8-slim
COPY ./requirements_full.txt /home/
COPY ./src /src/
USER root
#Install gcc
RUN apt-get update
RUN apt-get install gcc -y
RUN apt-get install g++ -y
RUN apt-get install python3-dev -y
RUN apt-get clean
# Install python packages
RUN python -m pip install --no-cache -r /home/requirements_full.txt

EXPOSE 7860
#naviage to the src folder on the container
WORKDIR /src
CMD ["python", "web_ui.py"]