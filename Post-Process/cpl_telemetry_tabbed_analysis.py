"""Hot-Fire Telemetry — PySide6 + PyQtGraph desktop dashboard."""
import sys
import base64
from pathlib import Path
import re
import numpy as np
import pandas as pd
from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6 import QtGui
from PySide6 import QtSvg

import pyqtgraph as pg

CPL_LOGO_SVG_BASE64 = """PHN2ZyB3aWR0aD0iMTQ5IiBoZWlnaHQ9IjE5IiB2aWV3Qm94PSIwIDAgMTQ5IDE5IiBmaWxsPSJub25lIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgo8cGF0aCBkPSJNMCAzLjIwNDUxQzAuMjY4MTk5IDIuMjcwNDQgMC44NjAwODYgMS41MDI4NCAxLjc3NTY2IDAuOTAxNzAzQzIuNzAwNDggMC4zMDA1NjggMy44NzAzOSAwIDUuMjg1MzcgMEgyMS4wMTY2QzIyLjEwNzkgMCAyMy4wNjUxIDAuMTY2NDY4IDIzLjg4ODIgMC40OTk0MDVDMjQuNzIwNSAwLjgyMzA5MyAyNS4zNjc5IDEuMjM0NjQgMjUuODMwMyAxLjczNDA0QzI2LjI5MjcgMi4yMjQyIDI2LjUyMzkgMi43MTQzNiAyNi41MjM5IDMuMjA0NTFIMFoiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik01MS40MTA5IDBDNTIuNjg3MiAwIDUzLjc1NTQgMC4yMDM0NjEgNTQuNjE1NCAwLjYxMDM4M0M1NS40NzU1IDEuMDE3MzEgNTYuMTE4MyAxLjU2NzU4IDU2LjU0MzcgMi4yNjExOUM1Ni45Nzg0IDIuOTQ1NTYgNTcuMTk1NyAzLjcwMzkyIDU3LjE5NTcgNC41MzYyNlY2LjMyNTc5QzU3LjE5NTcgNy4xNTgxMyA1Ni45Nzg0IDcuOTE2NDkgNTYuNTQzNyA4LjYwMDg2QzU2LjExODMgOS4yODUyMyA1NS40NzU1IDkuODMwODcgNTQuNjE1NCAxMC4yMzc4QzUzLjc1NTQgMTAuNjQ0NyA1Mi42ODcyIDEwLjg0ODIgNTEuNDEwOSAxMC44NDgySDM2LjEzNzVWMTguNTE5NkgzMC40OTE0VjcuNjU3NTRINTAuMzU2NkM1MC44MDA1IDcuNjU3NTQgNTEuMTk4MiA3LjUwNDk0IDUxLjU0OTcgNy4xOTk3NUM1MS45MDExIDYuODg1MzEgNTIuMDc2OCA2LjUwNjEzIDUyLjA3NjggNi4wNjIyMlY0Ljc4NTk2QzUyLjA3NjggNC4zNTEyOSA1MS45MDExIDMuOTgxMzYgNTEuNTQ5NyAzLjY3NjE3QzUxLjE5ODIgMy4zNjE3MyA1MC44MDA1IDMuMjA0NTEgNTAuMzU2NiAzLjIwNDUxSDMwLjQ5MTRWMEg1MS40MTA5WiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTI2LjUyMzkgMTUuMzE1MUMyNi41MjM5IDE1LjgwNTIgMjYuMjkyNyAxNi4yOTU0IDI1LjgzMDMgMTYuNzg1NUMyNS4zNjc5IDE3LjI3NTcgMjQuNzIwNSAxNy42ODcyIDIzLjg4ODIgMTguMDIwMkMyMy4wNjUxIDE4LjM1MzEgMjIuMTA3OSAxOC41MTk2IDIxLjAxNjYgMTguNTE5Nkg1LjI4NTM3QzQuMTg0ODMgMTguNTE5NiAzLjIyNzYzIDE4LjMzNDYgMi40MTM3OSAxNy45NjQ3QzEuNjA5MTkgMTcuNTg1NSAwLjk4NDkzNyAxNy4wODE1IDAuNTQxMDIyIDE2LjQ1MjZDMC4yODkzMjcgMTYuMDk2IDAuMTA4OTg3IDE1LjcxNzIgMCAxNS4zMTZMMjYuNTIzOSAxNS4zMTUxWiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTIxLjAxNjYgMEMyMi4xMDc5IDAgMjMuMDY1MSAwLjE2NjQ2OCAyMy44ODgyIDAuNDk5NDA1QzI0LjcyMDUgMC44MjMwOTMgMjUuMzY3OSAxLjIzNDY0IDI1LjgzMDMgMS43MzQwNEMyNi4yOTI3IDIuMjI0MiAyNi41MjM5IDIuNzE0MzYgMjYuNTIzOSAzLjIwNDUxVjBIMjEuMDE2NloiIGZpbGw9IndoaXRlIi8+CjxwYXRoIGQ9Ik0yNi41MjM5IDE1LjMxNTFDMjYuNTIzOSAxNS44MDUyIDI2LjI5MjcgMTYuMjk1NCAyNS44MzAzIDE2Ljc4NTVDMjUuMzY3OSAxNy4yNzU3IDI0LjcyMDUgMTcuNjg3MiAyMy44ODgyIDE4LjAyMDJDMjMuMDY1MSAxOC4zNTMxIDIyLjEwNzkgMTguNTE5NiAyMS4wMTY2IDE4LjUxOTZIMjYuNTIzOVYxNS4zMTUxWiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTY2LjU2MDUgNC4wMzY4NVYxNS4zMTUxSDcwLjk1OTlMNjYuNDkzIDE4LjUxOTZINjAuOTE0NFYwSDYxLjI2MTJDNjIuNjc2MiAwIDYzLjc2MjkgMC4xODQ5NjUgNjQuNTIxMiAwLjU1NDg5NEM2NS4yODg4IDAuOTE1NTc1IDY1LjgyMDYgMS40MDExMSA2Ni4xMTY1IDIuMDExNDlDNjYuNDEyNSAyLjYyMTg3IDY2LjU2MDUgMy4yOTcgNjYuNTYwNSA0LjAzNjg1WiIgZmlsbD0id2hpdGUiLz4KPHBhdGggZD0iTTcwLjk1OTkgMTUuMzE1MUw2Ni40OTMgMTguNTE5NkM2Ny40MTc5IDE4LjUxOTYgNjguMjEzMiAxOC4zNTMxIDY4Ljg3OTEgMTguMDIwMkM2OS41NDUgMTcuNjc4IDcwLjA1ODIgMTcuMjYxOCA3MC40MTg5IDE2Ljc3MTdDNzAuNzc5NiAxNi4yNzIzIDcwLjk1OTkgMTUuNzg2NyA3MC45NTk5IDE1LjMxNTFaIiBmaWxsPSJ3aGl0ZSIvPgo8cGF0aCBkPSJNNzIuNTYzOCAxOC41MTkzQzczLjg4MDMgMTcuOTY5MiA3NS4wNDE2IDE2LjY4NzEgNzUuMjEyNiAxNS4yOTcxTDE0OC41MjkgMTYuODc3Mkw3Mi41NjM4IDE4LjUxOTNaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4K"""

BG="#070b10"; PANEL="#0b1219"; PANEL2="#101b25"; EDGE="#1c3545"
TEXT="#e5edf4"; MUTED="#8c9baa"; BLUE="#39c7f3"
COLORS=["#37d5ff","#ffae69","#a890ff","#60e0bb","#ff6f9e","#f8d575","#8dbfff"]
pg.setConfigOptions(antialias=True, background=BG, foreground=MUTED)

class TraceView(pg.PlotWidget):
    moved=QtCore.Signal(float)
    def __init__(self):
        super().__init__()
        self.trace_active=False
        self._trace_dragging=False
        self.setMouseTracking(True)
        self.setMouseEnabled(x=True,y=True)
        self.showGrid(x=True,y=True,alpha=.09)
        self.getPlotItem().setLabel("bottom","TIME / SELECTED X CHANNEL")
        self.getPlotItem().setLabel("left","CHANNEL VALUE")
        self.getPlotItem().getViewBox().setBorder(pg.mkPen(EDGE))
        self.line=pg.InfiniteLine(angle=90,movable=False,pen=pg.mkPen("#e6edf5",width=1,style=QtCore.Qt.DashLine))
        self.line.sigPositionChanged.connect(lambda: self.moved.emit(self.line.value()))
        self.addItem(self.line,ignoreBounds=True)
        self.line.hide()
        self.dot=pg.ScatterPlotItem(size=11,brush=pg.mkBrush(BLUE),pen=pg.mkPen("#fff",width=1))
        self.addItem(self.dot)
    def _cursor_x_from_event(self,event):
        scene_pos=self.mapToScene(event.position().toPoint())
        if not self.getPlotItem().vb.sceneBoundingRect().contains(scene_pos):
            return None
        return float(self.getPlotItem().vb.mapSceneToView(scene_pos).x())

    def mousePressEvent(self,event):
        if (self.trace_active and event.button()==QtCore.Qt.LeftButton
                and not (event.modifiers() & QtCore.Qt.ControlModifier)):
            x=self._cursor_x_from_event(event)
            if x is not None:
                self._trace_dragging=True
                self.setCursor(QtCore.Qt.SizeHorCursor)
                self.moved.emit(x)
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self,event):
        if self._trace_dragging:
            x=self._cursor_x_from_event(event)
            if x is not None:
                self.moved.emit(x)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self,event):
        if self._trace_dragging and event.button()==QtCore.Qt.LeftButton:
            self._trace_dragging=False
            self.unsetCursor()
            event.accept()
            return
        super().mouseReleaseEvent(event)

class PlotTab(QtWidgets.QWidget):
    def __init__(self,app):
        super().__init__(); self.app=app; self.channels=[]; self.curves={}; self.trace_enabled=False
        self.trace_x=None;self.valves=[];self.valve_curves={}
        self.manual_axis_limits=None
        self.stats_selection_enabled=False
        self.stats_region=pg.LinearRegionItem(values=[0,1],movable=True,
            brush=pg.mkBrush(35,170,220,38),
            pen=pg.mkPen("#49b9db",width=1))
        self.stats_region.setZValue(15)
        self.stats_region.sigRegionChanged.connect(self.update_stats)
        layout=QtWidgets.QHBoxLayout(self); layout.setContentsMargins(3,5,3,3);layout.setSpacing(7)
        left=QtWidgets.QFrame();left.setObjectName("panel");left.setFixedWidth(252)
        ll=QtWidgets.QVBoxLayout(left);ll.setContentsMargins(9,10,9,9);ll.setSpacing(6)
        # Separate selector tabs give each channel library the full sidebar height.
        self.selector_tabs=QtWidgets.QTabWidget()
        ll.addWidget(self.selector_tabs,1)

        signals_page=QtWidgets.QWidget()
        sl=QtWidgets.QVBoxLayout(signals_page)
        sl.setContentsMargins(4,8,4,4);sl.setSpacing(5)
        sl.addWidget(self.label("SIGNAL LIBRARY"))
        self.search=QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Search channels...")
        self.search.textChanged.connect(self.populate);sl.addWidget(self.search)
        self.available=QtWidgets.QListWidget()
        self.available.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.available.itemDoubleClicked.connect(lambda _:self.add_selected())
        self.available.setMinimumHeight(200)
        sl.addWidget(self.available,5)
        add=QtWidgets.QPushButton("+ ADD CHANNELS")
        add.clicked.connect(self.add_selected);sl.addWidget(add)
        sl.addWidget(self.label("ACTIVE CHANNELS"))
        self.active=QtWidgets.QListWidget()
        self.active.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.active.itemDoubleClicked.connect(lambda _:self.remove_selected())
        sl.addWidget(self.active,2)
        rm=QtWidgets.QPushButton("REMOVE SELECTED")
        rm.clicked.connect(self.remove_selected);sl.addWidget(rm)
        self.selector_tabs.addTab(signals_page,"SIGNALS")

        valves_page=QtWidgets.QWidget()
        vl=QtWidgets.QVBoxLayout(valves_page)
        vl.setContentsMargins(4,8,4,4);vl.setSpacing(5)
        vl.addWidget(self.label("VALVE LIBRARY"))
        self.valve_search=QtWidgets.QLineEdit()
        self.valve_search.setPlaceholderText("Search SV, HV, MBV...")
        self.valve_search.textChanged.connect(self.populate_valves)
        vl.addWidget(self.valve_search)
        self.valve_available=QtWidgets.QListWidget()
        self.valve_available.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.valve_available.itemDoubleClicked.connect(lambda _:self.add_valves())
        self.valve_available.setMinimumHeight(200)
        vl.addWidget(self.valve_available,5)
        b=QtWidgets.QPushButton("+ ADD VALVES")
        b.clicked.connect(self.add_valves);vl.addWidget(b)
        vl.addWidget(self.label("ACTIVE VALVES"))
        self.valve_active=QtWidgets.QListWidget()
        self.valve_active.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.valve_active.itemDoubleClicked.connect(lambda _:self.remove_valves())
        vl.addWidget(self.valve_active,2)
        b=QtWidgets.QPushButton("REMOVE VALVES")
        b.clicked.connect(self.remove_valves);vl.addWidget(b)
        self.selector_tabs.addTab(valves_page,"VALVES")

        ll.addWidget(self.label("TRACE CHANNEL"))
        self.trace_choice=QtWidgets.QComboBox()
        self.trace_choice.currentTextChanged.connect(self.update_trace)
        ll.addWidget(self.trace_choice)
        layout.addWidget(left)
        center=QtWidgets.QFrame();center.setObjectName("panel")
        cl=QtWidgets.QVBoxLayout(center)
        cl.setContentsMargins(9,9,9,7)
        cl.setSpacing(4)
        top=QtWidgets.QHBoxLayout(); top.addWidget(self.label("01  /  SIGNAL HISTORY"))
        top.addStretch()
        self.readout=QtWidgets.QLabel("SELECT A CHANNEL TO BEGIN");self.readout.setObjectName("muted");top.addWidget(self.readout)
        cl.addLayout(top)
        telemetry=QtWidgets.QHBoxLayout()
        telemetry.setSpacing(7)
        self.signal_chip=QtWidgets.QLabel("SIGNALS  00")
        self.valve_chip=QtWidgets.QLabel("VALVES  00")
        self.sample_chip=QtWidgets.QLabel("SAMPLES  —")
        for chip in (self.signal_chip,self.valve_chip,self.sample_chip):
            chip.setObjectName("metric")
            chip.setAlignment(QtCore.Qt.AlignCenter)
            telemetry.addWidget(chip)
        telemetry.addStretch()
        cl.addLayout(telemetry)
        self.graph=TraceView();self.graph.moved.connect(self.on_trace)
        # One compact legend for both telemetry and right-axis valve traces.
        # The legend belongs to the PlotItem, so it is included in exports.
        self.legend=self.graph.plotItem.addLegend(
            offset=(-12, 12), labelTextColor="#d7e8f2",
            brush=pg.mkBrush(9, 17, 24, 225),
            pen=pg.mkPen("#294252", width=1),
            colCount=1)
        self.legend.setVisible(False)
        self.graph.getPlotItem().getAxis("bottom").setPen(pg.mkPen("#345264"))
        self.graph.getPlotItem().getAxis("left").setPen(pg.mkPen("#345264"))
        self.valve_axis=pg.AxisItem("right")
        self.graph.plotItem.layout.addItem(self.valve_axis,2,3)
        self.valve_axis.setLabel("VALVE STATE (0 / 1)",color="#e9a86b")
        self.valve_view=pg.ViewBox()
        self.graph.scene().addItem(self.valve_view)
        self.valve_axis.linkToView(self.valve_view)
        self.valve_view.setXLink(self.graph.plotItem.vb)
        self.valve_view.setMouseEnabled(x=False,y=False)
        self.valve_view.setYRange(-0.15,1.15,padding=0)
        self.valve_view.enableAutoRange(axis=pg.ViewBox.YAxis,enable=False)
        self.graph.plotItem.vb.sigResized.connect(self.sync_valve_view)
        self.sync_valve_view()
        self.graph.getPlotItem().getViewBox().sigXRangeChanged.connect(lambda *_:self.update_stats())
        cl.addWidget(self.graph,1);layout.addWidget(center,1)
        right=QtWidgets.QFrame();right.setObjectName("panel");right.setFixedWidth(225)
        rl=QtWidgets.QVBoxLayout(right)
        rl.setContentsMargins(11,11,11,9)
        rl.setSpacing(7)
        self.analysis_tabs=QtWidgets.QTabWidget()
        rl.addWidget(self.analysis_tabs,1)
        stats_page=QtWidgets.QWidget()
        sl=QtWidgets.QVBoxLayout(stats_page)
        sl.setContentsMargins(5,9,5,5)
        sl.setSpacing(7)
        sl.addWidget(self.label("TELEMETRY  /  STATISTICS"))
        sl.addWidget(self.label("ANALYSIS WINDOW"))
        self.stats_mode=QtWidgets.QComboBox()
        self.stats_mode.addItems(["Visible graph range","Selected time interval"])
        self.stats_mode.currentIndexChanged.connect(self.change_stats_mode)
        sl.addWidget(self.stats_mode)
        self.select_range_button=QtWidgets.QPushButton("SELECT INTERVAL")
        self.select_range_button.clicked.connect(self.select_stats_interval)
        sl.addWidget(self.select_range_button)
        self.reset_range_button=QtWidgets.QPushButton("RESET TO VISIBLE RANGE")
        self.reset_range_button.clicked.connect(lambda:self.stats_mode.setCurrentIndex(0))
        sl.addWidget(self.reset_range_button)
        self.stats_interval_label=QtWidgets.QLabel("Statistics follow the visible X-axis range")
        self.stats_interval_label.setObjectName("muted")
        self.stats_interval_label.setWordWrap(True)
        sl.addWidget(self.stats_interval_label)
        self.stats=QtWidgets.QTextEdit();self.stats.setReadOnly(True);self.stats.setFrameShape(QtWidgets.QFrame.NoFrame)
        sl.addWidget(self.stats,1)
        self.analysis_tabs.addTab(stats_page,"STATISTICS")
        axes_page=QtWidgets.QWidget()
        al=QtWidgets.QVBoxLayout(axes_page)
        al.setContentsMargins(5,9,5,5)
        al.setSpacing(7)
        al.addWidget(self.label("AXIS WINDOW  /  MANUAL"))
        limits_grid=QtWidgets.QGridLayout()
        limits_grid.setHorizontalSpacing(5)
        limits_grid.setVerticalSpacing(5)
        self.axis_inputs={}
        for i,(key,caption) in enumerate((("xmin","X MIN"),("xmax","X MAX"),
                                          ("ymin","Y MIN"),("ymax","Y MAX"))):
            field=QtWidgets.QLineEdit()
            field.setPlaceholderText("Auto")
            field.setToolTip(f"Enter {caption} as a number (scientific notation supported)")
            field.returnPressed.connect(self.apply_axis_window)
            self.axis_inputs[key]=field
            limits_grid.addWidget(self.label(caption),i//2*2,i%2)
            limits_grid.addWidget(field,i//2*2+1,i%2)
        al.addLayout(limits_grid)
        axis_buttons=QtWidgets.QHBoxLayout()
        apply_btn=QtWidgets.QPushButton("APPLY")
        apply_btn.clicked.connect(self.apply_axis_window)
        axis_buttons.addWidget(apply_btn)
        current_btn=QtWidgets.QPushButton("USE CURRENT")
        current_btn.clicked.connect(self.capture_axis_window)
        axis_buttons.addWidget(current_btn)
        al.addLayout(axis_buttons)
        auto_btn=QtWidgets.QPushButton("AUTO AXES")
        auto_btn.clicked.connect(self.reset_axis_window)
        al.addWidget(auto_btn)
        al.addStretch(1)
        self.analysis_tabs.addTab(axes_page,"AXES")
        layout.addWidget(right)
        self.populate()
    def label(self,text):
        w=QtWidgets.QLabel(text);w.setObjectName("heading");return w
    def populate(self,*_):
        self.available.clear()
        if self.app.data is None:return
        query=self.search.text().lower()
        self.available.addItems([c for c in self.app.numeric if query in c.lower() and c!=self.app.xcol and c not in self.app.valve_channels])
    def sync_valve_view(self):
        self.valve_view.setGeometry(self.graph.plotItem.vb.sceneBoundingRect())
        self.valve_view.linkedViewChanged(self.graph.plotItem.vb,self.valve_view.XAxis)
    def populate_valves(self,*_):
        self.valve_available.clear()
        if self.app.data is None:return
        q=self.valve_search.text().lower()
        self.valve_available.addItems([c for c in self.app.valve_channels if q in c.lower()])
    def add_valves(self):
        for item in self.valve_available.selectedItems():
            if item.text() not in self.valves:self.valves.append(item.text())
        self.redraw()
    def remove_valves(self):
        removed={item.text() for item in self.valve_active.selectedItems()}
        self.valves=[c for c in self.valves if c not in removed]
        self.redraw()
    def add_selected(self):
        for item in self.available.selectedItems():
            if item.text() not in self.channels:self.channels.append(item.text())
        self.redraw()
    def remove_selected(self):
        removed={item.text() for item in self.active.selectedItems()}
        self.channels=[c for c in self.channels if c not in removed];self.redraw()
    def redraw(self):
        self.legend.clear()
        self.graph.clear()
        self.graph.addItem(self.graph.line,ignoreBounds=True)
        self.graph.addItem(self.graph.dot)
        self.graph.addItem(self.stats_region,ignoreBounds=True)
        self.stats_region.setVisible(self.stats_selection_enabled)
        self.curves={};self.valve_curves={}
        self.valve_view.clear()
        self.valve_view.setYRange(-0.15,1.15,padding=0)
        self.valve_active.clear();self.valve_active.addItems(self.valves)
        self.active.clear();self.active.addItems(self.channels)
        self.trace_choice.blockSignals(True)
        old=self.trace_choice.currentText()
        self.trace_choice.clear();self.trace_choice.addItems(self.channels)
        if old in self.channels:self.trace_choice.setCurrentText(old)
        self.trace_choice.blockSignals(False)
        if self.app.data is not None and self.app.x is not None:
            for i,c in enumerate(self.channels):
                y=pd.to_numeric(self.app.data[c],errors="coerce").to_numpy(dtype=float)
                color=COLORS[i%len(COLORS)]
                self.curves[c]=(y,color)
                good=np.isfinite(self.app.x)&np.isfinite(y)
                curve=self.graph.plot(self.app.x[good],y[good],
                                      pen=pg.mkPen(color,width=1.5))
                self.legend.addItem(curve,c)
            for i,c in enumerate(self.valves):
                y=pd.to_numeric(self.app.data[c],errors="coerce").to_numpy(dtype=float)
                good=np.isfinite(self.app.x)&np.isfinite(y)
                color=COLORS[(len(self.channels)+i+1)%len(COLORS)]
                self.valve_curves[c]=(y,color)
                if good.any():
                    curve=pg.PlotDataItem(
                        self.app.x[good],y[good],pen=pg.mkPen(color,width=1.7),
                        stepMode="left")
                    self.valve_view.addItem(curve)
                    self.legend.addItem(curve,f"{c}  [VALVE]")
        self.legend.setVisible(bool(self.channels or self.valves))
        self.valve_axis.setVisible(bool(self.valves))
        self.signal_chip.setText(f"SIGNALS  {len(self.channels):02d}")
        self.valve_chip.setText(f"VALVES  {len(self.valves):02d}")
        self.sample_chip.setText(f"SAMPLES  {len(self.app.data):,}" if self.app.data is not None else "SAMPLES  —")
        if self.manual_axis_limits is not None:
            self._set_axis_window(*self.manual_axis_limits)
        self.update_trace();self.update_stats()

    def capture_axis_window(self):
        xlim,ylim=self.graph.viewRange()
        for key,value in zip(("xmin","xmax","ymin","ymax"),(*xlim,*ylim)):
            self.axis_inputs[key].setText(f"{value:.10g}")

    def _set_axis_window(self,xmin,xmax,ymin,ymax):
        vb=self.graph.getPlotItem().vb
        vb.setXRange(xmin,xmax,padding=0)
        vb.setYRange(ymin,ymax,padding=0)

    def apply_axis_window(self):
        current_x,current_y=self.graph.viewRange()
        fallback=(*current_x,*current_y)
        values=[]
        try:
            for key,default in zip(("xmin","xmax","ymin","ymax"),fallback):
                raw=self.axis_inputs[key].text().strip()
                value=float(raw) if raw else default
                if not np.isfinite(value):
                    raise ValueError(f"{key.upper()} must be finite")
                values.append(value)
            xmin,xmax,ymin,ymax=values
            if xmin>=xmax or ymin>=ymax:
                raise ValueError("Minimum must be smaller than maximum on both axes.")
        except ValueError as exc:
            QtWidgets.QMessageBox.warning(self,"Invalid axis window",str(exc))
            return
        self.manual_axis_limits=tuple(values)
        self._set_axis_window(*values)
        self.update_stats()

    def reset_axis_window(self):
        self.manual_axis_limits=None
        for field in self.axis_inputs.values():
            field.clear()
        self.graph.enableAutoRange(axis="xy",enable=True)
        self.update_stats()

    def set_trace(self,enabled):
        self.trace_enabled=enabled;self.graph.trace_active=enabled
        if not enabled:
            self.graph._trace_dragging=False
            self.graph.unsetCursor()
        self.update_trace()
    def on_trace(self,x):
        self.trace_x=x;self.update_trace()
    def update_trace(self,*_):
        self.graph.line.setVisible(self.trace_enabled and bool(self.curves))
        self.graph.dot.clear()
        if not self.trace_enabled or not self.curves or self.app.x is None:
            self.readout.setText("TRACE DISABLED" if not self.trace_enabled else "NO SIGNAL")
            self.update_stats();return
        x=self.app.x
        c=self.trace_choice.currentText()
        if c not in self.curves:return
        y,color=self.curves[c]
        good=np.isfinite(x)&np.isfinite(y)
        if not good.any():return
        if self.trace_x is None:self.trace_x=float(x[good][len(x[good])//2])
        indices=np.flatnonzero(good)
        idx=indices[np.argmin(np.abs(x[good]-self.trace_x))]
        self.graph.line.blockSignals(True)
        self.graph.line.setValue(float(x[idx]))
        self.graph.line.blockSignals(False)
        self.graph.dot.setData([x[idx]],[y[idx]],brush=pg.mkBrush(color))
        self.readout.setText(f"{c}   |   X {x[idx]:.7g}   |   Y {y[idx]:.7g}")
        self.update_stats()
    def change_stats_mode(self,index):
        if index==1 and not self.stats_selection_enabled:
            self.select_stats_interval()
            return
        self.stats_selection_enabled=(index==1)
        self.stats_region.setVisible(self.stats_selection_enabled)
        self.update_stats()

    def select_stats_interval(self):
        if self.app.x is None:
            QtWidgets.QMessageBox.information(self,"No data","Load a Parquet file first.")
            return
        lo,hi=self.graph.viewRange()[0]
        if not np.isfinite(lo) or not np.isfinite(hi) or hi<=lo:return
        span=hi-lo
        self.stats_region.setRegion((lo+span*.25,lo+span*.75))
        self.stats_selection_enabled=True
        self.stats_region.setVisible(True)
        self.stats_mode.blockSignals(True)
        self.stats_mode.setCurrentIndex(1)
        self.stats_mode.blockSignals(False)
        self.update_stats()

    def update_stats(self):
        if self.app.x is None:return
        if self.stats_selection_enabled:
            lo,hi=sorted(self.stats_region.getRegion())
            heading="SELECTED INTERVAL"
        else:
            lo,hi=self.graph.viewRange()[0]
            heading="VISIBLE INTERVAL"
        mask=np.isfinite(self.app.x)&(self.app.x>=lo)&(self.app.x<=hi)
        self.stats_interval_label.setText(
            "Drag the shaded region or either edge to adjust the interval"
            if self.stats_selection_enabled else
            "Statistics follow the visible X-axis range")
        parts=[f"{heading}\n{lo:.7g} — {hi:.7g}\nDURATION  {hi-lo:.7g} (X units)\nSAMPLES  {mask.sum():,}\n"]
        for c in self.channels:
            y=pd.to_numeric(self.app.data[c],errors="coerce").to_numpy(dtype=float)[mask]
            y=y[np.isfinite(y)]
            if not len(y):continue
            parts.append(f"\n{c}\n{'─'*27}\nMEAN       {np.mean(y):.7g}\nMEDIAN     {np.median(y):.7g}\nMIN        {np.min(y):.7g}\nMAX        {np.max(y):.7g}\nSTD DEV    {np.std(y):.7g}\nCOUNT      {len(y):,}\n")
        self.stats.setPlainText("\n".join(parts))

    def export(self):
        if not self.channels and not self.valves:
            QtWidgets.QMessageBox.information(self,"Nothing to save","Add at least one channel first.");return
        path,_=QtWidgets.QFileDialog.getSaveFileName(self,"Save plot","hotfire_plot.png","PNG (*.png);;SVG (*.svg)")
        if not path:return
        try:
            if path.lower().endswith(".svg"):
                from pyqtgraph.exporters import SVGExporter
                SVGExporter(self.graph.plotItem).export(path)
            else:
                from pyqtgraph.exporters import ImageExporter
                exporter=ImageExporter(self.graph.plotItem)
                exporter.parameters()["width"]=1800
                exporter.export(path)
            self.app.status.showMessage(f"Saved plot: {path}")
        except Exception as e:QtWidgets.QMessageBox.critical(self,"Export error",str(e))

class Dashboard(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.data=None;self.numeric=[];self.valve_channels=[];self.xcol=None;self.x=None
        self.setWindowTitle("CPL  |  Telemetry")
        self.resize(1550,900)
        outer=QtWidgets.QWidget();self.setCentralWidget(outer)
        root=QtWidgets.QVBoxLayout(outer);root.setContentsMargins(10,7,10,5);root.setSpacing(7)
        bar=QtWidgets.QHBoxLayout()
        logo_label=QtWidgets.QLabel()
        # Logo embedded directly in this script; no separate image file required.
        svg_data=base64.b64decode(CPL_LOGO_SVG_BASE64)
        renderer=QtSvg.QSvgRenderer(QtCore.QByteArray(svg_data))
        if renderer.isValid():
            # Render the exact uploaded SVG at high resolution for crisp scaling.
            pix=QtGui.QPixmap(596,76)
            pix.fill(QtCore.Qt.transparent)
            painter=QtGui.QPainter(pix)
            renderer.render(painter)
            painter.end()
            logo_label.setPixmap(pix.scaled(100,24,QtCore.Qt.KeepAspectRatio,
                                            QtCore.Qt.SmoothTransformation))
        else:
            logo_label.setText("CPL")
            logo_label.setObjectName("title")
        logo_label.setFixedWidth(110)
        logo_label.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        bar.addWidget(logo_label)
        bar.addSpacing(14)
        for name,fn in [("OPEN FILE",self.load),("+ PLOT",self.new_plot),("× CLOSE",self.close_plot),("↓ SAVE",self.save)]:
            b=QtWidgets.QPushButton(name);b.clicked.connect(fn);bar.addWidget(b)
        self.toggle=QtWidgets.QPushButton("○ TRACE OFF");self.toggle.setCheckable(True)
        self.toggle.clicked.connect(self.toggle_trace);bar.addWidget(self.toggle)
        bar.addStretch()
        bar.addWidget(QtWidgets.QLabel("TIMEBASE  /  X"))
        self.xchoice=QtWidgets.QComboBox();self.xchoice.setMinimumWidth(190)
        self.xchoice.currentTextChanged.connect(self.set_x);bar.addWidget(self.xchoice)
        root.addLayout(bar)
        self.tabs=QtWidgets.QTabWidget();self.tabs.currentChanged.connect(self.sync_toggle)
        root.addWidget(self.tabs,1)
        self.status=self.statusBar();self.status.showMessage("●  SYSTEM READY    /    LOAD A PARQUET FILE")
        self.new_plot()
    def tab(self):return self.tabs.currentWidget()
    def new_plot(self):
        tab=PlotTab(self);self.tabs.addTab(tab,f"Plot {self.tabs.count()+1}")
        self.tabs.setCurrentWidget(tab);self.sync_toggle()
    def close_plot(self):
        if self.tabs.count()<=1:return
        idx=self.tabs.currentIndex();w=self.tabs.widget(idx)
        self.tabs.removeTab(idx);w.deleteLater()
    def save(self):
        if self.tab():self.tab().export()
    def toggle_trace(self,enabled):
        if self.tab():self.tab().set_trace(enabled)
        self.sync_toggle()
    def sync_toggle(self,*_):
        tab=self.tab()
        if tab is None:return
        self.toggle.blockSignals(True);self.toggle.setChecked(tab.trace_enabled)
        self.toggle.setText("◎ TRACE ON" if tab.trace_enabled else "○ TRACE OFF")
        self.toggle.blockSignals(False)
    def load(self):
        path,_=QtWidgets.QFileDialog.getOpenFileName(self,"Open test data","","Parquet (*.parquet)")
        if not path:return
        try:df=pd.read_parquet(path)
        except Exception as e:QtWidgets.QMessageBox.critical(self,"Load failed",str(e));return
        self.data=df.reset_index(drop=True)
        self.numeric=[str(c) for c in self.data.columns if pd.api.types.is_numeric_dtype(self.data[c])]
        valve_pattern=re.compile(r"^(?:SV|HV|MBV|CV|RV|PV|VLV|VALVE)(?:_|\\b)",re.I)
        self.valve_channels=[c for c in self.numeric if
            valve_pattern.search(c) or re.search(r"(?:^|_)(?:valve|solenoid)(?:_|$)",c,re.I)]
        candidates=[str(c) for c in self.data.columns if pd.api.types.is_datetime64_any_dtype(self.data[c])]
        self.xchoice.blockSignals(True);self.xchoice.clear()
        self.xchoice.addItem("(row index)")
        self.xchoice.addItems([str(c) for c in self.data.columns])
        preferred=next((c for c in self.data.columns if str(c).lower() in ("time","time_s","timestamp","elapsed_time")),None)
        self.xchoice.setCurrentText(str(preferred) if preferred is not None else "(row index)")
        self.xchoice.blockSignals(False)
        self.set_x(self.xchoice.currentText())
        for i in range(self.tabs.count()):self.tabs.widget(i).populate();self.tabs.widget(i).populate_valves();self.tabs.widget(i).redraw()
        self.status.showMessage(f"{path}   |   {len(df):,} rows   |   {len(self.numeric)} numeric channels")
    def set_x(self,name):
        if self.data is None:return
        self.xcol=name
        if name=="(row index)":self.x=np.arange(len(self.data),dtype=float)
        else:
            series=self.data[name]
            if pd.api.types.is_datetime64_any_dtype(series):
                self.x=(series-series.iloc[0]).dt.total_seconds().to_numpy(dtype=float)
            else:
                self.x=pd.to_numeric(series,errors="coerce").to_numpy(dtype=float)
        for i in range(self.tabs.count()):
            tab=self.tabs.widget(i);tab.trace_x=None;tab.populate();tab.populate_valves();tab.redraw()

def main():
    app=QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    font=QtGui.QFont("Barlow",10)
    if "Barlow" not in QtGui.QFontDatabase.families():font=QtGui.QFont("Bahnschrift",10)
    app.setFont(font)
    app.setStyleSheet(f"""
    QMainWindow,QWidget{{background:{BG};color:{TEXT};}}
    QFrame#panel{{background:{PANEL};border:1px solid #1c303d;border-radius:2px;}}
    QLabel#title{{color:{TEXT};font-size:17px;font-weight:600;}}
    QLabel#heading{{background:transparent;color:{BLUE};font-size:10px;font-weight:600;letter-spacing:1.4px;}}
    QLabel#muted{{background:transparent;color:#8299a8;font-size:10px;}}
    QLabel#metric{{background:#0d1d28;color:#9cc6d9;border:1px solid #1b394b;
                   border-left:2px solid {BLUE};padding:5px 10px;font-size:10px;
                   font-family:Consolas;}}
    QLabel{{background:transparent;}}
    QPushButton{{background:#101b24;border:1px solid #1e3545;border-radius:2px;
                 padding:6px 10px;color:#b9cdd8;font-size:11px;font-weight:500;min-height:18px;}}
    QPushButton:hover{{background:#142b39;border-color:{BLUE};color:#eaffff;}}
    QPushButton:pressed{{background:#16445a;}}
    QPushButton:checked{{background:#0d394b;color:{BLUE};border-color:{BLUE};}}
    QLineEdit,QComboBox{{background:#080f15;color:#d7eaf3;border:1px solid #244053;
                         border-radius:2px;padding:4px 7px;min-height:19px;selection-background-color:#19516a;}}
    QComboBox::drop-down{{border:0px;width:20px;}}
    QListWidget,QTextEdit{{background:{PANEL};color:#c1d5e0;border:0px;
                           padding:2px;selection-background-color:#13465d;}}
    QListWidget::item{{padding:3px 5px;min-height:16px;border-radius:0px;}}
    QListWidget::item:hover{{background:#102d3a;}}
    QListWidget::item:selected{{background:#15516a;color:#eaffff;}}
    QTabWidget::pane{{border:0px;background:{BG};}}
    QTabBar::tab{{background:transparent;padding:7px 15px;border:0px;
                  border-bottom:1px solid #1b3444;color:#8297a6;font-size:11px;}}
    QTabBar::tab:selected{{color:{BLUE};border-bottom:2px solid {BLUE};}}
    QTabBar::tab:hover{{color:#e4f7ff;}}
    QStatusBar{{background:{BG};color:#6a9aaa;border-top:1px solid #18303e;font-size:10px;}}
    QScrollBar:vertical{{background:transparent;width:6px;margin:0;}}
    QScrollBar::handle:vertical{{background:#2b5368;border-radius:1px;min-height:25px;}}
    QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical{{height:0;}}
    QScrollBar:horizontal{{background:transparent;height:6px;}}
    QScrollBar::handle:horizontal{{background:#2b5368;border-radius:1px;}}
    QScrollBar::add-line:horizontal,QScrollBar::sub-line:horizontal{{width:0;}}
    """)
    w=Dashboard();w.show();sys.exit(app.exec())
if __name__=="__main__":main()
