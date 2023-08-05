import sys
import time
from datetime import datetime
import curses, curses.panel
from discord import VoiceChannel, CategoryChannel
from dline.client.channellog import PrivateChannel
from dline.input.messageEdit import MessageEdit
from dline.utils.log import log
from dline.ui.ui_utils import get_role_color
from dline.ui.userlist import UserList
from dline.utils.quicksort import quick_sort_channels, quick_sort_channel_logs

hasItalic = False
if sys.version_info >= (3,7):
    hasItalic = True

line = 0

colorNames = {
        'black':curses.COLOR_BLACK+1,
        'red':curses.COLOR_RED+1,
        'green':curses.COLOR_GREEN+1,
        'yellow':curses.COLOR_YELLOW+1,
        'blue':curses.COLOR_BLUE+1,
        'magenta':curses.COLOR_MAGENTA+1,
        'cyan':curses.COLOR_CYAN+1,
        'white':curses.COLOR_WHITE+1
}

class CursesUi:
    def __init__(self, lock):
        self.lock = lock
        self.frameWins = []
        self.contentWins = []

        self.messageEdit = None
        self.start_pos = 0
        self.views = {}
        self.isInitialized = False
        self.areLogsRead = False
        self.channel_log_offset = -1
        self.funcs = []
        # Windows
        self.topWin = None
        self.leftWin = None
        self.editWin = None
        self.chatWin = None
        self.chatWinWidth = 0
        self.userWin = None
        self.contentWins = []
        self.frameWin = None
        # Visibility
        self.separatorsVisible = True
        self.topWinVisible = True
        self.leftWinVisible = True
        self.userWinVisible = False

    def run(self, screen):
        self.screen = screen
        self.initScreen()
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.messageEdit = MessageEdit(self.max_x)

        self.makeFrameWin()
        self.makeDisplay()
        try:
            self.leftWinWidth = int(self.max_x // gc.settings["left_win_divider"])
            self.userWinWidth = int(self.max_x // gc.settings["user_win_divider"])
        except:
            self.leftWinWidth = int(self.max_x // gc.settings["left_bar_divider"])
            self.userWinWidth = int(self.max_x // gc.settings["user_bar_divider"])
        if self.leftWinWidth < 10:
            self.leftWinWidth = 10
        if self.userWinWidth < 10:
            self.userWinWidth = 10

        if self.topWinVisible:
            self.makeTopWin()
        self.makeBottomWin()
        if self.leftWinVisible:
            self.makeLeftWin()
        if self.userWinVisible:
            self.makeUserWin()
        self.makeChatWin()
        self.redrawFrames()

        self.isInitialized = True

        self.refreshAll()

    def initScreen(self):
        self.screen.keypad(True)
        self.screen.clear()
        curses.cbreak()
        curses.noecho()
        self.colors = {}
        curses.use_default_colors()
        curses.curs_set(1)
        for i in range(1,9):
            curses.init_pair(i, i-1, -1)
        for key,value in colorNames.items():
            self.colors[key] = curses.color_pair(value)
        self.separatorsVisible = gc.settings["show_separators"]
        try:
            self.topWinVisible = gc.settings["show_top_win"]
            self.leftWinVisible = gc.settings["show_left_win"]
        except:
            self.topWinVisible = gc.settings["show_top_bar"]
            self.leftWinVisible = gc.settings["show_left_bar"]
        try:
            self.userWinVisible = gc.settings["show_user_win"]
        except:
            pass

    def resize(self):
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.clearWins()
        try:
            if self.separatorsVisible:
                self.makeFrameWin(resize=True)
            if self.topWinVisible:
                self.makeTopWin(resize=True)
            self.makeBottomWin(resize=True)
            if self.leftWinVisible:
                self.makeLeftWin(resize=True)
            if self.userWinVisible:
                self.makeUserWin(resize=True)
            self.makeChatWin(resize=True)
            self.makeDisplay(resize=True)
        except Exception as e:
            log("Failed to resize windows. Error: {}".format(e))
        self.messageEdit.termWidth = self.messageEdit.width = self.max_x
        self.redrawFrames()
        draw_screen()

    def clearWins(self):
        self.frameWin.clear()
        for win in self.contentWins:
            win.erase()
        curses.doupdate()

    def makeFrameWin(self, resize=False):
        if resize:
            self.frameWin.resize(self.max_y,self.max_x)
            return
        self.frameWin = curses.newwin(self.max_y,self.max_x, 0,0)

    def makeTopWin(self, resize=False):
        if resize:
            self.topWin.resize(1,self.max_x)
            return
        content = curses.newwin(1,self.max_x, 0,0)
        self.topWin = content
        self.topWin.leaveok(True)

        self.contentWins.append(content)

    def makeBottomWin(self, resize=False):
        if resize:
            self.editWin.resize(1,self.max_x)
            self.editWin.mvwin(self.max_y-1,0)
            return
        content = curses.newwin(1,self.max_x, self.max_y-1,0)
        content.keypad(True)
        content.nodelay(True)
        self.editWin = content

        self.contentWins.append(content)

    def makeLeftWin(self, resize=False):
        # Win has 2 elements: frame and content pad
        width = self.leftWinWidth
        y_offset = 0
        if self.topWinVisible:
            y_offset = 2

        if resize:
            self.leftWin.resize(self.max_y-y_offset-2,width-1)
            return
        content = curses.newwin(self.max_y-y_offset-2,width-1, y_offset,0)
        self.leftWin = content
        self.leftWin.leaveok(True)

        self.contentWins.append(content)

    def makeUserWin(self, resize=False):
        width = self.userWinWidth
        y_offset = 0
        if self.topWinVisible:
            y_offset = 2

        if resize:
            self.userWin.resize(self.max_y-y_offset-2,width-1)
            return
        content = curses.newwin(self.max_y-y_offset-2,width-1, y_offset,self.max_x-width)
        self.userWin = content
        self.userWin.leaveok(True)

        self.contentWins.append(content)

    def makeChatWin(self, resize=False):
        x_offset = 0;width = self.max_x
        if self.leftWinVisible:
            x_offset = self.leftWinWidth+1
            width -= x_offset
        if self.userWinVisible:
            width -= self.userWinWidth+1
        y_offset = 0
        if self.topWinVisible:
            y_offset = 2

        if resize:
            self.chatWin.resize(self.max_y-y_offset-2,width)
            return
        content = curses.newwin(self.max_y-y_offset-2,width, y_offset,x_offset)
        self.chatWin = content
        self.chatWinWidth = width
        self.chatWin.leaveok(True)

    def makeDisplay(self, resize=False): #TODO: Make display separate view
        if resize:
            self.displayWin.resize(self.max_y,self.max_x)
            return
        self.displayWin = curses.newwin(self.max_y,self.max_x, 0,0)
        self.displayWin.keypad(True)
        self.displayWin.leaveok(True)
        self.displayWin.erase()
        self.displayPanel = curses.panel.new_panel(self.displayWin)
        self.displayPanel.hide()
        curses.panel.update_panels();self.screen.refresh()

    def refreshAll(self):
        for win in self.contentWins:
            win.noutrefresh()
        self.chatWin.noutrefresh()
        curses.doupdate()

    def redrawFrames(self):
        # redraw top frame
        y_offset = 0
        color = gc.ui.colors[gc.settings['separator_color']]
        self.frameWin.attron(color)
        try:
            if self.topWinVisible and self.separatorsVisible:
                y_offset = 1
                self.frameWin.hline(y_offset,0, curses.ACS_HLINE, self.max_x)
            # redraw bottom frame
            if self.separatorsVisible:
                self.frameWin.hline(self.max_y-2,0, curses.ACS_HLINE, self.max_x)
            # redraw left frame
            if self.leftWinVisible and self.separatorsVisible:
                self.frameWin.vline(y_offset+1,self.leftWinWidth, curses.ACS_VLINE,
                        self.max_y-y_offset-3)
                self.frameWin.addch(y_offset,self.leftWinWidth, curses.ACS_TTEE)
                self.frameWin.addch(self.max_y-2,self.leftWinWidth, curses.ACS_BTEE)
            # redraw user frame
            if self.userWinVisible and self.separatorsVisible:
                self.frameWin.vline(y_offset+1,self.max_x-self.userWinWidth-1, curses.ACS_VLINE,
                        self.max_y-y_offset-3)
                self.frameWin.addch(y_offset,self.max_x-self.userWinWidth-1, curses.ACS_TTEE)
                self.frameWin.addch(self.max_y-2,self.max_x-self.userWinWidth-1, curses.ACS_BTEE)
        except Exception as e:
            # if we're here, text has failed to draw
            log("Failed to draw frames. Error: {}".format(e))
        self.frameWin.attroff(color)
        self.frameWin.refresh()

    def toggleDisplay(self):
        if self.displayPanel.hidden():
            self.displayPanel.show()
            curses.curs_set(0)
        else:
            self.displayPanel.hide()
            curses.curs_set(1)

        curses.panel.update_panels();self.screen.refresh()
        if self.displayPanel.hidden():
            self.redrawFrames()

from dline.utils.globals import gc

def draw_screen():
    log("Updating")
    # init current channel if needed
    if gc.client.current_channel not in gc.channels_entered:
        gc.client.wait_until_client_task_completes(\
                (gc.client.init_channel,gc.client.current_channel))
    if gc.ui.topWinVisible:
        gc.ui_thread.wait_until_ui_task_completes((draw_top_win,))
    if gc.ui.leftWinVisible:
        gc.ui_thread.wait_until_ui_task_completes((draw_left_win,))
    if gc.ui.userWinVisible:
        gc.ui_thread.wait_until_ui_task_completes((draw_user_win,))
    if gc.guild_log_tree is not None:
        gc.ui_thread.wait_until_ui_task_completes((draw_channel_log,))
    gc.ui_thread.wait_until_ui_task_completes((draw_edit_win,))
    curses.doupdate()

def draw_top_win():
    topWin = gc.ui.topWin
    width = topWin.getmaxyx()[1]
    color = gc.ui.colors[gc.settings["guild_display_color"]]

    guildName = gc.client.current_guild.name

    topic = ""
    if gc.client.current_channel.topic is not None:
        topic = gc.client.current_channel.topic
    # if there is no channel topic, just print the channel name
    else:
        topic = gc.client.current_channel.name
    topic = topic.replace("\n", " ")
    if len(topic) >= width//2:
        topic = topic[:width//2-3] + "..."
    topicOffset = width//2-len(topic)//2

    # sleep required to get accurate user count
    time.sleep(0.05)
    try:
        online = str(gc.client.online)
        online_text = "Users online: " + online
        onlineOffset = width-len(online_text)-1

        topWin.erase()

        topWin.addstr(0,0, "Guild: ")
        topWin.addstr(guildName, color)

        topWin.addstr(0,topicOffset, topic)

        topWin.addstr(0,onlineOffset, "Users online: ", color)
        topWin.addstr(online)
    except Exception as e:
        # if we're here, text has failed to draw
        log("Failed to draw top window. Error: {}".format(e))

    topWin.noutrefresh()

def set_display(string, attrs=0):
    display = gc.ui.displayWin
    gc.ui.toggleDisplay()
    display.addstr(string + '\n\n', attrs)
    display.addstr("(press q to quit this dialog)")
    display.refresh()
    while True:
        ch = display.getch()
        if ch == ord('q'):
            break
        time.sleep(0.1)
    display.clear()
    gc.ui.toggleDisplay()
    draw_screen()

def draw_left_win():
    leftWin = gc.ui.leftWin
    left_win_height, left_win_width = leftWin.getmaxyx()

    if gc.ui.separatorsVisible:
        length = 0
        length = gc.term.height - gc.settings["margin"]

    # Create a new list so we can preserve the guild's channel order
    channel_logs = []

    for servlog in gc.guild_log_tree:
        if servlog.guild is gc.client.current_guild:
            for chanlog in servlog.logs:
                channel_logs.append(chanlog)
            break

    channel_logs = quick_sort_channel_logs(channel_logs)

    leftWin.erase()

    # TODO: Incorperate guilds into list
    for idx, clog in enumerate(channel_logs):
        # should the guild have *too many channels!*, stop them
        # from spilling over the screen
        try:
            if idx == left_win_height-1:
                leftWin.addstr(idx,0, "(more)", gc.ui.colors["green"])
                break

            # don't print categories or voice chats
            # TODO: this will break on private messages
            if isinstance(clog.channel, VoiceChannel) or \
                    isinstance(clog.channel, CategoryChannel):
                continue
            text = clog.name
            length = len(text)

            offset = 0
            if gc.settings["number_channels"]:
                offset = 3
                if idx >= 9:
                    offset = 4

            if length > left_win_width-offset:
                if gc.settings["truncate_channels"]:
                    text = text[0:left_win_width - offset]
                else:
                    text = text[0:left_win_width - 3 - offset] + "..."

            leftWin.move(idx,0)
            if gc.settings["number_channels"]:
                leftWin.addstr(str(idx+1) + ". ")
            if clog.channel is gc.client.current_channel:
                leftWin.addstr(text, gc.ui.colors[gc.settings["current_channel_color"]])
            else:
                if clog.channel is not channel_logs[0]:
                    pass

                if clog.unread and gc.settings["blink_unreads"]:
                    color = gc.settings["unread_channel_color"]
                    if "blink_" in color:
                        split = color.split("blink_")[1]
                        color = gc.ui.colors[split]|curses.A_BLINK
                    elif "on_" in color:
                        color = gc.ui.colors[color.split("on_")[1]]
                    leftWin.addstr(text, color)
                elif clog.mentioned_in and gc.settings["blink_mentions"]:
                    color = gc.settings["unread_mention_color"]
                    if "blink_" in color:
                        color = gc.ui.colors[color.split("blink_")[1]]
                    leftWin.addstr(text, color)
                else:
                    leftWin.addstr(text)
        except Exception as e:
            # if we're here, text has failed to draw
            log("Failed to draw left window. Error: {}".format(e))

    leftWin.noutrefresh()

def draw_user_win():
    userWin = gc.ui.userWin
    height, width = userWin.getmaxyx()

    userWin.erase()

    for idx,member in enumerate(gc.client.current_channel.members):
        try:
            if idx+2 > height:
                userWin.addstr(idx,0, "(more)", gc.ui.colors["green"])
                break
            name = member.display_name
            if len(name) >= width:
                name = name[:width-4] + "..."

            userWin.addstr(idx,0, name)
        except Exception as e:
            # if we're here, text has failed to draw
            log("Failed to draw user window. Error: {}".format(e))

    userWin.noutrefresh()

def draw_edit_win(update=False):
    editWin = gc.ui.editWin
    promptText = gc.client.prompt
    offset = len(promptText)+5
    width = gc.ui.max_x-offset
    edit = gc.ui.messageEdit

    borderColor = gc.ui.colors[gc.settings["prompt_border_color"]]
    hasHash = False
    hashColor = 0
    promptColor = 0
    if gc.client.prompt != gc.settings["default_prompt"]:
        hasHash = True
        hashColor = gc.ui.colors[gc.settings["prompt_hash_color"]]
    promptColor = gc.ui.colors[gc.settings["prompt_color"]]

    edit.setPrompt(gc.client.prompt)
    try:
        editWin.erase()
        editWin.addstr(0,0, "[", borderColor)
        if not hasHash:
            editWin.addstr(gc.settings["default_prompt"], promptColor)
        else:
            editWin.addstr("#", hashColor)
            editWin.addstr(promptText, promptColor)
        editWin.addstr("]: ", borderColor)
        try:
            text_data, text_data_pos, start_pos = edit.getCurrentData()
        except:
            text_data, text_data_pos, start_pos = ('', 0, 0)
        pos = text_data_pos-start_pos
        data = (text_data[start_pos:start_pos+width-1], pos)
        editWin.addstr(0,offset, data[0])
        editWin.move(0,offset+data[1])
        editWin.noutrefresh()
        if update:
            curses.doupdate()
    except Exception as e:
        # if we're here, text has failed to draw
        log("Failed to draw edit window. Error: {}".format(e))

def draw_guildlist():
    display = gc.ui.displayWin
    gc.ui.toggleDisplay()
    # Write guildlist to screen
    if len(gc.client.guilds) == 0:
        display.addstr("Error: You are not in any guilds.", gc.ui.colors["red"])
        while True:
            ch = display.getch()
            if ch == ord('q'):
                break
            time.sleep(0.1)
        display.clear()
        gc.ui.toggleDisplay()
        return

    buf = []
    for slog in gc.guild_log_tree:
        name = slog.name

        if slog.guild is gc.client.current_guild:
            buf.append((name, gc.ui.colors[gc.settings["current_channel_color"]]))
            continue

        string = ""
        for clog in slog.logs:
            if clog.mentioned_in:
                attrs = curses.A_NORMAL
                color = gc.settings["unread_mention_color"]
                if 'blink' in gc.settings["unread_mention_color"]:
                    if gc.settings["blink_mentions"]:
                        attrs = curses.A_BLINK
                    color = color.split('blink_')[1]
                string = (name, gc.ui.colors[color]|attrs)
                break
            elif clog.unread:
                attrs = curses.A_NORMAL
                color = gc.settings["unread_channel_color"]
                if 'blink' in gc.settings["unread_channel_color"]:
                    if gc.settings["blink_unreads"]:
                        attrs = curses.A_BLINK
                    color = color.split('blink_')[1]
                string = (name, gc.ui.colors[color]|attrs)
                break

        if string == "":
            string = (name, gc.ui.colors[gc.settings["text_color"]])

        buf.append(string)
    line_offset = 0
    while True:
        display.clear()
        display.addstr(0,0, "Available Guilds:", gc.ui.colors["yellow"])
        display.hline(1,0, curses.ACS_HLINE, gc.ui.max_x)
        for serv_id, serv in enumerate(buf[line_offset:line_offset+(gc.ui.max_y-5)]):
            color = serv[1]
            display.addstr(2+serv_id,0, serv[0], color)
        display.addstr(2+serv_id+2,0, "(press q to quit this dialog)", gc.ui.colors["green"])
        ch = display.getch()
        if ch == ord('q'):
            break
        if len(buf) > (gc.ui.max_y-5):
            if ch == curses.KEY_UP:
                line_offset -= 1
            elif ch == curses.KEY_DOWN:
                line_offset += 1
            if line_offset < 0:
                line_offset = 0
            elif len(buf) > (gc.ui.max_y-5) and line_offset > (len(buf)-(gc.ui.max_y-5)):
                line_offset = len(buf)-(gc.ui.max_y-5)
        time.sleep(0.01)
    gc.ui.toggleDisplay()
    gc.ui.refreshAll()
    draw_screen()

def draw_channellist():
    display = gc.ui.displayWin
    gc.ui.toggleDisplay()
    # Write guildlist to screen
    if len(gc.client.guilds) == 0:
        display.addstr("Error: You are not in any guilds.", gc.ui.colors["red"])
        while True:
            ch = display.getch()
            if ch == ord('q'):
                break
            time.sleep(0.1)
        display.clear()
        gc.ui.toggleDisplay()
        return

    if len(gc.client.current_guild.channels) == 0:
        display.addstr("Error: Does this guild not have any channels?", gc.ui.colors["red"])
        while True:
            ch = display.getch()
            if ch == ord('q'):
                break
            time.sleep(0.1)
        display.clear()
        gc.ui.toggleDisplay()
        return

    channels = quick_sort_channels(list(gc.client.current_guild.channels))

    buf = []
    for channel in channels:
        if (not isinstance(channel, VoiceChannel) and \
                not isinstance(channel, CategoryChannel)):
            if isinstance(channel, PrivateChannel) or \
                    channel.permissions_for(channel.guild.me).read_messages:
                buf.append((channel.name, 0))

    line_offset = 0
    while True:
        display.clear()
        display.addstr(0,0, "Available channels in ", gc.ui.colors["yellow"])
        display.addstr(gc.client.current_guild.name, gc.ui.colors["magenta"])
        display.hline(1,0, curses.ACS_HLINE, gc.ui.max_x)
        for chan_id, chan in enumerate(buf[line_offset:line_offset+(gc.ui.max_y-5)]):
            color = chan[1]
            display.addstr(2+chan_id,0, chan[0], color)
        display.addstr(2+chan_id+2,0, "(press q to quit this dialog)", gc.ui.colors["green"])
        ch = display.getch()
        if ch == ord('q'):
            break
        if len(buf) > (gc.ui.max_y-5):
            if ch == curses.KEY_UP:
                line_offset -= 1
            elif ch == curses.KEY_DOWN:
                line_offset += 1
            if line_offset < 0:
                line_offset = 0
            elif len(buf) > (gc.ui.max_y-5) and line_offset > (len(buf)-(gc.ui.max_y-5)):
                line_offset = len(buf)-(gc.ui.max_y-5)
        time.sleep(0.01)
    gc.ui.toggleDisplay()
    gc.ui.refreshAll()
    draw_screen()

def draw_emojilist():
    display = gc.ui.displayWin
    gc.ui.toggleDisplay()
    # Write guildlist to screen
    if len(gc.client.guilds) == 0:
        display.addstr("Error: You are not in any guilds.", gc.ui.colors["red"])
        while True:
            ch = display.getch()
            if ch == ord('q'):
                break
            time.sleep(0.1)
        display.clear()
        gc.ui.toggleDisplay()
        draw_screen()
        return

    emojis = []
    guild_emojis = None

    try: guild_emojis = gc.client.current_guild.emojis
    except: pass

    if guild_emojis is not None and guild_emojis != "":
        for emoji in guild_emojis:
            emojis.append((':' + emoji.name + ':', gc.ui.colors["yellow"]))

    line_offset = 0
    while True:
        display.clear()
        display.addstr(0,0, "Available emojis in ", gc.ui.colors["yellow"])
        display.addstr(gc.client.current_guild.name, gc.ui.colors["magenta"])
        display.hline(1,0, curses.ACS_HLINE, gc.ui.max_x)
        for emoji_id, emoji in enumerate(emojis[line_offset:line_offset+(gc.ui.max_y-5)]):
            color = emoji[1]
            display.addstr(2+emoji_id,0, emoji[0], color)
        display.addstr(2+emoji_id+2,0, "(press q to quit this dialog)", gc.ui.colors["green"])
        ch = display.getch()
        if ch == ord('q'):
            break
        if len(emojis) > (gc.ui.max_y-5):
            if ch == curses.KEY_UP:
                line_offset -= 1
            elif ch == curses.KEY_DOWN:
                line_offset += 1
            if line_offset < 0:
                line_offset = 0
            elif len(emojis) > (gc.ui.max_y-5) and line_offset > (len(emojis)-(gc.ui.max_y-5)):
                line_offset = len(emojis)-(gc.ui.max_y-5)
        time.sleep(0.01)
    gc.ui.toggleDisplay()
    gc.ui.refreshAll()
    draw_screen()

def draw_userlist():
    display = gc.ui.displayWin
    gc.ui.toggleDisplay()
    if len(gc.client.guilds) == 0:
        display.addstr("Error: You are not in any guilds.", gc.ui.colors["red"])
        while True:
            ch = display.getch()
            if ch == ord('q'):
                break
            time.sleep(0.1)
        display.clear()
        gc.ui.toggleDisplay()
        draw_screen()
        return

    if len(gc.client.current_guild.channels) == 0:
        display.addstr("Error: Does this guild not have any channels?", gc.ui.colors["red"])
        while True:
            ch = display.getch()
            if ch == ord('q'):
                break
            time.sleep(0.1)
        display.clear()
        gc.ui.toggleDisplay()
        draw_screen()
        return

    nonroles = UserList(gc.ui.colors)
    admins = UserList(gc.ui.colors)
    mods = UserList(gc.ui.colors)
    bots = UserList(gc.ui.colors)
    everything_else = UserList(gc.ui.colors)

    for member in gc.client.current_guild.members:
        if member is None: continue # happens if a member left the guild

        if member.top_role.name.lower() == "admin":
            admins.add(member, " - (Admin)")
        elif member.top_role.name.lower() == "mod":
            mods.add(member, " - (Mod)")
        elif member.top_role.name.lower() == "bot":
            bots.add(member, " - (Bot)")
        elif member.top_role.position == 0:
            nonroles.add(member, "")
        else:
            everything_else.add(member, " - " + member.top_role.name)


    # the final buffer that we're actually going to print
    buf = []

    if admins is not None:
        for user in admins.sort():
            buf.append(user)
    if mods is not None:
        for user in mods.sort():
            buf.append(user)
    if bots is not None:
        for user in bots.sort():
            buf.append(user)
    if everything_else is not None:
        for user in everything_else.sort():
            buf.append(user)
    if nonroles is not None:
        for user in nonroles.sort():
            buf.append(user)

    line_offset = 0
    while True:
        display.clear()
        display.addstr(0,0, "Members in ", gc.ui.colors["yellow"])
        display.addstr(gc.client.current_guild.name, gc.ui.colors["magenta"])
        display.hline(1,0, curses.ACS_HLINE, gc.ui.max_x)
        for user_id, user in enumerate(buf[line_offset:line_offset+(gc.ui.max_y-5)]):
            color = user[1]
            display.addstr(2+user_id,0, user[0], color)
        display.addstr(2+user_id+2,0, "(press q to quit this dialog)", gc.ui.colors["green"])
        ch = display.getch()
        if ch == ord('q'):
            break
        if len(buf) > (gc.ui.max_y-5):
            if ch == curses.KEY_UP:
                line_offset -= 1
            elif ch == curses.KEY_DOWN:
                line_offset += 1
            if line_offset < 0:
                line_offset = 0
            elif len(buf) > (gc.ui.max_y-5) and line_offset > (len(buf)-(gc.ui.max_y-5)):
                line_offset = len(buf)-(gc.ui.max_y-5)
        time.sleep(0.01)
    gc.ui.toggleDisplay()
    gc.ui.refreshAll()
    draw_screen()

def draw_help(terminateAfter=False):
    display = gc.ui.displayWin
    gc.ui.toggleDisplay()
    display.clear()
    buf = [
        [("Launch Arguments", gc.ui.colors["green"])],
        [("-----", gc.ui.colors["red"])],
        [("--copy-skeleton", gc.ui.colors["yellow"]),
            ('---', gc.ui.colors["cyan"]), ("copies template settings", 0)],
        [("This file can be found at ~/.config/dline/config.yaml", gc.ui.colors["cyan"])],
        [],
        [("--store-token", gc.ui.colors["yellow"]),
            ('---', gc.ui.colors["cyan"]), ("stores your token", 0)],
        [("This file can be found at ~/.config/dline/token", gc.ui.colors["cyan"])],
        [],
        [("--config-path", gc.ui.colors["yellow"]),
            ('---', gc.ui.colors["cyan"]), ("specify a specific config path", 0)],
        [("--token-path", gc.ui.colors["yellow"]),
            ('---', gc.ui.colors["cyan"]), ("specify a specific token path", 0)],
        [],
        [("Available Commands", gc.ui.colors["green"])],
        [("-----", gc.ui.colors["red"])],
        [("/channel", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("switch to channel - (alias: c)", 0)],
        [("/guild", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("switch guild - (alias: gld)", 0)],
        [("Note: These commands can now fuzzy-find!", gc.ui.colors["cyan"])],
        [],
        [("/dm", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("switch to private messages", 0)],
        [],
        [("/guilds", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("list available guilds", 0)],
        [("/channels", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("list available channels", 0)],
        [("/users", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("list guild users", 0)],
        [("/emojis", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("list guild emojis", 0)],
        [],
        [("/nick", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("change your guild nick", 0)],
        [("/game or /activity", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("change your activity status", 0)],
        [("/file", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("upload a file via path", 0)],
        [("/status", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("change online presence", 0)],
        [("This can be either online, offline, away, or dnd", gc.ui.colors["cyan"])],
        [],
        [("/cX", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("shorthand to change channel (Ex: /c1)", 0)],
        [("This can be configured to start at 0 in your config", gc.ui.colors["cyan"])],
        [],
        [("/quit", gc.ui.colors["yellow"]),
            ('-', gc.ui.colors["cyan"]), ("exit dline", 0)],
        [],
        [],
        [("(Press q to quit this dialog)", gc.ui.colors["green"])]
    ]

    line_offset = 0
    # needed for --help flag
    curses.cbreak()
    curses.noecho()
    while True:
        display.clear()
        for line_id, line in enumerate(buf[line_offset:line_offset+(gc.ui.max_y)]):
            display.move(line_id,0)
            for seg_id, segment in enumerate(line):
                if segment[0] == '-----':
                    display.addstr('-'*45, segment[1])
                    continue
                display.addstr(segment[0] + ' ', segment[1])
        ch = display.getch()
        if ch == ord('q'):
            break
        if len(buf) > (gc.ui.max_y-5):
            if ch == curses.KEY_UP:
                line_offset -= 1
            elif ch == curses.KEY_DOWN:
                line_offset += 1
            elif ch == curses.KEY_PPAGE:
                line_offset -= 5
            elif ch == curses.KEY_NPAGE:
                line_offset += 5
            if line_offset < 0:
                line_offset = 0
            elif len(buf) > (gc.ui.max_y-5) and line_offset > (len(buf)-(gc.ui.max_y-5)):
                line_offset = len(buf)-(gc.ui.max_y-5)
        time.sleep(0.01)
    if terminateAfter:
        raise SystemExit
    gc.ui.toggleDisplay()
    gc.ui.refreshAll()
    draw_screen()

def draw_channel_log():
    chatWin = gc.ui.chatWin
    ft = None
    doBreak = False
    for guild_log in gc.guild_log_tree:
        if guild_log.guild is gc.client.current_guild:
            for channel_log in guild_log.logs:
                if channel_log.channel is gc.client.current_channel:
                    if isinstance(channel_log.channel, VoiceChannel) or \
                            isinstance(channel_log.channel, CategoryChannel):
                        continue

                    try:
                        ft = gc.ui.views[str(channel_log.channel.id)].formattedText
                    except Exception as e:
                        log("e: {}".format(e))
                    if len(ft.messages) > 0 and channel_log.logs[-1].id == \
                            ft.messages[-1].id:
                        doBreak = True
                        break
                    if len(channel_log.logs) > 0:
                        ft.addMessage(channel_log.logs[-1])
                    doBreak = True
                    break
        if doBreak:
            break
    lines = ft.getLines()
    for line in lines:
        words = []
        for word in line.words:
            words.append(word.content)
        #log("Line: {}".format(" ".join(words)))
    name_offset = 0
    chatWin_height, chatWin_width = chatWin.getmaxyx()
    # upon entering a new channel, scroll all the way down
    if gc.ui.channel_log_offset == -1:
        if len(lines) > chatWin_height:
            gc.ui.channel_log_offset = len(lines) - chatWin_height
        else:
            gc.ui.channel_log_offset = 0
    # check to see if scrolling is out of bounds
    elif len(lines) > chatWin_height and \
            gc.ui.channel_log_offset > len(lines)-chatWin_height:
        gc.ui.channel_log_offset = len(lines)-chatWin_height
    elif gc.ui.channel_log_offset < -1:
        gc.ui.channel_log_offset = 0
    color = 0
    chatWin.erase()
    if not len(lines):
        chatWin.noutrefresh()
        return
    for idx, line in enumerate(
            lines[gc.ui.channel_log_offset:gc.ui.channel_log_offset+chatWin_height]):
        try:
            if line.isFirst:
                ts_str = ""
                if gc.settings["timestamps_enabled"]:
                    ts_now = time.time()
                    ts_offset = datetime.fromtimestamp(ts_now)-\
                            datetime.utcfromtimestamp(ts_now)
                    dt = line.date+ts_offset
                    ts_str = dt.strftime(gc.settings["timestamp_format"]) +\
                            " - "
                author_color = get_role_color(line.topRole, gc)
                chatWin.addstr(idx,0, "{}{}: ".format(ts_str, line.user), author_color)
                name_offset = chatWin.getyx()[1]
            elif name_offset == 0:
                # if line is at the top and it's not a "user" line
                for subline in reversed(lines[0:gc.ui.channel_log_offset]):
                    if subline.isFirst:
                        name_offset = len(subline.user) + 2
                        break
            chatWin.move(idx,name_offset)
            for idy, word in enumerate(line.words):
                color = 0
                if "@" + gc.client.current_guild.me.display_name in word.content:
                    color = gc.ui.colors[gc.settings["mention_color"]]
                if not word.content:
                    continue
                try:
                    # if the next word attrs are the same
                    if idy < len(line.words)-1 and word.attrs == line.words[idy+1].attrs:
                        chatWin.addstr(word.content + ' ', word.attrs|color)
                    else:
                        chatWin.addstr(word.content, word.attrs|color)
                        chatWin.addstr(' ', curses.A_NORMAL)
                except:
                    log("Text drawing failed at {}".format(word.content))
            chatWin.noutrefresh()
        except Exception as e:
            # if we're here, text has failed to draw
            log("Failed to draw channel log. Error: {}".format(e))
