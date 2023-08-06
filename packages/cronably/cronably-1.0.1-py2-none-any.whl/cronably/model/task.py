

class Task(object):

    def __init__(self, id, id_job, start, end=None, status=None, message=None ):
        self.id = id
        self.id_job = id_job
        self.start = start
        self.end = end
        self.status = status
        self.msg = message

    @staticmethod
    def createFromQuery( param):
        if param:
            return Task(param[0], param[1], param[2], param[3], param[4], param[5])