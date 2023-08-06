from simpleatlassian.common import Atlassian


class BitBucket(Atlassian):
    def get_all(self, url, max=None, params=None, resultfield='values', *kargs, **kwargs):
        limit = self.page_size
        offset = 0
        if params is None:
            params = {}

        while True:
            params.update({'limit': limit, 'start': offset})
            d = self.get(url, *kargs, params=params, **kwargs)

            if d is None:
                return

            for value in d[resultfield]:
                yield value
            offset += len(d[resultfield])

            if d.get('isLastPage', False) or (max is not None and offset >= max):
                return
