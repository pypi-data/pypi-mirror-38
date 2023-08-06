from bingads.v11.reporting import *
from io import BytesIO
import os

from ads_api.credentials import BingAdsCredentials
from ads_api.config import ENVIRONMENT


class BingAdsDownload:

    authorization_data = BingAdsCredentials.get_bing_auth_data(
        environment=ENVIRONMENT
    )
    reporting_service = ServiceClient(
        'ReportingService',
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
        version=11
    )
    reporting_service_manager = ReportingServiceManager(
        authorization_data=authorization_data,
        poll_interval_in_milliseconds=1000,
        environment=ENVIRONMENT,
    )

    @staticmethod
    def download_helper(report_request, download_file_name):

        account_ids = report_request.Scope.AccountIds
        print(account_ids)

        if account_ids is None:
            folder = "../downloads/bing"
        else:
            assert len(account_ids['long']) == 1
            folder = "../downloads/bing/{}".format(account_ids['long'][0])

        if not os.path.exists(folder):
            os.makedirs(folder)

        reporting_download_parameters = ReportingDownloadParameters(
            report_request=report_request,
            result_file_directory=folder,
            result_file_name=download_file_name,
            overwrite_result_file=True,  # Set this value true if you want to overwrite the same file.
            timeout_in_milliseconds=30000
        )

        result_file_path = BingAdsDownload.reporting_service_manager.download_file(reporting_download_parameters)
        print("Download result file: {0}\n".format(result_file_path))

        return result_file_path

    @staticmethod
    def download_report_as_string(report_request, timeout_in_milliseconds=30000):

        operation = BingAdsDownload.reporting_service_manager.submit_download(report_request)
        try:
            operation.track(timeout_in_milliseconds)
        except TimeoutException:
            raise ReportingDownloadException("Reporting file download tracking status timeout.")

        url = operation.final_status.report_download_url

        headers = {
            'User-Agent': USER_AGENT,
        }
        s = requests.Session()
        s.mount('https://', TlsHttpAdapter())
        timeout_seconds = None if timeout_in_milliseconds is None else timeout_in_milliseconds / 1000.0
        try:
            r = s.get(url, headers=headers, verify=True, timeout=timeout_seconds)

            with contextlib.closing(zipfile.ZipFile(BytesIO(r.content))) as compressed:
                first = compressed.namelist()[0]
                return compressed.read(first)
        except requests.Timeout as ex:
            raise FileDownloadException(ex)
