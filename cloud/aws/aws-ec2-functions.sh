#!/usr/bin/env bash


ensure_sg_rules() {
  local CIDR=$1
  local SG_ID=$2
  [[ "$SG_ID" == sg-* ]] || die "SG_ID must start with 'sg-'. Got: $SG_ID"
  log "Ensuring SG $SG_ID has inbound 22, 4444, 4445 from CIDR $CIDR ..."
  authorize_ingress_once 22   "$CIDR" "ssh"
  authorize_ingress_once 4444 "$CIDR" "app-4444"
  authorize_ingress_once 4445 "$CIDR" "app-4445"
}
