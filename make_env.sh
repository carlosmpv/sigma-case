cat > .env <<EOF
POSTGRES_PASSWORD=$(openssl rand -hex 32)
POSTGRES_HOST=host.docker.internal
POSTGRES_USER=sigmacase
POSTGRES_DB=sigmacase
TOKEN_EXPIRE_TIME=24
EOF

cat > client/.env <<EOF
API_URL=http://host.docker.internal:8001
EOF