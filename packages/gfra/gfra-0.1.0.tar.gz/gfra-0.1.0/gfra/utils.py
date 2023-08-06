def trailing_slash(route_path):
    if not route_path.endswith('/'):
        return route_path + '/'
    return route_path
