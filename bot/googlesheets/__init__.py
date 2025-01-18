from .googlesheets import GoogleSheets
import config_data

googlesheet = GoogleSheets(
    config_data.config.gt.service_account_file,
    config_data.config.gt.spreadsheet_id
)