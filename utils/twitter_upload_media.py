from __future__ import unicode_literals

import os

import mimetypes
from tweepy.binder import bind_api


def upload_media(api, filename):
    media_type, headers, post_data = pack_media(filename, 'media')
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
    BOUNDARY = b'Tw3ePy'
    body = []
    body.append(b'--' + BOUNDARY)
    body.append(b'Content-Disposition: form-data; name="{}"; filename="{}"'.format(
        form_field.encode('utf-8'), filename.encode('utf-8')))
    body.append(b'Content-Type: {}'.format(media_type.encode('utf-8')))
    body.append(b'')
    body.append(fp.read())
    body.append(b'--' + BOUNDARY + b'--')
    body.append(b'')
    fp.close()
    body = b'\r\n'.join(body)

    # build headers
    headers = {
        'Content-Type': 'multipart/form-data; boundary=Tw3ePy',
        'Content-Length': str(len(body))
    }

    return media_type, headers, body
