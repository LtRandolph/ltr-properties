import json
import inspect

class Serializer():
    def decode(jsonStr, module=None, postLoadMethod="postLoad"):
        decoder = json.JSONDecoder(
            object_hook=lambda jsonObject: Serializer.__decodeObjectHook(jsonObject, module, postLoadMethod)
            )
        return decoder.decode(jsonStr)

    def encode(obj, indent=None):
        encoder = Serializer.__Encoder(indent=indent)
        return encoder.encode(obj)
    
    def load(filename, module, postLoadMethod="postLoad"):
        with open(filename, 'r') as loadFile:
            return Serializer.decode(loadFile.read(), module, postLoadMethod)

    def save(filename, obj, indent=None):
        with open(filename, 'w') as saveFile:
            saveFile.write(Serializer.encode(obj, indent))

    class __Encoder(json.JSONEncoder):
        def default(self, o):
            if hasattr(o, "__slots__"):
                contents = {}
                for key in o.__slots__:
                    if not key.startswith("_"):
                        contents[key] = getattr(o, key)
                return { type(o).__name__ : contents }

    def __decodeObjectHook(jsonObject, module, postLoadMethod):
        if len(jsonObject) == 1 and module:
            className = next(iter(jsonObject.keys()))
            checkedModules = []
            classType = Serializer.__getClassType(className, module, checkedModules)
            if classType:
                classObj = classType()
                for k, v in jsonObject[className].items():
                    setattr(classObj, k, v)
                if hasattr(classObj, postLoadMethod):
                    getattr(classObj, postLoadMethod)()
                return classObj
        
        return jsonObject

    def __getClassType(className, module, checkedModules):
        # See if we find the class in this namespace.
        if hasattr(module, className):
            maybeClassType = getattr(module, className)
            if inspect.isclass(maybeClassType):
                return maybeClassType

        # Otherwise, recurse into any modules we find.
        for k, v in module.__dict__.items():
            if inspect.ismodule(v) and not k.startswith("_") and not k in checkedModules:
                checkedModules.append(k)
                maybeClassType = Serializer.__getClassType(className, v, checkedModules)
                if maybeClassType:
                    return maybeClassType

        # No dice.
        return None