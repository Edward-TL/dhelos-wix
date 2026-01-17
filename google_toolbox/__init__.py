import warnings
# Suppress the pkg_resources deprecation warning from google's core packages
warnings.filterwarnings("ignore", message=".*pkg_resources.*", category=UserWarning)

"""
Google Toolbox
"""

from google_toolbox.core import GoogleEnv, AuthMethodClass, DriveScopes
from google_toolbox.gdrive import GoogleDrive