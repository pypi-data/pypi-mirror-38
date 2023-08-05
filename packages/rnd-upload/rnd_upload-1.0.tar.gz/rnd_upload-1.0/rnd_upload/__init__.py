try:
    from .post import main
    from .livenviro_util import get_config_filename
except:
    from post import main
    from livenviro_util import get_config_filename

name = get_config_filename()
main(name)
