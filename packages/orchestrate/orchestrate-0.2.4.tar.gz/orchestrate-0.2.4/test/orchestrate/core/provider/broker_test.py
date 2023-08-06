import pytest
from mock import Mock

from orchestrate.core.provider.constants import UnknownProviderStringError
from orchestrate.core.provider.broker import ProviderBroker

class TestProviderBroker(object):
  @pytest.fixture
  def services(self):
    return Mock()

  @pytest.fixture
  def provider_broker(self, services):
    return ProviderBroker(services)

  def test_get_provider_service(self, provider_broker, services):
    assert provider_broker.get_provider_service('aws') == services.aws_service
    assert provider_broker.get_provider_service('AWS') == services.aws_service

  @pytest.mark.parametrize('provider_string', [
    'amazon',
    'google',
    'azure',
    'eks',
    'gke',
    'aks',
    None,
  ])
  def test_unknown_provider(self, provider_broker, provider_string):
    with pytest.raises(UnknownProviderStringError):
      provider_broker.get_provider_service(provider_string)
