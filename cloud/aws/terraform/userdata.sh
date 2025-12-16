#!/bin/bash
# --- Install enable am run Docker for the ice-user ---
set -euo pipefail

EC2_USER="ec2-user"
REGISTRY="https://registry.equa.se"
IMAGE="registry.equa.se/cfd/ubuntu-24.04-openfoam13-equa:latest"

REGISTRY_USER="EQUA-Registry-User"
REGISTRY_PASS="Rotting8-Demeaning5-Chaperone0-Distill4-Dictator2"

REGISTRY_CREDENTIALS="--username $REGISTRY_USER --password $REGISTRY_PASS"

dnf install -y docker
systemctl enable --now docker
usermod -aG docker ec2-user
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-X86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

sudo su - ec2-user -c "docker login $REGISTRY_CREDENTIALS $REGISTRY"
sudo su - ec2-user -c "docker pull $IMAGE"

sudo su - ec2-user -c 'docker run -d --rm \
    --name ice-cfd \
    --user cfd \
    -p 4444:4444 \
    -p 4445:4445 \
    -p 5000:5000 \
    -e NATS_SERVER= \
    $IMAGE /opt/cfd/bin/start-cfd-service.sh sleep'
