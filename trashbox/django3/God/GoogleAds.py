#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from googleads import adwords

PAGE_SIZE = 100

def get_ads_selector(request_type, requested_attribute_types, queries):
    ads_selector = {'ideaType': 'KEYWORD', 'requestType': request_type}
    ads_selector['requestedAttributeTypes'] = requested_attribute_types
    ads_selector['paging'] = {'startIndex': '0', 'numberResults': str(PAGE_SIZE)}
    ads_selector['searchParameters'] = [{
        'xsi_type': 'RelatedToQuerySearchParameter',
        'queries': queries
    }]
    ads_selector['searchParameters'].append({
        'xsi_type': 'LanguageSearchParameter',
        'languages': [{'id': '1005'}]
    })
    ads_selector['searchParameters'].append({
        'xsi_type': 'NetworkSearchParameter',
        'networkSetting': {
            'targetGoogleSearch': True,
            'targetSearchNetwork': False,
            'targetContentNetwork': False,
            'targetPartnerSearchNetwork': False
        }
    })
    return ads_selector

def get_ads_results(ads_selector):
    ads_list = []
    page = {}
    try:
        page = targeting_idea_service.get(ads_selector)
    except Exception as e:
        print(e)

    if 'entries' in page:
        for result in page['entries']:
            attributes = {}
            for attribute in result['data']:
                attributes[attribute['key']] = getattr(attribute['value'], 'value', '0')
            if isinstance(attributes['AVERAGE_CPC'], str):
                average_cpc = int(attributes['AVERAGE_CPC'])
            elif attributes['AVERAGE_CPC'] is None:
                average_cpc = 0
            else:
                average_cpc = int(attributes['AVERAGE_CPC']['microAmount'])//1000000
            if attributes['COMPETITION'] is None:
                competition = 0.0
            else:
                competition = attributes['COMPETITION']
            if attributes['SEARCH_VOLUME'] is not None and int(attributes['SEARCH_VOLUME']) > 0:
                record = {
                    'keyword': attributes['KEYWORD_TEXT'],
                    'search_volume': attributes['SEARCH_VOLUME'],
                    'average_cpc': average_cpc,
                    'competition': competition
                }
                ads_list.append(record)
    else:
        print('Adwords API: No related keywords were found.')
    return ads_list

def main(target_keywords):
    ads_selector = get_ads_selector('IDEAS', ['KEYWORD_TEXT', 'SEARCH_VOLUME', 'AVERAGE_CPC', 'COMPETITION'], target_keywords)
    ads_list = get_ads_results(ads_selector)

    targetidea_list = []
    cnt = 0
    for row in ads_list:
        cnt += 1
        str_search_volume = str(int(row['search_volume']))
        str_average_cpc   = str(int(row['average_cpc']))
        float_competition = float(row['competition'])
        str_competition = '%.3f' % float_competition
        if float_competition >= 0.67:
            str_competition_rank = '高'
        elif float_competition >= 0.43:
            str_competition_rank = '中'
        else:
            str_competition_rank = '低'
        record = {
            'no': cnt,
            'keyword': row['keyword'],
            'search_volume': str_search_volume,
            'average_cpc': str_average_cpc,
            'competition': str_competition,
            'competition_rank': str_competition_rank
        }
        targetidea_list.append(record)

    print(targetidea_list)

if __name__ == '__main__':
    ads_client = adwords.AdWordsClient.LoadFromStorage()
    targeting_idea_service = ads_client.GetService('TargetingIdeaService', version='v201806')

    target_keywords = ['ダイエット']
    main(target_keywords)
