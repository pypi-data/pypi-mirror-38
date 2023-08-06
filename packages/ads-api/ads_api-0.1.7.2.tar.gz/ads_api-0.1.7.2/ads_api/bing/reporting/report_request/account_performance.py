from ads_api.bing.reporting.reporting_helpers import BingAdsReportingHelpers
from ads_api.config import ACCOUNTSTATS


def get_account_performance_report_request():
    """
    Build a account performance report request, including Format, ReportName, Aggregation,
    Scope, Time, Filter, and Columns.
    """
    report_request = BingAdsReportingHelpers.get_default_report_request(
        report_type='AccountPerformanceReportRequest',
        report_name='My Account Performance Report'
    )

    report_request.Aggregation = 'Summary'

    scope = BingAdsReportingHelpers.reporting_service.factory.create('AccountReportScope')
    # scope.AccountIds = {'long': None}
    scope.AccountIds = None
    report_request.Scope = scope

    report_request.Time = BingAdsReportingHelpers.get_report_time(1)

    # If you specify a filter, results may differ from data you see in the Bing Ads web application

    report_filter = BingAdsReportingHelpers.reporting_service.factory.create('AccountPerformanceReportFilter')
    report_filter.AccountStatus = ACCOUNTSTATS
    report_request.Filter = report_filter

    # Specify the attribute and data report columns.

    report_columns = BingAdsReportingHelpers.reporting_service.factory.create('ArrayOfAccountPerformanceReportColumn')
    report_columns.AccountPerformanceReportColumn.append([
        'AccountName',
        'AccountId',
        'Spend'
    ])
    report_request.Columns = report_columns

    return report_request
