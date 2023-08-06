from unittest import TestCase

from botarang import View, Row, Button, Bot, BotConfigException

RESPONSE = {}

START_MESSAGE = {
    "ok": True,
    "result": [
        {
            "update_id": 100000000,
            "message": {
                "message_id": 484,
                "from": {
                    "id": 10000000,
                    "is_bot": False,
                    "first_name": "",
                    "last_name": "",
                    "username": "text",
                    "language_code": "ru"
                },
                "chat": {
                    "id": 10000000,
                    "first_name": "",
                    "last_name": "",
                    "username": "test",
                    "type": "private"
                },
                "date": 1540000000,
                "text": "/start",
                "entities":[
                    {
                        "offset": 0,
                        "length": 6,
                        "type": "bot_command"
                    }
                ]
            }
        }
    ]
}


class Back(Button):
    title = "<- Back"

    def is_visible(self, context: dict) -> bool:
        breadcrumbs = context.get("breadcrumbs", ["/start"])
        return len(breadcrumbs) > 1

    def get_callback_data(self, context) -> str:
        breadcrumbs = context.get("breadcrumbs", ["/start"])
        return breadcrumbs[-1]


class Navigation(Row):
    buttons = [
        Back()
    ]


class Breadcrumbs(Row):
    def get_buttons(self, context):
        breadcrumbs = context.get("breadcrumbs", ["/start"])

        buttons = []

        for raw_url in breadcrumbs:
            if ":" in raw_url:
                url, parameter = raw_url.split(":")
            else:
                url = raw_url
                parameter = ""
                
            view = context["bot"].routes.get(url)
            
            if not view:
                raise BotConfigException("View does not exist")

            buttons.append(
                Button(title=view.get_title(context), path=url, parameter=parameter)
            )

        return buttons


class AdminPanel(Row):
    def is_visible(self, context: dict) -> bool:
        return context.get("is_admin", False)


class UserPanel(Row):
    def is_visible(self, context: dict) -> bool:
        return not context.get("is_admin", False)


class HookException(BaseException):
    pass


class HomeView(View):
    title = "Home view"
    keyboard = [
        Navigation(),
        Breadcrumbs(),
        AdminPanel(),
        UserPanel(),
    ]


class BotForTest(Bot):
    def set_user_keyboard_id(self, username):
        pass

    def send_response(self, response, *args, **kwargs):
        global RESPONSE
        print(response)

        keys = list(RESPONSE.keys())
        for key in keys:
            del RESPONSE[key]

        RESPONSE.update(response)

    def get_user_keyboard_id(self, username):
        return 10000000




class ViewTestCase(TestCase):
    def test_view(self):
        global RESPONSE

        bot = BotForTest()
        bot.add_route("/start", HomeView())
        bot.handle_updates(START_MESSAGE)
        assert RESPONSE == {
            "text": "",
            "keyboard": {
                "inline_keyboard": [
                    [
                        {"text": "Home view", "callback_data": "/start"}
                    ]
                ],
                "resize_keyboard": True
            }
        }
