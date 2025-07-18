@echo off
setlocal

:: Set the path where all profiles are stored
set "PROFILE_DIR=C:\Users\Lenovo\selenium_profiles"

echo [🧹] Cleaning up temporary profiles in: %PROFILE_DIR%

:: Loop through all folders in the profile directory
for /d %%F in ("%PROFILE_DIR%\*") do (
    if /I not "%%~nxF"=="instagram_profile" (
        echo Deleting folder: %%F
        rmdir /s /q "%%F"
    )
)

echo [✔] Cleanup complete. Only 'instagram_profile' retained.
pause

