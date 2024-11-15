import gradio as gr
import os
import json
import HERMES
from openai import OpenAI
from dotenv import load_dotenv
import time
from enum import Enum

from typing import Iterable
# from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
# from llama_index.core.query_engine import CustomQueryEngine
# from llama_index.core.retrievers import BaseRetriever
# from llama_index.core import get_response_synthesizer
# from llama_index.core.response_synthesizers import BaseSynthesizer
# from llama_index.core import PromptTemplate
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
# from llama_index.llms.openai import OpenAI as openai
import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4
from huggingface_hub import CommitScheduler
reference = HERMES.HermesRef

# --------------------------------------------------------------
# loading openAI API Key
# --------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# --------------------------------------------------------------
# Interface Theme
# --------------------------------------------------------------

class Theme(Base):
    def __init__(
        self,
        *,
        primary_hue: colors.Color | str = colors.gray,
        secondary_hue: colors.Color | str = colors.gray,
        neutral_hue: colors.Color |  str = colors.gray,
        spacing_size: sizes.Size | str = sizes.spacing_md,
        radius_size: sizes.Size | str = sizes.radius_md,
        text_size: sizes.Size | str = sizes.text_lg,


        font: fonts.Font
        | str
        | Iterable[fonts.Font | str] = (
            fonts.GoogleFont("Roboto"),

        ),

    ):
        super().__init__(
            primary_hue=primary_hue,
            secondary_hue=secondary_hue,
            neutral_hue=neutral_hue,
            spacing_size=spacing_size,
            radius_size=radius_size,
            text_size=text_size,
            font=font,

        )


        super().set(
        #block_title_text_weight="600",
        #block_border_width="1.5px",
        block_shadow="*shadow_drop_lg",
        #button_shadow="*shadow_drop_lg",
        body_background_fill=None,
        body_background_fill_dark=None,
        body_text_color='#606060',
        body_text_color_dark=None,
        background_fill_primary='white',
        background_fill_primary_dark=None,
        background_fill_secondary=None,
        background_fill_secondary_dark=None,
        border_color_primary='#606060',
        border_color_primary_dark=None,
        input_border_color='#606060',
        body_text_size="40px",
        #block_title_text_size="None",

        block_background_fill='#F4F4F4',
        block_background_fill_dark=None,
        block_label_background_fill='#1066FF',
        block_label_background_fill_dark=None,
        block_label_text_color='white',
        block_label_text_color_dark=None,
        block_title_text_color='#606060',
        block_title_text_color_dark=None,
        input_background_fill='#E2E2E2',
        input_background_fill_dark=None,
        button_primary_background_fill='#606060',
        button_primary_background_fill_dark=None,
        button_primary_text_color='white',
        button_primary_text_color_dark=None,


        )

# --------------------------------------------------------------
# Helper classes
# --------------------------------------------------------------
#   --------------------
#   Language enum
#   --------------------
class Language(Enum):
    German=1
    French=2
    English=3



# --------------------------------------------------------------
# Questions
# --------------------------------------------------------------

#Question bank. TODO: Connect to question generator here.
questions = [

    {"question_text": "In welche Phasen wird der HERMES-Projektlebenszyklus unterteilt?",
    "correct_answer": "Der HERMES-Projektlebenszyklus wird unterteilt in Projektbeginn, Lösungsentstehung und Projektende",
    "link": "1.1.1"},

    {"question_text": "Welche Phasen gewährleisten die Einheitlichkeit der Projektstruktur und des Lebenszyklus?",
    "correct_answer": "Ein Projekt beginnt mit der Phase Initialisierung und endet mit der Phase Abschluss. Dadurch wird die Einheitlichkeit der Projektstruktur und des Projektlebenszyklus gewährleistet.",
    "link": "1.2.2"},

    {"question_text": "Auf welcher Grundlage beauftragt der Auftraggeber die Durchführung der Phase Initialisierung?",
    "correct_answer": "Projektinitialisierungsauftrags gibt der Auftraggeber die Ressourcen für die Phase Initialisierung frei. Er beauftragt den Projektleiter mit der Durchführung der Phase Initialisierung.",
    "link": "1.4.1.1"},

    {"question_text": "Wozu dienen die Checklisten?",
    "correct_answer": "Checklisten gehören zu den Dokumenten. Sie werden zur Unterstützung bei der Entscheidungsfindung genutzt.",
    "link": "4.4.1.12"},

    {"question_text": "Was bildet ein Szenario ab?",
    "correct_answer": "Wie die Abbildung 17 zeigt, bildet ein Szenario die komplette Lösungsentstehung eines Projekts ab und unterstützt den Projektleiter bei der Durchführungsplanung. ",
    "link": "2.1"},

    {"question_text": "Was muss in jedem Projekt erarbeitet werden, damit ein Projekt gesteuert und geführt werden kann?",
    "correct_answer": "In jedem Projekt müssen bestimmte Ergebnisse, die minimal geforderten Dokumente, erarbeitet werden, damit ein Projekt gesteuert und geführt werden kann.",
    "link": "7.4.1.7"},

    {"question_text": "Was passiert, wenn am Ende einer Phase oder eines Release die Risiken als nicht tragbar beurteilt werden?",
    "correct_answer": "Werden am Ende einer Phase oder eines Release die Risiken als nicht tragbar beurteilt, muss über das weitere Vorgehen befunden und das Projekt eventuell abgebrochen werden. ",
    "link": "7.4.1.7"},

    {"question_text": "Worin darf der Projektleiter beim Entwicklungsteam nicht eingreifen?",
    "correct_answer": "Die Projektführungsverantwortung liegt beim Projektleiter, er darf dennoch nicht in die Selbstorganisation des Entwicklungsteams eingreifen. Das Entwicklungsteam organisiert sich selbst.",
    "link": "6.4.3.5"},

    {"question_text": "Wann beginnt die finanzielle Steuerung und Führung des Projektes?",
    "correct_answer": "Die finanzielle Steuerung und Führung des Projekts beginnt mit dem Entscheid Projektinitialisierungsfreigabe und endet mit dem Entscheid Projektabschluss, allenfalls mit dem Entscheid Projektabbruch.",
    "link": "7.4.4.1"},

    {"question_text": "Wann ist ein Projektabbruch möglich?",
    "correct_answer": "Ein Projektabbruch ist nur im Rahmen der Lösungsentstehung möglich, also nach dem Entscheid Durchführungsfreigabe und vor dem Entscheid Phasenfreigabe Abschluss.",
    "link": "5.4.1.6"},

    {"question_text": "Wozu dient die Leistungsvereinbarung?",
    "correct_answer": "Mit der Leistungsvereinbarung entsteht eine klar geregelte Beziehung zwischen dem Projekt und den (internen oder externen) Dienstleistungserbringern einerseits und zwischen der Projekt- und der Stammorganisation anderseits.",
    "link": "5.4.3.18"},

    {"question_text": "Wofür schafft die Integration des Systems in die Betriebsinfrastruktur die Voraussetzungen?",
    "correct_answer": "Die Integration des Systems in die Betriebsinfrastruktur schafft die Voraussetzungen für die Durchführung der Tests und für die Vorabnahme.",
    "link": "5.4.3.47"},

    {"question_text": "In welchem Bereich unterscheiden sich die klassische und die agile Vorgehensweise?",
    "correct_answer": "Die klassische und die agile Vorgehensweise unterscheiden sich im Bereich der Lösungsentstehung durch das Entwicklungsvorgehen.",
    "link": "1.1.3"},

    {"question_text": "Welche Verantwortung trät die Projektunterstützung?",
    "correct_answer": "Verantwortung der an die Rolle delegierten Aktivitäten",
    "link": "6.4.2.3"},

    {"question_text": "Welche Rolle ist verantwortlich für die Ergebnisse des Projekts und die Erreichung der gesetzten Ziele innerhalb der gesetzten Rahmenbedingungen?",
    "correct_answer": "Der Auftraggeber ist verantwortlich für die Ergebnisse des Projekts und die Erreichung der gesetzten Ziele innerhalb der gesetzten Rahmenbedingungen." ,
    "link": "6.4.1.1"},

    {"question_text": "Zu welchem Zeitpunkt wird das für die Durchführung benötigte Investitionsbudget durch die Stammorganisation bewilligt?",
    "correct_answer": "Mit dem Entscheid Durchführungsfreigabe wird das für die Durchführung benötigte Investitionsbudget durch die Stammorganisation bewilligt.",
    "link": "7.4.4.3"},

    {"question_text": "Woraus basiert das Produktkonzept?",
    "correct_answer": "Das Produktkonzept basiert direkt auf den Lösungsanforderungen, auf allfälligen Organisationsanforderungen und auf der Studie.",
    "link": "5.4.3.32"},

    {"question_text": "Was wird im Anschluss an die Entwicklung oder Anpassung des Produkts erarbeitet?",
    "correct_answer": "Im Anschluss an die Entwicklung oder Anpassung des Produkts werden die Produktdokumentation sowie das Anwendungshandbuch erarbeitet.",
    "link": "5.4.3.31"},

    {"question_text": "Wie detailliert werden die Ausschreibungsunterlagen erstellt?",
    "correct_answer": "Die Ausschreibungsunterlagen werden so detailliert erstellt, dass die Angebote nachvollziehbar bewertet werden können.",
    "link": "5.4.3.5"},

    {"question_text": "Was ist der Zweck des Organisationskonzepts?",
    "correct_answer": "Das Organisationskonzept vertieft die in der Studie beschriebene und gewählte Lösungsvariante aus organisatorischer Sicht.",
    "link": "4.4.1.29"},

    {"question_text": "Wozu dient das Modul Projektgrundlagen?",
    "correct_answer": "Das Modul Projektgrundlagen schafft eine konkrete, fundierte Ausgangslage für eine mögliche Lösungsentstehung und den darauffolgenden Projektabschluss.",
    "link": "3.4.2.1"},

    {"question_text": "Wie kommt bei der agilen Vorgehensweise der Änderungsantrag zum Tragen?",
    "correct_answer": "Der Änderungsantrag kommt ausschliesslich bei klassisch geführter Lösungsentstehung zum Tragen und bildet die Grundlage für eine inhaltliche Änderung.",
    "link": "4.4.1.2"},

    {"question_text": "Wie kommt bei der agilen Vorgehensweise der Änderungsantrag zum Tragen?",
    "correct_answer": "Der Änderungsantrag kommt ausschliesslich bei klassisch geführter Lösungsentstehung zum Tragen und bildet die Grundlage für eine inhaltliche Änderung.",
    "link": "4.4.1.2"},

    {"question_text": "Kann das Szenario Organisationsanpassung agil verwendet werden?",
    "correct_answer": "Das Szenario Organisationsanpassung ist als ein klassisches Szenario angedacht. Will man es agil verwenden, muss das Szenario mittels Tailoring* entsprechend erweitert werden.",
    "link": "2.2.2"},

    {"question_text": "Woran richtet sich das Sizing eines HERMES-Szenarios?",
    "correct_answer": "Sizing richtet sich nach der Grösse des anzugehenden Vorhabens oder dessen Wertigkeit. ",
    "link": "2.2.3.2"},

    {"question_text": "Was erfolgt am Ende der Phase Abschluss?",
    "correct_answer": "Am Ende der Phase Abschluss wird der Projektabschluss durchgeführt. Die Projektschlussbeurteilung wird erarbeitet. Offene Punkte werden an die Stammorganisation sowie an die Anwendungsorganisation übergeben. Das Projekt wird abgeschlossen und die Projektorganisation aufgelöst.",
    "link": "1.4.4.1"},

    {"question_text": "Worauf basieren Szenarien?",
    "correct_answer": "Szenarien basieren auf Modulen mit thematisch zusammengehörenden Aufgaben und Ergebnissen.",
    "link": "2.2.1"},

    {"question_text": "Was enthalten Module?",
    "correct_answer": "Module enthalten thematisch zusammengehörende Aufgaben und Ergebnisse.",
    "link": "3.1"},

    {"question_text": "Womit wird neben Projektlebenszyklus und Phasen die Projektstruktur weiter unterstützt?",
    "correct_answer": "Die Projektstruktur wird zusätzlich durch die im Kapitel 4 beschriebenen Meilensteine unterstützt. Sie markieren im Projektverlauf wichtige Entscheidungsergebnisse der Projektsteuerung und -führung.",
    "link": "1.2.2"},

    {'question_text': 'Was sind die gleichwertigen Methodenelemente, die gemeinsam die HERMES-Methode bilden?',
     'correct_answer': 'HERMES-Portfoliomanagement, HERMES-Projektmanagement und HERMES-Anwendungsmanagement',
     'link': 'A.2'},

]

# --------------------------------------------------------------
# RAG ## TODO: Remove; not in the current version
# --------------------------------------------------------------

# --------------------------------------------------------------
# Loading the documents
# --------------------------------------------------------------

# documents_questions = SimpleDirectoryReader("questions").load_data()
# index_questions = VectorStoreIndex.from_documents(documents_questions)
# retriever_questions = index_questions.as_retriever()

# --------------------------------------------------------------
# Using query engine
# --------------------------------------------------------------
#from llama_index.llms.openai import OpenAI

'''
class RAGQueryEngine(CustomQueryEngine):
    """RAG Query Engine."""

    retriever: BaseRetriever
    response_synthesizer: BaseSynthesizer
    llm: OpenAI


    def custom_query(self, query_str: str):
        nodes = self.retriever.retrieve(query_str)
        response_obj = self.response_synthesizer.synthesize(query_str, nodes)
        return response_obj
llm = OpenAI(model="gpt-3.5-turbo")
synthesizer = get_response_synthesizer(response_mode="compact")
query_engine_question = RAGQueryEngine(retriever=retriever_questions, response_synthesizer=synthesizer, llm = llm)
'''
# --------------------------------------------------------------
# Format the response as a JSON object ##TODO: Either use it or check that it is in use
# --------------------------------------------------------------

def format_response(response,instruction):

    chat_completion = client.chat.completions.create(
        messages = [{"role": "system", "content": instruction},
        {"role": "user", "content": response},],
        model = "gpt-3.5-turbo",
        response_format = {"type": "json_object"},
        temperature = 0.2,
    ).choices[0]
    content = chat_completion.message.content
    formated_response = json.loads(content)
    return formated_response

# --------------------------------------------------------------
# Feedback functions
# --------------------------------------------------------------

'''
#RAG again; TODO remove

def get_correctness_queryEngine(question,answer):
    instruction_correctness = "classify the query as either correct or incorrect depending on the sense of the query and output a valid JSON containing the key correctness and the value as either correct or incorrect"
    query= f" Is : [{answer}], the correct answer to the question :'question_text': [{question}], output as either 'correct' or 'incorrect'."
    response = query_engine_question.query(query)
    response = str(response)
    formated_response = format_response(response,instruction_correctness)
    return formated_response['correctness']

    '''

##TODO: Check that "link no tfound/ question not found" doesn't happen in most situations/ fix it if it does
def get_link_questions(question):
    for q in questions:
        if q["question_text"] == question:
            return q["link"]
    return "Link not found."

def get_answer(question):
    for q in questions:
        if q["question_text"] == question:
            return q["correct_answer"]
    return "Question not found."

def summarize(question):
    #todo: if answer is correct, give chapter information as well.

    chapter = get_link_questions(question)
    text =  get_information(chapter)
    correct_answer = get_answer(question)

    chat_completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [{"role": "system", "content":f'''find the correct answer:[{correct_answer}] in the text:[{text}], output the coorect answer: [{correct_answer}] and summarize the text: [{text}] in 4 sentences in German'''},],
        temperature = 0.2,
    ).choices[0]
    content = chat_completion.message.content
    return content

def get_information(chapter_number):
    for entry in reference:
        if entry['chapter'] == chapter_number:
            return entry['information']
    return "Chapter not found"


# --------------------------------------------------------------
# New get_correctness
# --------------------------------------------------------------


def get_correctness(question,answer):
    lsp =  ' « '
    rsp = ' » '


    header_question = ('Die Frage lautet wie folgt: ')
    hermes_extract_link = get_link_questions(question)
    hermes_extract = get_information(hermes_extract_link)\
                .replace('\n    ','')\
                .replace('\n\t',' ')\
                .replace('- ','')\
                .replace('\n','')

    header_answer_to_test = 'Ist die folgende Antwort entweder korrect oder falsch: '
    answer_to_test = answer
    correct_answer = get_answer(question)
    header_correct_answer = 'Diese Antwort ist eine korrekte: '

    prefix2 = ('Bitte prüfen Sie die folgende Antwort, indem Sie diese mit '
                'den im Handbuch der Hermes-Methode verwendeten Konzepten und Terminologien vergleichen. '
                'Geben Sie an, ob diese Antwort nach den Standards der Hermes-Methode richtig oder falsch ist, '
                'und erläutern Sie ausführlich die Gründe für die Bewertung. '
                'Konzentrieren Sie sich auf Begriffe wie sie im folgenden Abschnitt der Hermes-Methode definiert sind: ')

    categorization ='Bitte klassifiert ein JSON mit key correctness und Wert als entweder:' + lsp + 'correct' + 'oder' + rsp + 'incorrect'

    prompt = prefix2 + lsp + hermes_extract + rsp \
    + header_correct_answer + lsp + correct_answer +rsp \
    + header_question + lsp + question + rsp \
    + header_answer_to_test + lsp + answer_to_test + rsp +'?'\
    +categorization

    chat_completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [{"role": "system", "content":prompt},],
        temperature = 0.2,
        response_format = {"type": "json_object"},
    ).choices[0]
    content = chat_completion.message.content
    data = content
    parsed_data = json.loads(data)
    correct_value = parsed_data["correctness"]

    return correct_value




# --------------------------------------------------------------
# Store User Data #TODO: tentatively, remove this; only useful for studying individual user's history
# if we use it, change datastore location - this one is a huggingface DB
# --------------------------------------------------------------

JSON_DATASET_DIR = Path("json_dataset")
JSON_DATASET_DIR.mkdir(parents=True, exist_ok=True)

JSON_DATASET_PATH = JSON_DATASET_DIR / f"train-{uuid4()}.json"

# scheduler = CommitScheduler(
#     repo_id="nana95/users_history",
#     repo_type="dataset",
#     folder_path=JSON_DATASET_DIR,
#     path_in_repo="data",
# )


def save(question,chatbot, request: gr.Request):
    user = request.username
    with scheduler.lock:
        with JSON_DATASET_PATH.open("a") as f:
            json.dump({"question": question, "chatbot": chatbot, "user": user, "datetime": datetime.now().isoformat()}, f)
            f.write("\n")

# --------------------------------------------------------------
# The Interaction has 3 steps: the first trial, a second trial with
# a hint and the last step with the correct answer and the feedback
# --------------------------------------------------------------

'''
##TODO remove; this is from the RAG version (RAG)
def submit(question, message, chat_history):

        correctness = get_correctness_queryEngine(question,message)
        if "incorrect" in correctness:
            bot_message = f"Deine Antwort ist falsch, versuche es noch einmal!"
        else:
            bot_message = f"Deine Antwort ist richtig, gute Arbeit!"  +" "+ summarize(question)
        return bot_message

        '''

# First attempt runs this
def retry(question, message, chat_history):
        answer = get_answer(question)
        correctness = get_correctness(question,message)
        link = get_link_questions(question)
        if "incorrect" in correctness:
            bot_message = f"Deine Antwort ist falsch, versuche es noch einmal, bitte sieh dir die folgenden Kapitel an: {link}."
        else:
            bot_message = f"Deine Antwort ist richtig, gute Arbeit!" +" "+ summarize(question)
        return bot_message

#Second attempt after a wrong answer
def feedback(question, message, chat_history):
    answer = get_answer(question)
    correctness = get_correctness(question,message)
    summary = summarize(question)
    if "incorrect" in correctness:
        bot_message = f"Deine Antwort ist falsch! "+ " " + summarize(question)
    else:
        bot_message = f"Deine Antwort ist richtig, gute Arbeit!" +" "+ summarize(question)

    #bot_message = f"{summary}"
    return bot_message


# --------------------------------------------------------------
# Interactive Interface
# --------------------------------------------------------------

'''
#TODO remove RAG
def update_chatbot(chatbot,question_text, msg):
    css = """
    #correct {background-color: #34D640}
    #incorrect {background-color: #ED73FF}

    """

    correctness = get_correctness_queryEngine(question_text, msg)
    if correctness == 'correct':
        chatbot = gr.Chatbot(height=250, label="Feedback", elem_id="correct")
    elif correctness == 'incorrect':
        chatbot = gr.Chatbot(height=250, label="Feedback", elem_id="incorrect")
    else:
        chatbot = gr.Chatbot(height=250, label="Feedback")
    return chatbot
    '''

#Just color changes
def update_chatbot(chatbot,question_text, msg):
    css = """
    #correct {background-color: #d8fc9d}
    #incorrect {background-color: #f590af}

    """

    correctness = get_correctness(question_text, msg)
    if correctness == 'correct':
        chatbot = gr.Chatbot(height=300, label="Feedback", elem_id="correct")
    elif correctness == 'incorrect':
        chatbot = gr.Chatbot(height=300, label="Feedback", elem_id="incorrect")
    #else:
        #chatbot = gr.Chatbot(height=150, label="Feedback")
    return chatbot

# --------------------------------------------------------------
# Interface
# --------------------------------------------------------------

theme = Theme()

css = """
    #correct {background-color: #34D640}
    #incorrect {background-color: #ED73FF}
    h1 {
    color: #2073F7;
    display:block;}

    """

users = [("Test", "Test")]




def user(user_message, history):
    return "", history + [[user_message, None]]



# History within the question (knowing if first or second attempt)
def bot(history, messages_history,question,attempt_tracker):
    user_message = history[-1][0]
    bot_message, messages_history, attempt_tracker= handle_response(question, user_message, messages_history,attempt_tracker)
    #bot_message, messages_history = ask_gpt(user_message, messages_history)
    messages_history += [{"role": "assistant", "content": bot_message}]
    history[-1][1] = bot_message
    time.sleep(1) #TODO check if this is actually necessary
    return history, messages_history,attempt_tracker

#Clear history -> next question
def init_history(messages_history):
    messages_history = []
    #messages_history += [system_message]
    return messages_history

with gr.Blocks(theme=theme, css=css) as demo:
    gr.Markdown("## HERMES TRAINING SYSTEM")
    gr.Markdown("Hier ist ein Satz Fragen basierend auf dem Referenzhandbuch der HERMES-Methode.")
    gr.Markdown("Beantworten Sie jede Frage mit Ihren eigenen Worten und drücken Sie die Eingabetaste, um Rückmeldung zu erhalten.")



    attempt_tracker = gr.State({})

    def handle_response(question, message, messages_history,attempt_tracker):
        if question not in attempt_tracker:
            attempt_tracker[question] = 0
        attempts = attempt_tracker[question]
        if attempts == 0:
            #bot_message = submit(question, message, messages_history)
            bot_message = retry(question, message, messages_history)

        #elif attempts == 1:
            #bot_message = retry(question, message, messages_history)

        else:
            bot_message = feedback(question, message, messages_history)

        messages_history += bot_message
        attempt_tracker[question] = attempts + 1

        return bot_message, messages_history, attempt_tracker


    #ENUM: 0=German, 1=French, (2=English to be added at a later date)
    language = 0

    for index,question in enumerate(questions, start=1):
        with gr.Accordion(f"Frage {index}", open=False):
            with gr.Row():
                question_text = gr.Textbox(value=question['question_text'], interactive=False, visible=False)
                msg = gr.Textbox(label=question['question_text'])
            with gr.Row():
                chatbot = gr.Chatbot(height='300px',label="Feedback")
                state = gr.State([])
               # msg.submit(fn=update_chatbot, inputs=[chatbot ,question_text, msg], outputs=chatbot).success(fn=save, inputs=[question_text, chatbot],outputs=None,)
                msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(bot, [chatbot, state,question_text,attempt_tracker], [chatbot, state])

demo.launch(share=True)