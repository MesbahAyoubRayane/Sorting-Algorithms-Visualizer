import pygame as pyg
import random as rnd
from sorting_algorithms import heap_sort as sorting_algorithm # this is the algorithm which will be visualized
from typing import Callable

pyg.init()
# Window constants
WINDOW_W , WINDOW_H = 1000,400
WINDOW_BG           = "black"
WINDOW_CAPTION      = "Sorting Visualization"

# pygame constants
CLOCK   = pyg.time.Clock()
DISPLAY = pyg.display
SCREEN  = DISPLAY.set_mode((WINDOW_W,WINDOW_H))
DISPLAY.set_caption(WINDOW_CAPTION)
# Time & Speed
FPS       = 30
MIN_FPS   = 1
MAX_FPS   = 60
FPS_DELTA = 5
PAUSED    = False

# BARS
BARS_COLOR_TO_RIGHT = "green"
BARS_COLOR_TO_LEFT  = "red"
BARS_COLOR         = BARS_COLOR_TO_RIGHT
BARS_HEIGHT        = int(WINDOW_H * 0.9) # pixels
BARS_MARGING       = 1 # pixels
MIN_VALUE          = 0
MAX_VALUE          = 1000
NUMBER_OF_BARS     = 200
NUMBER_OF_MARGINS  = NUMBER_OF_BARS - 1
BAR_WIDTH          = (WINDOW_W - NUMBER_OF_MARGINS * BARS_MARGING) // NUMBER_OF_BARS # in pixel
BARS_VALUES        = [rnd.randint(MIN_VALUE,MAX_VALUE) for _ in range(NUMBER_OF_BARS)]
MAX_BARS_VALUE     = max(BARS_VALUES)

# Sorting algorithm
SORT:Callable[[list[int]], list[list[int]]]      = sorting_algorithm
SORTING_STEPS           = [BARS_VALUES]+SORT(BARS_VALUES.copy())
CURRENT_STEP_DIRECTION  = 1 # 1 to the right which mean the next step represents a more sorted array , -1 for the left if you want to back track
CURRENT_STEP            = 0

def render() -> None:
    def render_text():
        font = pyg.font.Font(None,16)
        text = font.render("FPS:"+str(float(FPS)),True,"green")
        text_rect = text.get_rect(center=(30,10))
        SCREEN.blit(text,text_rect)

    SCREEN.fill(WINDOW_BG)
    x0=0
    for v in SORTING_STEPS[CURRENT_STEP]:
        pyg.draw.rect(
            SCREEN,
            BARS_COLOR,
            pyg.Rect(
                x0,
                WINDOW_H - BARS_HEIGHT*v//MAX_BARS_VALUE,
                BAR_WIDTH,
                BARS_HEIGHT*v//MAX_BARS_VALUE))
        x0 =  x0 + BAR_WIDTH + BARS_MARGING
    render_text()
    DISPLAY.update()
    
def stop(events:list[pyg.event.Event]) -> bool:
    for event in events:
        if event.type == pyg.QUIT:
            return True
    return False

def handle_keyborad_events(events:list[pyg.event.Event]) -> None:
    global CURRENT_STEP_DIRECTION,PAUSED,BARS_COLOR,FPS
    for event in events:
        if event.type == pyg.KEYDOWN :
            match event.key:
                case pyg.K_RIGHT:
                    CURRENT_STEP_DIRECTION=1
                    BARS_COLOR = BARS_COLOR_TO_RIGHT
                case pyg.K_LEFT:
                    CURRENT_STEP_DIRECTION=-1
                    BARS_COLOR = BARS_COLOR_TO_LEFT
                case pyg.K_p:
                    PAUSED = not PAUSED
                case pyg.K_UP:
                    FPS = min(max(MIN_FPS,FPS+FPS_DELTA),MAX_FPS)
                case pyg.K_DOWN:
                    FPS = min(max(MIN_FPS,FPS-FPS_DELTA),MAX_FPS)

def handle_tick_event() -> None:
    global CURRENT_STEP
    if not PAUSED:
        CURRENT_STEP += CURRENT_STEP_DIRECTION
        CURRENT_STEP = max(min(CURRENT_STEP,len(SORTING_STEPS)-1),0)


def main():
    events=[]
    while not stop(events):
        events = pyg.event.get()
        # handle events
        handle_tick_event()
        handle_keyborad_events(events)
        # render the image
        render()
        # synch time
        CLOCK.tick(FPS)
    # cleaning
    pyg.quit()

if __name__ == "__main__":
    main()