import pandas as pd
import pygal


def create_xy_chart(df, group_key, x="x", y="y"):

	plot_data = pd.DataFrame(index=df[group_key])
	plot_data['value'] = tuple(zip(df[x], df[y]))
	plot_data['label'] = df.index
	plot_data['data'] = plot_data[['label', 'value']].to_dict('records')
	plot_dict = plot_data.groupby(plot_data.index).data.apply(list)

	xy_chart = pygal.XY(stroke=False)
	[xy_chart.add(entry[0], entry[1]) for entry in plot_dict.iteritems()]
	return xy_chart