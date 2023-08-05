from stacker.blueprints.base import Blueprint
from stacker.blueprints.variables.types import EC2VPCId, EC2SubnetIdList, CFNCommaDelimitedList, CFNString, CFNNumber, \
    EC2KeyPairKeyName
from troposphere import cloudformation, ec2, Ref

from cumulus.chain import chain, chaincontext
from cumulus.components.userdata.linux import LinuxUserData
from cumulus.steps.ec2 import scaling_group, launch_config, block_device_data, ingress_rule


class ScalingGroupSimple(Blueprint):
    VARIABLES = {
        'VpcId': {'type': EC2VPCId,
                  'description': 'Vpc Id'},
        'PrivateSubnets': {'type': EC2SubnetIdList,
                           'description': 'Subnets to deploy private '
                                          'instances in.'},
        'AvailabilityZones': {'type': CFNCommaDelimitedList,
                              'description': 'Availability Zones to deploy '
                                             'instances in.'},
        'InstanceType': {'type': CFNString,
                         'description': 'EC2 Instance Type',
                         'default': 't2.micro'},
        'MinSize': {'type': CFNNumber,
                    'description': 'Minimum # of instances.',
                    'default': '1'},
        'MaxSize': {'type': CFNNumber,
                    'description': 'Maximum # of instances.',
                    'default': '5'},
        'SshKeyName': {'type': EC2KeyPairKeyName},
        'ImageName': {
            'type': CFNString,
            'description': 'The image name to use from the AMIMap (usually '
                           'found in the config file.)'},
    }

    def get_metadata(self):
        metadata = cloudformation.Metadata(
            cloudformation.Init(
                cloudformation.InitConfigSets(
                    default=['install_and_run']
                ),
                install_and_run=cloudformation.InitConfig(
                    commands={
                        '01-startup': {
                            'command': 'touch thisfilemeansiworked'
                        },
                    }
                )
            )
        )
        return metadata

    def create_template(self):
        t = self.template
        t.add_description("Acceptance Tests for cumulus scaling groups")

        instance_name = self.context.namespace + "testLinuxInstance"

        # TODO: give to builder
        the_chain = chain.Chain()

        launch_config_name = 'Lc%s' % instance_name
        asg_name = 'Asc%s' % instance_name
        ec2_role_name = 'Ec2RoleName%s' % instance_name

        the_chain.add(launch_config.LaunchConfig(launch_config_name=launch_config_name,
                                                 asg_name=asg_name,
                                                 ec2_role_name=ec2_role_name,
                                                 vpc_id=Ref('VpcId'),
                                                 bucket_name=self.context.bucket_name,
                                                 meta_data=self.get_metadata(),
                                                 user_data=LinuxUserData.user_data_for_cfn_init(
                                                     launch_config_name=launch_config_name,
                                                     asg_name=asg_name,
                                                     configsets='default')
                                                 )
                      )

        the_chain.add(ingress_rule.IngressRule(
            port_to_open="22",
            name="JonTestLinuxSshPort22",
            cidr='10.0.0.0/8'
        ))

        the_chain.add(block_device_data.BlockDeviceData(ec2.BlockDeviceMapping(
            DeviceName="/dev/xvda",
            Ebs=ec2.EBSBlockDevice(
                VolumeSize="40"
            ))))

        the_chain.add(scaling_group.ScalingGroup(name=asg_name,
                                                 launch_config_name=launch_config_name))

        chain_context = chaincontext.ChainContext(
            template=t,
            instance_name=instance_name
        )

        the_chain.run(chain_context)
