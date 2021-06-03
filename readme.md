## acl feed

### about

return an atom feed for every author on https://aclanthology.org until there is an official feed[1].

[1] https://github.com/acl-org/acl-anthology/issues/358


production version: http://acl-feed.fly.dev


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
