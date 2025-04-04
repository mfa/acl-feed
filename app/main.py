import httpx
from flask import (
    Flask,
    Response,
    abort,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from werkzeug.middleware.proxy_fix import ProxyFix

from .generate import generate_feed_atom, generate_feed_rss
from .parse import parse_html

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


@app.route("/robots.txt")
async def robots():
    response = make_response("User-Agent: *\nDisallow: /\n", 200)
    response.mimetype = "text/plain"
    return response


@app.route("/<person>.atom")
async def person_feed_atom(person):
    url = f"https://aclanthology.org/people/{person[0]}/{person}/"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
        if response.status_code == 200:
            feed = generate_feed_atom(parse_html(response.text, person))
            return Response(feed, mimetype="text/xml")
    abort(404)


@app.route("/<person>.rss")
async def person_feed_rss(person):
    url = f"https://aclanthology.org/people/{person[0]}/{person}/"
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
        if response.status_code == 200:
            feed = generate_feed_rss(parse_html(response.text, person))
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
                    "https://aclanthology.org/people/",
                )
            ):
                if url[-1] == "/":
                    url = url[:-1]
                person = url.split("/")[-1]
                return redirect(url_for("person_feed_atom", person=person))
            message = request.form["url"] + " is not valid."

    return render_template("home.html", message=message)
