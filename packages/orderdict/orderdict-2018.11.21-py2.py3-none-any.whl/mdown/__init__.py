#!/usr/bin/env python
# -*- coding: utf-8 -*-
import public


@public.add
def header(title, lvl=3):
    if not lvl:
        lvl = "3"
    number = "#" * lvl
    return "%s %s" % (number, title.rstrip().title())


@public.add
def image(url, title="", alt=""):
    if not alt:
        alt = ""
    if not title:
        title = ""
    kwargs = dict(url=url, title=title, alt=alt)
    return '![{alt}]({url} "{title}")'.format(**kwargs)


@public.add
def code(code, language=None):
    if not language:
        language = ""
    kwargs = dict(code=code.lstrip().rstrip(), language=language)
    return """```{language}
{code}
```""".format(**kwargs)


@public.add
def link():
    raise NotImplementedError


@public.add
def lists(items, ordered=False):
    raise NotImplementedError


@public.add
def blockquote(text):
    raise NotImplementedError
