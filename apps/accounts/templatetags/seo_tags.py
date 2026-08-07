"""Tag `capture` — rend un bloc dans une variable de contexte plutôt que
directement dans la sortie.

Sert uniquement à réutiliser le contenu (possiblement surchargé par une page
enfant) des blocks `title` et `meta_description` de templates/base.html à
plusieurs endroits (title, meta description, Open Graph, Twitter card) sans
dupliquer le texte par défaut et sans déclencher l'erreur Django "'block' tag
with name 'X' appears more than once" (un nom de bloc ne peut apparaître
qu'une seule fois par template).
"""
from django import template

register = template.Library()


class CaptureNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = self.nodelist.render(context)
        context[self.varname] = output
        return ""


@register.tag(name="capture")
def do_capture(parser, token):
    try:
        _tag_name, _as, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "Usage: {% capture as varname %}...{% endcapture %}"
        )
    nodelist = parser.parse(("endcapture",))
    parser.delete_first_token()
    return CaptureNode(nodelist, varname)
