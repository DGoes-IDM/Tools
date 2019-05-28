# TODO: make consistent with convertTBtoTBHIV versions


def delete_key(needles, haystack, deletions=0, performed_deletions=0):
    if not isinstance(needles, type([])):
        needles = [needles]

    if isinstance(haystack, type(dict())):
        for needle in needles:
            if needle in haystack.keys():
                if performed_deletions < deletions:
                    del haystack[needle]
                    performed_deletions += 1
            elif len(haystack.keys()) > 0:
                for key in haystack.keys():
                    performed_deletions = delete_key(needle, haystack[key], deletions, performed_deletions)
    elif isinstance(haystack, type([])):
        for node in haystack:
            performed_deletions = delete_key(needles, node, deletions, performed_deletions)
    return performed_deletions


def find_key(needles, haystack):
    found = {}
    if not isinstance(needles, type([])):
        needles = [needles]

    if isinstance(haystack, type(dict())):
        for needle in needles:
            if needle in haystack.keys():
                found[needle] = haystack[needle]
            elif len(haystack.keys()) > 0:
                for key in haystack.keys():
                    result = find_key(needle, haystack[key])
                    if result:
                        for k, v in result.items():
                            found[k] = v
    elif isinstance(haystack, type([])):
        for node in haystack:
            result = find_key(needles, node)
            if result:
                for k, v in result.items():
                    found[k] = v
    return found


def find_key_context(needle, haystack, ignore_first=0):
    found = {}
    if isinstance(haystack, type(dict())):
        if needle in haystack.keys():
            if ignore_first == 0:
                return haystack, ignore_first
            else:
                ignore_first -= 1
        elif len(haystack.keys()) > 0:
            for key in haystack.keys():
                result, ignore_first = find_key_context(needle, haystack[key], ignore_first)
                if result:
                    return result, ignore_first
    elif isinstance(haystack, type([])):
        for node in haystack:
            result, ignore_first = find_key_context(needle, node, ignore_first)
            if result:
                return result, ignore_first
    return found, ignore_first


def find_value_context(needles, haystack):
    found = {}
    if not isinstance(needles, type([])):
        needles = [needles]

    if isinstance(haystack, type(dict())):
        for needle in needles:
            if needle in haystack.values():
                return haystack
            elif len(haystack.keys()) > 0:
                for key in haystack.keys():
                    result = find_value_context(needle, haystack[key])
                    if result:
                        return result
    elif isinstance(haystack, type([])):
        for node in haystack:
            result = find_value_context(needles, node)
            if result:
                return result
    return found
