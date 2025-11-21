from werkzeug.datastructures import FileStorage
import zipfile

def unzip_file(file_to_unzip: FileStorage) -> list:
  try:

    xml_list = []

    with zipfile.ZipFile(file_to_unzip, "r") as zip_ref:
      for file_name in zip_ref.namelist():
        data = zip_ref.read(file_name)
        xml_list.append(data)
      
    return xml_list

  except Exception as exception:

    print(exception)