import json


def read_json(name):
    with open(name,'r', encoding='utf-8') as f:
        b = json.loads(f.read())
        return b

# 根据字段名读取json对应的字段值
def find_values( json_repr, id):
    results = []
    def _decode_dict(a_dict):
        try:
            results.append(a_dict[id])
        except KeyError:
            pass
        return a_dict

    json_repr = json_repr.lstrip('"')
    json_repr = json_repr.rstrip('"')
    print("请求报文" + json_repr)
    json.loads(json_repr, object_hook=_decode_dict)
    return results

# 更新json串中的字段值
def set_json_value(json_repr, **items):
    results = dict()

    def _find_key(dic):
        nonlocal results
        for key in items:
            if key in dic:
                dic[key] = items[key]
        results = dic
        return dic

    json_repr = json.dumps(json_repr)
    json.loads(json_repr, object_hook=_find_key)
    return results