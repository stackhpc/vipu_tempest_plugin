2. Edit the ``/etc/vipu_tempest/vipu_tempest.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://vipu_tempest:VIPU_TEMPEST_DBPASS@controller/vipu_tempest
