Err plugin for Zendesk
===

Requirements
---
```
pip install requests
```

Installation
---
```
!repos install https://github.com/sijis/err-zendesk.git
```

Configuration
---
Using your normal credentials
```
!config Zendesk {'api_pass': 'your-password', 'api_url': 'https://your-domain.zendesk.com/api/v2', 'api_user': 'email@domain', 'domain': 'https://your-domain.zendesk.com'}
```

Using an API token
```
!config Zendesk {'api_pass': 'token-key', 'api_url': 'https://your-domain.zendesk.com/api/v2', 'api_user': 'email@domain/token', 'domain': 'https://your-domain.zendesk.com'}
```

Usage
---
Simple example usage

```
!zendesk 1234
```
