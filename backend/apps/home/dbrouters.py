from .models import StatisticsValues, LsClaimList, LsEventList, ClOap, ClRegion, ClPersonList


class MyDBRouter(object):

    def db_for_read(self, model, **hints):
        if model in (StatisticsValues, LsClaimList, LsEventList, ClOap, ClRegion, ClPersonList):
            return 'kas'
        return None

    def db_for_write(self, model, **hints):
        if model in (StatisticsValues, LsClaimList, LsEventList, ClOap, ClRegion, ClPersonList):
            return 'kas'
        return None
