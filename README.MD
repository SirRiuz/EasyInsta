# EasyInsta

Unofficial async Instagram Private API for Python

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Fast and effective Instagram Private API wrapper using `aiohttp`. Uses the most recent version of the API from Instagram, obtained using reverse-engineering with Charles Proxy.

**Instagram API valid for April 2025** (last reverse-engineering check)

Support **Python >= 3.11**

## Features

- Login with username and password
- Login by token (sessionid + ds_user_id encoded)
- Getting public data of user profiles (by username or user ID)
- Follow and unfollow users
- Add and remove users from close friends list
- Block and unblock users
- Getting inbox conversations and unread messages
- Check if account exists by username or email
- Full async/await support
- 100% test coverage

## Basic Usage

```python
from easyinsta import Instagram

ig = Instagram()
await ig.auth.login("your_username", "your_password")

profile = await ig.profiles.get(username="zuck")
print(profile.username)  # 'zuck'
```

## Check if Account Exists

```python
from easyinsta import Instagram

ig = Instagram()

# No authentication required
exists = await ig.profiles.exists_by_username("zuck")
print(exists)  # True

exists = await ig.profiles.exists_by_email("test@example.com")
print(exists)  # True or False
```

## Get Unread Conversations

```python
from easyinsta import Instagram
from easyinsta.constants import ThreadStatus

ig = Instagram()
ig.auth.with_token("your_token")

inbox = await ig.direct.get_inbox(page=1)

for thread in inbox.threads:
    status = thread.get_status("your_user_id")

    if status == ThreadStatus.NEW:
        print(f"🟢 {thread.name}")
    elif status == ThreadStatus.UNREAD_MARKED:
        print(f"🟡 {thread.name}")
```

## Documentation

### Index

- [Basic Usage](#basic-usage)

### Modules

- [Auth](#auth) - Authentication handler (token login, logout)
- [Profiles](#profiles) - User profile data, follow/unfollow, account existence checks
- [Direct](#direct) - Inbox conversations and messages

### Models

- **Profile** - Full user profile data (username, bio, followers, following, etc.)
- **ProfileLight** - Short public user data (id, username, profile pic)
- **Inbox** - Inbox with list of threads and pagination
- **Thread** - Conversation thread (participants, last activity, read status)
- **ThreadStatus** - Read status enum (`NEW`, `UNREAD_MARKED`, `READ`)

### Exceptions

- **ApiError** - Base API error with status code
- **AuthRequiredError** - Authentication needed
- **ProfileNotFoundError** - Profile doesn't exist
- **RateLimitError** - Too many requests

---

## Auth

```python
ig = Instagram()

# Login with username and password
await ig.auth.login("your_username", "your_password")

# Login with token (manual authentication)
ig.auth.with_token("your_token")

# Login with cookies (sessionid and ds_user_id)
ig.auth.with_cookies(
    sessionid="YOUR_SESSION_ID",
    ds_user_id="YOUR_USER_ID"
)

# Check if authenticated
ig.auth.is_authenticated  # True

# Logout
ig.auth.logout()
```

## Profiles

```python
# Get by username (requires auth)
profile = await ig.profiles.get(username="zuck")

# Get by user ID (requires auth)
profile = await ig.profiles.get(profile_id="314216")

# Get public profile (no auth)
profile = await ig.profiles.get_public("314216")

# Get user ID from username (requires auth)
user_id = await ig.profiles.user_id_from_username("zuck")  # 314216

# Get username from user ID (requires auth)
username = await ig.profiles.username_from_user_id("314216")  # 'zuck'

# Follow a user (requires auth)
await ig.profiles.follow("314216")

# Unfollow a user (requires auth)
await ig.profiles.unfollow("314216")

# Add to close friends (requires auth)
await ig.profiles.add_to_close_friends("314216")

# Remove from close friends (requires auth)
await ig.profiles.remove_from_close_friends("314216")

# Block a user (requires auth)
await ig.profiles.block("314216")

# Unblock a user (requires auth)
await ig.profiles.unblock("314216")

# Check if account exists by username (no auth)
exists = await ig.profiles.exists_by_username("zuck")  # True

# Check if account exists by email (no auth)
exists = await ig.profiles.exists_by_email("test@example.com")  # True or False

# Access profile data
profile.id              # '314216'
profile.username        # 'zuck'
profile.full_name       # 'Mark Zuckerberg'
profile.biography       # Bio text
profile.follower_count  # 123456789
profile.following_count # 500
profile.is_verified     # True
profile.is_private      # False
```

## Direct

```python
from easyinsta.constants import ThreadStatus

# Get inbox (page 1 = first 20 conversations)
inbox = await ig.direct.get_inbox(page=1)

# Iterate threads
for thread in inbox.threads:
    print(thread.name)      # Display name
    print(thread.username)  # @username

    # Check read status for your user
    status = thread.get_status("your_user_id")

    if status == ThreadStatus.NEW:
        print("New message")
    elif status == ThreadStatus.UNREAD_MARKED:
        print("Marked as unread")
    elif status == ThreadStatus.READ:
        print("Already read")

# Pagination
if inbox.has_older:
    page2 = await ig.direct.get_inbox(page=2)
```

---

## Development

```bash
# Run tests
make test

# Run tests with coverage
make test-cov
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feat/feature-name`)
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Disclaimer

This library is for educational purposes only. Use at your own risk. Make sure to comply with Instagram's Terms of Service.
