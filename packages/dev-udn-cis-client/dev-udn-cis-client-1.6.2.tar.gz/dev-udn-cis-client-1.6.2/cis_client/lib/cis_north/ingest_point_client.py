import json
import requests

import urllib3

from cis_client.lib import base_http_client


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class IngestPointClient(base_http_client.BaseClient):
    def __init__(self, north_host, insecure=False):
        super(IngestPointClient, self)
        self.north_host = north_host
        self.insecure = insecure

    def get(self, auth_token, ingest_point, **kwargs):
        endpoint = self.get_endpoint(ingest_point)
        response = requests.get(
            endpoint,
            verify=(not self.insecure),
            headers={"X-Auth-Token": auth_token},
            params=self.get_auth_params(**kwargs)
        )
        base_http_client.raise_for_http_response(
            response,
            'Getting of ingest-point "{ingest_point}", brand-id="{brand_id}", '
            'account-id="{account_id}", group-id="{group_id}" was failed.'.format(
                ingest_point=ingest_point,
                brand_id=kwargs.get('brand_id', ''),
                account_id=kwargs.get('account_id', ''),
                group_id=kwargs.get('group_id', '')
            ))
        return json.loads(response.content)

    def list(self, auth_token, **kwargs):
        endpoint = '{north_host}/ingest_points'.format(north_host=self.north_host)
        params = self.get_auth_params(**kwargs)
        params['format'] = 'only_ids'
        response = requests.get(
            endpoint,
            verify=(not self.insecure),
            headers={"X-Auth-Token": auth_token},
            params=params
        )
        base_http_client.raise_for_http_response(
            response,
            'Listing of ingest-points for brand-id="{brand_id}", '
            'account-id="{account_id}", group-id="{group_id}" was failed.'.format(
                brand_id=kwargs.get('brand_id', ''),
                account_id=kwargs.get('account_id', ''),
                group_id=kwargs.get('group_id', '')
            ))
        return json.loads(response.content)

    def add(self, auth_token, ingest_point, clusters, **kwargs):
        data = {
            "clusters": clusters,
        }
        workflow_data = {}
        if kwargs.get('workflow_id'):
            workflow_data['id'] = kwargs.get('workflow_id')
        if kwargs.get('profile_ids'):
            workflow_data['profile_ids'] = kwargs['profile_ids']
        if workflow_data:
            data['workflow'] = workflow_data
        if kwargs.get('estimated_usage'):
            data['estimated_usage'] = kwargs['estimated_usage']
        response = requests.post(
            self.get_endpoint(ingest_point),
            verify=(not self.insecure),
            headers={
                "X-Auth-Token": auth_token
            },
            params=self.get_auth_params(**kwargs),
            json=data
        )
        base_http_client.raise_for_http_response(
            response, 'Adding of ingest-point was failed.')
        return json.loads(response.content)

    def remove(self, auth_token, ingest_point, **kwargs):
        response = requests.delete(
            self.get_endpoint(ingest_point),
            verify=(not self.insecure),
            headers={
                "X-Auth-Token": auth_token
            },
            params=self.get_auth_params(**kwargs),
        )
        base_http_client.raise_for_http_response(
            response,
            'Removing of ingest-point "{ingest_point}", brand-id="{brand_id}", '
            'account-id="{account_id}", group-id="{group_id}" was failed.'.format(
                ingest_point=ingest_point,
                brand_id=kwargs.get('brand_id', ''),
                account_id=kwargs.get('account_id', ''),
                group_id=kwargs.get('group_id', '')
            ))

    def get_endpoint(self, ingest_point):
        endpoint = '{north_host}/ingest_points/{ingest_point}'.format(
            north_host=self.north_host,
            ingest_point=ingest_point
        )
        return endpoint


@base_http_client.with_auth
def get_ingest_point(north_host, ingest_point_name, **kwargs):
    """Gets ingest points

    :param north_host:
    :param ingest_point_name:
    :param kwargs: can contains
        - brand_id: Brand ID
        - account_id: account ID
        - group_id: group ID
        - insecure: True if SSL verification must be skipped
        - aaa_host: AAA host, optional
        - username: username, optional
        - password: password, optional
        - token: auth token, must be specified if aaa_host,
                 username and password is not specified
    :return: ingest point info
    """
    ingest_point_client = IngestPointClient(north_host, insecure=kwargs['insecure'])
    return ingest_point_client.get(kwargs['token'], ingest_point_name, **kwargs)


@base_http_client.with_auth
def list_ingest_points(north_host, **kwargs):
    """Gets ingest points

    :param north_host:
    :param kwargs: can contains
        - brand_id: Brand ID
        - account_id: account ID
        - group_id: group ID
        - offset: offset
        - page_size: size of page, -1 means all rows
        - insecure: True if SSL verification must be skipped
        - aaa_host: AAA host, optional
        - username: username, optional
        - password: password, optional
        - token: auth token, must be specified if aaa_host,
                 username and password is not specified
    :return: list of ingest points
    """
    ingest_point_client = IngestPointClient(north_host, insecure=kwargs['insecure'])
    return ingest_point_client.list(kwargs['token'], **kwargs)


@base_http_client.with_auth
def add_ingest_point(north_host, ingest_point, clusters, **kwargs):
    """Adds ingest point

    :param north_host:
    :param ingest_point: Name of the ingest point
    :param clusters: List of cluster associated with ingest point.
    :param kwargs: can contains
        - brand_id: Brand ID
        - account_id: account ID
        - group_id: group ID
        - estimated_usage: Integer
        - workflow_id: Workflow ID
        - profile_ids: List of profile IDs like ["abr_tv_16_9_high", "abr_mobile_16_9_low"]
        - insecure: True if SSL verification must be skipped
        - aaa_host: AAA host, optional
        - username: username, optional
        - password: password, optional
        - token: auth token, must be specified if aaa_host,
                 username and password is not specified
    :return: added ingest point
    """
    ingest_point_client = IngestPointClient(north_host, insecure=kwargs['insecure'])
    return ingest_point_client.add(kwargs['token'], ingest_point, clusters, **kwargs)


@base_http_client.with_auth
def remove_ingest_point(north_host, ingest_point, **kwargs):
    """Removes ingest point

    :param north_host:
    :param ingest_point: Name of the ingest point
    :param kwargs: can contains
        - brand_id: Brand ID
        - account_id: account ID
        - group_id: group ID
        - insecure: True if SSL verification must be skipped
        - aaa_host: AAA host, optional
        - username: username, optional
        - password: password, optional
        - token: auth token, must be specified if aaa_host,
                 username and password is not specified
    """
    ingest_point_client = IngestPointClient(north_host, insecure=kwargs['insecure'])
    return ingest_point_client.remove(kwargs['token'], ingest_point, **kwargs)
