from invoke import task, run

# TODO: replace <base-project> with the base project name
ENV_TO_APP = {
    'test': '<base-project>-test',
    'demo': '<base-project>-demo',
    'prod': '<base-project>-prod'
}


@task()
def lint(ctx):
    run('npm run lint')


@task()
def test(ctx):
    run('npm run test')


@task(help={
    'environment': 'The environment to deploy to. Must be one of test, demo or prod.',
    'version': 'The module version.',
    'set-version': 'Whether or not to set the default version of the modules to the deployed version'
})
def deploy(ctx, environment, version, set_version=False):
    application = ENV_TO_APP.get(environment)
    if not application:
        raise ValueError('Invalid environment. Must be one of test, demo, or prod.')
    if environment == 'prod':
        run('npm run build:prod', echo=True)
    elif environment == 'demo':
        run('npm run build:demo', echo=True)
    else:
        run('npm run build:dev', echo=True)
    run("gcloud app deploy --project {0} --version {1} {2} --quiet --verbosity=info"
        .format(application, version, '--promote' if set_version else '--no-promote'), echo=True)
