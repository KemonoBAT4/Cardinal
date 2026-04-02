
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

    _url: "str | None" = None
    _dataframe: "pd.DataFrame | None" = None

    _config: dict
    _click: "str | typing.Callable | None"
    _buttons: "dict | None"
    _searchbar: bool

    _uuid: str

    def __init__(
        self,
        data_structure_or_url: "str | pd.DataFrame",
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

        if isinstance(data_structure_or_url, str):
            self._url = data_structure_or_url
        elif isinstance(data_structure_or_url, pd.DataFrame):
            self._dataframe = data_structure_or_url
        else:
            raise CardinalException(message = f"Data structure must be a type of {type(str)} or {type(pd.DataFrame)}, not {type(_data_structure_or_url)}")
        # #endif

        self._config    = config
        self._click     = click
        self._buttons   = buttons
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
    def url(self) -> "str | None":
        return self._url
    # #enddef url

    @property
    def dataframe(self) -> "pd.DataFrame | None":
        return self._dataframe
    # #enddef dataframe

    # # TODO: verify this property
    # @property
    # def dataset(self) -> "pd.DataFrame | dict[str, typing.Any] | None ":
    #     result = None

    #     if (self._dataframe is not None):
    #         result = self._dataframe
    #     elif (self._url is not None):
    #         # result = requests.get(self._url).json()
    #     # #endif

    #     return result
    # # #enddef dataset

    #endregion ----- PROPERTIES -------- #


    #region -------- METHODS -------- #

    def _get_template_from_url(self, url: str, column_keys: list[dict[str, str]]) -> "str":

        header_text: str = ""

        columns: dict = self._config.get("columns",  {})

        for key, value in columns.items():
            header_text += f"<th>{value.get('title', 'Undefined Title')}</th>"
        # #endfor

        template = """

        <head>
            <!-- DataTables -->
            <link rel="stylesheet"
                href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">

            <!-- Buttons -->
            <link rel="stylesheet"
                href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css">

            <!-- JS -->
            <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
            <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

            <!-- Buttons + Export -->
            <script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>
            <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>
        <head>

        <table id=""" + self._uuid + """ class="display nowrap" style="width:100%">
            <thead>
                <tr>
                    """ + header_text + """
                </tr>
            </thead>
        </table>

        <script>
            $(document).ready(function () {
                $('#""" + self._uuid + """').DataTable({
                    ajax: '""" + url + """',
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
    # #enddef _get_template_from_url

    def _get_template_from_dataframe(self) -> "str":
        return ""
    # #enddef _get_template_from_dataframe

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
        template: str = ""

        if (self._url is not None):
            template: str = self._get_template_from_url( url=self._url, column_keys=column_keys )
        elif (self._dataframe is not None):
            template: str = self._get_template_from_dataframe()
        # #endif

        print(template)

        return template
    # #enddef __cardinal__
# #endclass CardinalDataTable
