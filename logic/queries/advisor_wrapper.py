from advisor import ProbabilityAdvisor

class AdvisorLogic:
    @staticmethod
    def compute_best_keep(roll, abilities, last_reroll=True):
        return ProbabilityAdvisor.best_keep(roll, abilities, last_reroll)
