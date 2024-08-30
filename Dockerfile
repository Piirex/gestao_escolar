# Imagem Python oficial
FROM python:3.9-slim

# Diretorio de trabalho
WORKDIR /app

# Copia do arquivo requirements.txt e instalação das dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia do restante do código para o diretorio de trabalho
COPY . .

# Porta do Flask
EXPOSE 5000

# Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]
