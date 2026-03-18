# Azure

## AZ900 : Cloud Fundamental exam

D1 : Fundamentals
D2 : Azure serverless Technology
D3 : Security threats on Azure
D4 : Plan and Manage your Azure costs
D5 : Examp prep

Cloud Model
    - public
    - private
    - hybrid

Cloud services
    - IaaS
    - PaaS
    - SaaS

Cloud Benefits
    - High Availability
    - Scalability
        - Horizontal (Scaleout VMs)
        - Vertical (Increase the VM capacity)
    - Global reach
    - Adility
    - Disaster Recovery
    - Fault Tolerance
    - Elasticity
    - Customer latency capabilities
    - Predictive cost considerations
    - Security

Azure Services

- Azure functions : serverless
- Azure Cosmos DB : nosql db

Server -> Hypervisor
    |---> Fabric Controllers 
            |---> Orchestrator - Responsible for everything that happens in Azure


Azure Services
    - Compute (VMS)
    - Networking(VPN'S, LOAD BALANCING)
    - Storage (Block, object)
    - Mobile 
    - Databases
    - Web Services
    - IOT
    - Big Data
    - AI
    - Devops

Azure Region
    - AZ1
    - AZ2
    - AZ3

Azure Resource Manager (ARM) provides a management lauer that enables you to create update and delete resources in your azure subscription.

All the API's will hit the Cloud management Layer. In Azure this layer is called ARM.

- Portal
- Powershell
- Azure shell

When the request for vm creation hits ARM, it will be transferred to Resource Provider(microsoft.compute)
When the request for network cration hits ARM, it will be transferred to Resource provider(microsonf.net)
Same applies to Storage request.

Azure Subscriptions
    Billing Boundary : Generate separate billing reports and invoices for each subscription.
    Acess control boundary : Manage and control access to resurces that users can provision with specific subscriptions

Management Group (MG)
    It can have multiple subscriptions. Its possible to have multiple subscription within and account. Each subscription has a resource group and within each rg we can have the resources.

Any compliance or quotas you want to apply on the group can be applied to a management group.
you can have a Root MG and then you can create multiple MG's and apply the comliances.
You can go to 6 levels of depth with MG's

Powershell

to Install AZ module: Install-Module -name az

Connect-AzAccount

PS /Users/usename> Get-AzResourceGroup

ResourceGroupName : rg_uk_west
Location          : ukwest
ProvisioningState : Succeeded
Tags              :
                    Name     Value
                    =======  ==========
                    os_type  linux
                    region   western_uk

ResourceId        : /subscriptions/5811458f-50f8-4237-9638-03ee91bd9077/resourceGroups/rg_uk_west

ResourceGroupName : rg_uk_south
Location          : uksouth
ProvisioningState : Succeeded
Tags              :
                    Name     Value
                    =======  ========
                    os_type  windows
                    region   south_uk

ResourceId        : /subscriptions/5811458f-50f8-4237-9638-03ee91bd9077/resourceGroups/rg_uk_south

ResourceGroupName : NetworkWatcherRG
Location          : uksouth
ProvisioningState : Succeeded
Tags              :
ResourceId        : /subscriptions/5811458f-50f8-4237-9638-03ee91bd9077/resourceGroups/NetworkWatcherRG


PS /Users/usename>


PS /Users/usename> Get-AzVirtualNetwork

Name                   : rg_uk_south-vnet
ResourceGroupName      : rg_uk_south
Location               : uksouth
Id                     : /subscriptions/5811458f-50f8-4237-9638-03ee91bd9077/resourceGroups/rg_uk_south/providers/Microsoft.Ne
                         twork/virtualNetworks/rg_uk_south-vnet
Etag                   : W/"c2a2fa37-53e3-4463-a198-ad954a58035e"
ResourceGuid           : 0f50d37b-4be8-4152-85ff-c5faf129553d
ProvisioningState      : Succeeded
Tags                   :
AddressSpace           : {
                           "AddressPrefixes": [
                             "10.0.0.0/16"
                           ]
                         }
DhcpOptions            : null
FlowTimeoutInMinutes   : null
Subnets                : [
                           {
                             "Delegations": [],
                             "Name": "default",
                             "Etag": "W/\"c2a2fa37-53e3-4463-a198-ad954a58035e\"",
                             "Id": "/subscriptions/5811458f-50f8-4237-9638-03ee91bd9077/resourceGroups/rg_uk_south/providers/M
                         icrosoft.Network/virtualNetworks/rg_uk_south-vnet/subnets/default",
                             "AddressPrefix": [
                               "10.0.0.0/24"
                             ],
                             "IpConfigurations": [],
                             "ServiceAssociationLinks": [],
                             "ResourceNavigationLinks": [],
                             "ServiceEndpoints": [],
                             "ServiceEndpointPolicies": [],
                             "PrivateEndpoints": [],
                             "ProvisioningState": "Succeeded",
                             "PrivateEndpointNetworkPolicies": "Enabled",
                             "PrivateLinkServiceNetworkPolicies": "Enabled",
                             "IpAllocations": []
                           },
                           {
                             "Delegations": [],
                             "Name": "new_dept",
                             "Etag": "W/\"c2a2fa37-53e3-4463-a198-ad954a58035e\"",
                             "Id": "/subscriptions/5811458f-50f8-4237-9638-03ee91bd9077/resourceGroups/rg_uk_south/providers/M
                         icrosoft.Network/virtualNetworks/rg_uk_south-vnet/subnets/new_dept",
                             "AddressPrefix": [
                               "10.0.1.0/24"
                             ],
                             "IpConfigurations": [],
                             "ServiceAssociationLinks": [],
                             "ResourceNavigationLinks": [],
                             "ServiceEndpoints": [],
                             "ServiceEndpointPolicies": [],
                             "PrivateEndpoints": [],
                             "ProvisioningState": "Succeeded",
                             "PrivateEndpointNetworkPolicies": "Enabled",
                             "PrivateLinkServiceNetworkPolicies": "Enabled",
                             "IpAllocations": []
                           }
                         ]
VirtualNetworkPeerings : []
EnableDdosProtection   : false
DdosProtectionPlan     : null
ExtendedLocation       : null


PS /Users/usename>


PS /Users/usename> Get-AzVM
PS /Users/usename>

PS /Users/usename> Get-AzVM

ResourceGroupName         Name Location       VmSize OsType                NIC ProvisioningState Zone
-----------------         ---- --------       ------ ------                --- ----------------- ----
RG_UK_SOUTH       uksouth-vm01  uksouth Standard_B2s  Linux uksouth-vm01NetInt         Succeeded

PS /Users/usename>


Azure cli


az login

(py3) [usename@mymac][√][~]$ az vm list | jq ".[].storageProfile.osDisk"
{
  "caching": "ReadWrite",
  "createOption": "FromImage",
  "deleteOption": "Detach",
  "diffDiskSettings": null,
  "diskSizeGb": 30,
  "encryptionSettings": null,
  "image": null,
  "managedDisk": {
    "diskEncryptionSet": null,
    "id": "/subscriptions/5811458f-50f8-4237-9638-03ee91bd9077/resourceGroups/rg_uk_south/providers/Microsoft.Compute/disks/uksouth-vm01_disk1_5cad7edd93da4684b284a05cb12519f0",
    "resourceGroup": "rg_uk_south",
    "storageAccountType": "StandardSSD_LRS"
  },
  "name": "uksouth-vm01_disk1_5cad7edd93da4684b284a05cb12519f0",
  "osType": "Linux",
  "vhd": null,
  "writeAcceleratorEnabled": null
}
(py3) [usename@mymac][√][~]$
(py3) [usename@mymac][√][~]$
(py3) [usename@mymac][√][~]$
(py3) [usename@mymac][√][~]$


