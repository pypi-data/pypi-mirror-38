def args_to_string(args,kwargs):
    return '({},{})'.format(str(args),str(kwargs))


class debug(object):

    def __init__(self,output=print):
        self.output = output    


    def __call__(self,func):
        
        def wrapper(*args,**kwargs):
            self.output(args_to_string(args,kwargs))
            result = func(*args,**kwargs)
            return result

        return wrapper
