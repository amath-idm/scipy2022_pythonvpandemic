'''
Plot a map of all locations where Covasim has been used

Last updated: 2022mar14
'''

import sciris as sc
import pandas as pd
import geopandas
import pylab as pl

do_save = 1
mapping = sc.objdict(dict(equi='EPSG:4326', eckert='ESRI:54012', robinson='ESRI:54030'))
proj = 'robinson'
crs = mapping[proj]

pl.rc('font', family='Proxima Nova') # NB, you probably don't have this font :)

sc.tic()

# Define all countries we want to show on the map
countries = [
'Afghanistan',
'Albania',
'Algeria',
'Angola',
'Argentina',
'Armenia',
'Australia',
'Austria',
'Azerbaijan',
'Bahamas',
'Bangladesh',
'Belarus',
'Belgium',
'Belize',
'Benin',
'Bhutan',
'Bolivia',
'Bosnia and Herz.',
'Botswana',
'Brazil',
'Brunei',
'Bulgaria',
'Burkina Faso',
'Burundi',
'Cambodia',
'Cameroon',
'Canada',
'Central African Rep.',
'Chad',
'Chile',
'China',
'Colombia',
'Congo',
'Costa Rica',
'Croatia',
'Cuba',
'Cyprus',
'Czechia',
"Côte d'Ivoire",
'Dem. Rep. Congo',
'Denmark',
'Djibouti',
'Dominican Rep.',
'Ecuador',
'Egypt',
'El Salvador',
'Eq. Guinea',
'Eritrea',
'Estonia',
'Ethiopia',
'Falkland Is.',
'Fiji',
'Finland',
'Fr. S. Antarctic Lands',
'France',
'Gabon',
'Gambia',
'Georgia',
'Germany',
'Ghana',
'Greece',
'Greenland',
'Guatemala',
'Guinea',
'Guinea-Bissau',
'Guyana',
'Haiti',
'Honduras',
'Hungary',
'Iceland',
'India',
'Indonesia',
'Iran',
'Iraq',
'Ireland',
'Israel',
'Italy',
'Jamaica',
'Japan',
'Jordan',
'Kazakhstan',
'Kenya',
'Kosovo',
'Kuwait',
'Kyrgyzstan',
'Laos',
'Latvia',
'Lebanon',
'Lesotho',
'Liberia',
'Libya',
'Lithuania',
'Luxembourg',
'Macedonia',
'Madagascar',
'Malawi',
'Malaysia',
'Mali',
'Mauritania',
'Mexico',
'Moldova',
'Mongolia',
'Montenegro',
'Morocco',
'Mozambique',
'Myanmar',
'N. Cyprus',
'Namibia',
'Nepal',
'Netherlands',
'New Caledonia',
'New Zealand',
'Nicaragua',
'Niger',
'Nigeria',
'North Korea',
'Norway',
'Oman',
'Pakistan',
'Palestine',
'Panama',
'Papua New Guinea',
'Paraguay',
'Peru',
'Philippines',
'Poland',
'Portugal',
'Puerto Rico',
'Qatar',
'Romania',
'Russia',
'Rwanda',
'S. Sudan',
'Saudi Arabia',
'Senegal',
'Serbia',
'Sierra Leone',
'Slovakia',
'Slovenia',
'Solomon Is.',
'Somalia',
'Somaliland',
'South Africa',
'South Korea',
'Spain',
'Sri Lanka',
'Sudan',
'Suriname',
'Sweden',
'Switzerland',
'Syria',
'Taiwan',
'Tajikistan',
'Tanzania',
'Thailand',
'Timor-Leste',
'Togo',
'Trinidad and Tobago',
'Tunisia',
'Turkey',
'Turkmenistan',
'Uganda',
'Ukraine',
'United Arab Emirates',
'United Kingdom',
'United States of America',
'Uruguay',
'Uzbekistan',
'Vanuatu',
'Venezuela',
'Vietnam',
'W. Sahara',
'Yemen',
'Zambia',
'Zimbabwe',
'eSwatini',
 ]

# Define countries where Covasim has been used (must match the list above)
covasim_used = [
'United Kingdom',
'United States of America',
'Australia',
'Vietnam',
'eSwatini',
'South Africa',
'Kenya',
'Nigeria',
'Russia',
'Canada',
'Nigeria',
'India',
'Italy',
'Denmark',
'Japan',
'Zimbabwe',
'Luxembourg',
'Brazil',
'Nepal',
'Malawi',
'Bangladesh',
'S. Sudan',
'Pakistan',
'Germany',
'China',
'Czechia',
'Sri Lanka',
'Costa Rica',
'Uganda',
]

# Define countries where interest has been shown
covasim_interest = [
'Spain',
'Burkina Faso',
'Papua New Guinea',
'Senegal',
'Ghana',
'Uganda',
'Mozambique',
'Ukraine',
'Peru',
'Zambia',
'Taiwan',
'Dem. Rep. Congo',
'Dominican Republic',
'Thailand',
]

# Define cities to put stars -- must match worldcities.csv
cities = [
'Seattle',
'Portland',
'Oakland',
'Honolulu',
'Boston',
'Toronto',
'Denver',
'New York',
'Thiruvananthapuram',
'Lucknow',
'Dhaka',
'Johannesburg',
'Mbabane',
'Ho Chi Minh City',
'Bergamo',
'London',
'Barcelona',
'Edinburgh',
'Foz do Iguaçu',
'Lagos',
'Ouagadougou',
'Nairobi',
'Brisbane',
'Sydney',
'Melbourne',
'Novosibirsk',
'Copenhagen',
'Yokohama',
'Washington',
'Manaus',
'Harare',
'Kathmandu',
'Blantyre',
'Dhaka',
'Montréal',
'Orlando',
'Islamabad',
'Cologne',
'Luxembourg', # Here to make plotting better; should be after Washington
'New Delhi',
'Xi’an',
'Kolkāta',
'Harare',
'Colombo',
'Kampala',
'Kinshasa',
'Bangkok',
'Santo Domingo',
'Accra',
'San José',
'Prague',
'Singapore',
'Kyiv',
]


print('Loading city data...')
coords = dict()
df = pd.read_csv('worldcities.csv')
invalid = []
for city in cities:
    try:
        row = df.query('city == @city').iloc[0]
        coords[city] = (row['lat'], row['lng']) # Pull out the coordinates of this city
    except IndexError:
        invalid.append(city)
if len(invalid):
    errormsg = f'The following cities were invalid: {sc.strjoin(invalid)}'
    raise IndexError(errormsg)
citydf = pd.DataFrame.from_dict(coords, orient='index')
lats = citydf[1].values # Latitude
lngs = citydf[0].values # Longitude
cities = geopandas.GeoDataFrame(citydf, geometry=geopandas.points_from_xy(lats, lngs))
cities = cities.set_crs(mapping.equi)

print('Loading world data...')
world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres')) # Load the world
world = world[(world.pop_est>0) & (world.name!="Antarctica")] # Load all locations with population and exclude Antarctica
world['value'] = 0.0 # Set to default color
for index, row in world.iterrows():
    if row['name'] in covasim_used:
        world.at[index, 'value'] = 1.0 # Set countries where Covasim has been used to the maximum value
    elif row['name'] in covasim_interest:
        world.at[index, 'value'] = 0.5 # Set countries where Covasim has interest to an intermediate value

print('Changing projection...')
world  = world.to_crs(crs)
cities = cities.to_crs(crs)

print('Plotting...')
watercolor = 0.8*sc.cat(0.83,0.92,0.99)
fig = pl.figure(figsize=(12,5.8), dpi=300, facecolor=watercolor) # Create the figure
use_sns = False
if use_sns:
    import seaborn as sns; sns
    cmap = 'flare_r'
else:
    import matplotlib.colors as mplc
    data = [
        [0.8, 0.8, 0.8, 1],
        [0.4, 0.7, 0.5, 1],
        [0.1, 0.5, 0.3, 1],
    ]
    cmap = mplc.LinearSegmentedColormap.from_list('worldcmap', data)
ax = fig.add_axes([-0.10, 0.0, 1.20, 1.00]) # Add the axes -- whole figure
pl.axis('off')

# Plot the world
world.plot(ax=ax, column='value', edgecolor=[1.0]*3, linewidth=0.5, cmap=cmap); # Plot everything (except the cities)

# Plot the cities
cities.plot(ax=ax, c='gold', edgecolor='k', marker='*', markersize=60, linewidth=0.9, label='Collaborators')

# Create the legend
colors = sc.vectocolor([0,1.0,0.5], cmap=cmap) # Pick colors
for col,label in zip(colors, [None, 'Covasim in use', 'Project scoping stage']): # Create the legend
    pl.fill_between([0,0], [0,0], [0,0], facecolor=col, label=label)
pl.legend(bbox_to_anchor=(0.25,0.2), frameon=0)
x0,x1 = ax.get_xlim()
y0,y1 = ax.get_ylim()
fx0 = 1.0
fx1 = 1.0
fy0 = 1.0
fy1 = 1.0
ax.set_xlim(x0*fx0, x1*fx1)
ax.set_ylim(y0*fy0, y1*fy1)

# Tidy up
if do_save:
    for ext in ['png', 'svg']:
        name = f'worldmap_covasim.{ext}'
        sc.savefig(name, dpi=300)
sc.toc()
pl.show()
