# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Attachment(pulumi.CustomResource):
    """
    Attaches an EC2 instance to an Elastic Load Balancer (ELB). For attaching resources with Application Load Balancer (ALB) or Network Load Balancer (NLB), see the [`aws_lb_target_group_attachment` resource](https://www.terraform.io/docs/providers/aws/r/lb_target_group_attachment.html).
    
    ~> **NOTE on ELB Instances and ELB Attachments:** Terraform currently provides
    both a standalone ELB Attachment resource (describing an instance attached to
    an ELB), and an Elastic Load Balancer resource with
    `instances` defined in-line. At this time you cannot use an ELB with in-line
    instances in conjunction with an ELB Attachment resource. Doing so will cause a
    conflict and will overwrite attachments.
    """
    def __init__(__self__, __name__, __opts__=None, elb=None, instance=None):
        """Create a Attachment resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not elb:
            raise TypeError('Missing required property elb')
        elif not isinstance(elb, basestring):
            raise TypeError('Expected property elb to be a basestring')
        __self__.elb = elb
        """
        The name of the ELB.
        """
        __props__['elb'] = elb

        if not instance:
            raise TypeError('Missing required property instance')
        elif not isinstance(instance, basestring):
            raise TypeError('Expected property instance to be a basestring')
        __self__.instance = instance
        """
        Instance ID to place in the ELB pool.
        """
        __props__['instance'] = instance

        super(Attachment, __self__).__init__(
            'aws:elasticloadbalancing/attachment:Attachment',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'elb' in outs:
            self.elb = outs['elb']
        if 'instance' in outs:
            self.instance = outs['instance']
