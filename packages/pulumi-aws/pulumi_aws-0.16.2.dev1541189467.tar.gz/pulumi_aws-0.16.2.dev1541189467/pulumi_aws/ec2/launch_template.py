# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class LaunchTemplate(pulumi.CustomResource):
    """
    Provides an EC2 launch template resource. Can be used to create instances or auto scaling groups.
    """
    def __init__(__self__, __name__, __opts__=None, block_device_mappings=None, credit_specification=None, description=None, disable_api_termination=None, ebs_optimized=None, elastic_gpu_specifications=None, iam_instance_profile=None, image_id=None, instance_initiated_shutdown_behavior=None, instance_market_options=None, instance_type=None, kernel_id=None, key_name=None, monitoring=None, name=None, name_prefix=None, network_interfaces=None, placement=None, ram_disk_id=None, security_group_names=None, tag_specifications=None, tags=None, user_data=None, vpc_security_group_ids=None):
        """Create a LaunchTemplate resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if block_device_mappings and not isinstance(block_device_mappings, list):
            raise TypeError('Expected property block_device_mappings to be a list')
        __self__.block_device_mappings = block_device_mappings
        """
        Specify volumes to attach to the instance besides the volumes specified by the AMI.
        See Block Devices below for details.
        """
        __props__['blockDeviceMappings'] = block_device_mappings

        if credit_specification and not isinstance(credit_specification, dict):
            raise TypeError('Expected property credit_specification to be a dict')
        __self__.credit_specification = credit_specification
        """
        Customize the credit specification of the instance. See Credit 
        Specification below for more details.
        """
        __props__['creditSpecification'] = credit_specification

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        """
        Description of the launch template.
        """
        __props__['description'] = description

        if disable_api_termination and not isinstance(disable_api_termination, bool):
            raise TypeError('Expected property disable_api_termination to be a bool')
        __self__.disable_api_termination = disable_api_termination
        """
        If `true`, enables [EC2 Instance
        Termination Protection](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/terminating-instances.html#Using_ChangingDisableAPITermination)
        """
        __props__['disableApiTermination'] = disable_api_termination

        if ebs_optimized and not isinstance(ebs_optimized, basestring):
            raise TypeError('Expected property ebs_optimized to be a basestring')
        __self__.ebs_optimized = ebs_optimized
        """
        If `true`, the launched EC2 instance will be EBS-optimized.
        """
        __props__['ebsOptimized'] = ebs_optimized

        if elastic_gpu_specifications and not isinstance(elastic_gpu_specifications, list):
            raise TypeError('Expected property elastic_gpu_specifications to be a list')
        __self__.elastic_gpu_specifications = elastic_gpu_specifications
        """
        The elastic GPU to attach to the instance. See Elastic GPU
        below for more details.
        """
        __props__['elasticGpuSpecifications'] = elastic_gpu_specifications

        if iam_instance_profile and not isinstance(iam_instance_profile, dict):
            raise TypeError('Expected property iam_instance_profile to be a dict')
        __self__.iam_instance_profile = iam_instance_profile
        """
        The IAM Instance Profile to launch the instance with. See Instance Profile
        below for more details.
        """
        __props__['iamInstanceProfile'] = iam_instance_profile

        if image_id and not isinstance(image_id, basestring):
            raise TypeError('Expected property image_id to be a basestring')
        __self__.image_id = image_id
        """
        The AMI from which to launch the instance.
        """
        __props__['imageId'] = image_id

        if instance_initiated_shutdown_behavior and not isinstance(instance_initiated_shutdown_behavior, basestring):
            raise TypeError('Expected property instance_initiated_shutdown_behavior to be a basestring')
        __self__.instance_initiated_shutdown_behavior = instance_initiated_shutdown_behavior
        """
        Shutdown behavior for the instance. Can be `stop` or `terminate`.
        (Default: `stop`).
        """
        __props__['instanceInitiatedShutdownBehavior'] = instance_initiated_shutdown_behavior

        if instance_market_options and not isinstance(instance_market_options, dict):
            raise TypeError('Expected property instance_market_options to be a dict')
        __self__.instance_market_options = instance_market_options
        """
        The market (purchasing) option for the instance. See Market Options
        below for details.
        """
        __props__['instanceMarketOptions'] = instance_market_options

        if instance_type and not isinstance(instance_type, basestring):
            raise TypeError('Expected property instance_type to be a basestring')
        __self__.instance_type = instance_type
        """
        The type of the instance.
        """
        __props__['instanceType'] = instance_type

        if kernel_id and not isinstance(kernel_id, basestring):
            raise TypeError('Expected property kernel_id to be a basestring')
        __self__.kernel_id = kernel_id
        """
        The kernel ID.
        """
        __props__['kernelId'] = kernel_id

        if key_name and not isinstance(key_name, basestring):
            raise TypeError('Expected property key_name to be a basestring')
        __self__.key_name = key_name
        """
        The key name to use for the instance.
        """
        __props__['keyName'] = key_name

        if monitoring and not isinstance(monitoring, dict):
            raise TypeError('Expected property monitoring to be a dict')
        __self__.monitoring = monitoring
        """
        The monitoring option for the instance. See Monitoring below for more details.
        """
        __props__['monitoring'] = monitoring

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name of the launch template. If you leave this blank, Terraform will auto-generate a unique name.
        """
        __props__['name'] = name

        if name_prefix and not isinstance(name_prefix, basestring):
            raise TypeError('Expected property name_prefix to be a basestring')
        __self__.name_prefix = name_prefix
        """
        Creates a unique name beginning with the specified prefix. Conflicts with `name`.
        """
        __props__['namePrefix'] = name_prefix

        if network_interfaces and not isinstance(network_interfaces, list):
            raise TypeError('Expected property network_interfaces to be a list')
        __self__.network_interfaces = network_interfaces
        """
        Customize network interfaces to be attached at instance boot time. See Network 
        Interfaces below for more details.
        """
        __props__['networkInterfaces'] = network_interfaces

        if placement and not isinstance(placement, dict):
            raise TypeError('Expected property placement to be a dict')
        __self__.placement = placement
        """
        The placement of the instance. See Placement below for more details.
        """
        __props__['placement'] = placement

        if ram_disk_id and not isinstance(ram_disk_id, basestring):
            raise TypeError('Expected property ram_disk_id to be a basestring')
        __self__.ram_disk_id = ram_disk_id
        """
        The ID of the RAM disk.
        """
        __props__['ramDiskId'] = ram_disk_id

        if security_group_names and not isinstance(security_group_names, list):
            raise TypeError('Expected property security_group_names to be a list')
        __self__.security_group_names = security_group_names
        """
        A list of security group names to associate with. If you are creating Instances in a VPC, use
        `vpc_security_group_ids` instead.
        """
        __props__['securityGroupNames'] = security_group_names

        if tag_specifications and not isinstance(tag_specifications, list):
            raise TypeError('Expected property tag_specifications to be a list')
        __self__.tag_specifications = tag_specifications
        """
        The tags to apply to the resources during launch. See Tags below for more details.
        """
        __props__['tagSpecifications'] = tag_specifications

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags to assign to the launch template.
        """
        __props__['tags'] = tags

        if user_data and not isinstance(user_data, basestring):
            raise TypeError('Expected property user_data to be a basestring')
        __self__.user_data = user_data
        """
        The Base64-encoded user data to provide when launching the instance.
        """
        __props__['userData'] = user_data

        if vpc_security_group_ids and not isinstance(vpc_security_group_ids, list):
            raise TypeError('Expected property vpc_security_group_ids to be a list')
        __self__.vpc_security_group_ids = vpc_security_group_ids
        """
        A list of security group IDs to associate with.
        """
        __props__['vpcSecurityGroupIds'] = vpc_security_group_ids

        __self__.arn = pulumi.runtime.UNKNOWN
        """
        Amazon Resource Name (ARN) of the launch template.
        """
        __self__.default_version = pulumi.runtime.UNKNOWN
        """
        The default version of the launch template.
        """
        __self__.latest_version = pulumi.runtime.UNKNOWN
        """
        The latest version of the launch template.
        """

        super(LaunchTemplate, __self__).__init__(
            'aws:ec2/launchTemplate:LaunchTemplate',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'arn' in outs:
            self.arn = outs['arn']
        if 'blockDeviceMappings' in outs:
            self.block_device_mappings = outs['blockDeviceMappings']
        if 'creditSpecification' in outs:
            self.credit_specification = outs['creditSpecification']
        if 'defaultVersion' in outs:
            self.default_version = outs['defaultVersion']
        if 'description' in outs:
            self.description = outs['description']
        if 'disableApiTermination' in outs:
            self.disable_api_termination = outs['disableApiTermination']
        if 'ebsOptimized' in outs:
            self.ebs_optimized = outs['ebsOptimized']
        if 'elasticGpuSpecifications' in outs:
            self.elastic_gpu_specifications = outs['elasticGpuSpecifications']
        if 'iamInstanceProfile' in outs:
            self.iam_instance_profile = outs['iamInstanceProfile']
        if 'imageId' in outs:
            self.image_id = outs['imageId']
        if 'instanceInitiatedShutdownBehavior' in outs:
            self.instance_initiated_shutdown_behavior = outs['instanceInitiatedShutdownBehavior']
        if 'instanceMarketOptions' in outs:
            self.instance_market_options = outs['instanceMarketOptions']
        if 'instanceType' in outs:
            self.instance_type = outs['instanceType']
        if 'kernelId' in outs:
            self.kernel_id = outs['kernelId']
        if 'keyName' in outs:
            self.key_name = outs['keyName']
        if 'latestVersion' in outs:
            self.latest_version = outs['latestVersion']
        if 'monitoring' in outs:
            self.monitoring = outs['monitoring']
        if 'name' in outs:
            self.name = outs['name']
        if 'namePrefix' in outs:
            self.name_prefix = outs['namePrefix']
        if 'networkInterfaces' in outs:
            self.network_interfaces = outs['networkInterfaces']
        if 'placement' in outs:
            self.placement = outs['placement']
        if 'ramDiskId' in outs:
            self.ram_disk_id = outs['ramDiskId']
        if 'securityGroupNames' in outs:
            self.security_group_names = outs['securityGroupNames']
        if 'tagSpecifications' in outs:
            self.tag_specifications = outs['tagSpecifications']
        if 'tags' in outs:
            self.tags = outs['tags']
        if 'userData' in outs:
            self.user_data = outs['userData']
        if 'vpcSecurityGroupIds' in outs:
            self.vpc_security_group_ids = outs['vpcSecurityGroupIds']
