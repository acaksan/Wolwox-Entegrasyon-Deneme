#!/bin/bash

# Hata durumunda scripti durdur
set -e

# Değişkenleri tanımla
ENVIRONMENT=$1
APP_NAME="wolvox-backend"
DOCKER_REGISTRY="your-registry.com"
NAMESPACE="wolvox"

# Environment kontrolü
if [ -z "$ENVIRONMENT" ]; then
    echo "Environment belirtilmedi. Kullanım: ./deploy.sh [dev|staging|prod]"
    exit 1
fi

# Docker image tag'ini oluştur
TAG=$(git rev-parse --short HEAD)
DOCKER_IMAGE="${DOCKER_REGISTRY}/${APP_NAME}:${TAG}"

echo "🚀 Deployment başlatılıyor: ${ENVIRONMENT}"

# Docker image'ı build et
echo "📦 Docker image build ediliyor..."
docker build -t ${DOCKER_IMAGE} .

# Docker image'ı push et
echo "⬆️ Docker image push ediliyor..."
docker push ${DOCKER_IMAGE}

# Helm değerlerini güncelle
echo "⚙️ Helm değerleri güncelleniyor..."
helm upgrade --install ${APP_NAME} ./helm \
    --namespace ${NAMESPACE} \
    --set image.repository=${DOCKER_REGISTRY}/${APP_NAME} \
    --set image.tag=${TAG} \
    --values ./helm/values-${ENVIRONMENT}.yaml

# Deployment durumunu kontrol et
echo "🔍 Deployment durumu kontrol ediliyor..."
kubectl rollout status deployment/${APP_NAME} -n ${NAMESPACE}

echo "✅ Deployment tamamlandı!" 