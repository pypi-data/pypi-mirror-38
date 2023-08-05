from minty_ddd import CQRS
from minty_infrastructure import InfrastructureFactory
from pyramid.config import Configurator


def _build_cqrs_setup(cqrs):
    """Create a callable for setting up the "CQRS" methods request objects

    :param cqrs: A configured CQRS object
    :type cqrs: CQRS
    :return: A function, callable by Pyramid, to register the CQRS
        method(s)
    :rtype: callable
    """

    def setup_cqrs_request(config):
        """Add the CQRS accessors to the Pyramid request objects

        :param config: Pyramid configurator instance
        :type config: Configurator
        :return: Nothing
        :rtype: None
        """

        def get_query_instance(request, domain: str):
            return cqrs.get_query_instance(domain, context=request.host)

        config.add_request_method(get_query_instance, "get_query_instance")

        # add_request_method() for the cqrs "command" handler once it's been written

    return setup_cqrs_request


class Engine:
    """Pyramid configurator
    """

    __slots__ = ["config", "domains"]

    def __init__(self, domains: list):
        self.domains = domains
        self.config = None

    def setup(self, global_config: dict, **settings) -> object:
        """Setup the application by loading the Configurator

        :param global_config: Global configuration
        :type global_config: dict
        :return: Returns the Configurator from Pyramid
        :rtype: object
        """
        infra_factory = InfrastructureFactory(
            settings["minty_service.infrastructure.config_file"]
        )

        cqrs = CQRS(self.domains, infra_factory)

        config = Configurator(settings=settings)
        config.include(_build_cqrs_setup(cqrs))

        config.scan()
        self.config = config
        return config

    def main(self) -> object:
        """Run the application by calling the wsgi_app function of Pyramid

        :raises ValueError: When setup is forgotten
        :return: wsgi app
        :rtype: object
        """

        if self.config is None:
            raise ValueError("Make sure you run setup before 'main'")

        return self.config.make_wsgi_app()
