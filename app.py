### Libraries and Initialization
import os
from flask import Flask, render_template, request, abort

app = Flask(__name__)

# declaration of dicts, move to DB?
ARTICLES = {
    'vaccine-brand': {
        'name':     'Pfizer or Moderna or AZ?',
        'category': 'Vaccinations',
        'content':  """All these brand names can be confusing. We're here to help.

                       If you're in the process of deciding whether or not to get a vaccine, the choices seem to loom large. In the end, all that matters is that you protect yourself and your family. Vaccination for those who are not allergic is one of most effective ways to increase herd immunity.
                    """,
    },
    'diabetic-treatment': {
        'name': 'How do I get insulin without an in-person visit?',
        'category': 'Pre-existing Conditions',
        'content': "Diabetes.",
    },
    'testing-accuracy': {
        'name': 'What\'s a false positive? What about false negatives?',
        'category': 'Testing',
        'content': "something something",
    },
    'being-an-ally': {
        'name': 'My friend seems less active since the start of the pandemic...',
        'category': 'Mental Health',
        'content': "another thing to expand upon",
    },
    'managing-chronic-pain': {
        'name': 'I have chronic pain, and covid interrupted treatment.',
        'category': 'Pre-existing Conditions',
        'content': "See https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7566302/",
    },
}

PROFILES = [
    {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'password1234',
        'is_doctor': False,
        'specialty': ['diabetes', 'high blood pressure', 'amnesia']
    },
    {
        'first_name': 'Ebenezer',
        'last_name': 'Scrooge',
        'email': 'ebenezer@richerthanthou.com',
        'password': '$$$$$$$$$$$',
        'is_doctor': False,
        'specialty': ['hypothermia', 'time_perception', 'smoking', 'narcissism']
    },
    {
        'first_name': 'Yoda',
        'last_name': 'Whoneedsalastname',
        'email': 'yoda@usetheforce.com',
        'password': 'there_is_no_try',
        'is_doctor': False,
        'specialty': ['aphasia', 'smoking', 'violence']
    },
    {
        'first_name': 'Belle',
        'last_name': 'Whoneedsalastname',
        'email': 'beautyisonlyskindeep@bodypositivity.com',
        'password': '<3Beast',
        'is_doctor': False,
        'specialty': ['stockholm', 'amnesia', 'narcissism']
    },

    {
        'first_name': 'Doctor',
        'last_name': 'Who',
        'email': 'abluebritishbox@tardis.uk',
        'password': 'superSecure',
        'is_doctor': True,
        'credentials': "",
        'specialty': ['violence', 'narcissism', 'time_perception']
    },
    {
        'first_name': 'Victor',
        'last_name': 'Frankenstein',
        'email': 'notamonster@exonerateme.org',
        'password': 'halloween-is-overrated!',
        'is_doctor': False,
        'credentials': "",
        'specialty': ['amnesia', 'smoking', 'hypothermia']
    }
]

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.svg', mimetype='image/vnd.microsoft.icon')


# handles errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # direct 500 error, such as abort(500)
        return render_template("500.html"), 500

    # wrapped unhandled error
    return render_template("500_unhandled.html", e=original), 500


# sanity check: homepage only extends the navbar
@app.route('/')
@app.route('/home/')
def home():
    return render_template('home.html', webpage_title='Home')

# slightly more complicated
@app.route('/profile/')
@app.route('/profile/<user>')
def view_user(user=None):
    user = user or "World"
    return render_template('profile.html', user=user)

# uses the dictionary to list out the articles
@app.route('/article/')
def list_articles():
    return render_template('index.html', webpage_title='Articles', display_dict=ARTICLES)

# each article has its own webpage
@app.route('/article/<article_title>')
def show_article(article_title=None):
    article = ARTICLES.get(article_title)
    if not article:
        abort(404)
    else:
        return render_template('article.html', article=article)

# serves the videochat page
@app.route('/videochat')
def start_videochat():
    return render_template('videochat.html', webpage_title='Video')

# boilerplate for privacy and terms
@app.route('/privacy/')
def privacy():
    return render_template('privacy.html', webpage_title='Privacy Policy')

@app.route('/terms/')
def terms():
    return render_template('terms.html', webpage_title='Terms and Conditions')
