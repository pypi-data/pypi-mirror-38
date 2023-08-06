#!/usr/bin/env python3

"""A utility to setup (or update) a GitLab repository's labels and lists based
on the definitions provided in a text file. The module uses `argparse` and
responds to `-h`.


Alan Christie
November 2018
"""

import argparse
import re
import requests
import os
import sys

LABEL_DOC = 'GITLAB-LABELS.md'

GITLAB_API_V = 'v4'
GITLAB_API = 'https://gitlab.com/api/'

ACTION_SET = 'set'
ACTION_UPD = 'update'


# -----------------------------------------------------------------------------
# GitLabel
# -----------------------------------------------------------------------------
class LabLabel:  # pylint: disable=too-few-public-methods
    """In-memory representation of the configuration
     and the logic to execute it.
     """

    # -------------------------------------------------------------------------
    def apply(self, user_name, project_name, action, pat,
              api=GITLAB_API_V, test=False):
        """Applies the configuration by performing the variable substitution
         on the given files

         :param user_name: The name of the project user in GitLab
         :type user_name: ``str``
         :param project_name: The name of the project (repository) to label
         :type project_name: ``str``
         :param action: Whether to 'set' or 'update' labels
         :type action: ``str``
         :param pat: The project's Personal Access Code
         :type pat: ``str``
         :param api: The GitLab REST API to use
         :type api: ``str``
         :param test: True to test the inout file and not write to GitLab
         :type api: ``bool``
         """

        base_url = GITLAB_API + api

        # Parse labels out of the policy document...
        print('+ Looking for labels in the policy document...')
        policy_labels = {}
        in_labels = False
        cur_label = None
        cur_description = None
        re_label = re.compile('### (.+)')
        re_field = re.compile('- (.*):(.+)')
        with open(LABEL_DOC) as f:
            for line in f.readlines():
                lean_line = line.strip()
                if not in_labels:
                    if lean_line.startswith('## Common labels'):
                        in_labels = True
                elif in_labels:
                    if lean_line.startswith('## '):
                        if cur_description is not None:
                            if not cur_description.endswith('.'):
                                cur_description += '.'
                            policy_labels[cur_label]['description'] =\
                                cur_description
                        break
                    else:
                        match = re_label.match(lean_line)
                        if match:
                            if cur_description is not None:
                                if not cur_description.endswith('.'):
                                    cur_description += '.'
                                policy_labels[cur_label]['description'] =\
                                    cur_description
                            cur_label = match.group(1).strip()
                            policy_labels[cur_label] = {'name': cur_label}
                            cur_description = None
                        else:
                            match = re_field.match(lean_line)
                            if match:
                                field = match.group(1).strip().lower()
                                if field == 'colour':
                                    field = 'color'
                                value = match.group(2).strip()
                                if field != 'description':
                                    if (field == 'priority'
                                            or field == 'position'):
                                        policy_labels[cur_label][field] =\
                                            int(value)
                                    else:
                                        policy_labels[cur_label][field] = value
                                elif field == 'description':
                                    cur_description = value
                            elif cur_description and lean_line:
                                cur_description += ' ' + lean_line

        # Add any remaining description
        # i.e. if the last item if the file has ended.
        if cur_description is not None:
            policy_labels[cur_label]['description'] = cur_description

        num_policy_labels = len(policy_labels)
        print('- Found %s labels.' % len(policy_labels))
        if num_policy_labels < 1:
            print('Nothing to do.')
            sys.exit(0)

        # Search for the project's GitLab ID...
        print('+ Getting GitLab ID for %s project...' % project_name)
        hdr = {'Private-Token': pat}
        url = base_url + '/projects/{}%2F{}'.format(user_name, project_name)
        r = requests.get(url, headers=hdr)
        project = r.json()
        if 'error' in project:
            print('- Could not get projects ({})'. format(project['error']))
            sys.exit(1)
        if project['name'] == project_name:
            project_id = project['id']
        else:
            print('- Could not find project "%s" on %s' % (project_name,
                                                           GITLAB_API))
            sys.exit(1)
        print('- Got project (ID={})'.format(project_id))

        # Parse labels out of the policy document...
        print('+ Looking for board...')
        url = base_url + '/projects/%(id)s/boards' % {'id': project_id}
        r = requests.get(url, headers=hdr)
        boards = r.json()
        if len(boards) != 1:
            print()
            print('Expected 1 project issue board but found %s.' % len(boards))
            print('If this is the first time you have run this utility for')
            print('the project you might need to visit the project\'s issues')
            print('or boards just to poke it into life before trying again.')
            print()
            sys.exit(1)

        board_id = boards[0]['id']
        print('- Got ID %s.' % board_id)

        # Extract list labels that look like they're board lists.
        # These are labels that are black.
        board_lists = {}
        for policy_label in policy_labels:
            if policy_labels[policy_label]['color'] == '#000000':
                board_lists[policy_label] =\
                    {'position': policy_labels[policy_label]['position'],
                     'board_id': board_id}

        # Set or update the project's labels...
        print('+ Acting on project labels...')
        url = base_url + '/projects/%(id)s/labels' % {'id': project_id}
        num_errors = 0
        label_names = policy_labels.keys()
        for label_name in sorted(label_names):
            print('  ' + label_name)
            if not test:
                if action in [ACTION_UPD]:
                    r = requests.put(url,
                                     json=policy_labels[label_name],
                                     headers=hdr)
                    if r.status_code != 200:
                        print('    Failed! (%s)' % r.status_code)
                        num_errors += 1
                elif action in [ACTION_SET]:
                    r = requests.post(url,
                                      json=policy_labels[label_name],
                                      headers=hdr)
                    if r.status_code not in [201, 409]:
                        print('    Failed! (%s)' % r.status_code)
                        num_errors += 1

        if num_errors:
            print('- Acted (With Errors)')
        else:
            print('- Acted (Success)')

        # Nothing more to productively do if we're in test mode...
        if test:
            return

        if len(board_lists):

            # Here we create the lists
            # but, to order them we update them with a position
            # (which can;t be done when it's created)
            # In order to order we have to get the list ID from GitLab

            print('+ Acting on board lists...')

            # Get label IDs
            url = base_url + '/projects/%(id)s/labels' % {'id': project_id}
            r = requests.get(url, headers=hdr)
            if r.status_code != 200:
                print('    Failed! (%s)' % r.status_code)
                sys.exit(1)
            for label in r.json():
                if label['name'] in board_lists:
                    board_lists[label['name']]['label_id'] = label['id']

            # For lists to be ordered properly,
            # create them in position order.
            # We expect positions to run 1, 2, 3 etc.
            # and a board_list is expected to occupy each one.
            if action in [ACTION_SET]:
                num_errors = 0
                position = 1
                num_lists = len(board_lists)
                while position <= num_lists:
                    # Find board for this position...
                    found = False
                    board_list = None
                    for board_list in board_lists:
                        if board_lists[board_list]['position'] == position:
                            url = base_url + \
                                  '/projects/%(id)s/boards/%(bid)s/lists?' \
                                  'label_id=%(lid)s' % \
                                  {'id': project_id,
                                   'bid': board_id,
                                   'lid': board_lists[board_list]['label_id']}
                            r = requests.post(url, headers=hdr)
                            if r.status_code != 400 and r.status_code != 201:
                                print('    Failed! (%s)' % r.status_code)
                                num_errors += 1
                            found = True
                            break

                    if found:
                        print('  ' + board_list)
                    else:
                        print('    Could not find list for position %s' %
                              position)
                        num_errors += 1

                    position += 1

        if num_errors:
            print('- Acted (With Errors)')
        else:
            print('- Acted (Success)')


# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
def main():
    """The console script entry-point. Called when lablabel is executed
    or from __main__.py, which is used by the installed console script.
    """

    # Build the command-line parser
    # and parse the command-line
    cl_parser = argparse.ArgumentParser(
        description='Set or update GitLab labels'
                    ' and lists')
    cl_parser.add_argument('user',
                           help='The GitHub user name')
    cl_parser.add_argument('project',
                           help="The GitHub user's project name")
    cl_parser.add_argument('pat',
                           help='Your GitHub Personal Access Code')
    cl_parser.add_argument('action',
                           help='An action (set or update)',
                           choices=[ACTION_SET, ACTION_UPD])
    cl_parser.add_argument('--test',
                           help='Run the file processing but do not apply',
                           action='store_true')
    cl_parser.add_argument('--api',
                           help='Define the GitLab API. If not defined'
                                ' "{}" will be used'. format(GITLAB_API_V),
                           type=str,
                           default=GITLAB_API_V)
    args = cl_parser.parse_args()

    # Extract access code, project and action...
    pat = args.pat
    user_name = args.user
    project_name = args.project
    action = args.action

    # Does the label file exist?
    if not os.path.isfile(LABEL_DOC):
        print('ERROR: Label document ({}) does not exist'.format(LABEL_DOC))
        sys.exit(1)

    LabLabel().apply(user_name, project_name, action, pat,
                     args.api, args.test)

    print("Done.")


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
