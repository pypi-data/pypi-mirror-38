from dataclasses import dataclass, field
from typing import Callable, Any, List, Union, Dict


def search_property(instance, name):
    if hasattr(instance.__class__, name) and getattr(instance.__class__, name):
        return getattr(instance.__class__, name)
    else:
        return getattr(instance, name)


@dataclass
class UIElement:
    def render(self, context: dict) -> Any:
        raise NotImplementedError

    def is_visible(self, context: dict) -> bool:
        return True


@dataclass
class Button(UIElement):
    title: str = ""
    path: str = ""
    parameter: str = ""

    def render(self, context: dict) -> dict:
        return {
            "text": self.get_title(context),
            "callback_data": self.get_callback_data(context)
        }

    def get_title(self, context):
        return search_property(self, "title") or "Button"

    def get_path(self, context) -> str:
        return search_property(self, "path") or "/start"

    def get_parameter(self, context) -> str:
        return search_property(self, "parameter") or ""

    def get_callback_data(self, context) -> str:
        path = f"{self.get_path(context)}"

        parameter = self.get_parameter(context)
        if parameter:
            path += f":{parameter}"

        return path


@dataclass
class Row(UIElement):
    buttons: List[Button] = field(default_factory=list)

    def get_buttons(self, context):
        return search_property(self, "buttons")

    def get_view(self, context):
        return search_property(self, "view")

    def render(self, context: dict) -> list:
        _buttons = []

        for button in self.get_buttons(context):
            if button.is_visible(context):
                _buttons.append(
                    button.render(context)
                )

        return _buttons


@dataclass
class View:
    replace: bool = False

    title: str = ""
    init_hooks: List[Callable] = field(default_factory=list)
    input_hook: List[Callable] = field(default_factory=list)
    keyboard: List[Row] = field(default_factory=list)
    context: dict = field(default_factory=dict)

    def get_text(self, context):
        return ""

    def get_title(self, context):
        return search_property(self, "title")

    def get_init_hooks(self, context):
        return search_property(self, "init_hooks")

    def get_input_hook(self, context):
        return search_property(self, "init_hook")

    def get_keyboard(self, context):
        return search_property(self, "keyboard")

    def render(self, context):
        view = {
            "text": self.get_text(context),
            "keyboard": {
                "inline_keyboard": [],
                "resize_keyboard": True
            }
        }

        for hook in self.get_init_hooks(context):
            hook(context)

        for row in self.get_keyboard(context):
            if row.is_visible(context):
                rendered_row = row.render(context)

                if len(rendered_row):
                    view["keyboard"]["inline_keyboard"].append(rendered_row)

        return view

    def handle(self, *args, **kwargs):
        bot = kwargs.get("bot")
        context = {
            "bot": bot,
            "view": self
        }
        return self.render(context)


class EntityType:
    BOT_COMMAND = "bot_command"


@dataclass
class Bot:
    routes: Dict[str, View] = field(default_factory=dict)

    def add_route(self, path, view):
        self.routes[path] = view

    def handle_updates(self, updates: dict):
        if updates.get("ok"):
            for update in updates.get("result", []):
                self.handle_update(update)

    def handle_update(self, update: dict):
        chat_id = update["message"]["chat"]["id"]
        username = update["message"]["chat"]["username"]

        for entity in update.get("message", {}).get("entities", []):
            if entity.get("type") == EntityType.BOT_COMMAND:

                offset = entity["offset"]
                length = entity["length"]

                command = update["message"]["text"][offset:offset + length]

                self.handle_command(command, chat_id=chat_id, username=username)

    def handle_command(self, command, *args, **kwargs):
        view = self.routes.get(command)
        kwargs["bot"] = self

        if view:
            response = view.handle(*args, **kwargs)
            self.send_response(response, *args, **kwargs)

    def send_response(self, response, *args, **kwargs):
        raise NotImplementedError

    def set_user_keyboard_id(self, username):
        raise NotImplementedError

    def get_user_keyboard_id(self, username):
        raise NotImplementedError


__all__ = [
    "Button",
    "Row",
    "View",
    "Bot",
]
