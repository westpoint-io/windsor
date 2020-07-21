import subprocess


class CDKDependencies:
    @staticmethod
    def install(*deps):
        nsdeps = [f'@aws-cdk/{dep}' for dep in deps]
        strnsdeps = ' '.join(nsdeps)
        install_cmd = ['npm', 'i', strnsdeps]

        subprocess.call(install_cmd, shell=True)
