import subprocess

def main():
    sources = ["Movies", "TVShows"]
    
    for src in sources:
        source = f"/mnt/guill/media/new_media/{src}/"
        dest = f"/mnt/guill/media/{src}/"
        
        query = f"rsync -rP --remove-source-files rbtm2006@truenas.local::{source} {dest}"
    
        subprocess.call(query.split())

if __name__ == "__main__":
    main()
    
# rsync -rP /Users/rbtm2006/Downloads/ER/ rbtm2006@truenas.local:/mnt/rbtm/media/Movies/plexmediafiles/TVShows/ER


# /mnt/guill/media/new_media/Movies
# /mnt/guill/media/new_media/TVShows
