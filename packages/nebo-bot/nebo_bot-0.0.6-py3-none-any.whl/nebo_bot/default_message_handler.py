from nebo_bot.city import Work
from nebo_bot.quest import Quest
from nebo_bot.city import City
from nebo_bot.humans import Humans


class BaseDefaultHandler:

    @staticmethod
    def request_give_post(city: City) -> None:
        raise NotImplementedError()

    @staticmethod
    def finish_invite(city: City) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_exists_in_city(city: City) -> None:
        raise NotImplementedError()

    @staticmethod
    def time_expired_wait_post(city: City) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_wait_your_invite(city: City) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_canceled(bot: object) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_in_city(city: City) -> None:
        raise NotImplementedError()

    @staticmethod
    def finished_get_cost(work: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def finished_get_delivery(work: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def finished_get_buy_products(work: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def lift_visitor_up(work: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def lift_finished(work: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def open_new_floor(work: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def set_to_work_human(humans: Humans) -> None:
        raise NotImplementedError()

    @staticmethod
    def buy_new_floor(object) -> None:
        raise NotImplementedError()

    @staticmethod
    def build_new_floor(object) -> None:
        raise NotImplementedError()

    @staticmethod
    def get_award(quest: Quest) -> None:
        raise NotImplementedError()


class DefaultHandler(BaseDefaultHandler):
    @staticmethod
    def request_give_post(city: City) -> None:
        pass

    @staticmethod
    def finish_invite(city: City) -> None:
        pass

    @staticmethod
    def bot_exists_in_city(city: City) -> None:
        pass

    @staticmethod
    def time_expired_wait_post(city: City) -> None:
        pass

    @staticmethod
    def bot_wait_your_invite(city: City) -> None:
        pass

    @staticmethod
    def bot_canceled(bot: object) -> None:
        pass

    @staticmethod
    def bot_in_city(city: City) -> None:
        pass

    @staticmethod
    def finished_get_cost(work: Work) -> None:
        pass

    @staticmethod
    def finished_get_delivery(work: Work) -> None:
        pass

    @staticmethod
    def finished_get_buy_products(work: Work) -> None:
        pass

    @staticmethod
    def lift_visitor_up(work: Work) -> None:
        pass

    @staticmethod
    def lift_finished(work: Work) -> None:
        pass

    @staticmethod
    def open_new_floor(work: Work) -> None:
        pass

    @staticmethod
    def set_to_work_human(humans: Humans) -> None:
        pass

    @staticmethod
    def buy_new_floor(object) -> None:
        pass

    @staticmethod
    def build_new_floor(object) -> None:
        pass

    @staticmethod
    def get_award(quest: Quest) -> None:
        pass