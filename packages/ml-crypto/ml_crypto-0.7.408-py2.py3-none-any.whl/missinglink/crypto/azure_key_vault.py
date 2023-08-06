import re

from missinglink.crypto import Cipher


class AzureKeyVault(Cipher):
    """Azure Key Vault encryption client.

    :param credentials: credentials for authorizing Azure Key Vault.
     Can be created from console environment using
        get_azure_cli_credentials(resource='https://vault.azure.net')
    :type credentials: azure.cli.core.adal_authentication.AdalAuthentication
    :param key_id: azure key identifier
    :type key_id: str
    """
    def __init__(self, credentials, key_id):
        self.credentials = credentials
        self.vault_base, self.key_name, self.key_version = self._split_kid(key_id)

    def get_key_vault_client(self):
        try:
            from azure.keyvault import KeyVaultClient
        except ImportError:
            raise ImportError('azure-keyvault not found. It must be installed for this cipher')

        key_vault_client = KeyVaultClient(self.credentials)
        return key_vault_client

    @staticmethod
    def _split_kid(kid):
        pattern = '(.*vault.azure.net)/keys/(.*)/(.*)'
        m = re.match(pattern, kid)
        return m.group(1), m.group(2), m.group(3)

    def encrypt(self, data):
        result = self.get_key_vault_client().encrypt(self.vault_base, self.key_name, self.key_version, 'RSA-OAEP', data)
        return result.result

    def decrypt(self, data):
        result = self.get_key_vault_client().decrypt(self.vault_base, self.key_name, self.key_version, 'RSA-OAEP', data)
        return result.result
