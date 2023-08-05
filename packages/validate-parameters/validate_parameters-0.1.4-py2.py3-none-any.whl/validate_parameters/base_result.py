class Result(object):

    def __init__(self, flag=True, data=None, code=None, msg=None, status=None, return_values=None):
        self.flag = flag
        self.data = data
        self.code = code
        self.msg = msg
        self.status = status
        self.return_values = return_values

    def __setitem__(self, key, value):
        try:
            return super(Result, self).__setattr__(key, value)
        except AttributeError:
            raise KeyError('Result object has not key {}'.format(str(key)))

    def __getitem__(self, item):
        try:
            return super(Result, self).__getattribute__(item)
        except AttributeError:
            raise KeyError('Result object has not key {}'.format(str(item)))

    def __str__(self):
        return str(self.dict())

    @staticmethod
    def to_json(obj):
        """
        transfer Result objects to json objects
        usage: json.dumps(Result(), defaults=Result().to_json)
        :return:
        """
        return obj.dict()

    def dict(self):
        """
        transfer Result objects to dict
        :return:
        """
        return self.__dict__

    def __iter__(self):
        return self.dict().__iter__()


if __name__ == '__main__':
    result = Result()
    result.code = -1
    result["status"] = 2
    print result.status
    print result["code"]
    result_dict = result.dict()
    print type(result_dict)
    result_dict["tag"] = 1
    print result_dict
    import json
    print json.dumps(result, default=result.to_json)
    result["codesss"] = 1
    result.hahahaahah = 2
    print result