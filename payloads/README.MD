# Payloads

This directory contains raw HTTP request payloads for each Instagram API endpoint used by the library. These files serve as documentation and reference for the API requests.

## Structure

Each file contains the complete HTTP request including:
- HTTP method and endpoint
- Headers (Host, User-Agent, Authorization, etc.)
- Request body (if applicable)

## Endpoints

### Authentication

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `auth_user` | POST | `/api/v1/accounts/login/` | User login |
| `check_token` | GET | `/api/v1/accounts/current_user/` | Validate token |
| `get_token_from_cookies` | - | - | Extract token from cookies |

### Users

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `check_username` | POST | `/api/v1/users/check_username/` | Check if username exists |
| `check_email` | POST | `/api/v1/users/check_email/` | Check if email is registered |
| `search_user` | GET | `/api/v1/users/search/` | Search users by query |

### Profiles

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `get_user_profile_info_by_id` | GET | `/api/v1/users/{id}/info/` | Get profile by user ID |
| `get_user_profile_info_by_name` | GET | `/api/v1/users/{username}/usernameinfo/` | Get profile by username |
| `get_user_profile_info_web` | GET | `/api/v1/users/web_profile_info/` | Get web profile info |
| `get_user_sso_info` | GET | `/api/v1/users/{id}/sso_info/` | Get SSO information |
| `get_user_block_list` | GET | `/api/v1/users/blocked_list/` | Get blocked users list |

### Content

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `get_user_feed` | GET | `/api/v1/feed/user/{id}/` | Get user's feed posts |
| `get_user_story_by_user_id` | GET | `/api/v1/feed/user/{id}/story/` | Get user's stories |
| `get_user_highlights_tray` | GET | `/api/v1/highlights/tray/` | Get highlights tray |
| `get_user_highlights_tray_list_by_id` | GET | `/api/v1/highlights/{id}/highlights_tray/` | Get highlights by ID |

### Direct Messages

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `obtener_mensajes_no_leodos_o_marcados` | GET | `/api/v1/direct_v2/inbox/` | Get inbox with unread filter |

## Examples

### Check Username (No Auth Required)

```http
POST /api/v1/users/check_username/ HTTP/2
Host: i.instagram.com
User-Agent: Instagram 275.0.0.27.98 Android (26/8.0.0; 480dpi; 1080x1920; OnePlus; ONEPLUS A3003; OnePlus3; qcom; en_US; 458229237)
X-Ig-App-Id: 936619743392459
Content-Type: application/x-www-form-urlencoded

username=zuck
```

### Get Profile by ID (Auth Required)

```http
GET /api/v1/users/314216/info/ HTTP/2
Host: i.instagram.com
User-Agent: Instagram 275.0.0.27.98 Android (...)
Authorization: Bearer IGT:2:<token>
X-Ig-App-Id: 936619743392459
```

### Get Inbox (Auth Required)

```http
GET /api/v1/direct_v2/inbox/?visual_message_return_type=unseen&selected_filter=unread&limit=20 HTTP/2
Host: i.instagram.com
User-Agent: Instagram 275.0.0.27.98 Android (...)
Authorization: Bearer IGT:2:<token>
X-Ig-App-Id: 936619743392459
```

#### Pagination

To get the next page, add the `cursor` parameter:

```http
GET /api/v1/direct_v2/inbox/?visual_message_return_type=unseen&selected_filter=unread&limit=20&cursor=<oldest_cursor> HTTP/2
```

## Common Headers

| Header | Value | Description |
|--------|-------|-------------|
| `Host` | `i.instagram.com` | Instagram API host |
| `User-Agent` | `Instagram 275.0.0.27.98 Android (...)` | Mobile app user agent |
| `X-Ig-App-Id` | `936619743392459` | Instagram app ID |
| `X-Ig-Capabilities` | `3brTvwE=` | App capabilities |
| `X-Ig-Connection-Type` | `WIFI` | Connection type |
| `Authorization` | `Bearer IGT:2:<token>` | Auth token (when required) |
| `Content-Type` | `application/x-www-form-urlencoded` | For POST requests |

## Notes

- All endpoints use `i.instagram.com` as the host
- The User-Agent mimics the Instagram Android app
- Authorization header format: `Bearer IGT:2:<base64_token>`
- Some endpoints work without authentication (check_username, check_email)
