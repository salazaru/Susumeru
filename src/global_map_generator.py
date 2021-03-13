import json
import country_converter as coco
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def print_map(users_by_country, region):
    '''This function takes in a dataframe with integers indexed by the iso-2 country codes. It then 
    generates a heatmap based on the magnitude of the integer passed for each country. In this case,
    the number is the number of users of MAL in each country. Plots of different regions can be created
    by passing a string with a continent name. 

    :param users_by_country: dataframe with integers indexed by the iso-2 country codes
    :type users_by_country: dataframe
    :param region: A string that corresponds to continent and 'world' for the entire planet
                    (except Antarctica)
    :type region: str
    '''
    
    # Setting the path to the shapefile
    SHAPEFILE = 'shapedata/ne_10m_admin_0_countries.shp'

    # Read shapefile using Geopandas
    geo_df = gpd.read_file(SHAPEFILE)[['ADMIN', 'ADM0_A3', 'geometry']]

    # Rename columns.
    geo_df.columns = ['country', 'country_code', 'geometry']
    geo_df.head(3)

    # Drop row for 'Antarctica'. It takes a lot of space in the map and is not of much use
    geo_df = geo_df.drop(geo_df.loc[geo_df['country'] == 'Antarctica'].index)
    geo_df = geo_df.to_crs('EPSG:3395')

    # Print the map
    geo_df.plot(figsize=(20, 20), edgecolor='white',
                linewidth=1, color='lightblue')

    # Next, we need to ensure that our data matches with the country codes.
    iso3_codes = geo_df['country'].to_list()

    # Convert to iso2_codes
    iso2_codes_list = coco.convert(names=iso3_codes, to='ISO2', not_found='NULL')

    # Add the list with iso2 codes to the dataframe
    geo_df['iso2_code'] = iso2_codes_list

    # There are some countries for which the converter could not find a country code.
    # We will drop these countries.
    geo_df = geo_df.drop(geo_df.loc[geo_df['iso2_code'] == 'NULL'].index)

    # Set the index of the geographic data to the country code
    new_geo_df = geo_df.set_index('iso2_code')

    # Merge the dataframes
    df = new_geo_df.join(number_user_list, how='outer')

    # Clean up the file a bit
    df['number of users'].fillna(0, inplace=True)
    df.head(3)
    

    def print_world_map():
        # Print the map
        # Set the range for the choropleth
        title = 'My Anime List Users by Country'
        col = 'number of users'
        source = 'MAL Dataset. ECE 143 Team 3'
        vmin = df[col].min()
        vmax = df[col].max()
        cmap = 'YlGnBu'

        # Create figure and axes for Matplotlib
        fig, ax = plt.subplots(1, figsize=(20, 8))

        # Remove the axis
        ax.axis('off')
        df.plot(column=col, ax=ax, edgecolor='0.8', linewidth=1, cmap=cmap)

        # Add a title
        ax.set_title(title, fontdict={'fontsize': '25', 'fontweight': '3'})

        # Create an annotation for the data source
        ax.annotate(source, xy=(0.5, .08), xycoords='figure fraction', horizontalalignment='left',
                    verticalalignment='bottom', fontsize=10)

        # Create colorbar as a legend
        sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax), cmap=cmap)

        # Empty array for the data range
        sm._A = []

        # Add the colorbar to the figure
        cbaxes = fig.add_axes([0.25, 0.25, 0.01, 0.4])
        cbar = fig.colorbar(sm, cax=cbaxes)
        cbar.ax.tick_params(labelsize=15)
        
        fig.savefig('world_map.png', dpi=300)


    def print_continent(region):
        # Other regions.
        country_list = get_countries_in_continent(region)

        map_df = df.loc[country_list]
        
        if region == 'Asia' or region == 'Oceania':
            map_df = map_df.to_crs('EPSG:8859')

        
        title = 'MAL Users in ' + region
        col = 'number of users'
        source = 'MAL Dataset. ECE 143 Team 3'
        vmin = map_df[col].min()
        vmax = map_df[col].max()
        cmap = 'YlGnBu'
        fig, ax = plt.subplots(1, figsize=(20, 9))
        ax.axis('off')
        map_df.plot(column=col, ax=ax, edgecolor='0.8', linewidth=1, cmap=cmap)
        ax.set_title(title, fontdict={'fontsize': '25', 'fontweight': '3'})
        ax.annotate(source, xy=(0.5, .08), xycoords='figure fraction',
                    horizontalalignment='left',
                    verticalalignment='bottom', fontsize=10)
        sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax), cmap=cmap)
        
        if region == 'Asia':
            cbaxes = fig.add_axes([0.25, 0.25, 0.01, 0.5])
        if region == 'Oceania':
            cbaxes = fig.add_axes([0.18, 0.25, 0.01, 0.5])
        if region == 'Africa':
            cbaxes = fig.add_axes([0.35, 0.25, 0.01, 0.5])
        if region == 'North America':
            cbaxes = fig.add_axes([0.3, 0.25, 0.01, 0.5])
            ax.set_xlim(-2*10000000, 0*10000000)
            ax.set_ylim(0*10000000, 2*10000000)
        if region == 'Europe':
            ax.set_xlim(-0.15*10000000, 0.6*10000000)
            ax.set_ylim(0.1*10000000, 1.1*10000000)
            cbaxes = fig.add_axes([0.35, 0.25, 0.01, 0.5])
        if region == 'South America':
            cbaxes = fig.add_axes([0.35, 0.25, 0.01, 0.5])
        
        
        
        cbar = fig.colorbar(sm, cax=cbaxes)
        cbar.ax.tick_params(labelsize=15)
        
        fig.savefig(region + '_map.png', dpi=300)


    def get_countries_in_continent(continent):

        assert isinstance(continent, str)

        countries = {'Asia': ['AF', 'AZ', 'BH', 'BD', 'AM', 'BT', 'IO', 'BN', 'MM', 'KH', 'LK', 'CN',
                            'TW', 'CY', 'GE', 'PS', 'HK', 'IN', 'ID', 'IR', 'IQ', 'IL',
                            'JP', 'KZ', 'JO', 'KP', 'KR', 'KW', 'KG', 'LA', 'LB', 'MO', 'MY', 'MV',
                            'MN', 'OM', 'NP', 'PK', 'PH', 'TL', 'QA', 'RU', 'SA', 'SG', 'VN', 'SY',
                            'TJ', 'TH', 'AE', 'TR', 'TM', 'UZ', 'YE'],
                    'Oceania': ['AS', 'AU', 'SB', 'CK', 'FJ', 'PF', 'KI', 'GU', 'NR', 'NC', 'VU',
                                'NZ', 'NU', 'NF', 'MP', 'UM', 'FM', 'MH', 'PW', 'PG', 'PN',
                                'TO', 'TV', 'WF', 'WS'],
                    'Europe': ['AL', 'AD', 'AZ', 'AT', 'AM', 'BE', 'BA', 'BG', 'BY', 'HR', 'CY',
                                'CZ', 'DK', 'EE', 'FO', 'FI', 'AX', 'FR', 'GE', 'DE', 'GI', 'GR',
                                'VA', 'HU', 'IS', 'IE', 'IT', 'KZ', 'LV', 'LI', 'LT', 'LU', 'MT',
                                'MC', 'MD', 'ME', 'NL', 'NO', 'PL', 'PT', 'RO', 'RU', 'SM', 'RS',
                                'SK', 'SI', 'ES', 'SE', 'CH', 'TR', 'UA', 'MK', 'GB', 'GG',
                                'JE', 'IM'],
                    'North America': ['AG', 'BS', 'BB', 'BM', 'BZ', 'VG', 'CA', 'KY', 'CR', 'CU',
                                    'DM', 'DO', 'SV', 'GL', 'GD', 'GT', 'HT', 'HN', 'JM',
                                    'MQ', 'MX', 'MS', 'CW', 'AW', 'SX', 'NI', 'UM',
                                    'PA', 'PR', 'BL', 'KN', 'AI', 'LC', 'MF', 'PM', 'VC', 'TT',
                                    'TC', 'US', 'VI'],
                    'South America': ['AR', 'BO', 'BR', 'CL', 'CO', 'EC', 'FK', 'GY', 'PY',
                                    'PE', 'SR', 'UY', 'VE'],
                    'Africa': ['ZM', 'BF', 'TZ', 'EG', 'UG', 'TN', 'TG', 'SZ', 'SD',
                                'EH', 'SS', 'ZW', 'ZA', 'SO', 'SL', 'SC', 'SN', 'ST',
                                'SH', 'RW', 'GW', 'NG', 'NE', 'NA', 'MZ', 'MA',
                                'MU', 'MR', 'ML', 'MW', 'MG', 'LY', 'LR', 'LS', 'KE',
                                'CI', 'GN', 'GH', 'GM', 'GA', 'DJ', 'ER', 'ET', 'GQ',
                                'BJ', 'CD', 'CG', 'KM', 'TD', 'CF', 'CV', 'CM',
                                'BI', 'BW', 'AO', 'DZ']}
        
        return countries[continent]
    
    if region == 'World':
        print_world_map()
    else:
        print_continent(region)


# Getting the user location data.
location_data = pd.read_csv('users_with_country.csv', index_col=0)['countries']
users_by_country = {category: list(location_data).count(
    category) for category in pd.Categorical(location_data).categories}

number_user_list = pd.DataFrame.from_dict(
    users_by_country, orient='index', columns=['number of users'])

print_map(users_by_country, 'Africa')