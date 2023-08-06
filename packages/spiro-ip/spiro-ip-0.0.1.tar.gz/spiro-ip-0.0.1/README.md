spiro-ip
========

A quick and simple module to get information about the various IPs of your salt
minions.

This is meant to be installed on minions.

Installation
============

On minions, run `pip install spiro-ip`

Or, as a state:

```
{% if grains['pythonversion'][0] == 2 %}
{% set pipbin = "/usr/bin/pip2" %}
{% else %}
{% set pipbin = "/usr/bin/pip3" %}
{% endif %}

spiro-ip:
  pip.installed:
    - bin_env: {{pipbin}}
```

Interface
=========

A number of things are provided:

Grains
------

* `externalip4`, `externalip6`: Queries external services for your IP, useful
  if the minion is behind a NAT or other complex network

Modules
-------

* `ip.addrs4`, `ip.addrs6`: Collates information about a minion's IP address
  from several sources. 

    * `network.ipaddrs` / `network.ipaddrs6`
    * AWS metadata (if you've set `metadata_server_grains: True`, see the [metadata grain](https://docs.saltstack.com/en/latest/ref/grains/all/salt.grains.metadata.html))
    * `externalip4` / `externalip6` grains (above)

Configuration
=============

No configuration is required. However, as mentioned above, it might be useful to
set `metadata_server_grains: True`.
