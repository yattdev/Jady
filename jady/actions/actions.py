""" This files contains your custom actions which can be used to run
custom Python code.

See this guide on how to implement these action:
https://rasa.com/docs/rasa/custom-actions


This is a simple example for a custom action which utters "Hello World!"
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from typing import Any, Dict, List, Text

import requests
from indexation.index_book import IndexBook
from indexation.schema import BookSchema
from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
#  from rasa.core.actions.action import Action
from textwrap3 import wrap
from whoosh.qparser import QueryParser
import time


class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Bonjour! J'suis Jady")

        dispatcher.utter_message(
            text="Un IA Inpirer des entrepreneurs les plus reussites du monde")

        text = "Pour accompagner, conseiller, inspirer et orienter "
        text += "des entrepreneurs et les aspirants entrepreneur"
        dispatcher.utter_message(text)

        text = "Je réponds aux questions telles que:  \n"
        text += "• Quelles sont les convictions fondamentale de la reussite ?  \n"
        text += "• Comment définir ces objectifs ?  \n"
        text += "• Comment être plus productif dans mes tâches journalière ?  \n"
        dispatcher.utter_message(text)

        return []

    def delay(self, sec):
        time.sleep(sec)

        return None


class ActionAnswerQuestion(Action):
    """ Custom action that fetch from search ingine user qsn """
    def __init__(self):
        # Template to create a carousel for fetched books
        self.carousel = {
            "type": "template",
            "payload": {
                "template_type":
                "generic",
                "elements": [
                    # Responses from search engine will be place here as dict
                ]
            }
        }
        super().__init__()

    def name(self) -> Text:
        return "action_answer_question"

    async def action_searcher(self, qsn, search_field: List):
        """ Get user responses from book index
            by making search with asked question
            Correspond question and chapters Titles

            qsn: is a question
            search_field: is the list fields to search qsn into like 'title'
        """
        index = IndexBook.get_index(bookSchema=BookSchema)
        query_p = QueryParser('title', schema=index.schema)
        query = query_p.parse(u"" + str(qsn))
        with index.searcher() as searcher:
            result = searcher.search(query)

            return result

        return False

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:
        """
        type: (CollectingDispatcher, Tracker, Dict[Text, Any]
                )-> List[EventType]
        This method run custom action and back response to user
        """
        #  question = tracker.get_slot('question')  # Get user question
        # Get intent of last message
        intent = str(tracker.get_intent_of_latest_message())
        # delete _ in intent name
        intent = intent.split('_')
        intent = " ".join(intent)
        print('#######################################################')
        print('INTENT SEARCHING: ' + intent)
        print('############################ ANSWER ###################')
        # Le subjet n'exist plus dans les slot
        #  subject = tracker.get_slot('subject') Get subject for user question
        # ###### Call Database OR API #########

        #  dispatcher.utter_message(attachment=test_carousel)
        responses = "Search result:\n"

        if intent:  # if User asked qns
            """ Search qsn in index """
            answer = self.get_response(intent)

            if answer:
                responses = "Les meilleurs chapitres à lire:\n"
                # If there is the answer from search engine, answer == true
                dispatcher.utter_message(text=responses)
                dispatcher.utter_message(attachment=self.carousel)

                return []  # return empty, No slot here

            responses = "Désoler ! Je n'est pas de reponse pertinante pour\
                cette question actuellement."

            dispatcher.utter_message(text=responses)

            return []  # return empty, No slot here
        else:
            dispatcher.utter_message(text='No question asked !')

            return []  # return empty, No slot here
        #  return [SlotSet("question", question), SlotSet("subject", subject)]

    def get_response(self, intent: str):
        """ To search intent with search Engine """
        try:
            index = IndexBook.get_index(bookSchema=BookSchema())
            query_p = QueryParser('intent', schema=BookSchema())
            query = query_p.parse(u"" + intent)
            with index.searcher() as searcher:
                result = searcher.search(query, limit=10)

                if len(result) == 0:
                    # there is None for current intent so return False

                    return False

                for num, resp in enumerate(result):
                    self.carousel['payload']['elements'].append({
                        "index":
                        num,
                        "Livre":
                        resp['book_title'],
                        "Auteur":
                        str(resp['creator']).upper(),
                        "Chapitre":
                        resp['chapter_title'],
                        "image_url":
                        "http://0.0.0.0:5056/static/" + resp['cover_img_path'],
                        "buttons": [{
                            "title": "Lire",
                            "url": "#",
                            "type": "web_url"
                        }]
                    })

            return True
        except Exception as error:
            raise error

        return False

    @staticmethod
    def search_test():
        """ My search test """
        index = IndexBook.get_index(bookSchema=BookSchema())
        query_p = QueryParser('chapter_title', schema=BookSchema())
        query = query_p.parse(u"" + "La marchandise des rois")
        print("Search result:")
        with index.searcher() as searcher:
            with open('resulat.txt', 'w') as outfile:
                result = searcher.search(query)

                for num, resp in enumerate(result):
                    print(str(num) + ": " + resp['chapter_title'],
                          file=outfile)
                    #  print('\n'.join(wrap(resp['content'], 40)),
                    #  file=outfile)
                    print(resp['content'], file=outfile)
            #  response = result[0]
            #  print(responses)


class ActionPresentModels(Action):
    def name(self):
        return "action_bot_present_its_models"

    def run(self, dispatcher, tracker, domaine):
        """
            type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        """
        question = tracker.get_slot('question')  # Get user question
        subject = tracker.get_slot('subject')  # Get subject for user question
        # Call Database OR API #
        response = "Ta Question est: {qsn}\n Le Theme: {th}".format(
            qsn=question, th=subject)
        dispatcher.utter_message(response)


if __name__ == '__main__':
    print('Je suis jady et je bouffe du code humhum !')
    ActionAnswerQuestion.search_test()
