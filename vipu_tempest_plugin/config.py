# Copyright 2015
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

from tempest.config import cfg

test_sriov_group = cfg.OptGroup(name="testsriov",
                                title="test sriov options")


TestSriovGroup = [
    cfg.StrOpt("mgmt_port_uuid",
               default="",
               help="Management NIC port UUID"),
    cfg.StrOpt("rnic_port_uuid",
               default="",
               help="RDMA NIC port UUID"),
    cfg.StrOpt("custom_image_ssh_user",
               default="ubuntu",
               help="Custom image ssh user"),
    cfg.StrOpt("custom_image_uuid",
               default="",
               help="Custom image UUID")
]
