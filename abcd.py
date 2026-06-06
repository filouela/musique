from subprocess import run, PIPE
import sys

abcfile = f"scores/s{sys.argv[1]}.abc"
r = run(f"abcm2ps -O scores/Out{sys.argv[1]}.svg -g {abcfile}",shell=True, stdout=PIPE, stderr=PIPE)
print(f"\\includesvg[width=\\textwidth]{{scores/Out{sys.argv[1]}001.svg}}")
