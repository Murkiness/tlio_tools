from django.shortcuts import render, redirect

from django.http import JsonResponse

from .tools.case_filter import get_specific_case_ids, get_filtered_cases, get_case_ids, get_all_cases

import pickle
import os


def get_file_with_cases(request):
    auto, team, platform = _parse_params(request.body)
    all_cases = load_cases()

    filtered_cases = get_filtered_cases(all_cases, auto, team, platform)
    cids = get_case_ids(filtered_cases)

    return JsonResponse(cids, safe=False)


def _parse_params(body):
    _str = body.decode("UTF-8")
    _dict = eval(_str)
    auto = _dict.get('auto_value')
    team = _dict.get('team')
    platform = _dict.get('platform')

    return auto, team, platform


def load_cases():
    all_cases = None
    if os.path.exists('cases.dump'):
        with open('cases.dump', 'rb') as f:
            all_cases = pickle.load(f)
    else:
        all_cases = get_all_cases()
        with open('cases.dump', 'wb') as f:
            pickle.dump(all_cases, f)

    return all_cases