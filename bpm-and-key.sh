set -euf -o pipefail

filename="$1"
filename_mp3="$(echo $filename | sed 's/\.m4a$/.mp3/')"

if [ ! -f "$filename_mp3" ]; then
  ffmpeg -loglevel error -i "$filename" -c:a libmp3lame -q:a 4 "$filename_mp3"
fi

key=$(keyfinder-cli -n camelot "$filename_mp3")
bpm=$(sox "$filename_mp3" -t raw -r 44100 -e float -c 1 - | bpm)

echo $key $bpm $filename
