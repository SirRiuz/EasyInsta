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
| `login` | POST | `/api/v1/accounts/login/` | Login with username and password |
| `check_token` | GET | `/api/v1/accounts/current_user/` | Validate token |
| `get_token_from_cookies` | GET | `/api/v1/accounts/current_user/` | Extract token from cookies |

### Users

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `check_username` | POST | `/api/v1/users/check_username/` | Check if username exists |
| `check_email` | POST | `/api/v1/users/check_email/` | Check if email is registered |
| `search_user` | GET | `/api/v1/users/search/` | Search users by query |

### Profiles

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `get_user_profile_info_by_id` | GET | `/api/v1/users/{user_id}/info/` | Get profile by user ID |
| `get_user_profile_info_by_name` | GET | `/api/v1/users/{username}/usernameinfo/` | Get profile by username |
| `get_user_profile_info_web` | GET | `/api/v1/users/web_profile_info/` | Get web profile info |
| `get_user_sso_info` | POST | `/api/v1/web/fxcal/ig_sso_users/` | Get SSO information |
| `get_user_block_list` | GET | `/api/v1/users/blocked_list/` | Get blocked users list |

### Friendships

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `follow_user` | POST | `/api/v1/friendships/create/{user_id}/` | Follow a user |
| `unfollow_user` | POST | `/api/v1/friendships/destroy/{user_id}/` | Unfollow a user |
| `add_close_friend` | POST | `/api/v1/friendships/set_besties/` | Add user to close friends |
| `remove_close_friend` | POST | `/api/v1/friendships/set_besties/` | Remove user from close friends |
| `block_user` | POST | `/api/v1/friendships/block/{user_id}/` | Block a user |
| `unblock_user` | POST | `/api/v1/friendships/unblock/{user_id}/` | Unblock a user |

### Content

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `get_user_feed` | GET | `/api/v1/feed/user/{user_id}/` | Get user's feed posts |
| `get_user_story_by_user_id` | GET | `/api/v1/feed/user/{user_id}/story/` | Get user's stories |
| `get_user_highlights_tray` | GET | `/api/v1/highlights/{user_id}/highlights_tray/` | Get highlights tray |
| `get_user_highlights_tray_list_by_id` | GET | `/api/v1/feed/reels_media/` | Get highlights by ID |

### Direct Messages

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `get_unread_messages` | GET | `/api/v1/direct_v2/inbox/` | Get inbox with unread filter |

## Placeholders

All sensitive data in the payloads has been replaced with placeholders:

| Placeholder | Description |
|-------------|-------------|
| `{your_token}` | Authorization token |
| `{user_id}` | Target user ID |
| `{username}` | Target username |
| `{email}` | Email address |
| `{password}` | User password |
| `{timestamp}` | Unix timestamp |
| `{device_id}` | Device identifier |
| `{guid}` | GUID |
| `{sessionid}` | Session ID cookie |
| `{ds_user_id}` | User ID cookie |
| `{ig_did}` | Instagram device ID cookie |
| `{mid}` | Machine ID cookie |
| `{highlight_id}` | Highlight ID |
| `{query}` | Search query |

## Common Headers

| Header | Value | Description |
|--------|-------|-------------|
| `Host` | `i.instagram.com` | Instagram API host |
| `User-Agent` | `Instagram 275.0.0.27.98 Android (...)` | Mobile app user agent |
| `X-Ig-App-Id` | `936619743392459` | Instagram app ID |
| `X-Ig-Capabilities` | `3brTvwE=` | App capabilities |
| `X-Ig-Connection-Type` | `WIFI` | Connection type |
| `Authorization` | `Bearer IGT:2:{your_token}` | Auth token (when required) |
| `Content-Type` | `application/x-www-form-urlencoded` | For POST requests |

## Notes

- All endpoints use `i.instagram.com` as the host
- The User-Agent mimics the Instagram Android app
- Authorization header format: `Bearer IGT:2:{token}`
- Some endpoints work without authentication (check_username, check_email)
