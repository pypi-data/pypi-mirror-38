"""tween_factory.py

Contains the tween factory for printing 500 stack traces.
"""
import traceback

from pyramid import response


class IlluminatiAndStuffTweenFactory:
    """This tween prints out your 500 stack traces to the body of the
    response.
    """

    def __init__(self, handler, registry):
        """Initializes the tween factory."""
        self.handler = handler
        self.registry = registry

    def __call__(self, request):
        """This prints out the 500 response stack trace to the body of
        the response if needed.
        """
        try:
            return self.handler(request)
        except Exception:
            tb = traceback.format_exc()
            resp = response.Response(
                status_int=500,
                body=f'<pre>{tb}</pre>',
            )
            print(tb)
            return resp
