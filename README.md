Apache Role
===========

Configures an apache server based on Fedora with CustomOS settings:

- HTTPD virtual server with /var/www/html/customapp as root path.
- Testing index webpage.

Requirements
------------

A Fedora system.

Role Variables
--------------

No parameter or default variables are defined for this role.
Static variables like packages list or configuration file settings
can be found in vars/ directory.

Dependencies
------------

This role has iac_ansible-role-server as dependency, configured in ansible-galaxy .requirements file.

Example Playbook
----------------

```
    - hosts: servers
      roles:
         - { role: iac_ansible-role-apache }
```

License
-------

GPL3

Author Information
--------------

