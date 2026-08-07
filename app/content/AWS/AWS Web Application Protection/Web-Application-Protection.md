#  AWS Shield Advanced

##  Overview

AWS Shield Advanced is a managed Distributed Denial of Service (DDoS) protection service that safeguards applications running on AWS. It provides enhanced detection and mitigation against DDoS attacks, ensuring the availability and performance of your applications.

##  Key Features

- **DDoS Protection**: AWS Shield Advanced offers comprehensive protection against DDoS attacks, including volumetric, protocol, and application layer attacks.
- **24/7 Access to DDoS Response Team**: Subscribers have access to the AWS DDoS Response Team (DRT) for assistance during and after an attack.
- **Cost Protection**: AWS Shield Advanced provides financial protection against scaling charges resulting from DDoS attacks, helping to mitigate unexpected costs.
- **Real-time Attack Visibility**: The service offers real-time visibility into DDoS attacks, allowing you to monitor and respond effectively.

##  Use Cases

- **Web Applications**: Protect your web applications from DDoS attacks to ensure they remain available and responsive.
- **APIs**: Safeguard your APIs from DDoS attacks to maintain their functionality and performance.
- **Gaming**: Protect online gaming platforms from DDoS attacks to ensure a seamless gaming experience for users.

##  Getting Started

![DDos Attack](images/image-1.png)

DDoS attack typoes

![types of attack](images/image-2.png)

![volumetric attack example](images/image-3.png)

![how to protect](images/image-4.png)

![using aws edge services](images/image-5.png)

![how the shield works](images/image-6.png)

##  Conclusion

AWS Shield Advanced is a powerful tool for protecting your applications from DDoS attacks. By leveraging its features, you can ensure the availability and performance of your applications while minimizing the impact of potential attacks. Consider implementing AWS Shield Advanced to safeguard your applications and maintain a secure online presence.

### Shield Standard Vs Shield Advanced

![Shield Standard](images/image-7.png)

![Shield Advanced](images/image-8.png)

### How does SRT engagement works

![How does SRT engagement works](images/image-9.png)

### protecting web application

![protecting web application](images/image-10.png)

### protecting latency-sensitive applications

![protecting latency-sensitive applications](images/image-11.png)

### protecting serverless applications

![protecting serverless applications](images/image-12.png)

### protecting on-premises applications

![protecting on-premise applkications](images/image-13.png)

###  Getting started with Shield Advanced

![get started](images/image-14.png)

---

# AWS Web application firewall

## Overview

AWS Web Application Firewall (WAF) is a security service that helps protect your web applications from common web exploits and vulnerabilities. It allows you to create custom rules to block, allow, or monitor web requests based on specific conditions.

## Key Features

- **Customizable Rules**: AWS WAF allows you to create custom rules to filter web traffic based on specific conditions such as IP addresses, HTTP headers, and URI strings.
- **Real-time Monitoring**: The service provides real-time visibility into web traffic and allows you to monitor and analyze web requests.
- **Integration with AWS Services**: AWS WAF can be integrated with other AWS services such as Amazon CloudFront and Application Load Balancer for enhanced protection.

## Use Cases

- **Protecting Web Applications**: AWS WAF can be used to protect web applications from common web exploits such as SQL injection and cross-site scripting (XSS).
- **Blocking Malicious Traffic**: You can use AWS WAF to block malicious traffic based on specific conditions, such as IP addresses or HTTP headers.

![deployment on aws resources](images/image-15.png)

## protect AWS and on-premises apps

![protect AWS and on-premises apps](images/image-16.png)

## Web application attack surface

![attack surface](images/image-17.png)

## WAF sits inline and in parallel

![WAF sits inline and in parallel](images/image-18.png)

##  Reference Architecture to protect web apps

![architecture](images/image-19.png)

## AWS WAF building blocks

![WAF building blocks](images/image-20.png)

## WAF flow

![WAF Flow](images/image-21.png)

## IP Based controls

![ip based controls](images/image-22.png)

## Rule based controls

![rule based controls](images/image-23.png)

## Free AWS AMR (AWS Managed rules)

![Free AWS AMRs](images/image-24.png)

## AWS WAF L7 DD0S protection

![WAF L7 protection](images/image-25.png)

## WAF rules best principles

![waf rules application and order of precedence](images/image-26.png)

## WAF Rate based rules

![rate based rules in Aws waf](images/image-27.png)

## Conclusion

AWS Web Application Firewall (WAF) is an essential tool for protecting your web applications from common web exploits and vulnerabilities. By leveraging its customizable rules and real-time monitoring capabilities, you can enhance the security of your web applications and safeguard them against potential threats. Consider implementing AWS WAF to ensure the security and integrity of your web applications.

<https://join.workshops.aws>
Access code: 2097-043b63-c8

---

# Workshop

Create WAF Protection Pack

click on create protection pack and choose the category Other for App Category.

![create and choose other](images/image-28.png)

Click on add eresource and Choose "Add Cloudfront"

![add resources](images/image-29.png)

Choose your Web Application.

![Choose your Web App](images/image-30.png)

Choose Recommended pack and give a name to the WAF ACL

![name for acl](images/image-31.png)

In the customise protection pack, select the option "Set all to Count action"

![set count ation](images/image-32.png)

for the logging destination select Amazon Data firehose Stream.

![aws firehose stream](images/image-34.png)

Switch to Grid mode to see the WAF ACL's

![grid mode](images/image-34.png)

click on "View and Edit" next to Rules

![edit rules](images/image-35.png)

Edit the rule "AWS-AWSManagedRulesCommonRuleSet"

Uncheck override rule group. All rules should have an action of block. Click Save.
![uncheck override](images/image-36.png)

Do the same for "AWS-AWSManagedRulesSQLiRuleSet"

Add a custom rule to block access to the path "/include" in the API endpoint.

![custom rule](images/image-37.png)

![create custom rule](images/image-38.png)

Select rule type as Custom.

![custom rule type](images/image-39.png)

the new rule should be named "path-block". We should Inspect "URI Path". the statement should be Starts with and the value should be "/includes"
The ext transformation should be "URL Decode"

![rule settings](images/image-40.png)

this is now present at the bottom.
![new rules](images/image-41.png)

AWS WAF Security Automations<https://aws.amazon.com/solutions/implementations/aws-waf-security-automations/>

AWS WAF Developer Guide<https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html>

AWS Best Practices for DDoS Resiliency<https://docs.aws.amazon.com/whitepapers/latest/aws-best-practices-ddos-resiliency/welcome.html>

How to customize your response to layer 7 DDoS attacks using AWS WAF Anti-DDoS AMR <https://aws.amazon.com/blogs/security/how-to-customize-your-response-to-layer-7-ddos-attacks-using-aws-waf-anti-ddos-amr/>

The three most important AWS WAF rate-based rules<https://aws.amazon.com/blogs/security/three-most-important-aws-waf-rate-based-rules/>

How to improve visibility into AWS WAF with anomaly detection<https://aws.amazon.com/blogs/security/how-to-improve-visibility-into-aws-waf-with-anomaly-detection/>

Introducing AI traffic analysis dashboards for AWS WAF <https://aws.amazon.com/blogs/security/introducing-ai-traffic-analysis-dashboards-for-aws-waf/>
