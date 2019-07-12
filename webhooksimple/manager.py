from webexteamssdk import WebexTeamsAPI
from abc import ABC, abstractmethod
from .models import Webhook

class WebhookManager(ABC):
    def __init__(self, authentication, parameters):
        self.authentication = authentication
        self.parameters = parameters

    @abstractmethod
    def create(self, webhook):
        pass

    @abstractmethod
    def delete(self, webhook):
        pass

    @abstractmethod
    def update(self, webhook):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def is_registered(self, webhook):
        pass


class WebexTeamsWebhookManager(WebhookManager):
    def __init__(self, authentication, parameters):
        super().__init__(authentication, parameters)

        self.access_token = self.authentication['access_token']
        self.api = WebexTeamsAPI(access_token=self.access_token)

    def create(self, webhook):
        vals = webhook.get_values()
        self.api.webhooks.create(name=vals['name'],
                                 targetUrl=vals['target_url'],
                                 resource=vals['resource'],
                                 event=vals['event'])

        return True

    def delete(self, webhook):
        online_hook = self.__find_webhook(webhook.get_values()['name'])

        if online_hook is None:
            return False
        else:
            self.api.webhooks.delete(online_hook.id)
            return True

    def update(self, webhook):
        online_hook = self.__find_webhook(webhook.name)

        if online_hook is None:
            return False
        else:
            self.api.webhooks.update(online_hook.id,
                                     targetUrl=webhook.target_url)
            return True

    def list(self):
        l = []
        for w in self.api.webhooks.list():
            l.append(Webhook(w.name, w.resource, w.event, w.targetUrl))

        return l

    def is_registered(self, webhook):
        return not self.__find_webhook(webhook.name) is None

    def __find_webhook(self, name):
        for online_hook in self.api.webhooks.list():
            if online_hook.name == name:
                return online_hook

        return None
