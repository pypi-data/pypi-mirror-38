# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class KeyRingIAMBinding(pulumi.CustomResource):
    """
    Three different resources help you manage your IAM policy for KMS key ring. Each of these resources serves a different use case:
    
    * `google_kms_key_ring_iam_policy`: Authoritative. Sets the IAM policy for the key ring and replaces any existing policy already attached.
    * `google_kms_key_ring_iam_binding`: Authoritative for a given role. Updates the IAM policy to grant a role to a list of members. Other roles within the IAM policy for the key ring are preserved.
    * `google_kms_key_ring_iam_member`: Non-authoritative. Updates the IAM policy to grant a role to a new member. Other members for the role for the key ring are preserved.
    
    ~> **Note:** `google_kms_key_ring_iam_policy` **cannot** be used in conjunction with `google_kms_key_ring_iam_binding` and `google_kms_key_ring_iam_member` or they will fight over what your policy should be.
    
    ~> **Note:** `google_kms_key_ring_iam_binding` resources **can be** used in conjunction with `google_kms_key_ring_iam_member` resources **only if** they do not grant privilege to the same role.
    """
    def __init__(__self__, __name__, __opts__=None, key_ring_id=None, members=None, role=None):
        """Create a KeyRingIAMBinding resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if not key_ring_id:
            raise TypeError('Missing required property key_ring_id')
        elif not isinstance(key_ring_id, basestring):
            raise TypeError('Expected property key_ring_id to be a basestring')
        __self__.key_ring_id = key_ring_id
        """
        The key ring ID, in the form
        `{project_id}/{location_name}/{key_ring_name}` or
        `{location_name}/{key_ring_name}`. In the second form, the provider's
        project setting will be used as a fallback.
        """
        __props__['keyRingId'] = key_ring_id

        if not members:
            raise TypeError('Missing required property members')
        elif not isinstance(members, list):
            raise TypeError('Expected property members to be a list')
        __self__.members = members
        __props__['members'] = members

        if not role:
            raise TypeError('Missing required property role')
        elif not isinstance(role, basestring):
            raise TypeError('Expected property role to be a basestring')
        __self__.role = role
        """
        The role that should be applied. Only one
        `google_kms_key_ring_iam_binding` can be used per role. Note that custom roles must be of the format
        `[projects|organizations]/{parent-name}/roles/{role-name}`.
        """
        __props__['role'] = role

        __self__.etag = pulumi.runtime.UNKNOWN
        """
        (Computed) The etag of the key ring's IAM policy.
        """

        super(KeyRingIAMBinding, __self__).__init__(
            'gcp:kms/keyRingIAMBinding:KeyRingIAMBinding',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'etag' in outs:
            self.etag = outs['etag']
        if 'keyRingId' in outs:
            self.key_ring_id = outs['keyRingId']
        if 'members' in outs:
            self.members = outs['members']
        if 'role' in outs:
            self.role = outs['role']
