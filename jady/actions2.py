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

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionAnswerQuestion(Action):
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
        qp = QueryParser('title', schema=index.schema)
        query = qp.parse(u"" + str(qsn))
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

        responses = "Search result:\n"

        if intent:  # if User asked qns
            """ Search qsn in index """
            try:
                index = IndexBook.get_index(bookSchema=BookSchema())
                qp = QueryParser('intent', schema=BookSchema())
                query = qp.parse(u"" + intent)
                responses = "Les meilleurs chapitres ?? lire:\n"
                with index.searcher() as searcher:
                    result = searcher.search(query, limit=10)
                    # Change display msg if result is empty,

                    if len(result) == 0:
                        responses = "D??soler ! Je n'est pas de reponse pertinante pour cette question actuellement."
                        dispatcher.utter_message(text=responses)

                        return []

                    # Display answer if result not empty
                    dispatcher.utter_message(text=responses)

                    for num, resp in enumerate(result):
                        dispatcher.utter_message(
                            response="utter_answer_question",
                            chapter_title=resp['chapter_title'],
                            cover_img_path=resp['cover_img_path'],
                            book_title=resp['book_title'],
                            author=str(resp['creator']).upper(),
                            text_button="Je veux lire ce chapitre")
                        #  responses += "=============== "+str(num+1)+" =====================\n"
                        #  responses += 'Chapitre: ' + resp['chapter_title'] + "\n"
                        #  responses += "Livre: " + resp['book_title'] + " de " + str(resp['creator']).upper() + "\n"
                        # clique pour afficher le context/ resp['context']
                        #  responses += "Lien de lecture: Indisponible momentan??ment\n"
                        #  responses += 'Date de publication: ' + str(resp['published_date']) + "\n"
                        #  responses += 'Cat??gorie: ' + resp['tags'] + "\n"
                        #  responses += resp['content']
                        #  responses += "Cliquer ici pour acheter ce livre\n"
            except Exception as e:
                raise e

            return []
        else:
            dispatcher.utter_message(text='No question asked !')

            return []
        #  return [SlotSet("question", question), SlotSet("subject", subject)]

    @staticmethod
    def search_test():
        index = IndexBook.get_index(bookSchema=BookSchema())
        qp = QueryParser('chapter_title', schema=BookSchema())
        query = qp.parse(u"" + "La marchandise des rois")
        print("Search result:")
        with index.searcher() as searcher:
            with open('resulat.txt', 'w') as outfile:
                result = searcher.search(query)

                for num, resp in enumerate(result):
                    print(str(num) + ": " + resp['chapter_title'],
                          file=outfile)
                    #  print('\n'.join(wrap(resp['content'], 40)), file=outfile)
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
        ####### Call Database OR API #########
        response = "Ta Question est: {qsn}\n Le Theme: {th}".format(
            qsn=question, th=subject)
        dispatcher.utter_message(response)


if __name__ == '__main__':
    print('Je suis jady et je bouffe du code humhum !')
    ActionAnswerQuestion.search_test()
