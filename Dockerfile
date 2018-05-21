FROM python:2.7.14-jessie

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY wmts.py ./
COPY wmts.xml ./
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt

CMD [ "python", "./wmts.py"]
