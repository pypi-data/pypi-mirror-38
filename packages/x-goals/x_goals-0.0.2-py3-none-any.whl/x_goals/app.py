import base64
from io import BytesIO
import os
from IPython import display
import dash_html_components as html
import dash_core_components as dcc
import dash
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
from x_goals import state
from x_goals import pricing_engine as pe


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
host = 'localhost'
port = 8889

dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash_app.config.supress_callback_exceptions = True
dash_app.title = "XGoals Odds Calculator"
paramstates_home = state.ParamStates({'corners': state.SingleParamState(10),
                                      'shotson': state.SingleParamState(6),
                                      'cards': state.SingleParamState(3)})
paramstates_away = state.ParamStates({'corners': state.SingleParamState(10),
                                      'shotson': state.SingleParamState(6),
                                      'cards': state.SingleParamState(3)})


def show_app(app, port=port, width=700, height=350, offline=False, in_binder=None):

    in_binder = 'JUPYTERHUB_SERVICE_PREFIX' in os.environ if in_binder is None else in_binder
    if in_binder:
        base_prefix = '{}proxy/{}/'.format(os.environ['JUPYTERHUB_SERVICE_PREFIX'], port)
        url = 'https://hub.mybinder.org{}'.format(base_prefix)
        app.config.requests_pathname_prefix = base_prefix
    else:
        url = 'http://localhost:%d' % port

    iframe = '<a href="{url}" target="_new">Open in new window</a><hr><iframe src="{url}" ' \
             'width={width} height={height}></iframe>'.format(url=url, width=width, height=height)

    display.display_html(iframe, raw=True)
    if offline:
        app.css.config.serve_locally = True
        app.scripts.config.serve_locally = True
    return app.run_server(debug=False, host=host, port=port)  # False for Jupyter


def fig_to_uri(in_fig, close_all=True, **save_args):

    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)


def _slider_section(var, home_away):

    half_max = 10
    marks = {2 * i: 2 * i for i in range(half_max)}
    if var == 'cards':
        half_max = 5
        marks = {i: i for i in range(2 * half_max)}

    return html.Div([
        dcc.Slider(
            id='{}-slider-{}'.format(var, home_away), min=0, max=2 * half_max, step=0.5,
            value=half_max, marks=marks,),
    ], className="five columns")


def _html_section(variable):

    var = variable.lower()
    section = [html.Div([
        html.Div([html.H5(var.capitalize(), style={'textAlign': 'left', 'color': 'green'})],
                 className="six columns"),
        html.Div([html.H5(var.capitalize(), style={'textAlign': 'left', 'color': 'red'})],
                 className="six columns")],
        className="row"),
        _slider_section(var, 'home'),
        _slider_section(var, 'away'),
        html.Div(html.Img(id='{}-plot-container-home'.format(var), src='',
                          style={'width': '400px'}), className="five columns"),
        html.Div(html.Img(id='{}-plot-container-away'.format(var), src='',
                          style={'width': '400px'}), className="five columns"),
    ]
    return section


dash_app.layout = html.Div([
    html.Button('Description', n_clicks=0, id='my-button'),
    html.Div(id='my-button-output'),
    html.Div([
        html.Div([html.H3('Home Team ', style={'marginBottom': 10, 'marginTop': 10})], className="six columns"),
        html.Div([html.H3('Away Team')], className="six columns")
    ], className="row"),
    *_html_section('corners'),
    *_html_section('shotson'),
    *_html_section('cards'),
    html.Div(className="row"),
    html.Div([html.Div([html.H3('Probabilities (Odds)', style={'textAlign': 'center', 'color': 'orange'}),
                        ], className="row")
              ]),
    html.Div(id='odds-container', className="row")
])


@dash_app.callback(Output('my-button-output', 'children'), [Input('my-button', 'n_clicks')])
def on_click(n_clicks):
    if n_clicks % 2 == 1:
        return html.Div(
            [html.P("XGoals uses the weighting approach of 0.15 (corners), 0.2 (shots on) and -0.15 (cards)."),
             html.P("The trader enters the expected values for each variable using the slider. "
                    "The values for corners and cards may be found using sportingindex.com"),
             html.P("The slider moves in steps of size 0.5. The distribution plot updates for each "
                    "move of the slider, as does the probabilities/odds which are 100% lines."),
             html.P("Cards increases by 1 for a player's first yellow card, and by 2.5 for a second yellow "
                    "or a red (motivated by sportingindex.com weightings)."),
             html.P("Currently corners and shots on are modelled using the normal distribution, with 95% of "
                    "values lying in the range [0, 2 times the expected value]; this means the spread is set "
                    "to be half the expected value (this is motivated by historical behaviour for teams over "
                    "a whole season, and clearly that's not going to be ideal as it doesn't account for the "
                    "strength of the opposition properly. Don't judge too harshly as this is just Version 1!). "
                    "The distribution for the cards follows a Poisson distribution."),
             ])


for var in ['corners', 'shotson', 'cards']:
    for home_away in ['home', 'away']:
        @dash_app.callback(dash.dependencies.Output(component_id='{}-plot-container-{}'.format(var, home_away),
                                                    component_property='src'),
                           [dash.dependencies.Input('{}-slider-{}'.format(var, home_away), 'value')])
        def update_graph(value, var=var):
            return fig_to_uri(pe.attrib_distplot(var, state.SingleParamState(value, value / 2)))


@dash_app.callback(Output('odds-container', 'children'),
                   [Input('corners-slider-home', 'value'), Input('corners-slider-away', 'value'),
                    Input('shotson-slider-home', 'value'), Input('shotson-slider-away', 'value'),
                    Input('cards-slider-home', 'value'), Input('cards-slider-away', 'value')])
def update_output(corners_home, corners_away, shotson_home, shotson_away, cards_home, cards_away):
    paramstates_home.corners = state.SingleParamState(corners_home)
    paramstates_home.shotson = state.SingleParamState(shotson_home)
    paramstates_home.cards = state.SingleParamState(cards_home)

    paramstates_away.corners = state.SingleParamState(corners_away)
    paramstates_away.shotson = state.SingleParamState(shotson_away)
    paramstates_away.cards = state.SingleParamState(cards_away)
    prices = pe.price_match_V1(paramstates_home, paramstates_away, 50000)
    return html.Div([html.Div([html.H5('Home {:.3g} ({:.2g})'.format(1 / prices[0], prices[0]),
                                       style={'textAlign': 'left', 'color': 'green'}),
                               ], className="four columns"),
                     html.Div([html.H5('Draw {:.3g} ({:.2g})'.format(1 / prices[1], prices[1]),
                                       style={'textAlign': 'center', 'color': 'black'}),
                               ], className="four columns"),
                     html.Div([html.H5('Away {:.3g} ({:.2g})'.format(1 / prices[2], prices[2]),
                                       style={'textAlign': 'right', 'color': 'red'}),
                               ], className="four columns")
                     ])


if __name__ == "__main__":
    show_app(dash_app)
