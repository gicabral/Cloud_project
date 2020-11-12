import boto3
import time
from botocore.exceptions import ClientError


# Global variables Ohio
oh_region = "us-east-2"
oh_keypair_name = "GI_kp_oh"
oh_db_name = "GI_DB"
oh_db_sg_name = "GI_DB_sg"
oh_api_name = "GI_API"
oh_api_sg_name = "GI_API_sg"
oh_ami_ubuntu18 = "ami-0e82959d4ed12de3f"

# Global variables for North Virginia
nv_region = "us-east-1"
nv_keypair_name = "GI_kp_nv"
nv_client_name = "GI_DB"
nv_client_sg_name = "GI_DB_sg"
nv_ami_ubuntu18 = "ami-0817d428a6fb68645"
nv_tg_name = "GI-tg"
nv_asg_name = "GI_asg"
nv_lb_name = "GI-lb"
nv_lc_name = "GI_lc"

# Create Boto3 resources for North Virginia
nv_client_lb = boto3.client('elbv2', region_name=nv_region)
nv_client = boto3.client('ec2', region_name=nv_region)
nv_client_asg = boto3.client('autoscaling', region_name=nv_region)
nv_ec2 = boto3.resource("ec2", region_name=nv_region)


min_instances = 1
max_instances = 1
t2_micro = 't2.micro'

# Create Boto3 resources for Ohio
oh_ec2 = boto3.resource("ec2", region_name=oh_region)
oh_client = boto3.client("ec2", region_name=oh_region)

tags = [
        {
            'Key'  : 'Owner',
            'Value': 'Giovanna'
        },
        {
            'Key'  : 'Name',
            'Value': 'GiProjeto' 
        }
]

def create_keypair(ec2, filename, keyname):
    try:
        keypair = ec2.create_key_pair(KeyName=keyname)
        # Capture the key and store it in a file
        outfile = open(filename, "w")
        outfile.write(str(keypair.key_material))
        print(f"Keypair '{keyname}' created.")
    except ClientError as e:
        print(f"Could not create keypair '{keyname}'. Error: {e}")

def delete_keypair(client, keyname):
    try:
        # Get all keypairs
        result = client.describe_key_pairs(KeyNames=[keyname])

        # Delete keypair if it exists
        for keypair in result["KeyPairs"]:
            if keypair["KeyName"] == keyname:
                client.delete_key_pair(KeyName=keyname)
        print(f"Keypair '{keyname}' deleted.")
    except ClientError as e:
        print(f"Could not delete keypair '{keyname}'. Error: {e}")

def create_db_security_group(client, security_group_name):
    try:
        # Get VPC id
        response = client.describe_vpcs()
        vpcId = response["Vpcs"][0]["VpcId"]
        # Create sg
        response_sg = client.create_security_group(
            Description="Projeto Final Giovanna",
            GroupName=security_group_name,
            VpcId=vpcId
        )

        try:
            # Allow 8080
            response = client.authorize_security_group_ingress(
                GroupName=security_group_name,
                IpPermissions=[
                    {'IpProtocol': 'tcp', 
                        'FromPort': 5432, 
                        'ToPort': 5432,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }]
            )

            # Allow 22
            response = client.authorize_security_group_ingress(
                GroupName=security_group_name,
                IpPermissions=[
                    {'IpProtocol': 'tcp', 
                        'FromPort': 22, 
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }]
            )
            print(f"Security group and ingress rule for '{security_group_name}' created.")

        except ClientError as e:
                print(f"Could not create ingress rule for '{security_group_name}'. Error: {e}")
        
    except ClientError as e:
        print(f"Could not create security group '{security_group_name}'. Error: {e}")

def create_lc_security_group(client, security_group_name):
    try:
        # Get VPC id
        response = client.describe_vpcs()
        vpcId = response["Vpcs"][0]["VpcId"]
        # Create sg
        response_sg = client.create_security_group(
            Description="Projeto Final Giovanna",
            GroupName=security_group_name,
            VpcId=vpcId
        )

        try:
            # Allow 80
            response = client.authorize_security_group_ingress(
                GroupName=security_group_name,
                IpPermissions=[
                    {'IpProtocol': 'tcp', 
                        'FromPort': 80, 
                        'ToPort': 80,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }]
            )

            # Allow 22
            response = client.authorize_security_group_ingress(
                GroupName=security_group_name,
                IpPermissions=[
                    {'IpProtocol': 'tcp', 
                        'FromPort': 22, 
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }]
            )
            print(f"Security group and ingress rule for '{security_group_name}' created.")

        except ClientError as e:
                print(f"Could not create ingress rule for '{security_group_name}'. Error: {e}")
        
    except ClientError as e:
        print(f"Could not create security group '{security_group_name}'. Error: {e}")

def create_api_security_group(client, security_group_name):
    try:
        # Get VPC id
        response = client.describe_vpcs()
        vpcId = response["Vpcs"][0]["VpcId"]
        # Create sg
        response_sg = client.create_security_group(
            Description="Projeto Final Giovanna",
            GroupName=security_group_name,
            VpcId=vpcId
        )

        try:
            # Allow 8080
            response = client.authorize_security_group_ingress(
                GroupName=security_group_name,
                IpPermissions=[
                    {'IpProtocol': 'tcp', 
                        'FromPort': 80, 
                        'ToPort': 8080,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }]
            )

            # Allow 22
            response = client.authorize_security_group_ingress(
                GroupName=security_group_name,
                IpPermissions=[
                    {'IpProtocol': 'tcp', 
                        'FromPort': 22, 
                        'ToPort': 22,
                        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
                    }]
            )
            print(f"Security group and ingress rule for '{security_group_name}' created.")

        except ClientError as e:
                print(f"Could not create ingress rule for '{security_group_name}'. Error: {e}")
        
    except ClientError as e:
        print(f"Could not create security group '{security_group_name}'. Error: {e}")

def delete_security_group(client, security_group_name):
    try: 
        response = client.describe_security_groups(GroupNames=[security_group_name])
        try:
            response = client.delete_security_group(GroupName=security_group_name)
            print(f"Security group '{security_group_name}' deleted.")
        except ClientError as e:
            print(f"Could not delete security group '{security_group_name}'. Error: {e}")
    except ClientError as e:
        print(f"Could not find security group '{security_group_name}'. Error: {e}")

def create_instance_db(ec2, client, imageId, minCount, maxCount, keyname, tags, sg_name):
    # Create instance
    response = ec2.create_instances(
        ImageId=imageId,
        MinCount=minCount,
        MaxCount=maxCount,
        InstanceType="t2.micro",
        KeyName=keyname,
        SecurityGroups=[
            sg_name,
        ], 
        UserData='''#!/etc/bash
        sudo apt update
        sudo apt install postgresql postgresql-contrib -y
        sudo su - postgres
        psql -c "CREATE USER cloud WITH PASSWORD 'cloud';"
        createdb -O cloud tasks
        sed -i "/#listen_addresses = 'localhost'/ a\listen_addresses='*'" /etc/postgresql/9/main/postgresql.conf
        sed -i "/local   replication     all                                     peer/ a\host all all 0.0.0.0/0 md5" /etc/postgresql/9/main/pg_hba.conf
        exit
        sudo ufw allow 5432/tcp
        sudo systemctl restart postgresql 
        ''', 
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': tags
            },
        ]
    )

    # Wait until it's created
    waiter = client.get_waiter('instance_status_ok')
    waiter.wait(InstanceIds=[response[0].id])

    response = client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Owner',
                'Values': [
                    'Giovanna',
                ]
            }
        ]
    )

    r = []
    for i in response['Reservations']:
        for j in i['Instances']:
            if j['State']['Name'] != 'terminated':
                r.append(j)

    instance_ip = r[0]['NetworkInterfaces'][0]['PrivateIpAddresses'][0]['Association']['PublicIp']
    print(f"Instance created. IP: {instance_ip}")
    return instance_ip 

def create_instance_api(ec2, client, imageId, minCount, maxCount, keyname, tags, ip_database, sg_name):
    # Create instance
    response = ec2.create_instances(
        ImageId=imageId,
        MinCount=minCount,
        MaxCount=maxCount,
        InstanceType="t2.micro",
        KeyName=keyname,
        SecurityGroups=[
            sg_name,
        ],
        UserData='''#!/bin/sh
        sudo apt update
        sudo apt install python3-dev libpq-dev python3-pip -y
        git clone https://github.com/gicabral/tasks.git
        mv tasks /home/ubuntu
        sudo sed -i -e 's/node1/{}/g' /home/ubuntu/tasks/portfolio/settings.py
        sh ./home/ubuntu/tasks/install.sh
        echo "@reboot sh /home/ubuntu/tasks/run.sh" >> crontab
        sudo reboot
        '''.format(ip_database), 
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': tags
            },
        ]
    )

    # Wait until it's created
    waiter = client.get_waiter('instance_status_ok')
    waiter.wait(InstanceIds=[response[0].id])

def terminate_instance(client, keyname):
    response =  client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Owner',
                'Values': [
                    'Giovanna',
                ]
            }
        ]
    )

    instanceId = []
    for i in response['Reservations']:
            for j in i['Instances']:
                if j['State']['Name'] != 'terminated':
                    instanceId.append(j['InstanceId'])
                    if len(j) > 0:
                        client.terminate_instances(InstanceIds=[j['InstanceId']])     
                        waiter = client.get_waiter('instance_terminated')
                        waiter.wait(InstanceIds=instanceId) 

    print("Instances terminated.")


def create_target_group(client, client_lb, target_group_name):
    # Get VPC id
    response = client.describe_vpcs()
    vpcId = response["Vpcs"][0]["VpcId"]

    response = client_lb.create_target_group(
        Name=target_group_name,
        Protocol='HTTP',
        Port=80,
        VpcId=vpcId,
        HealthCheckProtocol='HTTP',
        HealthCheckPath='/',
        TargetType='instance'
    )

    print(f"Target group '{target_group_name}' created.")
    return response['TargetGroups'][0]['TargetGroupArn'] 

def delete_target_group(client, target_group_name):
    try:
        response = client.describe_target_groups(Names=[target_group_name])
        arn = response["TargetGroups"][0]["TargetGroupArn"]
        delete_target = client.delete_target_group(TargetGroupArn=arn)
        print(f"Target group '{target_group_name}' deleted.")

    except ClientError as e:
        print(f"Could not delete target group '{target_group_name}'. Error: {e}")

def create_launch_configuration(client, amiName, lauch_configuration_name, keyname, sg):
    response = client.create_launch_configuration(
        LaunchConfigurationName=lauch_configuration_name,
        InstanceType='t2.micro', 
        KeyName=keyname,
        InstanceMonitoring={'Enabled': True},
        SecurityGroups=[sg],
        ImageId=amiName,
        UserData="""
            curl -fsSL https://get.docker.com -o get-docker.sh
            sudo sh get-docker.sh
            sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
            sudo chmod +x /usr/local/bin/docker-compose

            sudo docker run -d --name=netdata -p 80:19999 \
            -v /proc:/host/proc:ro \
            -v /sys:/host/sys:ro \
            -v /var/run/docker.sock:/var/run/docker.sock:ro \
            --cap-add SYS_PTRACE \
            --security-opt apparmor=unconfined \
            netdata/netdata
        """
    )
    print(f"LC '{lauch_configuration_name}' created.")

def delete_launch_configuration(client, lauch_configuration_name):
    try:
        client.delete_launch_configuration(LaunchConfigurationName=lauch_configuration_name)
        print(f"LC '{lauch_configuration_name}' deleted")
    except ClientError as e:
        print("No Launch Configuration called "+ lauch_configuration_name)


def create_load_balancer(nv_client, nv_client_lb, load_balancer_name, security_group_name):
    security_group = nv_client.describe_security_groups(GroupNames=[security_group_name])["SecurityGroups"][0]["GroupId"]

    response_subnet = nv_client.describe_subnets()
    subnets_ids = [response_subnet['Subnets'][i]['SubnetId'] for i in range(6)]

    create_lb_response  = nv_client_lb.create_load_balancer(
        Name=load_balancer_name,
        Subnets=subnets_ids,
        SecurityGroups=[security_group],
        Scheme='internet-facing',
        Type='application',
        IpAddressType='ipv4'
    )
    
    waiter = nv_client_lb.get_waiter('load_balancer_exists')
    waiter.wait(LoadBalancerArns=[create_lb_response['LoadBalancers'][0]['LoadBalancerArn']])
    time.sleep(60)

    print(f"Load balancer '{load_balancer_name}' created.")
    return create_lb_response['LoadBalancers'][0]['LoadBalancerArn']

def delete_load_balancer(nv_client_lb, load_balancer_name):
    try:
        lbalancer = nv_client_lb.describe_load_balancers(Names=[load_balancer_name])["LoadBalancers"][0]["LoadBalancerArn"]
        
        response = nv_client_lb.delete_load_balancer(LoadBalancerArn=lbalancer)

        waiter = nv_client_lb.get_waiter('load_balancers_deleted')
        waiter.wait(LoadBalancerArns=[lbalancer])
        time.sleep(60)
        print(f"Load balancer '{load_balancer_name}' deleted.")

    except ClientError as e:
        print(f"Could not find Load balancer '{load_balancer_name}'. Error: {e}")

def createListener(nv_client_lb, tg, lb):
    response = nv_client_lb.create_listener(
        LoadBalancerArn = lb,
        Protocol='HTTP',
        Port=80,
        DefaultActions=[
            {
                'Type': 'forward',
                'TargetGroupArn': tg
            }
        ]
    )

def create_auto_scaling(nv_client_asg, min_instances, targetGroup, nv_lc_name, nv_asg_name):
    response = nv_client_asg.create_auto_scaling_group(
        AutoScalingGroupName=nv_asg_name,
        MinSize=min_instances,
        MaxSize=4,
        DesiredCapacity=min_instances,
        LaunchConfigurationName=nv_lc_name,
        TargetGroupARNs=[targetGroup],
        AvailabilityZones=['us-east-1a',
            'us-east-1b',
            'us-east-1c',
            'us-east-1d',
            'us-east-1e',
            'us-east-1f'],
        Tags=[
            {
                'Key'  : 'Owner',
                'Value': 'Giovanna'
            },
            {
                'Key'  : 'Name',
                'Value': 'Giautoscaling' 
            }]       
    )

    print(f"Autoscaling '{nv_asg_name}' created.")


def delete_autoscaling(nv_client_asg, nv_asg_name):
    response = nv_client_asg.describe_auto_scaling_groups(AutoScalingGroupNames=[nv_asg_name])
    if len(response['AutoScalingGroups']) > 0:
        try:
            response = nv_client_asg.delete_auto_scaling_group(
                AutoScalingGroupName=nv_asg_name,
                ForceDelete=True
            )

            response = nv_client_asg.describe_auto_scaling_groups(AutoScalingGroupNames=[nv_asg_name])
            while response['AutoScalingGroups']:
                response = nv_client_asg.describe_auto_scaling_groups(AutoScalingGroupNames=[nv_asg_name])
                time.sleep(5)

            print("[LOG] Autoscaling group deleted")
        except ClientError as e:
            print(f"[LOG] Could not delete autoscaling group {nv_asg_name}. Error: {e}")
    else:
        print("[LOG] Autoscaling group does not exist")

# Configs for Ohio
terminate_instance(oh_client, oh_keypair_name)
delete_keypair(oh_client, oh_keypair_name)
delete_security_group(oh_client, oh_db_sg_name)
delete_security_group(oh_client, oh_api_sg_name)

create_keypair(oh_ec2, oh_keypair_name, oh_keypair_name)
create_db_security_group(oh_client, oh_db_sg_name)
create_api_security_group(oh_client, oh_api_sg_name)

ip_database = create_instance_db(oh_ec2, oh_client, oh_ami_ubuntu18, min_instances, max_instances, oh_keypair_name, tags, oh_db_sg_name)
create_instance_api(oh_ec2, oh_client, oh_ami_ubuntu18, min_instances, max_instances, oh_keypair_name, tags, ip_database, oh_api_sg_name)

# Configs for North Virginia
delete_autoscaling(nv_client_asg, nv_asg_name)
delete_load_balancer(nv_client_lb, nv_lb_name)
delete_target_group(nv_client_lb, nv_tg_name)
delete_launch_configuration(nv_client_asg, nv_lc_name)
delete_keypair(nv_client, nv_keypair_name)
delete_security_group(nv_client, nv_client_sg_name)

create_keypair(nv_ec2, nv_keypair_name, nv_keypair_name)
create_lc_security_group(nv_client, nv_client_sg_name)
nv_tg_arn = create_target_group(nv_client, nv_client_lb, nv_tg_name)
create_launch_configuration(nv_client_asg, nv_ami_ubuntu18, nv_lc_name, nv_keypair_name, nv_client_sg_name)
nv_lb_arn = create_load_balancer(nv_client, nv_client_lb, nv_lb_name, nv_client_sg_name)
createListener(nv_client_lb, nv_tg_arn, nv_lb_arn)
create_auto_scaling(nv_client_asg, 1, nv_tg_arn, nv_lc_name, nv_asg_name)