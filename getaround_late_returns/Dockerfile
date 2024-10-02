FROM continuumio/miniconda3


WORKDIR /home/app


COPY requirements.txt .


RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 80

CMD streamlit run --server.port $PORT getaround.py