# Arxiv Copilot

ArXiv Copilot is a chrome extensions for google docs that recommends papers from arXiv based on the text you are writing.

## User Guide

### Installation

1. Download the latest version of the extension from [here](https://github.com/artefactory/redisventures-hackunamadata).
2. Go to `chrome://extensions/` in your browser.
3. Click on `Load unpacked` and select the folder `redisventures-hackunamadata/browser_extension` where you downloaded the repository.

### Configuration

1. Click on the extension icon in the top right corner of your browser.
2. Select the `Options` tab.
3. Configure the rest of the extension to your liking.
4. Press `Enter` to save your changes.

### Usage

1. Open a new google doc.
2. Start writing.
3. See the recommendations pop up as you write.
4. Click on the recommendations to open the paper in a new tab.

### Advanced Usage - Text collection method

Currently you are given the choice between two text collection methods:
1. `keyboards`: This method collects text from the keyboard events. This is the default method. It is not the most accurate method but it is the most performant.
2. `textContent`: This method collects text from the `textContent` property of the google doc. This method is more accurate but it is also more performant. However, it requires the user to refresh the page after each change so that the extension can collect the new text.

## Developper Guide

### Chome extension lifecycle

See [here](https://developer.chrome.com/extensions/getstarted#manifest) for more details.

### Architecture

See [here](../README.md) for more details.