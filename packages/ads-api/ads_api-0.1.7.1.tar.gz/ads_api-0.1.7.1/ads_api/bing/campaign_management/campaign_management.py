from ads_api.credentials import BingAdsCredentials
from ads_api.config import ENVIRONMENT
from bingads.v11.reporting import *
from suds.sudsobject import asdict


class BingCampaignManagement:

    def __init__(self, account_id):

        self.account_id = account_id
        self.authorization_data = BingAdsCredentials.get_bing_auth_data(
            environment=ENVIRONMENT, account_id=self.account_id
        )
        self.campaign_management_service = ServiceClient(
            service='CampaignManagementService',
            authorization_data=self.authorization_data,
            environment=ENVIRONMENT,
            version=11
        )

    def create_device_ad_group_criterion(self, ad_group_id, device_name, device_multiplier):

        biddable_ad_group_criterion = self.campaign_management_service.factory.create('BiddableAdGroupCriterion')

        device_criterion = self.campaign_management_service.factory.create('DeviceCriterion')
        device_criterion.Type = 'DeviceCriterion'
        device_criterion.DeviceName = device_name

        bid_multiplier = self.campaign_management_service.factory.create('BidMultiplier')
        bid_multiplier.Type = 'BidMultiplier'
        bid_multiplier.Multiplier = device_multiplier

        biddable_ad_group_criterion.Status = None
        biddable_ad_group_criterion.EditorialStatus = None
        biddable_ad_group_criterion.CriterionBid = bid_multiplier
        biddable_ad_group_criterion.Criterion = device_criterion

        biddable_ad_group_criterion.AdGroupId = ad_group_id

        print('biddable ad group criterions: ', asdict(biddable_ad_group_criterion))

        return biddable_ad_group_criterion

    def update_adgroup_criterions(self, ad_group_id, device_multipliers):

        DEVICE_AD_GROUP_CRITERION_TYPE = ['Device']

        ad_group_criterions = self.campaign_management_service.GetAdGroupCriterionsByIds(
            AdGroupId=ad_group_id,
            AdGroupCriterionIds=None,
            CriterionType=DEVICE_AD_GROUP_CRITERION_TYPE
        )

        if str(ad_group_criterions) != '':

            for ad_group_criterion in ad_group_criterions.AdGroupCriterion:

                multiplier = device_multipliers[ad_group_criterion.Criterion.DeviceName]
                ad_group_criterion.CriterionBid.Multiplier = multiplier

            return self.campaign_management_service.UpdateAdGroupCriterions(ad_group_criterions, 'Targets')

        else:

            ad_group_criterions = self.campaign_management_service.factory.create('ArrayOfAdGroupCriterion')

            print('ad group criterions: ', asdict(ad_group_criterions))

            for device_name, multiplier in device_multipliers.items():
                device_ad_group_criterion = self.create_device_ad_group_criterion(
                    ad_group_id=ad_group_id,
                    device_name=device_name,
                    device_multiplier=multiplier
                )
                ad_group_criterions.AdGroupCriterion.append(device_ad_group_criterion)

            return self.campaign_management_service.AddAdGroupCriterions(ad_group_criterions, 'Targets')


if __name__ == '__main__':

    bcm = BingCampaignManagement(140090722)

    DEVICE_AD_GROUP_CRITERION_TYPE = ['Device']

    ad_group_criterions = bcm.campaign_management_service.GetAdGroupCriterionsByIds(
        AdGroupId=1144591820452103,
        AdGroupCriterionIds=None,
        CriterionType=DEVICE_AD_GROUP_CRITERION_TYPE
    )
    # BingCampaignManagement.bid_multiplier_test(bcm.campaign_management_service)
    # print(BingCampaignManagement.get_ad_group_criterions(bcm.campaign_management_service))
    device_multipliers = {'Computers': 1, 'Smartphones': 2, 'Tablets': 1}
    update_status = bcm.update_adgroup_criterions(1144591820452103, device_multipliers)
    print('update status: ', update_status)
    # criterion = bcm.get_ad_group_criterions(1145691293247928)
    # criterion = bcm.get_ad_group_criterions(1146790696075113)
    # print('criterion: ', criterion)
    # print('criterion: ', str(criterion) == '')
    # print('criterion: ', criterion is None)
