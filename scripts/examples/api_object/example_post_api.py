from kdb.common.profiles import Profiles

from scripts.examples import BaseExampleAPI


class ExamplePostAPI(BaseExampleAPI):
    def __init__(self, profile: Profiles):
        super().__init__(profile, "/posts")

    def execute(self, data: dict | str, headers: dict = None, url_params: dict = None):
        super()._execute(data, self.POST_METHOD, headers, url_params=url_params)
        return self
