from PIL import Image
from jinja2 import Environment, PackageLoader, Template
import boto3
import string
import palette
import math

env = Environment(loader=PackageLoader('flossthree', 'templates'))

class Pattern(object):
    floss_num_chart = []# keeps the list of
    avail_symbols = []# symbols that have not yet been used in the chart
    floss_symbol_map = {} # has RGB tuples as keys and the floss identifiers as values
    my_palette = None # What are we making a pattern for?
    image = None # The original image
    rendered_chart = None

    def __init__(self, image, palette_choice):
        self.image = image.convert('RGB')
        # If you need this many symbols, you're doing pixel art wrong
        self.avail_symbols = list(":,.()-=!@#$%^&*+=?;<>~") + list(string.digits) + list(string.ascii_lowercase[::-1]) + list(string.ascii_uppercase[::-1])
        self.my_palette = palette.Palette(palette_choice)

    def build_and_save(self, image_url, image_name):
        self.build_pattern()
        self.render_chart('default')
        self.save_to_s3()

    def save_to_s3(self):
        aws_client = boto3.client

    def save_to_db(self, user_ref):
        session = Session()
        session.add(
            'pattern_requests',
            user_ref
        )
        session.commit()

    def build_pattern(self):
        for row in range(self.image.size[0]):
            templist = []
            for col in range(self.image.size[1]):
                r, g, b = self.image.getpixel((row,col))
                floss_info = self.my_palette.find_floss(r, g, b)
                floss_num = floss_info[0]
                if floss_num not in self.floss_symbol_map:
                    floss_data = {'symbol': self.avail_symbols.pop(),
                                  'count': 0,
                                  'hex': floss_info[1],
                                  'text_color': self.get_text_color(r, g, b)}
                    self.floss_symbol_map[floss_num] = floss_data
                self.floss_symbol_map[floss_num]['count'] += 1
                templist.append(floss_num)
            self.floss_num_chart.append(templist)
        return

    def get_text_color(self, red, green, blue):
        bright_sqrd = .299*(red**2) + .587*(green**2) + .114*(blue**2)
        if bright_sqrd <= (130**2):
            return 'FFFFFF'
        else:
            return '000000'

    def _get_context_data(self):
        return {'floss_symbol_map': self.floss_symbol_map,
                'floss_num_chart': self.floss_num_chart,
        }
    def render_chart(self, style):
        if style == 'print':
            self.render_print()
        else:
            self.render_HTML()

    def render_HTML(self):
        template = env.get_template('screen.html')
        context_data = self._get_context_data()
        print(context_data)
        rendered = template.render(self._get_context_data())
        with open('renderedchart.html', 'w') as htmlfile:
            htmlfile.write(rendered)
        return


    def _get_print_context_data(self):
        page_data = self._divide_pattern((60, 75))
        new_context = self._get_context_data()
        new_context.update({'divided_pattern': page_data})
        return new_context

    # FIXME: make views
    def render_print(self):
        template = env.get_template('print.html')
        rendered = template.render(self._get_print_context_data())
        with open('renderedchart.html', 'w') as htmlfile:
            htmlfile.write(rendered)



    def _divide_pattern(self, page_size):

        """
        This function should take the pattern and divide it into smaller, print-friendly patterns

        :param floss_num_chart: see floss_num_chart from floss.py; array of arrays
        :param page_size: tuple of how big each divided chart should be for printing; width, height
        :return: The chart, divided for printing.  Divided should be no larger than 60 x 75
        """

        tmp_chart = self.floss_num_chart.copy()
        floss_size = (float(len(tmp_chart[0])), float(len(tmp_chart)))
        chart_size = (int(math.ceil(floss_size[0]/page_size[0])), int(math.ceil(floss_size[1]/page_size[1])))
        num_patterns = chart_size[0] * chart_size[1]
        divided_patterns = []

        #TEST CODE
        print("chart_size = ", chart_size)
        print("num_patterns = ", num_patterns)

        while len(tmp_chart):
            divided_rows = tmp_chart[:60]
            while len(divided_rows[0]):
                templist = []
                for row in divided_rows:
                    templist.append(row[:60])
                    del row[:60]  # Note, decrease this number compared to number above to have repeated rows in table break
                divided_patterns.append(templist)
            del tmp_chart[:60]

        return divided_patterns
