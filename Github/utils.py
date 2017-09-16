def get_session_info(session_doc):
    if type(session_doc) is str:
        info_string = findbetween(session_doc, "<!--", "-->")
        if info_string is not None:
            infos = info_string.split('\n')
            info = {}
            for i in infos:
                i = i.split(":")
                if i.__len__() == 2:
                   info[i[0]] = i[1]
            return info
        return
    return

def findbetween(str, start, end):
    try:
        return (str.split(start))[1].split(end)[0]
    except:
        return None