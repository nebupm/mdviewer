# AWS

Users
## user deneasta
    Details
    - Accpount ID: 12345678
    - username/userpassword
    - Console acces: https://12345678.signin.aws.amazon.com/console
    - Access Key ID : THISISMYACCESSKEY
    - Secret access key: THISISMYSECRETACCESSKEY
    - eu-west-2

Provide above values to aws configure command.
## Get your VPC details
(py3) [mymac][√][timepass][master]$ aws ec2 describe-vpcs
{
"Vpcs": [
    {
        "CidrBlock": "172.31.0.0/16",
        "DhcpOptionsId": "dopt-0b621cc6be5b1d2f9",
        "State": "available",
        "VpcId": "vpc-0d504e9220b399706",
        "OwnerId": "136744280765",
        "InstanceTenancy": "default",
        "CidrBlockAssociationSet": [
            {
                "AssociationId": "vpc-cidr-assoc-07c3c774f98ef77a6",
                "CidrBlock": "172.31.0.0/16",
                "CidrBlockState": {
                    "State": "associated"
                }
            }
        ],
        "IsDefault": true
    }
]
}

## Config Details
> ~/.aws

py3) [mymac][√][timepass][master]$ ll ~/.aws
total 16
drwxr-xr-x+ 59 nmathews  staff   1.8K 27 Dec 17:45 ..
-rw-------   1 nmathews  staff   116B 27 Dec 17:45 credentials
drwxr-xr-x   4 nmathews  staff   128B 27 Dec 17:45 .
-rw-------   1 nmathews  staff    43B 27 Dec 17:45 config
(py3) [mymac][√][timepass][master]$


Creating a cloud9 instance
py3) [mymac][X][timepass][master]$ aws cloud9 create-environment-ec2 --name getting-started --description "Getting started with AWS Cloud9." --instance-type t3.micro --automatic-stop-time-minutes 60
{
    "environmentId": "977a23ad89094bf3b39bfc20f9caba94"
}
(py3) [mymac][√][timepass][master]$


Accessing this above env:
https://console.aws.amazon.com/cloud9/ide/<environment ID>?region=eu-west-2
https://console.aws.amazon.com/cloud9/ide/977a23ad89094bf3b39bfc20f9caba94?region=eu-west-2