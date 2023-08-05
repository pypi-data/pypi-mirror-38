from dns.resolver import NoNameservers
from dns.resolver import Resolver
import srvlookup
import random
import os


class DNSNotResolved(Exception):

    def __init___(self, name):
        Exception.__init__(self, "No DNS found for {}".format(name))


class DNS:
    resolver = None

    @classmethod
    def service_lookup(kls, name, domain="service.consul"):
        if not kls.resolver:

            host, port = os.getenv('NAMESERVER').split(":")

            if not host:
                host = os.getenv('NAMESERVER_HOST')
                port = os.getenv('NAMESERVER_PORT')

            kls.resolver = Resolver()

            kls.resolver.nameservers = [host]
            kls.resolver.nameserver_ports = {
                host: int(port)
            }

        srvlookup.resolver = kls.resolver

        result = None

        try:
            result = srvlookup.lookup(name=name, domain=domain)
        except (AttributeError, NoNameservers):
            pass

        if not result:
            raise DNSNotResolved(name)

        # todo: use weighting
        x = random.randint(0, len(result) - 1)

        return "http://{}:{}".format(result[x].host, result[x].port)
