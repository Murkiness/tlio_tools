import json

from django.shortcuts import render
from django.http import JsonResponse

from .testdroid_api_client.api_client import get_avaiable_devices

def available_devices(request):

    data = get_avaiable_devices()['data']
    new_data = get_processed_response(data)
    return JsonResponse(new_data, safe=False)


def get_processed_response(data):
    return list(map(_transform_json_response_for_devices, data))


def _transform_json_response_for_devices(object):
    new_object = {}
    new_object['name'] = object["displayName"]
    new_object['os'] = object['osType']
    new_object['os_version'] = object['softwareVersion']['releaseVersion']

    return new_object