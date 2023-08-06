import os
import sys, shlex
from track.logger import UnifiedLogger
from track.sync import SyncHook
import subprocess
import uuid
import shutil
from datetime import datetime
from .autodetect import (
    git_repo, dfl_local_dir, git_hash, invocation, git_pretty)
from .constants import METADATA_FOLDER, RESULT_SUFFIX
from . import log


def time_str():
    return datetime.now().strftime("%Y%m%d%H%M%S")


def flatten_dict(dt):
    dt = dt.copy()
    while any(type(v) is dict for v in dt.values()):
        remove = []
        add = {}
        for key, value in dt.items():
            if type(value) is dict:
                for subkey, v in value.items():
                    add[":".join([key, subkey])] = v
                remove.append(key)
        dt.update(add)
        for k in remove:
            del dt[k]
    return dt

class Trial(object):
    """
    Trial attempts to infer the local log_dir and remote upload_dir
    automatically.

    In order of precedence, log_dir is determined by:
    (1) the path passed into the argument of the Trial constructor
    (2) autodetect.dfl_local_dir()

    The upload directory may be None (in which case no upload is performed),
    or an S3 directory or a GCS directory.

    init_logging will automatically set up a logger at the debug level,
    along with handlers to print logs to stdout and to a persistent store.
    """
    def __init__(self,
                 log_dir=None,
                 upload_dir=None,
                 sync_period=None,
                 trial_prefix="",
                 param_map=None,
                 init_logging=True):
        if log_dir is None:
            log_dir = dfl_local_dir()
             # TODO should probably check if this exists and whether
             # we'll be clobbering anything in either the artifact dir
             # or the metadata dir, idk what the probability is that a
             # uuid truncation will get duplicated. Then also maybe
             # the same thing for the remote dir.

        base_dir = os.path.expanduser(log_dir)
        self.base_dir = base_dir
        self.data_dir = os.path.join(base_dir, METADATA_FOLDER)
        self.trial_id = str(uuid.uuid1().hex[:10])
        if trial_prefix:
            self.trial_id = "_".join([trial_prefix, self.trial_id])

        self._sync_period = sync_period
        self.artifact_dir = os.path.join(base_dir, self.trial_id)
        os.makedirs(self.artifact_dir, exist_ok=True)
        self.upload_dir = upload_dir
        self.param_map = param_map or {}

        # misc metadata to save as well
        self.param_map["trial_id"] = self.trial_id
        git_repo_or_none = git_repo()
        self.param_map["git_repo"] = git_repo_or_none or "unknown"
        self.param_map["git_hash"] = git_hash()
        self.param_map["git_pretty"] = git_pretty()
        self.param_map["start_time"] = datetime.now().isoformat()
        self.param_map["invocation"] = invocation()
        self.param_map["max_iteration"] = -1
        self.param_map["trial_completed"] = False

        if init_logging:
            log.init(self.logging_handler())
            log.debug("(re)initilized logging")



    def logging_handler(self):
        """
        For advanced logging setups, returns a file-based log handler
        pointing to a log.txt artifact.

        If you use init_logging = True there is no need to call this
        method.
        """
        return log.TrackLogHandler(
            os.path.join(self.artifact_dir, 'log.txt'))

    def start(self):
        for path in [self.base_dir, self.data_dir, self.artifact_dir]:
            if not os.path.exists(path):
                os.makedirs(path)

        self._logger = UnifiedLogger(
            self.param_map,
            self.data_dir,
            filename_prefix=self.trial_id + "_")
        self._hooks = []
        self._hooks.append(self._logger)

        if self.upload_dir:
            # note weird interaction here if user edits an artifact,
            # that would eventually get synced.
            self._hooks.append(SyncHook(
                self.base_dir,
                remote_dir=self.upload_dir,
                sync_period=self._sync_period))

    def metric(self, *, iteration=None, **kwargs):
        new_args = flatten_dict(kwargs)
        new_args.update({"iteration": iteration})
        new_args.update({"trial_id": self.trial_id})
        if iteration is not None:
            self.param_map["max_iteration"] = max(
                self.param_map["max_iteration"], iteration)
        for hook in self._hooks:
            hook.on_result(new_args)

    def trial_dir(self):
        """returns the local file path to the trial's artifact directory"""
        return self.artifact_dir

    def close(self):
        self.param_map["trial_completed"] = True
        self.param_map["end_time"] = datetime.now().isoformat()
        self._logger.update_config(self.param_map)

        for hook in self._hooks:
            hook.close()

    def get_result_filename(self):
        return os.path.join(self.data_dir, self.trial_id + "_" + RESULT_SUFFIX)
