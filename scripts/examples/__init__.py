from kdb.common.profiles import Profiles
from kdb.scripts import BaseAPI, BasePageObject, MobileAppPageObject


class BaseExampleAPI(BaseAPI):
    def __init__(self, profile: Profiles, path: str):
        super().__init__(profile, path)

    def _execute(self, data: dict | str | None, method: str = 'POST', headers: dict = None,
                 override_profile_data: dict = None, url_params: dict = None, **kwargs):
        super()._execute(data, method, headers, override_profile_data, url_params, **kwargs)
        return self

    def _define_any_common_function_if_you_need(self):
        return self


class BaseExamplePageObject(BasePageObject):

    def __init__(self, profile: Profiles, path: str, page_title: str = None, page_loaded_text: str = None):
        super().__init__(profile, path, page_title, page_loaded_text)


class BaseMobileAppPageObject(MobileAppPageObject):

    def __init__(self, profile: Profiles):
        super().__init__(profile)
