class Webhook:
    def __init__(self, name, resource, event, target_url):
        self.name = name
        self.resource = resource
        self.event = event
        self.target_url = target_url

    def get_values(self):
        keys = ["name", "resource", "event", "target_url"]

        ret = {}

        for k in keys:
            ret[k] = getattr(self, k)

        return ret

    def __str__(self):
        return "{} -> ({}, {}, {})".format(self.name,
                                           self.resource,
                                           self.event,
                                           self.target_url)
