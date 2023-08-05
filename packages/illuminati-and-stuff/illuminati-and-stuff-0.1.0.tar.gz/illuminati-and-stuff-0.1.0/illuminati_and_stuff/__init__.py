"""__init__.py"""


def includeme(config):
    """This will get called when you call
    ``config.include(illuminati_and_stuff)``
    """
    config.add_tween(
        'illuminati_and_stuff.tween_factory.IlluminatiAndStuffTweenFactory',
    )
