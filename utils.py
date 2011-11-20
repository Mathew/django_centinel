from django.core import get_callable


class NoCallableMatch(Exception):
    silent_variable_failure = True


def get_view(view_name):
    """ Retrieve a view by string """
    try:
        view = get_callable(view_name, True)
    except (ImportError, AttributeError), e:
        raise NoCallableMatch("Cannot Import {0} because {1}".format(view_name, e))

    return view
