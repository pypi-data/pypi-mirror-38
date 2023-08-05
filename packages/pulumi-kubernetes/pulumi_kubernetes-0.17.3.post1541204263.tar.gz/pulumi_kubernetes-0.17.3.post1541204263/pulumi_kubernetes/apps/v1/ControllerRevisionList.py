import pulumi
import pulumi.runtime

from ... import tables

class ControllerRevisionList(pulumi.CustomResource):
    """
    ControllerRevisionList is a resource containing a list of ControllerRevision objects.
    """
    def __init__(self, __name__, __opts__=None, items=None, metadata=None):
        if not __name__:
            raise TypeError('Missing resource name argument (for URN creation)')
        if not isinstance(__name__, str):
            raise TypeError('Expected resource name to be a string')
        if __opts__ and not isinstance(__opts__, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')

        __props__ = dict()

        __props__['apiVersion'] = 'apps/v1'
        __props__['kind'] = 'ControllerRevisionList'
        if not items:
            raise TypeError('Missing required property items')
        __props__['items'] = items
        __props__['metadata'] = metadata

        super(ControllerRevisionList, self).__init__(
            "kubernetes:apps/v1:ControllerRevisionList",
            __name__,
            __props__,
            __opts__)

    def translate_output_property(self, prop: str) -> str:
        return tables._CASING_FORWARD_TABLE.get(prop) or prop

    def translate_input_property(self, prop: str) -> str:
        return tables._CASING_BACKWARD_TABLE.get(prop) or prop
