from pyjade import (ext, compiler, convert, exceptions,
            filters, lexer, nodes, parser, runtime, utils)
from pyjade import (ext.django, ext.pyramid, ext.tornado, 
            ext.html, ext.jinja, ext.mako, ext.underscore)
from pyjade import (ext.django.compiler, ext.django.loader,
            ext.django.templatetags)

from pyjade.parser import Parser
from pyjade.compiler import Compiler
from pyjade.utils import process
from pyjade.filters import register_filter
from pyjade.ext import html

simple_convert = lambda t: html.process_jade(t)