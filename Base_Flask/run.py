# Imports
from flask import Flask
import views#, forms

main_app = views.app

if __name__ == '__main__':
    main_app.run(debug=True, port=2745) 