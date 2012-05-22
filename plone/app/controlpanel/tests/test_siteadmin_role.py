import re
from urllib import urlencode

from plone.app.controlpanel.tests.cptc import UserGroupsControlPanelTestCase


class TestSiteAdministratorRoleFunctional(UserGroupsControlPanelTestCase):

    def afterSetUp(self):
        super(TestSiteAdministratorRoleFunctional, self).afterSetUp()

        # add a user with the Site Administrator role
        self.portal.portal_membership.addMember('siteadmin', 'secret', ['Site Administrator'], [])

        token_re = re.compile(r'name="_authenticator" value="([^"]+)"')
        self.browser.addHeader('Authorization', 'Basic root:secret')
        self.browser.open(self.portal.absolute_url()+'/@@usergroup-userprefs')
        self.manager_token = token_re.search(self.browser.contents).group(1)
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(self.portal.absolute_url()+'/@@usergroup-userprefs')
        self.siteadmin_token = token_re.search(self.browser.contents).group(1)

        self.normal_user = 'DIispfuF'

    def testControlPanelOverview(self):
        # make sure we can view the Site Setup page,
        # at both old and new URLs
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(self.portal.absolute_url()+'/plone_control_panel')
        self.assertEqual('200 Ok', self.browser.headers['status'])
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(self.portal.absolute_url()+'/@@overview-controlpanel')
        self.assertEqual('200 Ok', self.browser.headers['status'])

    def testUserManagerRoleCheckboxIsDisabledForNonManagers(self):
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(self.portal.absolute_url()+'/@@usergroup-userprefs')
        contents = self.simplify_white_space(self.browser.contents)
        self.assertTrue('<input type="checkbox" class="noborder" '
                        'name="users.roles:list:records" value="Manager" '
                        'disabled="disabled" />' in contents)

    def testManagerCanDelegateManagerRoleForUsers(self):
        # a user with the Manager role can grant the Manager role
        form = {
            '_authenticator': self.manager_token,
            'users.id:records': self.normal_user,
            'users.roles:list:records': 'Manager',
            'form.button.Modify': 'Apply Changes',
            'form.submitted': 1,
            }
        post_data = urlencode(form)
        self.browser.addHeader('Authorization', 'Basic root:secret')
        self.browser.post(self.portal.absolute_url()+'/@@usergroup-userprefs',
                          post_data)
        self.assertEqual('200 Ok', self.browser.headers['status'])
        roles = self.portal.acl_users.getUserById(self.normal_user).getRoles()
        self.assertEqual(['Manager', 'Authenticated'], roles)

    def testNonManagersCannotDelegateManagerRoleForUsers(self):
        # a user without the Manager role cannot delegate the Manager role
        form = {
            '_authenticator': self.siteadmin_token,
            'users.id:records': self.normal_user,
            'users.roles:list:records': 'Manager',
            'form.button.Modify': 'Apply Changes',
            'form.submitted': 1,
            }
        post_data = urlencode(form)
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.post(self.portal.absolute_url()+'/@@usergroup-userprefs',
                          post_data)
        self.assertEqual('403 Forbidden', self.browser.headers['status'])
        roles = self.portal.acl_users.getUserById(self.normal_user).getRoles()
        self.assertEqual(['Member', 'Authenticated'], roles)

    def testNonManagersCanEditOtherRolesOfUsersWithManagerRole(self):
        roles = self.portal.acl_users.getUserById('root').getRoles()
        self.assertEqual(['Manager', 'Authenticated'], roles)
        form = {
            '_authenticator': self.siteadmin_token,
            'users.id:records': 'root',
            'users.roles:list:records': ('Member', 'Manager'),
            'form.button.Modify': 'Apply Changes',
            'form.submitted': 1,
            }
        post_data = urlencode(form, doseq=True)
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.post(self.portal.absolute_url()+'/@@usergroup-userprefs',
                          post_data)
        self.assertEqual('200 Ok', self.browser.headers['status'])
        roles = self.portal.acl_users.getUserById('root').getRoles()
        self.assertEqual(['Member', 'Manager', 'Authenticated'], roles)

    def testGroupManagerRoleCheckboxIsDisabledForNonManagers(self):
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(self.portal.absolute_url()+'/@@usergroup-groupprefs')
        contents = self.simplify_white_space(self.browser.contents)
        self.assertTrue('<input type="checkbox" class="noborder" '
                        'name="group_Reviewers:list" value="Manager" '
                        'disabled="disabled" />' in contents)

    def testManagerCanDelegateManagerRoleForGroups(self):
        # a user with the Manager role can grant the Manager role
        form = {
            '_authenticator': self.manager_token,
            'group_Reviewers:list': ('', 'Manager'),
            'form.button.Modify': 'Apply Changes',
            'form.submitted': 1,
            }
        post_data = urlencode(form, doseq=True)
        self.browser.addHeader('Authorization', 'Basic root:secret')
        self.browser.post(self.portal.absolute_url()+'/@@usergroup-userprefs',
                          post_data)
        self.assertEqual('200 Ok', self.browser.headers['status'])
        roles = self.portal.acl_users.getGroupById('Reviewers').getRoles()
        self.assertEqual(['Manager', 'Authenticated'], roles)

    def testNonManagersCannotDelegateManagerRoleForGroups(self):
        # a user without the Manager role cannot delegate the Manager role
        form = {
            '_authenticator': self.siteadmin_token,
            'group_Reviewers:list': ('', 'Manager'),
            'form.button.Modify': 'Apply Changes',
            'form.submitted': 1,
            }
        post_data = urlencode(form, doseq=True)
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.post(self.portal.absolute_url()+'/@@usergroup-groupprefs',
                          post_data)
        self.assertEqual('403 Forbidden', self.browser.headers['status'])
        roles = self.portal.acl_users.getGroupById('Reviewers').getRoles()
        self.assertEqual(['Reviewer', 'Authenticated'], roles)

    def testNonManagersCanEditOtherRolesOfGroupsWithManagerRole(self):
        roles = self.portal.acl_users.getUserById('root').getRoles()
        self.assertEqual(['Manager', 'Authenticated'], roles)
        form = {
            '_authenticator': self.siteadmin_token,
            'group_Administrators:list': ('', 'Member', 'Manager'),
            'form.button.Modify': 'Apply Changes',
            'form.submitted': 1,
            }
        post_data = urlencode(form, doseq=True)
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.post(self.portal.absolute_url()+'/@@usergroup-groupprefs',
                          post_data)
        self.assertEqual('200 Ok', self.browser.headers['status'])
        roles = self.portal.acl_users.getGroupById('Administrators').getRoles()
        self.assertEqual(['Member', 'Manager', 'Authenticated'], roles)

    def test_usergroup_usermembership_blocks_escalation(self):
        # groups granting the Manager role shouldn't show as a valid option to add
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(self.portal.absolute_url()+
                          '/@@usergroup-usermembership?userid=%s'
                          % self.normal_user)
        contents = self.simplify_white_space(self.browser.contents)
        self.assertTrue('<input type="checkbox" class="noborder" name="add:list" '
                        'value="Administrators" disabled="disabled" />' in contents)

        # and should not be addable
        form = {
            '_authenticator': self.siteadmin_token,
            'add:list': 'Administrators',
            'form.submitted': 1,
            }
        post_data = urlencode(form)
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.post(
            self.portal.absolute_url()+'/@@usergroup-usermembership?userid=%s'
            % self.normal_user, post_data)
        self.assertEqual('403 Forbidden', self.browser.headers['status'])
        roles = self.portal.acl_users.getUserById(self.normal_user).getRoles()
        self.assertEqual(['Member', 'Authenticated'], roles)

    def test_usergroup_groupmembership_blocks_escalation(self):
        # should not show section to add users for groups granting the Manager role
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(
            self.portal.absolute_url()+
            '/@@usergroup-groupmembership?groupname=Administrators')
        contents = self.simplify_white_space(self.browser.contents)
        self.assertFalse('Search for new group members' in contents)

        # and should not be addable if we try to force it
        form = {
            '_authenticator': self.siteadmin_token,
            'add:list': self.normal_user,
            'form.submitted': 1,
            }
        post_data = urlencode(form)
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.post(self.portal.absolute_url()+'/@@usergroup-groupmembership?groupname=Administrators',
                          post_data)
        self.assertEqual('403 Forbidden', self.browser.headers['status'])
        roles = self.portal.acl_users.getUserById(self.normal_user).getRoles()
        self.assertEqual(['Member', 'Authenticated'], roles)

    def test_user_registration_form_blocks_escalation(self):
        # groups granting the Manager role should not be available for selection
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(self.portal.absolute_url()+'/@@new-user')
        contents = self.simplify_white_space(self.browser.contents)
        self.assertFalse('<input class="label checkboxType" id="form.groups.0" '
                        'name="form.groups" type="checkbox" value="Administrators '
                        '(Administrators)" />' in contents)

        # and should not be addable if we try to force it
        form = {
            '_authenticator': self.siteadmin_token,
            'form.widgets.username': 'newuser',
            'form.widgets.email': 'newuser@example.com',
            'form.widgets.password': 'secret',
            'form.widgets.password_ctl': 'secret',
            'form.widgets.groups:list': 'Administrators',
            'form.widgets.groups-empty-marker': '1',
            'form.buttons.register': 'Register',
            }
        post_data = StringIO(urlencode(form))
        res = self.publish('/plone/@@new-user',
                           request_method='POST', stdin=post_data,
                           basic='siteadmin:secret')
        self.assertNotEqual(200, res.status)
        self.assertEqual(None, self.portal.acl_users.getUserById('newuser'))

    def test_users_overview_blocks_deleting_managers(self):
        # a user without the Manager role cannot delete a user with the
        # Manager role
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(self.portal.absolute_url()+'/@@usergroup-userprefs')
        contents = self.simplify_white_space(self.browser.contents)
        self.assertTrue('<input type="checkbox" class="noborder notify" '
                        'name="delete:list" value="root" disabled="disabled" />'
                        in contents)

        form = {
            '_authenticator': self.siteadmin_token,
            'users.id:records': 'root',
            'delete:list': 'root',
            'form.button.Modify': 'Apply Changes',
            'form.submitted': 1,
            }
        post_data = urlencode(form)
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.post(self.portal.absolute_url()+'/@@usergroup-userprefs',
                          post_data)
        self.assertEqual('403 Forbidden', self.browser.headers['status'])
        user = self.portal.acl_users.getUserById('root')
        self.assertTrue(user is not None)

    def test_groups_overview_blocks_deleting_managers(self):
        # a user without the Manager role cannot delete a group with the
        # Manager role
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.open(self.portal.absolute_url()+'/@@usergroup-groupprefs')
        contents = self.simplify_white_space(self.browser.contents)
        self.assertTrue('<input type="checkbox" class="noborder notify" '
                        'name="delete:list" value="Administrators" disabled="disabled" />'
                        in contents)

        form = {
            '_authenticator': self.siteadmin_token,
            'delete:list': 'Administrators',
            'form.button.Modify': 'Apply Changes',
            'form.submitted': 1,
            }
        post_data = urlencode(form)
        self.browser.addHeader('Authorization', 'Basic siteadmin:secret')
        self.browser.post(self.portal.absolute_url()+'/@@usergroup-groupprefs',
                          post_data)
        self.assertEqual('403 Forbidden', self.browser.headers['status'])
        group = self.portal.acl_users.getGroupById('Administrators')
        self.assertTrue(group is not None)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestSiteAdministratorRoleFunctional))
    return suite
