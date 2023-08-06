from simpleatlassian.common import Atlassian


class JIRA(Atlassian):
    def get_all(self, url, max=None, params=None, resultfield='values', *kargs, **kwargs):
        limit = self.page_size
        offset = 0
        if params is None:
            params = {}

        while True:
            params.update({'maxResults': limit, 'startAt': offset})
            d = self.get(url, *kargs, params=params, **kwargs)

            if d is None:
                return

            for value in d[resultfield]:
                yield value
            offset += len(d[resultfield])

            if d.get('isLast', False) or offset >= d.get('total', 1e8) or (max is not None and offset >= max):
                return
