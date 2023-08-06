#!/usr/bin/env python
"""
    JOCA -- Jira On Call Assignee -- Change project lead based on an ical event.
    Copyright (C) 2018 Bryce McNab

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import json
import sys
import re
import datetime
import time
import logging

try:
    import requests
except ImportError:
    logging.critical("ImportError for 'requests'; ensure it is installed.")
    sys.exit(71)

try:
    from icalendar import Calendar
except ImportError:
    logging.critical("ImportError for 'icalendar'; ensure it is installed.")
    sys.exit(71)

try:
    from jira import JIRA
except ImportError:
    logging.critical("ImportError for 'jira'; ensure it is installed.")
    sys.exit(71)

def get_current_project_lead(jira_config):
    """Polls Jira for the current project lead.

    Args:
        jira_config     dict    Server, username, password and project
                                key.
    Returns:
        String: user key.
    """
    logging.info("Project: %s", jira_config['project_key'].upper())
    jira = JIRA(jira_config['server'],
                basic_auth=(jira_config['username'],
                            jira_config['password']))
    project = jira.project(jira_config['project_key'].upper())
    logging.info("Current project lead: %s", project.lead.key)
    return project.lead.key

def get_supposed_lead(jira_config, url, regex):
    """Downloads current ICS file for parsing.

    Args:
        jira_config     dict    Server, username, password and project
                                key.
        url             str     URL for the ical file.
        regex           str     Regex string for parsing event
                                subjects.
    """
    jira = JIRA(jira_config['server'],
                basic_auth=(jira_config['username'],
                            jira_config['password']))
    cal = Calendar.from_ical(requests.get(url).text)
    for event in cal.walk():
        if event.name == "VEVENT":
            now = time.mktime(datetime.datetime.now().utcnow().timetuple())
            start = time.mktime(event.get('dtstart').dt.timetuple())
            end = time.mktime(event.get('dtend').dt.timetuple())
            if now > start and now < end:
                supposed_lead = re.search(regex, event.get('summary')).group(1)
                logging.debug("Event summary: %s", event.get('summary'))
                logging.debug("Regex find: %s", supposed_lead)
                logging.debug("End time of event: %s", event.get('dtend').dt.timetuple())
    assignee = jira.search_assignable_users_for_projects(supposed_lead,
                                                         jira_config['project_key'])[0].key
    logging.info("Supposed project lead: %s", assignee)
    return assignee

def assign_new_project_lead(jira_config, lead):
    """
    Args:
        jira_config     dict    Server, username, password and project
                                key.
        lead            str     User key to change to.
    """
    update_project_lead = requests.put(jira_config['server'] + \
                                       "/rest/api/latest/project/" + \
                                       jira_config['project_key'],
                                       json={"lead": lead},
                                       auth=(jira_config['username'],
                                             jira_config['password']))
    if update_project_lead.status_code == 200:
        logging.info("Assignee update successful.")
        return True
    else:
        logging.critical("Assignee update failed: %s", update_project_lead.status_code)
        sys.exit(76)

def main():
    """Main function, all work is done here."""
    with open('/etc/joca.config.json') as config_data_file:
        config_data = json.load(config_data_file)

    logging.basicConfig(filename=config_data['local']['logging']['file'],
                        format=config_data['local']['logging']['format'],
                        level=config_data['local']['logging']['level'].upper())

    logging.info("=== Starting sync ===")
    for project in config_data['projects']:
        jira_config = {
            "server": config_data['jira']['server'],
            "username": config_data['jira']['username'],
            "password": config_data['jira']['password'],
            "project_key": project['key']
        }
        current_lead_key = get_current_project_lead(jira_config)
        supposed_lead_key = get_supposed_lead(jira_config,
                                              project['ical'],
                                              project['regex'])
        if current_lead_key == supposed_lead_key:
            logging.info("No change is necessary, current assignee matches ical.")
        else:
            assign_new_project_lead(jira_config,
                                    supposed_lead_key)
    logging.info("=== Sync complete ===")

if __name__ == "__main__":
    main()
