import requests
from swiftace.utils.authorization import get_auth_header

API_URL = 'https://swiftai-217215.appspot.com'


class ApiError(Exception):
    """Error class for web API related Exceptions"""
    pass


def upload_conda_env(data, name):
    """Upload the anaconda environment to server"""
    files = {'env': ('environment.yml', data)}
    res = requests.post(f'{API_URL}/environment',
                        files=files, data={'name': name})
    if res.status_code == 200:
        res_json = res.json()
        env_hash = res_json['hash']
        return env_hash
    else:
        raise ApiError(f'Evironment upload failed! {res.content}')


def download_conda_env(env_id):
    """Download an anaconda environment to a string"""
    res = requests.get(f'{API_URL}/environment/{env_id}')
    if res.status_code == 200:
        return res.content
    else:
        raise ApiError(f'Environment download failed! {res.content}')


def create_project(slug):
    """Upload the anaconda environment to server"""
    # validate slug
    res = requests.post(f'{API_URL}/project',
                        data={'slug': slug}, headers=get_auth_header())
    if res.status_code == 200:
        res_json = res.json()
        slug = res_json['slug']
        return slug
    else:
        raise ApiError(f'Project init failed! {res.content}')


def create_experiment_run(project_slug, name="", desc=""):
    """Upload the anaconda environment to server"""
    # validate slug
    res = requests.post(f'{API_URL}/experiment',
                        data={'project': project_slug,
                              'name': name, 'desc': desc},
                        headers=get_auth_header())
    if res.status_code == 200:
        res_json = res.json()
        experiment_hash = res_json['hash']
        return experiment_hash
    else:
        raise ApiError(f'Project init failed! {res.content}')
