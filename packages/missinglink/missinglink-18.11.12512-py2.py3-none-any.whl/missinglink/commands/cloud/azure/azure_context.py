import json
import uuid

from azure.common.credentials import get_azure_cli_credentials
from azure.graphrbac import GraphRbacManagementClient
from azure.keyvault import KeyVaultClient
from azure.graphrbac.models import ServicePrincipalCreateParameters
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.authorization.models import RoleAssignmentCreateParameters
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.resource.resources.models import DeploymentProperties
from azure.common.client_factory import get_client_from_cli_profile
import click
from missinglink.crypto import SshIdentity

from missinglink.commands.cloud.aws import BackendContext
from missinglink.commands.cloud.cloud_connector import CloudConnector
from missinglink.commands.utilities import pop_key_or_prompt_if, PathTools

APP_ID = '7eba301b-077d-4d8e-a1dd-a0b70113e6ca'


class AzureContext(BackendContext, CloudConnector):
    def __init__(self, ctx, kwargs):
        super(AzureContext, self).__init__(ctx, kwargs)
        self.location = ctx.obj.azure.location
        self.kwargs = kwargs

    def init_and_authorise_app(self):
        service_principal = self._create_service_principal()
        self._get_and_deploy_template()
        self._create_key()
        self._authorize_app(service_principal)
        self._create_cloud_connector()
        self._init_prepare_connector_message(set_ssh=not self.auth_state['ssh_present'], set_ml=not self.auth_state['mali_config'])

    def _create_service_principal(self):
        rbac_client = get_client_from_cli_profile(GraphRbacManagementClient)
        app_sp = list(rbac_client.service_principals.list(filter='appId eq \'%s\'' % APP_ID))
        if not app_sp:
            service_principal = rbac_client.service_principals.create(
                ServicePrincipalCreateParameters(app_id=APP_ID, account_enabled=True))
        else:
            service_principal = app_sp[0]
        self.tenant_id = rbac_client.config.tenant_id
        return service_principal

    def _authorize_app(self, service_principal):
        click.echo('Authorizing MissingLink App to manage virtual machines')
        auth_client = get_client_from_cli_profile(AuthorizationManagementClient)
        roles = list(auth_client.role_assignments.list(filter='principalId eq \'%s\'' % service_principal.object_id))
        if not roles:
            role_definition_id = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Authorization/roleDefinitions/d73bb868-a0df-4d4d-bd69-98a00b01fccb' % (auth_client.config.subscription_id, self.rg_name)  # Virtual Machine Contributor
            auth_client.role_assignments.create('/subscriptions/%s/' % auth_client.config.subscription_id, uuid.uuid4(), RoleAssignmentCreateParameters(role_definition_id=role_definition_id, principal_id=service_principal.object_id))
        click.echo('Done')

    def _get_template(self):
        result = self._handle_api_call('get', '{}/azure/init_template'.format(self.org))
        return json.loads(result['template'])

    def _create_key(self):
        click.echo('Creating a key in the Key Vault')
        credentials, subscription_id = get_azure_cli_credentials(resource='https://vault.azure.net')
        key_vault_client = KeyVaultClient(credentials)
        key_name = 'MissingLinkRM'
        results = list(key_vault_client.get_key_versions(self.key_vault, key_name))
        if not results:
            key_bundle = key_vault_client.create_key(self.key_vault, key_name, 'RSA', key_size=4096)
            self.key_id = key_bundle.key.kid
        else:
            self.key_id = results[0].kid
        click.echo('Done')

    def _get_and_deploy_template(self):
        click.echo('Applying template for Resource Group, Network and Key Vault')
        template = self._get_template()
        rm_client = get_client_from_cli_profile(ResourceManagementClient)
        self.subscription_id = rm_client.config.subscription_id
        rbac_client = get_client_from_cli_profile(GraphRbacManagementClient)
        user = rbac_client.signed_in_user.get()
        params = {
            'rgLocation': self.location,
            'org': self.org[:20],
            'userObjectId': user.object_id
        }
        params = {k: {'value': v} for k, v in params.items()}
        poller = rm_client.deployments.create_or_update_at_subscription_scope('MissingLink', DeploymentProperties(template=template, mode='Incremental', parameters=params), location=self.location)
        poller.wait()
        result = poller.result()
        self.net_name = result.properties.outputs['netName']['value']
        self.rg_name = result.properties.outputs['groupName']['value']
        self.key_vault = result.properties.outputs['vaultPath']['value']
        self.subnet = result.properties.outputs['subnetName']['value']
        click.echo('Done')

    def _create_cloud_connector(self):
        click.echo('Saving state to MissingLink servers')
        template = {
            'subscription_id': self.subscription_id,
            'tenant_id': self.tenant_id,
            'key_name': self.key_id,
            'location': self.location,
            'net_data': [{'name': self.net_name, 'region': self.location, 'subnet': self.subnet}],
            'resource_group': self.rg_name,
            'key_vault': self.key_vault
        }
        url = '{org}/azure/save_connector'.format(org=self.org)
        self.auth_state = self._handle_api_call('post', url, template)

    @classmethod
    def get_kms(cls, key_id):
        from missinglink.crypto import AzureEnvelope

        credentials, subscription_id = get_azure_cli_credentials(resource='https://vault.azure.net')
        return AzureEnvelope(credentials, key_id)

    def _init_prepare_connector_message(self, set_ssh, set_ml):
        template, config_data = self.cloud_connector_defaults(self.ctx, cloud_type='azure', kwargs=dict(connector=self.subscription_id))
        kms = self.get_kms(self.key_id)
        if set_ssh:
            ssh_key_path = pop_key_or_prompt_if(self.kwargs, 'ssh_key_path', text='SSH key path [--ssh-key-path]', default=PathTools.get_ssh_path())
            ssh_key = SshIdentity(ssh_key_path)
            ssh_key_priv = ssh_key.export_private_key_bytes()
            ssh_key_pub = ssh_key.export_public_key_bytes().decode('utf-8')
            self._update_org_metadata_ssh_key(ssh_key_pub)
            ssh = self.encrypt(kms, ssh_key_priv)
            template['ssh'] = ssh
        if set_ml:
            mali = self.encrypt(kms, config_data)
            template['mali'] = mali

        template['cloud_data'] = {}
        url = '{org}/cloud_connector/{name}'.format(org=self.org, name=template['name'])
        self._handle_api_call('post', url, template)
        click.echo('Done')
