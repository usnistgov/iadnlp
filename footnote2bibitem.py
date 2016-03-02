import argparse


def process(fname):
    data = open(fname, "r").read()
    data = data.replace("\\end{document}", "")
    ofile = open(fname + ".converted", "w")
    bbl_list = []
    bbl_counter = 1
    while len(data) > 0:
        print("len(data)={}".format(len(data)))
        loc = data.find('\\footnote{')
        if loc == -1:
            break
        # Write up to the \footnote

        counter = "ref-{}".format(bbl_counter)
        bbl_counter += 1
        ofile.write(data[0:loc])
        ofile.write("\\cite{" + counter + "}")
        data = data[loc + 10:]
        # Find the closing brace
        b = data.find("}")
        bbl_list.append(("\\bibitem{" + counter + "} " + data[0:b]))
        data = data[b + 1:]
    ofile.write(data)

    # Write out the bibliography
    ofile.write("\\begin{thebibliography}{99}")
    for line in bbl_list:
        ofile.write(line + "\n")
    ofile.write("\\end{thebibliography}\n")
    ofile.write("\\end{document}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Turn footnotes into cites and bibitems.")
    parser.add_argument("files", help="Files or directories to analyze", nargs="+")
    args = parser.parse_args()
    for fname in args.files:
        process(fname)
