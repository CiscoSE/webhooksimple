class Webhook:
    """Class to model a webhook and its parameters.

    This class models a typical webhook and its parameters. It is used to
    represent webhooks in this framework and closely follows the definition
    of webhooks in the yaml file.
    """
    def __init__(self, name, resource, event, target_url):
        """Initialize a new webhook.

        Attributes:
            name (str): The name of this webhook. This **must** be unique since
                webhooksimple will use this to identify webhooks in the API.
            resource (str): The resource this webhook should react to
            event (str): The event this webhook should react to
            target_url (str): The url this webhook should fire to
        """
        self.name = name
        self.resource = resource
        self.event = event
        self.target_url = target_url

    def get_values(self):
        """Return a dict with the parameters of this webhook.

        Returns:
            dict: A dict containing the parameters of this webhook.
        """
        keys = ["name", "resource", "event", "target_url"]

        ret = {}

        for k in keys:
            ret[k] = getattr(self, k)

        return ret

    def __str__(self):
        """String represntation of this webhook.

        This representation is used in the list command and for debug reasons.

        Returns:
            str: A string representation of this webhook
        """
        return "{} -> ({}, {}, {})".format(self.name,
                                           self.resource,
                                           self.event,
                                           self.target_url)
