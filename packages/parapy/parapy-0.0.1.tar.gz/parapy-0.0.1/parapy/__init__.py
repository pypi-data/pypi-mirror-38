import sys

name = "params"


def params(parameters):
    argv = sys.argv
    posParams = list(filter(lambda x: type(x[1]) == int, parameters))
    namedParams = list(filter(lambda x: x not in posParams, parameters))
    del(argv[0])

    def findBool(x):
        return (x in argv)

    def findElse(x, t):
        if x in argv:
            a = argv.index(x) + 1
            try:
                retval = t(argv[a])
            except ValueError:
                print('\033[91mError:\033[0m parameter %s is not formatted properly. Is (%s) but expected (%s)' %
                      (x, str(type(argv[a])), str(t)))
                retval = None
            return retval
        else:
            return None

    retval = {}
    allowedTypes = [int, float, str]
    for i in namedParams:
        if i[2] == bool:
            i_val = findBool(i[1])
        elif (i[2] in allowedTypes):
            i_val = findElse(i[1], i[2])
        else:
            print('\033[91;1mError:\033[0m parameter %s has an invalid type: (%s)' %
                  (i[0], str(i[2])))
            i_val = None
        if (i[1] in argv):
            argv.remove(i[1])
        if (not (i_val is None)) and not (i[2] is bool):
            argv.remove(str(i_val))
        retval[i[0]] = i_val
    for i in posParams:
        if i[1] < len(argv):
            try:
                retval[i[0]] = i[2](argv[i[1]])
            except ValueError:
                print('\033[91mError:\033[0m parameter %s is not formatted properly. Is (%s) but expected (%s)' %
                      (i[0], str(type(argv[i[1]])), str(i[2])))
                retval[i[0]] = None
        else:
            retval[i[0]] = None
    return retval
