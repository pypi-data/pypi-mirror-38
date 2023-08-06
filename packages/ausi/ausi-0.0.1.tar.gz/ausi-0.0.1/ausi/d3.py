import pandas as pd
import json
import os
import numpy as np
from matplotlib import cm
from matplotlib.colors import rgb2hex
import pkg_resources


def create_json_for_semantic_substract(df, key_to_groupby, json_output_file):
    imports = df.groupby('from').to.agg(list)
    imports.index.name = "name"
    imports.name = "imports"

    json_data = json.loads(imports.to_json(orient='table'))['data']

    with open(json_output_file, mode='w') as json_file:
        json_file.write(json.dumps(json_data, indent=3).replace("null", ""))

    print("JSON file produced in '{}'".format(os.path.abspath(json_output_file)))


def create_json_for_zoomable_circle_packing(
        plot_data,
        column_to_color_name,
        join_color_column_name,
        hierarchy_column_name,
        hierarchy_column_name_separator,
        size_column_name,
        value_column_name,
        output_file_name_prefix,
        color_column_name='color'):
    # create unique colors per values in column
    colored_column = plot_data[[column_to_color_name]].drop_duplicates()
    # shuffle names to color because otherwise the colors for subsequent data would be too similar
    colored_column = colored_column.sample(frac=1, random_state=0)
    rgb_colors = [rgb2hex(x) for x in cm.Spectral(np.linspace(0, 1, len(colored_column)))]
    colored_column[color_column_name] = rgb_colors

    temp_color_column_name = '_XXX' + color_column_name
    # add colored column to plot_data
    colored_plot_data = pd.merge(
        plot_data, colored_column,
        left_on=join_color_column_name,
        right_on=column_to_color_name,
        how='left',
        suffixes=['', temp_color_column_name])
    colored_plot_data.loc[colored_plot_data[column_to_color_name] == 'None', color_column_name] = "white"
    colored_plot_data.rename(columns={ temp_color_column_name : "gen_color_code"})
    colored_plot_data.head()

    json_data = {'name': 'flare', 'children': []}

    for row in colored_plot_data.iterrows():
        series = row[1]
        path, filename = os.path.split(series[hierarchy_column_name])

        last_children = None
        children = json_data['children']

        for path_part in path.split(hierarchy_column_name_separator):
            entry = None

            for child in children:
                if "name" in child and child["name"] == path_part:
                    entry = child
            if not entry:
                entry = {}
                children.append(entry)

            entry['name'] = path_part
            if not 'children' in entry:
                entry['children'] = []

            children = entry['children']
            last_children = children

        last_children.append({
            'name': filename + " [" + series[join_color_column_name] + ", " + "{:6.2f}".format(
                series[value_column_name]) + "]",
            'ratio': series[value_column_name],
            'size': series[size_column_name],
            'color': series[color_column_name]})

    json_file_name = output_file_name_prefix + ".json"
    with open(json_file_name, mode='w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(json_data, indent=3))

    print("JSON file produced in '{}'".format(os.path.abspath(json_file_name)))

    resource_package = __name__
    resource_path = '/'.join(('d3_templates', 'zoomable_circle_package', 'template.html'))
    template = pkg_resources.resource_string(resource_package, resource_path)
    html_file = output_file_name_prefix + ".html"
    with open(html_file, mode='w', encoding='utf-8') as d3_file:
        html_as_string = template.decode("utf-8")
        html_as_string = html_as_string.replace("FLARE_JSON_FILE", json_file_name)
        d3_file.write(html_as_string)

    print("HTML file produced in '{}'".format(os.path.abspath(html_file)))
