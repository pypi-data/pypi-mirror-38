'''
A quick script to generate a BED file for masking plasmids
'''

import gzip
import pathlib
import click
from Bio import SeqIO

from mask_plasmid import __version__ as VERSION


def parse_record(record):
    '''
    A function to parse a record and return a BED line
    '''
    rec_length = len(record)
    rec_id = record.id
    print(f"{rec_id}\t1\t{rec_length}")


def print_version(ctx, param, value):
    '''
    Print version
    '''
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"mask-plasmid {VERSION}")
    ctx.exit()


@click.command()
@click.option('--version', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option("--format", default="genbank", help="Input file format", show_default=True)
@click.argument("filename")
def run_mask(format, filename):
    '''
    Take a file (`in`) with multiple sequence records (e.g., Genbank) and output a 
    BED file with the coordinates of each record.
    '''
    fn = pathlib.Path(filename)
    cmd = gzip.open if fn.suffix in ['.gz'] else open
    with cmd(filename, mode='rt') as f:
        for record in SeqIO.parse(f, format):
            parse_record(record)
