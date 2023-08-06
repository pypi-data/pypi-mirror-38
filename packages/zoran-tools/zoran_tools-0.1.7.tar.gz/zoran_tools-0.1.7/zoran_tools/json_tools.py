import re
import json

def jsonp2json(jsonp_text, format='str'):
    """
    将Jsonp格式以Json格式解析出来
    :param jsonp_text: 要解析的Jsonp文本
    :param format: 要解析为的格式, 可以是str或dict
    :return:
    """
    text_wihtout_new_line = re.sub('\s', '', jsonp_text)
    jsn = re.findall('.*\(({.*})\)[;]{0,1}', text_wihtout_new_line)[0]
    jsn_dict = json.loads(jsn)
    if format == 'dict':
        return jsn_dict
    elif format == 'str':
        return json.dumps(jsn_dict, indent=2, ensure_ascii=False)
    else:
        raise ValueError
