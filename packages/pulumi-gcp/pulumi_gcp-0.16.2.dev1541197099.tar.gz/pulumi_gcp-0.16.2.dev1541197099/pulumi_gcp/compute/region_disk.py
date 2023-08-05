# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class RegionDisk(pulumi.CustomResource):
    def __init__(__self__, __name__, __opts__=None, description=None, disk_encryption_key=None, labels=None, name=None, project=None, region=None, replica_zones=None, size=None, snapshot=None, source_snapshot_encryption_key=None, type=None):
        """Create a RegionDisk resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        __props__['description'] = description

        if disk_encryption_key and not isinstance(disk_encryption_key, dict):
            raise TypeError('Expected property disk_encryption_key to be a dict')
        __self__.disk_encryption_key = disk_encryption_key
        __props__['diskEncryptionKey'] = disk_encryption_key

        if labels and not isinstance(labels, dict):
            raise TypeError('Expected property labels to be a dict')
        __self__.labels = labels
        __props__['labels'] = labels

        if name and not isinstance(name, basestring):
            raise TypeError('Expected property name to be a basestring')
        __self__.name = name
        __props__['name'] = name

        if project and not isinstance(project, basestring):
            raise TypeError('Expected property project to be a basestring')
        __self__.project = project
        """
        The ID of the project in which the resource belongs.
        If it is not provided, the provider project is used.
        """
        __props__['project'] = project

        if region and not isinstance(region, basestring):
            raise TypeError('Expected property region to be a basestring')
        __self__.region = region
        __props__['region'] = region

        if not replica_zones:
            raise TypeError('Missing required property replica_zones')
        elif not isinstance(replica_zones, list):
            raise TypeError('Expected property replica_zones to be a list')
        __self__.replica_zones = replica_zones
        __props__['replicaZones'] = replica_zones

        if size and not isinstance(size, int):
            raise TypeError('Expected property size to be a int')
        __self__.size = size
        __props__['size'] = size

        if snapshot and not isinstance(snapshot, basestring):
            raise TypeError('Expected property snapshot to be a basestring')
        __self__.snapshot = snapshot
        __props__['snapshot'] = snapshot

        if source_snapshot_encryption_key and not isinstance(source_snapshot_encryption_key, dict):
            raise TypeError('Expected property source_snapshot_encryption_key to be a dict')
        __self__.source_snapshot_encryption_key = source_snapshot_encryption_key
        __props__['sourceSnapshotEncryptionKey'] = source_snapshot_encryption_key

        if type and not isinstance(type, basestring):
            raise TypeError('Expected property type to be a basestring')
        __self__.type = type
        __props__['type'] = type

        __self__.creation_timestamp = pulumi.runtime.UNKNOWN
        __self__.label_fingerprint = pulumi.runtime.UNKNOWN
        __self__.last_attach_timestamp = pulumi.runtime.UNKNOWN
        __self__.last_detach_timestamp = pulumi.runtime.UNKNOWN
        __self__.self_link = pulumi.runtime.UNKNOWN
        """
        The URI of the created resource.
        """
        __self__.source_snapshot_id = pulumi.runtime.UNKNOWN
        __self__.users = pulumi.runtime.UNKNOWN

        super(RegionDisk, __self__).__init__(
            'gcp:compute/regionDisk:RegionDisk',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'creationTimestamp' in outs:
            self.creation_timestamp = outs['creationTimestamp']
        if 'description' in outs:
            self.description = outs['description']
        if 'diskEncryptionKey' in outs:
            self.disk_encryption_key = outs['diskEncryptionKey']
        if 'labelFingerprint' in outs:
            self.label_fingerprint = outs['labelFingerprint']
        if 'labels' in outs:
            self.labels = outs['labels']
        if 'lastAttachTimestamp' in outs:
            self.last_attach_timestamp = outs['lastAttachTimestamp']
        if 'lastDetachTimestamp' in outs:
            self.last_detach_timestamp = outs['lastDetachTimestamp']
        if 'name' in outs:
            self.name = outs['name']
        if 'project' in outs:
            self.project = outs['project']
        if 'region' in outs:
            self.region = outs['region']
        if 'replicaZones' in outs:
            self.replica_zones = outs['replicaZones']
        if 'selfLink' in outs:
            self.self_link = outs['selfLink']
        if 'size' in outs:
            self.size = outs['size']
        if 'snapshot' in outs:
            self.snapshot = outs['snapshot']
        if 'sourceSnapshotEncryptionKey' in outs:
            self.source_snapshot_encryption_key = outs['sourceSnapshotEncryptionKey']
        if 'sourceSnapshotId' in outs:
            self.source_snapshot_id = outs['sourceSnapshotId']
        if 'type' in outs:
            self.type = outs['type']
        if 'users' in outs:
            self.users = outs['users']
