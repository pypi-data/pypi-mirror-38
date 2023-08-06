from cronably.actions.actions import Actions
from cronably.actions.pre_action.pre_action_validations import PreActionValidations
from cronably.actions.repetition.std_repetition import StdRepetition
from cronably.actions.repetition.weekly_repetition import WeeklyRepetition
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
            if self._get_frame() == 'WEEKLY':
                self.repetition = self.create_weeklyRepetition()
            else:
                self.repetition = StdRepetition(self._get_frame(), self._get_period())

    def create_job(self):
        loops = self.job_check_loop()
        report = self.job_check_report()
        job = Job(-1, self.processed_parameters['name'], True, loops, report)
        return self.__job_repository.create(job)

    def job_check_loop(self):
        return self._check_param("loops", 1)

    def job_check_report(self):
        report = self._check_param("report", "n")
        return 1 if report.lower() == "y" else 0

    def _check_param(self, param, default):
        if param in self.processed_parameters.keys():
            return self.processed_parameters[param]
        return default

    def _check_frame(self, frame):
        return self._get_frame() == frame

    def _get_period(self):
        return self._get_value_according_config_source('period')

    def _get_frame(self):
        frame = self._get_value_according_config_source('frame')
        return frame.upper()

    def _get_value_according_config_source(self, value):
        if self._check_param('ext_config', False):
            return self.processed_parameters['repetition.%s' % value]
        else:
            return self.processed_parameters['repetition_%s' % value]

    def _get_day(self):
        day = 'period.day' if self._check_param('ext_config', False) else 'period_day'
        return self._get_value_according_config_source(day)

    def _get_time(self):
        time = 'period.time' if self._check_param('ext_config', False) else 'period_time'
        return self._get_value_according_config_source(time)

    def create_weeklyRepetition(self):
        repetition = WeeklyRepetition(self._get_day(), self._get_time())
        repetition.update_next_time_run()
        return repetition
