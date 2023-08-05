# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import pulumi
import pulumi.runtime
from .. import utilities

class HealthCheck(pulumi.CustomResource):
    def __init__(__self__, __name__, __opts__=None, check_interval_sec=None, description=None, healthy_threshold=None, http_health_check=None, https_health_check=None, name=None, project=None, ssl_health_check=None, tcp_health_check=None, timeout_sec=None, unhealthy_threshold=None):
        """Create a HealthCheck resource with the given unique name, props, and options."""
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, basestring):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        if check_interval_sec and not isinstance(check_interval_sec, int):
            raise TypeError('Expected property check_interval_sec to be a int')
        __self__.check_interval_sec = check_interval_sec
        __props__['checkIntervalSec'] = check_interval_sec

        if description and not isinstance(description, basestring):
            raise TypeError('Expected property description to be a basestring')
        __self__.description = description
        __props__['description'] = description

        if healthy_threshold and not isinstance(healthy_threshold, int):
            raise TypeError('Expected property healthy_threshold to be a int')
        __self__.healthy_threshold = healthy_threshold
        __props__['healthyThreshold'] = healthy_threshold

        if http_health_check and not isinstance(http_health_check, dict):
            raise TypeError('Expected property http_health_check to be a dict')
        __self__.http_health_check = http_health_check
        __props__['httpHealthCheck'] = http_health_check

        if https_health_check and not isinstance(https_health_check, dict):
            raise TypeError('Expected property https_health_check to be a dict')
        __self__.https_health_check = https_health_check
        __props__['httpsHealthCheck'] = https_health_check

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

        if ssl_health_check and not isinstance(ssl_health_check, dict):
            raise TypeError('Expected property ssl_health_check to be a dict')
        __self__.ssl_health_check = ssl_health_check
        __props__['sslHealthCheck'] = ssl_health_check

        if tcp_health_check and not isinstance(tcp_health_check, dict):
            raise TypeError('Expected property tcp_health_check to be a dict')
        __self__.tcp_health_check = tcp_health_check
        __props__['tcpHealthCheck'] = tcp_health_check

        if timeout_sec and not isinstance(timeout_sec, int):
            raise TypeError('Expected property timeout_sec to be a int')
        __self__.timeout_sec = timeout_sec
        __props__['timeoutSec'] = timeout_sec

        if unhealthy_threshold and not isinstance(unhealthy_threshold, int):
            raise TypeError('Expected property unhealthy_threshold to be a int')
        __self__.unhealthy_threshold = unhealthy_threshold
        __props__['unhealthyThreshold'] = unhealthy_threshold

        __self__.creation_timestamp = pulumi.runtime.UNKNOWN
        __self__.self_link = pulumi.runtime.UNKNOWN
        """
        The URI of the created resource.
        """
        __self__.type = pulumi.runtime.UNKNOWN

        super(HealthCheck, __self__).__init__(
            'gcp:compute/healthCheck:HealthCheck',
            __name__,
            __props__,
            __opts__)

    def set_outputs(self, outs):
        if 'checkIntervalSec' in outs:
            self.check_interval_sec = outs['checkIntervalSec']
        if 'creationTimestamp' in outs:
            self.creation_timestamp = outs['creationTimestamp']
        if 'description' in outs:
            self.description = outs['description']
        if 'healthyThreshold' in outs:
            self.healthy_threshold = outs['healthyThreshold']
        if 'httpHealthCheck' in outs:
            self.http_health_check = outs['httpHealthCheck']
        if 'httpsHealthCheck' in outs:
            self.https_health_check = outs['httpsHealthCheck']
        if 'name' in outs:
            self.name = outs['name']
        if 'project' in outs:
            self.project = outs['project']
        if 'selfLink' in outs:
            self.self_link = outs['selfLink']
        if 'sslHealthCheck' in outs:
            self.ssl_health_check = outs['sslHealthCheck']
        if 'tcpHealthCheck' in outs:
            self.tcp_health_check = outs['tcpHealthCheck']
        if 'timeoutSec' in outs:
            self.timeout_sec = outs['timeoutSec']
        if 'type' in outs:
            self.type = outs['type']
        if 'unhealthyThreshold' in outs:
            self.unhealthy_threshold = outs['unhealthyThreshold']
