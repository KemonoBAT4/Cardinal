
from ._common import *


# NOTE: this class is not yet implemented
# TODO: implement this class
# the class should create a table with the given data (url or dataframe, need
# to decide which is better). then the class should render the table with all
# the actions possible (click event on the table rows, pdf download,
# excel download, etc.).a searchbar should be added too for better
# searching in the table in case of large quantities of records

"""

### TO-DO LIST
- [ ] get the data from the dataframe passed or retrieve it from the url
- [ ] render the table with the config passed
- [ ] implement the buttons (new, excel, pdf)
- [ ] implement the possibility to pass the configuration from the api url request (if necessary)
- [ ] implement the click event when a row is clicked
- [x] implement the searchbar
- [ ] clean the code

"""

class CardinalDataTable:

    _config: dict
    _click: "str | typing.Callable | None"
    _buttons: "dict | None"
    _searchbar: bool
    _url: str

    _uuid: str

    def __init__(
        self,
        url: str,
        config: dict,
        click: "str | typing.Callable | None" = None,
        buttons: "dict | None" = None,
        searchbar: bool = False
    ) -> "None":
        """
        #### DESCRIPTION:
        Creates a data table based on the give dataframe

        #### PARAMETERS:
        - url: str -> the url for the request to get the data
        - config: dict -> the configuration for the data table
        - click: str | typing.Callable | None -> the function to call when a row is clicked
        - buttons: dict | None -> the buttons to add to the top bar of the table

        #### RETURNS:
        - no return
        """

        self._uuid = uuid.uuid4().hex

        self._url = url
        self._config = config
        self._click = click
        self._buttons = buttons
        self._searchbar = searchbar
    # #enddef __init__

    #region -------- PROPERTIES -------- #

    @property
    def config(self) -> "dict[str, typing.Any]":
        return self._config
    # #enddef config

    @property
    def click(self) -> "str | typing.Callable | None":
        return self._click
    # #enddef click

    @property
    def buttons(self) -> "dict | None":
        return self._buttons
    # #enddef buttons

    @property
    def searchbar(self) -> bool:
        return self._searchbar
    # #enddef searchbar

    @property
    def url(self) -> str:
        return self._url
    # #enddef url

    #endregion ----- PROPERTIES -------- #


    #region -------- METHODS -------- #
    #endregion ----- METHODS -------- #

    def __cardinal__(self) -> "str":
        """
        #### DESCRIPTION:
        Renders the data table

        #### PARAMETERS:
        - no parameters

        #### RETURNS:
        - str
        """

        column_keys: list[dict[str, str]] = [{"data": key} for key in self._config["columns"].keys()]
        template = """

        <table id=""" + self._uuid + """ class="display nowrap" style="width:100%">
            <thead>
                <tr>
                    {% for key, value in config.items() %}
                        <th>{{ value }}</th>
                    {% endfor %}
                </tr>
            </thead>
        </table>

        <script>
            $(document).ready(function () {
                $('#""" + self._uuid + """').DataTable({
                    ajax: '""" + self._url + """',
                    columns:""" +  json.dumps(column_keys) + """,
                    dom: 'Bfrtip',
                    buttons: [
                        'excelHtml5',
                        'pdfHtml5'
                    ],
                    language: {
                        search: "",
                        lengthMenu: "Mostra _MENU_ righe",
                        info: "_START_ - _END_ di _TOTAL_",
                        paginate: {
                            next: "Avanti",
                            previous: "Indietro"
                        }
                    }
                });
            });

            // NOTE: make this work
            // // seta a placeholder
            // $('.dataTables_filter input').attr("placeholder", "🔍 Cerca...");
        </script>
        """

        return template
    # #enddef __cardinal__
# #endclass CardinalDataTable
