#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""generate README.md"""
import os
import sys
import imp
import inspect
import pydoc
import public
import setupcfg


def _help(obj):
    return pydoc.plain(pydoc.render_doc(obj))


def _getdoc(obj):
    doc = obj.__doc__ if obj.__doc__ else ""
    for l in filter(None, doc.strip().splitlines()):
        return l
    return ""


def _functions(module):
    for name, member in inspect.getmembers(module):
        if inspect.isroutine(member):
            yield member


def _classses(module):
    for name, member in inspect.getmembers(module):
        if inspect.isclass(member):
            yield member


def _methods(cls):
    for name, member in inspect.getmembers(cls):
        if inspect.isfunction(member) or inspect.ismethod(member):
            yield member


def _attrs(cls):
    for name, member in inspect.getmembers(cls):
        if not inspect.isroutine(member) and not isinstance(member, property):
            yield (name, member)


def _properties(cls):
    for name, member in inspect.getmembers(cls):
        if isinstance(member, property):
            yield (name, member)


def _has_header(body):
    return body.lstrip()[0] == "#"


HEADERS = dict(
    badges="",
    description="",
    how="How it works",
    cli="CLI",
    generator=""
)


def _active_sections(self):
    result = []
    for name in self.order:
        if name not in self.disabled:
            result.append(name)
    return result


def _get_sections(self):
    result = []
    for name in _active_sections(self):
        if hasattr(self, name):
            body = getattr(self, name)
            if body and str(body):
                result.append([name, str(body)])
    return result


def _table(columns, rows):
    """generate markdown table (one line rows only)"""
    if rows:
        return """%s
-|-
%s""" % ("|".join(columns), "\n".join(map(lambda r: "|".join(r), rows)))


@public.add
class Readme:
    """README.md generator"""
    __readme__ = ["order", "header_lvl"] + ["__init__", "save", "load", "table", "render"]
    order = ["badges", "description", "install", "features", "requirements", "index", "how", "config", "classes", "functions", "cli", "examples", "todo", "links", "generator"]
    disabled = []
    headers = None
    header_lvl = 4
    generator = """<p align="center"><a href="https://pypi.org/project/readme-md/">readme-md</a> - README.md generator</p>"""

    def __init__(self, path=None, **kwargs):
        self.load(path)
        self.update(**kwargs)
        self.headers = HEADERS

    def update(self, *args, **kwargs):
        inputdict = dict(*args, **kwargs)
        for k, v in inputdict.items():
            setattr(self, k, v)

    def header(self, section):
        header = self.headers.get(section, section.title())
        if not header:  # without header
            return ""
        if "#" in header:  # custom headering level
            return header
        return "%s %s" % ("#" * self.header_lvl, header)  # default headering level

    def render(self):
        """render to string"""
        sections = []
        for name, body in _get_sections(self):
            # todo: clean
            if not _has_header(body):  # without header
                if body.splitlines()[0].strip() != "":
                    header = self.header(name)
                body = "%s\n%s" % (header, str(body).lstrip())
            sections.append(str(body).lstrip().rstrip())
        return "\n\n".join(filter(None, sections))

    def save(self, path):
        """save to file"""
        output = self.render()
        if os.path.dirname(path) and not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        open(path, "w").write(output)

    def load(self, path="."):
        """load sections from .md files (filename as section name)"""
        """
path/<section_name>.md
path/<section_name2>.md
        """
        if not path:
            path = os.getcwd()
        for f in map(lambda l: os.path.join(path, l), os.listdir(path)):
            name = os.path.splitext(os.path.basename(f))[0]
            if name[0] != "." and os.path.isfile(f) and len(f) > 3 and f[-3:] == ".md":
                setattr(self, name, open(f).read())

    @property
    def name(self):
        if os.path.exists("setup.cfg"):
            return setupcfg.get("metadata", "name")

    @name.setter
    def name(self, string):
        self._name = string

    @property
    def pip_install(self):
        if os.path.exists("setup.cfg"):
            return """```bash
$ [sudo] pip install %s
```""" % self.name

    @property
    def install(self):
        """Install section"""
        if hasattr(self, "_install"):
            return getattr(self, "_install", None)
        if os.path.exists("setup.py"):
            return self.pip_install

    @install.setter
    def install(self, string):
        self._install = string

    @property
    def cli(self):
        """CLI section"""
        if hasattr(self, "_cli") or not os.path.exists("setup.py"):
            return getattr(self, "_cli", None)
        return "\n\n".join(filter(None, [self.py_cli, self.scripts_cli]))

    @property
    def py_cli(self):
        modules = []
        for f in self.py_files:
            for l in open(f).read().splitlines():
                if "__name__" in l and "__main__" in l:
                    modules.append(self._import(f))
        rows = []
        for module in sorted(set(modules), key=lambda m: m.__name__):
            USAGE = getattr(module, "USAGE", "python -m %s" % module.__name__)
            rows.append(("`%s`" % USAGE, _getdoc(module)))
        return _table(("usage", "description"), rows)

    @property
    def scripts_cli(self):
        usages = []
        scripts = setupcfg.get("options", "scripts", [])
        for path in filter(lambda f: os.path.basename(f)[0] != ".", scripts):
            code = open(path).read()
            if "#!" in code:
                shebang = code.splitlines()[0].replace("#!", "")
                out = os.popen("%s %s --help 2>&1" % (shebang, path)).read()
                usage = out.rstrip() if out else "usage: %s" % os.path.basename(path)
                usages.append("""```bash
%s
```""" % usage)
        if usages:
            return "\n\n".join(usages)

    @cli.setter
    def cli(self, string):
        self._cli = string

    def class_attrs(self, cls):
        rows = []
        for key, value in sorted(_attrs(cls), key=lambda kv: "__" in kv[0]):
            if key in getattr(cls, '__readme__', []):
                value = value if value != "" else "''"
                rows.append(("`%s`" % key, "`%s`" % value))
        return _table(("attr", "default value"), rows)

    def class_properties(self, cls):
        rows = []
        for name, prop in sorted(_properties(cls), key=lambda kv: "__" in kv[0]):
            if name in getattr(cls, '__readme__', []):
                rows.append(("`%s`" % name, _getdoc(prop)))
        return _table(("@property", "description"), rows)

    def class_methods(self, cls):
        rows = []
        for method in sorted(_methods(cls), key=lambda cls: "__" in cls.__name__):
            if method.__name__ in getattr(cls, '__readme__', []):
                spec = _help(method).splitlines()[2]
                spec = spec.replace("self, ", "").replace("(self)", "()")
                rows.append(("`%s`" % spec, _getdoc(method)))
        return _table(("method", "description"), rows)

    @property
    def classes(self):
        """Classes section"""
        if hasattr(self, "_classes") or not os.path.exists("setup.py"):
            return getattr(self, "_classes", None)
        modules = list(map(self._import, self.py_files))
        lines = []
        for module in sorted(modules, key=lambda m: m.__name__):
            for cls in _classses(module):
                if cls.__name__ in getattr(module, "__all__", []):
                    fullname = "%s.%s" % (module.__name__, cls.__name__)
                    header = "###### `%s`" % fullname
                    doc = _getdoc(cls)
                    attrs = self.class_attrs(cls)
                    methods = self.class_methods(cls)
                    props = self.class_properties(cls)
                    lines += list(filter(None, [header, doc, attrs, methods, props]))
        if lines:
            return "\n\n".join([self.header("Classes")] + lines)

    @classes.setter
    def classes(self, string):
        self._classes = string

    @property
    def py_files(self):
        if not os.path.exists("setup.py"):
            return
        py_modules = setupcfg.get("options", "py_modules", [])
        packages = setupcfg.get("options", "packages", [])
        py_files = list(map(lambda name: "%s.py" % name, py_modules))
        for package in packages:
            path = package.replace(".", "/")
            py = filter(lambda f: os.path.splitext(f)[1] == ".py", os.listdir(path))
            py_files += map(lambda l: os.path.join(path, l), py)
        return list(py_files)

    def _import(self, path):
        name = path.replace(os.getcwd() + os.sep, "").replace(os.sep + "__init__.py", "").replace("/", ".").replace(".py", "")
        return imp.load_source(name, path)

    @property
    def functions(self):
        """Functions section"""
        if hasattr(self, "_functions") or not os.path.exists("setup.py"):
            return getattr(self, "_functions", None)
        modules = list(map(self._import, self.py_files))
        rows = []
        for module in sorted(modules, key=lambda m: m.__name__):
            for func in _functions(module):
                if func.__name__ in getattr(module, "__all__", []):
                    doc = _getdoc(func)
                    spec = _help(func).splitlines()[2]
                    fullname = "%s.%s" % (module.__name__, spec)
                    rows.append(("`%s`" % fullname, doc))
        return _table(("function", "description"), rows)

    @functions.setter
    def functions(self, string):
        self._functions = string


USAGE = 'python -m readme_md [path ...]'


def _cli():
    paths = sys.argv[1:]
    readme = Readme()
    for path in paths:
        readme.load(path)
    print(readme.render())


if __name__ == '__main__':
    if sys.argv[-1] == "--help":
        print(USAGE)
        sys.exit(0)
    _cli()
