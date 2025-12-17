FROM

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

CMD ["uvicorn" "run" "main:app"]