import httpx
from flask import Flask, Response, abort, redirect, render_template, request, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

from .generate import generate_feed
from .parse import parse_html

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route("/<person>.atom")
async def person_feed(person):
    url = f"https://www.aclweb.org/anthology/people/{person[0]}/{person}/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code == 200:
        feed = generate_feed(parse_html(response.text, person))
        return Response(feed, mimetype="text/xml")
    abort(404)


@app.route("/", methods=["POST", "GET"])
async def home():
    message = None
    if request.method == "POST":
        if len(request.form.get("url", "")) > 0:
            url = request.form["url"]
            url = url.strip()
            if url.startswith(
                (
                    "https://www.aclweb.org/anthology/people/",
                    "https://www.aclanthology.org/people/",
                )
            ):
                if url[-1] == "/":
                    url = url[:-1]
                person = url.split("/")[-1]
                return redirect(url_for("person_feed", person=person))
            message = request.form["url"] + " is not valid."

    return render_template("home.html", message=message)
