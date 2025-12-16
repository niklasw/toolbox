# variables.tf
variable "region"                   { type = string             default = "eu-north-1" }
variable "set_name"                 { type = string             default = "cfd-set-a" }
variable "instance_count"           { type = number             default = 1 }
variable "instance_type"            { type = string             default = "r7a.xlarge" }
variable "instance_disk_size"       { type = number             default = 20 }
variable "vpc_cidr"                 { type = string             default = "10.42.0.0/16" }
variable "subnet_cidr"              { type = string             default = "10.42.1.0/24" }
variable "ssh_cidr"                 { type = string             default = "0.0.0.0/0" }      # tighten as needed
variable "app_cidrs"                { type = list(string)       default = ["0.0.0.0/0"] }
variable "key_name"                 { type = string             default = "cfd-key" }
variable "public_key"               { type = string }                                         # your ~/.ssh/*.pub
variable "ec2user"                  { type = string             default = "ec2-user" }
variable "user_data_file"           { type = string             default = "userdata.sh" }
variable "docker_registry_url"      { type = string             default = "https://registry.equa.se" }
variable "docker_registry_username" { type = string             default = "EQUA-Registry-User" }
variable "docker_registry_password" { type = string             default = "Rotting8-Demeaning5-Chaperone0-Distill4-Dictator2" }
variable "cfd_image"                { type = string             default = "registry.equa.se/cfd/ubuntu-23.04-openfoam13-equa:latest" }
variable "instance_count"           { type = number             default = 1 }

