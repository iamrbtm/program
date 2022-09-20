import subprocess

def main():
    subprocess.call("rsync -rP /Volumes/PTS/* rbtm2006@truenas.local:/mnt/rbtm/PTS/rbtm2006".split())

if __name__ == "__main__":
    main()
    
rsync -rP /Users/rbtm2006/Downloads/ER/ rbtm2006@truenas.local:/mnt/rbtm/media/Movies/plexmediafiles/TVShows/ER
