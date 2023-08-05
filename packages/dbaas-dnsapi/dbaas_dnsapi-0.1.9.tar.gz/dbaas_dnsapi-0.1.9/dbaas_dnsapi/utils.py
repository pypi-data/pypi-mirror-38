# -*- coding: utf-8 -*-

from models import PlanAttr
from .models import HOST
from .models import DatabaseInfraDNSList


def add_dns_record(databaseinfra, name, ip, type, database_sufix=None):
        name, domain = get_dns_name_domain(
            databaseinfra, name, type, database_sufix)

        records = DatabaseInfraDNSList.objects.filter(
            databaseinfra=databaseinfra.id,
            name=name,
            domain=domain,
            ip=ip,
            type=type).count()

        if records == 0:
            databaseinfradnslist = DatabaseInfraDNSList(
                databaseinfra=databaseinfra.id,
                name=name,
                domain=domain,
                ip=ip,
                type=type)
            databaseinfradnslist.save()

        dnsname = '%s.%s' % (name, domain)
        return dnsname


def get_dns_name_domain(databaseinfra, name, type, database_sufix=None):
        planattr = PlanAttr.objects.get(dbaas_plan=databaseinfra.plan)
        if database_sufix:
            sufix = '.' + database_sufix
        elif planattr.dnsapi_database_sufix:
            sufix = '.' + planattr.dnsapi_database_sufix
        else:
            sufix = ''

        if type == HOST:
            domain = planattr.dnsapi_vm_domain
        else:
            domain = planattr.dnsapi_database_domain
            name += sufix

        return name, domain
