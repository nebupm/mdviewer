# Secrets Manager

![what is secrets manager](images/image.png)

## What is Secrets Manager?

Secrets Manager is a service that helps you protect access to your applications, services, and IT resources.
Secrets Manager enables you to easily rotate, manage, and retrieve database credentials, API keys, and other secrets throughout their lifecycle. You can configure Secrets Manager to automatically rotate secrets for supported databases without any code changes.

## Benefits of Secrets Manager

Its a consumption based costing, so in the end it comes up as a cheaper choice.

- **Secure and rotate secrets**: Secrets Manager enables you to easily rotate, manage, and retrieve database credentials, API keys, and other secrets throughout their lifecycle. You can configure Secrets Manager to automatically rotate secrets for supported databases without any code changes.

- **Control access to secrets**: You can control access to secrets using fine-grained AWS Identity and Access Management (IAM) policies. You can also use resource-based policies to share secrets across accounts.

- **Audit secrets usage**: Secrets Manager integrates with AWS CloudTrail to provide you with logs of all secrets usage. This allows you to monitor and audit access to your secrets.

## How secrets manager works

![how it works](images/image-1.png)

### Usage example

![example1](images/image-2.png)

## Use Cases

- **Database credentials**: Store and manage database credentials securely, and rotate them automatically to enhance security.

- **API keys**: Store and manage API keys for third-party services, ensuring they are kept secure and rotated regularly.

- **SSH keys**: Store and manage SSH keys for accessing servers, ensuring they are kept secure and rotated regularly.

- **OAuth tokens**: Store and manage OAuth tokens for accessing APIs, ensuring they are kept secure and rotated regularly.

## AWS Secrets Manager Agent

The AWS Secrets Manager Agent is a lightweight software component that runs on your servers and retrieves secrets from AWS Secrets Manager. The agent can be used to securely retrieve secrets and inject them into your applications at runtime, eliminating the need to hard-code secrets in your application code or configuration files.

Link to Blog : <https://aws.amazon.com/blogs/security/how-to-use-the-aws-secrets-manager-agent/>

![secrets manager agent](images/image-3.png)

The AWS Secrets Manager Agent supports multiple programming languages and frameworks, making it easy to integrate with your applications. It also provides features such as caching and automatic rotation of secrets, ensuring that your applications always have access to the latest secrets without any downtime.

## Management of Secrets

Link to a blog: <https://aws.amazon.com/blogs/security/exploring-common-centralized-and-decentralized-approaches-to-secrets-management/>

### Centralised

![centralised creation of secrets](images/image-4.png)

### Decentralised

![decentralised creation of secrets](images/image-5.png)

## Consumptoin of secrets

### Centralised Consumption

![consumption of secrets](images/image-6.png)

### Decentralised Consumption

![decentralised consumption](images/image-7.png)

## Common industry approach

centralised creation and management but decentralised storage of secrets.
![mixed approach](images/image-8.png)

### Example customer

![capital one](images/image-9.png)

#### Architecture

![architecture](images/image-10.png)

##  Secrets Lifecycle management

Secrets Manager provides a comprehensive lifecycle management for secrets, which includes the following stages:

1. **Creation**: You can create secrets in Secrets Manager using the AWS Management Console, AWS CLI, or AWS SDKs. When you create a secret, you can specify the secret value, description, and tags.

2. **Rotation**: Secrets Manager enables you to automatically rotate secrets for supported databases without any code changes. You can configure rotation for your secrets using the AWS Management Console, AWS CLI, or AWS SDKs.

3. **Retrieval**: You can retrieve secrets from Secrets Manager using the AWS Management Console, AWS CLI, or AWS SDKs. When you retrieve a secret, you can specify the version of the secret that you want to retrieve.

4. **Deletion**: You can delete secrets from Secrets Manager using the AWS Management Console, AWS CLI, or AWS SDKs. When you delete a secret, it is marked for deletion and is not immediately removed from Secrets Manager. You can specify a recovery window for the secret, which allows you to recover the secret if it was deleted by mistake.

![secrets in AWS](images/image-11.png)

## Cross Account Access

![access management](images/image-12.png)

###  Scaling access using Tags (ABAC)

![ABAC](images/image-13.png)

###  Permission policy to manage secrets using tags

![managing secrets using tags](images/image-14.png)

### Secrets manager access control policy types

![policy types](images/image-15.png)

### Accessing secrets over a private network

![using vpc endpoints](images/image-16.png)

###  How rotation works

![secret rotation](images/image-17.png)

![post rotation](images/image-18.png)

![getting secret](images/image-19.png)

#### Rotation pre-reqs

![pre-requisites](images/image-20.png)

####  Rotation Strategies

![rotation](images/image-21.png)

##  Secret manager best practises

![best practises](images/image-22.png)

## Conclusion

Secrets Manager is a powerful service that helps you protect access to your applications, services, and IT resources. By securely storing and managing secrets, you can enhance the security of your applications and reduce the risk of unauthorized access.

## References

- [AWS Secrets Manager Documentation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)

CSAT Survey: <https://pulse.aws/survey/NA7TJTLU>
Workshop Guide: <https://catalog.workshops.aws/secrets-management-challenge>
Slides Link: <https://us-east-1.secure-attach.amazon.com/97689734-f048-45cc-8cd5-a20da0d7447c/6c8d1a0f-801c-4893-b97d-d4dae2d4798f>
Slide Passcode: 6gxFTb

Security Activation Days: <https://aws-experience.com/emea/smb/events/series/activation-days>

Security Reference Architecture: <https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/>
Best Practices: <https://docs.aws.amazon.com/secretsmanager/latest/userguide/best-practices.html>
Access Secrets Manager from outside AWS: <https://aws.amazon.com/blogs/security/use-aws-secrets-manager-to-store-and-manage-secrets-in-on-premises-or-multicloud-workloads/>
Centralised Secrets Manager: <https://aws.amazon.com/blogs/security/how-to-centrally-manage-secrets-with-aws-secrets-manager/>
BatchRetrieve Secrets: <https://aws.amazon.com/blogs/security/how-to-use-the-batchgetsecretsvalue-api-to-improve-your-client-side-applications-with-aws-secrets-manager/>

Skillsbuilder Links: <https://skillbuilder.aws/category/domain/security-identity-and-compliance>

Workshop One-Click Link: <https://catalog.us-east-1.prod.workshops.aws/join?access-code=5140-082c42-86>
Workshop Access URL: <https://join.workshops.aws>
Workshop Access Code: 5140-082c42-86
