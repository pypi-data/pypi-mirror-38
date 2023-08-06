"Data Objects\n\nThis module contains data objects used to represent the data returned from the API.\n"
import pandas as pd


class Column:
    "Data transfer object for a column.\n\n    Args:\n        id (int):           ID of the column.\n        name (str):         Name of the column.\n        externalId (str):   External ID of the column.\n        valueType (str):    Data type of the column.\n        metadata (dict):    Custom, application specific metadata. String key -> String Value.\n    "
    id: Union[(int, None)]
    name: str
    externalId: str
    valueType: str
    metadata: dict

    def __init__(self, id, name, externalId, valueType, metadata):
        self.id = id
        self.name = name
        self.externalId = externalId
        self.valueType = valueType
        self.metadata = metadata

    @staticmethod
    def from_JSON(the_column):
        return Column(
            id=the_column["id"],
            name=the_column["name"],
            externalId=the_column.get("externalId", None),
            valueType=the_column["valueType"],
            metadata=the_column["metadata"],
        )


class Sequence:
    "Data transfer object for a sequence.\n\n    Args:\n        id (int):           ID of the sequence.\n        name (str):         Name of the sequence.\n        externalId (str):   External ID of the sequence.\n        assetId (int):      ID of the asset the sequence is connected to, if any.\n        columns (list):     List of columns in the sequence.\n        description (str):  Description of the sequence.\n        metadata (dict):    Custom, application specific metadata. String key -> String Value.\n    "
    id: Union[(int, None)]
    name: str
    externalId: str
    assetId: int
    columns: List[Column]
    description: str
    metadata: dict

    def __init__(self, id, name, externalId, assetId, columns, description, metadata):
        self.id = id
        self.name = name
        self.externalId = externalId
        self.assetId = assetId
        self.columns = columns
        self.description = description
        self.metadata = metadata

    @staticmethod
    def from_JSON(the_sequence):
        return Sequence(
            id=the_sequence["id"],
            name=the_sequence["name"],
            externalId=the_sequence.get("externalId", None),
            assetId=the_sequence.get("assetId", None),
            columns=[Column.from_JSON(the_column) for the_column in the_sequence["columns"]],
            description=the_sequence["description"],
            metadata=the_sequence["metadata"],
        )


class RowValue:
    "Data transfer object for the value in a row in a sequence.\n\n    Args:\n        columnId (int):   The ID of the column that this value is for.\n        value (str):      The actual value.\n    "
    columnId: int
    value: str

    def __init__(self, columnId, value):
        self.columnId = columnId
        self.value = value

    @staticmethod
    def from_JSON(the_row_value):
        return RowValue(columnId=the_row_value["columnId"], value=the_row_value["value"])


class Row:
    "Data transfer object for a row of data in a sequence.\n\n    Args:\n        row_number (int):  The row number for this row.\n        values (list):     The values in this row.\n    "
    rowNumber: int
    values: List[RowValue]

    def __init__(self, rowNumber, values):
        self.rowNumber = rowNumber
        self.values = values

    @staticmethod
    def from_JSON(the_row):
        return Row(
            rowNumber=the_row["rowNumber"],
            values=[RowValue.from_JSON(the_row_value) for the_row_value in the_row["values"]],
        )

    def get_row_as_csv(self):
        return ",".join([str(x.value) for x in self.values])


class SequenceDataResponse:
    "Data transfer object for the data in a sequence, used when receiving data.\n\n    Args:\n        rows (list):  List of rows with the data.\n    "
    rows: List[Row]

    def __init__(self, rows):
        self.rows = rows

    @staticmethod
    def from_JSON(the_data):
        return SequenceDataResponse(rows=[Row.from_JSON(the_row) for the_row in the_data["rows"]])

    @staticmethod
    def _row_has_value_for_column(row, column_id):
        return column_id in [value.columnId for value in row.values]

    @staticmethod
    def _get_value_for_column(row, column_id):
        return next((value.value for value in row.values if (value.columnId == column_id)))

    def to_pandas(self):
        "Returns data as a pandas dataframe"
        column_ids = [value.columnId for value in self.rows[0].values]
        my_df = pd.DataFrame(columns=column_ids)
        for row in self.rows:
            data_this_row: List[float] = []
            for column_id in column_ids:
                if self._row_has_value_for_column(row, column_id):
                    data_this_row.append(self._get_value_for_column(row, column_id))
                else:
                    data_this_row.append("null")
            my_df.loc[len(my_df)] = data_this_row
        return my_df

    def to_json(self):
        "Returns data as a json object"
        pass


class SequenceDataRequest:
    "Data transfer object for requesting sequence data.\n\n    Args:\n        inclusiveFrom (int):    Row number to get from (inclusive).\n        inclusiveTo (int):      Row number to get to (inclusive).\n        limit (int):            How many rows to return.\n        columnsIds (List[int]): ids of the columns to get data for.\n    "
    inclusiveFrom: int
    inclusiveTo: int
    limit: int = 100
    columnIds: List[int] = []

    def __init__(self, inclusiveFrom, inclusiveTo, limit=100, columnIds=[]):
        self.inclusiveFrom = inclusiveFrom
        self.inclusiveTo = inclusiveTo
        self.limit = limit
        self.columnIds = columnIds
