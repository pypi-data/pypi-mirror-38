from datetime import datetime, timedelta
from bingads.v11.reporting import *

from ads_api.credentials import BingAdsCredentials
from ads_api.config import ENVIRONMENT


class BingAdsReportingHelpers:

    authorization_data = BingAdsCredentials.get_bing_auth_data(
        environment=ENVIRONMENT
    )
    reporting_service = ServiceClient(
        'ReportingService',
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
        version=11
    )

    @staticmethod
    def get_report_time(days_from_today=0):
        """
        Simplify the report time construction
        :param days_from_today: Report starts from how many days ago
        :return:
        """

        report_time = BingAdsReportingHelpers.reporting_service.factory.create('ReportTime')

        today = datetime.today()
        start = today - timedelta(days=days_from_today)

        # start date
        custom_date_range_start = BingAdsReportingHelpers.reporting_service.factory.create('Date')
        custom_date_range_start.Day = start.day
        custom_date_range_start.Month = start.month
        custom_date_range_start.Year = start.year
        report_time.CustomDateRangeStart = custom_date_range_start

        # end date
        custom_date_range_end = BingAdsReportingHelpers.reporting_service.factory.create('Date')
        custom_date_range_end.Day = today.day
        custom_date_range_end.Month = today.month
        custom_date_range_end.Year = today.year
        report_time.CustomDateRangeEnd = custom_date_range_end

        # predefined time None
        report_time.PredefinedTime = None

        return report_time

    @staticmethod
    def get_default_report_request(report_type, report_name):
        """
        Specify common analyzable download csv format
        :param report_type:
        :param report_name:
        :return:
        """
        report_request = BingAdsReportingHelpers.reporting_service.factory.create(report_type)
        report_request.Format = 'Csv'
        report_request.ReportName = report_name
        report_request.ReturnOnlyCompleteData = False
        report_request.Language = 'English'
        report_request.ExcludeReportHeader = True
        report_request.ExcludeReportFooter = True

        return report_request
