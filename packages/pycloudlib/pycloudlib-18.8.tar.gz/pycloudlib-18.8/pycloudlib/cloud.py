# This file is part of pycloudlib. See LICENSE file for license information.
"""Base class for all other clouds to provide consistent set of functions."""

import datetime
import getpass
import logging

from pycloudlib.key import KeyPair


class BaseCloud:
    """Base Cloud Class."""

    _type = 'base'

    def __init__(self, tag):
        """Initialize base cloud class.

        Args:
            tag: string used to name and tag resources with
        """
        self._log = logging.getLogger(__name__)

        _username = getpass.getuser()
        self.key_pair = KeyPair(
            '/home/%s/.ssh/id_rsa.pub' % _username, name=_username
        )
        self.tag = '%s-%s' % (
            tag, datetime.datetime.now().strftime("%m%d-%H%M%S")
        )

    def delete_image(self, image_id):
        """Delete an image.

        Args:
            image_id: string, id of the image to delete
        """
        raise NotImplementedError

    def daily_image(self, release):
        """ID of the latest image for a particular release.

        Args:
            release: The release to look for

        Returns:
            A single string with the latest image ID for the specified release

        """
        raise NotImplementedError

    def get_instance(self, instance_id):
        """Get an instance by id.

        Args:
            instance_id:

        Returns:
            An instance object to use to manipulate the instance further.

        """
        raise NotImplementedError

    def launch(self, instance_type, image_id, wait=False, **kwargs):
        """Launch an instance.

        Args:
            instance_type: string, type of instance to create
            image_id: string, image ID to use for the instance
            wait: wait for instance to be live
            **kwargs: dictionary of other arguments to pass to launch

        Returns:
            An instance object to use to manipulate the instance further.

        """
        raise NotImplementedError

    def snapshot(self, instance_id, clean=True, wait=True):
        """Snapshot an instance and generate an image from it.

        Args:
            instance: Instance to snapshot
            clean: run instance clean method before taking snapshot
            wait: wait for instance to get created

        Returns:
            An image object

        """
        raise NotImplementedError

    def use_key(self, public_key_path, private_key_path=None, name=None):
        """Use an existing key.

        Args:
            public_key_path: path to the public key to upload
        """
        raise NotImplementedError
