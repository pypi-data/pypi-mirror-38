import logging
from datetime import datetime
from typing import Optional, Dict, List, ClassVar, Type, Sequence

import attr
from marshmallow import fields


from simple_smartsheet.models.base import Schema, CoreSchema, Object, CoreObject, CRUD
from simple_smartsheet.models.column import Column, ColumnSchema
from simple_smartsheet.models.row import Row, RowSchema
from simple_smartsheet.models.extra import Result


logger = logging.getLogger(__name__)


class UserSettingsSchema(Schema):
    critical_path_enabled = fields.Bool(data_key="criticalPathEnabled")
    display_summary_tasks = fields.Bool(data_key="displaySummaryTasks")


@attr.s(auto_attribs=True, repr=False, kw_only=True)
class UserSettings(Object):
    critical_path_enabled: bool
    display_summary_tasks: bool


class SheetSchema(CoreSchema):
    """Marshmallow Schema for Smartsheet Sheet object

    Additional details about fields can be found here:
    http://smartsheet-platform.github.io/api-docs/#sheets

    """

    id = fields.Int()
    name = fields.Str()
    access_level = fields.Str(data_key="accessLevel")
    permalink = fields.Str()
    favorite = fields.Bool()
    created_at = fields.DateTime(data_key="createdAt")
    modified_at = fields.DateTime(data_key="modifiedAt")

    version = fields.Int()
    total_row_count = fields.Int(data_key="totalRowCount")
    effective_attachment_options = fields.List(
        fields.Str(), data_key="effectiveAttachmentOptions"
    )
    gantt_enabled = fields.Bool(data_key="ganttEnabled")
    dependencies_enabled = fields.Bool(data_key="dependenciesEnabled")
    resource_management_enabled = fields.Bool(data_key="resourceManagementEnabled")
    cell_image_upload_enabled = fields.Bool(data_key="cellImageUploadEnabled")
    user_settings = fields.Nested(UserSettingsSchema, data_key="userSettings")

    columns = fields.Nested(ColumnSchema, many=True)
    rows = fields.Nested(RowSchema, many=True)


@attr.s(auto_attribs=True, repr=False, kw_only=True)
class Sheet(CoreObject):
    """Represent Smartsheet Sheet object

    Additional details about fields can be found here:
    http://smartsheet-platform.github.io/api-docs/#sheets

    Extra attributes:
        row_rum_to_row: mapping of row number to Row object
        row_id_to_row: mapping of row id to Row object
        column_title_to_column: mapping of column title to Column object
        column_id_to_column: mapping of column id to Column object
        schema: reference to SheetSchema
    """

    name: str
    id: Optional[int] = None
    access_level: Optional[str] = None
    permalink: Optional[str] = None
    favorite: Optional[bool] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    version: Optional[int] = None
    total_row_count: Optional[int] = None
    effective_attachment_options: List[str] = attr.Factory(list)
    gantt_enabled: Optional[bool] = None
    dependencies_enabled: Optional[bool] = None
    resource_management_enabled: Optional[bool] = None
    cell_image_upload_enabled: Optional[bool] = None
    user_settings: Optional[UserSettings] = None

    columns: List[Column] = attr.Factory(list)
    rows: List[Row] = attr.Factory(list)

    row_num_to_row: Dict[int, Row] = attr.Factory(dict)
    row_id_to_row: Dict[int, Row] = attr.Factory(dict)
    column_title_to_column: Dict[str, Column] = attr.Factory(dict)
    column_id_to_column: Dict[int, Column] = attr.Factory(dict)

    schema: ClassVar[Type[SheetSchema]] = SheetSchema

    def __attrs_post_init__(self) -> None:
        self.update_index()

    def update_index(self) -> None:
        """Updates columns and row indices for quick lookup"""
        self.update_column_index()
        self.update_row_index()

    def update_column_index(self) -> None:
        """Updates columns index for quick lookup by title and ID"""
        self.column_title_to_column.clear()
        self.column_id_to_column.clear()

        for column in self.columns:
            if column.id is None:
                continue
            self.column_id_to_column[column.id] = column

            column_title = column.title
            if column_title is None:
                continue
            if column_title in self.column_title_to_column:
                logger.info(
                    "Column with the title %s is already present in the index"
                    % column_title
                )
            self.column_title_to_column[column_title] = column

    def update_row_index(self) -> None:
        """Updates row index for quick lookup by row number and ID"""
        self.row_num_to_row.clear()
        self.row_id_to_row.clear()

        for row in self.rows:
            self.row_num_to_row[row.num] = row
            self.row_id_to_row[row.id] = row
            row.update_index(self)

    def get_row(
        self, row_num: Optional[int] = None, row_id: Optional[int] = None
    ) -> Optional[Row]:
        """Returns Row object by row number or ID

        Either row_num or row_id must be provided

        Args:
            row_num: row number
            row_id: row id

        Returns:
            Row object
        """
        if row_num is not None:
            return self.row_num_to_row.get(row_num)
        elif row_id is not None:
            return self.row_id_to_row.get(row_id)
        else:
            raise ValueError("Either row_num or row_id argument should be provided")

    def get_column(
        self, column_title: Optional[str] = None, column_id: Optional[int] = None
    ) -> Optional[Column]:
        """Returns Column object by column title or ID

        Either column_title or column_id must be provided

        Args:
            column_title: column title (case-sensitive)
            column_id: column id

        Returns:
            Column object
        """
        if column_title is not None:
            return self.column_title_to_column.get(column_title)
        elif column_id is not None:
            return self.column_id_to_column.get(column_id)
        else:
            raise ValueError(
                "Either column_title or column_id argument should be provided"
            )

    def add_rows(self, rows: Sequence[Row]) -> Result:
        """Adds several rows to the smartsheet.

        Sheet must have api attribute set. It is automatically set when method
            Smartsheet.sheets.get() is used
        Every row must have either location-specifier attributes or row number set
        More details: http://smartsheet-platform.github.io/api-docs/#add-rows

        Args:
            rows: sequence of Row objects

        Returns:
            Result object
        """
        if self.api is None:
            raise ValueError("To use this method, api attribute must be set")
        include_fields = (
            "parent_id",
            "sibling_id",
            "above",
            "indent",
            "outdent",
            "to_bottom",
            "to_top",
            "expanded",
            "format",
            "cells.column_id",
            "cells.formula",
            "cells.value",
            "cells.hyperlink",
            "cells.link_in_from_cell",
            "cells.strict",
            "cells.format",
            "cells.image",
            "cells.override_validation",
            "locked",
        )
        data = []
        schema = RowSchema(only=include_fields)
        for row in rows:
            new_row = row.copy(deep=False)
            new_row.cells = [
                cell
                for cell in row.cells
                if cell.value is not None or cell.formula is not None
            ]
            data.append(schema.dump(new_row))
        return self.api.post(f"/sheets/{self.id}/rows", data=data)

    def add_row(self, row: Row) -> Result:
        """Adds a single row to the smartsheet.

        Sheet must have api attribute set. It is automatically set when method
            Smartsheet.sheets.get() is used
        A row must have either location-specifier attributes or row number set
        More details: http://smartsheet-platform.github.io/api-docs/#add-rows

        Args:
            row: Row object

        Returns:
            Result object
        """
        return self.add_rows([row])

    def update_rows(self, rows: Sequence[Row]) -> Result:
        """Updates several rows in the Sheet.

        Sheet must have api attribute set. It is automatically set when method
            Smartsheet.sheets.get() is used
        More details: http://smartsheet-platform.github.io/api-docs/#update-rows

        Args:
            rows: sequence of Row objects

        Returns:
            Result object
        """
        if self.api is None:
            raise ValueError("To use this method, api attribute must be set")
        include_fields = (
            "id",
            "parent_id",
            "sibling_id",
            "above",
            "indent",
            "outdent",
            "to_bottom",
            "to_top",
            "expanded",
            "format",
            "cells.column_id",
            "cells.formula",
            "cells.value",
            "cells.hyperlink",
            "cells.link_in_from_cell",
            "cells.strict",
            "cells.format",
            "cells.image",
            "cells.override_validation",
            "locked",
        )
        data = []
        schema = RowSchema(only=include_fields)
        for row in rows:
            new_row = row.copy(deep=False)
            new_row.cells = [
                cell
                for cell in row.cells
                if cell.value is not None or cell.formula is not None
            ]
            data.append(schema.dump(new_row))
        return self.api.put(f"/sheets/{self.id}/rows", data=data)

    def update_row(self, row: Row) -> Result:
        """Updates a single row in the Sheet.

        Sheet must have api attribute set. It is automatically set when method
            Smartsheet.sheets.get() is used
        More details: http://smartsheet-platform.github.io/api-docs/#update-rows

        Args:
            row: Row object

        Returns:
            Result object
        """
        return self.update_rows([row])

    def delete_rows(self, row_ids: Sequence[int]) -> Result:
        """Deletes several rows in the Sheet.

        Rows are identified by ids.

        Args:
            row_ids: sequence of row ids

        Returns:
            Result object
        """
        if self.api is None:
            raise ValueError("To use this method, api attribute must be set")
        endpoint = f"/sheets/{self.id}/rows"
        params = {"ids": ",".join(str(row_id) for row_id in row_ids)}
        return self.api.delete(endpoint, params=params)

    def delete_row(self, row_id: int) -> Result:
        """Deletes a single row in the Sheet specified by ID.

        Args:
            row_id: Row id

        Returns:
            Result object
        """
        return self.delete_rows([row_id])


class SheetsCRUD(CRUD[Sheet]):
    base_url = "/sheets"
    factory = Sheet
    default_path = "sheets"

    create_include_fields = (
        "name",
        "columns.primary",
        "columns.title",
        "columns.type",
        "columns.auto_number_format",
        "columns.options",
        "columns.symbol",
        "columns.system_column_type",
        "columns.width",
    )
