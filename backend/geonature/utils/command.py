"""
    Fichier de création des commandes geonature
    Ce module ne doit en aucun cas faire appel à des models ou au coeur de geonature
    dans les imports d'entête de fichier pour garantir un bon fonctionnement des fonctions
    d'administration de l'application GeoNature (génération des fichiers de configuration, des
    fichiers de routing du frontend etc...). Ces dernières doivent pouvoir fonctionner même si
    un paquet PIP du requirement GeoNature n'a pas été bien installé
"""
import os
import sys
import logging
import subprocess
import json

from jinja2 import Template
from pathlib import Path

from server import get_app
from geonature.utils.env import (
    BACKEND_DIR,
    ROOT_DIR,
    GN_MODULE_FE_FILE,
    load_config,
    get_config_file_path,
    DB,
    GN_EXTERNAL_MODULE,
)
from geonature.utils.errors import ConfigError
from geonature.utils.utilstoml import load_and_validate_toml
from geonature.utils.config_schema import GnGeneralSchemaConf

log = logging.getLogger(__name__)

MSG_OK = "\033[92mok\033[0m\n"


def start_gunicorn_cmd(uri, worker):
    cmd = "gunicorn server:app -w {gun_worker} -b {gun_uri}"
    subprocess.call(
        cmd.format(gun_worker=worker, gun_uri=uri).split(" "), cwd=str(BACKEND_DIR)
    )


def get_app_for_cmd(config_file=None, with_external_mods=True, with_flask_admin=True):
    """ Return the flask app object, logging error instead of raising them"""
    try:
        conf = load_config(config_file)
        return get_app(
            conf,
            with_external_mods=with_external_mods,
            with_flask_admin=with_flask_admin,
        )
    except ConfigError as e:
        log.critical(str(e) + "\n")
        sys.exit(1)


def supervisor_cmd(action, app_name):
    cmd = "sudo supervisorctl {action} {app}"
    subprocess.call(cmd.format(action=action, app=app_name).split(" "))


def start_geonature_front():
    subprocess.call(["npm", "run", "start"], cwd=str(ROOT_DIR / "frontend"))


def build_geonature_front(rebuild_sass=False):
    if rebuild_sass:
        subprocess.call(
            ["npm", "rebuild", "node-sass", "--force"], cwd=str(ROOT_DIR / "frontend")
        )
    subprocess.call(["npm", "run", "build"], cwd=str(ROOT_DIR / "frontend"))


def frontend_routes_templating(app=None):
    if not app:
        app = get_app_for_cmd(with_external_mods=False)

    log.info("Generating frontend routing")
    # recuperation de la configuration
    configs_gn = load_config(get_config_file_path())

    from geonature.utils.env import list_frontend_enabled_modules

    with open(
        str(ROOT_DIR / "frontend/src/app/routing/app-routing.module.ts.sample"), "r"
    ) as input_file:
        template = Template(input_file.read())
        routes = []
        for url_path, module_code in list_frontend_enabled_modules(app):
            location = Path(GN_EXTERNAL_MODULE / module_code.lower())

            # test if module have frontend
            if (location / "frontend").is_dir():
                path = url_path.lstrip("/")
                location = "{}/{}#GeonatureModule".format(
                    location, GN_MODULE_FE_FILE)
                routes.append(
                    {"path": path, "location": location, "module_code": module_code}
                )

            # TODO test if two modules with the same name is okay for Angular

        route_template = template.render(
            routes=routes,
            enable_user_management=configs_gn["ACCOUNT_MANAGEMENT"].get(
                "ENABLE_USER_MANAGEMENT"
            ),
            enable_sign_up=configs_gn["ACCOUNT_MANAGEMENT"].get(
                "ENABLE_SIGN_UP"),
        )

        with open(
            str(ROOT_DIR / "frontend/src/app/routing/app-routing.module.ts"), "w"
        ) as output_file:
            output_file.write(route_template)

    log.info("...%s\n", MSG_OK)


def tsconfig_templating():
    log.info("Generating tsconfig.json")
    with open(str(ROOT_DIR / "frontend/tsconfig.json.sample"), "r") as input_file:
        template = Template(input_file.read())
        tsconfig_templated = template.render(geonature_path=ROOT_DIR)

    with open(str(ROOT_DIR / "frontend/tsconfig.json"), "w") as output_file:
        output_file.write(tsconfig_templated)
    log.info("...%s\n", MSG_OK)


def tsconfig_app_templating(app=None):
    if not app:
        app = get_app_for_cmd(with_external_mods=False)
    log.info('Generating tsconfig.app.json')
    from geonature.utils.env import list_frontend_enabled_modules
    with open(
        str(ROOT_DIR / 'frontend/src/tsconfig.app.json.sample'),
        'r'
    ) as input_file:
        template = Template(input_file.read())
        routes = []
        for url_path, module_code in list_frontend_enabled_modules(app):
            location = Path(GN_EXTERNAL_MODULE / module_code.lower())

            # test if module have frontend
            if (location / 'frontend').is_dir():
                location = '{}/frontend/app'.format(location)
                routes.append(
                    {'location': location}
                )

            # TODO test if two modules with the same name is okay for Angular

        route_template = template.render(routes=routes)

        with open(
            str(ROOT_DIR / 'frontend/src/tsconfig.app.json'), 'w'
        ) as output_file:
            output_file.write(route_template)

    log.info("...%s\n", MSG_OK)


def update_app_configuration(conf_file, prod=True):
    log.info("Update app configuration")
    if prod:
        subprocess.call(["sudo", "supervisorctl", "reload"])
    create_frontend_config(conf_file)
    log.info("...%s\n", MSG_OK)


def create_frontend_config(conf_file):
    """
    Création du fichier de général du frontend (assets/config/config.json)
    en concatenant le fichier de conf général et tous les fichiers de conf des modules
    """
    configs_gn = load_and_validate_toml(conf_file, GnGeneralSchemaConf)
    app = get_app_for_cmd(conf_file)

    path = str(ROOT_DIR / "frontend/src/assets/config/config.json")
    with open(path, "w") as outputfile:
        for module_code, module_conf in get_modules_config(app):
            module_conf = {module_code: module_conf}
            configs_gn = {**configs_gn, **module_conf}
        json.dump(configs_gn, outputfile, indent=True)


def get_modules_config(app):
    """
        Create the frontend config
    """
    from geonature.core.gn_commons.models import TModules

    with app.app_context():

        for module_object in DB.session.query(TModules).filter(
            TModules.module_code != 'GEONATURE').filter(
                TModules.active_frontend == True).all():
            # Import module in sys.path
            try:
                mod_path = os.readlink(
                    str(GN_EXTERNAL_MODULE / module_object.module_code.lower())
                )

                module_parent_dir = str(Path(mod_path).parent)
                module_schema_conf = "{}.config.conf_schema_toml".format(
                    Path(mod_path).name
                )
                sys.path.insert(0, module_parent_dir)
                module = __import__(module_schema_conf, globals=globals())
                front_module_conf_file = os.path.join(
                    mod_path, "config/conf_gn_module.toml"
                )  # noqa
                config_module = load_and_validate_toml(
                    front_module_conf_file,
                    module.config.conf_schema_toml.GnModuleSchemaConf
                )

                # Set id_module and module_code
                config_module["ID_MODULE"] = module_object.id_module
                config_module["MODULE_CODE"] = module_object.module_code
                config_module["MODULE_URL"] = module_object.module_path.rstrip()

                yield module_object.module_code, config_module
            except FileNotFoundError:
                log.info("Skip module {} as its not in external module directory".format(
                    module_object.module_code
                ))
