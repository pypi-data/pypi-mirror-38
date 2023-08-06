@staticmethod
def download_campaign_adgroups(account_id):
    account_id = int(account_id)
    report_request = BingAdsDownload.get_campaign_adgroups_report_request(account_id)

    folder = "../downloads/bing/{}".format(account_id)
    if not os.path.exists(folder):
        os.makedirs(folder)

    reporting_download_parameters = ReportingDownloadParameters(
        report_request=report_request,
        result_file_directory=folder,
        result_file_name="active_campaign_adgroups.csv",
        overwrite_result_file=True,  # Set this value true if you want to overwrite the same file.
        timeout_in_milliseconds=30000
    )

    print("Awaiting Background Completion . . .");
    result_file_path = BingAdsDownload.reporting_service_manager.download_file(reporting_download_parameters)
    print("Download result file: {0}\n".format(result_file_path))

    return result_file_path