class TrafficGeneratorVChassisResource(object):
    def __init__(self, address=None, family=None, shell_name=None, fullname=None, name=None, attributes=None):
        """

        :param str address: IP address of the resource
        :param str family: resource family
        :param str shell_name: shell name
        :param str fullname: full name of the resource
        :param str name: name of the resource
        :param dict[str, str] attributes: attributes of the resource
        """
        self.address = address
        self.family = family
        self.shell_name = shell_name
        self.fullname = fullname
        self.name = name
        self.attributes = attributes or {}

        if shell_name:
            self.namespace_prefix = "{}.".format(self.shell_name)
        else:
            self.namespace_prefix = ""

    @property
    def user(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}User".format(self.namespace_prefix), None)

    @property
    def password(self):
        """

        :rtype: string
        """
        return self.attributes.get("{}Password".format(self.namespace_prefix), None)

    @property
    def api_user(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}API User".format(self.namespace_prefix), None)

    @property
    def api_password(self):
        """

        :rtype: string
        """
        return self.attributes.get("{}API Password".format(self.namespace_prefix), None)

    @property
    def cli_connection_type(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}CLI Connection Type".format(self.namespace_prefix), "SSH")

    @property
    def cli_tcp_port(self):
        """

        :rtype: str
        """
        return self.attributes.get("{}CLI TCP Port".format(self.namespace_prefix), 22)

    @property
    def sessions_concurrency_limit(self):
        """

        :rtype: float
        """
        return self.attributes.get("{}Sessions Concurrency Limit".format(self.namespace_prefix), 1)

    @property
    def tvm_comms_network(self):
        """TeraVM Comms Network Name

        :rtype: str
        """
        return self.attributes.get("{}TVM Comms Network".format(self.namespace_prefix), None)

    @property
    def tvm_mgmt_network(self):
        """TeraVM MGMT Network Name

        :rtype: str
        """
        return self.attributes.get("{}TVM MGMT Network".format(self.namespace_prefix), None)

    @property
    def license_server(self):
        """TeraVM License Server IP

        :rtype: str
        """
        return self.attributes.get("{}License Server".format(self.namespace_prefix), None)

    @property
    def executive_server(self):
        """TeraVM Executive Server IP

        :rtype: str
        """
        return self.attributes.get("{}Executive Server".format(self.namespace_prefix), None)

    @classmethod
    def from_context(cls, context, shell_name=None):
        """Create an instance of TrafficGeneratorVBladeResource from the given context

        :param cloudshell.shell.core.driver_context.ResourceCommandContext context:
        :param str shell_name: shell Name
        :rtype: TrafficGeneratorVBladeResource
        """
        return cls(address=context.resource.address,
                   family=context.resource.family,
                   shell_name=shell_name,
                   fullname=context.resource.fullname,
                   attributes=dict(context.resource.attributes),
                   name=context.resource.name)
