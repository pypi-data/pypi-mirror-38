# coding: utf-8
"""
1.验证参数类型
2.带条件的验证
3.有复杂的验证需求，还可以编写一个函数作为验证参数
"""

from base_result import Result

import traceback
import inspect
import re


class ValidateException(Exception):
    pass


def validParam(*varargs, **keywords):
    """验证参数的装饰器。"""
    result = Result()
    varargs = map(_toStardardCondition, varargs)  # map会根据提供的函数对指定序列做映射。
    keywords = dict((k, _toStardardCondition(keywords[k])) for k in keywords)

    def generator(func):       # 形参获取，形参及conditon的对应关系
        # print inspect.getargspec(func)
        # print func.__defaults__
        args, varargname, kwname, defaults = inspect.getargspec(func)[:4]
        # 仅用于方法，获取方法声明的参数，返回元组，分别是(普通参数名的列表, *参数名, **参数名, 默认值元组)。
        # 如果没有值，将是空列表和3个None。如果是2.6以上版本，将返回一个命名元组(Named Tuple)，
        # 即除了索引外还可以使用属性名访问元组中的元素。
        dctValidator = _getcallargs(args, varargname, kwname, varargs, keywords)
        # print dctValidator

        def wrapper(*callvarargs, **callkeywords):      # 实参获取 实参与condition的对应关系
            dctCallArgs = _getcallargs(args, varargname, kwname, callvarargs, callkeywords)
            dictDefaults = _getdefaultargs(args, callvarargs, callkeywords, defaults)
            # print 'dictDefaults', dictDefaults
            k, item, msg, code = None, None, '', None
            try:
                for k in dctValidator:
                    msg, code = None, None
                    if k == varargname:
                        for item in dctCallArgs[k]:
                            assert dctValidator[k](item)
                    elif k == kwname:
                        for item in dctCallArgs[k].values():
                            assert dctValidator[k](item)
                    else:
                        if k in dctCallArgs:
                            item = dctCallArgs[k]
                        elif k in dictDefaults:
                            item = dictDefaults[k]
                        else:
                            continue
                        func_result = dctValidator[k]
                        falg, msg, code = _return_func(dctValidator[k](item))
                        if not falg:
                            raise ValueError()
            except:
                import traceback
                if code:
                    result.code = code
                    result.status = code
                else:
                    result.code = -3000
                    result.status = -3000
                # traceback.print_exc()
                result.flag = False
                result.msg = '%s() parameter validation fails, param: %s, value: %s(%s), msg(%s)' \
                             % (func.func_name, k, item, item.__class__.__name__, str(msg))
                return result
            return func(*callvarargs, **callkeywords)
        wrapper = _wrapps(wrapper, func)
        return wrapper
    return generator


def _return_func(value):
    msg, code = None, None
    if isinstance(value, bool):
        return value, msg, code
    if isinstance(value, (tuple, list)):
        if len(value) == 2:
            return value[0], value[1], code
        elif len(value) >= 3:
            return tuple(value[:3])
    return value


def _toStardardCondition(condition):
    """将各种格式的检查条件转换为检查函数"""
    if inspect.isclass(condition):
        return lambda x: isinstance(x, condition)
    if isinstance(condition, (tuple, list)):
        cls, condition = condition[:2]
        if condition is None:
            return _toStardardCondition(cls)
        if cls in (str, unicode) and condition[0] == condition[-1] == '/':    # '//'
            # condition[0] == condition[-1] == '/' 正则
            return lambda x: (isinstance(x, cls)
                              and re.match(condition[1:-1], x) is not None)
        return condition if (lambda x: isinstance(x, cls)) else 0
    return condition


def nullOk(cls, condition=None):
    """这个函数指定的检查条件可以接受None值"""
    return lambda x: x is None or _toStardardCondition((cls, condition))(x)


def multiType(*conditions):
    """这个函数指定的检查条件只需要有一个通过"""
    lstValidator = map(_toStardardCondition, conditions)

    def validate(x):
        for v in lstValidator:
            if v(x):
                return True

    return validate


def _getdefaultargs(args, varargs, keywords, defaults):
    """获取调用函数的参数的默认值"""
    # add by chenyang21
    dctArgs = {}
    varargs = tuple(varargs)    # 实参个数
    keywords = dict(keywords)

    argcount = len(args)    # 形参参数个数
    if not defaults:
        defaults = []
    else:
        defaults = list(defaults)
    varcount = len(varargs)
    callvarargs = None
    if argcount <= varcount:
        # 形参个数小于等于实参个数
        for n, argname in enumerate(args):
            if n < varcount:
                pass
            else:
                dctArgs[argname] = defaults[n-varcount]

        callvarargs = varargs[-(varcount - argcount):]  # 位置参数
    else:
        # 形参个数大于实参个数
        for n, var in enumerate(args):
            if n < varcount:
                # dctArgs[args[n]] = varargs[n]
                pass
            else:
                dctArgs[args[n]] = defaults[n-varcount]
        for argname in args[-(argcount - varcount):]:
            if argname in keywords:
                dctArgs[argname] = keywords.pop(argname)
        callvarargs = ()
    dctArgs.update(keywords)
    return dctArgs


def _getcallargs(args, varargname, kwname, varargs, keywords):
    """获取调用时的各参数名-值的字典"""
    dctArgs = {}
    varargs = tuple(varargs)
    keywords = dict(keywords)
    argcount = len(args)
    varcount = len(varargs)
    callvarargs = None
    if argcount <= varcount:
        for n, argname in enumerate(args):
            dctArgs[argname] = varargs[n]

        callvarargs = varargs[-(varcount - argcount):]   # 位置参数
    else:
        for n, var in enumerate(varargs):
            dctArgs[args[n]] = var
        for argname in args[-(argcount - varcount):]:
            if argname in keywords:
                dctArgs[argname] = keywords.pop(argname)
        # callvarargs = ()
    if varargname is not None:
        if callvarargs:
            dctArgs[varargname] = callvarargs
        elif varargname in keywords:
            dctArgs[varargname] = keywords.pop(varargname)
    if kwname is not None:
        dctArgs[kwname] = keywords
    dctArgs.update(keywords)
    return dctArgs


def _wrapps(wrapper, wrapped):
    """复制元数据"""
    for attr in ('__module__', '__name__', '__doc__'):
        setattr(wrapper, attr, getattr(wrapped, attr))
    for attr in ('__dict__',):
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    return wrapper


def max_11(x):
    if x > 11:
        return True, 'success', 1
    else:
        return False, 'less than 11', -1


@validParam(a=int, b=max_11, args=int)
def func(a, b=1, *args, **kwargs):
    result = Result()
    result.data = a, b, args, kwargs
    return result


if __name__ == '__main__':
    print 'result:::', func('a', 12, 13)
