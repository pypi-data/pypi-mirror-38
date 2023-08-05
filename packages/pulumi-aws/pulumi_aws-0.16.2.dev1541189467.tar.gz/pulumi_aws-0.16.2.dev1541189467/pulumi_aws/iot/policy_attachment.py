# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class PolicyAttachment(pulumi.CustomResource):
    """
    Provides an IoT policy attachment.
    """
    def __init__(__self__, __name__, __opts__=None, policy=None, target=None):
        """Create a PolicyAttachment resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not policy:
            raise TypeError('Missing required property policy')
        elif not isinstance(policy, basestring):
            raise TypeError('Expected property policy to be a basestring')
        __self__.policy = policy
        """
        The name of the policy to attach.
        """
        __props__['policy'] = policy

        if not target:
            raise TypeError('Missing required property target')
        elif not isinstance(target, basestring):
            raise TypeError('Expected property target to be a basestring')
        __self__.target = target
        """
        The identity to which the policy is attached.
        """
        __props__['target'] = target

        super(PolicyAttachment, __self__).__init__(
            'aws:iot/policyAttachment:PolicyAttachment',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'policy' in outs:
            self.policy = outs['policy']
        if 'target' in outs:
            self.target = outs['target']
