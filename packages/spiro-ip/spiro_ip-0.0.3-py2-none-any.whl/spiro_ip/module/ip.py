def addrs4():
    """
    Get a list of all known public IPv4 addresses, from:

    * Network interfaces
    * AWS EC2 Metadata
    * External services
    """
    addrs = __salt__['network.ipaddrs'](type='public')
    extra = __salt__['grains.get']('meta-data:public-ipv4')
    ext = __salt__['grains.get']('externalip4')
    if extra:
        addrs += [extra]
    if ext:
        addrs += [ext]
    return list(set(
        a
        for a in addrs
        if ':' not in a
    ))


def addrs6():
    """
    Get a list of all known public IPv6 addresses, from:

    * Network interfaces
    * AWS EC2 Metadata
    * External services
    """
    addrs = __salt__['network.ipaddrs6']()
    extra = __salt__['grains.get']('meta-data:public-ipv6')
    ext = __salt__['grains.get']('externalip6')
    if extra:
        addrs += [extra]
    if ext:
        addrs += [ext]
    return list(set(
        a 
        for a in addrs
        if not a.lower().startswith('fe80:') and '.' not in a
    ))
