# Frontend Dockerfile

# Node.js base image
FROM node:18-alpine

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY package*.json ./
RUN npm install

# Uygulama kodunu kopyala
COPY . .

# Port ayarı
EXPOSE 3000

# Uygulamayı başlat
CMD ["npm", "run", "dev"] 