# EasyInsta

Unofficial async Instagram Private API for Python

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Fast and effective Instagram Private API wrapper using `aiohttp`. Uses the most recent version of the API from Instagram, obtained using reverse-engineering with Charles Proxy.

**Instagram API valid for April 2025** (last reverse-engineering check)

Support **Python >= 3.11**

## Features

- Login by token (sessionid + ds_user_id encoded)
- Getting public data of user profiles (by username or user ID)
- Getting inbox conversations and unread messages
- Check username and email availability
- Full async/await support
- 100% test coverage

## Installation

```bash
pip install easyinsta
```

## Basic Usage

```python
from easyinsta import Instagram

ig = Instagram()
ig.auth.with_token("your_token")

profile = await ig.profiles.get(username="zuck")
print(profile.username)  # 'zuck'
```

## Check Username Availability

```python
from easyinsta import Instagram

ig = Instagram()

# No authentication required
is_taken = await ig.validators.check_username("zuck")
print(is_taken)  # True
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

- [Getting Started](#installation)
- [Basic Usage](#basic-usage)

### Modules

- [Auth](#auth) - Authentication handler (token login, logout)
- [Profiles](#profiles) - User profile data (by username or ID)
- [Validators](#validators) - Check username/email availability
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

# Login with token
ig.auth.with_token("your_token")

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

## Validators

```python
# No authentication required

# Check username
is_taken = await ig.validators.check_username("zuck")

# Check email
is_registered = await ig.validators.check_email("test@example.com")
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
# Install dev dependencies
pip install -r requirements-dev.txt

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
