import os
import logging
import json

from windsor.config import current_config
from windsor.utils import run_command


class CDKDependencies:
    """Manage CDK dependencies and its versions for the project. """

    @staticmethod
    def init_cdk(cfg=current_config):
        """Run CDK init using the following arguments.

        `app` the template used to bootstrap the directory structure.

        `--language typescript` language in which cdk will be built.

        After running CDK init it will read the package.json created and get the CDK version to lock in Windsor config.

        :param cfg: Config object to use.
        :type cfg: windsor.config.ConfigBase
        """

        cdk_config_file = os.path.join(os.getcwd(), 'cdk.json')

        cdk_language = cfg.CDKLanguage
        cdk_init_cmd = ['cdk', 'init', 'app', '--language', cdk_language]

        if os.path.isfile(cdk_config_file):
            logging.info('CDK application already created.')
        else:
            logging.info('Creating a new CDK application.')
            run_command(cdk_init_cmd)

        deps_file = CDKDependencies.get_deps_file()
        deps = deps_file.get('dependencies', {})

        cdkversion = None
        for k, v in deps.items():
            if k.startswith('@aws-cdk') and k.endswith('/core'):
                cdkversion = v.replace('^', '')
                break

        if cdkversion is not None:
            logging.info(f'Using CDK version {cdkversion}')
        else:
            cfg.update({
                'CDKVersion': cdkversion
            })

    @staticmethod
    def get_deps_file():
        """Return the CDK dependencies file as a dict. """

        depsfilepath = os.path.join(os.getcwd(), 'package.json')

        if not os.path.isfile(depsfilepath):
            raise Exception(f'File {depsfilepath} not found')

        with open(depsfilepath) as buf:
            depsfile = json.load(buf)

        return depsfile

    @staticmethod
    def lock_version():
        """Lock the current CDK version. """

        cdkver = current_config.CDKVersion
        depsfile = CDKDependencies.get_deps_file()
        deps = depsfile.get('dependencies')

        to_install = []

        for k, v in deps.items():
            if k.startswith('@aws-cdk'):
                if v != cdkver:
                    depname = k.replace('@aws-cdk/', '')
                    to_install.append(depname)

        CDKDependencies.install(*to_install)

    @staticmethod
    def dep_is_installed(dep):
        """Check if dependency is installed already.

        Parameters
        ----------
            dep -> str
                Name of the dependency to check.

        Returns
        -------
            Bool indicating if dependency is installed.
        """

        cdkver = current_config.CDKVersion
        depsfile = CDKDependencies.get_deps_file()
        deps = depsfile.get('dependencies')

        for k, v in deps.items():
            if k.startswith(f'@aws-cdk/{dep}'):
                if v.endswith(cdkver):
                    return True

                return False

        return False

    @staticmethod
    def install(*deps):
        """Install dependencies into the current CDK project.

        All the dependencies will be prefixed with @aws-cdk/
        """

        cdkver = current_config.CDKVersion
        nsdeps = [f'@aws-cdk/{dep}@{cdkver}'
                  for dep in deps
                  if not CDKDependencies.dep_is_installed(dep)]

        if len(nsdeps) == 0:
            return

        strdeps = ' '.join(nsdeps)

        logging.info('The following packages will be installed')
        logging.info(f'{strdeps}')

        install_cmd = ['npm', 'i', *nsdeps]

        run_command(install_cmd)
