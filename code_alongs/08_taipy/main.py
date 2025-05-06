from taipy.gui import Gui
import taipy.gui.builder as tgb
import plotly.express as px

df = px.data.gapminder()
fig = px.line(df.query("country == 'Sweden'"), x = "year", y = "pop")

slider_value = 0
selected_fruit = ""
number1=1
number2=1
sum_add = number1 + number2
sum_mult = number1 * number2
sum_sub = number1 - number2
sum_div = number1 / number2

def perform_calculation(state):
    state.sum_add = int(state.number1) + int(state.number2)
    state.sum_mult = int(state.number1) * int(state.number2)
    state.sum_sub = int(state.number1) - int(state.number2)
    state.sum_div = int(state.number1) / int(state.number2)

def clear_results(state):
    state.sum_add = 0
    state.sum_mult = 0
    state.sum_sub = 0
    state.sum_div = 0

with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        with tgb.layout(columns = "1 1 1"):
            with tgb.part() as column_fruit:
                tgb.text("# Hello there taipy", 
                        mode = "md", 
                        class_name= "color-primary")
                tgb.text("Welcome to the world of reactive programming", 
                        class_name="text-underline")

                #Binds to slider_value variable and makes it dynamic
                tgb.slider(value= "{slider_value}",min = 1, max = 50, 
                        step = 2,
                        continuous=False) # gör så att slider värdet uppdateras när man släpper slidern
                tgb.text("Slider value is at {slider_value}")

                tgb.text("Select your favourite fruit", 
                        mode= "md")
                tgb.selector(value="{selected_fruit}", 
                            lov=["tomato", "apple", "avocado", "banana"], 
                            dropdown=True)
                tgb.text("Yummy {selected_fruit}")
                tgb.image("assets/{selected_fruit}.jpg")
            with tgb.part() as column_calculator:
                tgb.text("## Cool calculator", mode="md")
                tgb.text("Type in a number")
                tgb.input("{number1}",on_change=clear_results)
                tgb.text("Type in another number")
                #On_change this will run when value is changed
                tgb.input("{number2}", on_change=clear_results)
                tgb.text("You have typed in {number1} and {number2}")
                # on_action = this function will run when button is clicked
                tgb.button(label= "Calculate", 
                        class_name= "plain",# annan färg på knappen
                        on_action=perform_calculation
                        ) 
                tgb.text("{number1} + {number2} = {sum_add}")
                tgb.text("{number1} * {number2} = {sum_mult}")
                tgb.text("{number1} - {number2} = {sum_sub}")
                tgb.text("{number1} / {number2} = {sum_div}")
            with tgb.part() as column_data:
                tgb.table("{df}", page_size= 20)
                tgb.chart(figure = "{fig}")

if __name__ == '__main__':
    Gui(page).run(dark_mode=False, 
                  use_reloader=True, 
                  port=8080)