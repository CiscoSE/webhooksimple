from webexteamssdk import WebexTeamsAPI
from abc import ABC, abstractmethod
from .models import Webhook

class WebhookManager(ABC):
    """Abstract parent class for all webhook manager

    A webhook manager provides the functionality to create, update, delete and
    check a webhook with the API. The WebhookManager class does not provide any
    functionality as such but rather serves as a template for concrete
    implementations such as the WebexTeamsWebhookManager
    """

    def __init__(self, authentication, parameters):
        """Create a new WebhookManager

        Parent constructor that saves the authentication section and any
        additional parameters from the vars.yaml file.

        Attributes:
            authentication (dict): A dict containing any authentication
                information. Note that the format is not specified since some
                APIs might need a token while others use username/password.
            parameters (dict): Additional parameters specified in vars.yml
        """
        self.authentication = authentication
        self.parameters = parameters

    @abstractmethod
    def create(self, webhook):
        """Create a new webhook from the model

        Attributes:
            webhook (models.Webhook): The new webhook that is to be created
        """
        pass

    @abstractmethod
    def delete(self, webhook):
        """Delete the provided webhook.

        Attributes:
            webhook (models.Webhook): The webhook that should be deleted
        """
        pass

    @abstractmethod
    def update(self, webhook):
        """Update the provided webhook.

        Attributes:
            webhook (models.Webhook): The webhook that should be updated
        """
        pass

    @abstractmethod
    def list(self):
        """List all webhooks currently registered online.

        Returns:
            list(models.Webhook): A list of webhook objects representing the
                currently online registered webhooks.
        """
        pass

    @abstractmethod
    def is_registered(self, webhook):
        """Check if a webhook is already registered online.

        Returns:
            boolean: True if the webhook exists online, False otherwise
        """
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
