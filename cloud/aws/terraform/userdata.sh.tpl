#!/bin/bash
# --- Install enable am run Docker for the ice-user ---
set -euo pipefail


dnf install -y docker
systemctl enable --now docker
usermod -aG docker ${ec2user} 
curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-Linux-X86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

REGISTRY_CREDENTIALS="--username ${docker_registry_username} --password ${docker_registry_password}"

sudo su - ${ec2user} -c "docker login $REGISTRY_CREDENTIALS ${docker_registry_url}"
sudo su - ${ec2user} -c "docker pull ${cfd_image}"

sudo su - ${ec2user} -c 'docker run -d --rm \
    --name ice-cfd \
    --user cfd \
    -p 4444:4444 \
    -p 4445:4445 \
    -p 5000:5000 \
    -e NATS_SERVER= \
    ${cfd_image} /opt/cfd/bin/start-cfd-service.sh sleep'
