from django.test import TestCase
from console_base.menu import get_menu
from console_base import auth, models
from console_base.library import *
import json


class MenuTest(TestCase):
    CLUSTER_ID = None
    NODE_ID = None
    NEW_NODE_ID = None
    USER = None

    def setUp(self):
        user = models.NmUser(name='fabregas', password_hash='26c01dbc175433723c0f3ad4d5812948', email_address='blikporject@gmail.com', additional_info='')
        user.save()

        role = models.NmRole(role_sid='clusters_ro', role_name='Clusters viewer role')
        role.save()
        models.NmUserRole(user=user, role=role).save()

        role = models.NmRole(role_sid='nodes_ro', role_name='Nodes viewer role')
        role.save()
        models.NmUserRole(user=user, role=role).save()

        role = models.NmRole(role_sid='operlogs_viewer', role_name='Operations logs viewer role')
        role.save()
        models.NmUserRole(user=user, role=role).save()

        role = models.NmRole(role_sid='syslogs_viewer', role_name='Operations logs viewer role')
        role.save()
        models.NmUserRole(user=user, role=role).save()

        role = models.NmRole(role_sid='users_admin', role_name='Users administrator role')
        role.save()
        models.NmUserRole(user=user, role=role).save()

        cl_type = models.NmClusterType(type_sid='common', description='test')
        cl_type.save()
        cluster = models.NmCluster(cluster_sid='UT_CLUSTER_01', cluster_type=cl_type, cluster_name='Test cluster', description='', status=1, last_modifier_id=1)
        cluster.save()

        nd_type = models.NmNodeType(type_sid='common', description='common node')
        nd_type.save()
        node = models.NmNode(node_uuid='some_uuid', cluster=cluster, node_type=nd_type, hostname='UT-NODE-01', logic_name='Test node #1', login='', password='', last_modifier_id=user.id, mac_address='00:00:00:33:44:55', ip_address='192.22.44.1', architecture='x86_64')
        node.save()

        #crete unregistered node
        new_node = models.NmNode(node_uuid='unregistered_node_uuid', node_type=nd_type, hostname='UNREGISTERED-NODE', logic_name='Test node #2', login='', password='', last_modifier_id=user.id, mac_address='00:00:22:33:44:55', ip_address='192.22.44.2', architecture='x86', admin_status=NEW_NODE)
        new_node.save()

        auth.cache_users()

        #setup test cluster configuration
        int_val = models.NmConfigSpec(config_object=OT_CLUSTER, object_type_id=cl_type.id,  parameter_name='Test integer', parameter_type=PT_INTEGER, posible_values_list='', default_value='')
        int_val.save()
        int_list = models.NmConfigSpec(config_object=OT_CLUSTER, object_type_id=cl_type.id, parameter_name='Test integer list', parameter_type=PT_INTEGER, posible_values_list='0|1|2|3|4|5|6|7|8|9', default_value='5')
        int_list.save()
        str_val = models.NmConfigSpec(config_object=OT_CLUSTER, object_type_id=cl_type.id, parameter_name='String value', parameter_type=PT_STRING, posible_values_list='', default_value='')
        str_val.save()
        str_list = models.NmConfigSpec(config_object=OT_CLUSTER, object_type_id=cl_type.id, parameter_name='String list', parameter_type=PT_STRING, posible_values_list='Value #1|Value #2', default_value='')
        str_list.save()
        hidden_val = models.NmConfigSpec(config_object=OT_CLUSTER, object_type_id=cl_type.id, parameter_name='Hidden string', parameter_type=PT_HIDDEN_STRING, posible_values_list='', default_value='')
        hidden_val.save()

        models.NmConfig(object_id=cluster.id, parameter=int_val, parameter_value=4, last_modifier=user).save()

        MenuTest.CLUSTER_ID = cluster.id
        MenuTest.NODE_ID = node.id
        MenuTest.NEW_NODE_ID = new_node.id
        MenuTest.USER = user


    def test_menu_load(self):

        menu = get_menu()

        self.failUnlessEqual(len(menu)>0, True)
        self.failUnlessEqual(menu[0].has_key('children'), True)

    def test_01_authenticate(self):
        try:
            auth.authenticate('fabregas', 'test')

            auth.authenticate('fabregas1', 'blik')
        except Exception, err:
            pass
        else:
            raise Exception('Should be exception in this case')

        user = auth.authenticate('fabregas', 'blik')
        self.failUnlessEqual(user.name, 'fabregas')
        self.failUnlessEqual(user.email_address, 'blikporject@gmail.com')

        #update user
        old_pwd = user.password_hash
        user.password_hash = '8977dfac2f8e04cb96e66882235f5aba' #md5 of 'changed'
        user.save()

        auth.update_user_cache(user)

        try:
            auth.authenticate('fabregas', 'blik')
        except Exception, err:
            pass
        else:
            raise Exception('Should be exception in this case')

        user = auth.authenticate('fabregas', 'changed')
        self.failUnlessEqual(user.name, 'fabregas')

        #restore default password
        user.password_hash = old_pwd
        user.save()
        auth.update_user_cache(user)

    def authenticate(self):
        resp = self.client.post( '/auth/', {'username':'fabregas','passwd':'blik'}, follow=True)
        return resp.status_code

    def switch_to_megaadmin(self):
        #create write roles
        role = models.NmRole(role_sid='clusters_rw', role_name='Clusters writer role')
        role.save()
        models.NmUserRole(user=MenuTest.USER, role=role).save()

        role = models.NmRole(role_sid='nodes_rw', role_name='Nodes writer role')
        role.save()
        models.NmUserRole(user=MenuTest.USER, role=role).save()

        auth.cache_users()

    def test_02_read_auth(self):
        #try getting / page, should be redirected to /auth 
        resp = self.client.get('/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('auth_form') > 0, True)

        #get auth page
        resp = self.client.get('/auth/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('auth_form') > 0, True)

        #try authenticate
        resp = self.client.post( '/auth/', {'username':'fabregas','passwd':'blik'}, follow=True)
        self.assertEqual(resp.status_code, 200)

        #must redirect to /
        self.assertEqual(resp.content.find('auth_form') > 0, False)

    def test_03_clusters_list(self):
        #should be redirected to /auth page
        resp = self.client.get('/clusters_list', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('clusters_list_table') > 0, False)

        #get list of clusters
        status = self.authenticate()
        self.assertEqual(status, 200)
        resp = self.client.get('/clusters_list', follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('clusters_list_table') > 0, True)
        self.assertEqual(resp.content.find('UT_CLUSTER_01') > 0, True)
        self.assertEqual(resp.content.find('common') > 0, True)

    def test_04_view_cluster_parameters(self):
        #should be redirected to /auth page
        resp = self.client.get('/cluster_config/%s'%MenuTest.CLUSTER_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('cluster_params_table') > 0, False)

        #get list of cluster's parameters
        status = self.authenticate()
        self.assertEqual(status, 200)
        resp = self.client.get('/cluster_config/%s'%MenuTest.CLUSTER_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('cluster_params_table') > 0, True)
        self.assertEqual(resp.content.find('clusterName') > 0, True)
        self.assertEqual(resp.content.find('clusterDescr') > 0, True)
        self.assertEqual(resp.content.count('int_value'), 1)
        self.assertEqual(resp.content.count('option') > 10, True)

    def test_05_change_cluster_parameters(self):
        resp = self.client.get('/change_cluster_parameters/%s'%MenuTest.CLUSTER_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('cluster_params_table') > 0, False)

        #user is not autorized for this action
        resp = self.client.post('/change_cluster_parameters/%s'%MenuTest.CLUSTER_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('cluster_params_table') > 0, False)

        self.switch_to_megaadmin()

        specs = models.NmConfigSpec.objects.all()
        params = {}
        for spec in specs:
            params[spec.id] = 'test value'
        params['clusterName'] = 'new_cluster_name'
        params['clusterDescr'] = 'new_description'

        status = self.authenticate()
        self.assertEqual(status, 200)
        resp = self.client.post('/change_cluster_parameters/%s'%MenuTest.CLUSTER_ID, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('cluster_params_table') > 0, True)

        for item in models.NmConfig.objects.all():
            self.assertEqual(item.parameter_value, 'test value')

        cluster = models.NmCluster.objects.get(id=MenuTest.CLUSTER_ID)
        self.assertEqual(cluster.cluster_name, 'new_cluster_name')
        self.assertEqual(cluster.description, 'new_description')

    def test_06_new_cluster(self):
        resp = self.client.get('/new_cluster/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('new_cluster_form') > 0, False)

        self.switch_to_megaadmin()
        status = self.authenticate()
        self.assertEqual(status, 200)

        resp = self.client.get('/new_cluster/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('new_cluster_form') > 0, True)
        self.assertEqual(resp.content.find('symbolID') > 0, True)
        self.assertEqual(resp.content.find('clusterTypeID') > 0, True)
        self.assertEqual(resp.content.find('clusterName') > 0, True)
        self.assertEqual(resp.content.find('description') > 0, True)

        cluster_type_id = models.NmClusterType.objects.all()[0].id
        params = {'symbolID': 'UT_cluster_01', 'clusterTypeID':cluster_type_id, 'clusterName':'test #1', 'description': 'test description'}
        resp = self.client.post('/new_cluster/', params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('inform_area') > 0, True)

        new_cluster = models.NmCluster.objects.get(cluster_sid='UT_cluster_01')
        self.assertEqual(new_cluster.cluster_name, 'test #1')
        self.assertEqual(new_cluster.description, 'test description')
        self.assertEqual(new_cluster.cluster_type_id, cluster_type_id)

        #try delete created cluster
        resp = self.client.get('/delete_cluster/%s'%new_cluster.id, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('deleted!') > 0, True)
        deleted_cluster = models.NmCluster.objects.filter(cluster_sid='UT_cluster_01')
        self.assertEqual(len(deleted_cluster), 0)

    def test_07_nodes_list(self):
        #should be redirected to /auth page
        resp = self.client.get('/cluster_nodes/%s'%MenuTest.CLUSTER_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('nodes_list_table') > 0, False)

        #get list of nodes
        status = self.authenticate()
        self.assertEqual(status, 200)
        resp = self.client.get('/cluster_nodes/%s'%MenuTest.CLUSTER_ID, follow=True)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('nodes_list_table') > 0, True)
        self.assertEqual(resp.content.find('UT-NODE-01') > 0, True)
        self.assertEqual(resp.content.find('00:00:00:33:44:55') > 0, True)

    def test_08_configure_node_page(self):
        #should be redirected to /auth page
        resp = self.client.get('/configure_node/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('node_params_table') > 0, False)

        #get list of node's parameters
        status = self.authenticate()
        self.assertEqual(status, 200)
        resp = self.client.get('/configure_node/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('node_params_table') > 0, True)
        self.assertEqual(resp.content.find('node_base_params_table') > 0, True)

    def test_09_change_node_parameters(self):
        resp = self.client.get('/change_node_parameters/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('node_params_table') > 0, False)

        status = self.authenticate()
        self.assertEqual(status, 200)
        #user is not autorized for this action
        resp = self.client.post('/change_node_parameters/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('node_params_table') > 0, False)

        self.switch_to_megaadmin()

        specs = models.NmConfigSpec.objects.all()
        params = {}
        for spec in specs:
            params[spec.id] = 'test value'
        params['logicalName'] = 'changed'

        resp = self.client.post('/change_node_parameters/%s'%MenuTest.NODE_ID, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('node_params_table') > 0, True)

        for item in models.NmConfig.objects.filter(object_id=MenuTest.NODE_ID):
            self.assertEqual(item.parameter_value, 'test value')

        node = models.NmNode.objects.get(id=MenuTest.NODE_ID)
        self.assertEqual(node.logic_name, 'changed')

    def test_09_change_base_node_parameters(self):
        resp = self.client.get('/change_base_node_params/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('node_base_params_table') > 0, False)

        status = self.authenticate()
        self.assertEqual(status, 200)
        #user is not autorized for this action
        resp = self.client.post('/change_base_node_params/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('node_params_table') > 0, False)

        self.switch_to_megaadmin()

        node = models.NmNode.objects.get(id=MenuTest.NODE_ID)
        node_type_id = node.node_type.id
        params = dict()
        params['hostname'] = 'NEW-HOSTNAME'
        params['nodeType'] = node_type_id
        params['architecture'] = 'x86'

        resp = self.client.post('/change_base_node_params/%s'%MenuTest.NODE_ID, params, follow=True)
        self.assertEqual(resp.content.find('Parameters are installed for node!') > 0, True)

        node = models.NmNode.objects.get(id=MenuTest.NODE_ID)
        self.assertEqual(node.hostname, 'NEW-HOSTNAME')
        self.assertEqual(node.node_type.id, node_type_id)
        self.assertEqual(node.architecture, 'x86')

        #try change hostname to 'bad hostname'
        params['hostname'] = 'BAD_HOSTNAME'
        resp = self.client.post('/change_base_node_params/%s'%MenuTest.NODE_ID, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('Hostname is invalid') > 0, True)

        node = models.NmNode.objects.get(id=MenuTest.NODE_ID)
        self.assertEqual(node.hostname, 'NEW-HOSTNAME')
        self.assertEqual(node.node_type.id, node_type_id)
        self.assertEqual(node.architecture, 'x86')

        #put optional parameters (for node registration)
        params['hostname'] = 'registered-node'
        params['clusterId'] = MenuTest.CLUSTER_ID
        params['logicName'] = 'test node'
        resp = self.client.post('/change_base_node_params/%s'%MenuTest.NODE_ID, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('Parameters are installed for node!') > 0, True)
        node = models.NmNode.objects.get(id=MenuTest.NODE_ID)
        self.assertEqual(node.hostname, 'registered-node')
        self.assertEqual(node.cluster.id, MenuTest.CLUSTER_ID)
        self.assertEqual(node.logic_name, 'test node')

    def test_10_delete_node(self):
        resp = self.client.get('/delete_node/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('is deleted') > 0, False)

        self.switch_to_megaadmin()
        status = self.authenticate()
        self.assertEqual(status, 200)

        resp = self.client.get('/delete_node/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('is deleted') > 0, True)

        nodes = models.NmNode.objects.filter(id=MenuTest.NODE_ID)
        self.assertEqual(len(nodes), 0)

    def test_11_base_nodes_operations(self):
        #TODO: this testcase should mock operations backend
        resp = self.client.get('/reboot_node/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('is not supported') > 0, False)

        resp = self.client.get('/sync_node/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('is not supported') > 0, False)

        self.switch_to_megaadmin()
        status = self.authenticate()
        self.assertEqual(status, 200)

        resp = self.client.get('/reboot_node/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('is not supported') > 0, True)

        resp = self.client.get('/sync_node/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('is not supported') > 0, True)

    def test_12_unregister_nodes_list(self):
        resp = self.client.get('/unregistered_nodes', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('nodes_list_table') > 0, False)

        status = self.authenticate()
        self.assertEqual(status, 200)

        resp = self.client.get('/unregistered_nodes', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('nodes_list_table') > 0, True)
        self.assertEqual(resp.content.find('UNREGISTERED-NODE') > 0, True)

    def test_13_register_node_form(self):
        resp = self.client.get('/register_node/%s'%MenuTest.NEW_NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('node_base_params_table') > 0, False)

        self.switch_to_megaadmin()
        status = self.authenticate()
        self.assertEqual(status, 200)

        resp = self.client.get('/register_node/%s'%MenuTest.NEW_NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.content.find('node_base_params_table') > 0, True)
        self.assertEqual(resp.content.find('clusterId') > 0, True)
        self.assertEqual(resp.content.find('logicName') > 0, True)

        resp = self.client.get('/register_node/%s'%MenuTest.NODE_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('already registered!') > 0, True)

    def test_14_operations_logs(self):
        resp = self.client.get('/operations_log/%s'%MenuTest.CLUSTER_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('operations_logs_table') > 0, False)

        status = self.authenticate()
        self.assertEqual(status, 200)
        resp = self.client.get('/operations_log/%s'%MenuTest.CLUSTER_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('operations_logs_table') > 0, True)

        params = {'sortname': 'undefined', 'sortorder': 'desc', 'cluster_id':MenuTest.CLUSTER_ID, 'node':MenuTest.NODE_ID, 'page':1, 'rp':10}
        resp = self.client.post('/get_operlogs_data/', params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp._headers['content-type'][1], 'application/json')
        data = json.loads(resp.content)
        self.assertEqual(data.has_key('rows'), True)
        self.assertEqual(data.has_key('total'), True)
        self.assertEqual(data.has_key('page'), True)

    def test_15_system_logs(self):
        resp = self.client.get('/system_log/%s'%MenuTest.CLUSTER_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('system_logs_table') > 0, False)

        status = self.authenticate()
        self.assertEqual(status, 200)
        resp = self.client.get('/system_log/%s'%MenuTest.CLUSTER_ID, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('system_logs_table') > 0, True)

        params = {'sortname': 'undefined', 'sortorder': 'desc', 'cluster_id':MenuTest.CLUSTER_ID, 'node':MenuTest.NODE_ID, 'message':'a', 'page':1, 'rp':10}
        resp = self.client.post('/get_syslog_data/', params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp._headers['content-type'][1], 'application/json')
        data = json.loads(resp.content)
        self.assertEqual(data.has_key('rows'), True)
        self.assertEqual(data.has_key('total'), True)
        self.assertEqual(data.has_key('page'), True)

    def test_16_users_management_auth(self):
        resp = self.client.get('/users_list/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('users_list_table') > 0, True)
        self.assertEqual(resp.content.find('fabregas') > 0, True)

        resp = self.client.get('/edit_user/666', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('auth_form') > 0, True)

        resp = self.client.get('/edit_user_roles/666', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('auth_form') > 0, True)

        resp = self.client.get('/delete_user/666', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('auth_form') > 0, True)


    def create_user(self):
        resp = self.client.get('/create_new_user/', follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('new_user_table') > 0, True)

        #create new user...
        params = {'user_name': 'new_user', 'password':'1', 're_password':'1', 'email':'test@domain.com', 'addinfo':'---'}
        resp = self.client.post('/create_new_user/', params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('created!') > 0, True)
        user = models.NmUser.objects.get(name='new_user')
        self.assertEqual(user.email_address, 'test@domain.com')
        self.assertEqual(user.additional_info, '---')

        params['user_name'] = ''
        resp = self.client.post('/create_new_user/', params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('should be not empty!') > 0, True)

        params['user_name'] = 'new_user2'
        params['email'] = 'fail'
        resp = self.client.post('/create_new_user/', params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('is not valid!') > 0, True)

        params['email'] = 'test@domain.com'
        params['re_password'] = ''
        resp = self.client.post('/create_new_user/', params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('are not equal!') > 0, True)

        return user.id

    def edit_user(self, user_id):
        resp = self.client.get('/edit_user/%s'%user_id, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('edit_user_table') > 0, True)

        params = {'email':'new@domain.com', 'addinfo':'', 'password':'', 're_password':''}
        resp = self.client.post('/edit_user/%s'%user_id, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('updated!') > 0, True)

        user = models.NmUser.objects.get(id=user_id)
        self.assertEqual(user.email_address, 'new@domain.com')
        self.assertEqual(user.additional_info, '')
        passwd = user.password_hash

        params = {'email':'new@domain.com', 'addinfo':'', 'password':'123', 're_password':'123'}
        resp = self.client.post('/edit_user/%s'%user_id, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('updated!') > 0, True)
        user = models.NmUser.objects.get(id=user_id)
        self.assertNotEqual(user.password_hash, passwd)

        params['password'] = '321'
        resp = self.client.post('/edit_user/%s'%user_id, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('are not equal!') > 0, True)

        params['password'] = '123'
        params['email'] = 'fail'
        resp = self.client.post('/edit_user/%s'%user_id, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('is not valid!') > 0, True)

    def edit_user_roles(self, user_id):
        resp = self.client.get('/edit_user_roles/%s'%user_id, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('all_roles_list_table') > 0, True)
        self.assertEqual(resp.content.find('user_roles_list_table') > 0, True)

        role = models.NmRole.objects.all()[0]
        user = models.NmUser.objects.get(id=user_id)
        params = {'method':'push', 'value':role.id}
        resp = self.client.post('/edit_user_roles/%s'%user_id, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('ok') >= 0, True)
        ur = models.NmUserRole.objects.filter(role=role, user=user)
        self.assertEqual(len(ur), 1)

        resp = self.client.post('/edit_user_roles/%s'%user_id, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('ok') >= 0, True)
        ur = models.NmUserRole.objects.filter(role=role, user=user)
        self.assertEqual(len(ur), 1)

        params['method'] = 'pop'
        resp = self.client.post('/edit_user_roles/%s'%user_id, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('ok') >= 0, True)
        ur = models.NmUserRole.objects.filter(role=role, user=user)
        self.assertEqual(len(ur), 0)

        resp = self.client.post('/edit_user_roles/%s'%user_id, params, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('ok') >= 0, True)

    def delete_user(self, user_id):
        resp = self.client.get('/delete_user/%s'%user_id, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.content.find('deleted!') > 0, True)
        user = models.NmUser.objects.filter(id=user_id)
        self.assertEqual(len(user), 0)

    def test_17_users_management(self):
        status = self.authenticate()
        self.assertEqual(status, 200)

        user_id = self.create_user()
        self.edit_user(user_id)
        self.edit_user_roles(user_id)
        self.delete_user(user_id)
