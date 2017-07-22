import jinja2


def render(filename, context={}, error=None, path='templates'):
    if error:
        # Error should be a string
        if isinstance(error, str):
            context['error'] = error
        else:
            raise TypeError('Error message must be a string')
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path)
    ).get_template(filename).render(context)
