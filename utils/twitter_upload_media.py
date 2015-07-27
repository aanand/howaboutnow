from __future__ import unicode_literals

import os

import mimetypes
from tweepy.binder import bind_api


def upload_media(api, filename):
    media_type, headers, post_data = pack_media(filename, 'media')
    kwargs = dict(headers=headers, post_data=post_data)

    total_bytes = os.path.getsize(filename)

    media_id = init(
        api,
        media_type=media_type,
        total_bytes=total_bytes,
    )

    append(
        api,
        media_id=media_id,
        segment_index='0',
        headers=headers,
        post_data=post_data,
    )

    finalize(
        api,
        media_id=media_id,
    )

    return media_id


upload_kwargs = dict(
    path='/media/upload.json',
    method='POST',
    require_auth=True,
    upload_api=True,
)


def init(api, **kwargs):
    return bind_api(
        api=api,
        allowed_param=['command', 'media_type', 'total_bytes'],
        payload_type='json',
        **upload_kwargs
    )(command='INIT', **kwargs)['media_id_string']


def append(api, **kwargs):
    return bind_api(
        api=api,
        allowed_param=['command', 'media_id', 'media'],
        **upload_kwargs
    )(command='APPEND', **kwargs)


def finalize(api, **kwargs):
    return bind_api(
        api=api,
        allowed_param=['command', 'media_id'],
        **upload_kwargs
    )(command='FINALIZE', **kwargs)


def pack_media(filename, form_field):
    media_type = mimetypes.guess_type(filename)
    if not media_type:
        raise Exception("Couldn't guess file type")
    media_type = media_type[0]

    fp = open(filename, 'rb')
    BOUNDARY = 'Tw3ePy'
    body = []
    body.append('--' + BOUNDARY)
    body.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (form_field, filename))
    body.append('Content-Type: %s' % media_type)
    body.append('')
    body.append(fp.read())
    body.append('--' + BOUNDARY + '--')
    body.append('')
    fp.close()
    body = '\r\n'.join(body)

    # build headers
    headers = {
        'Content-Type': 'multipart/form-data; boundary=Tw3ePy',
        'Content-Length': str(len(body))
    }

    return media_type, headers, body
