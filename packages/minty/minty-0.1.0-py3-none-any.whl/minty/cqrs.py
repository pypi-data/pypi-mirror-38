from . import Base
from .infrastructure import InfrastructureFactory
from .repository import RepositoryFactory


class CQRS(Base):
    """Keep commands and queries separated

    CQRS: Command Query Responsibility Separation
    """

    __slots__ = ["domains"]

    def __init__(self, domains, infrastructure_factory: InfrastructureFactory):
        """Create a new CQRS instance from a list of domains

        :param domains: iterable returning domains. Domains are classes or
            packages with at least a "REQUIRED_REPOSITORIES" variable defining
            which repositories are necessary to use the domain.
        :type domains: object
        :param infrastructure_factory: Infrastructure factory, created with
            the required configuration, that the repositories can use to
            create infrastructure instances.
        :type infrastructure_factory: InfrastructureFactory
        """
        self.domains = {}

        for domain in domains:
            repo_factory = RepositoryFactory(infrastructure_factory)

            for repo in domain.REQUIRED_REPOSITORIES:
                repo_factory.register_repository(repo)

                for infra in repo.REQUIRED_INFRASTRUCTURE:
                    infrastructure_factory.register_infrastructure(infra)

            self.domains[domain.__name__] = {
                "module": domain,
                "repository_factory": repo_factory,
            }

    def get_query_instance(self, domain: str, context=None):
        """Instantiate and return the "query" part of the specified domain

        :param domain: name of the domain to get the query instance for
        :type domain: str
        :param context: context for this domain, defaults to None
        :param context: object, optional
        """
        # This can be probably be cached (per context = host)

        self.logger.debug(
            f"Creating query instance for domain '{domain}' with context "
            + f"'{context}'"
        )

        with self.statsd.get_timer("get_query_instance").time(domain):
            query_instance = self.domains[domain]["module"].get_query_instance(
                self.domains[domain]["repository_factory"], context=context
            )

        return query_instance

    # command is unimplemented for now: build when needed
