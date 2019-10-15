"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

from mlgit.config import mlgit_config_save
from mlgit.utils import yaml_load, yaml_save, RootPathException
from mlgit import log
from mlgit.constants import ROOT_FILE_NAME, CONFIG_FILE, ADMIN_CLASS_NAME
import os
from mlgit.utils import get_root_path


# define initial ml-git project structure
# ml-git-root/
# ├── .ml-git/config.yaml
# | 				# describe git repository (dataset, labels, nn-params, models)
# | 				# describe settings for actual S3/IPFS storage of dataset(s), model(s)



def init_mlgit():
	try:
		root_path = get_root_path()
		log.info("You already are in a ml-git repository (%s)" % (os.path.join(root_path, ROOT_FILE_NAME)),
				 class_name=ADMIN_CLASS_NAME)
		return
	except:
		pass
	
	try:
		os.mkdir(".ml-git")
	except PermissionError:
		log.error('Permission denied. You need write permission to initialize ml-git in this directory.', class_name=ADMIN_CLASS_NAME)
		return
	mlgit_config_save()
	root_path = get_root_path()
	log.info("Initialized empty ml-git repository in %s" % (os.path.join(root_path, ROOT_FILE_NAME)), class_name=ADMIN_CLASS_NAME)


def remote_add(repotype, ml_git_remote):
	try:
		root_path = get_root_path()
		file = os.path.join(root_path, CONFIG_FILE)
		conf = yaml_load(file)
	except Exception as e:
		raise e

	if repotype in conf:
		if conf[repotype]["git"] is None or not len(conf[repotype]["git"]) > 0:
			log.info("Add remote repository [%s] for [%s]" % (ml_git_remote, repotype), class_name=ADMIN_CLASS_NAME)
		else:
			log.info("Changing remote from [%s]  to [%s] for  [%s]" % (conf[repotype]["git"], ml_git_remote, repotype), class_name=ADMIN_CLASS_NAME)
	else:
		log.info("Add remote repository [%s] for [%s]" % (ml_git_remote, repotype), class_name=ADMIN_CLASS_NAME)
	try:
		conf[repotype]["git"] = ml_git_remote
	except:
		conf[repotype] = {}
		conf[repotype]["git"] = ml_git_remote
	yaml_save(conf, file)


def store_add(store_type, bucket, credentials_profile, region):
	if store_type not in ["s3", "s3h"]:
		log.error("Unknown data store type [%s]" % store_type, class_name=ADMIN_CLASS_NAME)
		return

	log.info(
		"Add store [%s://%s] in region [%s] with creds from profile [%s]" %
		(store_type, bucket, region, credentials_profile), class_name=ADMIN_CLASS_NAME
	)
	try:
		root_path = get_root_path()
		file = os.path.join(root_path, CONFIG_FILE)
		conf = yaml_load(file)
	except Exception as e:
		raise e

	if "store" not in conf:
		conf["store"] = {}
	if store_type not in conf["store"]:
		conf["store"][store_type] = {}
	conf["store"][store_type][bucket] = {}
	conf["store"][store_type][bucket]["aws-credentials"] = {}
	conf["store"][store_type][bucket]["aws-credentials"]["profile"] = credentials_profile
	conf["store"][store_type][bucket]["region"] = region
	yaml_save(conf, file)
