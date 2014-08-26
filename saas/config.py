# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Yannick Buron
#    Copyright 2013 Yannick Buron
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


from openerp import netsvc
from openerp import pooler
from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

import time
from datetime import datetime, timedelta
import subprocess
import execute
import ast

import logging
_logger = logging.getLogger(__name__)

class saas_config_backup_method(osv.osv):
    _name = 'saas.config.backup.method'
    _description = 'Backup Method'

    _columns = {
        'name': fields.char('Name', size=64, required=True)
    }


class saas_config_settings(osv.osv):
    _name = 'saas.config.settings'
    _description = 'SaaS configuration'

    _columns = {
        'conductor_path': fields.char('Conductor Path', size=128),
        'email_sysadmin': fields.char('Email SysAdmin', size=128),
        'log_path': fields.char('SaaS Log Path', size=128),
        'archive_path': fields.char('Archive path', size=128),
        'services_hostpath': fields.char('Host services path', size=128),
        'backup_directory': fields.char('Backup directory', size=128),
        'piwik_server': fields.char('Piwik server', size=128),
        'piwik_password': fields.char('Piwik Password', size=128),
        'dns_id': fields.many2one('saas.container', 'DNS Server'),
        'shinken_id': fields.many2one('saas.container', 'Shinken Server'),
        'backup_id': fields.many2one('saas.container', 'Backup Server'),
        'backup_ids': fields.many2many('saas.config.backup.method', 'saas_config_backup_method_rel', 'config_id', 'method_id', 'Backup methods'),
        'restore_method': fields.many2one('saas.config.backup.method', 'Restore method'),
        'home_directory': fields.char('Home directory', size=128),
        'ftpuser': fields.char('FTP User', size=64),
        'ftppass': fields.char('FTP Pass', size=64),
        'ftpserver': fields.char('FTP Server', size=64),
        'mailchimp_username': fields.char('MailChimp Username', size=64),
        'mailchimp_apikey': fields.char('MailChimp API Key', size=64),
    }

    def get_vals(self, cr, uid, context={}):
        context['from_config'] = True
        config = self.pool.get('ir.model.data').get_object(cr, uid, 'saas', 'saas_settings')

        vals = {}

        if config.dns_id:
            dns_vals = self.pool.get('saas.container').get_vals(cr, uid, config.dns_id.id, context=context)
            vals.update({
                'dns_id': dns_vals['container_id'],
                'dns_fullname': dns_vals['container_fullname'],
                'dns_ssh_port': dns_vals['container_ssh_port'],
                'dns_server_id': dns_vals['server_id'],
                'dns_server_domain': dns_vals['server_domain'],
                'dns_server_ip': dns_vals['server_ip'],
            })

        if config.shinken_id:
            shinken_vals = self.pool.get('saas.container').get_vals(cr, uid, config.shinken_id.id, context=context)
            vals.update({
                'shinken_id': shinken_vals['container_id'],
                'shinken_fullname': shinken_vals['container_fullname'],
                'shinken_ssh_port': shinken_vals['container_ssh_port'],
                'shinken_server_id': shinken_vals['server_id'],
                'shinken_server_domain': shinken_vals['server_domain'],
                'shinken_server_ip': shinken_vals['server_ip'],
            })

        if config.backup_id:
            backup_vals = self.pool.get('saas.container').get_vals(cr, uid, config.backup_id.id, context=context)
            vals.update({
                'backup_id': backup_vals['container_id'],
                'backup_fullname': backup_vals['container_fullname'],
                'backup_ssh_port': backup_vals['container_ssh_port'],
                'backup_server_id': backup_vals['server_id'],
                'backup_server_domain': backup_vals['server_domain'],
                'backup_server_ip': backup_vals['server_ip'],
            })
        del context['from_config']

        backups = []
        for backup in config.backup_ids:
            backups.append(backup.name)

        now = datetime.now()
        vals.update({
            'config_conductor_path': config.conductor_path,
            'config_email_sysadmin': config.email_sysadmin,
            'config_log_path': config.log_path,
            'config_archive_path': config.archive_path,
            'config_services_hostpath': config.services_hostpath,
            'config_backup_directory': config.backup_directory,
            'config_piwik_server': config.piwik_server,
            'config_piwik_password': config.piwik_password,
            'config_home_directory': config.home_directory,
            'config_ftpuser': config.ftpuser,
            'config_ftppass': config.ftppass,
            'config_ftpserver': config.ftpserver,
            'config_mailchimp_username': config.mailchimp_username,
            'config_mailchimp_apikey': config.mailchimp_apikey,
            'now_date': now.strftime("%Y-%m-%d"),
            'now_hour': now.strftime("%H-%M"),
            'now_hour_regular': now.strftime("%H:%M:%S"),
            'now_bup': now.strftime("%Y-%m-%d-%H%M%S"),
            'config_backups': backups,
            'config_restore_method': config.restore_method.name
        })
        return vals


    def reset_keys(self, cr, uid, ids, context={}):
        container_obj = self.pool.get('saas.container')
        container_ids = container_obj.search(cr, uid, [], context=context)
        container_obj.reset_key(cr, uid, container_ids, context=context)


    def save_all(self, cr, uid, ids, context={}):
        container_obj = self.pool.get('saas.container')
        base_obj = self.pool.get('saas.base')
        context.update({'saas-self': self, 'saas-cr': cr, 'saas-uid': uid})

        vals = self.get_vals(cr, uid, context=context)


        context['save_comment'] = 'Save before upload_save'
        container_ids = container_obj.search(cr, uid, [], context=context)
        container_obj.save(cr, uid, container_ids, context=context)
        base_ids = base_obj.search(cr, uid, [], context=context)
        base_obj.save(cr, uid, base_ids, context=context)

    def save_fsck(self, cr, uid, ids, context={}):
        context.update({'saas-self': self, 'saas-cr': cr, 'saas-uid': uid})
        vals = self.get_vals(cr, uid, context=context)
        ssh, sftp = execute.connect(vals['backup_fullname'], username='backup', context=context)
        execute.execute(ssh, ['export BUP_DIR=/opt/backup/bup;', 'bup', 'fsck', '-r'], context)
        execute.execute(ssh, ['export BUP_DIR=/opt/backup/bup;', 'bup', 'fsck', '-g'], context)
        ssh.close()
        sftp.close()

    def save_upload(self, cr, uid, ids, context={}):
        context.update({'saas-self': self, 'saas-cr': cr, 'saas-uid': uid})
        vals = self.get_vals(cr, uid, context=context)
        ssh, sftp = execute.connect(vals['backup_fullname'], context=context)
        execute.execute(ssh, ['tar', 'czf', '/opt/backup.tar.gz', '-C', '/opt/backup', '.'], context)
        stdin =[
            'rm -rf /*\n',
            'put /opt/backup.tar.gz\n',
            'exit\n'
        ]
        execute.execute(ssh, ['ncftp', '-u', vals['config_ftpuser'], '-p' + vals['config_ftppass'], vals['config_ftpserver']], context, stdin_arg=stdin)
        execute.execute(ssh, ['rm', '/opt/backup.tar.gz'], context)
        ssh.close()
        sftp.close()


    def purge_expired_saves(self, cr, uid, ids, context={}):
        repo_obj = self.pool.get('saas.save.repository')
        save_obj = self.pool.get('saas.save.save')
        vals = self.get_vals(cr, uid, context=context)
        expired_saverepo_ids = repo_obj.search(cr, uid, [('date_expiration','!=',False),('date_expiration','<',vals['now_date'])], context=context)
        repo_obj.unlink(cr, uid, expired_saverepo_ids, context=context)
        expired_save_ids = save_obj.search(cr, uid, [('date_expiration','!=',False),('date_expiration','<',vals['now_date'])], context=context)
        save_obj.unlink(cr, uid, expired_save_ids, context=context)

    def purge_expired_logs(self, cr, uid, ids, context={}):
        log_obj = self.pool.get('saas.log')
        vals = self.get_vals(cr, uid, context=context)
        expired_log_ids = log_obj.search(cr, uid, [('expiration_date','!=',False),('expiration_date','<',vals['now_date'])], context=context)
        log_obj.unlink(cr, uid, expired_log_ids, context=context)

    def launch_next_saves(self, cr, uid, ids, context={}):
        context['save_comment'] = 'Auto save'
        container_obj = self.pool.get('saas.container')
        vals = self.get_vals(cr, uid, context=context)
        container_ids = container_obj.search(cr, uid, [('date_next_save','!=',False),('date_next_save','<',vals['now_date'] + ' ' + vals['now_hour_regular'])], context=context)
        container_obj.save(cr, uid, container_ids, context=context)
        base_obj = self.pool.get('saas.base')
        vals = self.get_vals(cr, uid, context=context)
        base_ids = base_obj.search(cr, uid, [('date_next_save','!=',False),('date_next_save','<',vals['now_date'] + ' ' + vals['now_hour_regular'])], context=context)
        base_obj.save(cr, uid, base_ids, context=context)


    def reset_bases(self, cr, uid, ids, context={}):
        base_obj = self.pool.get('saas.base')
        base_ids = base_obj.search(cr, uid, [('reset_each_day','=',True)], context=context)
        base_obj.reinstall(cr, uid, base_ids, context=context)

    def cron_daily(self, cr, uid, ids, context={}):
        self.reset_keys(cr, uid, [], context=context)
        self.save_fsck(cr, uid, [], context=context)
        self.save_all(cr, uid, [], context=context)
        self.save_upload(cr, uid, [], context=context)
        self.purge_expired_saves(cr, uid, [], context=context)
        self.purge_expired_logs(cr, uid, [], context=context)
        self.launch_next_saves(cr, uid, [], context=context)
        self.reset_bases(cr, uid, [], context=context)
        return True
