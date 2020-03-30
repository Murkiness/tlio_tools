import pytest

from ..tools.case_filter import get_filtered_cases, get_case_ids

test_data = [
    {
        "id":1,
        "title":"Fully automated",
        "custom_automation_type":2,
        "custom_ios_automation_type":2,
        "custom_international_android_test_type":2,
        "custom_international_ios_test_type":2
    },
    {
        "id":2,
        "title":"Android automated, ios planned",
        "custom_automation_type":2,
        "custom_ios_automation_type":3,
        "custom_international_android_test_type":2,
        "custom_international_ios_test_type":2
    },
    {
        "id":3,
        "title":"All planned",
        "custom_automation_type":3,
        "custom_ios_automation_type":3,
        "custom_international_android_test_type":2,
        "custom_international_ios_test_type":2
    },
    {
        "id":4,
        "title":"Fully manual",
        "custom_automation_type":1,
        "custom_ios_automation_type":1,
        "custom_international_android_test_type":2,
        "custom_international_ios_test_type":2
    },
    {
        "id":5,
        "title":"Ios internal - android manual",
        "custom_automation_type":1,
        "custom_ios_automation_type":2,
        "custom_international_android_test_type":2,
        "custom_international_ios_test_type":1
    },
    {
        "id":6,
        "title":"Full internal automation",
        "custom_automation_type":2,
        "custom_ios_automation_type":2,
        "custom_international_android_test_type":1,
        "custom_international_ios_test_type":1
    },
    {
        "id":7,
        "title":"Only ios auto",
        "custom_automation_type":1,
        "custom_ios_automation_type":2,
        "custom_international_android_test_type":2,
        "custom_international_ios_test_type":2
    },
    {
        "id":8,
        "title":"Only android auto",
        "custom_automation_type":2,
        "custom_ios_automation_type":1,
        "custom_international_android_test_type":2,
        "custom_international_ios_test_type":2
    },
    
    ]

def test_android_auto_tlio():
    f_cases = get_filtered_cases(test_data, 'automated', 'testlio', 'android')
    ids = get_case_ids(f_cases)

    assert ids == [1, 2, 8]


def test_ios_auto_internal():
    f_cases = get_filtered_cases(test_data, 'automated', 'internal', 'ios')
    ids = get_case_ids(f_cases)

    assert ids == [5, 6]


def test_all_or_auto_tlio():
    f_cases = get_filtered_cases(test_data, 'automated', 'testlio', 'all (OR)')
    ids = get_case_ids(f_cases)

    assert ids == [1, 2, 7, 8]


def test_all_and_auto_tlio():
    f_cases = get_filtered_cases(test_data, 'automated', 'testlio', 'all (AND)')
    ids = get_case_ids(f_cases)

    assert ids == [1]