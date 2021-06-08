# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.common import utils
from tempest.common import waiters
from tempest import config
from tempest.scenario import manager

CONF = config.CONF


class TestSRIOV(manager.NetworkScenarioTest):
    credentials = ['primary', 'admin']

    @classmethod
    def setup_clients(cls):
        super(TestSRIOV, cls).setup_clients()
        cls.networks_client = cls.os_admin.networks_client
        cls.ports_client = cls.os_primary.ports_client
        cls.servers_client = cls.os_primary.servers_client

    @classmethod
    def skip_checks(cls):
        super(TestSRIOV, cls).skip_checks()
        if not CONF.network.project_networks_reachable or \
                CONF.network.public_network_id:
            msg = ('Either project_networks_reachable must be "true", or '
                   'public_network_id must be defined.')
            raise cls.skipException(msg)
        if not CONF.network_feature_enabled.floating_ips:
            raise cls.skipException("Floating ips are not available")

    @classmethod
    def setup_credentials(cls):
        # Create no network resources for these tests.
        cls.set_network_resources()
        super(TestSRIOV, cls).setup_credentials()

    def _setup_server(self, keypair):
        security_groups = []
        if utils.is_extension_enabled('security-group', 'network'):
            security_group = self.create_security_group()
            security_groups = [{'name': security_group['name']}]
        # TODO(johngarbutt) add config for networks
        mgmt_uuid = "fa905f55-f4ba-494e-8b6b-9436b2c8cac0"
        mgmt_port = self.create_port(mgmt_uuid)

        rnic_uuid = "2163eae3-e3ed-47f0-b1f9-dc67b8a85eb9"
        vnic_direct = {"binding:vnic_type": "direct"}
        rnic_port = self.create_port(rnic_uuid, **vnic_direct)

        server = self.create_server(
            networks=[
                {'port': mgmt_port['id']},
                {'port': rnic_port['id']},
            ],
            key_name=keypair['name'],
            security_groups=security_groups)
        return server

    def _setup_network(self, server, keypair):
        public_network_id = CONF.network.public_network_id
        floating_ip = self.create_floating_ip(server, public_network_id)
        # Verify that we can indeed connect to the server before we mess with
        # it's state
        self._wait_server_status_and_check_network_connectivity(
            server, keypair, floating_ip)

        return floating_ip

    def _check_network_connectivity(self, server, keypair, floating_ip,
                                    should_connect=True,
                                    username=CONF.validation.image_ssh_user):
        # inspired by tempest.scenario.test_network_advanced_server_ops
        private_key = keypair['private_key']
        self.check_tenant_network_connectivity(
            server, username, private_key,
            should_connect=should_connect,
            servers_for_debug=[server])
        floating_ip_addr = floating_ip['floating_ip_address']
        # Check FloatingIP status before checking the connectivity
        self.check_floating_ip_status(floating_ip, 'ACTIVE')
        self.check_vm_connectivity(floating_ip_addr, username,
                                   private_key, should_connect,
                                   'Public network connectivity check failed',
                                   server)

    def _wait_server_status_and_check_network_connectivity(
        self, server, keypair, floating_ip,
        username=CONF.validation.image_ssh_user):
        # inspired by tempest.scenario.test_network_advanced_server_ops
        waiters.wait_for_server_status(self.servers_client, server['id'],
                                       'ACTIVE')
        self._check_network_connectivity(server, keypair, floating_ip,
                                         username=username)

    @utils.services('compute', 'network')
    def test_server_connectivity(self):
        keypair = self.create_keypair()
        server = self._setup_server(keypair)
        floating_ip = self._setup_network(server, keypair)
        self._wait_server_status_and_check_network_connectivity(
            server, keypair, floating_ip)
