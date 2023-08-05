#!/usr/bin/env python
import decorator
import public
import detect


def _func_factory(check, msg):
    def run(f, *args, **kw):
        if not check():
            raise OSError("%s %s" % (f.__name__, msg))
        return f(*args, **kw)
    return decorator.decorator(run)


linux = _func_factory(lambda: detect.linux, "is Linux only :(")
mac = _func_factory(lambda: detect.mac, "is MacOS only :(")
osx = _func_factory(lambda: detect.osx, "is OSX only :(")
unix = _func_factory(lambda: detect.unix, "is Unix only :(")
windows = _func_factory(lambda: detect.windows, "is Unix only :(")


public.add(linux, mac, osx, unix, windows)
