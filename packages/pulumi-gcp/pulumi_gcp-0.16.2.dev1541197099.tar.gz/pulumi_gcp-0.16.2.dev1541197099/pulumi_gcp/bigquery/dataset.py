# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class Dataset(pulumi.CustomResource):
    """
    Creates a dataset resource for Google BigQuery. For more information see
    [the official documentation](https://cloud.google.com/bigquery/docs/) and
    [API](https://cloud.google.com/bigquery/docs/reference/rest/v2/datasets).
    
    """
    def __init__(__self__, __name__, __opts__=None, accesses=None, dataset_id=None, default_table_expiration_ms=None, description=None, friendly_name=None, labels=None, location=None, project=None):
        """Create a Dataset resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if accesses and not isinstance(accesses, list):
            raise TypeError('Expected property accesses to be a list')
        __self__.accesses = accesses
        """
        An array of objects that define dataset access for
        one or more entities. Structure is documented below.
        """
        __props__['accesses'] = accesses

        if not dataset_id:
            raise TypeError('Missing required property dataset_id')
        elif not isinstance(dataset_id, basestring):
            raise TypeError('Expected property dataset_id to be a basestring')
        __self__.dataset_id = dataset_id
        """
        The ID of the dataset containing this table.
        """
        __props__['datasetId'] = dataset_id

        if default_table_expiration_ms and not isinstance(default_table_expiration_ms, int):
            raise TypeError('Expected property default_table_expiration_ms to be a int')
        __self__.default_table_expiration_ms = default_table_expiration_ms
        """
        The default lifetime of all
        tables in the dataset, in milliseconds. The minimum value is 3600000
        milliseconds (one hour).
        """
        __props__['defaultTableExpirationMs'] = default_table_expiration_ms

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        """
        A user-friendly description of the dataset.
        """
        __props__['description'] = description

        if friendly_name and not isinstance(friendly_name, basestring):
            raise TypeError('Expected property friendly_name to be a basestring')
        __self__.friendly_name = friendly_name
        """
        A descriptive name for the dataset.
        """
        __props__['friendlyName'] = friendly_name

        if labels and not isinstance(labels, dict):
            raise TypeError('Expected property labels to be a dict')
        __self__.labels = labels
        """
        A mapping of labels to assign to the resource.
        """
        __props__['labels'] = labels

        if location and not isinstance(location, basestring):
            raise TypeError('Expected property location to be a basestring')
        __self__.location = location
        """
        The geographic location where the dataset should reside.
        See [official docs](https://cloud.google.com/bigquery/docs/dataset-locations).
        """
        __props__['location'] = location

        if project and not isinstance(project, basestring):
            raise TypeError('Expected property project to be a basestring')
        __self__.project = project
        """
        The ID of the project in which the resource belongs. If it
        is not provided, the provider project is used.
        """
        __props__['project'] = project

        __self__.creation_time = pulumi.runtime.UNKNOWN
        """
        The time when this dataset was created, in milliseconds since the epoch.
        """
        __self__.etag = pulumi.runtime.UNKNOWN
        """
        A hash of the resource.
        """
        __self__.last_modified_time = pulumi.runtime.UNKNOWN
        """
        The date when this dataset or any of its tables was last modified,
        in milliseconds since the epoch.
        """
        __self__.self_link = pulumi.runtime.UNKNOWN
        """
        The URI of the created resource.
        """

        super(Dataset, __self__).__init__(
            'gcp:bigquery/dataset:Dataset',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'accesses' in outs:
            self.accesses = outs['accesses']
        if 'creationTime' in outs:
            self.creation_time = outs['creationTime']
        if 'datasetId' in outs:
            self.dataset_id = outs['datasetId']
        if 'defaultTableExpirationMs' in outs:
            self.default_table_expiration_ms = outs['defaultTableExpirationMs']
        if 'description' in outs:
            self.description = outs['description']
        if 'etag' in outs:
            self.etag = outs['etag']
        if 'friendlyName' in outs:
            self.friendly_name = outs['friendlyName']
        if 'labels' in outs:
            self.labels = outs['labels']
        if 'lastModifiedTime' in outs:
            self.last_modified_time = outs['lastModifiedTime']
        if 'location' in outs:
            self.location = outs['location']
        if 'project' in outs:
            self.project = outs['project']
        if 'selfLink' in outs:
            self.self_link = outs['selfLink']
