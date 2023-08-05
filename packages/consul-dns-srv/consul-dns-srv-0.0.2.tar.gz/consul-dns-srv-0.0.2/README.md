# Consul DNS SRV

## Install

```
pip install consul-dns-srv

```

Environment Variables


```
NAMESERVER
```

or

```
NAMESERVER_HOST
NAMESERVER_PORT
```

## Usage

```
from consul_dns_srv import DNS

host = DNS.service_lookup("myservice")

```