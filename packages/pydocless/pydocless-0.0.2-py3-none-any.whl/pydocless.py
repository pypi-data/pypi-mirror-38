import importlib
import re
import inspect


def rep(name, item):
    if inspect.isfunction(item):
        title = '**%s**%s' % (item.__name__, str(inspect.signature(item)))
        doc = inspect.getdoc(item)
    elif inspect.isclass(item):
        title = '## ' + item.__name__
        doc = inspect.getdoc(item)
    else:
        title = ' = '.join((name, str(item)))
        doc = None

    return title + '\n\n' + doc.replace('\n', '\n\n') if doc is not None else title


def recurse(name, value, prefix=''):
    items = []
    if hasattr(value, '__dict__'):
        for name, item in value.__dict__.items():
            if hasattr(item, '__module__') and item.__module__ is not None:
                name = '.'.join((item.__module__, item.__qualname__ if hasattr(item, '__qualname__') else name))
            include = any([i.match(name) is not None for i in includes])
            exclude = any([e.match(name) is not None for e in excludes])

            if include and not exclude:
                items.append(rep(name, item) + '\n')
                elements = recurse(name, item, prefix + '#')
                if elements:
                    items.extend(elements)
    else:
        items.append(rep(name, value))

    return items


def pydocless(config):
    global includes
    global excludes
    module = importlib.import_module(config['module'])
    includes, excludes = [], []
    if 'includes' in config:
        includes = [re.compile(i) for i in config['includes']]
    if 'excludes' in config:
        excludes = [re.compile(e) for e in config['excludes']]
    lines = recurse(module.__name__, module)
    seen = set()
    lines = [x for x in lines if not (x.strip() in seen or seen.add(x.strip()))]
    lines.insert(0, '# ' + module.__name__)

    return '\n'.join(lines)
