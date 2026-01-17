"""
File formats for Google Drive.
"""

from dataclasses import dataclass, field
from typing import Optional

@dataclass(frozen=True)
class FileFormat:
    """Represents a file format."""
    name: str
    mimetype: str
    extension: str
    method_name: str
    pd_kwargs: Optional[dict] = field(default_factory=dict)

    def export_to_dict(self) -> dict:
        """Export file format to dictionary."""
        return self.__dict__.copy()

    def __str__(self) -> str:
        """String representation of file format."""
        return f"{self.name} ({self.extension})"

ParquetFormat = FileFormat(
    name="parquet",
    mimetype="application/octet-stream",
    extension="parquet",
    method_name="to_parquet",
    pd_kwargs={
        "index": False,
        "engine": "pyarrow"
    }
)

ExcelFormat = FileFormat(
    name="excel",
    mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    extension="xlsx",
    method_name="to_excel",
    pd_kwargs={
        "index": False,
        "engine": "openpyxl"
    }
)

JsonFormat = FileFormat(
    name="json",
    mimetype="application/json",
    extension="json",
    method_name="to_json",
    pd_kwargs={
        "index": False
    }
)

CsvFormat = FileFormat(
    name="csv",
    mimetype="text/csv",
    extension="csv",
    method_name="to_csv",
    pd_kwargs={
        "index": False,
        "sep": ",",
        "encoding": "utf-8"
    }
)

@dataclass
class FileFormats:
    """Represents a collection of file formats."""
    parquet: FileFormat = ParquetFormat
    excel: FileFormat = ExcelFormat
    json: FileFormat = JsonFormat
    csv: FileFormat = CsvFormat
 
    def __post_init__(self):
        """Post initialization."""
        self.available_formats = self.get_available_formats()
    
    def get_format_class(self, file_format: str) -> FileFormat:
        """Get file format by name."""
        return getattr(self, file_format)

    def get_extension(self, file_format: str) -> str:
        """Get file extension by name."""
        return self.get_format_class(file_format).extension

    def get_mimetype(self, file_format: str) -> str:
        """Get file mimetype by name."""
        return self.get_format_class(file_format).mimetype
    
    def export_formats_to_dict(self) -> dict:
        """Convert all file formats to dictionary."""
        return {
            file_format.name: file_format.export_to_dict()\
            for file_format in self.__dict__.values()\
            if isinstance(file_format, FileFormat)
        }

    def get_available_formats(self, as_set: bool = False) -> list:
        """Get available file formats."""
        if as_set:
            return set(self.export_formats_to_dict().keys())
        return list(self.export_formats_to_dict().keys())
    
    def export_to_dict(self) -> dict:
        """Convert file format to dictionary."""
        return self.__dict__.copy()
    
    def is_format_available(self, file_format: str, raise_error: bool = True) -> bool:
        """Check if format is available."""
        if file_format not in self.available_formats:
            if raise_error:
                available_formats = ", ".join(self.available_formats)
                err_msg = f"Unsupported format: {file_format}.\n"
                err_msg += f"Available formats: [{available_formats}]."
                raise ValueError(err_msg)
            return False
        return True