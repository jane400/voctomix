import os

def with_ui_path(filename: str):
    import __main__
    if not hasattr(__main__, '__file__'):
        raise Exception("Can't find the voctogui root dir (__main__ doesn't have a __file__ attr)")

    main_path = os.path.realpath(__main__.__file__)
    ui_dir_path = os.path.join(os.path.dirname(main_path), 'ui')

    path = os.path.join(ui_dir_path, filename)
    if not os.path.isfile(path):
        raise Exception(f"Can't find this .ui-file: {path}")

    return path