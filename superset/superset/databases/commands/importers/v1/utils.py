# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import json
from typing import Any, Dict

from sqlalchemy.orm import Session

from superset.databases.ssh_tunnel.models import SSHTunnel
from superset.models.core import Database


def import_database(
    session: Session, config: Dict[str, Any], overwrite: bool = False
) -> Database:
    existing = session.query(Database).filter_by(uuid=config["uuid"]).first()
    if existing:
        if not overwrite:
            return existing
        config["id"] = existing.id

    # https://github.com/apache/superset/pull/16756 renamed ``csv`` to ``file``.
    config["allow_file_upload"] = config.pop("allow_csv_upload")
    if "schemas_allowed_for_csv_upload" in config["extra"]:
        config["extra"]["schemas_allowed_for_file_upload"] = config["extra"].pop(
            "schemas_allowed_for_csv_upload"
        )

    # TODO (betodealmeida): move this logic to import_from_dict
    config["extra"] = json.dumps(config["extra"])

    # Before it gets removed in import_from_dict
    ssh_tunnel = config.pop("ssh_tunnel", None)

    database = Database.import_from_dict(session, config, recursive=False)
    if database.id is None:
        session.flush()

    if ssh_tunnel:
        ssh_tunnel["database_id"] = database.id
        SSHTunnel.import_from_dict(session, ssh_tunnel, recursive=False)

    return database
