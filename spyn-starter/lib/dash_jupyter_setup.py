import dash
from IPython import display


def show_app(app,  # type: dash.Dash
             port=9999,
             width=900,
             height=600,
             offline=True,
             style=True,
             **dash_flask_kwargs):
    """
    Run the application inside a Jupyter notebook and show an iframe with it
    :param app:
    :param port:
    :param width:
    :param height:
    :param offline:
    :return:
    """
    url = 'http://192.168.2.99:%d' % port
    iframe = '<iframe src="{url}" width={width} height={height}></iframe>' \
             ''.format(
        url=url,
        width=width,
        height=height)
    display.display_html(iframe, raw=True)
    if offline:
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
    if style:
        external_css = [
            "https://fonts.googleapis.com/css?family=Raleway:400,300,600",
            "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-"
            "awesome.min.css",
            "http://getbootstrap.com/dist/css/bootstrap.min.css", ]

        for css in external_css:
            app.css.append_css({"external_url": css})

        external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
                       "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a34"
                       "01de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-"
                       "sachs-report-js.js",
                       "http://getbootstrap.com/dist/js/bootstrap.min.js"]

        for js in external_js:
            app.scripts.append_script({"external_url": js})

    return app.run_server(debug=False,  # needs to be false in Jupyter
                          port=port,
                          host="0.0.0.0",
                          **dash_flask_kwargs)
