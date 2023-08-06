import inspect

class TypesValidator(object):
    
    def validator(value=True):
        def _validar(f):
            def wrapper(*args, **kwargs):
                ret = inspect.signature(f).return_annotation
                pos = 0
                for i in inspect.signature(f).parameters.keys():
                    try:
                        if (inspect.signature(f).parameters[i].annotation != type(args[pos])):
                            raise TypeError("El parametro de la posicion{} debe ser del tipo {}".format(pos, inspect.signature(f).parameters[i].annotation))
                        pos = pos +1
                    except IndexError as e:
                        pass
                if (ret == inspect._empty):
                    raise TypeError("La funcion debe retornar al menos un valor None")
            
                r = f(*args, **kwargs)
                if (type(r) == ret or type(r)== type(ret)):
                    return r
                else:
                    raise TypeError("La funcion debe retornar un "+str(ret))
            return wrapper
        return _validar
