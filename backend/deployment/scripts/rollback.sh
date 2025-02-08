#!/bin/bash

# Hata durumunda scripti durdur
set -e

# Değişkenleri tanımla
APP_NAME="wolvox-backend"
NAMESPACE="wolvox"
REVISION=$1

# Revision kontrolü
if [ -z "$REVISION" ]; then
    echo "Revision numarası belirtilmedi. Kullanım: ./rollback.sh [revision-number]"
    exit 1
fi

echo "🔄 Rollback başlatılıyor..."

# Helm rollback işlemi
echo "⚙️ Helm rollback yapılıyor..."
helm rollback ${APP_NAME} ${REVISION} -n ${NAMESPACE}

# Deployment durumunu kontrol et
echo "🔍 Rollback durumu kontrol ediliyor..."
kubectl rollout status deployment/${APP_NAME} -n ${NAMESPACE}

echo "✅ Rollback tamamlandı!" 