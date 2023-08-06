from ipaddress import ip_address

from command_handler.request.validator.exceptions import AssertionFailedException


def privateIp(request):
    try:
        assert ip_address(request.remote_addr).is_private, "Remote address is not private"
        if "X-Forwarded-For" in request.headers:
            assert ip_address(request.headers["X-Forwarded-For"]).is_private, "X-Forwarded-For IP is not private"
    except AssertionError as e:
        raise AssertionFailedException(str(e), 403) from e
    except ValueError as e:
        raise AssertionFailedException("X-Forwarded-For does not contain IP address") from e
