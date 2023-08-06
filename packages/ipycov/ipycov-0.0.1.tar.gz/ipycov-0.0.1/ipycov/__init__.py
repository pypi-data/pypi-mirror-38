from IPython.display import IFrame

from .magic import CoverageMagic


IFRAME_TEMPLATE_SHIM = (
    " " * 12 + "sandbox=\"allow-forms allow-same-origin allow-scripts\"\n"
)


def load_ipython_extension(ipython):
    """ Load the extension in IPython and shim IPython's IFrame. """
    ipython.register_magics(CoverageMagic)

    # Attempt to make IPython IFrames interactive, doesn't seem to work though
    if "sandbox" not in IFrame.iframe:
        IFrame.iframe = IFrame.iframe.replace(
            "allowfullscreen\n",
            "allowfullscreen\n" + IFRAME_TEMPLATE_SHIM,
        )


def unload_ipython_extension(ipython):
    """ Remove IPython's IFrame template shim. """
    # If you want your extension to be unloadable, put that logic here.
    IFrame.iframe.replace(IFRAME_TEMPLATE_SHIM, "")
