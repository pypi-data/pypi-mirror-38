# coding: utf-8


def _ipython(local, banner):
    from IPython.terminal.embed import InteractiveShellEmbed
    from IPython.terminal.ipapp import load_default_config

    InteractiveShellEmbed.clear_instance()
    shell = InteractiveShellEmbed.instance(
        banner1=banner,
        user_ns=local,
        config=load_default_config()
    )
    shell()


def _bpython(local, banner):
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    import bpython

    bpython.embed(locals_=local, banner=banner)


def _python(local, banner):
    import code

    try:
        # noinspection PyUnresolvedReferences
        import readline
    except ImportError:
        pass
    else:
        import rlcompleter
        readline.parse_and_bind('tab:complete')

    code.interact(local=local, banner=banner)


def embed(local=None, banner='', shell=None):
    """
    To Interactive Python Console, and embed the current thread.
    Supported: ipython, bpython, python
    :param str shell:
        'ipython', 'bpython', 'python', or their first letter.
        `None`: to the first available Python Console
    :param dict local:
        local env. or `None` for Auto
    :param str banner:
        welcome text
    """

    import inspect

    if local is None:
        local = inspect.currentframe().f_back.f_locals

    if isinstance(shell, str):
        shell = shell.strip().lower()
        if shell.startswith('b'):
            shell = _bpython
        elif shell.startswith('i'):
            shell = _ipython
        elif shell.startswith('p') or not shell:
            shell = _python

    for _shell in shell, _ipython, _bpython, _python:
        try:
            _shell(local=local, banner=banner)
        except (TypeError, ImportError):
            continue
        except KeyboardInterrupt:
            break
        else:
            break
