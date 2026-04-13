"""Instagram API headers constants."""


class Headers:
    """Instagram API header names."""

    SET_AUTHORIZATION = "ig-set-authorization"
    SET_WWW_CLAIM = "x-ig-set-www-claim"


class AuthPrefix:
    """Authorization token prefixes."""

    BEARER_IGT2 = "Bearer IGT:2:"


class RequestHeaders:
    """Request header names for Instagram API."""

    # User Agent
    USER_AGENT = "User-Agent"

    # Instagram headers
    X_IG_APP_ID = "X-Ig-App-Id"
    X_IG_CAPABILITIES = "X-Ig-Capabilities"
    X_IG_CONNECTION_TYPE = "X-Ig-Connection-Type"
    X_IG_DEVICE_ID = "X-Ig-Device-Id"
    X_IG_ANDROID_ID = "X-Ig-Android-Id"
    X_IG_TIMEZONE_OFFSET = "X-Ig-Timezone-Offset"
    X_IG_VALIDATE_NULL = "X-IG-VALIDATE-NULL-IN-LEGACY-DICT"
    X_IG_BANDWIDTH_SPEED = "X-IG-Bandwidth-Speed-KBPS"
    X_IG_BANDWIDTH_BYTES = "X-IG-Bandwidth-TotalBytes-B"
    X_IG_BANDWIDTH_TIME = "X-IG-Bandwidth-TotalTime-MS"
    X_IG_WWW_CLAIM = "X-Ig-Www-Claim"
    X_IG_CONNECTION_SPEED = "X-IG-Connection-Speed"

    # Locale headers
    X_IG_APP_LOCALE = "X-Ig-App-Locale"
    X_IG_DEVICE_LOCALE = "X-Ig-Device-Locale"
    X_IG_MAPPED_LOCALE = "X-Ig-Mapped-Locale"

    # Pigeon headers
    X_PIGEON_RAWCLIENTTIME = "X-Pigeon-Rawclienttime"
    X_PIGEON_SESSION_ID = "X-Pigeon-Session-Id"

    # Facebook headers
    X_FB_HTTP_ENGINE = "X-Fb-Http-Engine"
    X_FB_CLIENT_IP = "X-Fb-Client-Ip"
    X_FB_SERVER_CLUSTER = "X-Fb-Server-Cluster"

    # Standard headers
    ACCEPT_LANGUAGE = "Accept-Language"
    ACCEPT_ENCODING = "Accept-Encoding"
    AUTHORIZATION = "Authorization"
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"

    # Upload headers (rupload)
    X_INSTAGRAM_RUPLOAD_PARAMS = "X-Instagram-Rupload-Params"
    X_ENTITY_TYPE = "X-Entity-Type"
    X_ENTITY_NAME = "X-Entity-Name"
    X_ENTITY_LENGTH = "X-Entity-Length"
    OFFSET = "Offset"
