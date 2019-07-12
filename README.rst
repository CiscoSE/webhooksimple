=============
WebhookSimple
=============


.. image:: https://img.shields.io/pypi/v/webhooksimple.svg
        :target: https://pypi.python.org/pypi/webhooksimple

.. image:: https://img.shields.io/travis/squ4rks/webhooksimple.svg
        :target: https://travis-ci.org/squ4rks/webhooksimple

.. image:: https://readthedocs.org/projects/webhooksimple/badge/?version=latest
        :target: https://webhooksimple.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/squ4rks/webhooksimple/shield.svg
     :target: https://pyup.io/repos/github/squ4rks/webhooksimple/
     :alt: Updates



A simple framework/cli tool to setup and sync (Webex Teams) API webhooks


* Free software: MIT license
* Documentation: https://webhooksimple.readthedocs.io.


Features
--------

* Create, update and delete (webex teams) webhooks from a yaml file
* Modular architecture makes it suitable for other APIs as well

How to Use
----------

WebhookSimple is a simple (and open source) python framework/command line tool that allows you to quickly describe your desired Webex Teams web hooks and then creates or synchronises them for you.

WebhookSimple requires two files from you. *vars.yml* and *hooks.yml*

*vars.yml* specifies the different variables while *hooks.yml* lets you specify the web hooks itself.

A web hook always looks like this  (in *hooks.yml*)

.. code-block:: yaml

   ---
   hooks:
     - name: test hook 1
       resource: "messages"
       event: "created"
       target_url: "https://your_url_here"

Make sure that the ``name`` of your web hook is always unique since this is what webhookSimple will use to identify and synchronise your webhooks.  Your ::vars.yml:: **must include**  an *adapter* that specifies the kind of api we are interacting with as well as the authentication details. Leave this to the provided ``parser.WebexTeamsWebhookManager`` for now and add the access token in the correct spot.

*vars.yml*:

.. code-block:: yaml

   # vars file. The adapter section **needs** to be here
   adapter:
     name: WebexTeamsWebhookManager
     authentication:
       access_token: your access token here
     parameters:

   # Add your variables from here on
   urls:
     - https://www.cisco.com
     - https://www.google.com



You can now ``setup``\ , ``purge``\ , ``list``\ , ``export`` or ``sync``\  your webhooks.


* ``setup`` will **delete** all webhooks currently present for this bot and create new ones based on the *hooks.yml* file.
* ``sync`` will update all existing webhooks based on the ``name``\ attribute and create those not present. It will **not** delete webhooks that are registered on the server.
* ``purge``\ will delete all webhooks without creating new ones
* ``list``\ will list all webhooks currently registered
* ``export`` will save all your currently active webhooks to a .yml file

Invoke the module by running

.. code-block:: bash

   $ ls
   hooks.yml vars.yml
   $ python3 -m webhooksimple setup

Taking it one step further
--------------------------

Setting up web hook from a command line and based of a configuration file is already pretty cool and convenient. But what if we have ten webhooks and need to update the target_url on all of them? We’d have to manually edit all the web hook entries in ::hooks.yml::. This is where the ::vars.yml:: file comes into play. ::hooks.yml:: is not a simple configuration file but rather a `Jinja2 <http://jinja.pocoo.org/docs/2.10/>`_ template of a configuration file. What you can do is this:

*vars.yml*

.. code-block:: yaml

   ---
   # Note: Adapter part (see above) omited for bravity
   url_prefix: https://my_url_base

*hooks.yml*:

.. code-block:: yaml

   ---
   hooks:
     - name: test hook 1
       resource: "messages"
       event: "created"
       target_url: "https://{{ url_prefix }}/messages"

But this is not all. Those that worked with jinja2 before probably already know what is coming next. You can also add some (generator) logic here. Lets say we want to create a debug and a production version of our web hook. We can do this by doing the following:

*vars.yml*:

.. code-block:: yaml

   ---
   # Note: Adapter part (see above) omited for bravity
   envs:
     - name: production
       url: https://my_production_prefix
     - name: development
       url: https://my_development_prefix

*hooks.yml*:

.. code-block:: yaml

   ---
   hooks:
     {% for env in envs %}
     - name: {{ env.name }} message hook
       resource: "message"
       event: "created"
       target_url: {{ env.url }}/messages
     {% endfor %}

Or you want to setup the same web hook for different urls. This would look something like this

*vars.yml*:

.. code-block:: yaml

   ---
   # Note: Adapter part (see above) omited for bravity
   urls:
    - https://url_number_1
    - https://url_number_2
    - https://url_number_3

*hooks.yml*:

.. code-block:: yaml

   ---
   hooks:
     {% for url in urls %}
     - name: "hook for {{ url }}"
       resource: "message"
       event: "created"
       target_url: {{ url }}
     {% endfor %}

Happy programming! You can get WebhookSimple by running

.. code-block:: bash

   $ pip3 install webhooksimple


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
