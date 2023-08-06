import six


from orchestrate.common import safe_format
from orchestrate.core.provider.constants import (
  STRING_TO_PROVIDER,
)
from orchestrate.core.cluster.errors import *
from orchestrate.core.services.base import Service


class ClusterService(Service):
  def connected_clusters(self):
    return self.services.kubernetes_service.get_cluster_names()

  def assert_is_connected(self):
    connected_clusters = self.connected_clusters()
    if not connected_clusters:
      raise NotConnectedError()
    elif len(connected_clusters) > 1:
      raise MultipleClustersConnectionError(connected_clusters)
    return connected_clusters[0]

  def assert_is_disconnected(self):
    connected_clusters = self.connected_clusters()
    if connected_clusters:
      if len(connected_clusters) == 1:
        raise PleaseDisconnectError(connected_clusters[0])
      else:
        raise MultipleClustersConnectionError(connected_clusters)

  def connect(self, cluster_name, provider_string, kubeconfig):
    try:
      self.assert_is_disconnected()
    except PleaseDisconnectError as e:
      if e.current_cluster_name != cluster_name:
        raise

    if kubeconfig is None:
      # TODO(alexandra): make provider_string required in 0.3.0. For now, keep it from being a breaking change
      # raise ClusterError('Please provide either a kubeconfig or a provider to connect to a cluster')
      if provider_string is None:
        provider_string = 'aws'

      provider_service = self.services.provider_broker.get_provider_service(provider_string)
      kubeconfig = provider_service.create_kubeconfig(cluster_name)
    else:
      if provider_string is not None:
        raise ClusterError('Please do not use a cloud provider when connecting with a kubeconfig file')

    self.services.kubernetes_service.write_config(cluster_name, kubeconfig)
    self.test()

  def create(self, options):
    try:
      self.assert_is_disconnected()
    except PleaseDisconnectError as e:
      if e.current_cluster_name != options.get('cluster_name', ''):
        raise

    self.services.options_validator_service.validate_cluster_options(**options)
    cluster_name = options.get('cluster_name', '')

    if 'provider' in options and 'cloud_provider' in options:
      raise ClusterError('Cannot provider both "provider" and "cloud_provider"')

    provider_string = options.get('provider') or options.get('cloud_provider', 'aws')
    provider_service = self.services.provider_broker.get_provider_service(provider_string)

    try:
      cluster = provider_service.create_kubernetes_cluster(options)
      self.services.kubernetes_service.wait_until_nodes_are_ready()
      return cluster.name
    except Exception as e:
      try:
        self.disconnect(cluster_name, None)
      except Exception:
        pass
      six.raise_from(
        ClusterError(safe_format(
          "Cluster create error: {}\n"
          "Resolve the issue and recreate your cluster.",
          str(e),
        )),
        e,
      )

  def destroy(self, cluster_name, provider_string):
    provider_service = self.services.provider_broker.get_provider_service(provider_string)
    provider_service.destroy_kubernetes_cluster(cluster_name=cluster_name)

  def disconnect(self, cluster_name, disconnect_all):
    if (cluster_name and disconnect_all) or (not cluster_name and not disconnect_all):
      raise ClusterError('Must provide exactly one of --cluster-name <cluster_name> and --all')

    try:
      current_cluster_name = self.assert_is_connected()
      if cluster_name is not None and current_cluster_name != cluster_name:
        raise PleaseDisconnectError(current_cluster_name)
    except MultipleClustersConnectionError:
      if not disconnect_all:
        raise

    for cname in self.connected_clusters():
      try:
        self.services.kubernetes_service.ensure_config_deleted(cluster_name=cname)
      except Exception as e:
        six.raise_from(ClusterError(safe_format(
          'Looks like an error occured while attempting to disconnect from cluster "{}".',
          cname,
        )), e)

  def test(self):
    cluster_name = self.assert_is_connected()
    self.services.kubernetes_service.test_config()

    provider_strings = []

    for provider_string in STRING_TO_PROVIDER:
      provider_service = self.services.provider_broker.get_provider_service(provider_string)
      try:
        provider_service.test_kubernetes_cluster(cluster_name)
      except Exception:
        continue
      provider_strings.append(provider_string)

    return (cluster_name, provider_strings)
