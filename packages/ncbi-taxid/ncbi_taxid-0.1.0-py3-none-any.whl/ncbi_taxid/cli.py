import csv
from typing import Optional, TextIO
import sys

import click
from .taxid_utils import TaxIDExpander


@click.command(short_help='Annotate diamond output with taxonomy names')
@click.option('--taxdump_filename', type=click.Path(exists=True, file_okay=True),
              help='Path to local copy of NCBI taxdump.tar.gz file')
@click.option('--taxdb_filename', type=click.Path(),
              help='Name for the processed database, will be loaded if it exists')
@click.option('--diamond_output_format',
              default='6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore slen qlen qcovhsp stitle staxids',
              help='Output format used by DIAMOND (most include staxids)')
@click.option('--output_file', type=click.File('w'), default=sys.stdout,
              help='Output file to write output with expanded taxonomy information (TSV format)')
@click.argument('diamond_output_file', type=click.File())
def annotate_diamond(diamond_output_file: TextIO,
                     diamond_output_format: str,
                     output_file: TextIO,
                     taxdump_filename: Optional[str] = None,
                     taxdb_filename: Optional[str] = None):
    annotater = TaxIDExpander(taxdb_filename=taxdb_filename, taxdump_filename=taxdump_filename)
    assert 'staxids' in diamond_output_format, "The DIAMOND output format must include the staxids column"
    taxid_column = diamond_output_file.split().index('staxids') - 1  # the column position, minus 1 to ignore '6'
    output = csv.writer(output_file, delimiter='\t')
    for row in csv.reader(diamond_output_file, delimiter='\t'):
        taxid = int(row[taxid_column])
        lineage_info = annotater.get_lineage(taxid, only_standard_ranks=True)
        output_row = row + [taxon_info[0] for taxon_info in lineage_info]
        output.write_row(output_row)
    output.close()


if __name__ == '__main__':
    annotate_diamond()  # pylint: disable=E1120
