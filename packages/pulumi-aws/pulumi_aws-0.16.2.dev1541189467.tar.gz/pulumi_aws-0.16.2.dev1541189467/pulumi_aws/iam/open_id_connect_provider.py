# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class OpenIdConnectProvider(pulumi.CustomResource):
    """
    Provides an IAM OpenID Connect provider.
    """
    def __init__(__self__, __name__, __opts__=None, client_id_lists=None, thumbprint_lists=None, url=None):
        """Create a OpenIdConnectProvider resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not client_id_lists:
            raise TypeError('Missing required property client_id_lists')
        elif not isinstance(client_id_lists, list):
            raise TypeError('Expected property client_id_lists to be a list')
        __self__.client_id_lists = client_id_lists
        """
        A list of client IDs (also known as audiences). When a mobile or web app registers with an OpenID Connect provider, they establish a value that identifies the application. (This is the value that's sent as the client_id parameter on OAuth requests.)
        """
        __props__['clientIdLists'] = client_id_lists

        if not thumbprint_lists:
            raise TypeError('Missing required property thumbprint_lists')
        elif not isinstance(thumbprint_lists, list):
            raise TypeError('Expected property thumbprint_lists to be a list')
        __self__.thumbprint_lists = thumbprint_lists
        """
        A list of server certificate thumbprints for the OpenID Connect (OIDC) identity provider's server certificate(s). 
        """
        __props__['thumbprintLists'] = thumbprint_lists

        if not url:
            raise TypeError('Missing required property url')
        elif not isinstance(url, basestring):
            raise TypeError('Expected property url to be a basestring')
        __self__.url = url
        """
        The URL of the identity provider. Corresponds to the _iss_ claim.
        """
        __props__['url'] = url

        __self__.arn = pulumi.runtime.UNKNOWN
        """
        The ARN assigned by AWS for this provider.
        """

        super(OpenIdConnectProvider, __self__).__init__(
            'aws:iam/openIdConnectProvider:OpenIdConnectProvider',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'arn' in outs:
            self.arn = outs['arn']
        if 'clientIdLists' in outs:
            self.client_id_lists = outs['clientIdLists']
        if 'thumbprintLists' in outs:
            self.thumbprint_lists = outs['thumbprintLists']
        if 'url' in outs:
            self.url = outs['url']
