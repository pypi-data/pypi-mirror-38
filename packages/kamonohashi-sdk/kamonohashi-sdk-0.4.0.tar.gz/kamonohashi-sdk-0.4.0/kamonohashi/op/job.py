# -*- coding: utf-8 -*-
# Copyright 2018 NS Solutions Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from kamonohashi.op import object_storage
from kamonohashi.op import rest


def get(api_client, id):
    api = rest.JobApi(api_client)
    result = api.get_job(id)
    return result


def create(api_client, name, registry_image, registry_tag, data_set_id, entry_point, git_owner, git_repository, cpu, memory, gpu,
           git_branch=None, git_commit=None, partition=None, memo=None, parent_id=None, options=()):
    api = rest.JobApi(api_client)
    container_image = rest.ComponentsContainerImageInputModel(image=registry_image, tag=registry_tag)
    git_model = rest.ComponentsGitCommitInputModel(branch=git_branch, commit_id=git_commit, owner=git_owner, repository=git_repository)
    option_dict = None
    if options is not None:
        option_dict = {}
        for option in options:
            option_dict[option[0]] = option[1]
    model = rest.JobApiModelsCreateInputModel(container_image=container_image, cpu=cpu, data_set_id=data_set_id, entry_point=entry_point,
                                              git_model=git_model, gpu=gpu, memo=memo, memory=memory, name=name, options=option_dict,
                                              parent_id=parent_id, partition=partition)
    result = api.create_job(model=model)
    return result


def update(api_client, id, memo):
    api = rest.JobApi(api_client)
    model = rest.JobApiModelsEditInputModel(memo=memo)
    result = api.update_job(id, model=model)
    return result


def upload_file(api_client, id, file_path):
    api = rest.JobApi(api_client)
    attached_info = object_storage.upload_file(api_client, file_path, 'TrainingHistoryAttachedFiles')
    model = rest.ComponentsAddFileInputModel(file_name=attached_info.file_name, stored_path=attached_info.stored_path)
    result = api.add_job_file(id, model=model)
    return result


def download_files(api_client, id, dir_path):
    api = rest.JobApi(api_client)
    result = api.list_job_files(id, with_url=True)
    pool_manager = api_client.rest_client.pool_manager
    for x in result:
        object_storage.download_file(pool_manager, x.url, dir_path, x.file_name)
