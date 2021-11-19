FROM uraniumman2/alpine-pyinstaller:3.8 as builder
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src
RUN pyinstaller --onefile -n buildme ./src/starter.py
WORKDIR /build
RUN chmod +x buildme
CMD ["./buildme"]