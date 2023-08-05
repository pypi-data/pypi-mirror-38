# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class SSLCertificate(pulumi.CustomResource):
    def __init__(__self__, __name__, __opts__=None, certificate=None, description=None, name=None, name_prefix=None, private_key=None, project=None):
        """Create a SSLCertificate resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not certificate:
            raise TypeError('Missing required property certificate')
        elif not isinstance(certificate, basestring):
            raise TypeError('Expected property certificate to be a basestring')
        __self__.certificate = certificate
        __props__['certificate'] = certificate

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        __props__['description'] = description

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        __props__['name'] = name

        if name_prefix and not isinstance(name_prefix, basestring):
            raise TypeError('Expected property name_prefix to be a basestring')
        __self__.name_prefix = name_prefix
        """
        Creates a unique name beginning with the
        specified prefix. Conflicts with `name`.
        """
        __props__['namePrefix'] = name_prefix

        if not private_key:
            raise TypeError('Missing required property private_key')
        elif not isinstance(private_key, basestring):
            raise TypeError('Expected property private_key to be a basestring')
        __self__.private_key = private_key
        __props__['privateKey'] = private_key

        if project and not isinstance(project, basestring):
            raise TypeError('Expected property project to be a basestring')
        __self__.project = project
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        __props__['project'] = project

        __self__.certificate_id = pulumi.runtime.UNKNOWN
        __self__.creation_timestamp = pulumi.runtime.UNKNOWN
        __self__.self_link = pulumi.runtime.UNKNOWN
        """
        The URI of the created resource.
        """

        super(SSLCertificate, __self__).__init__(
            'gcp:compute/sSLCertificate:SSLCertificate',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'certificate' in outs:
            self.certificate = outs['certificate']
        if 'certificateId' in outs:
            self.certificate_id = outs['certificateId']
        if 'creationTimestamp' in outs:
            self.creation_timestamp = outs['creationTimestamp']
        if 'description' in outs:
            self.description = outs['description']
        if 'name' in outs:
            self.name = outs['name']
        if 'namePrefix' in outs:
            self.name_prefix = outs['namePrefix']
        if 'privateKey' in outs:
            self.private_key = outs['privateKey']
        if 'project' in outs:
            self.project = outs['project']
        if 'selfLink' in outs:
            self.self_link = outs['selfLink']
