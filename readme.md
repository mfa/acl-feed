## ACL Anthology People Feed

[![Run Tests](https://github.com/mfa/acl-feed/actions/workflows/tests.yml/badge.svg)](https://github.com/mfa/acl-feed/actions/workflows/tests.yml)
[![Fly Deploy](https://github.com/mfa/acl-feed/actions/workflows/deploy.yml/badge.svg)](https://github.com/mfa/acl-feed/actions/workflows/deploy.yml)


### about

Return an Atom feed for people on https://aclanthology.org until there is an official feed[^1].

deployed version: https://acl-feed.madflex.de/

[^1] https://github.com/acl-org/acl-anthology/issues/358

### development

```
python -m pip install -r requirements.txt
FLASK_APP=app.main flask run
```


### deployment on fly.io

(needs flyctl cmdline tool)

```
flyctl deploy
```


### run tests

```
python -m pytest
```
