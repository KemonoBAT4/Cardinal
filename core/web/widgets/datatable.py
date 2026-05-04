
from ._common import *

# the class should create a table with the given data (url or dataframe, need
# to decide which is better). then the class should render the table with all
# the actions possible (click event on the table rows, pdf download,
# excel download, etc.).a searchbar should be added too for better
# searching in the table in case of large quantities of records

"""

### TO-DO LIST
- [ ] get the data from the dataframe passed or retrieve it from the url
- [ ] render the table with the config passed
- [X] implement the buttons (download excel, pdf)
- [ ] implement the possibility to pass the configuration from the api url request (if necessary)
- [ ] implement the click event when a row is clicked
- [X] implement the searchbar
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
                <meta charset="UTF-8">
                <!-- Google Fonts -->
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
                <!-- DataTables -->
                <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
                <link rel="stylesheet" href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css">
                <!-- JS -->
                <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
                <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
                <script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
                <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>
                <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>

                <style>
                    :root {
                        --bg:          #f7f8fa;
                        --surface:     #ffffff;
                        --border:      #e4e7ec;
                        --text:        #111827;
                        --text-muted:  #6b7280;
                        --accent:      #2563eb;
                        --accent-soft: #eff6ff;
                        --radius:      10px;
                        --shadow:      0 1px 4px rgba(0,0,0,.07), 0 4px 16px rgba(0,0,0,.06);
                    }

                    * { box-sizing: border-box; margin: 0; padding: 0; }

                    /*
                    body {
                        background: var(--bg);
                        font-family: 'DM Sans', sans-serif;
                        color: var(--text);
                        padding: 2rem;
                    }
                    */

                    /* ── Wrapper card ── */
                    .dt-wrapper {
                        background: var(--surface);
                        border: 1px solid var(--border);
                        border-radius: var(--radius);
                        box-shadow: var(--shadow);
                        padding: 1.5rem;
                        animation: fadeUp .35s ease both;
                    }

                    @keyframes fadeUp {
                        from { opacity: 0; transform: translateY(10px); }
                        to   { opacity: 1; transform: translateY(0); }
                    }

                    /* ── Top bar (buttons + search) ── */
                    .dataTables_wrapper .dt-buttons { margin-bottom: 0; }

                    div.dt-buttons {
                        display: flex;
                        gap: .5rem;
                    }

                    .dt-button {
                        display: inline-flex !important;
                        align-items: center;
                        gap: .4rem;
                        padding: .45rem 1rem !important;
                        border-radius: 6px !important;
                        border: 1px solid var(--border) !important;
                        background: var(--surface) !important;
                        color: var(--text) !important;
                        font-family: 'DM Sans', sans-serif !important;
                        font-size: .82rem !important;
                        font-weight: 500 !important;
                        cursor: pointer;
                        box-shadow: 0 1px 2px rgba(0,0,0,.05) !important;
                        transition: background .15s, border-color .15s, transform .1s;
                    }

                    .dt-button:hover {
                        background: var(--accent-soft) !important;
                        border-color: var(--accent) !important;
                        color: var(--accent) !important;
                        transform: translateY(-1px);
                    }

                    .dt-button:active { transform: translateY(0) !important; }

                    /* ── Search ── */
                    .dataTables_filter label {
                        display: flex;
                        align-items: center;
                        gap: .5rem;
                        font-size: .85rem;
                        color: var(--text-muted);
                    }

                    .dataTables_filter input {
                        padding: .45rem .85rem .45rem 2.2rem !important;
                        border: 1px solid var(--border) !important;
                        border-radius: 6px !important;
                        font-family: 'DM Sans', sans-serif !important;
                        font-size: .85rem !important;
                        color: var(--text) !important;
                        background: var(--bg) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%236b7280' stroke-width='2.2'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.35-4.35'/%3E%3C/svg%3E") .7rem center / 14px no-repeat !important;
                        outline: none;
                        transition: border-color .2s, box-shadow .2s;
                    }

                    .dataTables_filter input:focus {
                        border-color: var(--accent) !important;
                        box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important;
                    }

                    .dataTables_filter input::placeholder { color: var(--text-muted); }

                    /* ── Table ── */
                    table.dataTable {
                        border-collapse: separate !important;
                        border-spacing: 0 !important;
                        width: 100% !important;
                        margin: 1rem 0 !important;
                        font-size: .88rem;
                    }

                    table.dataTable thead th {
                        background: #1e293b !important;
                        color: #e2e8f0 !important;
                        font-family: 'DM Sans', sans-serif;
                        font-weight: 600;
                        font-size: .78rem;
                        letter-spacing: .06em;
                        text-transform: uppercase;
                        padding: .85rem 1rem !important;
                        border: none !important;
                        white-space: nowrap;
                    }

                    table.dataTable thead th:first-child { border-radius: 8px 0 0 0; }
                    table.dataTable thead th:last-child  { border-radius: 0 8px 0 0; }

                    table.dataTable thead th.sorting::after,
                    table.dataTable thead th.sorting_asc::after,
                    table.dataTable thead th.sorting_desc::after { opacity: .6; }

                    table.dataTable tbody tr {
                        transition: background .12s;
                    }

                    table.dataTable tbody tr td {
                        padding: .75rem 1rem !important;
                        border-bottom: 1px solid var(--border) !important;
                        border-top: none !important;
                        color: var(--text);
                        font-family: 'DM Mono', monospace;
                        font-size: .82rem;
                    }

                    table.dataTable tbody tr:hover td {
                        background: var(--accent-soft) !important;
                    }

                    table.dataTable tbody tr:last-child td { border-bottom: none !important; }

                    /* ── Footer info + pagination ── */
                    .dataTables_info {
                        font-size: .8rem;
                        color: var(--text-muted);
                        padding-top: .6rem !important;
                    }

                    .dataTables_paginate { padding-top: .4rem !important; }

                    .dataTables_paginate .paginate_button {
                        padding: .3rem .65rem !important;
                        border-radius: 6px !important;
                        border: 1px solid transparent !important;
                        font-size: .82rem !important;
                        font-family: 'DM Sans', sans-serif !important;
                        color: var(--text-muted) !important;
                        margin: 0 2px !important;
                        transition: background .15s, color .15s;
                    }

                    .dataTables_paginate .paginate_button:hover {
                        background: var(--accent-soft) !important;
                        color: var(--accent) !important;
                        border-color: var(--border) !important;
                    }

                    .dataTables_paginate .paginate_button.current,
                    .dataTables_paginate .paginate_button.current:hover {
                        background: var(--accent) !important;
                        color: #fff !important;
                        border-color: var(--accent) !important;
                        font-weight: 600 !important;
                    }

                    .dataTables_paginate .paginate_button.disabled { opacity: .35 !important; }

                    /* ── Length select ── */
                    .dataTables_length label {
                        font-size: .85rem;
                        color: var(--text-muted);
                        display: flex;
                        align-items: center;
                        gap: .4rem;
                    }

                    .dataTables_length select {
                        padding: .3rem .5rem;
                        border: 1px solid var(--border);
                        border-radius: 6px;
                        font-family: 'DM Sans', sans-serif;
                        font-size: .82rem;
                        color: var(--text);
                        background: var(--bg);
                        outline: none;
                    }
                </style>
            </head>

            <div class="dt-wrapper">
                <table id=""" + self._uuid + """ class="display nowrap" style="width:100%">
                    <thead>
                        <tr>
                            """ + header_text + """
                        </tr>
                    </thead>
                </table>
            </div>

            <script>
                $(document).ready(function () {
                    var table = $('#""" + self._uuid + """').DataTable({
                        ajax: '""" + url + """',
                        columns: """ + json.dumps(column_keys) + """,
                        dom: 'Bfrtip',
                        buttons: [
                            { extend: 'excelHtml5', text: '↓ Excel' },
                            { extend: 'pdfHtml5',   text: '↓ PDF'   }
                        ],
                        language: {
                            search:     "",
                            searchPlaceholder: "🔍 Cerca...",
                            lengthMenu: "Mostra _MENU_ righe",
                            info:       "_START_ – _END_ di _TOTAL_",
                            paginate: {
                                next:     "Avanti →",
                                previous: "← Indietro"
                            }
                        }
                    });
                });
            </script>
        """

        # template = """

        # <head>
        #     <!-- DataTables -->
        #     <link rel="stylesheet"
        #         href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">

        #     <!-- Buttons -->
        #     <link rel="stylesheet"
        #         href="https://cdn.datatables.net/buttons/2.4.2/css/buttons.dataTables.min.css">

        #     <!-- JS -->
        #     <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
        #     <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>

        #     <!-- Buttons + Export -->
        #     <script src="https://cdn.datatables.net/buttons/2.4.2/js/dataTables.buttons.min.js"></script>
        #     <script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
        #     <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/pdfmake.min.js"></script>
        #     <script src="https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/vfs_fonts.js"></script>
        #     <script src="https://cdn.datatables.net/buttons/2.4.2/js/buttons.html5.min.js"></script>
        # <head>

        # <table id=""" + self._uuid + """ class="display nowrap" style="width:100%">
        #     <thead>
        #         <tr>
        #             """ + header_text + """
        #         </tr>
        #     </thead>
        # </table>

        # <script>
        #     $(document).ready(function () {
        #         $('#""" + self._uuid + """').DataTable({
        #             ajax: '""" + url + """',
        #             columns:""" +  json.dumps(column_keys) + """,
        #             dom: 'Bfrtip',
        #             buttons: [
        #                 'excelHtml5',
        #                 'pdfHtml5'
        #             ],
        #             language: {
        #                 search: "",
        #                 lengthMenu: "Mostra _MENU_ righe",
        #                 info: "_START_ - _END_ di _TOTAL_",
        #                 paginate: {
        #                     next: "Avanti",
        #                     previous: "Indietro"
        #                 }
        #             }
        #         });
        #     });

        #     // NOTE: make this work
        #     // // seta a placeholder
        #     // $('.dataTables_filter input').attr("placeholder", "🔍 Cerca...");
        # </script>
        # """

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
