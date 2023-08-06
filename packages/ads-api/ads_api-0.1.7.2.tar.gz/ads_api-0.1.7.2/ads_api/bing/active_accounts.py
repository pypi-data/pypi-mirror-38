@staticmethod
def download_active_accounts():
    report_request = BingAdsDownload.get_account_performance_report_request()

    folder = "../downloads/bing"
    if not os.path.exists(folder):
        os.makedirs(folder)

    reporting_download_parameters = ReportingDownloadParameters(
        report_request=report_request,
        result_file_directory=folder,
        result_file_name="accounts_summary.csv",
        overwrite_result_file=True,  # Set this value true if you want to overwrite the same file.
        timeout_in_milliseconds=30000
    )

    print("Awaiting Background Completion . . .")
    result_file_path = BingAdsDownload.reporting_service_manager.download_file(reporting_download_parameters)
    print("Download result file: {0}\n".format(result_file_path))

    return result_file_path


    def get_active_accounts():

        file_path = BingAdsDownload.download_active_accounts()

        records = []
        with open(file_path, 'r', encoding='utf-8-sig') as f:

            csv_reader = csv.reader(f)

            header1, header2 = next(csv_reader)[:-1]
            assert header1 == 'AccountName' and header2 == 'AccountId'

            for account_name, account_id, _ in csv_reader:

                records.append({
                    "account": account_name,
                    "client_customer_id": account_id,
                    "str": "{} ({})".format(
                        account_name, account_id
                    )
                })

        return records