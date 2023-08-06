import re

from ads_api.credentials import GoogleAdsCredentials
from pathlib import Path
import os
import csv
from enum import Enum


class Columns(Enum):
    Date = 'Date'
    CampaignId = 'CampaignId'
    CampaignName = 'CampaignName'
    AdGroupId = 'AdGroupId',
    AdGroupName = 'AdGroupName'
    CpcBid = 'CpcBid'
    Device = 'Device'
    AverageCost = 'AverageCost'
    SearchExactMatchImpressionShare = 'SearchExactMatchImpressionShare'
    SearchImpressionShare = 'SearchImpressionShare'
    Conversions = 'Conversions'
    Cost = 'Cost'
    Impressions = 'Impressions'
    Clicks = 'Clicks'
    Criteria = 'Criteria'
    Id = 'Id'
    CostPerConversion = 'CostPerConversion'
    SystemServingStatus = 'SystemServingStatus'


class GoogleAdwordsReport:

    @staticmethod
    def download_report(adwords_client, report_query, dir, filename, include_zero_impressions=True):

        report_downloader = adwords_client.GetReportDownloader(version='v201705')

        datafolder = os.path.join("./downloads", dir)
        if not os.path.exists(datafolder):
            os.mkdir(datafolder)

        path = os.path.join(datafolder, filename)

        print("Download Report For: ", adwords_client.client_customer_id)

        with open(path, 'w') as output_file:
            report_downloader.DownloadReportWithAwql(
                report_query, 'CSV', output_file, skip_report_header=True,
                skip_column_header=False, skip_report_summary=True,
                include_zero_impressions=include_zero_impressions)

    @staticmethod
    def download_report_string(adwords_client, report_query, include_zero_impressions=True):

        report_downloader = adwords_client.GetReportDownloader(version='v201802')

        return report_downloader.DownloadReportAsStringWithAwql(
            report_query, 'CSV', skip_report_header=True, skip_column_header=True,
            skip_report_summary=True, include_zero_impressions=include_zero_impressions
        )

    @staticmethod
    def get_campaign_adgroups_string(client_customer_id):

        report_query = ('SELECT CampaignId, CampaignName, AdGroupId, AdGroupName '
                        'FROM ADGROUP_PERFORMANCE_REPORT '
                        'WHERE AdGroupStatus IN [ENABLED] AND '
                        'CampaignStatus IN [ENABLED]')

        campaign_adgroups = GoogleAdwordsReport.download_report_string(
            adwords_client=GoogleAdsCredentials.get_google_client(client_customer_id),
            report_query=report_query
        )

        return campaign_adgroups

    @staticmethod
    def get_campaign_adgroups(client_customer_id):

        enabled_campaign_adgroups = GoogleAdwordsReport.get_campaign_adgroups_string(client_customer_id)

        # print('length of campaign adgroups: ', len(enabled_campaign_adgroups))
        records = []

        for record in enabled_campaign_adgroups.splitlines():

            try:
                # campaign_id, campaign_name, ad_group_id, ad_group_name = record.split(',')
                campaign_id, campaign_name, ad_group_id, ad_group_name = \
                    re.split(',(?=(?:[^"]*"[^"]*")*[^"]*$)', record)

                record = {
                    'campaign_id': campaign_id,
                    'campaign_name': campaign_name,
                    'ad_group_id': ad_group_id,
                    'ad_group_name': ad_group_name,
                    'target_position': 2.0,
                    'cpc_constraint': 25.0
                }
                records.append(record)

            except Exception as e:
                print('failed record: ', record.split(','), e)
                print('re split: ', re.split(',(?=(?:[^"]*"[^"]*")*[^"]*$)', record))

        return records

    @staticmethod
    def get_active_accounts():

        accounts = []

        with open('ads_api/downloads/google/accounts_summary.csv', 'r') as f:
            csv_reader = csv.DictReader(f)
            for row in csv_reader:
                accounts.append(
                    {
                        "account": row['account'],
                        "platform_id": row['platform_id'],
                        "str": "{} ({})".format(row['account'], row['platform_id'])
                    }
                )

        return accounts

    @staticmethod
    def download_active_accounts():

        print("download google accounts. ...")
        client = GoogleAdsCredentials.get_google_client("279-940-3165")
        managed_customer_service = client.GetService(
            'ManagedCustomerService', version='v201705')

        accounts = managed_customer_service.get({'fields': ['CustomerId', 'Name']})
        pattern = re.compile(r'^(\d{3})(\d{3})(\d{4})$')

        datafolder = "ads_api/downloads/google"

        os.makedirs(datafolder, exist_ok=True)

        file_path = os.path.join(datafolder, 'accounts_summary.csv')
        print(accounts.entries[:3])

        with open(file_path, 'w') as f:
            csv_writer = csv.DictWriter(f, fieldnames=['platform_id', 'account'])
            csv_writer.writeheader()
            csv_writer.writerows(
                [
                    {
                        "account": str(account.name),
                        "platform_id": pattern.sub(r'\1-\2-\3', str(account.customerId))
                    } for account in accounts.entries
                ]
            )

        print("accounts downloaded in " + os.path.abspath(file_path))

