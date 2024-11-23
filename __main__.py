import pulumi
import pulumi_aws as aws
from components.network import Network
from components.security import SecurityGroup
from components.ec2 import EC2Instance

# Charger les configurations
config = pulumi.Config()
region = config.require("aws:region")
public_key = config.require("vpn:public_key")

# Obtenir l'AMI Amazon Linux 2
ami_id = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[{"name": "name", "values": ["amzn2-ami-hvm-*-x86_64-gp2"]}],
).id

# Créer le réseau
network = Network("vpn")

# Créer le groupe de sécurité
security_group = SecurityGroup("vpn", network.vpc.id)

# Créer une clé SSH
key_pair = aws.ec2.KeyPair("vpn-keypair", public_key=public_key)

# Créer l'instance EC2
ec2_instance = EC2Instance(
    name="vpn",
    ami_id=ami_id,
    instance_type="t4g.micro",  # Instance éligible au Free Tier
    subnet_id=network.subnet.id,
    security_group_id=security_group.sg.id,
    key_name=key_pair.key_name,
)

# Exporter les informations
pulumi.export("instance_public_ip", ec2_instance.instance.public_ip)
pulumi.export("vpn_connection_port", 1194)
