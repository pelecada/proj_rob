def DirImportFn():
    import sys
    sys.path.append("/bluebot/data/Pyrocon/")
    sys.path.append(sys.path[0].replace("proj_rob","pyrocon"))
    sys.path.append(sys.path[0].replace("proj_rob","robtoolbox"))

    