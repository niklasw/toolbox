#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

CURRENT_PUBLIC_IP="$(curl -s https://checkip.amazonaws.com || true)"

terraform init

terraform apply -auto-approve \
    -var ssh_cidr = ${CURRENT_PUBLIC_IP}/32 \
