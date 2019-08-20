from app import creat_app

app = creat_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=81, threaded=True)



