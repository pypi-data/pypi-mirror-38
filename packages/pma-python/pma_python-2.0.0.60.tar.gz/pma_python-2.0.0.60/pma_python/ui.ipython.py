from pma_python import pma

__version__ = pma.__version__

def show_slide(server, session, slide):
    try:
        from IPython.core.display import display, HTML
    except ImportError:
        print("Unable to render slide inline. Make sure that you are running this code within IPython")
        return
    render = """
        <script src='""" + server + """scripts/pma.ui/pma.ui.view.min.js' type="text/javascript"></script>

<div id="viewer" style="height: 500px;"></div>
<script type="text/javascript">
            // initialize the viewport
            var viewport = new PMA.UI.View.Viewport({
                    caller: "Jupyter",
                    element: "#viewer",
                    image: '""" + slide + """',
                    serverUrls: ['"""+ server + """'],
                    sessionID: '""" + session + """'
                },
                function () {
                    console.log("Success!");
                },
                function () {
                    console.log("Error! Check the console for details.");
                });
        </script>"""
    display(HTML(render))