# aioexponent

If you have problems with the code in this repository, please file an issue or a pull-request. Thanks!

## Installation

```
pip install aioexponent
```

## Usage

Use to send push notifications to Exponent Experiences from a Python server.

[Full documentation](https://docs.expo.io/versions/latest/guides/push-notifications.html#http2-api) on the API is available if you want to dive into the details.

Here's an example on how to use this with retries and reporting via [pyrollbar](https://github.com/rollbar/pyrollbar).
```python
from aioexponent import DeviceNotRegisteredError
from aioexponent import PushClient
from aioexponent import PushMessage
from aioexponent import PushResponseError
from aioexponent import PushServerError
from aiohttp import ClientError


# Basic arguments. You should extend this function with the push features you
# want to use, or simply pass in a `PushMessage` object.
async def send_push_message(tokens, message, extra=None):
    client = PushClient()
    try:
        response = await client.publish_multiple([
            PushMessage(to=token,
                        body=message,
                        data=extra) for token in tokens])
    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        rollbar.report_exc_info(
            extra_data={
                'tokens': tokens, 'message': message, 'extra': extra
                'errors': exc.errors,
                'response_data': exc.response_data,
            })
        raise
    except (ClientError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        rollbar.report_exc_info(
            extra_data={'tokens': tokens, 'message': message, 'extra': extra})
        raise retry(exc=exc)

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()
    except DeviceNotRegisteredError:
        # Mark the push token as inactive
        from notifications.models import PushToken
        PushToken.objects.filter(token=token).update(active=False)
    except PushResponseError as exc:
        # Encountered some other per-notification error.
        rollbar.report_exc_info(
            extra_data={
                'tokens': tokens,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
            })
        raise retry(exc=exc)
```
