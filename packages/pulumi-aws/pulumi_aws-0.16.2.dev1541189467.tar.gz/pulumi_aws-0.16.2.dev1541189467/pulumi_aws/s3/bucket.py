# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Bucket(pulumi.CustomResource):
    """
    Provides a S3 bucket resource.
    """
    def __init__(__self__, __name__, __opts__=None, acceleration_status=None, acl=None, arn=None, bucket=None, bucket_prefix=None, cors_rules=None, force_destroy=None, hosted_zone_id=None, lifecycle_rules=None, loggings=None, policy=None, region=None, replication_configuration=None, request_payer=None, server_side_encryption_configuration=None, tags=None, versioning=None, website=None, website_domain=None, website_endpoint=None):
        """Create a Bucket resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if acceleration_status and not isinstance(acceleration_status, basestring):
            raise TypeError('Expected property acceleration_status to be a basestring')
        __self__.acceleration_status = acceleration_status
        """
        Sets the accelerate configuration of an existing bucket. Can be `Enabled` or `Suspended`.
        """
        __props__['accelerationStatus'] = acceleration_status

        if acl and not isinstance(acl, basestring):
            raise TypeError('Expected property acl to be a basestring')
        __self__.acl = acl
        """
        The [canned ACL](https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl) to apply. Defaults to "private".
        """
        __props__['acl'] = acl

        if arn and not isinstance(arn, basestring):
            raise TypeError('Expected property arn to be a basestring')
        __self__.arn = arn
        """
        The ARN of the bucket. Will be of format `arn:aws:s3:::bucketname`.
        """
        __props__['arn'] = arn

        if bucket and not isinstance(bucket, basestring):
            raise TypeError('Expected property bucket to be a basestring')
        __self__.bucket = bucket
        """
        The ARN of the S3 bucket where you want Amazon S3 to store replicas of the object identified by the rule.
        """
        __props__['bucket'] = bucket

        if bucket_prefix and not isinstance(bucket_prefix, basestring):
            raise TypeError('Expected property bucket_prefix to be a basestring')
        __self__.bucket_prefix = bucket_prefix
        """
        Creates a unique bucket name beginning with the specified prefix. Conflicts with `bucket`.
        """
        __props__['bucketPrefix'] = bucket_prefix

        if cors_rules and not isinstance(cors_rules, list):
            raise TypeError('Expected property cors_rules to be a list')
        __self__.cors_rules = cors_rules
        """
        A rule of [Cross-Origin Resource Sharing](https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html) (documented below).
        """
        __props__['corsRules'] = cors_rules

        if force_destroy and not isinstance(force_destroy, bool):
            raise TypeError('Expected property force_destroy to be a bool')
        __self__.force_destroy = force_destroy
        """
        A boolean that indicates all objects should be deleted from the bucket so that the bucket can be destroyed without error. These objects are *not* recoverable.
        """
        __props__['forceDestroy'] = force_destroy

        if hosted_zone_id and not isinstance(hosted_zone_id, basestring):
            raise TypeError('Expected property hosted_zone_id to be a basestring')
        __self__.hosted_zone_id = hosted_zone_id
        """
        The [Route 53 Hosted Zone ID](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_website_region_endpoints) for this bucket's region.
        """
        __props__['hostedZoneId'] = hosted_zone_id

        if lifecycle_rules and not isinstance(lifecycle_rules, list):
            raise TypeError('Expected property lifecycle_rules to be a list')
        __self__.lifecycle_rules = lifecycle_rules
        """
        A configuration of [object lifecycle management](http://docs.aws.amazon.com/AmazonS3/latest/dev/object-lifecycle-mgmt.html) (documented below).
        """
        __props__['lifecycleRules'] = lifecycle_rules

        if loggings and not isinstance(loggings, list):
            raise TypeError('Expected property loggings to be a list')
        __self__.loggings = loggings
        """
        A settings of [bucket logging](https://docs.aws.amazon.com/AmazonS3/latest/UG/ManagingBucketLogging.html) (documented below).
        """
        __props__['loggings'] = loggings

        if policy and not isinstance(policy, basestring):
            raise TypeError('Expected property policy to be a basestring')
        __self__.policy = policy
        """
        A valid [bucket policy](https://docs.aws.amazon.com/AmazonS3/latest/dev/example-bucket-policies.html) JSON document. Note that if the policy document is not specific enough (but still valid), Terraform may view the policy as constantly changing in a `terraform plan`. In this case, please make sure you use the verbose/specific version of the policy. For more information about building AWS IAM policy documents with Terraform, see the [AWS IAM Policy Document Guide](https://www.terraform.io/docs/providers/aws/guides/iam-policy-documents.html).
        """
        __props__['policy'] = policy

        if region and not isinstance(region, basestring):
            raise TypeError('Expected property region to be a basestring')
        __self__.region = region
        """
        If specified, the AWS region this bucket should reside in. Otherwise, the region used by the callee.
        """
        __props__['region'] = region

        if replication_configuration and not isinstance(replication_configuration, dict):
            raise TypeError('Expected property replication_configuration to be a dict')
        __self__.replication_configuration = replication_configuration
        """
        A configuration of [replication configuration](http://docs.aws.amazon.com/AmazonS3/latest/dev/crr.html) (documented below).
        """
        __props__['replicationConfiguration'] = replication_configuration

        if request_payer and not isinstance(request_payer, basestring):
            raise TypeError('Expected property request_payer to be a basestring')
        __self__.request_payer = request_payer
        """
        Specifies who should bear the cost of Amazon S3 data transfer.
        Can be either `BucketOwner` or `Requester`. By default, the owner of the S3 bucket would incur
        the costs of any data transfer. See [Requester Pays Buckets](http://docs.aws.amazon.com/AmazonS3/latest/dev/RequesterPaysBuckets.html)
        developer guide for more information.
        """
        __props__['requestPayer'] = request_payer

        if server_side_encryption_configuration and not isinstance(server_side_encryption_configuration, dict):
            raise TypeError('Expected property server_side_encryption_configuration to be a dict')
        __self__.server_side_encryption_configuration = server_side_encryption_configuration
        """
        A configuration of [server-side encryption configuration](http://docs.aws.amazon.com/AmazonS3/latest/dev/bucket-encryption.html) (documented below)
        """
        __props__['serverSideEncryptionConfiguration'] = server_side_encryption_configuration

        if tags and not isinstance(tags, dict):
            raise TypeError('Expected property tags to be a dict')
        __self__.tags = tags
        """
        A mapping of tags that identifies subset of objects to which the rule applies.
        The rule applies only to objects having all the tags in its tagset.
        """
        __props__['tags'] = tags

        if versioning and not isinstance(versioning, dict):
            raise TypeError('Expected property versioning to be a dict')
        __self__.versioning = versioning
        """
        A state of [versioning](https://docs.aws.amazon.com/AmazonS3/latest/dev/Versioning.html) (documented below)
        """
        __props__['versioning'] = versioning

        if website and not isinstance(website, dict):
            raise TypeError('Expected property website to be a dict')
        __self__.website = website
        """
        A website object (documented below).
        """
        __props__['website'] = website

        if website_domain and not isinstance(website_domain, basestring):
            raise TypeError('Expected property website_domain to be a basestring')
        __self__.website_domain = website_domain
        """
        The domain of the website endpoint, if the bucket is configured with a website. If not, this will be an empty string. This is used to create Route 53 alias records.
        """
        __props__['websiteDomain'] = website_domain

        if website_endpoint and not isinstance(website_endpoint, basestring):
            raise TypeError('Expected property website_endpoint to be a basestring')
        __self__.website_endpoint = website_endpoint
        """
        The website endpoint, if the bucket is configured with a website. If not, this will be an empty string.
        """
        __props__['websiteEndpoint'] = website_endpoint

        __self__.bucket_domain_name = pulumi.runtime.UNKNOWN
        """
        The bucket domain name. Will be of format `bucketname.s3.amazonaws.com`.
        """
        __self__.bucket_regional_domain_name = pulumi.runtime.UNKNOWN
        """
        The bucket region-specific domain name. The bucket domain name including the region name, please refer [here](https://docs.aws.amazon.com/general/latest/gr/rande.html#s3_region) for format. Note: The AWS CloudFront allows specifying S3 region-specific endpoint when creating S3 origin, it will prevent [redirect issues](https://forums.aws.amazon.com/thread.jspa?threadID=216814) from CloudFront to S3 Origin URL.
        """

        super(Bucket, __self__).__init__(
            'aws:s3/bucket:Bucket',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'accelerationStatus' in outs:
            self.acceleration_status = outs['accelerationStatus']
        if 'acl' in outs:
            self.acl = outs['acl']
        if 'arn' in outs:
            self.arn = outs['arn']
        if 'bucket' in outs:
            self.bucket = outs['bucket']
        if 'bucketDomainName' in outs:
            self.bucket_domain_name = outs['bucketDomainName']
        if 'bucketPrefix' in outs:
            self.bucket_prefix = outs['bucketPrefix']
        if 'bucketRegionalDomainName' in outs:
            self.bucket_regional_domain_name = outs['bucketRegionalDomainName']
        if 'corsRules' in outs:
            self.cors_rules = outs['corsRules']
        if 'forceDestroy' in outs:
            self.force_destroy = outs['forceDestroy']
        if 'hostedZoneId' in outs:
            self.hosted_zone_id = outs['hostedZoneId']
        if 'lifecycleRules' in outs:
            self.lifecycle_rules = outs['lifecycleRules']
        if 'loggings' in outs:
            self.loggings = outs['loggings']
        if 'policy' in outs:
            self.policy = outs['policy']
        if 'region' in outs:
            self.region = outs['region']
        if 'replicationConfiguration' in outs:
            self.replication_configuration = outs['replicationConfiguration']
        if 'requestPayer' in outs:
            self.request_payer = outs['requestPayer']
        if 'serverSideEncryptionConfiguration' in outs:
            self.server_side_encryption_configuration = outs['serverSideEncryptionConfiguration']
        if 'tags' in outs:
            self.tags = outs['tags']
        if 'versioning' in outs:
            self.versioning = outs['versioning']
        if 'website' in outs:
            self.website = outs['website']
        if 'websiteDomain' in outs:
            self.website_domain = outs['websiteDomain']
        if 'websiteEndpoint' in outs:
            self.website_endpoint = outs['websiteEndpoint']
