from __future__ import division
from __future__ import print_function

import plotly.graph_objs as go
from plotly.offline import plot

from cea.plots.variable_naming import LOGO, COLOR, NAMING


def energy_use_intensity(data_frame, analysis_fields, title, output_path):
    # CREATE FIRST PAGE WITH TIMESERIES
    traces = []
    area = data_frame["GFA_m2"]
    x = ["Absolute [MWh/yr]", "Relative [kWh/m2.yr]"]
    for field in analysis_fields:
        name = NAMING[field]
        y = [data_frame[field], data_frame[field] / area * 1000]
        trace = go.Bar(x=x, y=y, name=name,
                       marker=dict(color=COLOR[field]))
        traces.append(trace)

    layout = go.Layout(images=LOGO, title=title, barmode='stack', showlegend=True)
    fig = go.Figure(data=traces, layout=layout)
    plot(fig, auto_open=False, filename=output_path)

    return {'data': traces, 'layout': layout}

def energy_use_intensity_district(data_frame, analysis_fields, title, output_path):
    traces = []
    data_frame_copy = data_frame.copy()# make a copy to avoid passing new data of the dataframe around the class
    for field in analysis_fields:
        data_frame_copy[field] = data_frame_copy[field] * 1000 / data_frame_copy["GFA_m2"]  # in kWh/m2y
        data_frame_copy['total'] = data_frame_copy[analysis_fields].sum(axis=1)
        data_frame_copy = data_frame_copy.sort_values(by='total', ascending=False)  # this will get the maximum value to the left
    x = data_frame_copy["Name"].tolist()
    for field in analysis_fields:
        y = data_frame_copy[field]
        name = NAMING[field]
        trace = go.Bar(x=x, y=y, name=name, marker=dict(color=COLOR[field]))
        traces.append(trace)

    layout = go.Layout(images=LOGO, title=title, barmode='stack', yaxis=dict(title='Energy Use Intensity [kWh/m2.yr]'),
                       showlegend=True)
    fig = go.Figure(data=traces, layout=layout)
    plot(fig, auto_open=False, filename=output_path)

    return {'data': traces, 'layout': layout}
