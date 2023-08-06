from collections import namedtuple

def fill(nt, values):
    return nt(*[values.get(field.lower(), field + ' - not set') for field in nt._fields])

TagData = namedtuple("Tag", ["name", "count"])
BlogData = namedtuple("Blog", ["title", "domain", "image", "description"])
AuthorData = namedtuple("Author", ["name", "email", "photo", "blurb", "links"])

template = """
#+TITLE: ElCato Static Blogging Platform
#+DATE: {now}
#+DESCRIPTION:
#+FILETAGS: colon:split:tags
#+LATEX_CLASS: article
#+CATEGORY: cato
#+SLUG: slugified-title"""
