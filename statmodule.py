from datetime import datetime, timedelta


class Last24Stat:
    def __init__(self):
        self._counts = {}

    @property
    def now(self):
        now = datetime.now()
        # 'rounded' time to hours
        now = now.replace(microsecond=0, second=0, minute=0)
        return now

    def increase(self, n=1):
        self.update()
        now = self.now
        self._counts[now] = self._counts.get(now, 0) + n

    def update(self):
        now = self.now
        td = timedelta(hours=24)
        self._counts = {k: v for k, v in self._counts.items() if (now - k) < td}

    def get(self):
        self.update()
        return sum(self._counts.values())


class TotalDone:
    def __init__(self):
        self._last_stat = Last24Stat()
        self._total = 0

    def increase(self, n=1):
        self._last_stat.increase(n)
        self._total += n

    def get(self):
        return self._total, self._last_stat.get()


class TotalChange(Last24Stat):
    def __init__(self, total=0):
        Last24Stat.__init__(self)
        #now = self.now - timedelta(hours=1)
        #self._counts[now] = 0

    def set(self, n=1):
        now = self.now
        self._counts[now] = n

    def last(self):
        return 0 if not self._counts else self._counts[min(self._counts)]

    def first(self):
        return 0 if not self._counts else self._counts[max(self._counts)]

    def get(self):
        self.update()
        first = self.first()
        last = self.last()
        return first, first - last


if __name__ == "__main__":
    pass

