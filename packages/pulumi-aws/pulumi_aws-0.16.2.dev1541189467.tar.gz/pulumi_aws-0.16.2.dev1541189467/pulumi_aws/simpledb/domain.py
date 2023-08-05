# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Domain(pulumi.CustomResource):
    """
    Provides a SimpleDB domain resource
    """
    def __init__(__self__, __name__, __opts__=None, name=None):
        """Create a Domain resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        """
        The name of the SimpleDB domain
        """
        __props__['name'] = name

        super(Domain, __self__).__init__(
            'aws:simpledb/domain:Domain',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'name' in outs:
            self.name = outs['name']
