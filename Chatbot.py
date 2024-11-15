
# --------------------------------------------------------------
# Imports
# --------------------------------------------------------------

import gradio as gr
import os
import HERMES
import json
from openai import OpenAI
from dotenv import load_dotenv
import time
from gradio.themes.base import Base
from gradio.themes.utils import colors, fonts, sizes
from typing import Dict, Optional, Iterable
reference = HERMES.reference
from typing import List, Tuple, Optional
from dataclasses import dataclass




# --------------------------------------------------------------
# loading openAI API Key
# --------------------------------------------------------------
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


# --------------------------------------------------------------
# Gradio Interface Theme
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

        block_shadow="*shadow_drop_lg",
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
# Questions Database for HERMES Training System
# --------------------------------------------------------------

# This contains a collection of questions and answers related to
# the HERMES project management methodology.
# These questions are designed by Serge

# The 'questions' list contains dictionaries with the following structure:
# - question_text: The actual question being asked
# - correct_answer: The complete correct answer to the question
# - link: A reference number linking to the relevant section in HERMES documentation


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
# Feedback functions:
# get_link: Retrieves the documentation link form the HERMES manual for a given question
# get_answer: Returns the correct answer for a given question
# summarize: Provides a feedback summary of the question context and answer as a second step feedback
# get_information: Retrieves detailed information for a specific chapter of the HERMES manual
# --------------------------------------------------------------

def get_link_questions(question):
    """
    Retrieves the documentation link associated with a specific question.
    
    Args:
        question (str): The full text of the question to search for
        
    Returns:
        str: The link reference number (e.g., "1.1.1") if found,
             or "Link not found." if the question doesn't exist
    """
    for q in questions:
        if q["question_text"] == question:
            return q["link"]
    return "Link not found."

def get_answer(question):
    """
    Retrieves the correct answer for a given question.
    
    Args:
        question (str): The full text of the question to search for
        
    Returns:
        str: The correct answer text if found,
             or "Question not found." if the question doesn't exist
    """
    for q in questions:
        if q["question_text"] == question:
            return q["correct_answer"]
    return "Question not found."

def get_information(chapter_number):
    """
    Retrieves detailed information for a specific chapter number.
    
    Args:
        chapter_number (str): The chapter reference number (e.g., "1.1.1")
        
    Returns:
        str: The detailed information text for the chapter if found,
             or "Chapter not found" if the chapter doesn't exist
    """
    for entry in reference:
        if entry['chapter'] == chapter_number:
            return entry['information']
    return "Chapter not found"

def summarize(question):
    """
    Creates a comprehensive summary feedback of a question's context and answer.
    
    This function:
    1. Gets the chapter link for the question
    2. Retrieves the detailed information from that chapter
    3. Gets the correct answer that corresponds to the question
    4. Uses GPT-4.o to generate a 4-sentence summary in German that 
    summarizes the key information relevant to answer the question at hand
    
    Args:
        question (str): The question to summarize
        
    Returns:
        str: AI-generated summary combining the correct answer and chapter information
    """
    chapter = get_link_questions(question)
    text = get_information(chapter)
    correct_answer = get_answer(question)
    chat_completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {
                "role": "system", 
                "content": f'''find the correct answer:[{correct_answer}] in the text:[{text}], output the coorect answer: [{correct_answer}] and summarize the text: [{text}] in 4 sentences in German'''
            }
        ],
        temperature = 0.2,
    ).choices[0]
    content = chat_completion.message.content
    return content

# --------------------------------------------------------------
# Determine the correctness of the learners' answers
# --------------------------------------------------------------

class TextMarkers:
    """Constants for text formatting markers"""
    LEFT = ' « '
    RIGHT = ' » '

class Headers:
    """Constants for prompt section headers in German"""
    QUESTION = 'Die Frage lautet wie folgt: '
    ANSWER_TEST = 'Ist die folgende Antwort entweder korrect oder falsch: '
    CORRECT_ANSWER = 'Diese Antwort ist eine korrekte: '
    EVALUATION_PREFIX = (
        'Bitte prüfen Sie die folgende Antwort, indem Sie diese mit '
        'den im Handbuch der Hermes-Methode verwendeten Konzepten und Terminologien vergleichen. '
        'Geben Sie an, ob diese Antwort nach den Standards der Hermes-Methode richtig oder falsch ist, '
        'und erläutern Sie ausführlich die Gründe für die Bewertung. '
        'Konzentrieren Sie sich auf Begriffe wie sie im folgenden Abschnitt der Hermes-Methode definiert sind: '
    )

def clean_hermes_extract(text: str) -> str:
    """
    Cleans and formats the HERMES documentation extract by removing unnecessary whitespace and markers.
    
    Args:
        text (str): Raw text from HERMES documentation
        
    Returns:
        str: Cleaned and formatted text
    """
    replacements = {
        '\n ': '',
        '\n\t': ' ',
        '- ': '',
        '\n': ''
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text

def construct_evaluation_prompt(
    hermes_extract: str,
    correct_answer: str,
    question: str,
    answer_to_test: str,
    markers: TextMarkers
) -> str:
    """
    Constructs the evaluation prompt for the AI model.
    
    Args:
        hermes_extract (str): Cleaned HERMES documentation extract
        correct_answer (str): The known correct answer
        question (str): The question being evaluated
        answer_to_test (str): The learner's answer being evaluated
        markers: Text marker constants
        
    Returns:
        str: Formatted prompt for the AI model
    """
    categorization = (
        f'Bitte klassifiert ein JSON mit key correctness und Wert als entweder:'
        f'{markers.LEFT}correct oder{markers.RIGHT}incorrect'
    )
    
    # Using f-strings for better readability and performance
    return (
        f'{Headers.EVALUATION_PREFIX}{markers.LEFT}{hermes_extract}{markers.RIGHT}'
        f'{Headers.CORRECT_ANSWER}{markers.LEFT}{correct_answer}{markers.RIGHT}'
        f'{Headers.QUESTION}{markers.LEFT}{question}{markers.RIGHT}'
        f'{Headers.ANSWER_TEST}{markers.LEFT}{answer_to_test}{markers.RIGHT}?'
        f'{categorization}'
    )

def get_correctness(question: str, answer: str) -> Optional[str]:
    """
    Evaluates whether a given answer to a HERMES methodology question is correct 
    by comparing it against official HERMES documentation and standards.

    Args:
        question (str): The HERMES methodology question to evaluate
        answer (str): The proposed answer to evaluate for correctness

    Returns:
        str: Either 'correct' or 'incorrect' based on the AI evaluation
        None: If there's an error in processing

    Raises:
        JSONDecodeError: If the AI response cannot be parsed as JSON
        KeyError: If the expected 'correctness' key is missing from the response
    """
    try:
        # Get and process HERMES documentation
        hermes_extract_link = get_link_questions(question)
        hermes_extract = clean_hermes_extract(get_information(hermes_extract_link))
        correct_answer = get_answer(question)
        
        # Construct the evaluation prompt
        prompt = construct_evaluation_prompt(
            hermes_extract=hermes_extract,
            correct_answer=correct_answer,
            question=question,
            answer_to_test=answer,
            markers=TextMarkers
        )
        
        # Make the API call
        chat_completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.2,
            response_format={"type": "json_object"}
        ).choices[0]
        
        # Parse and validate the response
        parsed_data = json.loads(chat_completion.message.content)
        if "correctness" not in parsed_data:
            raise KeyError("Response missing 'correctness' field")
            
        return parsed_data["correctness"]
        
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error processing response: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None



# --------------------------------------------------------------
# Interactive Learning Flow
# --------------------------------------------------------------
# The interaction follows a 3-step learning process:
# 1. First trial: Student attempts the question with a link to relevant docs if incorrect
# 2. Second trial: Student gets another try with a detailed summary as a hint
# 3. Final step: Shows correct answer and comprehensive feedback
# --------------------------------------------------------------

@dataclass
class LearningResponse:
   """Structured response for learning interactions"""
   is_correct: bool
   message: str
   summary: Optional[str] = None
   
class FeedbackMessages:
   """Constants for feedback messages in German"""
   CORRECT = "Deine Antwort ist richtig, gute Arbeit!"
   INCORRECT_WITH_LINK = "Deine Antwort ist falsch, versuche es noch einmal, bitte sieh dir die folgenden Kapitel an: {}"
   INCORRECT_WITH_HINT = "Deine Antwort ist falsch!"

def evaluate_answer(question: str, message: str) -> LearningResponse:
   """
   Evaluates a student's answer and prepares appropriate feedback.
   
   Args:
       question (str): The question being answered
       message (str): Student's answer
       
   Returns:
       LearningResponse: Contains evaluation results and feedback
   """
   correctness = get_correctness(question, message)
   is_correct = "incorrect" not in correctness
   summary = summarize(question) if is_correct else None
   
   return LearningResponse(
       is_correct=is_correct,
       message=FeedbackMessages.CORRECT if is_correct else "",
       summary=summary
   )

def first_trial(
   question: str, 
   message: str, 
   chat_history: List[Tuple[str, str]]
) -> str:
   """
   Handles the first attempt at answering a question.
   
   Args:
       question (str): The question being answered
       message (str): Student's answer
       chat_history: List of previous interactions
       
   Returns:
       str: Feedback message with link to documentation if incorrect
   """
   try:
       response = evaluate_answer(question, message)
       
       if not response.is_correct:
           link = get_link_questions(question)
           return FeedbackMessages.INCORRECT_WITH_LINK.format(link)
           
       return f"{FeedbackMessages.CORRECT} {response.summary}"
       
   except Exception as e:
       print(f"Error in first trial: {str(e)}")
       return "Es ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut."

def second_trial(
   question: str, 
   message: str, 
   chat_history: List[Tuple[str, str]]
) -> str:
   """
   Handles the second attempt at answering a question with more detailed feedback.
   
   Args:
       question (str): The question being answered
       message (str): Student's answer
       chat_history: List of previous interactions
       
   Returns:
       str: Feedback message with comprehensive summary
   """
   try:
       summary = summarize(question)
       response = evaluate_answer(question, message)
       
       if not response.is_correct:
           return f"{FeedbackMessages.INCORRECT_WITH_HINT} {summary}"
           
       return f"{FeedbackMessages.CORRECT} {summary}"
       
   except Exception as e:
       print(f"Error in second trial: {str(e)}")
       return "Es ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut."

def get_final_feedback(question: str) -> str:
   """
   Provides the final feedback with correct answer and comprehensive explanation.
   
   Args:
       question (str): The question being answered
       
   Returns:
       str: Complete feedback with correct answer and explanation
   """
   try:
       answer = get_answer(question)
       summary = summarize(question)
       return f"Die korrekte Antwort lautet: {answer}\n\nErklärung:\n{summary}"
       
   except Exception as e:
       print(f"Error getting final feedback: {str(e)}")
       return "Es ist ein Fehler aufgetreten. Bitte versuchen Sie es später erneut."


# --------------------------------------------------------------
# Interactive Chatbot Interface with Visual Feedback
# --------------------------------------------------------------
# provides a dynamic chatbot interface that updates its appearance
# based on answer correctness:
# - Correct answers trigger a green background (#d8fc9d)
# - Incorrect answers trigger a pink background (#f590af)
# The visual feedback helps learners immediately identify their performance
# --------------------------------------------------------------

def update_chatbot(
   chatbot: "gr.Chatbot",
   question_text: str, 
   msg: str
) -> "gr.Chatbot":
   """
   Updates the chatbot's visual appearance based on answer correctness.
   
   The function evaluates the user's answer and modifies the chatbot's
   background color to provide immediate visual feedback. Green indicates
   a correct answer, while pink indicates an incorrect one.

   Args:
       chatbot (gr.Chatbot): The current Gradio chatbot instance to be updated
       question_text (str): The question that was asked
       msg (str): The user's answer to evaluate

   Returns:
       gr.Chatbot: A new chatbot instance with updated styling based on 
                  answer correctness

   Note:
       The function uses CSS styling to provide visual feedback:
       - Correct answers: Light green background (#d8fc9d)
       - Incorrect answers: Light pink background (#f590af)
   """

   # Define CSS styles for visual feedback
   css = """
   #correct {
       background-color: #d8fc9d;    /* Light green for correct answers */
   }
   #incorrect {
       background-color: #f590af;    /* Light pink for incorrect answers */
   }
   """

   # Evaluate the correctness of the answer
   correctness = get_correctness(question_text, msg)

   # Create new chatbot instance with appropriate styling
   if correctness == 'correct':
       # Configure chatbot with correct answer styling
       chatbot = gr.Chatbot(
           height=300,           # Fixed height for consistent appearance
           label="Feedback",     # Label indicating purpose
           elem_id="correct"     # ID for CSS styling
       )
   elif correctness == 'incorrect':
       # Configure chatbot with incorrect answer styling
       chatbot = gr.Chatbot(
           height=300,           # Fixed height for consistent appearance
           label="Feedback",     # Label indicating purpose
           elem_id="incorrect"   # ID for CSS styling
       )

   return chatbot

# --------------------------------------------------------------
# Chat history handling
# --------------------------------------------------------------


def user(user_message, history):
    return "", history + [[user_message, None]]

def bot(history, messages_history,question,attempt_tracker):
    user_message = history[-1][0]
    bot_message, messages_history, attempt_tracker= handle_response(question, user_message, messages_history,attempt_tracker)
    messages_history += [{"role": "assistant", "content": bot_message}]
    history[-1][1] = bot_message
    time.sleep(1)
    return history, messages_history,attempt_tracker

def init_history(messages_history):
    messages_history = []
    return messages_history

# --------------------------------------------------------------
# HERMES Training System Interface
# Creates a Gradio-based web interface for the HERMES training system
# with visual feedback and authentication
# --------------------------------------------------------------

# Initialize theme and define CSS styling
theme = Theme()

# CSS styles for visual feedback and layout
css = """
   /* Correct answer indicator - green background */
   #correct {
       background-color: #34D640  /* Bright green */
   }
   
   /* Incorrect answer indicator - purple background */
   #incorrect {
       background-color: #ED73FF  /* Light purple */
   }
   
   /* Main heading style */
   h1 {
       color: #2073F7;           /* Bright blue */
       display: block;           /* Full width display */
   }
"""

# Create main interface using Gradio Blocks
with gr.Blocks(theme=theme, css=css) as demo:
   # Header and introduction
   gr.Markdown("## HERMES TRAINING SYSTEM")
   gr.Markdown("Hier ist ein Satz Fragen basierend auf dem Referenzhandbuch der HERMES-Methode.")
   gr.Markdown("Beantworten Sie jede Frage mit Ihren eigenen Worten und drücken Sie die Eingabetaste, um Rückmeldung zu erhalten.")
   
   # Initialize attempt tracking
   attempt_tracker = gr.State({})

   def handle_response(question, message, messages_history, attempt_tracker):
       """Process user responses and manage attempt tracking"""
       # Initialize attempt counter for new questions
       if question not in attempt_tracker:
           attempt_tracker[question] = 0
           
       attempts = attempt_tracker[question]
       
       # Handle different attempt stages
       if attempts == 0:
           # First attempt - provide link to relevant documentation
           bot_message = first_trial(question, message, messages_history)
       else:
           # Subsequent attempts - provide detailed feedback
           bot_message = second_trial(question, message, messages_history)
           messages_history += bot_message
           
       # Increment attempt counter
       attempt_tracker[question] = attempts + 1
       
       return bot_message, messages_history, attempt_tracker

   # Create interface elements for each question
   for index, question in enumerate(questions, start=1):
       with gr.Accordion(f"Frage {index}", open=False):
           with gr.Row():
               # Hidden question text storage
               question_text = gr.Textbox(
                   value=question['question_text'],
                   interactive=False,
                   visible=False
               )
               # User input field
               msg = gr.Textbox(label=question['question_text'])
               
           with gr.Row():
               # Feedback display area
               chatbot = gr.Chatbot(
                   height='300px',
                   label="Feedback"
               )
               # Conversation state tracking
               state = gr.State([])
               
               # Connect interface events
               # Update chatbot appearance based on answer correctness
               msg.submit(
                   fn=update_chatbot,
                   inputs=[chatbot, question_text, msg],
                   outputs=chatbot
               )
               
               # Process user input and generate response
               msg.submit(
                   user,
                   [msg, chatbot],
                   [msg, chatbot],
                   queue=False
               ).then(
                   bot,
                   [chatbot, state, question_text, attempt_tracker],
                   [chatbot, state]
               )

   # Set up authentication
   users = [("Test", "Test")]  # Username/password pair
   
   # Launch the interface with authentication enabled
   demo.launch(auth=users)




