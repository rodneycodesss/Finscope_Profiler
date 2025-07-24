from pyfiglet import figlet_format
from colorama import init, Fore, Style

# Initialize colorama for Windows compatibility
init(autoreset=True)

BOX_WIDTH = 63

def draw_finscope_banner():
    # Use 'block' font for both title and subtitle for a close match
    title_art = figlet_format("FINSCOPE", font="block").rstrip().split("\n")
    subtitle_art = figlet_format("PROFILER", font="block").rstrip().split("\n")
    tagline = "Know Your Investment Personality"

    def box_line(text):
        return Fore.CYAN + Style.BRIGHT + "║" + text.center(BOX_WIDTH) + "║" + Style.RESET_ALL

    box_top = Fore.CYAN + Style.BRIGHT + "╔" + ("═" * BOX_WIDTH) + "╗"
    box_bottom = Fore.CYAN + Style.BRIGHT + "╚" + ("═" * BOX_WIDTH) + "╝" + Style.RESET_ALL

    print(box_top)
    print(box_line(""))
    for line in title_art:
        if line.strip():
            print(box_line(line))
    for line in subtitle_art:
        if line.strip():
            print(box_line(line))
    print(box_line(""))
    print(box_line(tagline))
    print(box_line(""))
    print(box_bottom)

if __name__ == "__main__":
    draw_finscope_banner()
