from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.campaign import Campaign

import sys

from env import ACCESS_TOKEN, CAMPAIGN_ID

FacebookAdsApi.init(access_token=ACCESS_TOKEN)

campaign = Campaign(fbid=CAMPAIGN_ID)

ad_sets = campaign.get_ad_sets(fields=['name'])

since = sys.argv[1] if len(sys.argv) > 1 else '2017-05-10'
until = sys.argv[2] if len(sys.argv) > 2 else '2019-04-18'

metric = sys.argv[3] if len(sys.argv) > 3 else 'link_click'


def find_cost_per_action_type(action_type, list):
    for entry in list:
        if metric == entry['action_type']:
            return float(entry['value'])
    return None


def get_insights(ad_set, action_type):
    insight_list = ad_set.get_insights(
        fields=['cost_per_action_type'],
        params={
            'time_range': {
                'since': since,
                'until': until
            }
        }
    )

    if len(insight_list) > 0 and 'cost_per_action_type' in insight_list[0]:
        cost = find_cost_per_action_type(
            action_type,
            insight_list[0]['cost_per_action_type']
        )

        if cost is None:
            return None

        return {
            'ad_set': ad_set,
            'cost': cost
        }
    return None


ad_set_insights = []

for ad_set in ad_sets:
    insights = get_insights(ad_set, metric)
    if insights is not None:
        ad_set_insights.append(insights)

cheapest_ad_set = None
cheapest_cost = 0

for pair in ad_set_insights:
    ad_set = pair['ad_set']
    cost = pair['cost']

    if cheapest_ad_set is None or cheapest_cost > cost:
        cheapest_ad_set = ad_set
        cheapest_cost = cost

if cheapest_ad_set is None:
    print('No metrics found')
else:
    print(f"{cheapest_ad_set['name']} {cheapest_cost}")
