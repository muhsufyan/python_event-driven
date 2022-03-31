# gunakan python versi 3.9
FROM python:3.9
# buat virtual environment, tampilkan logs jika ada error dg set 1
ENV PYTHONUNBUFFERED 1
# dir kerja(posisi dir now)
WORKDIR /app
# copas requirements.txt ke dir kerja yaitu dir app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
# copas semua file & dir ke workdir yaitu dir app
COPY . /app

# run server
CMD 'python main.py'