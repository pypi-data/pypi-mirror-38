# -*- coding: utf-8 -*-

import requests
import shutil

"""
 http, https url 파일 다운로드
"""
def download_file(url, downloadPath, fileOpenMode = 'wb',
auth_verify=False, auth_id='usrname', auth_pw='password'
):
    r = requests.get(url, auth=(auth_id, auth_pw), verify=auth_verify,stream=True)
    r.raw.decode_content = True        
    with open(downloadPath, fileOpenMode) as f:
        shutil.copyfileobj(r.raw, f)