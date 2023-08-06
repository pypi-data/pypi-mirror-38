#!/usr/bin/env python
"""find travis repos with `mdfind`"""
import mac_travis


def _cli():
    paths = mac_travis.mdfind()
    if paths:
        print("\n".join(paths))


if __name__ == "__main__":
    _cli()
