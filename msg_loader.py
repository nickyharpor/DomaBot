import polib
import glob
import os
from typing import Dict


def load_translations(folder_path: str = 'translations') -> Dict[str, Dict[str, str]]:
    """
    Scans a folder for .po files matching the pattern 'msg_XX.po', where XX is
    the language code, and creates a dictionary mapping msgid to msgstr for each language.

    Args:
        folder_path: The directory containing the .po files. Defaults to 'translations'.

    Returns:
        A dictionary where keys are language codes (e.g., 'en', 'ru') and values
        are dictionaries mapping msgid strings to msgstr strings.
    """
    # 1. Use glob to find all files matching the pattern
    pattern = os.path.join(folder_path, 'msg_*.po')
    po_files = glob.glob(pattern)

    # Check if any files were found
    if not po_files:
        print(f"Warning: No .po files found matching '{pattern}'.")
        return {}

    # Initialize the main results dictionary
    all_translations: Dict[str, Dict[str, str]] = {}

    print(f"Found {len(po_files)} translation file(s).")

    for file_path in po_files:
        try:
            # 2. Extract the language code (XX) from the filename (e.g., 'msg_en.po' -> 'en')
            # Get the base filename (e.g., 'msg_en.po')
            filename = os.path.basename(file_path)
            # Remove the prefix 'msg_' and the suffix '.po'
            # Example: 'msg_en.po'.removeprefix('msg_').removesuffix('.po') -> 'en'
            lang_code = filename.removeprefix('msg_').removesuffix('.po')

            # 3. Load the .po file using polib
            po = polib.pofile(file_path)

            # 4. Create the msgid -> msgstr dictionary for the current language
            lang_dict: Dict[str, str] = {}

            for entry in po:
                # The first entry in a PO file is usually the metadata header (msgid="").
                # We skip entries that are obsolete, plural forms, or headers.
                if entry.obsolete or not entry.msgid:
                    continue

                # Use the singular msgid and msgstr
                lang_dict[entry.msgid] = entry.msgstr

            # 5. Store the resulting dictionary in the main container
            all_translations[lang_code] = lang_dict
            print(f"Successfully processed {filename} for language '{lang_code}'.")

        except Exception as e:
            # Handle potential file reading or parsing errors
            print(f"Error processing file {file_path}: {e}")

    return all_translations