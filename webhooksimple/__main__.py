import sys
commands_available = ["help", "sync", "setup", "purge", "list", "export"]

# Command functions
def help(parser, webhook_manager):
    print("webhook_simple lets you setup webhooks from a configuration file")
    print("Available commands")
    print()
    print("help:    Print this help message")
    print("sync:    Synchronise the webhooks registered with the configruation")
    print("setup:   Delete all webhooks and deploy the configuration")
    print("purge:   Delete all webhooks currently registered")
    print("list:    List all webhooks currently registered with the API")
    print("export:  Export all currently registered webhooks")
    print()
    print("Usage: python -m webhook_simple <command>")

def sync(parser, webhook_manager):
    offline_hooks = parser.convert()
    online_hooks = webhook_manager.list()

    hooks_to_add = []
    hooks_to_update = []

    for h in offline_hooks:
        if not webhook_manager.is_registered(h):
            hooks_to_add.append(h)
        else:
            hooks_to_update.append(h)
    print("Creating {} new webhooks".format(len(hooks_to_add)))
    for h in hooks_to_add:
        webhook_manager.create(h)
        print("- {}".format(h))

    print("Updating {} existing webhooks".format(len(hooks_to_update)))
    for h in hooks_to_update:
        webhook_manager.update(h)
        print("- {}".format(h))

def purge(parser, webhook_manager):
    print("Purging all webhooks")
    webhooks = webhook_manager.list()
    for hook in webhooks:
        webhook_manager.delete(hook)

def setup(parser, webhook_manager):
    purge(parser, webhook_manager)
    hooks = parser.convert()

    print("Creating webhooks: ")
    for h in hooks:
        print("- {}".format(h))
        webhook_manager.create(h)

def list(parser, webhook_manager):
    print("List of webhooks")
    webhooks = webhook_manager.list()

    for hook in webhooks:
        print("- {}".format(hook))

def export(parser, webhook_manager):
    print(parser.export(webhook_manager.list()))

if not len(sys.argv) == 2:
    print("Please provide an action to take.")
    print("Possible actions are: {}".format(", ".join(commands_available)))
    print("Example: python -m webhook_simple help")
    sys.exit(-1)

command_str = str(sys.argv[1]).lower()

if command_str not in commands_available:
    print("I don't know the action '{}'".format(command_str))
    print("Possible actions are: {}".format(", ".join(commands_available)))
    print("Example: python -m webhook_simple help")
    sys.exit(-1)


from .models import Webhook
from .parser import YAMLParser

parser = YAMLParser("vars.yml", "hooks.yml")
manager = parser.get_manager_instance()

# Since we know that the string is in commands_available this is semi-save
locals()[command_str](parser, manager)
