# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

RE_CAMEL = re.compile(r'([A-Z][^A-Z]*)')


def humanize(text):
    '''Transform code conventions to human readable strings'''
    words = []
    for part in text.split('_'):
        for word in RE_CAMEL.findall(part) or [part]:
            words.append(word.lower())
    words[0] = words[0].title()
    return ' '.join(words)
