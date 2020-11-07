import boto3


UBUNTU18_OHIO = "ami-0e82959d4ed12de3f"
UBUNTU18_NV = "ami-0817d428a6fb68645"
NVirginia_key = "NVirginia"
ohio_key = "ohio"

min_instances = 1
max_instances = 1
region_ohio = "us-east-2"
region_virginia = "us-east-1"


ec2_ohio = boto3.resource('ec2', region_name=region_ohio)
ec2_virginia = boto3.resource('ec2', region_name=region_virginia)
clientOhio = boto3.client('ec2', region_name=region_ohio)
clientVirginia = boto3.client('ec2', region_name=region_virginia)

############ INSTANCE AND KEY PAIR ##################################################

def create_instances_and_key_pair(name_file, name_key, ImageId, client, ec2):

    outfile = open(name_file,'w')

    key_pair = ec2.create_key_pair(KeyName=name_key)

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    outfile.write(KeyPairOut)

    describe_key = client.describe_key_pairs(KeyNames=[name_key])
    
    # create a new EC2 instance
    instances = ec2.create_instances(
        ImageId=ImageId,
        MinCount=min_instances,
        MaxCount=max_instances,
        InstanceType='t2.micro',
        KeyName=name_key
    )

    for first in describe_key:
        for name in describe_key[first]:
            for name_key in name:
                if len(name_key) > 1:
                    i_name = name['KeyName']
                    if i_name == ohio_key:
                        client.delete_key_pair(KeyName=i_name)
                    else:
                        break

def terminate_instance(client):
    d_instances = client.describe_instances()
    print(d_instances)

    for first in d_instances['Reservations']:
            for name in first['Instances']:
                if name['KeyName'] == ohio_key and name['State']['Name'] != 'terminated':
                    if len(name) > 0:
                        client.terminate_instances(InstanceIds=[name['InstanceId']])


terminate_instance(clientOhio)
create_instances_and_key_pair('ohio.pem', ohio_key, UBUNTU18_OHIO, clientOhio, ec2_ohio)
