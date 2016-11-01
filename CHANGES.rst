Changelog
=========

2.3.11 (2016-11-01)
-------------------

New features:

- Added options to change default search order.
  [rodfersou]


2.3.10 (2016-09-07)
-------------------

Bug fixes:

- Fix tests for syndication control panel to pass also with
  new plone.app.registry versions
  [Asko Soukka]


2.3.9 (2015-09-27)
------------------

- Added ``text-decoration`` to allowed css style attributes in
  ``@@filter-controlpanel``.  Change backported from master.
  [jnachtigall, vangheem, maurits]


2.3.8 (2013-12-07)
------------------

- Fix test email: msgid was sent, not translation.
  [thomasdesvenain]

- Fix syndication settings to not write on read.
  [vangheem]


2.3.7 (2013-08-13)
------------------

- In the users listing and group membership listing, show the user's
  login name instead of the user id, which is an internal identifier.
  [davisagli]

- In the groups listing, don't show the group name if it is the same
  as the group title.
  [davisagli]

- Don't display the upgrade portal message unless the logged in user
  actually has the permission to upgrade the portal. No one likes a
  tease.
  [eleddy]


2.3.6 (2013-05-30)
------------------

- Fix get_display_pub_date_in_byline when upgrading your site, refs
  https://dev.plone.org/ticket/13604
  [maartenkling]


2.3.5 (2013-05-23)
------------------

- Do not assume roles managed through the control panel include Manager.
  [danjacka]


2.3.4 (2013-01-13)
------------------

- Call searchUsers with the 'name' argument instead of 'login'.
  'name' is the officially supported way according to the PAS interface.
  [maurits]


2.3.3 (2013-01-01)
------------------

- Fix description of 'email as login' security setting.  It said
  existing users could go to the personalize information page and save
  it to start using their email as login, but that no longer works and
  is too hard to fix.  We now only recommend using the
  migrate-to-emaillogin page as manager.
  Fixes http://dev.plone.org/ticket/11283
  [maurits]

- Only show the inline editing setting if plone.app.kss is present.
  [davisagli]

- Fix as site administrator modify users in controlpanel
  when a user in the list is in administrator group, refs #12307
  [maartenkling]

- When browsing users and groups, clear searchstring when adding
  or removing.  Also do not show search results then.
  [maurits]

- When browsing users and groups, clear searchstring when selecting
  show all.
  [maartenkling]

- Add error class to portalMessage when portalMessage contains error
  [maartenkling]

- Fix 'Redirect immediately to link target' setting doesn't stick #12892
  [maartenkling]

- Change title and description for permitted styles so its correct
  [maartenkling]

- Fix @@usergroup-groupmembership "Show All users" batching broken
  [maartenkling]


2.3.2 (2012-10-16)
------------------

- Fixed issue with email_from_name set as string instead of unicode
  This fixes http://dev.plone.org/ticket/12385
  [ericof]

- Fixed issue with non-ascii Workflow titles breaking types
  control panel.
  [ericof]


2.3.1 (2012-08-29)
------------------

- Fixed i18n regression in control-panel.pt
  [vincentfretin]


2.3 (2012-07-02)
----------------

- Added 'display publication date in author byline' option to Site
  Settings control panel.
  [vipod]


2.2.6 (2012-06-29)
------------------

- Nothing changed yet.

- Users/groups controlpanel: When sending a password mail fails, an error
  message will now be issued. Fixes http://dev.plone.org/ticket/6047
  (together with a commit for Products.CMFPlone).
  [kleist]


2.2.5 (2012-05-25)
------------------

- Move form help inside field labels to improve accessibility.
  [smcmahon]

- Updated zope.formlib imports.
  [hannosch]

- Avoid hard dependency on Archetypes.
  [davisagli]

- Add missing condition in usergroups template.
  [pjstevns]

- Add .gitignore.
  [pjstevns]

- Fix component lookup error during startup.
  [pjstevns]


2.2.4 (2012-04-15)
------------------

- Don't display an empty list element if the control panel item isn't visible.
  [esteele]

- Restore the ILockSettings support using the
  EditingControlPanelAdapter.  This may affect plone.app.form (IOW,
  formlib) forms whose subscribers call
  plone.locking.TTWLockable.lock().
  [rossp]


2.2.3 (2012-01-26)
------------------

- Fix tests after recent plone.app.layout change to create a
  useractions view.
  [maurits]

- Really make the dependency of the markup control panel on wicked optional.
  [vincentfretin]

- Don't use plone_utils's getUserFriendlyTypes for blacklisting calculation in
  navigation-controlpanel, so it isn't dependend on search-controlpanel
  settings anymore. Fixes: #9012.
  [thet]

- Pyflakes cleanup.
  [thet]


2.2.2 (2011-10-17)
------------------

- Forward-port http://dev.plone.org/plone/changeset/52199, which displays both
  CMFPlone's package and profile versions on the control panel overview.
  [esteele]

- Make a condition in usergroup_groupdetails.pt Chameleon-safe.
  [stefan]


2.2.1 (2011-08-23)
------------------

- Mail-panel: If sending of test e-mail fails, log the exception
  and show it in the status message.
  [kleist]


2.2 - 2011-07-19
----------------

- Merge PLIP 11774. Refs http://dev.plone.org/plone/ticket/11774
  [esteele]

- Merge PLIP 9352. Refs http://dev.plone.org/plone/ticket/9352
  [esteele]


2.1.3 (2011-09-21)
------------------

- Display both CMFPlone's package version and profile version in the control
  panel overview.
  [esteele]


2.1.2 (2011-09-16)
------------------

- Introduced an update method in GroupMembershipControlPanel and
  UserMembershipControlPanel to seperate setting of variables and template
  rendering, so it is possible to subclass those classes to add new
  functionnalities.
  [vincentfretin]

- Fixed canAddToGroup check in usergroups_usermembership view, apparently
  a bad copy and paste from the old prefs_search_macros. It checked against
  the authenticated user instead of the member we're currently looking at.
  [vincentfretin]

- On usergroup-groupmembership view, check for each found principal that it
  can be added to the group. Previously it checked that authenticated user can
  be added to the group, that is non sense.
  [vincentfretin]

- On the Type-panel, fix the case when no workflow is set as default workflow.
  Fixes http://dev.plone.org/plone/ticket/11901
  [WouterVH]


2.1.1 - 2011-05-13
------------------

- Many users/groups setting should provide warning to users/groups config
  Fixes http://dev.plone.org/plone/ticket/11753
  [aclark]


2.1 - 2011-04-03
----------------

- Make the dependency of the markup control panel on wicked optional.
  [davisagli]

- Remove hidden `form.submitted` field in the form wrapping the "Add New User"
  button on the groups overview page. The presence of that field forces a
  CSRF check in the add groups form, which fails. Fixes #11553.
  [smcmahon]


2.1b1 - 2011-01-03
------------------

- Depend on ``Products.CMFPlone`` instead of ``Plone``.
  [elro]

- Make sure the ConfigurationChangedEvent is fired when the types
  control panel setting changed.
  [timo]

- Fix critical errors on user and group pages
  when some groups or users have a non-ascii character in their title.
  Sort groups and users on their fullname or title normalized.
  Similar as http://dev.plone.org/plone/ticket/11301
  [thomasdesvenain]

- Fixed : Group titles were not display on group prefs page
  when title property was got from mutable properties plugin.
  [thomasdesvenain]

- Prevent privilege escalation when access to the Users and Groups control
  panel is given to non-Manager users.  Only users with the "Manage portal"
  permission can grant the Manager role, or assign users to groups that grant
  the Manager role. Also, non-Managers cannot edit the roles of, reset the
  password of, or delete users or groups with the Manager role.
  [davisagli]

- Declare dependency on Zope2 >= 2.13.0.
  [davisagli]

- Protect each control panel using its own specific permission, instead of the
  generic "Manage portal". This way access to particular control panels can be
  delegated.
  [davisagli]

- Update the @@overview-controlpanel view to match changes that had happened in
  plone_control_panel.pt in CMFPlone.
  [davisagli]

- Replace reference to "personalize_form" with "@@personal-information".
  http://dev.plone.org/plone/ticket/10890
  [khink]

- Add extra info message if passwords were reset.
  http://dev.plone.org/plone/ticket/10756
  [khink]


2.0.5 - 2011-01-03
------------------

- Fix critical errors on user and group pages
  when some groups or users have a non-ascii character in their title.
  Sort groups and users on their fullname or title normalized.
  Similar as http://dev.plone.org/plone/ticket/11301
  [thomasdesvenain]

- Fixed : Group titles were not display on group prefs page
  when title property was got from mutable properties plugin.
  [thomasdesvenain]

- Replace reference to "personalize_form" with "@@personal-information".
  http://dev.plone.org/plone/ticket/10756
  [khink]

- Add extra info message if passwords were reset.
  http://dev.plone.org/plone/ticket/10756
  [khink]


2.0.4 - 2010-10-27
------------------

- Disable autocomplete for the mail control panel's SMTP user id and password
  fields. Otherwise some browsers complete them with the site user id and
  password. This closes http://dev.plone.org/plone/ticket/9185.
  [davisagli]

- Different descriptions for Stripped attributes and Stripped combinations
  fields.
  [thomasdesvenain]

2.0.3 - 2010-09-09
------------------

- Increased refresh time interval to 30 seconds for the restart action of the
  maintenance control panel.
  [kleist, hannosch]


2.0.2 - 2010-08-08
------------------

- Changed some messages in @@ramcache-controlpanel view.
  [vincentfretin]


2.0.1 - 2010-07-31
------------------

- Check whether users can be added to the group. Don't show the add form on
  @@usergroup-groupmembership if not.
  [esteele]


2.0 - 2010-07-18
----------------

- Use the standard libraries doctest module.
  [hannosch]

- Adjusted tests to match new PortalTransforms and Plone defaults.
  [hannosch]

- Use correct listingheader_user_name or listingheader_group_name instead
  of listingheader_group_user_name in @@usergroups-usermembership
  and @@usergroups-groupmembership.
  Fixes http://dev.plone.org/plone/ticket/10747
  [vincentfretin]

- Removed text from @@skins-control panel, since 'Mark External Links'
  does not have to be checked for 'open in new window' to work. #10772
  [cwainwright]

- Update license to GPL version 2 only.
  [hannosch]


2.0b7 - 2010-05-31
------------------

- Fixed types.pt to render in cmf.pt.
  [pilz]

- Fixed typo that prevented a message from showing up when switching
  back from emaillogin to login in with userid.
  [maurits]

- Updated help text for users overview control panel.
  [davisagli]


2.0b6 - 2010-05-01
------------------

- Use new i18n:translate identifiers in usergroups_usermembership.pt.
  Correct capitalization of tab names.
  [esteele]

- Fix capitalization of "Group Name" in groups overview.
  [esteele]

- Remove the email column from the Users Overview page.
  [esteele]

- Replaced prefs_user_details form with personal information and personal
  preferences forms (plone.app.users). Added two tabs for these forms.
  http://dev.plone.org/plone/ticket/10327
  [kcleong]


2.0b5 - 2010-04-08
------------------

- Remove setting of display_border from all templates; this is now done in
  prefs_main_template.
  [davisagli]

- Removed msgid for "Site Setup" message in plone/app/controlpanel/overview.pt
  [vincentfretin]

- Made formlib-based forms consistent with the updated breadcrumb style in
  Plone 4.
  [limi]

- Fixed various i18n issues.
  [vincentfretin]


2.0b4 - 2010-03-05
------------------

- Reworked user and group listings to prevent excessively long batching URLs and
  resubmission of role changes via the batching links; requires changes to
  batching templates in Plone 4.0b1.
  [cah190]

- Added a link to show all search results (thus temporarily disabling batching)
  for user and group listings.
  [cah190]

- Performing a search on the users and groups overviews now resets the batching
  state such that page 1 is always shown after the search is submitted.
  [cah190]

- The users overview will now return to the same page of results after role
  changes are submitted.
  [cah190]

- Remove the option to turn off nesting.
  [esteele]

- Updated emaillogin.pt to recent markup conventions.
  References http://dev.plone.org/plone/ticket/9981
  [spliter]

- Remove unused imports in usergroups.py.
  [esteele]

- Add the recursive_groups plugin to the bottom of the IGroupsPlugin list, not
  the top.
  [esteele]


2.0b3 - 2010-02-18
------------------

- Updated usergroups* templates to the recent markup conventions.
  References http://dev.plone.org/plone/ticket/9981
  [spliter]

- Removed #region-content from all templates.
  This refs http://dev.plone.org/plone/ticket/10231
  [limi]


2.0b2 - 2010-02-17
------------------

- Updated
    - usergroups_groupmembership.pt
    - usergroups_groupsoverview.pt
    - usergroups_usermembership.pt
    - usergroups_usersoverview.pt
    - usergroupssettings.pt

  to the recent markup conventions. And got rid of redundant
  .documentContent/#region-content markup.
  References
  http://dev.plone.org/plone/ticket/9981
  http://dev.plone.org/plone/ticket/10231
  [spliter]

- Removing redundant .documentContent markup.
  This refs http://dev.plone.org/plone/ticket/10231
  [limi]

- Create a new dedicated @@editing-controlpanel instead of splitting up the
  site control panel.
  [hannosch]

- Updated control-panel.pt and maintenance.pt to recent markup conventions.
  Got rid of 'viewspace' CSS ID and slot.
  References http://dev.plone.org/plone/ticket/9981
  [spliter]

- Fixed a string which contained double quote.
  [vincentfretin]

- Split @@site-controlpanel form in two fieldsets "general" and "editing".
  [csenger]


2.0b1 - 2010-01-29
------------------

- Add an enable/disable nested groups option to the users/groups settings prefs.
  [esteele]

- @@usergroup-userprefs now requires the zope2.ManageUsers permission instead
  of cmf.ManagePortal.
  [esteele]

- @@usergroup-userprefs now shows an icon to designate that the user has
  inherited that global role through group membership.
  [esteele]

- Display users in @@usergroup-userprefs by Fullname (user id).
  [esteele]

- Add membershipSearch method to UsersGroupsControlPanelView. Will replace the
  soon-to-be-deprecated prefs_user_group_search.py from Plone's plone_prefs.
  [esteele]

- Properly handle nesting of groups. UI now allows addition and display of
  groups within other groups.
  Closes http://dev.plone.org/plone/ticket/8556
  [esteele, cah190]

- @@usergroup-groupprefs now shows an icon to designate that the group has
  inherited that global role from another group.
  [esteele, cah190]

- Factor up commonly used methods in user/groups controlpanel views.
  [esteele]

- Add @@usergroup-groupmembership to handle adding, removing, modifying group
  members.
  [esteele, cah190]

- Added explicit i18n:translate for the fieldset legends, so Chameleon
  translates the labels.
  [limi]

- Display group title in @@usergroup-groupprefs form.
  [esteele]


2.0a4 - 2009-12-27
------------------

- Specify all package dependencies and use zope.site for the getSite function.
  [hannosch]


2.0a3 - 2009-12-16
------------------

- Don't mark site.py's "default_editor" field as required as it's a select
  field.
  [esteele]


2.0a2 - 2009-12-03
------------------

- Adjusted filter controlpanel tests to new defaults in PortalTransforms.
  [hannosch]

- Move prefs_navigation_form to plone.app.controlpanel as
  @@navigation-controlpanel.
  [esteele]

- "Users", "Groups" and "Settings" configlets' views are polished visually
  to follow rest of configlets. Fixes #9825
  [spliter]

- Point the users overview 'add user' button to the new @@new-user form.
  [esteele]

- Rephrased debug-mode info.
  This closes http://dev.plone.org/plone/ticket/9788
  [naro]

- Fixed bad i18n markup in emaillogin.pt. This closes
  http://dev.plone.org/plone/ticket/9767
  [vincentfretin]


2.0a1 - 2009-11-14
------------------

- Fixed calendar and filter tests.
  [hannosch]

- Add option in themes configlet to enable/disable overlay popups.
  [smcmahon]

- Make sure the filter control panel doesn't fail if kupu is not installed.
  [davisagli]

- Added test for DC meta data properties.
  [robgietema]

- Added default editor setting to the Site settings control panel.
  [rob gietema]

- Moved remaining html filter settings from Kupu library tool to safe_html
  transform.
  [robgietema]

- Added @@migrate-to-emaillogin browser view so admins can update the login
  names of existing users. It can check for duplicate emails and can update the
  login name of all users to their email addresses or back to their user ids.
  http://dev.plone.org/plone/ticket/9214
  [maurits]

- Added use_email_as_login property to security control panel.
  http://dev.plone.org/plone/ticket/9214
  [maurits]

- Force a page refresh when saving changes to the skins control panel. This
  forces newly-chosen themes to fully take effect.
  [esteele]

- Use `zope.ramcache` in favor of `zope.app.cache`.
  [hannosch]

- Removed the dependency on plone.app.form's named_template_adapter, as it
  does not work with Zope 2.12.
  [hannosch]


1.3 - 2010-03-03
------------------

- Fixed some duplicated msgids with different defaults.
  There is no new strings to translate.
  See http://dev.plone.org/plone/ticket/9633
  [vincentfretin]

- Explicitely set the default workflow on types before re-mapping said
  workflow to their new states. See http://dev.plone.org/plone/ticket/9031
  Thanks to fmoret for the patch.
  [mj]


1.2 - 2009-05-09
----------------

- Bug fix: so called 'bad types' are not listed in the search panel, but on
  save they should still be added to the types_not_searched property in the
  site_properties.
  [maurits]


1.2b1 - 2009-03-09
------------------

- Add 'Redirect immediately to link target' option for Link type in Site
  Settings Types
  [andrewb]

- Add 'Enable locking for through-the-web edits' option in Site Settings
  [davisagli]

- Let the site settings adapter also adapt ILockSettings so it
  can be used from plone.locking
  [davisagli]


1.1.3 - 2009-03-07
------------------

- "Mark external links" and "External links open in new window" were not working
  independently ('mark' had to be set for 'new window' to work) and marking could
  not be turned off at all (#7383). Fixed by having either one enable the js
  support and adding a new site property to control marking. Implemented so
  that new site property will be assumed false if missing and created on change
  if missing -- so no migration required. There is a matching change in Plone
  app in a couple of javascripts.
  [smcmahon]

- 'Enable User Folders' in the security control panel supports
  create/delete a 'My Folder' link user action know from Plone 2.*
  http://dev.plone.org/plone/ticket/8417
  [pelle]

- Added failing browser test to catch the missing 'My Folder' link
  when member creation is enabled http://dev.plone.org/plone/ticket/8417
  [pelle]


1.1.2 - 2008-08-18
------------------

- Use the MultiCheckBoxWidget from plone.app.form that uses <label>s
  to be accessible. This closes http://dev.plone.org/plone/ticket/7211
  [csenger]

- Refactor handling of versioning policies in the types control panel:
  allow the admin to choose from three common versioning policies (no
  versioning, manual versioning and automatic versioning) which map to
  CMFEditions settings.
  [wichert]

- Added checkbox for enabling/disabling inline editing.
  [fschulze]

- Simplified the mail control panel to present all information on one tab.
  In case of validation errors the panel behaved in most unintuitive ways.
  This closes http://dev.plone.org/plone/ticket/7425,
  http://dev.plone.org/plone/ticket/7694 and
  http://dev.plone.org/plone/ticket/6916.
  [hannosch]


1.1.1 - 2008-06-02
------------------

- Declare dependencies for plone.* packages.
  [wichert]

- Reformat documentation in reST and include it in the package description.
  [wichert]

- Fix nested forms in RAMCache control panel.
  [witsch]


1.1 - 2008-04-19
----------------

- Fixed saving of esmtp username and password in SecureMailHost
  [csenger]

- Added new IPloneControlPanelView marker interface and let all views and
  forms implement it.
  [hannosch]

- Added new yet unused controlpanel overview page.
  [hannosch]

- Fix invalid leading space in all 'Up to Site Setup' links.
  [wichert]

- Added authenticator token and verification calls for CSRF protection.
  [witsch]


1.0.5 - 2008-03-26
------------------

- `Enable self registration flag` in security control panel was broken
  in some cases with custom roles. Patch provided by davidray, thx!
  This closes http://dev.plone.org/plone/ticket/7690.
  [hannosch]

- Added an IConfigurationChangedEvent which is fired on each successful
  change of any configuration setting and a subscriber which empties all
  RAM caches when some configuration changed. This closes
  http://dev.plone.org/plone/ticket/7008.
  [hannosch]


1.0.4 -  2008-02-13
-------------------

- Take advantage of NORMALIZE_WHITESPACE to be independent of the tidy_html
  transform.
  [shh42]

- Fixed vocabulary in skins control panel to support proper i18n.
  This closes http://dev.plone.org/plone/ticket/7766.
  [hannosch]

- Changed import of FormFieldsets to avoid a deprecation warning.
  [hannosch]

- Fixed filter control panel tests.
  [hannosch]


1.0.3 - 2007-11-30
------------------

- Fixed description in filter control panel to be recognizable by i18ndude.
  [hannosch]

- Protected the maintenance control panel with the View management screens
  permission at the Zope root folder. This closes
  http://dev.plone.org/plone/ticket/6973.
  [hannosch]


1.0.2 - 2007-10-07
------------------

- Fixed language control panel to only show one language option and fix
  its description. This closes http://dev.plone.org/plone/ticket/6963 and
  http://dev.plone.org/plone/ticket/6946.
  [hannosch]


1.0.1 - 2007-09-10
------------------

- Updated help text to match implementation.
  [fschulze]

- Fixed test in site.txt to work in Zope 2.11.
  [hannosch]

- If we are looking at settings for the default workflow lookup the real
  workflow. This fixes #6843 (yes, that bug again).
  [wichert]

- Another small string update while we're at it.
  [limi]


1.0 - 2007-08-14
----------------

- If we are looking at settings for the default workflow lookup the
  real workflow. This fixes http://dev.plone.org/plone/ticket/6843
  (yes, that bug again).
  [wichert]

- Fixed the translation of type names on the search and markup control
  panels. This refs http://dev.plone.org/plone/ticket/6911.
  [hannosch]

- The UI allowed to disable country-specific language variants even if
  one was still active as the default language. You get a nice error
  message now. This closes http://dev.plone.org/plone/ticket/6862.
  [hannosch]

- Use checkboxes instead of a evil MultiSelect for the wiki settings.
  This closes http://dev.plone.org/plone/ticket/6872 for real.
  [hannosch]

- Internationalized the workflow part of the types control panel. All
  descriptions, states and titles should be translated now.
  [hannosch]

- Fixed order of types in the dropdown. We sort by translated title now.
  [hannosch]

- When updating the default workflow do not reset the workflow for types
  using the default workflow to the new default workflow. This fixes
  the last part of http://dev.plone.org/plone/ticket/6843.
  [wichert]

- Handle changing the workflow from a type to the default workflow if the
  default workflow is the same as the previous workflow correctly. This
  fixes part of http://dev.plone.org/plone/ticket/6843.
  [wichert]

- When we remap the default workflow change the default workflow in
  the workflow tool as well. This fixes part of
  http://dev.plone.org/plone/ticket/6843.
  [wichert]

- Remapping the "(Default)" workflow to No Workflow didn't work.
  Fixes http://dev.plone.org/plone/ticket/6818.
  [optilude]

- Remapping to "No Workflow" resulted in an error, fixed. Thanks to
  rsantos for the patch. Fixes http://dev.plone.org/plone/ticket/6819.
  [limi]

- Made column checkbox widget easily subclassable for being able to use it
  with different amount of columns from other packages.
  [davconvent]


1.0rc3 - 2007-07-28
-------------------

- Fixed missing history entries.
  [hannosch]


1.0rc2 - 2007-07-27
-------------------

- Add a description to the no-workflow fallback. This fixes
  http://dev.plone.org/plone/ticket/6812.
  [wichert]

- Filter control panel doesn't warn you when you haven't saved your changes
  Added enableUnloadFormProtection class to the control panel form.
  This references http://dev.plone.org/plone/ticket/6654.
  [duncan]

- Removed lots of irrelevant options from the language control panel. The
  selection of the default language could use a simpler widget, but it's
  too late to change that now. All advanced options should be made
  available through control panels in add-ons which actually use these
  settings. This closes http://dev.plone.org/plone/ticket/6784.
  [hannosch]

- Fixed various bugs in the LanguageTableWidget. Removed broken code that
  tried to show the country flags. Showing 150 flags is rather excessive.
  This closes http://dev.plone.org/plone/ticket/6814.
  [hannosch]

- Removed multilingual content settings from the language control panel.
  These don't have any effect in a standard Plone site. LinguaPlone /
  plone.app.multilingual features its own control panel.
  [hannosch]


1.0rc1 - 2007-07-09
-------------------

- Do not show really user unfriendly types anymore in the search and types
  control panels. This closes http://dev.plone.org/plone/ticket/6292.
  [hannosch]

- Consistently bicapitalized 'JavaScript'. This refs
  http://dev.plone.org/plone/ticket/6636.
  [hannosch]

- Fixed another spelling error on the filter control panel. This closes
  http://dev.plone.org/plone/ticket/6653.
  [hannosch]

- Fixed two spelling errors on the filter control panel. This closes
  http://dev.plone.org/plone/ticket/6644.
  [hannosch]

- Added and used the new LanguageTableWidget for the available language
  listing.
  [hannosch]

- Use the new LanguageDropdownChoiceWidget for the default language field.
  [hannosch]

- Added first working version of the new language control panel. It still
  needs two new locale aware widgets for the language listings. This refs
  http://dev.plone.org/plone/ticket/5442.
  [hannosch]

- Added support for optional descriptions on fieldsets.
  [hannosch]

- Added RAMCache control panel. You can invoke it via
  http://portal/@@ramcache-controlpanel.
  [hannosch]

- Localized the calendar control panel weekday names based on the Zope 3
  locales information, which is available from the portal_state view.
  [hannosch]

- Removed title customization from the types control panel. This is
  currently not possible in any i18n-safe way. This closes
  http://dev.plone.org/plone/ticket/6551.
  [hannosch]


1.0b5 - 2007-05-05
------------------

- Fixed dummy on_save method to accept the data argument.
  [hannosch]


1.0b4 - 2007-05-05
------------------

- Pass data to the on-save template method.
  [optilude]

- Add a callback method from the save button handler. This makes it easier
  to react when saving is finished (successfully) - otherwise, the schema
  adapter properties are simple set one-by-one and you can't do anything
  when form saving is complete. The alternative is to override the button
  handler, but then we lose some of the consistency that plone.app.form
  tries to introduce.
  [optilude]

- Wording.
  [limi]


1.0b3 - 2007-05-01
------------------

- Adjusted the mail control panel to store the email settings on the portal
  root intead of in the site properties. This closes
  http://dev.plone.org/plone/ticket/6173.
  [hannosch]


1.0b2 - 2007-03-23
------------------

- Spelling corrections and wording.
  [limi]

- Replace getToolByNames by getUtility.
  [hannosch]


1.0b1 - 2007-03-05
------------------

- Lots more control panels.
  [hannosch, optilude, limi, siebo, aclark, jladage, andrewb]


1.0a2 - 2007-02-06
------------------

- Additional control panels.
  [tomster, whit]

- Groundwork and first control panels.
  [hannosch]
