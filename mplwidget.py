import pandas
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from datetime import datetime, timedelta
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT
from matplotlib.figure import Figure

class MplWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.x = None
        self.y = None

        self.canvas = FigureCanvas(Figure(figsize=(4,4)))
        self.vertical_layout = QVBoxLayout()
        self.vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)

        # Create a QHBoxLayout for the toolbar, spin box, and combo box
        toolbar_layout = QHBoxLayout()

        # Navigation toolbar
        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        toolbar_layout.addWidget(self.toolbar)

        # Combo box
        self.combo_box = QComboBox()
        self.combo_box.addItems(['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'])
        self.combo_box.activated.connect(self.on_cmap_changed)  # Connect the activated signal
        self.combo_box.highlighted.connect(self.on_cmap_hovered)  # Connect the highlighted signal
        toolbar_layout.addWidget(self.combo_box)

        # Spin box
        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(0)
        self.spin_box.setMaximum(10)
        self.spin_box.valueChanged.connect(self.on_point_size_changed)  # Connect the valueChanged signal
        toolbar_layout.addWidget(self.spin_box)

        # Add the toolbar layout to the main vertical layout
        self.vertical_layout.addLayout(toolbar_layout)

        self.point_size = 1.5

        self.setLayout(self.vertical_layout)
    def plotG(self, x, y, cmap='viridis'):
        s = self.point_size
        self.cmap = cmap
        self.canvas.axes.clear()
        self.canvas.axes.scatter(x, y, s=s, c=range(len(x)), cmap=self.cmap)
        self.canvas.axes.set_yscale("log")

        self.canvas.axes.grid(True)





        self.x = x
        self.y = y

        self.canvas.draw()

    def on_cmap_changed(self, index):
        cmap = self.combo_box.currentText()
        self.plotG(self.x, self.y, cmap)

    def on_cmap_hovered(self, index):
        cmap = self.combo_box.itemText(index)
        self.plotG(self.x, self.y, cmap)

    def on_point_size_changed(self, value):
        self.point_size = value
        self.plotG(self.x, self.y, self.combo_box.currentText())