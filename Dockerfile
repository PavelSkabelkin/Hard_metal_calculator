FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY gost_8239_89_d_beam_202312252235.csv /app/
COPY gost_8240_97_202312252235.csv /app/
COPY gost_8509_93_202312252236.csv /app/
COPY metal_calc.py /app/


CMD ["python", "metal_calc.py"]
