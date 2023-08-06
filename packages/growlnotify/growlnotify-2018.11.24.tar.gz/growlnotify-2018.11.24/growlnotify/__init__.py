#!/usr/bin/env python
# -*- coding: utf-8 -*-
import public
import runcmd


@public.add
def args(**kwargs):
    """return list with `growlnotify` cli arguments"""
    args = []
    for k, v in kwargs.items():
        short = len(k) == 1
        string = "-%s" % k if short else "--%s" % k
        if v is True:
            """flag, e.g.: -s, --sticky"""
            args += [string]
        else:
            """ -t "title text", --title "title text """
            args += [string, str(v)]
    return args


@public.add
def notify(**kwargs):
    """run growlnotify"""
    if "m" not in kwargs and "message" not in kwargs:
        kwargs["m"] = ""
    cmd = ["growlnotify"] + args(**kwargs)
    runcmd.run(cmd)._raise()
