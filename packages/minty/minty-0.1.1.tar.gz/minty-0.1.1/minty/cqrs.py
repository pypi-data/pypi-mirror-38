from . import Base
from .infrastructure import InfrastructureFactory
from .repository import RepositoryFactory


def event(name: str):
    def register_event(f):
        f.minty_event_name = name
        return f

    return register_event


class Event(Base):
    __slots__ = ["domain", "event_name", "parameters"]

    def __init__(self, domain, event_name, parameters):
        self.domain = domain
        self.event_name = event_name
        self.parameters = parameters

        self.logger.info(
            f"Event created. Domain = '{domain}', "
            + f"event = '{event_name}', "
            + f"parameters = '{parameters}'"
        )


class CommandWrapper(Base):
    """Wrapper class for command instances. Handles creation of Events"""

    def __init__(self, domain, command_instance):
        self.domain = domain
        self.command_instance = command_instance

    def __getattr__(self, attr):
        """Get an attribute on the wrapped class, wrapped by "event" code

        This event code ensures the command can't return anything, and creates
        an Event instance.

        :param attr: attribute to retrieve
        :type attr: str
        :return: wrapped method
        :rtype: callable
        """

        orig_attr = self.command_instance.__getattribute__(attr)
        if callable(orig_attr):

            def wrapped(*args, **kwargs):
                event_name = orig_attr.minty_event_name

                # The created event is discarded for now.
                Event(self.domain, event_name, kwargs)

                timer = self.statsd.get_timer(self.domain)
                with timer.time(f"{event_name}.execute"):
                    orig_attr(**kwargs)

                # TODO Save event, get event-id ("orig_attr" does parameter
                #      validation)
                # TODO Broadcast the event-type + saved-event-id

                # Enforce "command cannot return a value"
                return

            return wrapped
        else:
            return orig_attr


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
        # This can probably be cached (per context = host)

        self.logger.debug(
            f"Creating query instance for domain '{domain}' with context "
            + f"'{context}'"
        )

        with self.statsd.get_timer(domain).time("get_query_instance"):
            query_instance = self.domains[domain]["module"].get_query_instance(
                self.domains[domain]["repository_factory"], context=context
            )

        return query_instance

    def get_command_instance(self, domain: str, context=None):
        """Execute the a command on a domain

        :param domain: name of the domain to get the query instance for
        :type domain: str
        :param context: context for this domain, defaults to None
        :param context: object, optional
        """
        self.logger.debug(
            f"Creating command instance for domain '{domain}' with context "
            + f"'{context}'"
        )

        with self.statsd.get_timer(domain).time("get_command_instance"):
            # This should be cacheable per domain+context
            cmd_instance = self.domains[domain]["module"].get_command_instance(
                self.domains[domain]["repository_factory"], context=context
            )

        cmd_wrapped = CommandWrapper(domain, cmd_instance)

        return cmd_wrapped
