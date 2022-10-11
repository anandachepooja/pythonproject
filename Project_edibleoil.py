####importing required modules
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt
import tkinter as tk
import seaborn as sns
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk

class Plotwindow(tk.Tk):
    def __init__(self, size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Plotting Edible Oil data")   ### Title of root window
        f1 = ttk.Frame(self)      ####frame for plot window
        f1.grid(row=0, column=1)
        self.fig = plt.Figure(size, dpi=100)  ####defining plot figure
        with sns.axes_style("dark"):  #####using matplotlib plot style
            self.ax = self.fig.add_subplot()
        self.colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'brown']  ####basic colors used in graph
        self.canvas = FigureCanvasTkAgg(self.fig, master=f1)       #
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2)
        self.toolbar = NavigationToolbar2Tk(self.canvas, f1, pack_toolbar=False)
        self.toolbar.grid(column=1, row=8, sticky="se")
        self.oilVar = tk.StringVar()  ####variable used in combobox and radio button
        self.rbVar = tk.StringVar()
        self.createWidgets()
        self.mainloop()

    def read_data(self):
        #####https://www.indexmundi.com/commodities/?commodity=coconut-oil data source
        #####read csv data and convert it to dataframe'''
        oil_data = pd.read_csv('8 Edible Oils.csv', parse_dates=["Month"], usecols=[0, 1, 3, 5, 7, 9, 11, 13, 15])
        ####changing the datatype of columns in dataframe from string to float
        for i in range(1, 9):
            oil_data[oil_data.columns[i]] =oil_data[oil_data.columns[i]].str.replace(',','').astype('float')
        return oil_data

       ##### grouping of data to find mean
    def read_data_bar(self):
        df=self.read_data()
        oil_data_avg = df.groupby(df.Month.dt.year).mean() #######obtaining mean price for all columns per year
        return oil_data_avg

        ##### oil list formatting using list compression
    def col_names(self):
        df=self.read_data_bar()
        Oils_list = [i.rstrip(' Price') for i in list(df)]  ####gives formatted list of column names using string formatting
        Oils_list.append("All")
        return Oils_list

    def createWidgets(self):
        combo_list=self.col_names()
        self.oilVar.set(combo_list[0])

        f2 = ttk.Frame(self)
        f2.grid(row = 0, column = 0, sticky = "nw")

        lf= ttk.LabelFrame(f2, text="Select Plot Options")
        lf.grid(row=0, column=0, columnspan=2, sticky="nsew",padx=1, pady=1)

        lf1 = ttk.LabelFrame(lf, text="Select Plot type")
        lf1.grid(row=1, column=0,columnspan=2,sticky="nw",padx=1, pady=1)

        rb = ttk.Radiobutton(lf1, variable=self.rbVar, value="lineplot",text="Line Plot")
        rb.grid(row=2, column=0, sticky="nw")

        rb1 = ttk.Radiobutton(lf1, variable=self.rbVar, value="barplot", text="Bar Plot")
        rb1.grid(row=3, column=0, sticky="nw")

        lf2 = ttk.LabelFrame(lf, text="Select Oil")
        lf2.grid(row=4, column=0,columnspan=2,sticky="nsew",padx=1, pady=1)

        c1 = ttk.Combobox(lf2, textvariable=self.oilVar, values=combo_list, state="readonly")
        c1.grid(row=5, column=0, columnspan=2)
        c1.current([0])

        b1=ttk.Button(lf,text="Plot",command=self.plot_type)
        b1.grid(row=6, column=0)

        b2=ttk.Button(lf,text="Clear",command=self.clear)
        b2.grid(row=6,column=1)

        b3 = ttk.Button(lf, text="Quit", command=self.quit)
        b3.grid(row=7, column=0,columnspan=2)

#########function to plot line graph
    def apply(self):
        df=self.read_data()
        colname=self.col_names()
        x = df["Month"]      ###### x values for graph is first column
        if self.oilVar.get()=="All":
             for i in range(1,9):
                 y=df[df.columns[i]] ##### y values for graph are columns from 1 to 8 based on user selection
                 self.ax.plot(x,y,label=colname[i-1],color=self.colors[i-1])
                 self.canvas.draw()
        else:
            oil_name = self.oilVar.get()
            i = colname.index(oil_name)
            y = df[df.columns[i + 1]]
            self.ax.plot(x, y, label=colname[i], color=self.colors[i])
            self.canvas.draw()
     ####formatting of plot figure
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator(tz=None, minticks=8, maxticks=22, interval_multiples=True))
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("USD($)/Metric Ton")
        self.ax.legend(loc='upper right')
        self.ax.set_title("Edible Oil prices over past 30 years",fontsize=12)
        self.fig.tight_layout()
        self.ax.grid()
        self.canvas.draw()

########function to plot bar graph
    def apply_bar(self):
        df=self.read_data()
        df1=self.read_data_bar()
        col=self.col_names()
        x = df.Month.dt.year.unique().tolist()  #### obtaining unique values of years from Month column as x values for plot
        if self.oilVar.get() != "All":
            oil_name = self.oilVar.get()
            i = col.index(oil_name)
            y = df1[df1.columns[i]]
            self.ax.bar(x, y, label=col[i],width=0.5, color=self.colors[i],alpha=0.5)
            self.ax.plot(x,y,color=self.colors[i])
            self.ax.scatter(x,y)
            self.ax.set_xticks(x)
            self.ax.tick_params(axis="x", labelrotation=45)
            self.canvas.draw()
        else:
            df1.plot.bar(width=0.78,ax=self.ax,alpha=0.75)
            self.canvas.draw()
        self.ax.set_xlabel("Year")
        self.ax.set_ylabel("Mean Price\n USD($)/Metric Ton")
        self.ax.set_title("Edible Oil prices over past 30 years",fontsize=12)
        self.ax.legend(loc='upper left')
        self.canvas.draw()

#####function to pass radio button output and decide plot type
    def plot_type(self):
        if self.rbVar.get() == "lineplot":
            plot = self.apply()
        elif self.rbVar.get()=="barplot":
            plot = self.apply_bar()

    def clear(self):    ########function for clear command
        self.ax.clear()
        self.canvas.draw()

if __name__ == "__main__":

    plw = Plotwindow((15, 8)) #### initiate class