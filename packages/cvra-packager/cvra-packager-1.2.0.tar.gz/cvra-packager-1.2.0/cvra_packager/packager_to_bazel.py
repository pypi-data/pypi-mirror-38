#!/usr/bin/env python3
"""
Converts a package.yml to Bazel's BUILD format.

Of course additional steps might be required
"""
import argparse
import jinja2
import yaml

BAZEL_LIBRARY_TEMPLATE = """
cc_library(
    name = "{{ name }}",
    srcs = [{% for p in srcs %}
        "{{ p }}",
        {%- endfor %}
    ],
    hdrs = glob(['*.h']),
    visibility = ["//visibility:public"],
)

cc_test(
    name = "{{ name }}-test",
    srcs = [{% for p in tests %}
        "{{ p }}",
        {%- endfor %}
    ],
    deps = [':{{ name }}'],
)
"""


def package_to_build(package, package_name):
    template = jinja2.Template(BAZEL_LIBRARY_TEMPLATE)
    tests = package.get('tests', [])
    srcs = package.get('source', [])
    return template.render(name=package_name, srcs=srcs, tests=tests)


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=argparse.FileType(), help='Input package file')
    parser.add_argument("output", type=argparse.FileType('w'), help='Output BUILD file')

    return parser.parse_args()


def main():
    args = parse_args()
    package = yaml.load(args.input.read())


if __name__ == '__main__':
    main()
