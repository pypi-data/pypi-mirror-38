import json
import re

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from schema import Schema, And, Optional


class Disambiguator(object):
    def __init__(self, disamb_rule=None, fallback_rule=None):

        self.disamb_schema = Schema({
            "trigger": And(str, len),
            Optional("max_suggestions", default=2): int,
            Optional("slot_name"): str,
            "display": {
                Optional("intro_template"): And(str, len),
                "text_template": And(str, len, error="text_template is required"),
                Optional("button_title_template_prefix", default="utter_disamb"): And(str, len),
                Optional("fallback_button"): {
                    "title": And(str, len, error="fallback button title is required"),
                    "payload": And(str, len, error="fallback button payload is required")
                },
                Optional("exclude", default=[]): list
            }
        })
        self.fallback_schema = Schema({
            "trigger": And(str, len),
            Optional("slot_name"): str,
            "display": {
                "text": And(str, len),
                Optional("buttons"):
                    [{"title": And(str, len, error="button title is required"),
                      "payload": And(str, len, error="button title is required")}]
            }
        })
        if disamb_rule:
            self.disamb_schema.validate(disamb_rule)
        if fallback_rule:
            self.fallback_schema.validate(fallback_rule)

        self.disamb_rule = disamb_rule
        self.fallback_rule = fallback_rule

        if self.disamb_rule and "max_suggestion" not in self.disamb_rule:
            self.disamb_rule["max_suggestions"] = 2

        if self.disamb_rule and "exclude" not in self.disamb_rule["display"]:
            self.disamb_rule["display"]["exclude"] = []

        if self.disamb_rule and "button_title_template_prefix" not in self.disamb_rule["display"]:
            self.disamb_rule["display"]["button_title_template_prefix"] = "utter_disamb"

    @staticmethod
    def is_triggered(parse_data, trigger):
        pattern = re.compile(r"\$(\d)")
        eval_string = trigger
        matches = re.findall(pattern, trigger)
        for i in matches:
            # if not enough intents in ranking to apply the rule, policy rule can't be triggered
            if int(i) >= len(parse_data["intent_ranking"]):
                return False
            eval_string = re.sub(r'\$' + i, str(parse_data["intent_ranking"][int(i)]["confidence"]), eval_string)

        return len(parse_data["intent_ranking"]) and eval(eval_string, {'__builtins__': {}})

    def should_fallback(self, parse_data):
        if not self.fallback_rule or "intent_ranking" not in parse_data:
            return False

        return self.is_triggered(parse_data, self.fallback_rule["trigger"])

    def should_disambiguate(self, parse_data):
        if not self.disamb_rule or "intent_ranking" not in parse_data:
            return False

        return self.is_triggered(parse_data, self.disamb_rule["trigger"])

    def should_exclude(self, intent_name):
        return any([re.match(x, intent_name) for x in self.disamb_rule["display"]["exclude"]])

    def get_payloads(self, parse_data, intents, keep_entities=True):
        entities = ""
        if "entities" in parse_data and keep_entities:
            entities = json.dumps(dict(map(lambda e: (e["entity"], e["value"]), parse_data["entities"])))
        payloads = list(["/{}{}".format(i, entities) for i in intents])
        return payloads

    def get_intent_names(self, parse_data):
        intent_names = list(map(lambda x: x["name"], parse_data["intent_ranking"]))
        if self.disamb_rule["display"]["exclude"]:
            intent_names = list(filter(lambda x: not self.should_exclude(x), intent_names))
        return intent_names[:self.disamb_rule["max_suggestions"]]

    def disambiguate(self, parse_data, tracker, dispatcher, run_action):
        should_disambiguate = self.should_disambiguate(parse_data)

        if should_disambiguate:
            intents = self.get_intent_names(parse_data)
            self.disamb_rule['parse_data'] = parse_data
            action = ActionDisambiguate(self.disamb_rule, self.get_payloads(parse_data, intents), intents)
            run_action(action, tracker, dispatcher)
            return True

    def fallback(self, parse_data, tracker, dispatcher, run_action):
        should_fallback = self.should_fallback(parse_data)

        if should_fallback:
            self.fallback_rule['parse_data'] = parse_data
            action = ActionFallback(self.fallback_rule)
            run_action(action, tracker, dispatcher)
            return True


class ActionDisambiguate(Action):

    def __init__(self, rule, payloads, intents):
        self.rule = rule
        self.payloads = payloads
        self.intents = intents

    @staticmethod
    def get_disambiguation_message(dispatcher, rule, payloads, intents, tracker):
        buttons = []
        for intent, payload in zip(intents, payloads):
            template_key = "{}_{}".format(rule["display"]["button_title_template_prefix"], intent)
            buttons.append({
                "title": ActionDisambiguate.generate_title(dispatcher, template_key, tracker),
                "payload": payload
            })

        if "fallback_button" in rule["display"] and \
                "title" in rule["display"]["fallback_button"] and \
                "payload" in rule["display"]["fallback_button"]:
            buttons.append({
                "title": ActionDisambiguate.generate_title(dispatcher, rule["display"]["fallback_button"]["title"],
                                                           tracker),
                "payload": rule["display"]["fallback_button"]["payload"],
            })

        disambiguation_message = {
            "text": ActionDisambiguate.generate_title(dispatcher, rule["display"]["text_template"], tracker),
            "buttons": buttons
        }

        return disambiguation_message

    @staticmethod
    def generate_title(dispatcher, template_key, tracker):
        template = dispatcher.nlg.generate(template_key, tracker, dispatcher.output_channel)
        if isinstance(template, list):
            assert len(template), 'expected list to be populated with at least one element'
            template = template[0]

        assert isinstance(template, dict), 'template should be converted to a dict object'
        return template["text"]

    def run(self, dispatcher, tracker, domain):
        if "intro_template" in self.rule["display"]:
            dispatcher.utter_template(self.rule["display"]["intro_template"], tracker)

        disambiguation_message = self.get_disambiguation_message(dispatcher, self.rule, self.payloads, self.intents,
                                                                 tracker)
        dispatcher.utter_response(disambiguation_message)

        return_value = []
        if self.rule['slot_name']:
            return_value.append(SlotSet(self.rule['slot_name'], self.rule['parse_data']))
        return return_value

    def name(self):
        return 'action_disambiguate'


class ActionFallback(Action):

    def __init__(self, rule):
        self.rule = rule

    @staticmethod
    def get_fallback_message(dispatcher, rule, tracker):
        fallback_message = {
            "text": dispatcher.nlg.generate(rule["display"]["text"], tracker, dispatcher.output_channel)["text"]
        }
        if "buttons" in rule["display"]:
            buttons = list(
                [{"title": dispatcher.nlg.generate(button["title"], tracker, dispatcher.output_channel)["text"],
                  "payload": button["payload"]} for button in rule["display"]["buttons"]])
            fallback_message["buttons"] = buttons
        return fallback_message

    def run(self, dispatcher, tracker, domain):
        fallback_message = self.get_fallback_message(dispatcher, self.rule, tracker)
        dispatcher.utter_response(fallback_message)

        return_value = []
        if self.rule['slot_name']:
            return_value.append(SlotSet(self.rule['slot_name'], self.rule['parse_data']))
        return return_value

    def name(self):
        return 'action_fallback'
