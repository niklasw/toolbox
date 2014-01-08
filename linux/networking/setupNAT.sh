## May be necessary. Check if set to 1 first.
# echo 1 > /proc/sys/net/ipv4/ip_forward
# echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf


external=p3p1
internal=em1
iptables -A FORWARD -i $internal -o $external  -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i $external -o $internal -j ACCEPT
iptables -t nat -A POSTROUTING -o $external -j MASQUERADE

## To make permanent
# service iptables save
