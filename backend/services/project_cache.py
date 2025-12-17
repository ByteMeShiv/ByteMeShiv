import time

class ProjectCache:
    def __init__(self):
        self.data = []
        self.last_fetched = 0
        self.cache_duration = 1800  

    def is_valid(self):
        return (time.time() - self.last_fetched) < self.cache_duration

    def update(self, data):
        self.data = data
        self.last_fetched = time.time()


project_cache = ProjectCache()
