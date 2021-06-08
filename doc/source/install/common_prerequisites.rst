Prerequisites
-------------

Before you install and configure the vipu service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``vipu_tempest`` database:

     .. code-block:: none

        CREATE DATABASE vipu_tempest;

   * Grant proper access to the ``vipu_tempest`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON vipu_tempest.* TO 'vipu_tempest'@'localhost' \
          IDENTIFIED BY 'VIPU_TEMPEST_DBPASS';
        GRANT ALL PRIVILEGES ON vipu_tempest.* TO 'vipu_tempest'@'%' \
          IDENTIFIED BY 'VIPU_TEMPEST_DBPASS';

     Replace ``VIPU_TEMPEST_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``vipu_tempest`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt vipu_tempest

   * Add the ``admin`` role to the ``vipu_tempest`` user:

     .. code-block:: console

        $ openstack role add --project service --user vipu_tempest admin

   * Create the vipu_tempest service entities:

     .. code-block:: console

        $ openstack service create --name vipu_tempest --description "vipu" vipu

#. Create the vipu service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        vipu public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        vipu internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        vipu admin http://controller:XXXX/vY/%\(tenant_id\)s
