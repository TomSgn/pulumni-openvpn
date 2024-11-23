import pulumi_aws as aws

class EC2Instance:
    def __init__(self, name, ami_id, instance_type, subnet_id, security_group_id, key_name):
        self.instance = aws.ec2.Instance(
            f"{name}-ec2",
            ami=ami_id,
            instance_type=instance_type,
            subnet_id=subnet_id,
            vpc_security_group_ids=[security_group_id],
            key_name=key_name,
            tags={"Name": f"{name}-ec2"},
            user_data="""#!/bin/bash
            yum update -y
            yum install -y openvpn easy-rsa
            mkdir -p /etc/openvpn/easy-rsa/keys
            cp -r /usr/share/easy-rsa/3/* /etc/openvpn/easy-rsa/
            cd /etc/openvpn/easy-rsa

            ./easyrsa init-pki
            echo -e "yes" | ./easyrsa build-ca nopass
            ./easyrsa gen-req server nopass
            echo -e "yes" | ./easyrsa sign-req server server
            ./easyrsa gen-dh
            openvpn --genkey --secret /etc/openvpn/ta.key

            cat <<EOF > /etc/openvpn/server.conf
            port 1194
            proto udp
            dev tun
            ca /etc/openvpn/easy-rsa/pki/ca.crt
            cert /etc/openvpn/easy-rsa/pki/issued/server.crt
            key /etc/openvpn/easy-rsa/pki/private/server.key
            dh /etc/openvpn/easy-rsa/pki/dh.pem
            server 10.8.0.0 255.255.255.0
            keepalive 10 120
            persist-key
            persist-tun
            status /var/log/openvpn-status.log
            log /var/log/openvpn.log
            verb 3
            EOF

            systemctl enable openvpn@server
            systemctl start openvpn@server
            """,
instance_initiated_shutdown_behavior="stop",
        )
