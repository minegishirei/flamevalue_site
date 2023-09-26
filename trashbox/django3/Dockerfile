FROM python


RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

EXPOSE 5000
WORKDIR /app
COPY app /app
COPY requirements.txt ./
COPY God /God

RUN apt-get update 

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
RUN pip3 install Pillow

# Install Node.js and npm
#RUN apt-get install -y nodejs npm
#RUN npm install --save-dev jsdoc
#RUN npm install -g jsdoc

RUN apt-get install -y mecab \
  && apt-get install -y mecab-ipadic \
  && apt-get install -y libmecab-dev \
  && apt-get install -y mecab-ipadic-utf8 \
  && apt-get install -y swig


USER root


CMD ["./cmd.sh"]

