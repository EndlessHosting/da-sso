# DirectAdmin JWT SSO Server
This is an app we use in order to provide SSO to our DeskPRO instance through DirectAdmin.
### Info
This app should work with anything that can handle JWTs. Configurable support for the parameters is coming soon
### Can I demo this?
This software is in use at Endless Hosting. You'll need to [setup a DirectAdmin account](https://theendlessweb.com/signup), then you can log into our [helpdesk](https://support.theendlessweb.com).
### Setup
Edit `config.py`, run the app with Gunicorn! You'll also want to edit `templates/da_login.html`, to change the branding.
Configurable support for the branding is coming soon.
### License
This software is licensed under the MIT license, with modifications from the PortAudio license.
You may read the license in full in the LICENSE file.
### Attributions
This software was written by Adam Gilbert for use at Endless Hosting. The [DirectAdmin API](https://github.com/sensson/python-directadmin) was written by ju5t.
### Contributions
Pull requests and issues are encouraged! Please let me know any feedback you have.

# Version History
### Version 1.0
Initial functionality. The code for this version was not released.
### Version 1.1
Initial commit to Git, this version refactors and cleans functions. Comments were added, and the code was prepared to be uploaded to Git.