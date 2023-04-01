# Stash Topaz Gigapixel AI, Performer Image Upscaler

This is a plugin for Stash App, that will use the program Topaz Gigapixel AI, to upscale or downscale performer images that are tagged with the relavent tags.

## Topaz Gigapixel Version Required

[Topaz Gigapixel AI](https://www.topazlabs.com/gigapixel-ai) **v6** of **newer** required

## Other Requirements

For the plugin to be able to upload upscaled images to Stash, the feature Custom Served Folders must be enabled, detailed here, [Advanced Configuration Options](https://github.com/stashapp/stash/wiki/Advanced-Configuration-Options), and here, [Add custom served folders](https://github.com/stashapp/stash/pull/620)

## Usage

1. Copy repository into Stash plugins folder.
2. In repository folder setup a Python virtual enviorment under .venv and install requirements or edit upscale.yml and just enter ' - "python"' instead of ' - "/.venv/Scripts/python"'
3. Install requirements.txt with Pipo
4. Open config.py and fill out requirements
    * STASH_URL (Url to your Stash instance)
    * API_KEY (The API Key if set under Settings > Security > Authentication)
    * CUSTOM_MAPPED_FOLDER & CUSTOM_MAPPED_URL, setup using guide here, [Add custom served folders](https://github.com/stashapp/stash/pull/620)
        * Usually in main Stash Folder, open config.yml and add something like this <a href="#example">Example</a>:
    * SET_TAG_IMAGE_GENERATION (Set to Yes, uncomment or set to No, this allows SVG images to be added to the tags created during Setup Tags)
    * EXE_PATH (Path to Topaz Gigapixel Executable, should not need set, as if not set during runnning of any Tasks, there is a variable check and if unset version_query.py runs and saves the value to config.py, when variable is set version_query.py will not run. If changing the Gigapixel installation path, be sure to update or delete the variable value)
    * VERSION (Version of Topaz Gigapixel), same as above, should not need to be set and the script queries it. Be sure to update or delete variable value, when updating Gigapixel
    * IMAGE_NAME (Name for the image that will be saved from Stash and processed through Gigapixel)
    * OUTPUT_SUFFIX (A suffix name that Gigapixel will add to processed images, which the script uses to identify for uploading to Stash)
        * Set in Topaz Gigapixel by navigating to File > Preferences > Processing / Save (Left Pane) > Default filename suiffix (Right Pane)
            * Unset or clear Default filename prefix or plugin will not work
            * Uncheck add scaling mode to filename or Plugin will not work
    * IMAGE_TYPES (A list of image types that are compatible with Gigapixel, if Performer image downloaded from Stash is not compatible, the Plugin will convert it to a compatible format before upscaling)
5. Goto Stash Settings > Plugins, and press Reload Plugins. The plugin will now appear in Settings > Tasks
6. Press Setup Tags, to create a list of tags featureing both available scales and modes for Gigapixel
7. Tag performers you wish to upscale with relavent tags
8. In Setting > Tasks, under Upscale Performer Images, press "Run Upscaler"
    * Once the upscaler is running, do not use the computer mouse, as this plugin relies on Pywinauto to automate Gigapixel. Using the mouse will result in Gigapixel windows not found errors and will halt the plugin

### Example *Add this to config.yml*

```yaml
custom_served_folders:<br />
  /: {Including drive letter, Path to Stash installation}\custom\static<br />
```

*I.E.*

```yaml
custom_served_folders:
  /: C:\Stash\custom\static
```

Use the folder path you set above to set the CUSTOM_MAPPED_FOLDER variable in config.py and for the CUSTOM_MAPPED_URL variable this will generally resolve to "http://localhost:9999/custom", or whichever ports you've setup Stash with

## Known Bugs

Microsoft Powertoys and some of it's features interfere with the Plugins ability to press the save button on Gigapxel, so if experiencing problem in saving close Powertoys.
