.. _configuration_index:

=================
Configuration
=================

All configurations' files are in the directory `setting` of the application.

For the main part as for the plugins, there are two types of files :

- <name>.default.yml :

  It contains all the default conf and must not be modified. Each upgrade can erease or rewrite its content.

- <name>.local.yml

  If exists, it override default conf by all your customizations. All your modification must be here.

.. note:: The environment variable `PBD__CONFIG_DIR` can be used to defined another place for them

.. toctree::
   :maxdepth: 2

   main



