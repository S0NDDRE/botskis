#!/bin/bash
# Mindframe AI - Google Cloud Production Setup Script
# Author: Sondre Kjær (hello@mframe.io)

set -e

echo "=================================================="
echo "🚀 Mindframe AI - Google Cloud Setup"
echo "=================================================="

# Configuration
PROJECT_ID="${GCLOUD_PROJECT_ID:-mindframe-production}"
REGION="${GCLOUD_REGION:-europe-north1}"
ZONE="${GCLOUD_ZONE:-europe-north1-a}"
CLUSTER_NAME="mindframe-cluster"
DB_INSTANCE="mindframe-db"
REDIS_INSTANCE="mindframe-redis"

echo ""
echo "📋 Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo "  Zone: $ZONE"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI not installed"
    echo "Install: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ gcloud CLI found"

# Set project
echo ""
echo "1️⃣ Setting Google Cloud project..."
gcloud config set project $PROJECT_ID
gcloud config set compute/region $REGION
gcloud config set compute/zone $ZONE

# Enable required APIs
echo ""
echo "2️⃣ Enabling required APIs..."
gcloud services enable \
    container.googleapis.com \
    sqladmin.googleapis.com \
    redis.googleapis.com \
    compute.googleapis.com \
    cloudresourcemanager.googleapis.com \
    storage-api.googleapis.com \
    containerregistry.googleapis.com \
    secretmanager.googleapis.com \
    monitoring.googleapis.com \
    logging.googleapis.com

echo "✅ APIs enabled"

# Create GKE cluster
echo ""
echo "3️⃣ Creating GKE cluster..."
if gcloud container clusters describe $CLUSTER_NAME --region=$REGION &> /dev/null; then
    echo "⚠️  Cluster $CLUSTER_NAME already exists"
else
    gcloud container clusters create $CLUSTER_NAME \
        --region=$REGION \
        --num-nodes=2 \
        --machine-type=e2-standard-2 \
        --disk-size=20 \
        --disk-type=pd-standard \
        --enable-autoscaling \
        --min-nodes=2 \
        --max-nodes=10 \
        --enable-autorepair \
        --enable-autoupgrade \
        --enable-stackdriver-kubernetes \
        --addons=HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver

    echo "✅ GKE cluster created"
fi

# Get cluster credentials
echo ""
echo "4️⃣ Getting cluster credentials..."
gcloud container clusters get-credentials $CLUSTER_NAME --region=$REGION

# Create Cloud SQL instance (PostgreSQL)
echo ""
echo "5️⃣ Creating Cloud SQL instance..."
if gcloud sql instances describe $DB_INSTANCE &> /dev/null; then
    echo "⚠️  Database instance $DB_INSTANCE already exists"
else
    gcloud sql instances create $DB_INSTANCE \
        --database-version=POSTGRES_15 \
        --tier=db-f1-micro \
        --region=$REGION \
        --storage-type=SSD \
        --storage-size=10GB \
        --storage-auto-increase \
        --backup-start-time=03:00 \
        --enable-bin-log \
        --maintenance-window-day=SUN \
        --maintenance-window-hour=04

    echo "✅ Cloud SQL instance created"

    # Set root password
    echo "Setting database password..."
    DB_PASSWORD=$(openssl rand -base64 32)
    gcloud sql users set-password postgres \
        --instance=$DB_INSTANCE \
        --password=$DB_PASSWORD

    echo "✅ Database password set"
    echo "⚠️  IMPORTANT: Save this password securely!"
    echo "Database Password: $DB_PASSWORD"

    # Store in Secret Manager
    echo "$DB_PASSWORD" | gcloud secrets create db-password --data-file=-
fi

# Create database
echo ""
echo "6️⃣ Creating production database..."
gcloud sql databases create mindframe_production --instance=$DB_INSTANCE || echo "⚠️  Database already exists"

# Create Redis instance
echo ""
echo "7️⃣ Creating Redis instance..."
if gcloud redis instances describe $REDIS_INSTANCE --region=$REGION &> /dev/null; then
    echo "⚠️  Redis instance $REDIS_INSTANCE already exists"
else
    gcloud redis instances create $REDIS_INSTANCE \
        --size=1 \
        --region=$REGION \
        --tier=basic \
        --redis-version=redis_7_0

    echo "✅ Redis instance created"
fi

# Create static IP for load balancer
echo ""
echo "8️⃣ Creating static IP address..."
gcloud compute addresses create mindframe-ip \
    --region=$REGION \
    --network-tier=PREMIUM || echo "⚠️  IP address already exists"

STATIC_IP=$(gcloud compute addresses describe mindframe-ip --region=$REGION --format="get(address)")
echo "✅ Static IP: $STATIC_IP"

# Setup Cloud Storage bucket for static files
echo ""
echo "9️⃣ Creating Cloud Storage bucket..."
BUCKET_NAME="${PROJECT_ID}-static"
gsutil mb -l $REGION gs://$BUCKET_NAME || echo "⚠️  Bucket already exists"
gsutil iam ch allUsers:objectViewer gs://$BUCKET_NAME
echo "✅ Storage bucket created: gs://$BUCKET_NAME"

# Setup Secret Manager secrets
echo ""
echo "🔟 Setting up Secret Manager..."

# Function to create or update secret
create_or_update_secret() {
    SECRET_NAME=$1
    SECRET_VALUE=$2

    if gcloud secrets describe $SECRET_NAME &> /dev/null; then
        echo "$SECRET_VALUE" | gcloud secrets versions add $SECRET_NAME --data-file=-
    else
        echo "$SECRET_VALUE" | gcloud secrets create $SECRET_NAME --data-file=-
    fi
}

echo "Enter your OpenAI API Key:"
read -s OPENAI_API_KEY
create_or_update_secret "openai-api-key" "$OPENAI_API_KEY"

# Generate secret key for FastAPI
SECRET_KEY=$(openssl rand -base64 64)
create_or_update_secret "app-secret-key" "$SECRET_KEY"

# Generate Redis password
REDIS_PASSWORD=$(openssl rand -base64 32)
create_or_update_secret "redis-password" "$REDIS_PASSWORD"

echo "✅ Secrets configured in Secret Manager"

# Build and push Docker image
echo ""
echo "1️⃣1️⃣ Building Docker image..."
cd /home/user/botskis
docker build -t gcr.io/$PROJECT_ID/mindframe:latest .
docker push gcr.io/$PROJECT_ID/mindframe:latest
echo "✅ Docker image pushed to Container Registry"

# Create Kubernetes secrets
echo ""
echo "1️⃣2️⃣ Creating Kubernetes secrets..."
kubectl create secret generic app-secrets \
    --from-literal=DATABASE_URL="postgresql://postgres:$(gcloud secrets versions access latest --secret=db-password)@/mindframe_production?host=/cloudsql/$PROJECT_ID:$REGION:$DB_INSTANCE" \
    --from-literal=REDIS_URL="redis://$(gcloud redis instances describe $REDIS_INSTANCE --region=$REGION --format='get(host)'):6379" \
    --from-literal=OPENAI_API_KEY="$(gcloud secrets versions access latest --secret=openai-api-key)" \
    --from-literal=SECRET_KEY="$(gcloud secrets versions access latest --secret=app-secret-key)" \
    --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Kubernetes secrets created"

# Deploy to Kubernetes
echo ""
echo "1️⃣3️⃣ Deploying to Kubernetes..."
kubectl apply -f /home/user/botskis/kubernetes/deployment.yml

echo "✅ Application deployed"

# Wait for load balancer
echo ""
echo "1️⃣4️⃣ Waiting for load balancer..."
echo "This may take a few minutes..."
kubectl wait --for=condition=available --timeout=300s deployment/mindframe

LOAD_BALANCER_IP=$(kubectl get service mindframe-service -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
echo "✅ Load Balancer IP: $LOAD_BALANCER_IP"

# Setup Cloud CDN
echo ""
echo "1️⃣5️⃣ Setting up Cloud CDN..."
gcloud compute backend-buckets create mindframe-cdn \
    --gcs-bucket-name=$BUCKET_NAME \
    --enable-cdn || echo "⚠️  CDN backend already exists"

echo "✅ Cloud CDN configured"

# Setup monitoring
echo ""
echo "1️⃣6️⃣ Setting up monitoring..."

# Create uptime check
gcloud monitoring uptime create mindframe-uptime \
    --display-name="Mindframe API Health" \
    --resource-type=uptime-url \
    --host=$LOAD_BALANCER_IP \
    --path=/health || echo "⚠️  Uptime check already exists"

echo "✅ Monitoring configured"

# Final summary
echo ""
echo "=================================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "=================================================="
echo ""
echo "📊 Deployment Summary:"
echo "  GKE Cluster: $CLUSTER_NAME"
echo "  Database: $DB_INSTANCE"
echo "  Redis: $REDIS_INSTANCE"
echo "  Load Balancer IP: $LOAD_BALANCER_IP"
echo "  Static IP: $STATIC_IP"
echo "  Storage Bucket: gs://$BUCKET_NAME"
echo ""
echo "🔗 Next Steps:"
echo "  1. Point mindframe.ai DNS to: $LOAD_BALANCER_IP"
echo "  2. Point mframe.io DNS to: $LOAD_BALANCER_IP"
echo "  3. Configure SSL certificates"
echo "  4. Setup Cloudflare (optional)"
echo "  5. Configure email domain (hello@mframe.io)"
echo ""
echo "📋 Important URLs:"
echo "  GKE Dashboard: https://console.cloud.google.com/kubernetes/clusters/$CLUSTER_NAME?project=$PROJECT_ID"
echo "  Cloud SQL: https://console.cloud.google.com/sql/instances/$DB_INSTANCE?project=$PROJECT_ID"
echo "  Logs: https://console.cloud.google.com/logs?project=$PROJECT_ID"
echo "  Monitoring: https://console.cloud.google.com/monitoring?project=$PROJECT_ID"
echo ""
echo "=================================================="
