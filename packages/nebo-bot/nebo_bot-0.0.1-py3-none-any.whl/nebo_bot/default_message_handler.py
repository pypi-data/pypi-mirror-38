
from nebo_bot._city import Work


class BaseDefaultHandler:

    @staticmethod
    def request_give_post(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def finish_invite(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_exists_in_city(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def time_expired_wait_post(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_wait_your_invite(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_canceled(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def bot_in_city(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def finished_get_cost(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def finished_get_delivery(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def finished_get_buy_products(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def lift_visitor_up(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def lift_finished(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def open_new_floor(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def set_to_work_human(object: Work) -> None:
        raise NotImplementedError()

    @staticmethod
    def buy_new_floor(object) -> None:
        raise NotImplementedError()

    @staticmethod
    def build_new_floor(object) -> None:
        raise NotImplementedError()

    @staticmethod
    def get_award(object) -> None:
        raise NotImplementedError()


class DefaultHandler(BaseDefaultHandler):
    @staticmethod
    def get_award(object) -> None:
        pass

    @staticmethod
    def build_new_floor(object) -> None:
        pass

    @staticmethod
    def buy_new_floor(object) -> None:
        pass

    @staticmethod
    def request_give_post(object: Work) -> None:
        pass

    @staticmethod
    def finish_invite(object: Work) -> None:
        pass

    @staticmethod
    def bot_exists_in_city(object: Work) -> None:
        pass

    @staticmethod
    def time_expired_wait_post(object: Work) -> None:
        pass

    @staticmethod
    def bot_wait_your_invite(object: Work) -> None:
        pass

    @staticmethod
    def bot_canceled(object: Work) -> None:
        pass

    @staticmethod
    def bot_in_city(object: Work) -> None:
        pass

    @staticmethod
    def finished_get_cost(object: Work) -> None:
        pass

    @staticmethod
    def finished_get_delivery(object: Work) -> None:
        pass

    @staticmethod
    def finished_get_buy_products(object: Work) -> None:
        pass

    @staticmethod
    def lift_visitor_up(object: Work) -> None:
        pass

    @staticmethod
    def lift_finished(object: Work) -> None:
        pass

    @staticmethod
    def open_new_floor(object: Work) -> None:
        pass

    @staticmethod
    def set_to_work_human(object: Work) -> None:
        pass
