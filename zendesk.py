from errbot import BotPlugin, botcmd
import logging

log = logging.getLogger(name='errbot.plugins.Zendesk')

try:
    import requests
except ImportError:
    log.error("Please install 'requests' python package")

class Zendesk(BotPlugin):
    """Plugin for Zendesk"""

    def get_configuration_template(self):
        """ configuration entries """
        config = {
            'api_url': None,
            'api_user': None,
            'api_pass': None,
            'domain': None,
        }
        return config

    @botcmd(split_args_with=" ")
    def zendesk(self, msg, args):
        """ Returns the subject of the ticket along with a link to it.
        Example:
            !zendesk <id>
        """

        ticket = args.pop(0)
        if ticket == '':
            self.send(msg.frm,
                      'id is required',
                      message_type=msg.type,
                      in_reply_to=msg,
                      groupchat_nick_reply=True)
            return

        username = self.config['api_user']
        password = self.config['api_pass']
        api_url = self.config['api_url']
        domain = self.config['domain']

        url = '{0}/tickets/{1}.json'.format(api_url, ticket)
        display_url = '{0}/tickets/{1}'.format(domain, ticket)
        req = requests.get(url, auth=(username, password))

        log.debug('ticket url: {}'.format(url))

        if req.status_code == requests.codes.ok:

            data = req.json()
            requester_user = self._get_name_by_id(data['ticket']['requester_id'])


            # This is a cases where a ticket is created but not assigned
            assignee_id = data['ticket']['assignee_id']
            if assignee_id is None:
                assignee_user = 'Unassigned'
            else:
                assignee_user = self._get_name_by_id(data['ticket']['assignee_id'])

            response = '{0} created by {2} on {1}. Assigned: {5}, Status: {4} - {3}'.format(
                data['ticket']['subject'],
                data['ticket']['created_at'],
                requester_user,
                display_url,
                data['ticket']['status'],
                assignee_user
            )
        else:
            response = 'Id {0} not found.'.format(ticket)

        self.send(msg.frm,
                  response,
                  message_type=msg.type,
                  in_reply_to=msg,
                  groupchat_nick_reply=True)

    def _get_name_by_id(self, id):

        username = self.config['api_user']
        password = self.config['api_pass']
        api_url = self.config['api_url']

        url = '{0}/users/{1}.json'.format(api_url, id)

        log.debug('user url: {}'.format(url))

        req = requests.get(url, auth=(username, password))
        data = req.json()

        return data['user']['name']
