import os
import subprocess
import json

from windsor.config import current_config


class CDKDependencies:
    """Manage CDK dependencies and its versions for the project. """

    @staticmethod
    def init_cdk():
        """Run CDK init using the following arguments.

        `app` the template used to bootstrap the directory structure.

        `--language typescript` language in which cdk will be built.
        """

        cdk_language = current_config.language
        cdk_init_cmd = ['cdk', 'init', 'app', '--language', cdk_language]

        subprocess.call(cdk_init_cmd, shell=True)

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
    def check_version():
        """Check the version being used on CDK core. """

        depsfile = CDKDependencies.get_deps_file()
        deps = depsfile.get('dependencies')
        cdkver = deps.get('@aws-cdk/core')

        return cdkver

    @staticmethod
    def lock_version():
        """Lock the current CDK version. """

        cdkver = CDKDependencies.check_version()
        depsfile = CDKDependencies.get_deps_file()
        deps = depsfile.get('dependencies')

        for k, v in deps.items():
            if k.startswith('@aws-cdk'):
                if v != cdkver:
                    CDKDependencies.install(k.replace('@aws-cdk/', ''))

    @staticmethod
    def install(*deps):
        """Install dependencies into the current CDK project.

        All the dependencies will be prefixed with @aws-cdk/
        """

        cdkver = CDKDependencies.check_version()
        nsdeps = [f'@aws-cdk/{dep}@{cdkver}' for dep in deps]
        install_cmd = ['npm', 'i', *nsdeps]

        subprocess.call(install_cmd, shell=True)
