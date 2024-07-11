from flask import Flask, request, jsonify
import argostranslate.package
import argostranslate.translate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/translate", methods=["POST"])
def translate():
    from_code = request.json['from_lang']
    to_code = request.json['to_lang']

    # Download and install Argos Translate package
    argostranslate.package.update_package_index()
    available_packages = argostranslate.package.get_available_packages()
    package_to_install = next(
        filter(
            lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
        )
    )
    argostranslate.package.install_from_path(package_to_install.download())
    text_to_translate = request.json["text"]
    # Translate
    translatedText = argostranslate.translate.translate(text_to_translate, from_code, to_code)
    return {"translation" : translatedText}