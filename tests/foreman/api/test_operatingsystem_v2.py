"""Unit tests for the ``operatingsystems`` paths.

References for the relevant paths can be found here:

* http://theforeman.org/api/apidoc/v2/operatingsystems.html
* http://theforeman.org/api/apidoc/v2/parameters.html

"""
from fauxfactory import gen_utf8
from robottelo.common.decorators import run_only_on
from robottelo import entities
from unittest import TestCase
# (too many public methods) pylint: disable=R0904


@run_only_on('sat')
class OSParameterTestCase(TestCase):
    """Tests for operating system parameters."""
    def test_bz_1114640(self):
        """@Test: Create a parameter for operating system 1.

        @Assert: A parameter is created and can be read afterwards.

        @Feature: OperatingSystemParameter

        """
        # Check whether OS 1 exists.
        entities.OperatingSystem(id=1).read_json()

        # Create and read a parameter for operating system 1. The purpose of
        # this test is to make sure an HTTP 422 is not returned, but we're also
        # going to verify the name and value of the parameter, just for good
        # measure.
        name = gen_utf8(20)
        value = gen_utf8(20)
        osp_id = entities.OperatingSystemParameter(
            1,
            name=name,
            value=value,
        ).create()['id']
        attrs = entities.OperatingSystemParameter(1, id=osp_id).read_json()
        self.assertEqual(attrs['name'], name)
        self.assertEqual(attrs['value'], value)


@run_only_on('sat')
class OSTestCase(TestCase):
    """Tests for operating systems."""
    def test_point_to_arch(self):
        """@Test: Create an operating system that points at an architecture.

        @Assert: The operating system is created and points at the given
        architecture.

        @Feature: OperatingSystem

        """
        arch_id = entities.Architecture().create()['id']
        os_id = entities.OperatingSystem(architecture=[arch_id]).create()['id']
        attrs = entities.OperatingSystem(id=os_id).read_json()
        self.assertEqual(len(attrs['architectures']), 1)
        self.assertEqual(attrs['architectures'][0]['id'], arch_id)

    def test_point_to_ptable(self):
        """@Test: Create an operating system that points at a partition table.

        @Assert: The operating system is created and points at the given
        partition table.

        @Feature: OperatingSystem

        """
        ptable_id = entities.PartitionTable().create()['id']
        os_id = entities.OperatingSystem(ptable=[ptable_id]).create()['id']
        attrs = entities.OperatingSystem(id=os_id).read_json()
        self.assertEqual(len(attrs['ptables']), 1)
        self.assertEqual(attrs['ptables'][0]['id'], ptable_id)
