# Government of Canada Freshdesk for Concierge
This is the Government of Canada Freshdesk for Concierge

## Quick start

### Install

    pip install concierge_freshdesk_plugin
    
### Configure
Add "concierge_freshdesk_plugin" to concierge's INSTALLED_APPS by adding it your
config.py's INSTALLED_APPS_PREFIX array.

    INSTALLED_APPS_PREFIX = [
        'concierge_freshdesk_plugin',
        ...
    ]

## Development
If you plan on making changes to freshdesk, instead of installing it using
pip, clone the repo and execute the following commands.

    python setup.py develop
    cd concierge_freshdesk_plugin
    yarn
    yarn build
    
## Building
To create a bundle ready for distribution, execute the following commands:

    (cd concierge_freshdesk_plugin && yarn && yarn build)
    python setup.py sdist
   
## Testing
To execute test locally, execute the following command:
    
    py.test
