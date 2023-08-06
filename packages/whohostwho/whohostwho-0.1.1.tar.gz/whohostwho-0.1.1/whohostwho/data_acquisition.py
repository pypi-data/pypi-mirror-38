from datetime import datetime
from ipaddress import ip_address
from collections import namedtuple

import dns.resolver


class DataAcquisition:
    IpInfo = namedtuple("IpInfo", "asn network country registry date")
    AsnInfo = namedtuple("AsnInfo", "asn country registry date description")

    def __init__(self, ns=[], date_fmt="%Y-%m-%d %H:%M:%S"):
        self.date_fmt = date_fmt
        self.my_reso = dns.resolver.Resolver()
        if len(ns) > 0:
            self.my_reso.nameservers = list(ns)

    def run(self, domain):
        res = self.resolve(domain)
        res["ips"] = [self.get_ip_info(ip) for ip in res["ips"]]
        for ns, ips in res["nameservers"].items():
            res["nameservers"][ns] = [self.get_ip_info(ip) for ip in ips]
        res["meta"] = {
            "created_at": datetime.utcnow().strftime(self.date_fmt),
            "resolvers": self.my_reso.nameservers,
        }
        return res

    def get_ip_info(self, ip, count=0):
        ip = ip_address(ip)
        try:
            hostname = str(self.my_reso.query(ip.reverse_pointer, "PTR")[0])
        except (
            dns.resolver.NXDOMAIN,
            dns.resolver.NoNameservers,
            dns.resolver.Timeout,
        ):
            hostname = None
        if ip.version == 4:
            domain = ip.reverse_pointer.replace("in-addr.arpa", "origin.asn.cymru.com.")
        elif ip.version == 6:
            domain = ip.reverse_pointer.replace("ip6.arpa", "origin6.asn.cymru.com.")
        result = str(self.my_reso.query(domain, "TXT")[0])
        info = {"ip": str(ip), "hostname": hostname}
        ipinf = self.IpInfo(*result.strip('"').split(" | "))
        asns = [int(asn) for asn in ipinf.asn.split(" ")]
        ipinf = ipinf._replace(asn=asns)
        info.update(ipinf._asdict())
        descriptions = []
        for asn in asns:
            result = str(
                self.my_reso.query("AS{}.asn.cymru.com.".format(asn), "TXT")[0]
            )
            asninf = self.AsnInfo(*result.strip('"').split(" | "))
            descriptions.append(asninf.description)
        info["descriptions"] = descriptions
        return info

    def resolve_ips(self, domain):
        ipv6 = True
        try:
            ips = [str(r) for r in self.my_reso.query(domain, "A")]
        except dns.resolver.NoAnswer:
            ips = []
        try:
            ips.extend(str(r) for r in self.my_reso.query(domain, "AAAA"))
        except dns.resolver.NoAnswer:
            ipv6 = False
        return ips, ipv6

    def resolve(self, domain):
        res = {"ips": [], "nameservers": {}}
        ips, ipv6 = self.resolve_ips(domain)
        res["ips"].extend(ips)
        res["ipv6"] = bool(ipv6)
        for ns in self.resolve_ns(domain):
            ns_ips, _ = self.resolve_ips(ns)
            res["nameservers"][str(ns)] = ns_ips
        return res

    def resolve_ns(self, domain):
        try:
            return [str(ns) for ns in self.my_reso.query(domain, "NS")]
        except dns.resolver.NoAnswer:
            new_dom = ".".join(domain.split(".")[1:])
            return self.resolve_ns(new_dom)
