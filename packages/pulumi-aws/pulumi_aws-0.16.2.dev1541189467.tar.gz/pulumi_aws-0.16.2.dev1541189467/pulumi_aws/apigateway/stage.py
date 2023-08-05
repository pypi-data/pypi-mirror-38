# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Stage(pulumi.CustomResource):
    """
    Provides an API Gateway Stage.
    """
    def __init__(__self__, __name__, __opts__=None, access_log_settings=None, cache_cluster_enabled=None, cache_cluster_size=None, client_certificate_id=None, deployment=None, description=None, documentation_version=None, rest_api=None, stage_name=None, tags=None, variables=None, xray_tracing_enabled=None):
        """Create a Stage resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if access_log_settings and not isinstance(access_log_settings, dict):
            raise TypeError('Expected property access_log_settings to be a dict')
        __self__.access_log_settings = access_log_settings
        """
        Enables access logs for the API stage. Detailed below.
        """
        __props__['accessLogSettings'] = access_log_settings

        if cache_cluster_enabled and not isinstance(cache_cluster_enabled, bool):
            raise TypeError('Expected property cache_cluster_enabled to be a bool')
        __self__.cache_cluster_enabled = cache_cluster_enabled
        """
        Specifies whether a cache cluster is enabled for the stage
        """
        __props__['cacheClusterEnabled'] = cache_cluster_enabled

        if cache_cluster_size and not isinstance(cache_cluster_size, basestring):
            raise TypeError('Expected property cache_cluster_size to be a basestring')
        __self__.cache_cluster_size = cache_cluster_size
        """
        The size of the cache cluster for the stage, if enabled.
        Allowed values include `0.5`, `1.6`, `6.1`, `13.5`, `28.4`, `58.2`, `118` and `237`.
        """
        __props__['cacheClusterSize'] = cache_cluster_size

        if client_certificate_id and not isinstance(client_certificate_id, basestring):
            raise TypeError('Expected property client_certificate_id to be a basestring')
        __self__.client_certificate_id = client_certificate_id
        """
        The identifier of a client certificate for the stage.
        """
        __props__['clientCertificateId'] = client_certificate_id

        if not deployment:
            raise TypeError('Missing required property deployment')
        elif not isinstance(deployment, basestring):
            raise TypeError('Expected property deployment to be a basestring')
        __self__.deployment = deployment
        """
        The ID of the deployment that the stage points to
        """
        __props__['deployment'] = deployment

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        """
        The description of the stage
        """
        __props__['description'] = description

        if documentation_version and not isinstance(documentation_version, basestring):
            raise TypeError('Expected property documentation_version to be a basestring')
        __self__.documentation_version = documentation_version
        """
        The version of the associated API documentation
        """
        __props__['documentationVersion'] = documentation_version

        if not rest_api:
            raise TypeError('Missing required property rest_api')
        elif not isinstance(rest_api, basestring):
            raise TypeError('Expected property rest_api to be a basestring')
        __self__.rest_api = rest_api
        """
        The ID of the associated REST API
        """
        __props__['restApi'] = rest_api

        if not stage_name:
            raise TypeError('Missing required property stage_name')
        elif not isinstance(stage_name, basestring):
            raise TypeError('Expected property stage_name to be a basestring')
        __self__.stage_name = stage_name
        """
        The name of the stage
        """
        __props__['stageName'] = stage_name

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags to assign to the resource.
        """
        __props__['tags'] = tags

        if variables and not isinstance(variables, dict):
            raise TypeError('Expected property variables to be a dict')
        __self__.variables = variables
        """
        A map that defines the stage variables
        """
        __props__['variables'] = variables

        if xray_tracing_enabled and not isinstance(xray_tracing_enabled, bool):
            raise TypeError('Expected property xray_tracing_enabled to be a bool')
        __self__.xray_tracing_enabled = xray_tracing_enabled
        """
        Whether active tracing with X-ray is enabled. Defaults to `false`.
        """
        __props__['xrayTracingEnabled'] = xray_tracing_enabled

        __self__.execution_arn = pulumi.runtime.UNKNOWN
        """
        The execution ARN to be used in [`lambda_permission`](https://www.terraform.io/docs/providers/aws/r/lambda_permission.html)'s `source_arn`
        when allowing API Gateway to invoke a Lambda function,
        e.g. `arn:aws:execute-api:eu-west-2:123456789012:z4675bid1j/prod`
        """
        __self__.invoke_url = pulumi.runtime.UNKNOWN
        """
        The URL to invoke the API pointing to the stage,
        e.g. `https://z4675bid1j.execute-api.eu-west-2.amazonaws.com/prod`
        """

        super(Stage, __self__).__init__(
            'aws:apigateway/stage:Stage',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'accessLogSettings' in outs:
            self.access_log_settings = outs['accessLogSettings']
        if 'cacheClusterEnabled' in outs:
            self.cache_cluster_enabled = outs['cacheClusterEnabled']
        if 'cacheClusterSize' in outs:
            self.cache_cluster_size = outs['cacheClusterSize']
        if 'clientCertificateId' in outs:
            self.client_certificate_id = outs['clientCertificateId']
        if 'deployment' in outs:
            self.deployment = outs['deployment']
        if 'description' in outs:
            self.description = outs['description']
        if 'documentationVersion' in outs:
            self.documentation_version = outs['documentationVersion']
        if 'executionArn' in outs:
            self.execution_arn = outs['executionArn']
        if 'invokeUrl' in outs:
            self.invoke_url = outs['invokeUrl']
        if 'restApi' in outs:
            self.rest_api = outs['restApi']
        if 'stageName' in outs:
            self.stage_name = outs['stageName']
        if 'tags' in outs:
            self.tags = outs['tags']
        if 'variables' in outs:
            self.variables = outs['variables']
        if 'xrayTracingEnabled' in outs:
            self.xray_tracing_enabled = outs['xrayTracingEnabled']
