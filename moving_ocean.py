import curses
import time

def main(stdscr):
    # Clear screen
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    
    ocean = ['0' * (sw - 1) for _ in range(sh - 1)]  # Ensure ocean width and height fit within the window
    
    while True:
        w.clear()
        
        for i in range(min(sh - 1, len(ocean))):
            try:
                w.addstr(i, 0, ocean[i])
            except curses.error:
                pass
        
        ocean = ocean[1:] + [ocean[0]]
        
        w.refresh()
        
        key = w.getch()
        if key == ord('q'):
            break
        
        time.sleep(0.1)

curses.wrapper(main)
