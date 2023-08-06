#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ruamel.yaml as yaml
import public
import travis_yml.quoted

KEYS = [
    "language",         # https://docs.travis-ci.com/user/languages/

    # https://docs.travis-ci.com/user/languages/
    # https://docs.travis-ci.com/user/languages/c/
    "compiler",

    # C#, F, Visual Basic
    # https://docs.travis-ci.com/user/languages/csharp/
    "solution",
    "mono",

    # https://docs.travis-ci.com/user/languages/cpp/
    "compiler",

    # https://docs.travis-ci.com/user/languages/clojure/
    "lein",

    # https://docs.travis-ci.com/user/languages/crystal/
    "crystal",

    # https://docs.travis-ci.com/user/languages/d/
    "d",

    # https://docs.travis-ci.com/user/languages/dart/
    "dart",
    "dart_task",
    "dartanalyzer",

    # https://docs.travis-ci.com/user/languages/erlang/
    "otp_release",

    # https://docs.travis-ci.com/user/languages/elixir/
    "elixir",
    "otp_release",

    # https://docs.travis-ci.com/user/languages/go/
    "go",
    "go_import_path",
    "gobuild_args",

    # https://docs.travis-ci.com/user/languages/groovy/
    "jdk",

    # https://docs.travis-ci.com/user/languages/haskell/
    "ghc",

    # https://docs.travis-ci.com/user/languages/haxe/
    "haxe",
    "neko",
    "hxml",

    # https://docs.travis-ci.com/user/languages/java/
    "jdk",

    # https://docs.travis-ci.com/user/languages/javascript-with-nodejs/
    "node_js",

    # https://docs.travis-ci.com/user/languages/julia/
    "julia",

    # https://docs.travis-ci.com/user/languages/nix/

    # Objective-C or Swift
    # https://docs.travis-ci.com/user/languages/objective-c/
    "osx_image",
    "xcode_project",
    "xcode_scheme",
    "xcode_sdk",
    "podfile",

    # https://docs.travis-ci.com/user/languages/perl/
    "perl",

    # https://docs.travis-ci.com/user/languages/perl6/
    "perl6",

    # https://docs.travis-ci.com/user/languages/php/
    "php",

    # https://docs.travis-ci.com/user/languages/python/
    "python",
    "virtualenv",

    # https://docs.travis-ci.com/user/languages/r/
    "r",
    "pandoc_version",
    "repos",
    "r_github_packages",
    "Imports",
    "Remotes",

    # https://docs.travis-ci.com/user/languages/ruby/
    "rvm",
    "gemfile",
    "bundler_args",
    "jdk",

    # https://docs.travis-ci.com/user/languages/rust/
    "rust",

    # https://docs.travis-ci.com/user/languages/scala/
    "scala",
    "sbt_args",

    # https://docs.travis-ci.com/user/languages/smalltalk/
    "smalltalk_vm",
    "smalltalk",

    "os",               # https://docs.travis-ci.com/user/multi-os/
    "sudo",             # https://docs.travis-ci.com/user/reference/trusty/
    "dist",             # https://docs.travis-ci.com/user/reference/trusty/
    "addons",           # https://docs.travis-ci.com/user/addons/
    "cache",            # https://docs.travis-ci.com/user/caching
    "podfile",          # https://docs.travis-ci.com/user/caching#Determining-the-Podfile-path
    "branches",         # https://docs.travis-ci.com/user/customizing-the-build/#Safelisting-or-blocklisting-branches
    "git",              # https://docs.travis-ci.com/user/customizing-the-build/#Git-Clone-Depth
    "env",              # https://docs.travis-ci.com/user/environment-variables/
    "notifications",    # https://docs.travis-ci.com/user/notifications/
    "matrix",           # https://docs.travis-ci.com/user/customizing-the-build/#Build-Matrix
    "services",         # https://docs.travis-ci.com/user/database-setup/#Starting-Services

    "before_install",
    "install",
    "before_script",
    "script"
]


@public.add
class TravisYML:
    __readme__ = ["data", "load", "save"]
    """.travis.yml class based on travis.yml known keys"""

    def __init__(self, path=None, **kwargs):
        if path:
            self.load(path)
        self.update(kwargs)

    def update(self, *args, **kwargs):
        inputdict = dict(*args, **kwargs)
        for k, v in inputdict.items():
            setattr(self, k, v)

    def load(self, path):
        """load from .travis.yml file"""
        with open(path, 'r') as stream:
            data = yaml.load(stream)
            self.update(data)

    def save(self, path=".travis.yml"):
        """save to file"""
        if not path:
            path = ".travis.yml"
        with open(path, 'w') as outfile:
            yaml.dump(self.data, outfile, default_flow_style=True)

    @property
    def data(self):
        """return dictionary with .travis.yml data"""
        result = dict()
        for key in KEYS:
            if hasattr(self, key):
                value = getattr(self, key)
                result[key] = value
        return result

    def __str__(self):
        data = self.data
        if data:
            return yaml.dump(data, Dumper=yaml.RoundTripDumper)
        return ""
