from invoke import task, run

ENV_TO_APP = {
    'test': 'vbc-test',
    'demo': 'vbc-demo',
    'prod': 'vbc-prod'
}


@task()
def lint(ctx):
    run('yarn run lint')


@task()
def test(ctx):
    run('yarn run test')


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
        run('yarn run build:prod', echo=True)
    elif environment == 'demo':
        run('yarn run build:demo', echo=True)
    else:
        run('yarn run build:dev', echo=True)
    run("gcloud app deploy --project {0} --version {1} {2} --quiet --verbosity=info"
        .format(application, version, '--promote' if set_version else '--no-promote'), echo=True)
