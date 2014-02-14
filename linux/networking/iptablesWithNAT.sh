external=p3p1
internal=em1
iptables -F
#	iptables -A INPUT -p tcp --tcp-flags ALL NONE -j DROP
#	iptables -A INPUT -p tcp ! --syn -m state --state NEW -j DROP
#	iptables -A INPUT -p tcp --tcp-flags ALL ALL -j DROP
#	iptables -A INPUT -i lo -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 8080 -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 8081 -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 46555 -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 443 -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 22 -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 5901:5910 -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 11111 -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 22221:22222 -j ACCEPT
#	iptables -A INPUT -p tcp -m tcp --dport 30000:60000 -j ACCEPT
#	iptables -I INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
#	iptables -A INPUT -p icmp -j ACCEPT
iptables -I INPUT -j ACCEPT
## NAT iptables -A FORWARD -i $internal -o $external  -m state --state RELATED,ESTABLISHED -j ACCEPT
## NAT iptables -A FORWARD -i $external -o $internal -j ACCEPT
## NAT iptables -t nat -A POSTROUTING -o $external -j MASQUERADE
iptables -P OUTPUT ACCEPT
#	iptables -P INPUT DROP

