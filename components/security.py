import pulumi_aws as aws

class SecurityGroup:
    def __init__(self, name, vpc_id):
        self.sg = aws.ec2.SecurityGroup(
            f"{name}-sg",
            vpc_id=vpc_id,
            description="Allow SSH and VPN",
            ingress=[
                {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]},
                {"protocol": "udp", "from_port": 1194, "to_port": 1194, "cidr_blocks": ["0.0.0.0/0"]},
            ],
            egress=[
                {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]},
            ],
            tags={"Name": f"{name}-sg"},
        )
