import logging
import time
import atexit
import os
from subprocess import Popen, PIPE, DEVNULL

logger = logging.getLogger(__name__)
dir = ''

class Player:
    def __init__(self, movie, layer):
       self.movie = movie
       self.process = None
       self.layer = layer

    def start(self):
        args = ['omxplayer']
        #args.append('--alpha')
        #args.append('150')
        #args.append('--win')
        #args.append('0,0,500,500')
        args.append('--no-osd')
        args.append('--loop')
        args.append('--layer')
        args.append(str(self.layer))
        args.append(self.movie)
        self.stop()
        self.process = Popen(args, stdin=PIPE, stdout=DEVNULL, close_fds=True, bufsize=0)
        #start_command = ""
        #self.process.stdin.write(start_args) # start playing

    def stop(self):
        p = self.process
        if p is not None:
           try:
               p.stdin.write('q'.encode()) # send quit command
               p.terminate()
               p.wait() # -> move into background thread if necessary
           except EnvironmentError as e:
               logger.error("can't stop %s: %s", self.movie, e)
           else:
               self.process = None



run = True
player = None
player_bg = None

def main() -> None:
    global player, player_bg, dir
    dirname = os.path.dirname(__file__)
    
    player_bg = Player(os.path.join(dirname, 'dog.mov'), 0)
    player_bg.start()
    
    default_file = os.path.join(dirname, 'default.mp4')
    current_file = default_file
    player = Player(current_file, 1)
    player.start()
    
    while run:
        time.sleep(10)
        file = ''
        with open(os.path.join(dirname, 'video.txt'), 'r') as reader:
            file = reader.read()
        if file == '':
            file = default_file
        if file == current_file:
            continue
        current_file = file
        if player is not None:
            player.stop()
            if player.movie != default_file:
                os.remove(player.movie)
            del player
        player = Player(current_file, 1)
        player.start()
        

def goodbye():
    global player, player_bg
    print("GoodBye.")
    
    if player is not None:
        player.stop()
        del player
        
    if player_bg is not None:
        player_bg.stop()
        del player_bg


def canstart():
    try:
        print("Video starts in 5 seconds... Press Ctrl-C to cancel NOW!")
        for i in range(0, 5):
            time.sleep(1)
        return True
    except KeyboardInterrupt:
        print("Video cancelled")
        return False


atexit.register(goodbye)
if __name__ == '__main__':
    if canstart():
        main()