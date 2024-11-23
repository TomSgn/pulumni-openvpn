import pulumi_aws as aws

class Network:
    def __init__(self, name):
        self.vpc = aws.ec2.Vpc(
            f"{name}-vpc",
            cidr_block="10.0.0.0/24",
            enable_dns_support=True,
            enable_dns_hostnames=True,
            tags={"Name": f"{name}-vpc"},
        )

        self.subnet = aws.ec2.Subnet(
            f"{name}-subnet",
            vpc_id=self.vpc.id,
            cidr_block="10.0.0.0/28",
            map_public_ip_on_launch=True,
            tags={"Name": f"{name}-subnet"},
        )

        self.internet_gateway = aws.ec2.InternetGateway(
            f"{name}-igw",
            vpc_id=self.vpc.id,
            tags={"Name": f"{name}-igw"},
        )

        self.route_table = aws.ec2.RouteTable(
            f"{name}-route-table",
            vpc_id=self.vpc.id,
            routes=[
                {"cidr_block": "0.0.0.0/0", "gateway_id": self.internet_gateway.id},
            ],
            tags={"Name": f"{name}-route-table"},
        )

        self.route_table_association = aws.ec2.RouteTableAssociation(
            f"{name}-rta",
            subnet_id=self.subnet.id,
            route_table_id=self.route_table.id,
        )
