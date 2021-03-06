"""
Convert notebooks listed in `chapters` into html files in the directory
`riemann_book_files`.

Run this code on the master branch with the latest set of notebooks,
adjusting the specification of `chapters` below first if you want to
process only a subset of the notebooks.

To post on the website, check out the `gh-pages` branch and then
    cp -r build_html/* html/
and then git add, commit, and push to Github.

The files `build_html/*.ipynb` can be deleted, but copy over all the
subdirectories (`figures`, `exact_solvers`, etc.) in order for figures to
display in html files and links to Python code to work properly.

Note:

 - The notebooks are first copied into the directory `build_html` and pre-processed
   to use static_widgets (or jsanimation_widgets in certain notebooks),
   and cross references to other notebooks have `.ipynb` replaced by `.html`
   so the links work in the html files.

 - The directories `utils`, `exact_solvers`, and `figures` are also copied
   in before processing.

 - The list `all_chapters` is used to replace cross-reference links
   `chapter.ipynb` by `chapter.html`.

 - The bibliography files `riemann.html` and riemann_bib.html` are
   copied into `build_html`.  These might need to be updated before
   running this script (using make_html_bib.sh).

"""

import os
from traitlets.config import Config
import nbformat
from nbinteract import InteractExporter

all_chapters = [
    'Preface', 'Index', 'Introduction', 'Advection', 'Acoustics',
    'Traffic_flow', 'Shallow_water', 'Shallow_tracer', 'Euler_equations',
    'Approximate_solvers', 'Euler_approximate_solvers',
    'Traffic_variable_speed', 'Nonlinear_elasticity',
    'Euler_equations_TammannEOS', 'Nonconvex_scalar', 'Pressureless_flow',
    'Kitchen_sink_problem'
]

chapters = all_chapters.copy()  # which chapters to process

# test on a subset:
# chapters.remove('Shallow_water')

# Exporter config
template_path = os.path.abspath('./html.tpl')
config = Config(
    InteractExporter=dict(
        # Use the NbiExecutePreprocessor to correctly generate widget output
        # for interact() calls.
        preprocessors=['nbinteract.preprocessors.NbiExecutePreprocessor'],
        template_file=template_path,
        spec='Calebs97/riemann_book/master',
    ),
    NbiExecutePreprocessor=dict(kernel_name='python2', timeout=60),
)

exporter = InteractExporter(config=config)

os.system('mkdir -p build_html')  # for intermediate processing
# copy some things needed for processing
os.system('cp -r exact_solvers build_html/')
os.system('cp -r utils build_html/')
os.system('cp -r figures build_html/')
os.system('cp custom.css build_html/')

# Putting figures inside an img folder doesn't seem to be needed now:
# os.system('mkdir -p build_html/img')  # for viewing images
# os.system('cp -r figures build_html/img/')

# Might need to update bibliography first with make_html_bib.sh
os.system('cp riemann.html build_html/')  # bibliography
os.system('cp riemann_bib.html build_html/')  # bibtex version of bibliography

for i, chapter in enumerate(chapters):
    nb_name = chapter + '.ipynb'
    print("Processing %s" % nb_name)

    notebook = nbformat.read(nb_name, as_version=4)

    html_filename = chapter + '.html'

    # Convert notebook to HTML
    try:
        html, _ = exporter.from_notebook_node(notebook)
    except Exception as e:
        print('Error converting %s: %s' % (nb_name, e))
        continue

    with open(os.path.join('build_html', html_filename), 'w') as output:
        output.write(html)

    # with open(output_filename, "w") as output:
    #     if chapter in ['Introduction', 'Shallow_water', 'Nonconvex_scalar']:
    #         widget = 'from utils.jsanimate_widgets import interact'
    #     else:
    #         widget = 'from utils.snapshot_widgets import interact'

    #     for line in lines:
    #         # nbinteract needs ipywidgets
    #         # line = re.sub(r'from ipywidgets import interact', widget, line)
    #         for j, chapter_name in enumerate(all_chapters):
    #             line = re.sub(
    #                 chapter_name + '.ipynb', chapter_name + '.html', line
    #             )
    #         output.write(line)

    # args = [
    #     "jupyter", "nbconvert", "--to", "html", "--execute",
    #     "--ExecutePreprocessor.kernel_name=python2", "--output", html_filename,
    #     "--template", template_path, "--ExecutePreprocessor.timeout=60",
    #     output_filename
    # ]
    # subprocess.check_call(args)

print("The html files can be found in build_html")
print("Open build_html/Index.html for the index")

if 0:
    # Recommend doing this after switching to gh-pages branch:
    os.system('mkdir -p html/figures')
    os.system('cp build_html/img/figures/* html/figures/')

    print("You may delete the directory build_html")
    print("Open html/Index.html for the index")
