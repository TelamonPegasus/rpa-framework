from typing import Optional

from . import (
    LibraryContext,
    keyword,
)


class AppsScriptKeywords(LibraryContext):
    """Class for Google Apps Script API

    **Note:** The Apps Script API does not work with _service accounts_

    Following steps are needed to authenticate and use the service:

    1. enable Apps Script API in the Cloud Platform project (GCP)
    2. create OAuth credentials so API can be authorized (download ``credentials.json``
       which is needed to initialize service)
    3. the Google Script needs to be linked to Cloud Platform project number
    4. Google Script needs to have necessary OAuth scopes to access app
       which is being scripted
    5. necessary authentication scopes and credentials.json are needed
       to initialize service and run scripts

    For more information about Google Apps Script API link_.

    .. _link: https://developers.google.com/apps-script/api
    """

    def __init__(self, ctx):
        super().__init__(ctx)
        self.service = None

    @keyword
    def init_apps_script(
        self,
        service_account: str = None,
        credentials: str = None,
        use_robocorp_vault: Optional[bool] = None,
        scopes: list = None,
        token_file: str = None,
    ) -> None:
        """Initialize Google Apps Script client

        :param service_account: file path to service account file
        :param credentials: file path to credentials file
        :param use_robocorp_vault: use credentials in `Robocorp Vault`
        :param scopes: list of extra authentication scopes
        :param token_file: file path to token file
        """
        apps_scopes = ["script.projects"]
        if scopes:
            apps_scopes += scopes
        self.service = self.init_service(
            service_name="script",
            api_version="v1",
            scopes=apps_scopes,
            service_account_file=service_account,
            credentials_file=credentials,
            use_robocorp_vault=use_robocorp_vault,
            token_file=token_file,
        )

    @keyword
    def run_script(
        self, script_id: str, function_name: str, parameters: dict = None
    ) -> None:
        """Run the Google Apps Script function

        :param script_id: Google Script identifier
        :param function_name: name of the script function
        :param parameters: script function parameters as a dictionary
        :raises AssertionError: thrown when Google Script returns errors

        Example:

        .. code-block:: robotframework

            &{params}=    Create Dictionary  formid=aaad4232  formvalues=1,2,3
            ${response}=  Run Script    abc21397283712da  submit_form   ${params}
            Log Many   ${response}
        """
        request = {
            "function": function_name,
        }
        if parameters:
            request["parameters"] = [parameters]
        response = (
            self.service.scripts()
            .run(
                body=request,
                scriptId=script_id,
            )
            .execute()
        )
        if "error" in response.keys():
            raise AssertionError(response["error"])
        return response
