#!/usr/bin/env python3
import click
import os
import zipfile
import tempfile
import shutil
import urllib.request
from redminelib import Redmine

# https://stackoverflow.com/a/1855118/1249951
def zipdir(path, ziph):
  # ziph is zipfile handle
  for root, dirs, files in os.walk(path):
    for file in files:
      p = os.path.join( root[len(path):], file) # remove "root folder"
      ziph.write(os.path.join(root, file), p)

def load_redmine_config(base, key):
  opts = {}
  if base and key:
    opts['url'] = base
    opts['key'] = key
  else:
    f = open(os.path.join('.', '.redart'), 'r')
    opts['url'] = f.read()
    f.close()
    f = open(os.path.join('.', '.redart-auth'), 'r')
    opts['key'] = f.read()
    f.close()
  return opts

def get_redmine(base, key):
  conf = load_redmine_config(base, key)
  return Redmine(conf['url'], key= conf['key'])

def get_redmine_spec(spec, redmine):
  path, version_name_tag = spec.split(':')
  prj, fn = path.split('/')
  versions = redmine.version.filter(project_id = prj)
  version_id = None
  version_name = None
  for version in versions:
    if version.name == version_name_tag:
      version_id = version.id
      version_name = version.name
  return {'project': prj, 'filename': fn, 'version_name': version_name, 'version_id': version_id}

def get_existing_file(spec, redmine):
  existing_file = None
  existing_files = redmine.file.filter(project_id=spec['project'], version_id=spec['version_id'])
  for f in existing_files:
    if not hasattr(f, 'version'):
      continue
    if f.filename == spec['filename'] and f.version.id == spec['version_id']:
      existing_file = f

  return existing_file

@click.group()
def cli():
  pass

# -------------------------------- PUBLISH ------------------------------------------

@click.command()
@click.option('--compress/--no-compress', default=False, help='Whether the folder should be zipped before upload or not.')
@click.option('--force/--no-force', default=False, help='When a file exists with matching filename and version_id, overwrite it automatically.')
@click.option('--redmine-base', default=None, help='The base URL for your redmine instance. (optional, can be specified via *init*)')
@click.option('--redmine-key', default=None, help='The API access key of your account. (optional, can be specified via *init*)')
@click.argument('redmine_spec')
@click.argument('folder_or_file')
def pub(compress, force, redmine_spec, folder_or_file, redmine_base, redmine_key):
  source_file = None
  tmpdir = None
  redmine = get_redmine(redmine_base, redmine_key)
  spec = get_redmine_spec(redmine_spec, redmine)
  
  if compress:
    # https://stackoverflow.com/a/11967760/1249951
    tmpdir = tempfile.mkdtemp() 
    source_file = os.path.join(tmpdir, 'tmp.zip')
    zipf = zipfile.ZipFile(source_file, 'w', zipfile.ZIP_DEFLATED)
    zipdir(folder_or_file, zipf)
    zipf.close()
  else:
    source_file = os.path.join('.', folder_or_file)

  
  click.echo('Uploading the artifact %s in project %s for version %s (%s) ...' % (
    spec['filename'],
    spec['project'],
    spec['version_name'],
    spec['version_id']
  ))

  # Handle Existing File:
  existing_file = get_existing_file(spec, redmine)

  if existing_file and force==False:
    click.confirm('An existing file has been found, do you want to overwrite it?', abort=True)

  if existing_file:
    redmine.file.delete(existing_file.id)
  
  # Now create the File
  redmine.file.create(
    project_id = spec['project'],
    path = source_file,
    filename = spec['filename'],
    description = '',
    version_id = spec['version_id']
  )

  # Cleaning up:
  if tmpdir:
    shutil.rmtree(tmpdir)

  click.echo('Done.')


# -------------------------------- FETCH --------------------------------------------

@click.command()
@click.option('--extract/--no-extract', default=False, help='Whether to extract the specified artifact into the target folder or not')
@click.option('--target-name', default=None, help='The new filename, after the artifact has been downloaded (ignored when using --extract)')
@click.option('--redmine-base', default=None, help='The base URL for your redmine instance. (optional, can be specified via *init*)')
@click.option('--redmine-key', default=None, help='The API access key of your account. (optional, can be specified via *init*)')
@click.argument('redmine_spec')
@click.argument('target_folder')
def fetch(extract, target_name, redmine_spec, target_folder, redmine_base, redmine_key):
  redmine = get_redmine(redmine_base, redmine_key)
  spec = get_redmine_spec(redmine_spec, redmine)
  existing_file = get_existing_file(spec, redmine)

  if not existing_file:
    click.echo('Error: The specified artifact could not be found.')
    exit(1)

  tmpdir = tempfile.mkdtemp()
  tmpfile = os.path.join(tmpdir, spec['filename'])

  target_dir = os.path.join(target_folder)
  click.echo("Downloading artifact %s to %s ..." % (spec['filename'], target_dir))
  rconf = load_redmine_config(redmine_base, redmine_key)
  url = "%s?key=%s" % (existing_file.content_url, rconf['key'])
  with urllib.request.urlopen(url) as response, open(tmpfile, 'wb') as out_file:
    shutil.copyfileobj(response, out_file)

  if extract:
    click.echo(' + ... extracting ...')
    zip_ref = zipfile.ZipFile(tmpfile, 'r')
    zip_ref.extractall(target_dir)
    zip_ref.close()
  else:
    shutil.copyfile(tmpfile, os.path.join(target_dir, target_name or spec['filename']))

  shutil.rmtree(tmpdir)
  click.echo('Done.')


# -------------------------------- INIT ---------------------------------------------

@click.command()
@click.option('--redmine', default=None, help='The base URL for your redmine instance.')
@click.option('--key', default=None, help='The API access key of your account')
def init(redmine, key):
  click.echo('+ Storing base url to .redart ...')
  f = open(os.path.join('.', '.redart'), 'w')
  f.write(redmine)
  f.close()

  click.echo('+ Storing your auth key to .redart-auth ...')
  f = open(os.path.join('.', '.redart-auth'), 'w')
  f.write(key)
  f.close()

  click.echo('')
  click.echo('Info: make sure to ignore .redart-auth in your version control tool.')



# -------------------------------- MAIN ---------------------------------------------

cli.add_command(pub)
cli.add_command(fetch)
cli.add_command(init)

if __name__ == "__main__":
  cli()