#!/usr/bin/env python
"""set Finder tags (`red` - failed, `none` - passed)"""
import mac_travis


def _cli():
    mac_travis.tag()


if __name__ == "__main__":
    _cli()
