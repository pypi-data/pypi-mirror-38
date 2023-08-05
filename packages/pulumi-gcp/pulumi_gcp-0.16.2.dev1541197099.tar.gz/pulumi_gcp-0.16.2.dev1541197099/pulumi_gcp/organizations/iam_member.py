# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class IAMMember(pulumi.CustomResource):
    """
    Allows creation and management of a single member for a single binding within
    the IAM policy for an existing Google Cloud Platform Organization.
    
    ~> **Note:** This resource __must not__ be used in conjunction with
       `google_organization_iam_binding` for the __same role__ or they will fight over
       what your policy should be.
    """
    def __init__(__self__, __name__, __opts__=None, member=None, org_id=None, role=None):
        """Create a IAMMember resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not member:
            raise TypeError('Missing required property member')
        elif not isinstance(member, basestring):
            raise TypeError('Expected property member to be a basestring')
        __self__.member = member
        """
        The user that the role should apply to.
        """
        __props__['member'] = member

        if not org_id:
            raise TypeError('Missing required property org_id')
        elif not isinstance(org_id, basestring):
            raise TypeError('Expected property org_id to be a basestring')
        __self__.org_id = org_id
        """
        The numeric ID of the organization in which you want to create a custom role.
        """
        __props__['orgId'] = org_id

        if not role:
            raise TypeError('Missing required property role')
        elif not isinstance(role, basestring):
            raise TypeError('Expected property role to be a basestring')
        __self__.role = role
        """
        The role that should be applied. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        __props__['role'] = role

        __self__.etag = pulumi.runtime.UNKNOWN
        """
        (Computed) The etag of the organization's IAM policy.
        """

        super(IAMMember, __self__).__init__(
            'gcp:organizations/iAMMember:IAMMember',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'etag' in outs:
            self.etag = outs['etag']
        if 'member' in outs:
            self.member = outs['member']
        if 'orgId' in outs:
            self.org_id = outs['orgId']
        if 'role' in outs:
            self.role = outs['role']
