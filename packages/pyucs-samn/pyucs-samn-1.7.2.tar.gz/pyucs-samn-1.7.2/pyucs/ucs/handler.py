
from ucsmsdk.ucshandle import UcsHandle, UcsException
from ucsmsdk import mometa
from pyucs.logging.handler import Logger
from pycrypt.encryption import AESCipher


class Ucs(UcsHandle):
    """
        This is a custom UCS class that is used to simplify some of the methods and processes
        with ucsmsdk into a single class class with simple method calls. The ucsmsdk lacks
        a lot of built-in 'functionality' and really only provides raw data returned via
        query_dn and query_classid. These are the only two meaningful methods of ucsmsdk
        and this class is an attempt to bring some simplified method calls to ucsmsdk.
        This class also encrypts the password so that it is not stored in clear text in memory.
    """

    def __init__(self, ip, username, password, port=None, secure=None,
                 proxy=None, timeout=None, query_classids=None):
        super().__init__(ip, username, password, port=port, secure=secure, proxy=proxy, timeout=timeout)
        self.cipher = AESCipher()
        self._password = self.cipher.encrypt(self._UcsSession__password)
        self._UcsSession__password = None
        self._connected = False
        # define default classids in which the Ucs object will by default
        # have properties for. Since these are default we assign immutable
        # and hidden Tuple object here.
        self._default_classids = ('OrgOrg',
                                  'FabricChassisEp',
                                  'ComputeBlade',
                                  'VnicLanConnTempl',
                                  'LsServer')
        self._query_classids = list(self._default_classids)
        # allow at initialization the option to add to the 'default' property list of managed objects
        if query_classids:
            self._query_classids.append(query_classids)
        # make the _query_classids property an immutable object after initialization
        self._query_classids = tuple(self._query_classids)

    def login(self, **kwargs):
        self.connect(**kwargs)

    def connect(self, **kwargs):
        """
        Connect method so that the password can be decrypted for the connection
        as well as to populate the default properties of the Ucs object
        :param kwargs:
        :return:
        """
        self._UcsSession__password = self.cipher.decrypt(self._password, self.cipher.AES_KEY)
        self._connected = self._login(**kwargs)
        self._UcsSession__password = None
        self.refresh_inventory()

    def logout(self, **kwargs):
        self.disconnect(**kwargs)

    def disconnect(self, **kwargs):
        self._logout(**kwargs)
        self._connected = False

    def refresh_inventory(self):
        self._is_connected()
        q = self.query_classids(*self._query_classids)
        for k in q.keys():
            setattr(self, k, q[k])

    def clear_default_properties(self):
        self._is_connected()
        q = self.query_classids(*self._query_classids)
        for k in q.keys():
            delattr(self, k)

    def _is_connected(self):
        """
        method to check if there is a connection to ucsm
        and raise an exception if not.
        This is used as a check prior to running any other
        methods.
        """
        if self._connected:
            return True
        else:
            raise UcsException(error_code=1,
                               error_descr='Not currently logged in. Please connect to a UCS domain first')

    def query_rn(self, rn, class_id):
        """
        Added a missing method that Cisco should add in the ability to query the relative_name (rn)
        of a managed object
        :param rn:
        :param class_id:
        :return:
        """
        return self.query_classid(class_id=class_id,
                                  filter_str='(rn, "{}")'.format(rn)
                                  )

    def _query_mo(self, class_id, chassis=None, slot=None, vlan_id=None, name=None,
                  service_profile=None, org=None, dn=None, rn=None):
        """
        This is a beast of a method and really the brains of the operation of all the
        availbel methods in this class.
        :param class_id: Required parameter
        :param chassis: required for chassis query
        :param slot: required for chassis/blade query
        :param vlan_id: required for vlan query
        :param name:
        :param service_profile: required for service_profile query
        :param org: required for org query
        :param dn: required for dn query
        :param rn: required for rn query
        :return: one or more managedObjects
        """
        self._is_connected()

        # The below is fairly self explanatory and won't be commented
        # built-in query_dn method
        if dn:
            return self.query_dn(dn=dn)

        # custom query_rn method with an optional org search filter
        if rn:
            if org:
                return self.query_classid(class_id=class_id,
                                          filter_str='((rn, "{}") and (dn, "{}"))'.format(rn, org))
            return self.query_rn(rn=rn, class_id=class_id)

        # vlan_id and optionally adding the name of the vlan
        if vlan_id:
            if name:
                return self.query_classid(class_id=class_id,
                                          filter_str='((id, "{}") and (name, "{}"))'.format(vlan_id, name))
            return self.query_classid(class_id=class_id,
                                      filter_str='(id, "{}")'.format(vlan_id))
        # search for anything with a name parameter and optionally use an org search filter
        if name:
            if org:
                return self.query_classid(class_id=class_id,
                                          filter_str='((name, "{}") and (dn, "{}"))'.format(name, org))
            return self.query_rn(rn=name, class_id=class_id)

        # chassis ID and optionally a blade slot id
        if chassis:
            if slot:
                return self.query_classid(class_id=class_id,
                                          filter_str='((chassis_id, "{}") and (slot_id, "{}"))'.format(chassis, slot))
            return self.query_classid(class_id=class_id,
                                      filter_str='(chassis_id, "{}")'.format(chassis))

        # all chassis blade slots with slot id
        if slot:
            return self.query_classid(class_id=class_id,
                                      filter_str='((slot_id, "{}"))'.format(slot))

        # service profile managedobject
        if service_profile:
            return self.query_classid(class_id=class_id,
                                      filter_str='((dn, "{}"))'.format(service_profile.dn)
                                      )

        # by default return all managedObjects from classid
        return self.query_classid(class_id=class_id)

    def get_vnic_template(self, name=None, org=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='VnicLanConnTempl',
                              name=name,
                              org=org,
                              dn=dn,
                              rn=rn
                              )

    def get_vnic(self, service_profile=None, dn=None):
        self._is_connected()

        if service_profile and isinstance(service_profile, mometa.ls.LsServer.LsServer):
            return self._query_mo(class_id='VnicEther',
                                  service_profile=service_profile,
                                  dn=dn
                                  )
        elif service_profile and isinstance(service_profile, str):
            raise UcsException(
                "InvalidType: Parameter 'service_profile' expected type "
                "'ucsmsdk.mometa.ls.LsServer.LsServer' and recieved 'str'")

        elif dn:
            self._query_mo(class_id='VnicEther',
                           dn=dn
                           )
        return self._query_mo(class_id='VnicEther')

    def get_vhba(self, service_profile=None, dn=None):
        self._is_connected()

        if service_profile and isinstance(service_profile, mometa.ls.LsServer.LsServer):
            return self._query_mo(class_id='VnicFc',
                                  service_profile=service_profile,
                                  dn=dn
                                  )
        elif service_profile and isinstance(service_profile, str):
            raise UcsException(
                "InvalidType: Parameter 'service_profile' expected type "
                "'ucsmsdk.mometa.ls.LsServer.LsServer' and recieved 'str'")

        elif dn:
            self._query_mo(class_id='VnicFc',
                           dn=dn
                           )
        return self._query_mo(class_id='VnicFc')

    def get_org(self, name=None, org=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='OrgOrg',
                              name=name,
                              org=org,
                              dn=dn,
                              rn=rn
                              )

    def get_vlan(self, name=None, vlan_id=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='FabricVlan',
                              name=name,
                              vlan_id=vlan_id,
                              dn=dn,
                              rn=rn
                              )

    def get_service_profile(self, name=None, org=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='LsServer',
                              name=name,
                              org=org,
                              dn=dn,
                              rn=rn
                              )

    def get_chassis(self, name=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='FabricChassisEp',
                              name=name,
                              dn=dn,
                              rn=rn
                              )

    def get_blade(self, chassis=None, slot=None, dn=None, rn=None):
        self._is_connected()
        return self._query_mo(class_id='ComputeBlade',
                              chassis=chassis,
                              slot=slot,
                              dn=dn,
                              rn=rn
                              )

    def get_vnic_stats(self, vnic=None, service_profile=None, ignore_error=False):
        self._is_connected()

        # check if a service profile was provided as a way to reduce returned results
        if isinstance(service_profile, mometa.ls.LsServer.LsServer):
            stats = self.get_vnic_stats(vnic=self.get_vnic(service_profile=service_profile), ignore_error=ignore_error)
            if stats:
                return stats

        # check if the vnic parameter is a managedobject
        if isinstance(vnic, mometa.vnic.VnicEther.VnicEther):
            if vnic.equipment_dn:
                return self.query_dn("{}/vnic-stats".format(vnic.equipment_dn))

        # if vnic is a list/tuple then loop through each one to get the stats of each
        if isinstance(vnic, list) or isinstance(vnic, tuple):
            tmp = []
            for v in vnic:
                if v.equipment_dn:
                    tmp.append(self.get_vnic_stats(v, ignore_error=ignore_error))
            return tmp
        if not ignore_error:
            raise UcsException("InvalidType: Unexpected type with parameter 'vnic'."
                               "Use type VnicEther or list/tuple of VnicEther")

    def get_vhba_stats(self, vhba=None, service_profile=None, ignore_error=False):
        self._is_connected()

        # check if a service profile was provided as a way to reduce returned results
        if isinstance(service_profile, mometa.ls.LsServer.LsServer):
            stats = self.get_vhba_stats(vhba=self.get_vnic(service_profile=service_profile), ignore_error=ignore_error)
            if stats:
                return stats

        # check if the vnic parameter is a managedobject
        if isinstance(vhba, mometa.vnic.VnicFc.VnicFc):
            if vhba.equipment_dn:
                return self.query_dn("{}/vnic-stats".format(vhba.equipment_dn))

        # if vnic is a list/tuple then loop through each one to get the stats of each
        if isinstance(vhba, list) or isinstance(vhba, tuple):
            tmp = []
            for v in vhba:
                if v.equipment_dn:
                    tmp.append(self.get_vhba_stats(v, ignore_error=ignore_error))
            return tmp

        if not ignore_error:
            raise UcsException("InvalidType: Unexpected type with parameter 'vhba'."
                               "Use type VnicFc or list/tuple of VnicFc")
