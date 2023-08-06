import os
import json
import yaml
import importlib
from slugify import slugify
from feedgen.feed import FeedGenerator

from eorg.parser import parse
from eorg.generate import html

from elcato.helpers import images, files, webfinger, minify

from elcato.data import BlogData, AuthorData, fill
from elcato import settings


def build_feed(destination, Blog, Author, items):
    fg = FeedGenerator()
    fg.id(Blog.domain)
    fg.title(Blog.title)
    fg.author({"name": Author.name, "email": Author.email})
    fg.logo(Blog.domain + Blog.image)
    fg.subtitle(Blog.description)
    fg.link(href=Blog.domain + "/rss.xml", rel="self")
    fg.language("en")

    for item in items:
        fe = fg.add_entry()
        fe.id(Blog.domain + "/posts/" + item.slug.strip() + ".html")
        fe.title(item.title)
        fe.category(
            [{"term": i, "scheme": i, "label": i} for i in item.filetags]
        )
        fe.pubDate(item.date)
        fe.link(href=Blog.domain + "/posts/" + item.slug.strip() + ".html")

    fg.rss_file(f"{destination}/rss.xml")


def build_tag_indexes(template, destination, tag, pages, Author):
    with open(f"{destination}/tags/{tag}.html", "wb") as f:
        f.write(
            template.viewIndex(
                title=f"{tag}",
                search=tag,
                path="../",
                cards=pages,
                author=Author,
            )
        )

    search = {}
    for page in pages:
        search[page.title.strip()] = page.slug.strip()

    with open(f"{destination}/tags/{tag}.js", "w") as f:
        f.write("var searchData = ")
        json.dump(search, f)
        minify(f"{destination}/tags/{tag}.js")


def build_tag_page(template, destination, tags, Author):
    with open(f"{destination}/tags/all.html", "wb") as f:
        f.write(
            template.viewTags(
                title=f"Tags", path="../", tags=tags, author=Author
            )
        )


def build_activitypub(destination, author):
    webfinger(destination, author)


def skip_rules(doc):
    if "draft" in doc.filetags:
        print(f"## Skipped file in draft mode.")
        return True

    if getattr(doc, "filetags") is None:
        print(
            f"## Skipped without file tags add #+FILETAGS: to the document head."
        )
        return True

    if getattr(doc, "date", None) is None:
        print(f"## Skipped no date add #+DATE: to the document head.")
        return True

    return False


def load_template(config):
    return importlib.import_module(
        f"elcato.templates.{config.get('theme', 'enaml')}.template"
    )


def build(source, destination, config):
    template = load_template(config.get("Config"))
    pages = []
    tags = {}
    search = {"all": {}}
    source = os.path.abspath(source)
    destination = os.path.abspath(destination)
    if config:
        Blog = fill(BlogData, config["Blog"])
        Author = fill(AuthorData, config["Author"])
    pos = 0
    for filename in files(source):
        filepath = os.path.abspath(os.path.dirname(filename))
        print(f"#### Processing {filename}")
        with open(filename, "r") as fp:
            doc = parse(fp)
            slug = getattr(doc, "slug", slugify(doc.title)).strip()
            filetags = getattr(doc, "filetags", "")
            taglist = [tag.strip() for tag in filetags.split(":")]
            doc.filetags = taglist
            doc.slug = slug
            images(source, filepath, destination, doc)

            with open(f"{destination}/posts/{slug.strip()}.html", "wb") as f:
                f.write(
                    template.viewPage(
                        title=doc.title,
                        path="../",
                        doc=doc,
                        body=html(doc).read(),
                    )
                )

            if skip_rules(doc) is False:
                search["all"][doc.title.strip()] = slug
                pages.append(doc)
                for tag in doc.filetags:
                    tags.setdefault(tag, []).append(pos)
                pos += 1

    with open(f"{destination}/index.html", "wb") as f:
        f.write(
            template.viewIndex(
                title="Index",
                search="search",
                path="./",
                cards=pages,
                author=Author,
            )
        )

    with open(f"{destination}/tags/search.js", "w") as f:
        f.write("var searchData = ")
        json.dump(search["all"], f)

    build_tag_page(template, destination, tags, Author)
    for (tag, tag_pages) in tags.items():
        build_tag_indexes(
            template, destination, tag, [pages[p] for p in tag_pages], Author
        )
    build_activitypub(destination, Author)
    build_feed(destination, Blog, Author, pages)


if __name__ == "__main__":
    source_path = settings.ROOT
    destination_path = settings.PATH

    config_path = os.path.abspath("./") + os.sep + "elcato.yaml"
    if os.path.exists(config_path):
        with open(config_path, "r") as fp:
            config = yaml.load(fp)
        source_path = config.org_file_path
    print(f"Reading org files from {source_path}")
    print(f"Generting files to {destination_path}")

    # init(settings.PATH)
    build(source=source_path, destination=destination_path, config=None)
# build(settings.ROOT, settings.PATH)
