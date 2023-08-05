import logging
logger = logging.getLogger(__name__)

from ec2userkeyd import clients, utils
from ec2userkeyd.methods.base import BaseCredentialSource


class UserRole(BaseCredentialSource):
    """AssumeRole to an existing user-oriented role.
    """

    def get(self, username, instance_role_name):
        identity = clients.sts.get_caller_identity()
        role_arn = (
            'arn:aws:iam::{account}:role/' + self.config.role_name_pattern
        ).format(account=identity['Account'], username=username)
        logger.debug(f'{username}: {role_arn}')
        
        # We're not going to check if the role exists, we're just
        # going to try it. We'll have the same response if the role
        # doesn't exist versus if the role exists but we can't
        # AssumeRole to it.
        try:
            response = clients.cached_assume_role(
                RoleArn=role_arn,
                RoleSessionName=username)
            return utils.assume_role_response(response)
        except clients.sts.exceptions.ClientError as ex:
            if 'AccessDenied' not in str(ex):
                raise ex
            logger.debug(str(ex))
            return None
