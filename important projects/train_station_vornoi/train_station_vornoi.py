import numpy as np
from geovoronoi import voronoi_regions_from_coords, coords_to_points
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
from shapely.geometry import shape
from shapely.ops import transform
import fiona
import pyproj
import xlrd
import matplotlib.pyplot as plt
import geopandas as gpd


DATA_RANGE = (12, 500) # row numbers of the train station data
X_COL = "B" # the excel collumn letter corresponding to the X coordinate
Y_COL = "C"
STATION_COLS = {"x": "F", "y": "G", "name": "D", "category": ""}
STATION_CATEGORY_COL = "G"



class TrainVornoi():
    def __init__(self):
        pass
    
    def column_to_number(self, col): # char of colum name, only defined from A to ZZ
        col = col.upper() # make all chars uppercase
        
        if len(col) == 1:
            return ord(col) - 65 # ord returns the ascii value which has an offset of 65

        elif len(col) == 2:
            value = (26 * (ord(col[0])-64)) + (ord(col[1])-65) # first char is like offset of 26 columns
            # A means zero as the second char, but as the first char it stands for + 1*26, so we need to subtract only 64
            return value
        
        return -1 # if column name is too long, return -1

    def import_data(self, geoJson_path, excel_path, x_col, y_col, data_range, sheet_no=0):
        with fiona.open(geoJson_path) as f:
            #src_crs = pyproj.CRS.from_dict(f.meta['crs'])
            #target_crs = pyproj.CRS.from_epsg(3395)         # World Mercator CRS
            #print('source CRS:', src_crs)
            #print('target CRS:', target_crs)
            #crs_transformer = pyproj.Transformer.from_crs(src_crs, target_crs)
            self.area_shape = shape(f[0]['geometry'])
            # note that we also apply ".buffer(0)", otherwise the shape is not valid
            # see https://shapely.readthedocs.io/en/stable/manual.html#object.buffer on the "buffer(0)" trick
            #self.area_shape = transform(crs_transformer.transform, self.area_shape).buffer(0)

        with xlrd.open_workbook(excel_path) as book:
            sh = book.sheet_by_index(sheet_no)
            temp = []
            # list with station name, category and coordinates
            self.station_header = {}
            self.station_list = []

            
            for i in range(data_range[0], data_range[1]):

                name = sh.cell_value
                x = str(sh.cell_value(rowx=i, colx=self.column_to_number(x_col)))
                y = str(sh.cell_value(rowx=i, colx=self.column_to_number(y_col)))
                x = x.replace(",", ".")
                y = y.replace(",", ".")

                # for some reason, i have to order the coords (y,x) instead of expected (x, y), but im too lazy to find out where it mixes both up...
                self.stationlist.append((float(x), float(y)))

            
            tmp_coords = np.array(temp)
                    

            self.coords = [p for p in coords_to_points(tmp_coords) if p.within(self.area_shape)]  # converts to shapely Point and removes points outside of shape (mainly basel bad bf)

        

    def generate_vornoi(self):
        if self.area_shape is None or self.coords is None:
            print("shape or station coords not defined")
            return

        print("generating vornoi")
        self.region_polys, self.region_pts = voronoi_regions_from_coords(self.coords, self.area_shape)
        print("voronoi ready")

    def show_vornoi(self):
        fig, ax = subplot_for_map()

        plot_voronoi_polys_with_points_in_area(ax, self.area_shape, self.region_polys, self.coords, self.region_pts)
        # add point_labels later!

        ax.set_title("Vornoi Regions of train stations")

        plt.tight_layout()
        plt.show()

myTrainVornoi = TrainVornoi()

myTrainVornoi.import_data("/home/yannick/git-repos/MyPython/important projects/train_station_vornoi/deutschlandGeoJSON-main/1_deutschland/2_hoch.geo.json", "/home/yannick/git-repos/MyPython/important projects/train_station_vornoi/D_Bahnhof_2020_alle.xls", "F", "G", (2, 1000))

myTrainVornoi.generate_vornoi()

myTrainVornoi.show_vornoi()