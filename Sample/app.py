import pygame
from pygame.locals import *
import sys
import os

class App:
    def draw_text(self, font, color, x, y, align='left', text=''):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        if align == 'center':
            text_rect.midtop = (x, y)
        elif align == 'right':
            text_rect.topright = (x, y)
        else:  # left
            text_rect.topleft = (x, y)
        self.screen.blit(text_obj, text_rect)
        
    def draw_scrollbox(self, x, y, width, percent):
        height = self.app_height - y - 30
        scrollbox_width = 4
        scrollbox_height = height // (self.memo_lines_max / self.memo_lines_ouput_max)
        scrollbox_y = y + (height - scrollbox_height) * (percent / 100.0)
        # background scrollbox
        pygame.draw.rect(self.screen, self.scrollbox_background_color, (x, y, scrollbox_width, height), 0)
        # active scroll
        if percent != -1:
            pygame.draw.rect(self.screen, self.white, (x, scrollbox_y, scrollbox_width, scrollbox_height), 0)

    def __init__(self):
        pygame.init()
        self.app_width = 640
        self.app_height = 480
        self.screen = pygame.display.set_mode((self.app_width, self.app_height))
        pygame.display.set_caption('App')
        self.background = pygame.Surface(self.screen.get_size()).convert()
        self.background.fill((7, 18, 22))
        self.black = pygame.Color(0, 0, 0)
        self.white = pygame.Color(255, 255, 255)
        self.gray = pygame.Color(128, 128, 128)
        self.menu_item_color = pygame.Color(58, 69, 73)
        self.memo_background_color = pygame.Color(31, 37, 4)
        self.scrollbox_background_color = pygame.Color(60, 70, 72)
        #self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), 'arial.ttf'), 17)
        self.font = pygame.font.Font(None, 24)
        self.font_height = 24
        self.fps_controller = pygame.time.Clock()
        self.layout_index = 0
        self.main_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        self.main_list_output_max = 17
        self.list_selected_index = 0    
        self.list_selected_offset = 0  
        self.list_selected_item = ''  
        
        self.memo = 'We''ve trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer followup questions, admit its mistakes, challenge incorrect premises, and reject inappropriate requests.\n\n'
        self.memo += 'ChatGPT is a sibling model to InstructGPT, which is trained to follow an instruction in a prompt and provide a detailed response.\n\n' 
        self.memo += 'We are excited to introduce ChatGPT to get users feedback and learn about its strengths and weaknesses. During the research preview, usage of ChatGPT is free.' 
        self.memo += 'We''ve trained a model called ChatGPT which interacts in a conversational way. The dialogue format makes it possible for ChatGPT to answer followup questions, admit its mistakes, challenge incorrect premises, and reject inappropriate requests.\n\n'
        self.memo += 'ChatGPT is a sibling model to InstructGPT, which is trained to follow an instruction in a prompt and provide a detailed response.'
        
        self.memo_line_offset = 0
        self.memo_lines_max = 0
        self.memo_lines_ouput_max = 17

        self.main_loop()

    def main_loop(self):
        while True:
            self.handle_events()
            self.update_screen()
            self.fps_controller.tick(30) #fps limiter

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # L1=K_e, L2=K_TAB, R1=K_t, R2=K_BACKSPACE, X=K_LSHIFT, Y=K_LALT, B=K_LCTRL, A=K_SPACE, SELECT=K_RCTRL, START=K_RETURN, DPADUP=K_UP, DPADDOWN=K_DOWN, DPAFLEFT=K_LEFT, DPADRIGHT=K_RIGHT
                if self.layout_index == 0:
                    if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_SPACE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_UP:
                        if self.list_selected_index > 0:
                            self.list_selected_index -= 1
                    elif event.key == K_DOWN:
                        if self.list_selected_index < len(self.main_list) - 1:
                            self.list_selected_index += 1
                    elif event.key == K_RETURN or event.key == K_LCTRL:
                        self.list_selected_item = self.main_list[self.list_selected_index]
                        self.layout_index = 1
                        self.memo_line_offset = 0
                    
                    if self.list_selected_index > self.main_list_output_max - 1:
                        self.list_selected_offset = self.list_selected_index // self.main_list_output_max * self.main_list_output_max
                    else:
                        self.list_selected_offset = 0
                        
                elif self.layout_index == 1:
                    if event.key == K_ESCAPE or event.key == K_BACKSPACE or event.key == K_SPACE:
                        self.layout_index = 0
                    elif event.key == K_UP:
                        if self.memo_line_offset > 0:
                            self.memo_line_offset -= 1
                    elif event.key == K_DOWN:
                        #if self.memo_line_offset < self.memo_lines_max - 1:
                        if self.memo_line_offset < self.memo_lines_max - self.memo_lines_ouput_max:
                            self.memo_line_offset += 1
                    
                    
    def update_screen(self):
        self.screen.fill((0, 0, 0))
        if self.layout_index == 0:
            self.draw_layout_list()
        elif self.layout_index == 1:
            self.draw_layout_memo()
        
        pygame.display.flip()
        
    def draw_layout_list(self):
        self.draw_text(self.font, self.white, 8, 8, 'left', 'List')
        
        for i, line in enumerate(self.main_list):
            if i < self.list_selected_offset:
                continue
            if i - self.list_selected_offset >= self.main_list_output_max:
                continue
            if i == self.list_selected_index:
                item_background_color = self.white
                item_font_color = self.black
            else:
                item_background_color = self.menu_item_color
                item_font_color = self.white
            
            # Items
            x = 8
            y = self.font_height * (i - self.list_selected_offset + 1) + 8
            width = self.app_width - 16
            height = self.font_height
            pygame.draw.rect(self.screen, item_background_color, (x, y, width, height - 1), 0)
            self.draw_text(self.font, item_font_color, x + 2, y + 4, 'left', self.cut_str(line, 70))
            
            if i == 0:
                self.draw_text(self.font, item_font_color, self.app_width - 60, y + 4, 'center', '< turn on >')
            
    def draw_layout_memo(self):
        self.draw_text(self.font, self.white, 8, 8, 'left', 'Display: ' + self.list_selected_item)
        lines = self.add_line_breaks(self.memo, 64).split('\n')
        self.memo_lines_max = len(lines)
        
        # Scroll
        if self.memo_lines_max > self.memo_lines_ouput_max:
            scroll_percent = self.memo_line_offset * 100 // (self.memo_lines_max - self.memo_lines_ouput_max)
        else:
            scroll_percent = -1
        self.draw_scrollbox(self.app_width - 8, 30, 6, scroll_percent)
        
        self.draw_text(self.font, self.gray, 620, 455, 'right', str(self.memo_line_offset * 100 // (self.memo_lines_max - self.memo_lines_ouput_max)) + '%')
        pygame.draw.rect(self.screen, self.memo_background_color, (9, 30, self.app_width - 24, self.app_height - 60), 0)
        
        # Output lines of text
        for i, line in enumerate(lines):
            if i < self.memo_line_offset:
                continue
            if i - self.memo_line_offset >= self.memo_lines_ouput_max:
                continue
            self.draw_text(self.font, self.white, 18, self.font_height * (i - self.memo_line_offset) + 40, 'left', line)
        
    def cut_str(self, string, n):
        if len(string) > n:
            return string[:n-3] + '...'
        else:
            return string
            
    def add_line_breaks(self, text, n):
        result = ''
        buffer = ''
        count = 0

        for char in text:
            result += char
            buffer += char
            count += 1

            if count == n:
                if ' ' in buffer:
                    last_space_index = buffer.rfind(' ')
                    result = result[:-(len(buffer) - last_space_index)] + '\n' + result[-(len(buffer) - last_space_index):]
                    buffer = buffer[last_space_index + 1:]
                else:
                    result += '\n'
                    buffer = ''
                count = 0

        return result

if __name__ == "__main__":
    app = App()