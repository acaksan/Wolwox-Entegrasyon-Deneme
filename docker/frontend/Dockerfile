# Development stage
FROM node:20-alpine

WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY frontend/package*.json ./
RUN npm install

# Kaynak kodları kopyala
COPY frontend .

# Port ayarı
EXPOSE 3000

# Uygulamayı development modunda başlat
CMD ["npm", "run", "dev"]

# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY frontend/package*.json ./
RUN npm ci

# Kaynak kodları kopyala
COPY frontend .

# Uygulamayı derle
RUN npm run build

# Production stage
FROM node:20-alpine AS runner

WORKDIR /app

# Sadece gerekli dosyaları kopyala
COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Port ayarı
EXPOSE 3000

# Uygulamayı başlat
CMD ["node", "server.js"] 