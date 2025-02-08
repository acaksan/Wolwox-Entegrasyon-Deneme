#!/bin/bash
# Gerekli dizinleri oluştur
mkdir -p logs

# .env dosyasını kopyala (eğer yoksa)
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env dosyası oluşturuldu. Lütfen gerekli değişiklikleri yapın."
    exit 1
fi 