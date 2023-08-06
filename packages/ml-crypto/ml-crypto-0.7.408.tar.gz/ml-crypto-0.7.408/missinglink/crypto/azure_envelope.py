from .envelope import Envelope
from .azure_key_vault import AzureKeyVault


class AzureEnvelope(Envelope):
    def __init__(self, credentials, key_id):
        super(AzureEnvelope, self).__init__(AzureKeyVault(credentials, key_id))
