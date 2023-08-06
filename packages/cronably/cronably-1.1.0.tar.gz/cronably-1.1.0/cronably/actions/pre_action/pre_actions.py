from cronably.actions.actions import Actions
from cronably.actions.pre_action.pre_action_validations import PreActionValidations
from cronably.actions.repetition.repetition_factory import RepetitionFactory
from cronably.model.job import Job
from cronably.repositories.db_manager import DbManager


class PreActions(Actions):

    def __init__(self, atts = {}):
        super(PreActions, self).__init__()
        self.processed_parameters = atts
        self.load_from_file = False
        self.repetition = None
        self.__job_repository = DbManager.get_instance().get_job_repository()
        self.run()

    def run(self):
        print "pre-actions started"
        validations = PreActionValidations(self.processed_parameters)
        validations.run()
        self.create_repetition(validations)
        self.create_job()

    def create_repetition(self, validations):
        if validations.has_repetition_strategy():
            self.repetition = RepetitionFactory(self.processed_parameters).get_repetition()

    def create_job(self):
        job = Job.create_job_from_params(self.processed_parameters)
        return self.__job_repository.create(job)
