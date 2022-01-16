import flask
import folder_size

app = flask.Flask("folder size app")

@app.route('/')
def get_size():
	if "path" in flask.request.args:
		return folder_size.get_folder_size(flask.request.args["path"])
	else:
		return '<b style="color:red">Specify `path` parameter</b>'

if __name__ == '__main__':
	app.run(host='localhost', port='81')
