#!/usr/bin/env bash
set -euo pipefail

CURRENT_PUBLIC_IP="$(curl -s https://checkip.amazonaws.com || true)"
echo "Current public IP appears to be: ${CURRENT_PUBLIC_IP:-unknown}"

# ========= EDITABLE DEFAULTS =========
INSTANCE_TYPE="r7a.xlarge"
REGION="eu-north-1"
KEY_NAME="aws_rsa_key_2021"
SG_ID="sg-0533e2c17d6b17dba"    # must start with 'sg-'
EIP_ID=eipalloc-0549c0394947e78be  # Elastic IP allocation ID
MY_SSH_CIDR="$CURRENT_PUBLIC_IP/32"      # better: your.public.ip/32
INSTANCE_NAME="CFD-$(tr '.' '-' <<< $INSTANCE_TYPE)"
ROOT_VOL_GB=20                 # root volume size (GB)
SCRATCH_VOL_GB=0               # scratch volume size (GB)
AMI_PARAM="/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64"
# ====================================
REGISTRY="https://registry.equa.se"
REGISTRY_USER="EQUA-Registry-User"
REGISTRY_PASS="Rotting8-Demeaning5-Chaperone0-Distill4-Dictator2"
IMAGE="registry.equa.se/cfd/ubuntu-24.04-openfoam13-equa:latest"
# ====================================

# Global (filled during run)
AMI_ID=""
SUBNET_ID=""
INSTANCE_ID=""
PUB_IP=""
USERDATA_PATH="$(mktemp -t userdata.XXXXXX.sh)"

cleanup() { rm -f "$USERDATA_PATH" 2>/dev/null || true; }
trap cleanup EXIT

log()   { printf '[%s] %s\n' "$(date +%H:%M:%S)" "$*"; }
die()   { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
need()  { command -v "$1" >/dev/null 2>&1 || die "Missing required command: $1"; }

# ====================================
if [[ "${1:-}" != "delete" ]]; then
    [[ -n "${BW_SESSION:-}" ]] || die "Bitwarden session not set in BW_SESSION env var"
fi
# ====================================

ensure_prereqs() {
  need aws
  need jq
  aws --version || true
}

get_ami_id() {
  log "Fetching AMI from SSM: $AMI_PARAM"
  AMI_ID="$(aws ssm get-parameters \
    --region "$REGION" \
    --names "$AMI_PARAM" \
    --query 'Parameters[0].Value' \
    --output text)"
  [[ -n "$AMI_ID" && "$AMI_ID" != "None" ]] || die "Failed to resolve AMI ID"
  log "AMI_ID=$AMI_ID"
}

ensure_key_pair() {
  local name="$1"
  if aws ec2 describe-key-pairs --region "$REGION" --key-names "$name" >/dev/null 2>&1; then
    log "Key pair '$name' exists (ok)."
  else
    log "Creating key pair '$name' and saving to ~/.ssh/${name}.pem"
    aws ec2 create-key-pair --region "$REGION" --key-name "$name" \
      --query 'KeyMaterial' --output text > "$HOME/.ssh/${name}.pem"
    chmod 600 "$HOME/.ssh/${name}.pem"
  fi
}

authorize_ingress_once() {
  local port="$1" cidr="$2" desc="${3:-port $1}"
  aws ec2 authorize-security-group-ingress --region "$REGION" \
    --group-id "$SG_ID" \
    --ip-permissions "IpProtocol=tcp,FromPort=$port,ToPort=$port,IpRanges=[{CidrIp=\"$cidr\",Description=\"$desc\"}]" \
    >/dev/null 2>&1 || true
}

ensure_sg_rules() {
  [[ "$SG_ID" == sg-* ]] || die "SG_ID must start with 'sg-'. Got: $SG_ID"
  log "Ensuring SG $SG_ID has inbound 22, 4444, 4445 from CIDR $MY_SSH_CIDR ..."
  authorize_ingress_once 22   "$MY_SSH_CIDR" "ssh"
  authorize_ingress_once 4444 "$MY_SSH_CIDR" "app-4444"
  authorize_ingress_once 4445 "$MY_SSH_CIDR" "app-4445"
}

pick_default_subnet() {
  log "Selecting a default VPC subnet with public IP assignment"
  local vpc_id
  vpc_id="$(aws ec2 describe-vpcs --region "$REGION" --filters Name=isDefault,Values=true \
            --query 'Vpcs[0].VpcId' --output text)"
  [[ -n "$vpc_id" && "$vpc_id" != "None" ]] || die "No default VPC found in $REGION"

  # Pick the first subnet in that VPC
  SUBNET_ID="$(aws ec2 describe-subnets --region "$REGION" \
    --filters Name=vpc-id,Values="$vpc_id" \
    --query 'Subnets[0].SubnetId' --output text)"
  [[ -n "$SUBNET_ID" && "$SUBNET_ID" != "None" ]] || die "No subnet found in VPC $vpc_id"
  log "Using subnet $SUBNET_ID (VPC $vpc_id)"
}

associate_elastic_ip() {
  local allocation_id="$1"
  local instance_id="${2:-$INSTANCE_ID}"

  [[ -n "$allocation_id" ]] || die "Elastic IP allocation ID not provided"
  [[ -n "$instance_id" ]]  || die "Instance ID not provided or unknown"

  log "Associating Elastic IP ($allocation_id) with instance $instance_id ..."
  # Disassociate if it's already attached somewhere else
  local assoc_id
  assoc_id="$(aws ec2 describe-addresses --region "$REGION" \
              --allocation-ids "$allocation_id" \
              --query 'Addresses[0].AssociationId' --output text 2>/dev/null || true)"

  if [[ "$assoc_id" != "None" && -n "$assoc_id" ]]; then
    log "Elastic IP currently associated ($assoc_id). Disassociating first..."
    aws ec2 disassociate-address --region "$REGION" --association-id "$assoc_id" >/dev/null
  fi

  aws ec2 associate-address --region "$REGION" \
    --allocation-id "$allocation_id" \
    --instance-id "$instance_id" >/dev/null

  log "Elastic IP $allocation_id successfully associated with $instance_id"

  # Print final IP for confirmation
  local pub_ip
  pub_ip="$(aws ec2 describe-addresses --region "$REGION" \
              --allocation-ids "$allocation_id" \
              --query 'Addresses[0].PublicIp' --output text)"
  log "Instance now reachable at fixed IP: $pub_ip"
}


write_user_data() {
  # REGISTRY_CREDENTIALS=$(bw list items --search registry.equa.se_ro   | jq -r '.[] | "--username \(.login.username) --password \(.login.password)"')
  REGISTRY_CREDENTIALS="--username $REGISTRY_USER --password $REGISTRY_PASS"
  cat > "$USERDATA_PATH" <<EOF
#!/bin/bash
set -euo pipefail
# --- Install and enable Docker for the ice-user ---
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
EOF
  log "User-data written to $USERDATA_PATH"
}

launch_instance() {
  log "Launching $INSTANCE_TYPE with $ROOT_VOL_GB GB root volume..."
  local run_json
  run_json="$(aws ec2 run-instances --region "$REGION" \
    --image-id "$AMI_ID" \
    --instance-type "$INSTANCE_TYPE" \
    --key-name "$KEY_NAME" \
    --network-interfaces "DeviceIndex=0,AssociatePublicIpAddress=true,SubnetId=$SUBNET_ID,Groups=$SG_ID" \
    --block-device-mappings "[
      {\"DeviceName\":\"/dev/xvda\",\"Ebs\":{\"VolumeSize\":$ROOT_VOL_GB,\"VolumeType\":\"gp3\",\"DeleteOnTermination\":true}}
    ]" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
    --user-data "file://$USERDATA_PATH" \
    --query 'Instances[0]' --output json)"
  INSTANCE_ID="$(jq -r '.InstanceId' <<<"$run_json")"
  [[ -n "$INSTANCE_ID" && "$INSTANCE_ID" != "null" ]] || die "Failed to launch instance"
  log "Instance launched: $INSTANCE_ID"
}

wait_for_running_and_ip() {
  log "Waiting for instance to enter 'running'..."
  aws ec2 wait instance-running --region "$REGION" --instance-ids "$INSTANCE_ID"
  log "Fetching public IP..."
  PUB_IP="$(aws ec2 describe-instances --region "$REGION" --instance-ids "$INSTANCE_ID" \
    --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)"
  [[ "$PUB_IP" != "None" && -n "$PUB_IP" ]] || die "No public IP assigned"
  log "Public IP: $PUB_IP"
}

find_latest_instance_by_name() {
  local name="$1"
  aws ec2 describe-instances --region "$REGION" \
    --filters "Name=tag:Name,Values=$name" "Name=instance-state-name,Values=pending,running,stopping,stopped,shutting-down" \
    --query 'Reservations[].Instances[].{Id:InstanceId,LaunchTime:LaunchTime}' --output json \
  | jq -r 'sort_by(.LaunchTime) | reverse | .[0].Id // empty'
}

find_all_instance_ids_by_name() {
  local name="$1"
  aws ec2 describe-instances --region "$REGION" \
      --filters "Name=tag:Name,Values=$name" "Name=instance-state-name,Values=pending,running,stopping,stopped,shutting-down" \
      --query 'Reservations[].Instances[].InstanceId' --output text
}

print_connect_help() {
  cat <<EOF

Instance ready.

  Instance ID : $INSTANCE_ID
  Public IP   : $PUB_IP
  Name tag    : $INSTANCE_NAME
  Region      : $REGION

SSH (Amazon Linux):
  ssh -i "\$HOME/.ssh/${KEY_NAME}.pem" -o IdentitiesOnly=yes ec2-user@${PUB_IP}
  or
  ssh -F cfd-ssh.conf cfd-aws

Check cloud-init logs:
  sudo tail -n +1 -f /var/log/cloud-init-output.log

EOF

cat <<EOF2 > cfd-ssh.conf
Host cfd-aws
    HostName $PUB_IP
    User ec2-user
    IdentityFile ~/.ssh/${KEY_NAME}.pem
    IdentitiesOnly yes
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
EOF2
}

create() {
  ensure_prereqs
  get_ami_id
  ensure_key_pair "$KEY_NAME"
  ensure_sg_rules
  pick_default_subnet
  write_user_data
  launch_instance
  wait_for_running_and_ip
  associate_elastic_ip $EIP_ID
  print_connect_help
}

delete_all() {
  ensure_prereqs
  INSTANCES_FOUND=$(find_all_instance_ids_by_name "$INSTANCE_NAME")
  if [[ -z "$INSTANCES_FOUND" ]]; then
      log "No instances found with name tag '$INSTANCE_NAME'. Nothing to delete."
      return
  fi
  for instance in $INSTANCES_FOUND; do
    log "Terminating instance $instance..."
    aws ec2 terminate-instances --region "$REGION" --instance-ids "$instance" >/dev/null
    aws ec2 wait instance-terminated --region "$REGION" --instance-ids "$instance"
    log "Instance $instance terminated."
  done
}

main() {
  if [[ "${1:-}" == "delete" ]]; then
    delete_all
  else
    create
  fi
}

main "$@"

