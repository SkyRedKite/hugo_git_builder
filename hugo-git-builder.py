#!/usr/bin/python3
# hugo git builder
# version 0.1
#
# Description: Intented as a server script that runs either from a cron job
#              or a git hook to checkout and build hugo websites maintained
#              in git repos.
#
# Usage: hugo-git-builder.py sites.json site
#        sites.json = json file with config details for every website
#        site = site to process (optional)

import os
import sys
import json
from datetime import datetime

#tmp_dir = '/var/tmp/hgb-tmp1234'
tmp_dir = '/home/srk/tmp/hgb-tmp1234'
# hugo_pgm = '/home/linuxbrew/.linuxbrew/bin/hugo'
hugo_pgm = '/snap/bin/hugo'

def main():
    print('** hugo git builder - ', datetime.now())
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1]) as config_src_file:
                sites_config = json.load(config_src_file)
        except FileNotFoundError:
            print('ERROR: Site config file not found')
            return
    else:
        print('ERROR: No parameters privded.')
        return
    if len(sys.argv) > 2:
        cur_site = sys.argv[2]
        for site_key in list (sites_config):
            if site_key == cur_site:
                deploy_site(site_key, sites_config[site_key])
                return
        print('ERROR: Site not found in config file.')
        return
    for site_key in list(sites_config):
        deploy_site(site_key, sites_config[site_key])

def deploy_site(website, site_conf):
    print('Deploying website ' + website)
    os.system('mkdir ' + tmp_dir)
    os.system('git -C ' + site_conf['git_repo'] +
              ' archive ' + site_conf['git_branch'] +
              ' | (cd ' + tmp_dir + ' && tar xf -)')
    #os.system('git -C ' + site_conf['git_repo'] + ' archive ' + site_conf['git_branch'] + ' --prefix=' + tmp_dir)
    #os.system('cd ' + tmp_dir +
    #          ' && cd ' + site_conf['git_site_dir'] +
    #          ' && ' + hugo_pgm + ' --cleanDestinationDir -d ' + site_conf['website_dir'])
    os.system('cd ' + tmp_dir + ' && cd ' + site_conf['git_site_dir'] + ' && ' + hugo_pgm )
    os.system('rsync -a --delete ' + tmp_dir + '/' + site_conf['git_site_dir'] + '/public/ ' + site_conf['website_dir'])
    os.system('rm -rf ' + tmp_dir)

if __name__ == '__main__':
                  main()
