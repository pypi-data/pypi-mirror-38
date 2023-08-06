# *****************************************************************************
#   Copyright 2017 Karl Einar Nelson
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# *****************************************************************************

from __future__ import absolute_import

# Optional jpype module to support:
#   import <java_pkg> [ as <name> ]
#   import <java_pkg>.<java_class> [ as <name> ]
#   from <java_pkg> import <java_class>[,<java_class>*]
#   from <java_pkg> import <java_class> [ as <name> ]
#   from <java_pkg>.<java_class> import <java_static> [ as <name> ]
#   from <java_pkg>.<java_class> import <java_inner> [ as <name> ]
#
#   jpype.imports.registerDomain(moduleName, alias=<java_pkg>)
#   jpype.imports.registerImportCustomizer(JImportCustomizer)
#
# Requires Python 3.6 or later
# Usage:
#   import jpype
#   import jpype.imports
#   <start or attach jvm>
#   # Import java packages as modules
#   from java.lang import String

import sys     as _sys
import types   as _types
import keyword as _keyword
try:
    from importlib.machinery import ModuleSpec as _ModuleSpec
except Exception:  # pragma: no cover # <AK> added
    # For Python2 compatiblity (Note: customizers are not supported)
    class _ModuleSpec(object):
        def __init__(self, name, loader):
            self.name   = name
            self.loader = loader

from ..jtypes._jpackage_jpype import JavaPackage
from ._jvm import isJVMStarted as _isJVMStarted

__all__ = ('registerDomain', 'registerImportCustomizer', 'JImportCustomizer')

_export_types = ()


# %% Domains

_JDOMAINS = {}

def registerDomain(mod, alias=None):
    """ Add a java domain to python as a dynamic module.

    Args:
        mod is the name of the dynamic module
        alias is the name of the java path. (optional)
    """
    _JDOMAINS[mod] = alias or mod

# Preregister common top level domains
registerDomain("com")
registerDomain("gov")
registerDomain("java")
registerDomain("org")


# %% Customizer

_CUSTOMIZERS = []

if _sys.version_info.major >= 3:

    def registerImportCustomizer(customizer):
        """ Import customizers can be used to import python packages
        into java modules automatically.
        """
        _CUSTOMIZERS.append(customizer)

    # Support hook for placing other things into the java tree

    class JImportCustomizer(object):

        """
        Base class for Import customizer.

        Import customizers should implement canCustomize and getSpec.

        Example:
          | # Site packages for each java package are stored under $DEVEL/<java_pkg>/py
          | class SiteCustomizer(jpype.imports.JImportCustomizer):
          |     def canCustomize(self, name):
          |         if name.startswith('org.mysite') and name.endswith('.py'):
          |             return True
          |         return False
          |     def getSpec(self, name):
          |         pname = name[:-3]
          |         devel = os.environ.get('DEVEL')
          |         path = os.path.join(devel, pname,'py','__init__.py')
          |         return importlib.util.spec_from_file_location(name, path)
        """

        def canCustomize(self, name):
            """ Determine if this path is to be treated differently

            Return:
                True if an alternative spec is required.
            """
            return False

        def getSpec(self, name):
            """ Get the module spec for this module."""
            raise NotImplementedError
else:

    def registerImportCustomizer(customizer):
        raise NotImplementedError("Import customizers not implemented for Python 2.x")

    JImportCustomizer = object


# %% Import

# In order to get properties to be attached to the JavaPackage class,
# we must create a dynamic class between

def _JImportFactory(spec, javaname):

    """
    (internal) Factory for creating java modules dynamically.

    This is needed to create a new type node to hold static methods.
    """

    def get_all(self):
        global _export_types
        exports  = [name for name, attr in self.__dict__.items()
                  if not name.startswith("_") and isinstance(attr, _export_types)]
        exports += [name for name, attr in self.__class__.__dict__.items()
                  if not name.startswith("_") and isinstance(attr, _export_types)]
        return exports

    # Set up a new class for this type
    members = {
        "__init__":     lambda self, name: JavaPackage.__init__(self, name),
        "__javaname__": javaname,
        "__name__":     spec.name,
        "__all__":      property(get_all),
        "__spec__":     spec,
    }

    # Is this module also a class, if so insert class info
    from ..jvm            import EJavaModifiers
    from ..jtypes._jclass import JavaClass
    from ..jtypes._jvm    import JVM
    try:
        jvm = JVM.jvm
    except:
        import warnings
        warnings.warn("JVM not started yet, can not inspect JavaPackage contents")
        return None
    try:
        jclass = jvm.JClass(javaname)
    except Exception:
        pass
    else:
        # Mark this as a class (will cause children to be inner classes)
        members["__javaclass__"] = jclass

        # Exposed static members as part of the module

        # Copy properties
        jmetaclass = jclass.__class__
        for member_name in dir(jmetaclass):
            if not member_name.startswith("_"):  # Skip private members
                # Copy properties
                attr = getattr(jmetaclass, member_name)
                if isinstance(attr, property):
                    members[member_name] = attr

        # Copy static methods
        for jmethod in jclass.__javaclass__.getMethods():
            if EJavaModifiers.STATIC in jmethod.getModifiers():
                method_name = jmethod.getName()
                member_name = JavaClass._JavaClass__make_member_name(method_name)
                members[member_name] = getattr(jclass, member_name)

    return type("module." + spec.name, (JavaPackage,), members)


# %% Finder

class _JImportLoader(object):

    """ (internal) Finder hook for importlib. """

    def find_spec(self, name, path, target):

        parts = name.split(".", 1)
        if not parts[0] in _JDOMAINS:
            return None

        # Support for external modules in java tree
        for customizer in _CUSTOMIZERS:
            if customizer.canCustomize(name):
                return customizer.getSpec(name)
        else:
            # Import the java module
            return _ModuleSpec(name, self)

    def create_module(self, spec):

        """ (internal) Loader hook for importlib. """

        if not _isJVMStarted():
            raise ImportError("Attempt to create java modules without jvm")

        # Handle creating the java name based on the path
        parts = spec.name.split(".")

        if len(parts) == 1:
            javaname = _JDOMAINS[spec.name]
        else:
            # Use the parent module to simplify name mangling
            parent = _sys.modules[".".join(parts[:-1])]
            name   = parts[-1]

            # Support of inner classes
            if not isinstance(parent, JavaPackage):
                return getattr(parent, name)

            if name.endswith("_") and _keyword.iskeyword(name[:-1]):
                name = name[:-1]

            javaname = object.__getattribute__(parent, "__javaname__")
            try:
                object.__getattribute__(parent, "__javaclass__")
            except AttributeError:
                javaname += "."
            else:
                javaname += "$"
            javaname += name

        module_class = _JImportFactory(spec, javaname)
        module = module_class(spec.name)
        return module

    def exec_module(self, fullname):
        pass

    # For compatablity with Python 2.7
    def find_module(self, name, path=None):

        domain = name.split('.', 1)[0]
        return self if domain in _JDOMAINS else None

    # For compatablity with Python 2.7
    def load_module(self, name):

        _sys.modules[name] = module = self.create_module(_ModuleSpec(name, self))
        return module


# Install hooks into python importlib
_sys.meta_path.append(_JImportLoader())


# %% Initialize

def _initialize(state):

    from ..jtypes._jclass  import JavaClass
    from ..jtypes._jmethod import JavaMethod
    global _export_types
    _export_types = (property, JavaPackage, JavaClass, JavaMethod)

from ..jtypes import _imports
from ..jtypes._jvm import JVM
_imports.unregister()
JVM.register_initializer(_initialize)
del _imports, JVM


# %% Utility

#def _keyword_unwrap(name):
#    return name[:-1] if name.endswith("_") and _keyword.iskeyword(name[:-1]) else name
