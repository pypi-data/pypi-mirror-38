from orchestrate.core.services.base import Service
from orchestrate.core.provider.constants import (
  Provider,
  string_to_provider,
)


class ProviderBroker(Service):
  def get_provider_service(self, provider_string):
    provider = string_to_provider(provider_string)

    if provider == Provider.AWS:
      return self.services.aws_service
    else:
      raise NotImplementedError()
