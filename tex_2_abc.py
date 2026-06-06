import main
import subprocess
import sys



def abc_2_svg(abc_file) :
    abcfile = f"scores/s{abc_file}.abc"
    r = subprocess.run(f"abcm2ps -O scores/Out{abc_file}.svg -g {abcfile}",shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"\\includesvg[width=\\textwidth]{{scores/Out{abc_file}001.svg}}")

def ecrire_K(K, infile_name, outfile_name) :
    with open(infile_name) as f :
        data = f.read()
    latex = data.replace("CLE", K)
    with open(outfile_name, 'w') as f :
        f.write(latex)

def ecrire_partition(partition, infile_name, outfile_name) :
    with open(infile_name) as f :
        data = f.read()
    latex = data.replace("SCORE", partition)
    with open(outfile_name, 'w') as f :
        f.write(latex)

def run_latex(file_name) :
    subprocess.run(['pdflatex', '--shell-escape', file_name])

def ecrire(K, partition, infile_name, outfile_name) :
    ecrire_K(K, infile_name, outfile_name)
    ecrire_partition(partition, outfile_name, outfile_name)



if __name__ == "__main__" :
    if len(sys.argv) != 2:
        print("S'il vous plait, donnez le nom du fichier audio.")
        sys.exit(0)
    file_name = sys.argv[1]
    armure, cle, partition = main.main(file_name)
    K = f"K:{armure} {cle}"
    partition = f"{partition}||"
    infile_name = "./assets/vierge.tex"
    outfile_name = "./assets/newfile.tex"
    ecrire(K, partition, infile_name, outfile_name)
    run_latex('./assets/newfile.tex')
