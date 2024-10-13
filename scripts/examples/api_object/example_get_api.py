from kdb.common.profiles import Profiles

from scripts.examples import BaseExampleAPI


class ExampleGetAPI(BaseExampleAPI):
    def __init__(self, profile: Profiles):
        super().__init__(profile, "/posts/{id}")

    def execute(self, data_id: int | str, headers: dict = None):

        url_params = {'id': data_id}

        super()._execute(None, self.GET_METHOD, headers, url_params=url_params)
        return self
