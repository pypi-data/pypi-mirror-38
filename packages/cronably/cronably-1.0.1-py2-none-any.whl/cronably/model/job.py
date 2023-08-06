

class Job:

    def __init__(self, id, name, should_run=True, loops=1, report = False):
        self.id = id
        self.name = name
        self.should_run = should_run
        self.loops = loops
        self.report = report


    @staticmethod
    def createFromQuery( param):
        if param:
            return Job(param[0], param[1], param[2], param[3], param[4])