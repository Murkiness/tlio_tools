from .testrail_api_client import APIClient


team_values = {
    'internal': 1,
    'testlio': 2
}

auto_tag_values = {
    'planned': 3,
    'automated': 2,
    'manual': 1
}

dict_keys_for_platform = {
    'android': ('custom_automation_type', 'custom_international_android_test_type'),
    'ios': ('custom_ios_automation_type', 'custom_international_ios_test_type')
}

def get_all_cases():
    client = APIClient("https://cbsientqa.testrail.io/")
    return client.get_all_cases()


def get_specific_case_ids(auto_tag_value: str, team_value: str, platform: str) -> [str]:
    cases = get_all_cases()
    f_cases = get_filtered_cases(cases, auto_tag_value, team_value, platform)
    only_ids = get_case_ids(f_cases)
    return only_ids

def get_case_ids(cases: [dict]) -> [str]:
    return list(map(lambda case: case.get('id'), cases))


def get_filtered_cases(cases: [dict], auto_tag_value: str, team_value: str, platform: str) -> [str]:
    # auto, testlio, android   x.get('custom_automation_type') == 2 and x.get('custom_international_android_test_type') == 2
    # auto, testlio, both (or) x.get('custom_automation_type') == 2 and x.get('custom_international_android_test_type') == 2 or x.get('custom_ios_automation_type') == 2 and x.get('custom_international_ios_test_type') == 2)

    filtered_cases = []
    filter_func = get_filter_function(auto_tag_value, team_value, platform)
    for c in cases:
        if filter_func(c):
            filtered_cases.append(c)

    return filtered_cases


def get_filter_function(auto_tag_value: str, team_value: str, platform: str):
    filter_func = None
    if platform in dict_keys_for_platform.keys():
        filter_func = get_filter_function_for_platform(auto_tag_value, team_value, platform)
    else:
        func1 = get_filter_function_for_platform(auto_tag_value, team_value, 'android')
        func2 = get_filter_function_for_platform(auto_tag_value, team_value, 'ios')
        if 'OR' in platform:
            filter_func = lambda case: func1(case) or func2(case)
        else:
            filter_func = lambda case: func1(case) and func2(case)

    return filter_func


def get_filter_function_for_platform(auto_tag_value: str, team_value: str, platform: str):
    ''' This method should accept only android or ios as platform param '''

    auto_key, team_key = dict_keys_for_platform.get(platform)
    parsed_team_value = team_values.get(team_value)
    parsed_auto_value = auto_tag_values.get(auto_tag_value)
    filter_func = lambda case: case.get(auto_key) == parsed_auto_value and case.get(team_key) == parsed_team_value
    return filter_func


    