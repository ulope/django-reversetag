from django.conf import settings
from django.template import Context, Library, Node, NodeList, Template, Variable
from django.utils.encoding import smart_str, smart_unicode

register = Library()

def _merge(view, args, kwargs):
    """Merge arguments with PartialResolveNode's"""
    # If view is a PartialResolveNode update arguments with its args and kwargs
    if isinstance(view, PartialResolveNode):
        args_ = view.args[:]
        args_.extend(args)
        args = args_
        kwargs_ = view.kwargs.copy()
        kwargs_.update(kwargs)
        kwargs = kwargs_
        # the "real" view is inside the PartialResolveNode's view attribute
        view = view.view
    return view, args, kwargs



class ResolveNode(Node):
    """Represents a to-be-resolved url"""
    def __init__(self, view, args, kwargs, asvar):
        self.view = view
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar
    
    def render(self, context):
        view = self.view.resolve(context)
        args = self.args
        kwargs = self.kwargs

        args = [arg.resolve(context) for arg in args]
        kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                       for k, v in kwargs.items()])

        view, args, kwargs = _merge(view, args, kwargs)

        from django.core.urlresolvers import reverse, NoReverseMatch
        # Try to look up the URL twice: once given the view name, and again
        # relative to what we guess is the "main" app. If they both fail, 
        # re-raise the NoReverseMatch unless we're using the 
        # {% resolve ... as var %} construct in which cause return nothing.
        url = ''
        try:
            url = reverse(view, args=args, kwargs=kwargs)
        except NoReverseMatch, exc:
            project_name = settings.SETTINGS_MODULE.split('.')[0]
            try:
                url = reverse(project_name + '.' + view,
                              args=args, kwargs=kwargs)
            except NoReverseMatch:
                if self.asvar is None:
                    # reraise the original NoReverseMatch since the above is 
                    # just a (failed, if we reach here) attempt to fix things.
                    raise exc
                    
        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            return url


class PartialResolveNode(Node):
    """Represents a partial to-be-resolved url"""
    def __init__(self, view, args, kwargs, asvar):
        # Store in "private" attributes so we can re-resolve variables in loops
        self._view = view
        self._args = args
        self._kwargs = kwargs

        self.asvar = asvar

    def render(self, context):
        self.view = self._view.resolve(context)
        self.args = [arg.resolve(context) for arg in self._args]
        self.kwargs = dict([(smart_str(k,'ascii'), v.resolve(context))
                            for k, v in self._kwargs.items()])

        self.view, self.args, self.kwargs = _merge(self.view, self.args, self.kwargs)
        
        if self.asvar:
            context[self.asvar] = self
            return ''
        else:
            raise TemplateSyntaxError("When using 'partial' '%s' requires"
                                      " (as varname) argument" % bits[0])

    def __unicode__(self):
        # don't output partialy resolved urls
        if settings.TEMPLATE_DEBUG:
            return "[Cannot render partialy resolved url for view: %s " \
                   "with args %s and kwargs %s. You have to use it through " \
                   "the 'resolve' tag.]" % (self.view, self.args, self.kwargs)
        else:
            return '' # fail silently

@register.tag
def resolve(parser, token):
    """
    Returns an absolute URL matching given view with its parameters.

    This is a way to define links that aren't tied to a particular URL
    configuration::

        {% resolve "path.to.some_view" "arg1","arg2" [as varname] %}
    or:
        {% resolve "path.to.some_view" name1="value1" [as varname] %}

    The first argument is a path to a view or a view name. It can be an 
    absolute python path or just ``app_name.view_name`` without the project 
    name if the view is located inside the project.  Other arguments are 
    comma-separated values that will be filled in place of positional and 
    keyword arguments in the URL. All arguments for the URL must be present 
    unless you use the ``partial`` form of ``resolve`` which is described 
    below.
    If you'd like to store the url in a ``context`` variable instead of 
    directly displaying it you can use the optional ``as varname`` argument.

    For example if you have a view ``app_name.client`` taking client's id and
    the corresponding line in a URLconf looks like this::

        ('^client/(\d+)/$', 'app_name.client')

    and this app's URLconf is included into the project's URLconf under some
    path::

        ('^clients/', include('project_name.app_name.urls'))

    then in a template you can create a link for a certain client like this::

        {% resolve "app_name.client" client.id %}

    The URL will look like ``/clients/client/123/``.
    
    
    Advanced usage
    ~~~~~~~~~~~~~~
    
    The ``resolve`` tag also supports a more advanced mode of operation
    called "partial resolving". This allows you to resolve an URL in two or 
    more stages. Each time only specifying some of required view arguments
    until the URL is resolved.
    Syntax:
    
        {% resolve partial "path.to.some_view" "arg1" key1="value1" as varname %}
    
    TODO: add more doc and usage examples
    
    Note: When using the partial keyword the ``as varname`` clause is required
          since a partially resolved URL can not be output directly but only 
          be used as the ``view`` argument to another invocation of 
          ``resolve``. 
    """
    bits = token.contents.split(' ')
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument"
                                  " (path to a view)" % bits[0])
    partial = False
    args = []
    kwargs = {}
    asvar = None

    argstart = 2
    if bits[1] == "partial":
        partial = True
        view = parser.compile_filter(bits[2])
        argstart = 3
    else:
        view = parser.compile_filter(bits[1])

    if len(bits) > 2:
        bits = iter(bits[argstart:])
        for bit in bits:
            if bit == 'as':
                asvar = bits.next()
                break
            else:
                for arg in bit.split(","):
                    if '=' in arg:
                        k, v = arg.split('=', 1)
                        k = k.strip()
                        kwargs[k] = parser.compile_filter(v)
                    elif arg:
                        args.append(parser.compile_filter(arg))
        if partial and asvar is None:
            raise TemplateSyntaxError("When using 'partial' '%s' requires"
                                      " (as varname) argument" % bits[0])
    if partial:
        return PartialResolveNode(view, args, kwargs, asvar)
    return ResolveNode(view, args, kwargs, asvar)

