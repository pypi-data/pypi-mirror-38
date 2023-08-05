from DocString2Json import DocString2Json


def generate_for(scope):
    json_docs = []
    for function_name, function in scope.items():
        valid_doc_string = function and function.__doc__ and function.__doc__.find("@json") == 0
        if valid_doc_string:
            doc = DocString2Json(function.__doc__)
            json_docs.append(doc)


    return [dict(doc) for doc in json_docs]
