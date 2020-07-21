import subprocess


class CDKDependencies:
    """Manage CDK dependencies and its versions for the project. """

    @staticmethod
    def install(*deps):
        """Install dependencies into the current CDK project.

        All the dependencies will be prefixed with @aws-cdk/
        """

        nsdeps = [f'@aws-cdk/{dep}' for dep in deps]
        strnsdeps = ' '.join(nsdeps)
        install_cmd = ['npm', 'i', strnsdeps]

        subprocess.call(install_cmd, shell=True)
