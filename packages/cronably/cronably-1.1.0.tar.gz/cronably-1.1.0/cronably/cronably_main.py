from cronably.actions.pre_action.pre_actions import PreActions
from cronably.context.context import Context

ext_cronably = None

class Cronably(object):

    def __init__(self, **kwargs):
        global ext_cronably
        self.annotation_params = kwargs
        self.context = Context()
        ext_cronably = self


    def __call__(self, original_func):
        decorator_self = self
        def execute(*args):
            preaction = decorator_self.pre_actions()
            decorator_self.context.execute(original_func, decorator_self.annotation_params, preaction.repetition)
            decorator_self.post_actions()
        return execute

    def pre_actions(self):
        global context
        if not self.annotation_params:
            self.annotation_params = {}
        return PreActions(self.annotation_params)



    def post_actions(self):
        print "post actions"

def exist_job(name):
    context = ext_cronably.context
    if not context:
        context = Context()
    return context.check_exist_job(name)


@Cronably(name="HOLA_MUNDO", loops=1)
def my_process():
    print "Hola Mundo"


