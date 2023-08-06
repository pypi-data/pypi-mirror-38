#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import public


@public.add
def seconds():
    """afk time in seconds"""
    os.environ["LC_ALL"] = "C"
    out = os.popen("ioreg -c IOHIDSystem | perl -ane 'if (/Idle/) {$idle=(pop @F)/1000000000; print $idle,\"\n\"; last}'").read()
    return int(float(out.strip()))


@public.add
def minutes():
    """afk time in minutes"""
    return seconds() % 60


@public.add
def hours():
    """afk time in hours"""
    return minutes() % 60


@public.add
def days():
    """afk time in days"""
    return hours() % 24
