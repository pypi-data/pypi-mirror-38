#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cli_args
import public
import runcmd


@public.add
def notify(**kwargs):
    """run growlnotify. keys as arguments"""
    if "m" not in kwargs and "message" not in kwargs:
        kwargs["m"] = ""
    args = cli_args.make(long=True, **kwargs)
    cmd = ["growlnotify"] + args
    runcmd.run(cmd)._raise()
