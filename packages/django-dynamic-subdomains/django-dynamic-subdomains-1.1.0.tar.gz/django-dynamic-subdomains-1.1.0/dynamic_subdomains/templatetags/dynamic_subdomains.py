from django import template
from django.template import TemplateSyntaxError
from django.utils.encoding import smart_str
from django.template.defaulttags import kwarg_re

from ..reverse import reverse_crossdomain
from ..app_settings import app_settings

register = template.Library()

@register.tag
def domain_url(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least 1 argument" % bits[0])

    view = parser.compile_filter(bits[1])
    bits = bits[1:] # Strip off view

    try:
        pivot = bits.index('on')
    except ValueError:
        # No "on <subdomain>" was specified so use the default domain
        domain = app_settings.DEFAULT_SUBDOMAIN
        view_args, view_kwargs = parse_args_kwargs(parser, bits[1:])
        domain_args, domain_kwargs = (), {}
    else:
        try:
            domain = bits[pivot + 1]
        except IndexError:
            raise TemplateSyntaxError(
                "'%s' arguments must include a domain after 'on'" % bits[0]
            )

        view_args, view_kwargs = parse_args_kwargs(parser, bits[1:pivot])
        domain_args, domain_kwargs = parse_args_kwargs(parser, bits[pivot + 2:])

    return DomainURLNode(
        domain,
        view,
        domain_args,
        domain_kwargs,
        view_args,
        view_kwargs,
    )

class DomainURLNode(template.Node):
    def __init__(self, subdomain, view, subdomain_args, subdomain_kwargs, view_args, view_kwargs):
        self.subdomain = subdomain
        self.view = view

        self.subdomain_args = subdomain_args
        self.subdomain_kwargs = subdomain_kwargs

        self.view_args = view_args
        self.view_kwargs = view_kwargs

    def render(self, context):
        subdomain_args = [x.resolve(context) for x in self.subdomain_args]
        subdomain_kwargs = {
            smart_str(k, 'ascii'): v.resolve(context)
            for k, v in self.subdomain_kwargs.items()
        }

        view_args = [x.resolve(context) for x in self.view_args]
        view_kwargs = {
            smart_str(k, 'ascii'): v.resolve(context)
            for k, v in self.view_kwargs.items()
        }

        return reverse_crossdomain(
            self.subdomain,
            self.view.resolve(context),
            subdomain_args,
            subdomain_kwargs,
            view_args,
            view_kwargs,
        )

def parse_args_kwargs(parser, bits):
    args = []
    kwargs = {}

    for bit in bits:
        match = kwarg_re.match(bit)
        if not match:
            raise TemplateSyntaxError("Malformed arguments to domain_url tag")

        name, value = match.groups()
        if name:
            kwargs[name] = parser.compile_filter(value)
        else:
            args.append(parser.compile_filter(value))

    return args, kwargs
