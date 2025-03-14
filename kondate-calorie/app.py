from pathlib import Path
from shiny import render , reactive
from shiny.express import input,ui

import pandas as pd

ui.include_css(
    Path(__file__).parent / "www" / "custom.css")


with pd.ExcelFile(Path(__file__).parent / "kondate.xlsx" ) as xlsx:
     syusyoku = pd.read_excel(xlsx, sheet_name="rice")
     main = pd.read_excel(xlsx, sheet_name="main")
     sub = pd.read_excel(xlsx, sheet_name="sub")
     soup = pd.read_excel(xlsx, sheet_name="soup")

ui.page_opts(fillable=True)


with ui.layout_column_wrap():
    with ui.card(class_="card-syusyoku"):
        ui.input_select("syusyoku","主食",syusyoku["名称"],multiple=True)


    with ui.card(class_="card-main"):
        ui.input_select("main","主菜",main["名称"],multiple=True)
        
    with ui.card(class_="card-sub"):
        ui.input_select("sub","副菜",sub["名称"],multiple=True)
    
    
    with ui.card(class_="card-soup"):
        ui.input_select("soup","汁物",soup["名称"],multiple=True)

@reactive.calc
def df_syusyoku():
    selected = [int(i) for i in input.syusyoku()]
    return syusyoku.loc[selected, :]

@reactive.calc
def df_main():
    selected = [int(i) for i in input.main()]
    return main.loc[selected, :]

@reactive.calc
def df_sub():
    selected = [int(i) for i in input.sub()]
    return sub.loc[selected, :]

@reactive.calc
def df_soup():
    selected = [int(i) for i in input.soup()]
    return soup.loc[selected, :]


@reactive.calc
def menu():
    return pd.concat([df_syusyoku(),
                      df_main(),
                      df_sub(),
                      df_soup()])


@render.express
def txt():
    menu()

    n=sum(menu()['カロリー（kcal）'])
    ui.p(ui.span(str(n)+"kcal", class_="calorie-info"),
         )