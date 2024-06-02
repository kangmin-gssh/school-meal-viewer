import json
import flet as ft

with open('./saved/menus.json', 'r', encoding='utf-8') as file:
    data = json.loads(file.read())

def date_format(raw: str):
    month, day = raw[4:6], raw[6:8]
    return f'{month}월 {day}일'

def main(page: ft.Page):
    page.window_width = 400
    page.window_height = 600
    page.title = 'Find today\'s Menu'
    page.fonts = {'pretendard': 'assets/Pretendard-Regular.ttf'}
    page.theme = ft.Theme(font_family='pretendard')

    time_index = None
    date_index = None

    class OptionButton(ft.Container):
        instances: list = []

        def __init__(self, text: str, position: str, index_type: str, index: int):
            super().__init__()
            self.content = ft.Text(text, size=15, weight=ft.FontWeight.W_500)
            self.padding = ft.padding.symmetric(8, 13)
            self.bgcolor = ft.colors.BLUE_50
            self.border_radius = \
                ft.border_radius.only(top_left=20, bottom_left=20) if position == 'left' else \
                ft.border_radius.only() if position == 'middle' else \
                ft.border_radius.only(top_right=20, bottom_right=20) if position == 'right' else \
                ft.border_radius.only()
            self.on_hover = self.when_hover
            self.on_click = self.when_clicked
            self.index_type = index_type
            self.index = index
            self.set_selected()
            OptionButton.instances.append(self)

        def set_selected(self):
            if self.index_type == 'time':
                self.is_selected = (self.index == time_index)
            elif self.index_type == 'date':
                self.is_selected = (self.index == date_index)
            else:
                self.is_selected = None

        @classmethod
        def update_color(cls):
            instance: OptionButton
            for instance in cls.instances:
                instance.set_selected()
                instance.bgcolor = ft.colors.BLUE_200 if instance.is_selected else ft.colors.BLUE_50
                instance.update()

        def when_clicked(self, e: ft.ControlEvent):
            nonlocal time_index, date_index
            nonlocal list_of_meal
            if self.index_type == 'time':
                time_index = self.index
            elif self.index_type == 'date':
                date_index = self.index
            print(time_index, date_index)
            self.update_color()
            self.set_selected()

            if isinstance(time_index, int) and isinstance(date_index, int):
                meals = data[2 + 3 * date_index + time_index]
                if meals == [None]:
                    list_of_meal.controls = [date_text(data[date_index])] + [dish_text('식단이 없습니다 :(')]
                else:
                    list_of_meal.controls = [date_text(data[date_index])] + [dish_text(name) for name in data[2 + 3 * date_index + time_index]]
            else:
                list_of_meal.controls = [dish_text('날짜 및 시간를 선택해주세요 :P')]
            list_of_meal.update()
        
        def when_hover(self, e: ft.ControlEvent):
            self.set_selected()
            self.bgcolor = ft.colors.BLUE_200 if self.is_selected else ft.colors.BLUE_100 if e.data == 'true' else ft.colors.BLUE_50
            self.update()


    def dish_text(name):
        return ft.Text(name, size=18, weight=ft.FontWeight.W_600)
    
    def date_text(date):
        return ft.Text(date_format(date), size=22, weight=ft.FontWeight.W_700)
    
    list_of_meal = ft.ListView(expand=1, auto_scroll=True, spacing=10, controls=[dish_text('날짜 및 시간를 선택해주세요 :P')])

    page.add(
        ft.Row([
            ft.Row([
                OptionButton('아침', 'left', 'time', 0),
                OptionButton('점심', 'middle', 'time', 1),
                OptionButton('저녁', 'right', 'time', 2)
            ], spacing=0),
            ft.Row([
                OptionButton('오늘', 'left', 'date', 0),
                OptionButton('내일', 'right', 'date', 1)
            ], spacing=0)], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
        ft.Container(
            list_of_meal,
            height=500,
            alignment=ft.alignment.top_center, border=ft.border.all(1, ft.colors.GREY), border_radius=5, padding=15)
    )

ft.app(main)
