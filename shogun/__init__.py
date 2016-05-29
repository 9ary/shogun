from glob import glob
import sys, os
from jinja2 import Environment, PackageLoader

cd = os.path.abspath(os.path.curdir)
srcdir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(srcdir)

jinja = Environment(loader = PackageLoader(__name__, "templates"))
jinja.globals["builddir"] = "$builddir"
jinja.globals["srcdir"] = "$srcdir"

def subext(f, ext):
    return os.path.splitext(f)[0] + "." + ext
jinja.filters["subext"] = subext

def prepath(f, pre):
    return os.path.join(pre, f)
jinja.filters["prepath"] = prepath

template_obj = jinja.get_template("objects.ninja")
template_asm = jinja.get_template("assembly.ninja")
template_vars = jinja.get_template("variables.ninja")

class Objects:
    def __init__(self, pathname, rule, extout, *, recursive = False):
        self.files = glob(pathname, recursive = recursive)
        self.pathname = pathname
        self.extout = extout
        self.rule = rule

    def objs(self):
        for f in self.files:
            yield subext(f, self.extout)

    def targets(self):
        return template_obj.render(objects = self.files,
                pathname = self.pathname, rule = self.rule, extout = self.extout)

class Assembly:
    def __init__(self, path, rule, *objects, options = {}):
        self.path = path
        self.rule = rule
        self.objects = objects
        self.options = options

    def objs(self):
        return [self.path]

    def targets(self):
        def objs():
            for o in self.objects:
                for ob in o.objs():
                    yield ob

        return template_asm.render(objects = objs(),
                path = self.path, rule = self.rule, variables = self.options)

class Variables:
    def __init__(self, *, comment = None, **variables):
        self.variables = variables
        self.comment = comment

    def targets(self):
        return template_vars.render(variables = self.variables, comment = self.comment)

def build(*targets, out = "targets.ninja", builddir = None):
    out = os.path.join(srcdir, out)
    if builddir is None:
        if cd == srcdir:
            builddir = os.path.join(srcdir, "build")
        else:
            builddir = cd

    locations = Variables(comment = "Asset and output locations",
        srcdir = srcdir, builddir = builddir)

    with open(out, "w") as fd:
        for t in (locations,) + targets:
            fd.write(t.targets())
            fd.write("\n")

