import click
import download as dl

@click.group()
def main():
    """
    a CLI tool for packaging patches from CommunityDragon
    """
    pass

@main.command()
@click.argument('patch')
@click.option('--path', type=str, default='.export', show_default=True)
def download(patch, path):
  """
  downloads a patch from the CommunityDragon and DataDragon server
  """
  dl.download(patch, path)

if __name__ == "__main__":
    main()